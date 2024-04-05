#include <stdbool.h>
#include <unordered_map>
#include <utility>
#include <vector>
#include <string>
#include <algorithm>

#include "engine.h"
#include <fcntl.h>
#include <unistd.h>

#define DEBUG 0

#define COMMENT '#'

#define TERMINATOR '\n'

std::unordered_map<std::string, uint32_t> variables;

std::vector<void *> allocations;  // Level 1 only

void skip_whitespace_and_comments(uint8_t *&line){
    while (*line == ' ' || *line == '\t' || *line == COMMENT) {
        if (*line == COMMENT) {
            while (*line != TERMINATOR && *line != '\r' && *line != '\0') {
                line++;
            }
        }
        line++;
    }
}

uint8_t *advance_to_first_argument(uint8_t *line) {
    while (*(line++) != '(') {}
    return line;
}

bool is_assignment(uint8_t *line) {
    return strstr((const char *)line, "=") != NULL;
}

uint8_t * get_variable_name(uint8_t *line, uint8_t *dst) {
    // skip whitespace
    while (*(line) == ' ') {
        line++;
    }
    if (!isalpha(*line)) {
        printf("Syntax error: invalid variable name\n");
        return line;
    }
    while (*(line) != '=' && *(line) != ' ') {
        if (!isalnum(*line)) {
            printf("Syntax error: invalid variable name\n");
            return line;
        }
        *dst = *line;
        dst++;
        line++;
    }
    // skip whitespace
    while (*(line) == ' ') {
        line++;
    }
    if (*(line++) != '=') {
        printf("Syntax error: expected '='\n");
        return line;
    }
    // skip whitespace
    while (*(line) == ' ') {
        line++;
    }
    return line;
}

void custom_free(uint32_t id){
    command_t command;
    command.command = RELEASE;
    object_t *obj_ptr = (object_t *)allocations[id];
    if (obj_ptr->type == STRING || obj_ptr->type == INTEGER) {
        if (DEBUG && obj_ptr->type == STRING)
            printf("Id: %d Contents: %s\n", id, obj_ptr->data);
        else if (DEBUG && obj_ptr->type == INTEGER)
            printf("Contents: %d\n", *(int *)obj_ptr->data);
        free(obj_ptr->data);
    }
    void *temp = (void *)(uint64_t)id;
    command.arg1 = temp;
    if (DEBUG)
        printf("Command: %d, Arg1: %p\n", command.command, temp);
    execute(&command, allocations);
    // Iterate through variables and remove the one we just freed and if it is in other variables
    for (auto it = variables.begin(); it != variables.end();) {
        if (it->second == (uint64_t)temp) { 
            variables.erase(it++);
        }
        else {
            ++it;
        }
    }
}

void custom_alloc(object_t *obj_ptr, uint8_t *var, bool doing_free) {
    uint32_t id = 0;
    command_t command;
    command.command = STORE;
    command.arg1 = (void *)obj_ptr;
    if(DEBUG)
        printf("Command: %d, Arg1: %p, Len: %ld, Type: %d\n", command.command, command.arg1, obj_ptr->size, obj_ptr->type);
    if (doing_free) {
        id = variables[std::string((char *)var)];
    }
    if (DEBUG)
        printf("num_allocations: %ld\n", allocations.size());
    if (doing_free) {
        if (DEBUG)
            printf("doing free\n");
        custom_free(id);
    }
    if (DEBUG) {
        printf("new id: %d\n", variables[std::string((char *)var)]);
        printf("free id: %d\n", id);
        if (obj_ptr->type == STRING)
            printf("Contents: %s\n", obj_ptr->data);
        else if (obj_ptr->type == INTEGER)
            printf("Contents: %d\n", *(int *)obj_ptr->data);
    }
    variables[std::string((char *)var)] = execute(&command, allocations);
    if (DEBUG)
        printf("Allocated %ld bytes for %s at %p id: %d type: %d\n", obj_ptr->size, var, allocations[variables[std::string((char *)var)]], variables[std::string((char *)var)], obj_ptr->type);
}

