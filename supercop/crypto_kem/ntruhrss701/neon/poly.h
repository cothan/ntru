/*=============================================================================
This file has been adapted from the implementation 
(available at, CC0-1.0 License https://github.com/jschanck/ntru) 
of "NTRU:A submission to the NIST post-quantum standardization effort"
by : Cong Chen, Oussama Danba, Jeffrey Hoffstein, Andreas Hülsing, 
Joost Rijneveld, Tsunekazu Saito, John M. Schanck, Peter Schwabe, 
William Whyte,Keita Xagawa, Takashi Yamakawa, Zhenfei Zhang.
=============================================================================*/

#ifndef POLY_H
#define POLY_H

#include <stdint.h>
#include "params.h"

#define MODQ(X) ((X) & (NTRU_Q-1))

typedef struct{
  // round to nearest multiple of 32 to make it easier to load into vector
  //   registers without having to do bound checks
  #define NTRU_N_32 PAD32(NTRU_N)
  uint16_t coeffs[NTRU_N_PAD] __attribute__((aligned(32)));
} poly;

void poly_mod_3_Phi_n(poly *r);
void poly_mod_q_Phi_n(poly *r);

void poly_Sq_tobytes(unsigned char *r, const poly *a);
void poly_Sq_frombytes(poly *r, const unsigned char *a);

void poly_Rq_sum_zero_tobytes(unsigned char *r, const poly *a);
void poly_Rq_sum_zero_frombytes(poly *r, const unsigned char *a);

void poly_S3_tobytes(unsigned char msg[NTRU_PACK_TRINARY_BYTES], const poly *r);
void poly_S3_frombytes(poly *r, const unsigned char msg[NTRU_PACK_TRINARY_BYTES]);

void poly_Sq_mul(poly *r, poly *a, poly *b);
void poly_Rq_mul(poly *r, poly *a, poly *b);
void poly_S3_mul(poly *r, poly *a, poly *b);
void poly_lift(poly *r, const poly *a);
void poly_Rq_to_S3(poly *r, const poly *a);

void poly_R2_inv(poly *r, const poly *a);
void poly_Rq_inv(poly *r, const poly *a);
void poly_S3_inv(poly *r, const poly *a);

void poly_Z3_to_Zq(poly *r);
void poly_trinary_Zq_to_Z3(poly *r);

#endif
