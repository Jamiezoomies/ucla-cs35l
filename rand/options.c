#include "options.h"
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

Options parse_options(int argc, char **argv) {
    // Initialize options
    Options opts = {0};
    // Defaults
    opts.input_option = "rdrand";
    opts.output_option = "stdio";
    opts.output_block_size = 0;


    // Read options using getopt
    int opt;
    while ((opt = getopt(argc, argv, "i:o:")) != -1) {
        switch (opt) {
            case 'i':
                opts.input_option = optarg;
                break;
            case 'o':
                opts.output_option = optarg;
                // If optarg is a number, parse it for block size
                if (strcmp(optarg, "stdio") != 0) {
                    opts.output_block_size = atoi(optarg);
                    if (opts.output_block_size <= 0) {
                        fprintf(stderr, "Invalid block size: %s\n", optarg);
                        opts.valid = false;
                        return opts;
                    }
                }
                break;
            default:
                // Unrecognized options
                fprintf(stderr, "Usage: %s [-i input] [-o output] nbytes\n", argv[0]);
                opts.valid = false;
                return opts;
        }
    }

    // After processing all options, it checks for additional non-option arguments
    if (optind < argc) {
        opts.nbytes = atoll(argv[optind]);
        if (opts.nbytes > 0) {
            opts.valid = true;
        } else {
            fprintf(stderr, "Invalid number of bytes: %s\n", argv[optind]);
            opts.valid = false;
        }
    } else {
        fprintf(stderr, "Missing nbytes argument\n");
        opts.valid = false;
    }

    return opts;
}