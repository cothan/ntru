#include <stdio.h>
#include <stdlib.h>
#include "../poly.h"
#include "../neon_poly_rq_mul.c"
#include "../poly_rq_mul.c"

#define TESTS 100000
#define MASK (2047)

// Compile flags
// clang -o test_poly_Rq_mul ../rq_mul/neon_batch_multiplication.c ../rq_mul/neon_matrix_transpose.c ../rq_mul/neon_poly_rq_mul.c  test_poly_Rq_mul.c -g3 -O0 -Wall -Wextra

// Return 0 when PASS, otherwise 1
uint16_t compare_array(uint16_t *a, uint16_t *b, uint16_t size,
                       const char *string) {
//   printf("%s: \n", string);
  uint16_t error = 0;
  uint16_t tmp1, tmp2;

  for (uint16_t i = 0; i < size; i ++) {
    tmp1 = a[i] & MASK;
    tmp2 = b[i] & MASK;
    if (tmp1 != tmp2) {
        error = 1;
        printf("%d: %d != %d\n", i, a[i], b[i]);
    }
    
    if (error) {
      printf("FAILED\n");
      return 1;
    }
  }
//   printf("CORRECT\n");
  return 0;
}

uint16_t compare_array_8(uint16_t *a, uint16_t *b, uint16_t size,
                       const char *string) {
  printf("%s: \n", string);
  uint16_t error = 0;
  uint16_t tmp1, tmp2;
  for (uint16_t i = 0; i < size; i += 8) {
    for (uint16_t j = 0; j < 8; j++) {
        tmp1 = a[i + j] & MASK;
        tmp2 = b[i + j] & MASK;
      if (tmp1 != tmp2) {
        error = 1;
        printf("%d: %d != %d\n", i + j, tmp1, tmp2);
      }
    }
    if (error) {
      printf("FAILED\n");
      return 1;
    }
  }
  // printf("CORRECT\n");
  return 0;
}


int test_poly_Rq_mul(poly *a, poly *b)
{
    poly e, f;
    poly_Rq_mul(&e, a, b);
    neon_poly_Rq_mul(&f, a,  b);

    int res = 0;
    res |= compare_array(e.coeffs, f.coeffs, NTRU_N, "poly_Rq_mul vs neon_poly_Rq_mul");

    return res;
}


int main()
{
    poly a, b;
    int res = 0;
    for (int i = 0; i < TESTS; i++)
    {
        // 1st
        for (uint16_t j = 0; j < NTRU_N; j++)
        {
            a.coeffs[j] = rand() & MASK;
            b.coeffs[j] = rand() & MASK;
        }
        for (uint16_t k = NTRU_N; k < NTRU_N_PAD; k++)
        {
            a.coeffs[k] = 0;
            b.coeffs[k] = 0;
        }

        res |= test_poly_Rq_mul(&a, &b);

        if (res) break;
    }
    return res;
}