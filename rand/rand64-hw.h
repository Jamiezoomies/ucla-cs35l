#ifndef RAND64_HW_H
#define RAND64_HW_H
#include <stdbool.h>

// Initializes the hardware RNG.
void hardware_rand64_init(void);

// Returns a random value using hardware operations.
unsigned long long hardware_rand64(void);

// Finalizes the hardware RNG.
void hardware_rand64_fini(void);

// Checks if the CPU supports RDRAND instruction.
_Bool rdrand_supported(void);

#endif