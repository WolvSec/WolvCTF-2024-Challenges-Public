#include "engine.h"


uint32_t execute(command_t *command, std::vector<void *> &allocations) {
    switch (command->command) {
        case STORE:
        {
            allocations.push_back(command->arg1);
            return allocations.size() - 1;
            break;
        }
        case RELEASE:
            free(allocations[(size_t)command->arg1]);
            return 0;
            break;
        case CLEAR:
        {
            for (size_t i = 0; i < allocations.size(); i++) {
                free((void *)allocations[i]);
            }
            allocations.clear();
            return 0;
            break;
        }
        default:
            return 0;
            break;
    }
}
