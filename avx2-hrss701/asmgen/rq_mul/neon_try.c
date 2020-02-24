#include <arm_neon.h>

#define N 704

typedef struct Poly
{
  int16_t coeffs[N];
} poly;

int K2_schoolbook_64x11(poly *r,  poly *a,  poly *b)
{

  int16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15;
  int16x8_t

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 2; j++)
    {

      y0 = vld1q_s16(0 + a->coeffs);
      y6 = vld1q_s16(0 + b->coeffs);
      y1 = vld1q_s16(16 + a->coeffs);
      y7 = vld1q_s16(16 + b->coeffs);
      y2 = vld1q_s16(32 + a->coeffs);
      y8 = vld1q_s16(32 + b->coeffs);
      y3 = vld1q_s16(48 + a->coeffs);
      y9 = vld1q_s16(48 + b->coeffs);
      y4 = vld1q_s16(64 + a->coeffs);
      y10 = vld1q_s16(64 + b->coeffs);
      y5 = vld1q_s16(80 + a->coeffs);
      y11 = vld1q_s16(80 + b->coeffs);

      y12 = vmulq_s16(y0, y6);
      vst1q_s16(0 + r->coeffs, y12);

      y13 = vmulq_s16(y0, y7);
      y13 = vmlaq_s16(y13, y1, y6);
      vst1q_s16(16 + r->coeffs, y13);

      y12 = vmulq_s16(y0, y8);
      y12 = vmlaq_s16(y12, y1, y7);
      y12 = vmlaq_s16(y12, y2, y6);
      vst1q_s16(32 + r->coeffs, y12);

      y13 = vmulq_s16(y0, y9);
      y13 = vmlaq_s16(y13, y1, y8);
      y13 = vmlaq_s16(y13, y2, y7);
      y13 = vmlaq_s16(y13, y3, y6);
      vst1q_s16(48 + r->coeffs, y13);

      y12 = vmulq_s16(y0, y10);
      y12 = vmlaq_s16(y12, y1, y9);
      y12 = vmlaq_s16(y12, y2, y8);
      y12 = vmlaq_s16(y12, y3, y7);
      y12 = vmlaq_s16(y12, y4, y6);
      vst1q_s16(64 + r->coeffs, y12);

      y13 = vmulq_s16(y0, y11);
      y13 = vmlaq_s16(y13, y1, y10);
      y13 = vmlaq_s16(y13, y2, y9);
      y13 = vmlaq_s16(y13, y3, y8);
      y13 = vmlaq_s16(y13, y4, y7);
      y13 = vmlaq_s16(y13, y5, y6);
      vst1q_s16(80 + r->coeffs, y13);

      y12 = vmulq_s16(y1, y11);
      y12 = vmlaq_s16(y12, y2, y10);
      y12 = vmlaq_s16(y12, y3, y9);
      y12 = vmlaq_s16(y12, y4, y8);
      y12 = vmlaq_s16(y12, y5, y7);
      vst1q_s16(96 + r->coeffs, y12);

      y13 = vmulq_s16(y2, y11);
      y13 = vmlaq_s16(y13, y3, y10);
      y13 = vmlaq_s16(y13, y4, y9);
      y13 = vmlaq_s16(y13, y5, y8);
      vst1q_s16(112 + r->coeffs, y13);

      y12 = vmulq_s16(y3, y11);
      y12 = vmlaq_s16(y12, y4, y10);
      y12 = vmlaq_s16(y12, y5, y9);
      vst1q_s16(128 + r->coeffs, y12);

      y13 = vmulq_s16(y4, y11);
      y13 = vmlaq_s16(y13, y5, y10);
      vst1q_s16(144 + r->coeffs, y13);

      y12 = vmulq_s16(y5, y11);
      vst1q_s16(160 + r->coeffs, y12);

      y0 = vld1q_s16(96 + a->coeffs);
      y6 = vld1q_s16(96 + b->coeffs);
      y1 = vld1q_s16(112 + a->coeffs);
      y7 = vld1q_s16(112 + b->coeffs);
      y2 = vld1q_s16(128 + a->coeffs);
      y8 = vld1q_s16(128 + b->coeffs);
      y3 = vld1q_s16(144 + a->coeffs);
      y9 = vld1q_s16(144 + b->coeffs);
      y4 = vld1q_s16(160 + a->coeffs);
      y10 = vld1q_s16(160 + b->coeffs);

      y12 = vmulq_s16(y0, y6);
      vst1q_s16(192 + r->coeffs, y12);

      y13 = vmulq_s16(y0, y7);
      y13 = vmlaq_s16(y13, y1, y6);
      vst1q_s16(208 + r->coeffs, y13);

      y12 = vmulq_s16(y0, y8);
      y12 = vmlaq_s16(y12, y1, y7);
      y12 = vmlaq_s16(y12, y2, y6);
      vst1q_s16(224 + r->coeffs, y12);

      y13 = vmulq_s16(y0, y9);
      y13 = vmlaq_s16(y13, y1, y8);
      y13 = vmlaq_s16(y13, y2, y7);
      y13 = vmlaq_s16(y13, y3, y6);
      vst1q_s16(240 + r->coeffs, y13);

      y12 = vmulq_s16(y0, y10);
      y12 = vmlaq_s16(y12, y1, y9);
      y12 = vmlaq_s16(y12, y2, y8);
      y12 = vmlaq_s16(y12, y3, y7);
      y12 = vmlaq_s16(y12, y4, y6);
      vst1q_s16(256 + r->coeffs, y12);

      y13 = vmulq_s16(y1, y10);
      y13 = vmlaq_s16(y13, y2, y9);
      y13 = vmlaq_s16(y13, y3, y8);
      y13 = vmlaq_s16(y13, y4, y7);
      vst1q_s16(272 + r->coeffs, y13);

      y12 = vmulq_s16(y2, y10);
      y12 = vmlaq_s16(y12, y3, y9);
      y12 = vmlaq_s16(y12, y4, y8);
      vst1q_s16(288 + r->coeffs, y12);

      y13 = vmulq_s16(y3, y10);
      y13 = vmlaq_s16(y13, y4, y9);
      vst1q_s16(304 + r->coeffs, y13);

      y12 = vmulq_s16(y4, y10);
      vst1q_s16(320 + r->coeffs, y12);

      y12 = vld1q_s16(0 + a->coeffs);
      y0 = vaddq_s16(y12, y0);
      y12 = vld1q_s16(0 + b->coeffs);
      y6 = vaddq_s16(y12, y6);
      y12 = vld1q_s16(16 + a->coeffs);
      y1 = vaddq_s16(y12, y1);
      y12 = vld1q_s16(16 + b->coeffs);
      y7 = vaddq_s16(y12, y7);
      y12 = vld1q_s16(32 + a->coeffs);
      y2 = vaddq_s16(y12, y2);
      y12 = vld1q_s16(32 + b->coeffs);
      y8 = vaddq_s16(y12, y8);
      y12 = vld1q_s16(48 + a->coeffs);
      y3 = vaddq_s16(y12, y3);
      y12 = vld1q_s16(48 + b->coeffs);
      y9 = vaddq_s16(y12, y9);
      y12 = vld1q_s16(64 + a->coeffs);
      y4 = vaddq_s16(y12, y4);
      y12 = vld1q_s16(64 + b->coeffs);
      y10 = vaddq_s16(y12, y10);

      y12 = vmulq_s16(y0, y11);
      y12 = vmlaq_s16(y12, y1, y10);
      y12 = vmlaq_s16(y12, y2, y9);
      y12 = vmlaq_s16(y12, y3, y8);
      y12 = vmlaq_s16(y12, y4, y7);
      y12 = vmlaq_s16(y12, y5, y6);
      y13 = vld1q_s16(80 + r->coeffs);
      y12 = vsubq_s16(y12, y13);
      y13 = vld1q_s16(272 + r->coeffs);
      y12 = vsubq_s16(y12, y13);
      vst1q_s16(176 + r->coeffs, y12);

      y12 = vmulq_s16(y5, y7);
      y13 = vmulq_s16(y5, y8);
      y14 = vmulq_s16(y5, y9);
      y15 = vmulq_s16(y5, y10);

      y12 = vmlaq_s16(y12, y1, y11);
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

      y0 = vld1q_s16(96 + r->coeffs);
      y0 = vsubq_s16(y0, vld1q_s16(192 + r->coeffs));
      y6 = vsubq_s16(y12, y0);
      y6 = vsubq_s16(y6, vld1q_s16(288 + r->coeffs));
      vst1q_s16(192 + r->coeffs, y6);

      y0 = vaddq_s16(y7, y0);
      y0 = vsubq_s16(y0, vld1q_s16(0 + r->coeffs));
      vst1q_s16(96 + r->coeffs, y0);

      y1 = vld1q_s16(112 + r->coeffs);
      y1 = vsubq_s16(y1, vld1q_s16(208 + r->coeffs));
      y7 = vsubq_s16(y13, y1);
      y7 = vsubq_s16(y7, vld1q_s16(304 + r->coeffs));
      vst1q_s16(208 + r->coeffs, y7);

      y1 = vaddq_s16(y8, y1);
      y1 = vsubq_s16(y1, vld1q_s16(16 + r->coeffs));
      vst1q_s16(112 + r->coeffs, y1);

      y2 = vld1q_s16(128 + r->coeffs);
      y2 = vsubq_s16(y2, vld1q_s16(224 + r->coeffs));
      y8 = vsubq_s16(y14, y2);
      y8 = vsubq_s16(y8, vld1q_s16(320 + r->coeffs));
      vst1q_s16(224 + r->coeffs, y8);

      y2 = vaddq_s16(y9, y2);
      y2 = vsubq_s16(y2, vld1q_s16(32 + r->coeffs));
      vst1q_s16(128 + r->coeffs, y2);

      y3 = vld1q_s16(144 + r->coeffs);
      y3 = vsubq_s16(y3, vld1q_s16(240 + r->coeffs));
      y9 = vsubq_s16(y15, y3);
      vst1q_s16(240 + r->coeffs, y9);

      y3 = vaddq_s16(y10, y3);
      y3 = vsubq_s16(y3, vld1q_s16(48 + r->coeffs));
      vst1q_s16(144 + r->coeffs, y3);

      y4 = vld1q_s16(160 + r->coeffs);
      y3 = vld1q_s16(256 + r->coeffs);
      y4 = vsubq_s16(y4, y3);
      y4 = vaddq_s16(y11, y4);
      y9 = vld1q_s16(64 + r->coeffs);
      y4 = vsubq_s16(y4, y9);
      vst1q_s16(160 + r->coeffs, y4);

      // r->coeffs += 8;
      // a->coeffs += 8;
      // b->coeffs += 8;
    }
    // a->coeffs += N - 16;
    // b->coeffs += N - 16;
    // r->coeffs += 2 * N - 16;
  }
}

