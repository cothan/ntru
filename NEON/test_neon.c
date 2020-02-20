#include <arm_neon.h>

#define N 704

typedef struct Poly
{
    int16_t coeffs[N];
} poly;

int K2_schoolbook_64x11(poly *r, const poly *a, const poly *b)
{
    /*
    Load to 12 Q registers 
    */
    int16x8_t a0 = vld1q_s16(a->coeffs); // y0
    // int16x8_t a1 = vld1q_s16(a->coeffs + 8); // y0

    int16x8_t b0 = vld1q_s16(b->coeffs); // y6
    // int16x8_t b1 = vld1q_s16(b->coeffs + 8); // y6

    int16x8_t a2 = vld1q_s16(a->coeffs + 16); // y1
    // int16x8_t a3 = vld1q_s16(a->coeffs + 24); // y1

    int16x8_t b2 = vld1q_s16(b->coeffs + 16); // y7
    // int16x8_t b3 = vld1q_s16(b->coeffs + 24); // y7

    int16x8_t a4 = vld1q_s16(a->coeffs + 32); // y2
    // int16x8_t a5 = vld1q_s16(a->coeffs + 40); // y2

    int16x8_t b4 = vld1q_s16(b->coeffs + 32); // y8
    // int16x8_t b5 = vld1q_s16(b->coeffs + 40); // y8

    int16x8_t a6 = vld1q_s16(a->coeffs + 48); // y3
    // int16x8_t a7 = vld1q_s16(a->coeffs + 56); // y3

    int16x8_t b6 = vld1q_s16(b->coeffs + 48); // y9
    // int16x8_t b7 = vld1q_s16(b->coeffs + 56); // y9

    int16x8_t a8 = vld1q_s16(a->coeffs + 64); // y4
    // int16x8_t a9 = vld1q_s16(a->coeffs + 72); // y4

    int16x8_t b8 = vld1q_s16(b->coeffs + 64); // y10
    // int16x8_t b9 = vld1q_s16(b->coeffs + 72); // y10

    int16x8_t a10 = vld1q_s16(a->coeffs + 80); // y5
    // int16x8_t a11 = vld1q_s16(a->coeffs + 88); // y5

    int16x8_t b10 = vld1q_s16(b->coeffs + 80); // y11
    // int16x8_t b11 = vld1q_s16(b->coeffs + 88); // y11

    // (0, 6)

    int16x8_t c0 = vmulq_s16(a0, b0); // y12 = y0*y6
    // int16x8_t c1 = vmulq_s16(a1, b1); // y12 = y0*y6

    vst1q_s16(r->coeffs, c0);
    // vst1q_s16(r->coeffs + 8, c0);

    // (0, 7) + (1, 6)

    c0 = vmulq_s16(a0, b2); // y13 = y0 * y7
    // c1 = vmulq_s16(a1, b3); // y13 = y0 * y7

    // MUL and ADD
    c0 = vmlaq_s16(c0, a3, b0); // y15 = y13 + y1 * y6
    // c1 = vmlaq_s16(c1, a4, b1); // y15 = y13 + y1 * y6

    vst1q_s16(r->coeffs + 16, c0);
    // vst1q_s16(r->coeffs + 24, c1);

    // (0, 8) + (1, 7) + (2, 6)

    c0 = vmulq_s16(a0, b4); // (0, 8)
    // c1 = vmulq_s16(a1, b5); // (0, 8)

    c0 = vmlaq_s16(c0, a2, b2); // (0, 8) + (1, 7)
    // c1 = vmlaq_s16(c1, a3, b3); // (0, 8) + (1, 7)

    c0 = vmlaq_s16(c0, a4, b0); // (0, 8) + (1, 7) + (2, 6)
    // c1 = vmlaq_s16(c1, a5, b1); // (0, 8) + (1, 7) + (2, 6)

    vst1q_s16(r->coeffs + 32, c0);
    // vst1q_s16(r->coeffs + 40, c1);

    // (0, 9) + (1, 8) + (2, 7) + (3 , 6)

    c0 = vmulq_s16(a0, b6); // (0, 9)
    // c1 = vmulq_s16(a1, b7); // (0, 9)

    c0 = vmlaq_s16(c0, a2, b4); // (0, 9) + (1, 8)
    // c1 = vmlaq_s16(c1, a3, b5); // (0, 9) + (1, 8)

    c0 = vmlaq_s16(c0, a4, b2); // (0, 9) + (1, 8) + (2, 7)
    // c1 = vmlaq_s16(c1, a5, b3); // (0, 9) + (1, 8) + (2, 7)

    c0 = vmlaq_s16(c0, a6, b0); // (0, 9) + (1, 8) + (2, 7) + (3, 6)
    // c1 = vmlaq_s16(c1, a7, b1); // (0, 9) + (1, 8) + (2, 7) + (3, 6)

    vst1q_s16(r->coeffs + 48, c0);
    // vst1q_s16(r->coeffs + 56, c1);

    // (0, 10) + (1, 9) + (2, 8) + (3, 7) + (4 , 6)

    c0 = vmulq_s16(a0, b8); // (0, 10)
    // c1 = vmulq_s16(a1, b9); // (0, 10)

    c0 = vmlaq_s16(c0, a2, b6); // (0, 10) + (1, 9)
    // c1 = vmlaq_s16(c1, a3, b7); // (0, 10) + (1, 9)

    c0 = vmlaq_s16(c0, a4, b4); // (0, 10) + (1, 9) + (2, 8)
    // c1 = vmlaq_s16(c1, a5, b5); // (0, 10) + (1, 9) + (2, 8)

    c0 = vmlaq_s16(c0, a6, b2); // (0, 10) + (1, 9) + (2, 8) + (3, 7)
    // c1 = vmlaq_s16(c1, a7, b3); // (0, 10) + (1, 9) + (2, 8) + (3, 7)

    c0 = vmlaq_s16(c0, a8, b0); // (0, 10) + (1, 9) + (2, 8) + (3, 7) + (4, 6)
    // c1 = vmlaq_s16(c1, a9, b1); // (0, 10) + (1, 9) + (2, 8) + (3, 7) + (4, 6)

    vst1q_s16(r->coeffs + 64, c0);
    // vst1q_s16(r->coeffs + 72, c1);

    // (0,11) + (1, 10) + (2, 9) + (3, 8) + (4, 7) + (5, 6)

    c0 = vmulq_s16(a0, b10); // (0, 11)
    // c1 = vmulq_s16(a1, b11); // (0, 11)

    c0 = vmlaq_s16(c0, a2, b8); // (0, 11) + (1, 10)
    // c1 = vmlaq_s16(c1, a3, b9); // (0, 11) + (1, 10)

    c0 = vmlaq_s16(c0, a4, b6); // (0, 11) + (1, 10) + (2, 9)
    // c1 = vmlaq_s16(c1, a5, b7); // (0, 11) + (1, 10) + (2, 9)

    c0 = vmlaq_s16(c0, a6, b4); // (0, 11) + (1, 10) + (2, 9) + (3, 8)
    // c1 = vmlaq_s16(c1, a7, b5); // (0, 11) + (1, 10) + (2, 9) + (3, 8)

    c0 = vmlaq_s16(c0, a8, b2); // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7)
    // c1 = vmlaq_s16(c1, a9, b3); // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7)

    c0 = vmlaq_s16(c0, a10, b0); // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7) + (5, 6)
    // c1 = vmlaq_s16(c1, a11, b1); // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7) + (5, 6)

    vst1q_s16(r->coeffs + 80, c0);
    // vst1q_s16(r->coeffs + 88, c1);

    // (1, 11) + (2, 10) + (3, 9) + (4, 8) + (5, 7)

    c0 = vmulq_s16(a2, b10); // (1, 11)
    // c1 = vmulq_s16(a3, b11); // (1, 11)

    c0 = vmlaq_s16(c0, a4, b8); // (1, 11) + (2, 10)
    // c1 = vmlaq_s16(c1, a5, b9); // (1, 11) + (2, 10)

    c0 = vmlaq_s16(c0, a6, b6); // (1, 11) + (2, 10) + (3, 9)
    // c1 = vmlaq_s16(c1, a7, b7); // (1, 11) + (2, 10) + (3, 9)

    c0 = vmlaq_s16(c0, a8, b4); // (1, 11) + (2, 10) + (3, 9) + (4, 8)
    // c1 = vmlaq_s16(c1, a9, b5); // (1, 11) + (2, 10) + (3, 9) + (4, 8)

    c0 = vmlaq_s16(c0, a10, b2); // (1, 11) + (2, 10) + (3, 9) + (4, 8) + (5, 7)
    // c1 = vmlaq_s16(c1, a11, b3); // (1, 11) + (2, 10) + (3, 9) + (4, 8) + (5, 7)

    vst1q_s16(r->coeffs + 96, c0);
    // vst1q_s16(r->coeffs + 104, c1);

    // (2, 11) + (3, 10) + (4, 9) + (5, 8) 

    c0 = vmulq_s16(a4, b10); // (2, 11)
    // c1 = vmulq_s16(a5, b11); // (2, 11)

    c0 = vmlaq_s16(c0, a6, b8); // (2, 11) + (3, 10) 
    // c1 = vmlaq_s16(c1, a7, b9); // (2, 11) + (3, 10) 

    c0 = vmlaq_s16(c0, a8, b6); // (2, 11) + (3, 10) + (4, 9)
    // c1 = vmlaq_s16(c1, a9, b7); // (2, 11) + (3, 10) + (4, 9)

    c0 = vmlaq_s16(c0, a10, b4); // (2, 11) + (3, 10) + (4, 9) + (5, 8)
    // c1 = vmlaq_s16(c1, a11, b5); // (2, 11) + (3, 10) + (4, 9) + (5, 8)
    
    vst1q_s16(r->coeffs + 112, c0);
    // vst1q_s16(r->coeffs + 120, c1);

    // (3, 11) + (4, 10) + (5, 9) 

    c0 = vmulq_s16(a6, b10); // (3, 11)
    // c1 = vmulq_s16(a7, b11); // (3, 11)

    c0 = vmlaq_s16(c0, a8, b8); // (3, 11) + (4, 10)
    // c1 = vmlaq_s16(c1, a9, b9); // (3, 11) + (4, 10)

    c0 = vmlaq_s16(c0, a10, b6); // (3, 11) + (4, 10) + (5, 9)
    // c1 = vmlaq_s16(c1, a11, b7); // (3, 11) + (4, 10) + (5, 9)

    vst1q_s16(r->coeffs + 128, c0);
    // vst1q_s16(r->coeffs + 136, c1);
    
    // (4, 11) + (5, 10)

    c0 = vmulq_s16(a8, b10); // (4, 11)
    // c1 = vmulq_s16(a9, b11); // (4, 11)

    c0 = vmlaq_s16(c0, a10, b8); // (5, 10)
    // c1 = vmulq_s16(c1, a11, b9); // (5, 10)

    vst1q_s16(r->coeffs + 144, c0);
    // vst1q_s16(r->coeffs + 152, c1);

    // (5, 11)

    c0 = vmulq_s16(a10, b10); // (5, 11)
    // c1 = vmulq_s16(a11, b11); // (5, 11)

    vst1q_s16(r->coeffs + 160, c0);
    // vst1q_s16(r->coeffs + 168, c1);

    
}

int main()
{
    return 0;
}