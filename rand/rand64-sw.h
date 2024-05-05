#ifndef RAND64_SW_H
#define RAND64_SW_H

// Initializes the software RNG.
void software_rand64_init(const char *);

// Returns a random value using software operations.
unsigned long long software_rand64(void);

// Finalizes the software RNG.
void software_rand64_fini(void);

#endif