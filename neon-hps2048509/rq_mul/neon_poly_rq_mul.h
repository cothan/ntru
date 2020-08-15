#ifndef NEON_POLY_RQ_MUL_H
#define NEON_POLY_RQ_MUL_H

#include <stdint.h>

void poly_mul_neon(uint16_t polyC[512], uint16_t polyA[512], uint16_t polyB[512]);

#endif
