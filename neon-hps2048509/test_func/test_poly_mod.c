#include <stdio.h>
#include <stdlib.h>
#include "../poly.h"
#include "../poly_mod.c"
#include "../neon_poly_mod.c"

#define TESTS 100000
#define MASK (2047)

// Compile flags
//  clang -o test_poly_mod  test_poly_mod.c -g3 -O0 -Wall -Wextra

// Return 0 when PASS, otherwise 1
uint16_t compare_array(uint16_t *a, uint16_t *b, uint16_t size,
                       const char *string) {
//   printf("%s: \n", string);
  uint16_t error = 0;
  for (uint16_t i = 0; i < size; i ++) {
    if (a[i] != b[i]) {
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



int test_poly_mod_3_Phi_n(poly *a, poly *b)
{
    poly_mod_3_Phi_n(a);
    neon_poly_mod_3_Phi_n(b);

    int res = 0;
    res |= compare_array(a->coeffs, b->coeffs, NTRU_N, "poly_mod_3_Phi_n vs neon_poly_mod_3_Phi_n");
    
    return res;
}

int test_poly_mod_q_Phi_n(poly *a, poly *b)
{
    poly_mod_q_Phi_n(a);
    neon_poly_mod_q_Phi_n(b);

    int res = 0;
    res |= compare_array(a->coeffs, b->coeffs, NTRU_N, "poly_mod_q_Phi_n vs neon_poly_mod_q_Phi_n");
    
    return res;
}

int test_poly_Rq_to_S3(poly *a, poly *b)
{
    poly e, f;
    poly_Rq_to_S3(&e, a);
    neon_poly_Rq_to_S3(&f, b);

    int res = 0;
    res |= compare_array(e.coeffs, f.coeffs, NTRU_N, "poly_Rq_to_S3 vs neon_poly_Rq_to_S3");

    return res;
}

int main()
{
    poly a, b;
    int res = 0;
    uint16_t t; 
    for (int i = 0; i < TESTS; i++)
    {
        // 1st
        for (uint16_t j = 0; j < NTRU_N; j++)
        {
            t = rand();
            a.coeffs[j] = t & MASK;
            b.coeffs[j] = t & MASK;
        }
        for (uint16_t k = NTRU_N; k < NTRU_N_PAD; k++)
        {
            a.coeffs[k] = 0;
            b.coeffs[k] = 0;
        }

        res |= test_poly_mod_3_Phi_n(&a, &b);

        // 2nd 
        for (uint16_t j = 0; j < NTRU_N; j++)
        {
            t = rand();
            a.coeffs[j] = t & MASK;
            b.coeffs[j] = t & MASK;
        }
        for (uint16_t k = NTRU_N; k < NTRU_N_PAD; k++)
        {
            a.coeffs[k] = 0;
            b.coeffs[k] = 0;
        }
        res |= test_poly_mod_q_Phi_n(&a, &b);

        // 3rd 
        for (uint16_t j = 0; j < NTRU_N; j++)
        {
            t = rand();
            a.coeffs[j] = t & MASK;
            b.coeffs[j] = t & MASK;
        }
        for (uint16_t k = NTRU_N; k < NTRU_N_PAD; k++)
        {
            a.coeffs[k] = 0;
            b.coeffs[k] = 0;
        }
        res |= test_poly_Rq_to_S3(&a, &b);

        if (res) break;

    }
    return res;
}
