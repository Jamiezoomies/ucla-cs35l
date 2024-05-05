#ifndef OPTIONS_H
#define OPTIONS_H
#include <stdbool.h>

typedef struct {
    bool valid;
    long long nbytes;

    char *input_option; // Input option: "rdrand", "lrand48_r", or file path
    char *output_option; // Output option: "stdio" or number of bytes as string
    int output_block_size;
} Options;

Options parse_options(int argc, char **argv);

#endif