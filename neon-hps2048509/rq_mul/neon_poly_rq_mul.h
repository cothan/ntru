#ifndef NEON_POLY_RQ_MUL_H
#define NEON_POLY_RQ_MUL_H

#include <stdint.h>

void poly_mul_neon(uint16_t *restrict polyC, 
                   uint16_t const polyA[512], 
                   uint16_t const polyB[512]);

#endif
