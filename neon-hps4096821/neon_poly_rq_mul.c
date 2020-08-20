#include "rq_mul/neon_poly_rq_mul.h"
#include "poly.h"
#include <arm_neon.h>

// store c <= a
#define polyrq_vstore_const(c, a) \
    vst1q_u16(c +  0, a);         \
    vst1q_u16(c +  8, a);         \
    vst1q_u16(c + 16, a);         \
    vst1q_u16(c + 24, a);

#define polyrq_vstore_x1(c, a) vst1q_u16(c, a);


// void neon_poly_Rq_mul(poly *r, const poly *a, const poly *b)
void poly_Rq_mul(poly *r, poly *a, poly *b)
{
    // Must zero garbage data at the end

    uint16x8_t last;
    last = vdupq_n_u16(0);

    // 821, 822, 823
    a->coeffs[NTRU_N] = 0;
    a->coeffs[NTRU_N+1] = 0;
    a->coeffs[NTRU_N+2] = 0;
    // 821, 822, 823
    b->coeffs[NTRU_N] = 0;
    b->coeffs[NTRU_N+1] = 0;
    b->coeffs[NTRU_N+2] = 0;

    // 824 + 32 = 856
    polyrq_vstore_const(&a->coeffs[NTRU_N + 3], last);
    // 856 -> 864
    polyrq_vstore_x1(&a->coeffs[NTRU_N + 35], last);

    // 824 + 32 = 856
    polyrq_vstore_const(&b->coeffs[NTRU_N + 3], last);
    // 856 -> 864
    polyrq_vstore_x1(&b->coeffs[NTRU_N + 35], last);
    
    // Multiplication
    poly_mul_neon(r->coeffs, a->coeffs, b->coeffs);
    
}