void K2_schoolbook_64x11_addictive(poly *r,  poly *a,  poly *b)
{
    int16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15;
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 2; j++)
    {
      y0 = vld1q_s16(0 + a->coeffs);
      y6 = vld1q_s16(0 + b->coeffs);
      y0 = vaddq_s16(vld1q_s16(176 + a->coeffs), y0);
      y6 = vaddq_s16(vld1q_s16(176 + b->coeffs), y6);
      y1 = vld1q_s16(16 + a->coeffs);
      y7 = vld1q_s16(16 + b->coeffs);
      y1 = vaddq_s16(vld1q_s16(192 + a->coeffs), y1);
      y7 = vaddq_s16(vld1q_s16(192 + b->coeffs), y7);
      y2 = vld1q_s16(32 + a->coeffs);
      y8 = vld1q_s16(32 + b->coeffs);
      y2 = vaddq_s16(vld1q_s16(208 + a->coeffs), y2);
      y8 = vaddq_s16(vld1q_s16(208 + b->coeffs), y8);
      y3 = vld1q_s16(48 + a->coeffs);
      y9 = vld1q_s16(48 + b->coeffs);
      y3 = vaddq_s16(vld1q_s16(224 + a->coeffs), y3);
      y9 = vaddq_s16(vld1q_s16(224 + b->coeffs), y9);
      y4 = vld1q_s16(64 + a->coeffs);
      y10 = vld1q_s16(64 + b->coeffs);
      y4 = vaddq_s16(vld1q_s16(240 + a->coeffs), y4);
      y10 = vaddq_s16(vld1q_s16(240 + b->coeffs), y10);
      y5 = vld1q_s16(80 + a->coeffs);
      y11 = vld1q_s16(80 + b->coeffs);
      y5 = vaddq_s16(vld1q_s16(256 + a->coeffs), y5);
      y11 = vaddq_s16(vld1q_s16(256 + b->coeffs), y11);
      y12 = vmulq_s16(y0, y6);
      vst1q_s16(0 + r->coeffs, y12);
      y13 = vmulq_s16(y0, y7);
      y13 = vmlaq_s16(y13, y1, y6);
      vst1q_s16(16 + r->coeffs, y13);
      y12 = vmulq_s16(y0, y8);
      y12 = vmlaq_s16(y12, y1, y7);
      y12 = vmlaq_s16(y12, y2, y6);
      vst1q_s16(32 + r->coeffs, y12);
      y13 = vmulq_s16(y0, y9);
      y13 = vmlaq_s16(y13, y1, y8);
      y13 = vmlaq_s16(y13, y2, y7);
      y13 = vmlaq_s16(y13, y3, y6);
      vst1q_s16(48 + r->coeffs, y13);
      y12 = vmulq_s16(y0, y10);
      y12 = vmlaq_s16(y12, y1, y9);
      y12 = vmlaq_s16(y12, y2, y8);
      y12 = vmlaq_s16(y12, y3, y7);
      y12 = vmlaq_s16(y12, y4, y6);
      vst1q_s16(64 + r->coeffs, y12);
      y13 = vmulq_s16(y0, y11);
      y13 = vmlaq_s16(y13, y1, y10);
      y13 = vmlaq_s16(y13, y2, y9);
      y13 = vmlaq_s16(y13, y3, y8);
      y13 = vmlaq_s16(y13, y4, y7);
      y13 = vmlaq_s16(y13, y5, y6);
      vst1q_s16(80 + r->coeffs, y13);
      y12 = vmulq_s16(y1, y11);
      y12 = vmlaq_s16(y12, y2, y10);
      y12 = vmlaq_s16(y12, y3, y9);
      y12 = vmlaq_s16(y12, y4, y8);
      y12 = vmlaq_s16(y12, y5, y7);
      vst1q_s16(96 + r->coeffs, y12);
      y13 = vmulq_s16(y2, y11);
      y13 = vmlaq_s16(y13, y3, y10);
      y13 = vmlaq_s16(y13, y4, y9);
      y13 = vmlaq_s16(y13, y5, y8);
      vst1q_s16(112 + r->coeffs, y13);
      y12 = vmulq_s16(y3, y11);
      y12 = vmlaq_s16(y12, y4, y10);
      y12 = vmlaq_s16(y12, y5, y9);
      vst1q_s16(128 + r->coeffs, y12);
      y13 = vmulq_s16(y4, y11);
      y13 = vmlaq_s16(y13, y5, y10);
      vst1q_s16(144 + r->coeffs, y13);
      y12 = vmulq_s16(y5, y11);
      vst1q_s16(160 + r->coeffs, y12);
      y0 = vld1q_s16(96 + a->coeffs);
      y6 = vld1q_s16(96 + b->coeffs);
      y0 = vaddq_s16(vld1q_s16(272 + a->coeffs), y0);
      y6 = vaddq_s16(vld1q_s16(272 + b->coeffs), y6);
      y1 = vld1q_s16(112 + a->coeffs);
      y7 = vld1q_s16(112 + b->coeffs);
      y1 = vaddq_s16(vld1q_s16(288 + a->coeffs), y1);
      y7 = vaddq_s16(vld1q_s16(288 + b->coeffs), y7);
      y2 = vld1q_s16(128 + a->coeffs);
      y8 = vld1q_s16(128 + b->coeffs);
      y2 = vaddq_s16(vld1q_s16(304 + a->coeffs), y2);
      y8 = vaddq_s16(vld1q_s16(304 + b->coeffs), y8);
      y3 = vld1q_s16(144 + a->coeffs);
      y9 = vld1q_s16(144 + b->coeffs);
      y3 = vaddq_s16(vld1q_s16(320 + a->coeffs), y3);
      y9 = vaddq_s16(vld1q_s16(320 + b->coeffs), y9);
      y4 = vld1q_s16(160 + a->coeffs);
      y10 = vld1q_s16(160 + b->coeffs);
      y4 = vaddq_s16(vld1q_s16(336 + a->coeffs), y4);
      y10 = vaddq_s16(vld1q_s16(336 + b->coeffs), y10);
      y12 = vmulq_s16(y0, y6);
      vst1q_s16(192 + r->coeffs, y12);
      y13 = vmulq_s16(y0, y7);
      y13 = vmlaq_s16(y13, y1, y6);
      vst1q_s16(208 + r->coeffs, y13);
      y12 = vmulq_s16(y0, y8);
      y12 = vmlaq_s16(y12, y1, y7);
      y12 = vmlaq_s16(y12, y2, y6);
      vst1q_s16(224 + r->coeffs, y12);
      y13 = vmulq_s16(y0, y9);
      y13 = vmlaq_s16(y13, y1, y8);
      y13 = vmlaq_s16(y13, y2, y7);
      y13 = vmlaq_s16(y13, y3, y6);
      vst1q_s16(240 + r->coeffs, y13);
      y12 = vmulq_s16(y0, y10);
      y12 = vmlaq_s16(y12, y1, y9);
      y12 = vmlaq_s16(y12, y2, y8);
      y12 = vmlaq_s16(y12, y3, y7);
      y12 = vmlaq_s16(y12, y4, y6);
      vst1q_s16(256 + r->coeffs, y12);
      y13 = vmulq_s16(y1, y10);
      y13 = vmlaq_s16(y13, y2, y9);
      y13 = vmlaq_s16(y13, y3, y8);
      y13 = vmlaq_s16(y13, y4, y7);
      vst1q_s16(272 + r->coeffs, y13);
      y12 = vmulq_s16(y2, y10);
      y12 = vmlaq_s16(y12, y3, y9);
      y12 = vmlaq_s16(y12, y4, y8);
      vst1q_s16(288 + r->coeffs, y12);
      y13 = vmulq_s16(y3, y10);
      y13 = vmlaq_s16(y13, y4, y9);
      vst1q_s16(304 + r->coeffs, y13);
      y12 = vmulq_s16(y4, y10);
      vst1q_s16(320 + r->coeffs, y12);
      y12 = vld1q_s16(0 + a->coeffs);
      y0 = vaddq_s16(y12, y0);
      y12 = vld1q_s16(0 + b->coeffs);
      y6 = vaddq_s16(y12, y6);
      y12 = vld1q_s16(176 + a->coeffs);
      y0 = vaddq_s16(y12, y0);
      y12 = vld1q_s16(176 + b->coeffs);
      y6 = vaddq_s16(y12, y6);
      y12 = vld1q_s16(16 + a->coeffs);
      y1 = vaddq_s16(y12, y1);
      y12 = vld1q_s16(16 + b->coeffs);
      y7 = vaddq_s16(y12, y7);
      y12 = vld1q_s16(192 + a->coeffs);
      y1 = vaddq_s16(y12, y1);
      y12 = vld1q_s16(192 + b->coeffs);
      y7 = vaddq_s16(y12, y7);
      y12 = vld1q_s16(32 + a->coeffs);
      y2 = vaddq_s16(y12, y2);
      y12 = vld1q_s16(32 + b->coeffs);
      y8 = vaddq_s16(y12, y8);
      y12 = vld1q_s16(208 + a->coeffs);
      y2 = vaddq_s16(y12, y2);
      y12 = vld1q_s16(208 + b->coeffs);
      y8 = vaddq_s16(y12, y8);
      y12 = vld1q_s16(48 + a->coeffs);
      y3 = vaddq_s16(y12, y3);
      y12 = vld1q_s16(48 + b->coeffs);
      y9 = vaddq_s16(y12, y9);
      y12 = vld1q_s16(224 + a->coeffs);
      y3 = vaddq_s16(y12, y3);
      y12 = vld1q_s16(224 + b->coeffs);
      y9 = vaddq_s16(y12, y9);
      y12 = vld1q_s16(64 + a->coeffs);
      y4 = vaddq_s16(y12, y4);
      y12 = vld1q_s16(64 + b->coeffs);
      y10 = vaddq_s16(y12, y10);
      y12 = vld1q_s16(240 + a->coeffs);
      y4 = vaddq_s16(y12, y4);
      y12 = vld1q_s16(240 + b->coeffs);
      y10 = vaddq_s16(y12, y10);
      y12 = vmulq_s16(y0, y11);
      y12 = vmlaq_s16(y12, y1, y10);
      y12 = vmlaq_s16(y12, y2, y9);
      y12 = vmlaq_s16(y12, y3, y8);
      y12 = vmlaq_s16(y12, y4, y7);
      y12 = vmlaq_s16(y12, y5, y6);
      y12 = vsubq_s16(y12, vld1q_s16(80 + r->coeffs));
      y12 = vsubq_s16(y12, vld1q_s16(272 + r->coeffs));
      vst1q_s16(176 + r->coeffs, y12);
      y12 = vmulq_s16(y5, y7);
      y13 = vmulq_s16(y5, y8);
      y14 = vmulq_s16(y5, y9);
      y15 = vmulq_s16(y5, y10);
      y12 = vmlaq_s16(y12, y1, y11);
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
      y0 = vld1q_s16(96 + r->coeffs);
      y0 = vsubq_s16(y0, vld1q_s16(192 + r->coeffs));
      y6 = vsubq_s16(y12, y0);
      y6 = vsubq_s16(y6, vld1q_s16(288 + r->coeffs));
      vst1q_s16(192 + r->coeffs, y6);
      y0 = vaddq_s16(y7, y0);
      y0 = vsubq_s16(y0, vld1q_s16(0 + r->coeffs));
      vst1q_s16(96 + r->coeffs, y0);
      y1 = vld1q_s16(112 + r->coeffs);
      y1 = vsubq_s16(y1, vld1q_s16(208 + r->coeffs));
      y7 = vsubq_s16(y13, y1);
      y7 = vsubq_s16(y7, vld1q_s16(304 + r->coeffs));
      vst1q_s16(208 + r->coeffs, y7);
      y1 = vaddq_s16(y8, y1);
      y1 = vsubq_s16(y1, vld1q_s16(16 + r->coeffs));
      vst1q_s16(112 + r->coeffs, y1);
      y2 = vld1q_s16(128 + r->coeffs);
      y2 = vsubq_s16(y2, vld1q_s16(224 + r->coeffs));
      y8 = vsubq_s16(y14, y2);
      y8 = vsubq_s16(y8, vld1q_s16(320 + r->coeffs));
      vst1q_s16(224 + r->coeffs, y8);
      y2 = vaddq_s16(y9, y2);
      y2 = vsubq_s16(y2, vld1q_s16(32 + r->coeffs));
      vst1q_s16(128 + r->coeffs, y2);
      y3 = vld1q_s16(144 + r->coeffs);
      y3 = vsubq_s16(y3, vld1q_s16(240 + r->coeffs));
      y9 = vsubq_s16(y15, y3);
      vst1q_s16(240 + r->coeffs, y9);
      y3 = vaddq_s16(y10, y3);
      y3 = vsubq_s16(y3, vld1q_s16(48 + r->coeffs));
      vst1q_s16(144 + r->coeffs, y3);
      y4 = vld1q_s16(160 + r->coeffs);
      y4 = vsubq_s16(y4, vld1q_s16(256 + r->coeffs));
      y4 = vaddq_s16(y11, y4);
      y4 = vsubq_s16(y4, vld1q_s16(64 + r->coeffs));
      vst1q_s16(160 + r->coeffs, y4);

      // r->coeffs += 8;
      // a->coeffs += 8;
      // b->coeffs += 8;
    }
    // a->coeffs += N - 16;
    // b->coeffs += N - 16;
    // r->coeffs += 2 * N - 16;
  }
}

int main()
{
  return 0;
}