std::vector<std::pair<object_t *, uint8_t *>> arg_parse(uint8_t *line, char separator, char terminator, bool dereference) {
    // get number of characters until separator or terminator
    int arg = 0;
    uint32_t len = 0;
    std::vector<std::pair<object_t *, uint8_t *>> args;
    // skip whitespace
    skip_whitespace_and_comments(line);
    if (*line == terminator || *line == separator || *line == TERMINATOR) {
        return {std::make_pair((object_t *)NULL, line)};
    }
    while (line[++len] != terminator && line[len] != TERMINATOR);
    while (*line != terminator && *line != TERMINATOR) {
        skip_whitespace_and_comments(line);
        if (*line == TERMINATOR) {
            printf("Syntax error: unexpected end of statement\n");
            return {std::make_pair((object_t *)NULL, line)};
        }
        char *arg_str = (char *)malloc(len + 1); // TODO: free this
        memset(arg_str, 0, len + 1);
        bool arg_is_integer = isdigit(*line) || (line[0] == '-' && isdigit(line[1]));
        bool arg_is_string = *line == '"';

        if (arg_is_string)
            line++;

        size_t arg_len = 0;
        bool copy_mode = true;
        while (*line != separator && *line != TERMINATOR && *line != terminator) {
            if (!arg_is_string && *line == ' ') {
                skip_whitespace_and_comments(line);
                break;
            }
            if (arg_is_integer && !isdigit(*line) && !(*line == '-' && arg_len == 0)) {
                printf("Syntax error: invalid number\n");
                return {std::make_pair((object_t *)NULL, line)};
            }
            if (arg_is_string && *line == '"') {
                copy_mode = false;
                line++;
                continue;
            }
            if (copy_mode) {
                arg_str[arg_len++] = *line++;
            }
            else
                line++;
        }
        if (!(*line == separator || separator == '\0') && !(*line == terminator || terminator == '\0')) {
            if (dereference)
                printf("Syntax error: expected '%c'\n", terminator);
            free(arg_str);
            return {std::make_pair((object_t *)NULL, line)};
        }
        line++;
        // check if boolean
        if (strcmp(arg_str, "true") == 0) {
            object_t *obj_ptr = (object_t *)malloc(sizeof(object_t));
            obj_ptr->type = BOOLEAN;
            obj_ptr->size = 1;
            obj_ptr->print = NULL;
            obj_ptr->data = (uint8_t *)malloc(sizeof(bool));
            *(bool *)obj_ptr->data = true;
            args.push_back(std::make_pair(obj_ptr, line));
        }
        else if (strcmp(arg_str, "false") == 0) {
            object_t *obj_ptr = (object_t *)malloc(sizeof(object_t));
            obj_ptr->type = BOOLEAN;
            obj_ptr->size = 1;
            obj_ptr->print = NULL;
            obj_ptr->data = (uint8_t *)malloc(sizeof(bool));
            *(bool *)obj_ptr->data = false;
            args.push_back(std::make_pair(obj_ptr, line));
        }
        else if (!arg_is_string && !arg_is_integer) {
            if (!dereference) {
                object_t *obj_ptr = (object_t *)malloc(sizeof(object_t));
                obj_ptr->type = OBJECT;
                obj_ptr->size = arg_len + 1;
                obj_ptr->print = NULL;
                obj_ptr->data = (uint8_t *)malloc(obj_ptr->size);
                memcpy(obj_ptr->data, arg_str, obj_ptr->size);
                args.push_back(std::make_pair(obj_ptr, line));
            }
            // look up variable
            else {
                if (variables.find(std::string(arg_str)) == variables.end()) {
                    printf("Syntax error: unknown variable\n");
                    free(arg_str);
                    return {std::make_pair((object_t *)NULL, line)};
                }
                object_t *obj_ptr = (object_t *)allocations[variables[std::string(arg_str)]];
                args.push_back(std::make_pair(obj_ptr, line));
            }
        }
        else if (arg_is_integer) {
            if (arg_str[0] == '-') {
                arg = atoi(arg_str + 1) * -1;
            }
            else {
                arg = atoi(arg_str);
            }
            object_t *obj_ptr = (object_t *)malloc(sizeof(object_t));
            obj_ptr->type = INTEGER;
            obj_ptr->size = sizeof(int);
            obj_ptr->print = NULL;
            obj_ptr->data = (uint8_t *)malloc(sizeof(int));
            memset(obj_ptr->data, 0, sizeof(int));
            memcpy(obj_ptr->data, &arg, sizeof(int));
            args.push_back(std::make_pair(obj_ptr, line));
        }
        else if (arg_is_string) {
            // dump arg_str as hex
            object_t *obj_ptr = (object_t *)malloc(sizeof(object_t));
            obj_ptr->type = STRING;
            obj_ptr->print = NULL;
            obj_ptr->size = arg_len + 1;
            obj_ptr->data = (uint8_t *)malloc(obj_ptr->size);
            memset(obj_ptr->data, 0, obj_ptr->size);
            memcpy(obj_ptr->data, arg_str, obj_ptr->size);
            args.push_back(std::make_pair(obj_ptr, line));
        }
        else {
            free(arg_str);
            return {std::make_pair((object_t *)NULL, line)};
        }
        free(arg_str);
        if (*((char *)line - 1) == terminator || *((char *)line - 1) == TERMINATOR) {
            break;
        }
    }
    return args;
}

