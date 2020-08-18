#include "rq_mul/neon_poly_rq_mul.h"
#include "poly.h"

void neon_poly_Rq_mul(poly *r, const poly *a, const poly *b)
// void poly_Rq_mul(poly *r, const poly *a, const poly *b)
{
    poly_mul_neon(r->coeffs, a->coeffs, b->coeffs);
}

