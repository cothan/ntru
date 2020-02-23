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
    int16x8_t y0 = vld1q_s16(a->coeffs); // y0

    int16x8_t y6 = vld1q_s16(b->coeffs); // y6

    int16x8_t y1 = vld1q_s16(a->coeffs + 16); // y1

    int16x8_t y7 = vld1q_s16(b->coeffs + 16); // y7

    int16x8_t y2 = vld1q_s16(a->coeffs + 32); // y2

    int16x8_t y8 = vld1q_s16(b->coeffs + 32); // y8

    int16x8_t y3 = vld1q_s16(a->coeffs + 48); // y3

    int16x8_t y9 = vld1q_s16(b->coeffs + 48); // y9

    int16x8_t y4 = vld1q_s16(a->coeffs + 64); // y4

    int16x8_t y10 = vld1q_s16(b->coeffs + 64); // y10

    int16x8_t y5 = vld1q_s16(a->coeffs + 80); // y5

    int16x8_t y11 = vld1q_s16(b->coeffs + 80); // y11

    // (0, 6)

    int16x8_t c0 = vmulq_s16(y0, y6); // y12 = y0*y6

    vst1q_s16(r->coeffs, c0);

    // (0, 7) + (1, 6)

    c0 = vmulq_s16(y0, y7); // y13 = y0 * y7

    c0 = vmlaq_s16(c0, y1, y6); // y15 = y13 + y1 * y6

    vst1q_s16(r->coeffs + 16, c0);

    // (0, 8) + (1, 7) + (2, 6)

    c0 = vmulq_s16(y0, y8); // (0, 8)

    c0 = vmlaq_s16(c0, y1, y7); // (0, 8) + (1, 7)

    c0 = vmlaq_s16(c0, y2, y6); // (0, 8) + (1, 7) + (2, 6)

    vst1q_s16(r->coeffs + 32, c0);

    // (0, 9) + (1, 8) + (2, 7) + (3, 6)

    c0 = vmulq_s16(y0, y9); // (0, 9)

    c0 = vmlaq_s16(c0, y1, y8); // (0, 9) + (1, 8)

    c0 = vmlaq_s16(c0, y2, y7); // (0, 9) + (1, 8) + (2, 7)

    c0 = vmlaq_s16(c0, y3, y6); // (0, 9) + (1, 8) + (2, 7) + (3, 6)

    vst1q_s16(r->coeffs + 48, c0);

    // (0, 10) + (1, 9) + (2, 8) + (3, 7) + (4, 6)

    c0 = vmulq_s16(y0, y10); // (0, 10)

    c0 = vmlaq_s16(c0, y1, y9); // (0, 10) + (1, 9)

    c0 = vmlaq_s16(c0, y2, y8); // (0, 10) + (1, 9) + (2, 8)

    c0 = vmlaq_s16(c0, y3, y7); // (0, 10) + (1, 9) + (2, 8) + (3, 7)

    c0 = vmlaq_s16(c0, y4, y6); // (0, 10) + (1, 9) + (2, 8) + (3, 7) + (4, 6)

    vst1q_s16(r->coeffs + 64, c0);

    // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7) + (5, 6)

    c0 = vmulq_s16(y0, y11); // (0, 11)

    c0 = vmlaq_s16(c0, y1, y10); // (0, 11) + (1, 10)

    c0 = vmlaq_s16(c0, y2, y9); // (0, 11) + (1, 10) + (2, 9)

    c0 = vmlaq_s16(c0, y3, y8); // (0, 11) + (1, 10) + (2, 9) + (3, 8)

    c0 = vmlaq_s16(c0, y4, y7); // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7)

    c0 = vmlaq_s16(c0, y5, y6); // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7) + (5, 6)

    vst1q_s16(r->coeffs + 80, c0);

    // (1, 11) + (2, 10) + (3, 9) + (4, 8) + (5, 7)

    c0 = vmulq_s16(y1, y11); // (1, 11)

    c0 = vmlaq_s16(c0, y2, y10); // (1, 11) + (2, 10)

    c0 = vmlaq_s16(c0, y3, y9); // (1, 11) + (2, 10) + (3, 9)

    c0 = vmlaq_s16(c0, y4, y8); // (1, 11) + (2, 10) + (3, 9) + (4, 8)

    c0 = vmlaq_s16(c0, y5, y7); // (1, 11) + (2, 10) + (3, 9) + (4, 8) + (5, 7)

    vst1q_s16(r->coeffs + 96, c0);

    // (2, 11) + (3, 10) + (4, 9) + (5, 8)

    c0 = vmulq_s16(y2, y11); // (2, 11)

    c0 = vmlaq_s16(c0, y3, y10); // (2, 11) + (3, 10)

    c0 = vmlaq_s16(c0, y4, y9); // (2, 11) + (3, 10) + (4, 9)

    c0 = vmlaq_s16(c0, y5, y8); // (2, 11) + (3, 10) + (4, 9) + (5, 8)

    vst1q_s16(r->coeffs + 112, c0);

    // (3, 11) + (4, 10) + (5, 9)

    c0 = vmulq_s16(y3, y11); // (3, 11)

    c0 = vmlaq_s16(c0, y4, y10); // (3, 11) + (4, 10)

    c0 = vmlaq_s16(c0, y5, y9); // (3, 11) + (4, 10) + (5, 9)

    vst1q_s16(r->coeffs + 128, c0);

    // (4, 11) + (5, 10)

    c0 = vmulq_s16(y4, y11); // (4, 11)

    c0 = vmlaq_s16(c0, y5, y10); // (5, 10)

    vst1q_s16(r->coeffs + 144, c0);

    // (5, 11)

    c0 = vmulq_s16(y5, y11); // (5, 11)

    vst1q_s16(r->coeffs + 160, c0);

    y0 = vld1q_s16(a->coeffs + 96);
    y6 = vld1q_s16(b->coeffs + 96);

    y1 = vld1q_s16(a->coeffs + 112);
    y7 = vld1q_s16(b->coeffs + 112);

    y2 = vld1q_s16(a->coeffs + 128);
    y8 = vld1q_s16(b->coeffs + 128);

    y3 = vld1q_s16(a->coeffs + 144);
    y9 = vld1q_s16(b->coeffs + 144);

    y4 = vld1q_s16(a->coeffs + 160);
    y10 = vld1q_s16(b->coeffs + 160);

    // (0, 6)

    c0 = vmulq_s16(y0, y6);

    vst1q_s16(r->coeffs + 192, c0);

    // (0, 7) + (1, 6)

    c0 = vmulq_s16(y0, y7);

    c0 = vmlaq_s16(c0, y1, y6);

    vst1q_s16(r->coeffs + 208, c0);

    // (0, 8) + (1, 7) + (2, 6)

    c0 = vmulq_s16(y0, y8);

    c0 = vmlaq_s16(c0, y1, y7);

    c0 = vmlaq_s16(c0, y2, y6);

    vst1q_s16(r->coeffs + 224, c0);

    // (0, 9) + (1, 8) + (2, 7) + (3, 6)

    c0 = vmulq_s16(y0, y9);

    c0 = vmlaq_s16(c0, y1, y8);

    c0 = vmlaq_s16(c0, y2, y7);

    c0 = vmlaq_s16(c0, y3, y6);

    vst1q_s16(r->coeffs + 240, c0);

    // (0, 10) + (1, 9) + (2, 8) + (3, 7) + (4, 6)

    c0 = vmulq_s16(y0, y10);

    c0 = vmlaq_s16(c0, y1, y9);

    c0 = vmlaq_s16(c0, y2, y8);

    c0 = vmlaq_s16(c0, y3, y7);

    c0 = vmlaq_s16(c0, y4, y6);

    vst1q_s16(r->coeffs + 256, c0);

    // (1, 10) + (2, 9) + (3, 8) + (4, 7)

    c0 = vmulq_s16(y1, y10);

    c0 = vmlaq_s16(c0, y2, y9);

    c0 = vmlaq_s16(c0, y3, y8);

    c0 = vmlaq_s16(c0, y4, y7);

    vst1q_s16(r->coeffs + 272, c0);

    // (2, 10) + (3, 9) + (4, 8)

    c0 = vmulq_s16(y2, y10);

    c0 = vmlaq_s16(c0, y3, y9);

    c0 = vmlaq_s16(c0, y4, y8);

    vst1q_s16(r->coeffs + 288, c0);

    // (3, 10) + (4, 9)

    c0 = vmulq_s16(y3, y10);

    c0 = vmlaq_s16(c0, y4, y9);

    vst1q_s16(r->coeffs + 304, c0);

    // (4, 10)

    c0 = vmulq_s16(y4, y10);

    vst1q_s16(r->coeffs + 320, c0);

    y0 = vaddq_s16(y0, vld1q_s16(a->coeffs));
    y6 = vaddq_s16(y6, vld1q_s16(b->coeffs));

    y1 = vaddq_s16(y1, vld1q_s16(a->coeffs + 16));
    y7 = vaddq_s16(y7, vld1q_s16(b->coeffs + 16));

    y2 = vaddq_s16(y2, vld1q_s16(a->coeffs + 32));
    y8 = vaddq_s16(y8, vld1q_s16(b->coeffs + 32));

    y3 = vaddq_s16(y3, vld1q_s16(a->coeffs + 48));
    y9 = vaddq_s16(y9, vld1q_s16(b->coeffs + 48));

    y4 = vaddq_s16(y4,   vld1q_s16(a->coeffs + 64));
    y10 = vaddq_s16(y10, vld1q_s16(b->coeffs + 64));

    // (0, 11) + (1, 10) + (2, 9) + (3, 8) + (4, 7) + (5, 6)
    c0 = vmulq_s16(y0, y11);

    c0 = vmlaq_s16(c0, y1, y10);

    c0 = vmlaq_s16(c0, y2, y9);

    c0 = vmlaq_s16(c0, y3, y8);

    c0 = vmlaq_s16(c0, y4, y7);

    c0 = vmlaq_s16(c0, y5, y6);

    c0 = vsubq_s16(c0, vld1q_s16(r->coeffs + 80));

    c0 = vsubq_s16(c0, vld1q_s16(r->coeffs + 272));

    vst1q_s16(r->coeffs + 176, c0);

    int16x8_t y12 = vmulq_s16(y5, y7);
    int16x8_t y13 = vmulq_s16(y5, y8);
    int16x8_t y14 = vmulq_s16(y5, y9);
    int16x8_t y15 = vmulq_s16(y5, y10);
    
    y12 = vmulq_s16(y1, y11);
    // y12 = vmlaq_s16(y12, y1, y11);
    y12 = vmlaq_s16(y12, y2, y10);
    y12 = vmlaq_s16(y12, y3, y9);
    y12 = vmlaq_s16(y12, y4, y8);

    y13 = vmlaq_s16(y13, y2, y11);
    y13 = vmlaq_s16(y13, y3, y10);
    y13 = vmlaq_s16(y13, y4, y9);

    y14 = vmlaq_s16(y14, y3, y11);
    y14 = vmlaq_s16(y14, y4, y10);

    y15 = vmlaq_s16(y15, y4, y11);

    y11 = vmulq_s16(y0, y10);
    y11 = vmlaq_s16(y11, y1, y9);
    y11 = vmlaq_s16(y11, y2, y8);
    y11 = vmlaq_s16(y11, y3, y7);
    y11 = vmlaq_s16(y11, y4, y6);

    y10 = vmulq_s16(y0, y9);
    y10 = vmlaq_s16(y10, y1, y8);
    y10 = vmlaq_s16(y10, y2, y7);
    y10 = vmlaq_s16(y10, y3, y6);

    y9 = vmulq_s16(y0, y8);
    y9 = vmlaq_s16(y9, y1, y7);
    y9 = vmlaq_s16(y9, y2, y6);

    y8 = vmulq_s16(y0, y7);
    y8 = vmlaq_s16(y8, y1, y6);

    y7 = vmulq_s16(y0, y6);

    y0 = vld1q_s16(r->coeffs + 96); 

    y0 = vsubq_s16(y0, vld1q_s16(r->coeffs + 192));
    y6 = vsubq_s16(y12, y0);
    y6 = vsubq_s16(y6, vld1q_s16(r->coeffs + 288));
    vst1q_s16(r->coeffs + 192, y6);

    y0 = vaddq_s16(y0, y7);
    y0 = vsubq_s16(y0, vld1q_s16(r->coeffs));
    vst1q_s16(r->coeffs + 96, y0);

    y1 = vsubq_s16(vld1q_s16(r->coeffs + 112), vld1q_s16(r->coeffs + 208));
    y7 = vsubq_s16(y13, y1);
    y7 = vsubq_s16(y7, vld1q_s16(r->coeffs + 304));
    vst1q_s16(r->coeffs + 208, y7);

    y1 = vaddq_s16(y1, y8);
    y1 = vsubq_s16(y1, vld1q_s16(r->coeffs + 16));
    vst1q_s16(r->coeffs + 112, y1);

    y2 = vsubq_s16(vld1q_s16(r->coeffs +128), vld1q_s16(r->coeffs + 224));
    y8 = vsubq_s16(y14, y2);
    y8 = vsubq_s16(y8, vld1q_s16(r->coeffs + 320));
    vst1q_s16(r->coeffs + 224, y8);

    y2 = vaddq_s16(y2, y9);
    y2 = vsubq_s16(y2, vld1q_s16(r->coeffs + 32));
    vst1q_s16(r->coeffs + 128, y2);

    y3 = vsubq_s16(vld1q_s16(r->coeffs + 144), vld1q_s16(r->coeffs + 240));
    y9 = vsubq_s16(y15, y3);
    vst1q_s16(r->coeffs + 240, y9);

    y3 = vaddq_s16(y3, y10);
    y3 = vsubq_s16(y3, vld1q_s16(r->coeffs + 48));
    vst1q_s16(r->coeffs + 144, y3);

    y4 = vsubq_s16(vld1q_s16(r->coeffs + 160), vld1q_s16(r->coeffs + 256));
    y4 = vaddq_s16(y4, y11);
    y4 = vsubq_s64(y4, vld1q_s16(r->coeffs + 64));
    vst1q_s16(r->coeffs + 160, y4);
}

int main()
{
    
    return 0;
}