bool validate_var_name(char *var) {
    if (!isalpha(var[0])) {
        return false;
    }
    for (size_t i = 1; i < strlen(var); i++) {
        if (!isalnum(var[i])) {
            return false;
        }
    }
    return true;
}

void run_line(uint8_t *line) {
    bool doing_assignment = false;
    auto var = arg_parse(line, ',', '=', false)[0];
    auto var_iter = variables.begin();
    if (var.first != NULL) {
        var_iter = variables.find(std::string((char *)var.first->data));
        if (DEBUG)
            if (var_iter != variables.end())
                printf("freeing %s\n", var.first->data);
        doing_assignment = true;
        line = var.second;
    }
    auto test_var = arg_parse(line, '\0', ')', false)[0];
    if (test_var.first == NULL) {
        goto exit;
    }
    if (doing_assignment && DEBUG)
        printf("var->data: %s\n", var.first->data);

    
    // skip whitespace
    skip_whitespace_and_comments(line);
    if (DEBUG)
        printf("Line: %s\n", line);
    if (!strncmp((const char *)line, "Store", strlen("Store")) && doing_assignment) {
        if (!validate_var_name((char *)var.first->data)) {
            printf("Invalid variable name: %s\n", var.first->data);
            goto exit;
        }
        line += strlen("Store");
        skip_whitespace_and_comments(line);
        if (line[0] != '(') {
            printf("Syntax error: expected '('\n");
            goto exit;
        }
        line++;
        auto obj = arg_parse(line, ',', ')', false)[0];
        if (obj.first == NULL) {
            printf("Syntax error: expected valid argument\n");
            goto exit;
        }
        if (DEBUG) {
            if (obj.first->type == STRING)
                printf("obj->data (string): %s\n", obj.first->data);
            else if (obj.first->type == INTEGER)
                printf("obj->data (integer): %d\n", *(int *)obj.first->data);
            else if (obj.first->type == BOOLEAN)
                printf("obj->data (boolean): %s\n", obj.first->data);
            else if (obj.first->type == OBJECT)
                printf("obj->data (object): %s\n", obj.first->data);
        }
        if (obj.first->type == OBJECT) {
            if (variables.find(std::string((char *)obj.first->data)) == variables.end()) {
                printf("Unknown variable: %s\n", obj.first->data);
                free(obj.first);
                goto exit;
            }
            // create new object for deepcopy
            std::string key = std::string((char *)obj.first->data);
            free(obj.first);
            object_t *old_obj = (object_t *)allocations[variables[key]];
            void *buffer = malloc(old_obj->size);
            object_t *new_obj = (object_t *)malloc(sizeof(object_t));
            new_obj->type = old_obj->type;
            new_obj->size = old_obj->size;
            new_obj->print = old_obj->print;
            new_obj->data = (uint8_t *)buffer;
            memcpy(new_obj->data, old_obj->data, old_obj->size);
            if (DEBUG)
                printf("new_obj->data: %s\n", new_obj->data);
            obj.first = new_obj;
        }
        custom_alloc(obj.first, var.first->data, var_iter != variables.end());
        if (DEBUG)
            printf("Data: %p\n", obj.first->data);  // used to backdoor
    }
    else if (!strncmp((const char *)line, "Release", strlen("Release"))) {
        line += strlen("Release");
        skip_whitespace_and_comments(line);
        if (line[0] != '(') {
            printf("Syntax error: expected '('\n");
            goto exit;
        }
        line++;
        auto obj = arg_parse(line, ',', ')', false)[0];
        if (obj.first != NULL) {
            if (variables.find(std::string((char *)obj.first->data)) == variables.end()) {
                printf("Syntax error: unknown variable\n");
                free(obj.first);
                goto exit;
            }
            if (DEBUG)
                printf("freeing %s with id %d\n", obj.first->data, variables[std::string((char *)obj.first->data)]);
            custom_free(variables[std::string((char *)obj.first->data)]);
            free(obj.first);
        }
        else {
            printf("Syntax error: expected argument\n");
            goto exit;
        }
    }
    else if (!strncmp((const char *)line, "Print", strlen("Print"))) {
        line += strlen("Print");
        skip_whitespace_and_comments(line);
        if (line[0] != '(') {
            printf("Syntax error: expected '('\n");
            goto exit;
        }
        line++;
        auto obj_ptr = arg_parse(line, ',', ')', true)[0].first;
        if (obj_ptr == NULL)
            goto exit;

        if (DEBUG) {
            // Dump all bytes related to obj_ptr in hex
            for (size_t i = 0; i < sizeof(object_t); i++) {
                printf("%02x ", ((uint8_t *)obj_ptr)[i]);
            }
            printf("\n");
        }
        if (obj_ptr->print != NULL) {
            asm("mov %0, %%rbx" : : "r"(obj_ptr->size));
            obj_ptr->print(obj_ptr->data);
        }
        else if (obj_ptr->type == STRING) {
            printf("%s\n", obj_ptr->data);
        }
        else if (obj_ptr->type == INTEGER) {
            printf("%d\n", *(int *)obj_ptr->data);
        }
        else if (obj_ptr->type == BOOLEAN) {
            printf("%d\n", *(uint8_t *)obj_ptr->data);
        }
        else {
            printf("Unknown type\n");
        }
        if (DEBUG)
            printf("Command: %d, Arg1: %s, Len: %ld\n", PRINT, obj_ptr->data, obj_ptr->size);
        if (std::find(allocations.begin(), allocations.end(), obj_ptr) == allocations.end()) {
            free(obj_ptr->data);
            free(obj_ptr);
        }
    }
    else if (strchr((char *)line, '+') != NULL && doing_assignment) {
        size_t len = strlen((const char *)line);
        auto temp = arg_parse(line, '+', '\n', true);
        object_t *result = temp[0].first;
        if (temp.size() < 2) {
            printf("Syntax error: expected at least 2 arguments\n");
            goto exit;
        }
        for (size_t i = 1; i < temp.size(); i++) {
            // Actually do the addition
            if ((result->type == INTEGER || result->type == BOOLEAN) && 
                (temp[i].first->type == INTEGER || temp[i].first->type == BOOLEAN)) {
                int arg1 = 0;
                int arg2 = 0;
                int type = BOOLEAN;
                size_t size = sizeof(bool);
                if (temp[i].first->type == INTEGER) {
                    arg1 = *(int *)temp[i].first->data;
                    type = INTEGER;
                    size = sizeof(int);
                }
                else if (temp[i].first->type == BOOLEAN) {
                    arg1 = *(uint8_t *)temp[i].first->data;
                }
                if (result->type == INTEGER) {
                    arg2 = *(int *)result->data;
                    type = INTEGER;
                    size = sizeof(int);
                }
                else if (result->type == BOOLEAN) {
                    arg2 = *(uint8_t *)result->data;
                }
                int add_result = arg1 + arg2;
                void (*old_print)(void *) = result->print;
                if (std::find(allocations.begin(), allocations.end(), result) == allocations.end()) {
                    free(result->data);
                    free(result);
                }
                if (std::find(allocations.begin(), allocations.end(), temp[i].first) == allocations.end()) {
                    free(temp[i].first->data);
                    free(temp[i].first);
                }
                // Store result in variable
                result = (object_t *)malloc(sizeof(object_t));
                memset(result, 0, sizeof(object_t));
                result->size = size;
                result->type = type;
                result->data = (uint8_t *)malloc(size);
                result->print = old_print;
                memset(result->data, 0, size);
                memcpy(result->data, &add_result, size);
            }
            // treat integer and string addition like string and string addition
            else if (
                (result->type == INTEGER || result->type == STRING || result->type == BOOLEAN) && 
                (temp[i].first->type == INTEGER || temp[i].first->type == STRING || temp[i].first->type == BOOLEAN)
            ) {
                char *add_result = NULL;
                char *arg1_str = NULL;
                char *arg2_str = NULL;

                if (result->type == BOOLEAN) {
                    arg1_str = (char *)malloc(len);
                    memset(arg1_str, 0, len);
                    sprintf(arg1_str, "%d", *(bool *)result->data);
                }
                else if (result->type == INTEGER) {
                    arg1_str = (char *)malloc(len);
                    memset(arg1_str, 0, len);
                    sprintf(arg1_str, "%d", *(int *)result->data);
                }
                else {
                    arg1_str = (char *)malloc(result->size + 1);
                    memset(arg1_str, 0, result->size + 1);
                    memcpy(arg1_str, result->data, result->size);
                }
                if (temp[i].first->type == BOOLEAN) {
                    arg2_str = (char *)malloc(len);
                    memset(arg2_str, 0, len);
                    sprintf(arg2_str, "%d", *(bool *)temp[i].first->data);
                }
                else if (temp[i].first->type == INTEGER) {
                    arg2_str = (char *)malloc(len);
                    memset(arg2_str, 0, len);
                    sprintf(arg2_str, "%d", *(int *)temp[i].first->data);
                }
                else {
                    arg2_str = (char *)malloc(temp[i].first->size + 1);
                    memset(arg2_str, 0, temp[i].first->size + 1);
                    memcpy(arg2_str, temp[i].first->data, temp[i].first->size);
                }
                if (std::find(allocations.begin(), allocations.end(), result) == allocations.end()) {
                    free(result->data);
                    free(result);
                }
                // This allows a use after free.
                // What the code should be:
                // if (std::find(allocations.begin(), allocations.end(), temp[i].first) == allocations.end()) {
                //     free(temp[i].first->data);
                //     free(temp[i].first);
                // }
                free(temp[i].first->data);
                free(temp[i].first);
                add_result = (char *)malloc(strlen(arg1_str) + strlen(arg2_str) + 1);
                memset(add_result, 0, strlen(arg1_str) + strlen(arg2_str) + 1);
                void (*old_print)(void *) = result->print;
                strcat(add_result, arg1_str);
                strcat(add_result, arg2_str);
                if (DEBUG)
                    printf("Result: %s\n", add_result);

                // Store result in variable
                result = (object_t *)malloc(sizeof(object_t));
                memset(result, 0, sizeof(object_t));
                result->size = strlen(add_result);
                result->type = STRING;
                result->print = old_print;
                result->data = (uint8_t *)add_result;
                free(arg1_str);
                free(arg2_str);
            }
            else {
                printf("Syntax error: invalid type\n");
                goto exit;
            }
        }
        custom_alloc(result, var.first->data, var_iter != variables.end());
    }
    else if (doing_assignment) {
        if (!validate_var_name((char *)var.first->data)) {
            printf("Syntax error: invalid variable name\n");
            goto exit;
        }
        auto obj = arg_parse(line, '\0', TERMINATOR, false)[0];
        if (obj.first == NULL) {
            printf("Syntax error: invalid assignment\n");
            goto exit;
        }
        if (variables.find(std::string((char *)var.first->data)) != variables.end()) {
            printf("Syntax error: variable already exists\n");
            goto exit;
        }
        if (variables.find(std::string((char *)obj.first->data)) != variables.end()) {
            variables[std::string((char *)var.first->data)] = variables[std::string((char *)obj.first->data)];
        }
        else {
            printf("Syntax error: unknown variable %s\n", line);
            goto exit;
        }
    }
    else {
        if (DEBUG)
            printf("DBG Line: %s\n", line);
    }
exit:
    free(var.first);
}

