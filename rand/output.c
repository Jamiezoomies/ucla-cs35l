#include "output.h"
#include <errno.h>
#include <limits.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

bool writebytes (unsigned long long x, int nbytes)
{
    do
    {
        if (putchar (x) < 0)
	        return false;
        x >>= CHAR_BIT;
        nbytes--;
    }
    while (0 < nbytes);

    return true;
}

bool write_N_bytes(unsigned long long x, int nbytes, int N) {
    // Allocates memory for a buffer of size N bytes
    unsigned char* buffer = malloc(N * sizeof(unsigned char));
    if (!buffer) {
        perror("Failed to allocate memory for output buffer");
        return false;
    }

    // Iterates over each byte of the nbytes data and fills the buffer 
    for (int i = 0; i < nbytes; ++i) {
        buffer[i % N] = (x >> (i * CHAR_BIT)) & 0xFF;

        // When buffer is full or on the last iteration, write out
        if ((i % N == N - 1) || (i == nbytes - 1)) {
            if (write(STDOUT_FILENO, buffer, (i % N) + 1) == -1) {
                perror("Failed to write to stdout");
                free(buffer);
                return false;
            }
        }
    }

    free(buffer);
    return true;
}