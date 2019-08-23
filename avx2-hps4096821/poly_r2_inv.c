#include "poly_r2_inv.h"
#include "poly.h"

// TODO this costs 1764 cycles.. (implementing as S3_to_bytes results in 2108)
// This can be implemented nicely in assembly using pdep / pext functions
void poly_R2_tobytes(unsigned char *out, const poly *a)
{
  #if NTRU_N != 821
    #error This function requires NTRU_N = 821!
  #endif
  int i, j, k;
  for (i = 0; i < 16; i++) {
    for (k = 0; k < 8; k++) {
      out[i*8+k] = 0;
      for (j = 0; j < 8; j++) {
        if ((i*8+k)*8 + j < NTRU_N) {
          out[i*8+k] |= (a->coeffs[(i*8+k)*8 + j] & 1) << j;
        }
      }
    }
  }
}

void poly_R2_frombytes(poly *a, const unsigned char *in)
{
  #if NTRU_N != 821 
    #error This function requires NTRU_N = 821!
  #endif
  int i, j, k;
  for (i = 0; i < 16; i++) {
    for (k = 0; k < 8; k++) {
      for (j = 0; j < 8; j++) {
        if ((i*8+k)*8 + j < NTRU_N) {
          a->coeffs[(i*8+k)*8 + j] = (in[i*8+k] >> j) & 1;
        }
      }
    }
  }
}

void poly_R2_mul(unsigned char* out, const unsigned char* a, const unsigned char* b)
{
  int i;
  poly ap, bp, rp;
  poly_R2_frombytes(&ap, a);
  poly_R2_frombytes(&bp, b);
  poly_Rq_mul(&rp, &ap, &bp);
  poly_R2_tobytes(out, &rp);
}

int poly_R2_inv(poly *r, const poly *a) {
    #if NTRU_N != 821
      #error This function requires NTRU_N = 821!
    #endif
    unsigned char squares[13][128] __attribute__((aligned(32)));

    // This relies on the following addition chain:
    // 1, 2, 3, 6, 12, 24, 48, 51, 102, 204, 408, 816, 819

    poly_R2_tobytes(squares[0], a); // TODO alignment

    square_1_821(squares[1], squares[0]);
    poly_R2_mul(squares[1], squares[1], squares[0]);
    square_1_821(squares[2], squares[1]);
    poly_R2_mul(squares[2], squares[2], squares[0]);
    square_3_821(squares[3], squares[2]);
    poly_R2_mul(squares[3], squares[3], squares[2]);
    square_6_821(squares[4], squares[3]);
    poly_R2_mul(squares[4], squares[4], squares[3]);
    square_12_821(squares[5], squares[4]);
    poly_R2_mul(squares[5], squares[5], squares[4]);
    square_24_821(squares[6], squares[5]);
    poly_R2_mul(squares[6], squares[6], squares[5]);
    square_3_821(squares[7], squares[6]);
    poly_R2_mul(squares[7], squares[7], squares[2]);
    square_51_821(squares[8], squares[7]);
    poly_R2_mul(squares[8], squares[8], squares[7]);
    square_102_821(squares[9], squares[8]);
    poly_R2_mul(squares[9], squares[9], squares[8]);
    square_204_821(squares[10], squares[9]);
    poly_R2_mul(squares[10], squares[10], squares[9]);
    square_408_821(squares[11], squares[10]);
    poly_R2_mul(squares[11], squares[11], squares[10]);
    square_3_821(squares[12], squares[11]);
    poly_R2_mul(squares[12], squares[12], squares[2]);
    square_1_821(squares[0], squares[12]);


    poly_R2_frombytes(r, squares[0]);
    return 0;
}
