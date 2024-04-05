
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
    char buffer[48];
    if (argc != 3) {
        printf("[wolphvlog] usage: %s <infile> <ofile>", argv[0]);
        return 1;
    }

    FILE* infile = fopen(argv[1], "r");
    fread(buffer, sizeof(char), 48, infile);

    for (int i = 0; i < 12; ++i) {
        uint32_t* p = (uint32_t*)(buffer + (i * 4));
        *p = (*p << 13) | ((*p >> 19));
    }

    FILE* outfile = fopen(argv[2], "wb");
    fwrite(buffer, sizeof(char), 48, outfile);
}

