#include "rand64-lrand48.h"
#include <stdlib.h>
#include <time.h>   

void lrand48_rand64_init(void) {
    // Seed the pseudo-random generator.
    srand48(time(NULL));
}

unsigned long long lrand48_rand64(void) {
    // Generate 64-bit random value by combining two 32-bit values from lrand48()
    // lrand48() twice to generate high and low parts. 
    unsigned long long high = lrand48();
    unsigned long long low = lrand48();
    // shifts high left by 32 bits and combines it with low to form the 64-bit result.
    return (high << 32) | low;
}

void lrand48_rand64_fini(void) {
}
