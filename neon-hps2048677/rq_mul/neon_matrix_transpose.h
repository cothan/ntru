#ifndef NEON_MATRIX_TRANSPOSE_H
#define NEON_MATRIX_TRANSPOSE_H

#include <stdint.h>

void half_transpose_8x32(uint16_t *matrix);
void half_transpose_8x16(uint16_t *matrix);

#endif 
