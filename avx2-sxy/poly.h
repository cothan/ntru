#ifndef POLY_H
#define POLY_H

#include <stdint.h>
#include <stdlib.h>
#include "params.h"

typedef struct{
  // round to nearest multiple of 32 to make it easier to load into vector
  //   registers without having to do bound checks
  #define NTRU_N_32 ((NTRU_N + 31) / 32) * 32
  uint16_t coeffs[NTRU_N_32] __attribute__((aligned(32)));
} poly;

void poly_Rq_sum_zero_tobytes(unsigned char *r, const poly *a);
void poly_Rq_sum_zero_frombytes(poly *r, const unsigned char *a);

void poly_S3_tobytes(unsigned char msg[NTRU_PACK_TRINARY_BYTES], const poly *r);
void poly_S3_frombytes(poly *r, const unsigned char msg[NTRU_PACK_TRINARY_BYTES]);

void poly_S3_xof(unsigned char *output, const size_t sizeof_output, const unsigned char seed[NTRU_SEEDBYTES], const unsigned char domain[NTRU_DOMAINBYTES]);
void poly_S3_format(poly *r, const unsigned char uniformbytes[NTRU_S3_RANDOMBYTES]);
void poly_S3_format_plus(poly *r, const unsigned char uniformbytes[NTRU_S3_RANDOMBYTES]);

void poly_Rq_mul(poly *r, const poly *a, const poly *b);
void poly_Rq_mul_x_minus_1(poly *r, const poly *a);
void poly_S3_mul(poly *r, const poly *a, const poly *b);
void poly_S3_to_Rq(poly *r, const poly *a);
void poly_Rq_to_S3(poly *r, const poly *a);

void poly_Rq_inv(poly *r, const poly *a);
void poly_S3_inv(poly *r, const poly *a);

void poly_Z3_to_Zq(poly *r);
void poly_trinary_Zq_to_Z3(poly *r);

#endif
