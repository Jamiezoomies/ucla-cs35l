#ifndef OUTPUT_H
#define OUTPUT_H
#include <stdbool.h>

bool writebytes(unsigned long long x, int nbytes);
bool write_N_bytes(unsigned long long x, int nbytes, int N);

#endif