void print_heap_line() {
    int mapsfd = open("/proc/self/maps", O_RDONLY);
    if(mapsfd == -1) {
        fprintf(stderr, "open() failed: %s.\n", strerror(errno));
        exit(1);
    }
    char maps[BUFSIZ] = "";
    if(read(mapsfd, maps, BUFSIZ) == -1){
        fprintf(stderr, "read() failed: %s.\n", strerror(errno));
        exit(1);
    }
    if(close(mapsfd) == -1){
        fprintf(stderr, "close() failed: %s.\n", strerror(errno));
        exit(1);
    }

    char* line = strtok(maps, "\n");
    while((line = strtok(NULL, "\n")) != NULL) {
        if(strstr(line, "heap") != NULL) {
            void* heap_base;
            sscanf(line, "%p", &heap_base);
            printf("Heap base: %p\n", heap_base);
        }
    }
}

int main(int argc, char **argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    print_heap_line();

    FILE *fd;
    if (argc == 2) {
        // Parse lines from source file
        fd = fopen(argv[1], "r");
        if (fd == NULL) {
            printf("Failed to open source file\n");
            return 1;
        }
    }
    else if (argc == 1) {
        // Parse lines from stdin
        fd = stdin;
    }
    else {
        printf("Usage: %s [source file]\n", argv[0]);
        return 1;
    }
    
    // Parse line to run from source file (up to newline)
    char *line = NULL;
    size_t len = 0;
    ssize_t fs;
    if (argc == 1) {
        printf(">> ");
        fflush(stdout);
    }
    while ((fs = getline(&line, &len, fd)) != -1) {
        if (line[fs - 1] == TERMINATOR || line[fs - 1] == '\r' || line[fs - 1] == EOF)
            line[fs - 1] = (uint8_t)TERMINATOR;
        run_line((uint8_t *)line);
        if (argc == 1) {
            printf(">> ");
            fflush(stdout);
        }
    }   
    return 0;
}
