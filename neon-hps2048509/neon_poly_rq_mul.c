#include "rq_mul/neon_poly_rq_mul.h"
#include "poly.h"

// void neon_poly_Rq_mul(poly *r, const poly *a, const poly *b)
void poly_Rq_mul(poly *r, poly *a, poly *b)
{
    // Must zero garbage data at the end
    a->coeffs[NTRU_N] = 0;
    a->coeffs[NTRU_N+1] = 0;
    a->coeffs[NTRU_N+2] = 0;
    b->coeffs[NTRU_N] = 0;
    b->coeffs[NTRU_N+1] = 0;
    b->coeffs[NTRU_N+2] = 0;
    
    poly_mul_neon(r->coeffs, a->coeffs, b->coeffs);
}
