#ifndef NEON_BATCH_MULTIPLICATION_H
#define NEON_BATCH_MULTIPLICATION_H

#include <stdint.h>

void schoolbook_half_8x_neon(uint16_t *restrict c_in_mem,
                             uint16_t *restrict a_in_mem,
                             uint16_t *restrict b_in_mem);
#endif 
