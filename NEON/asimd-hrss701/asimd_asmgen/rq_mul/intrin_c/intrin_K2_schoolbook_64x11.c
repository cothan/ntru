#include <arm_neon.h>
#include <stdio.h>

void K2_schoolbook_64x11(uint16_t *c, uint16_t *a, uint16_t *b)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31;
    for (int i = 0; i < 4; i++)
    {
    
y0 = vld1q_s16(0 + a);
y6 = vld1q_s16(0 + b);
y16 = vld1q_s16(8 + a);
y22 = vld1q_s16(8 + b);
y1 = vld1q_s16(16 + a);
y7 = vld1q_s16(16 + b);
y17 = vld1q_s16(24 + a);
y23 = vld1q_s16(24 + b);
y2 = vld1q_s16(32 + a);
y8 = vld1q_s16(32 + b);
y18 = vld1q_s16(40 + a);
y24 = vld1q_s16(40 + b);
y3 = vld1q_s16(48 + a);
y9 = vld1q_s16(48 + b);
y19 = vld1q_s16(56 + a);
y25 = vld1q_s16(56 + b);
y4 = vld1q_s16(64 + a);
y10 = vld1q_s16(64 + b);
y20 = vld1q_s16(72 + a);
y26 = vld1q_s16(72 + b);
y5 = vld1q_s16(80 + a);
y11 = vld1q_s16(80 + b);
y21 = vld1q_s16(88 + a);
y27 = vld1q_s16(88 + b);
y12 = vmulq_s16(y0, y6);
y28 = vmulq_s16(y16, y22);
vst1q_u16(0 + c, y12);
vst1q_u16(8 + c, y28);
y13 = vmulq_s16(y0, y7);
y29 = vmulq_s16(y16, y23);
y13 = vmlaq_s16 (y13, y1, y6);
y29 = vmlaq_s16 (y29, y17, y22);
vst1q_u16(16 + c, y13);
vst1q_u16(24 + c, y29);
y12 = vmulq_s16(y0, y8);
y28 = vmulq_s16(y16, y24);
y12 = vmlaq_s16 (y12, y1, y7);
y28 = vmlaq_s16 (y28, y17, y23);
y12 = vmlaq_s16 (y12, y2, y6);
y28 = vmlaq_s16 (y28, y18, y22);
vst1q_u16(32 + c, y12);
vst1q_u16(40 + c, y28);
y13 = vmulq_s16(y0, y9);
y29 = vmulq_s16(y16, y25);
y13 = vmlaq_s16 (y13, y1, y8);
y29 = vmlaq_s16 (y29, y17, y24);
y13 = vmlaq_s16 (y13, y2, y7);
y29 = vmlaq_s16 (y29, y18, y23);
y13 = vmlaq_s16 (y13, y3, y6);
y29 = vmlaq_s16 (y29, y19, y22);
vst1q_u16(48 + c, y13);
vst1q_u16(56 + c, y29);
y12 = vmulq_s16(y0, y10);
y28 = vmulq_s16(y16, y26);
y12 = vmlaq_s16 (y12, y1, y9);
y28 = vmlaq_s16 (y28, y17, y25);
y12 = vmlaq_s16 (y12, y2, y8);
y28 = vmlaq_s16 (y28, y18, y24);
y12 = vmlaq_s16 (y12, y3, y7);
y28 = vmlaq_s16 (y28, y19, y23);
y12 = vmlaq_s16 (y12, y4, y6);
y28 = vmlaq_s16 (y28, y20, y22);
vst1q_u16(64 + c, y12);
vst1q_u16(72 + c, y28);
y13 = vmulq_s16(y0, y11);
y29 = vmulq_s16(y16, y27);
y13 = vmlaq_s16 (y13, y1, y10);
y29 = vmlaq_s16 (y29, y17, y26);
y13 = vmlaq_s16 (y13, y2, y9);
y29 = vmlaq_s16 (y29, y18, y25);
y13 = vmlaq_s16 (y13, y3, y8);
y29 = vmlaq_s16 (y29, y19, y24);
y13 = vmlaq_s16 (y13, y4, y7);
y29 = vmlaq_s16 (y29, y20, y23);
y13 = vmlaq_s16 (y13, y5, y6);
y29 = vmlaq_s16 (y29, y21, y22);
vst1q_u16(80 + c, y13);
vst1q_u16(88 + c, y29);
y12 = vmulq_s16(y1, y11);
y28 = vmulq_s16(y17, y27);
y12 = vmlaq_s16 (y12, y2, y10);
y28 = vmlaq_s16 (y28, y18, y26);
y12 = vmlaq_s16 (y12, y3, y9);
y28 = vmlaq_s16 (y28, y19, y25);
y12 = vmlaq_s16 (y12, y4, y8);
y28 = vmlaq_s16 (y28, y20, y24);
y12 = vmlaq_s16 (y12, y5, y7);
y28 = vmlaq_s16 (y28, y21, y23);
vst1q_u16(96 + c, y12);
vst1q_u16(104 + c, y28);
y13 = vmulq_s16(y2, y11);
y29 = vmulq_s16(y18, y27);
y13 = vmlaq_s16 (y13, y3, y10);
y29 = vmlaq_s16 (y29, y19, y26);
y13 = vmlaq_s16 (y13, y4, y9);
y29 = vmlaq_s16 (y29, y20, y25);
y13 = vmlaq_s16 (y13, y5, y8);
y29 = vmlaq_s16 (y29, y21, y24);
vst1q_u16(112 + c, y13);
vst1q_u16(120 + c, y29);
y12 = vmulq_s16(y3, y11);
y28 = vmulq_s16(y19, y27);
y12 = vmlaq_s16 (y12, y4, y10);
y28 = vmlaq_s16 (y28, y20, y26);
y12 = vmlaq_s16 (y12, y5, y9);
y28 = vmlaq_s16 (y28, y21, y25);
vst1q_u16(128 + c, y12);
vst1q_u16(136 + c, y28);
y13 = vmulq_s16(y4, y11);
y29 = vmulq_s16(y20, y27);
y13 = vmlaq_s16 (y13, y5, y10);
y29 = vmlaq_s16 (y29, y21, y26);
vst1q_u16(144 + c, y13);
vst1q_u16(152 + c, y29);
y12 = vmulq_s16(y5, y11);
y28 = vmulq_s16(y21, y27);
vst1q_u16(160 + c, y12);
vst1q_u16(168 + c, y28);
y0 = vld1q_s16(96 + a);
y6 = vld1q_s16(96 + b);
y16 = vld1q_s16(104 + a);
y22 = vld1q_s16(104 + b);
y1 = vld1q_s16(112 + a);
y7 = vld1q_s16(112 + b);
y17 = vld1q_s16(120 + a);
y23 = vld1q_s16(120 + b);
y2 = vld1q_s16(128 + a);
y8 = vld1q_s16(128 + b);
y18 = vld1q_s16(136 + a);
y24 = vld1q_s16(136 + b);
y3 = vld1q_s16(144 + a);
y9 = vld1q_s16(144 + b);
y19 = vld1q_s16(152 + a);
y25 = vld1q_s16(152 + b);
y4 = vld1q_s16(160 + a);
y10 = vld1q_s16(160 + b);
y20 = vld1q_s16(168 + a);
y26 = vld1q_s16(168 + b);
y12 = vmulq_s16(y0, y6);
y28 = vmulq_s16(y16, y22);
vst1q_u16(192 + c, y12);
vst1q_u16(200 + c, y28);
y13 = vmulq_s16(y0, y7);
y29 = vmulq_s16(y16, y23);
y13 = vmlaq_s16 (y13, y1, y6);
y29 = vmlaq_s16 (y29, y17, y22);
vst1q_u16(208 + c, y13);
vst1q_u16(216 + c, y29);
y12 = vmulq_s16(y0, y8);
y28 = vmulq_s16(y16, y24);
y12 = vmlaq_s16 (y12, y1, y7);
y28 = vmlaq_s16 (y28, y17, y23);
y12 = vmlaq_s16 (y12, y2, y6);
y28 = vmlaq_s16 (y28, y18, y22);
vst1q_u16(224 + c, y12);
vst1q_u16(232 + c, y28);
y13 = vmulq_s16(y0, y9);
y29 = vmulq_s16(y16, y25);
y13 = vmlaq_s16 (y13, y1, y8);
y29 = vmlaq_s16 (y29, y17, y24);
y13 = vmlaq_s16 (y13, y2, y7);
y29 = vmlaq_s16 (y29, y18, y23);
y13 = vmlaq_s16 (y13, y3, y6);
y29 = vmlaq_s16 (y29, y19, y22);
vst1q_u16(240 + c, y13);
vst1q_u16(248 + c, y29);
y12 = vmulq_s16(y0, y10);
y28 = vmulq_s16(y16, y26);
y12 = vmlaq_s16 (y12, y1, y9);
y28 = vmlaq_s16 (y28, y17, y25);
y12 = vmlaq_s16 (y12, y2, y8);
y28 = vmlaq_s16 (y28, y18, y24);
y12 = vmlaq_s16 (y12, y3, y7);
y28 = vmlaq_s16 (y28, y19, y23);
y12 = vmlaq_s16 (y12, y4, y6);
y28 = vmlaq_s16 (y28, y20, y22);
vst1q_u16(256 + c, y12);
vst1q_u16(264 + c, y28);
y13 = vmulq_s16(y1, y10);
y29 = vmulq_s16(y17, y26);
y13 = vmlaq_s16 (y13, y2, y9);
y29 = vmlaq_s16 (y29, y18, y25);
y13 = vmlaq_s16 (y13, y3, y8);
y29 = vmlaq_s16 (y29, y19, y24);
y13 = vmlaq_s16 (y13, y4, y7);
y29 = vmlaq_s16 (y29, y20, y23);
vst1q_u16(272 + c, y13);
vst1q_u16(280 + c, y29);
y12 = vmulq_s16(y2, y10);
y28 = vmulq_s16(y18, y26);
y12 = vmlaq_s16 (y12, y3, y9);
y28 = vmlaq_s16 (y28, y19, y25);
y12 = vmlaq_s16 (y12, y4, y8);
y28 = vmlaq_s16 (y28, y20, y24);
vst1q_u16(288 + c, y12);
vst1q_u16(296 + c, y28);
y13 = vmulq_s16(y3, y10);
y29 = vmulq_s16(y19, y26);
y13 = vmlaq_s16 (y13, y4, y9);
y29 = vmlaq_s16 (y29, y20, y25);
vst1q_u16(304 + c, y13);
vst1q_u16(312 + c, y29);
y12 = vmulq_s16(y4, y10);
y28 = vmulq_s16(y20, y26);
vst1q_u16(320 + c, y12);
vst1q_u16(328 + c, y28);
y12 = vld1q_s16(0 + a);
y0 = vaddq_s16(y12, y0);
y12 = vld1q_s16(0 + b);
y6 = vaddq_s16(y12, y6);
y28 = vld1q_s16(8 + a);
y16 = vaddq_s16(y28, y16);
y28 = vld1q_s16(8 + b);
y22 = vaddq_s16(y28, y22);
y12 = vld1q_s16(16 + a);
y1 = vaddq_s16(y12, y1);
y12 = vld1q_s16(16 + b);
y7 = vaddq_s16(y12, y7);
y28 = vld1q_s16(24 + a);
y17 = vaddq_s16(y28, y17);
y28 = vld1q_s16(24 + b);
y23 = vaddq_s16(y28, y23);
y12 = vld1q_s16(32 + a);
y2 = vaddq_s16(y12, y2);
y12 = vld1q_s16(32 + b);
y8 = vaddq_s16(y12, y8);
y28 = vld1q_s16(40 + a);
y18 = vaddq_s16(y28, y18);
y28 = vld1q_s16(40 + b);
y24 = vaddq_s16(y28, y24);
y12 = vld1q_s16(48 + a);
y3 = vaddq_s16(y12, y3);
y12 = vld1q_s16(48 + b);
y9 = vaddq_s16(y12, y9);
y28 = vld1q_s16(56 + a);
y19 = vaddq_s16(y28, y19);
y28 = vld1q_s16(56 + b);
y25 = vaddq_s16(y28, y25);
y12 = vld1q_s16(64 + a);
y4 = vaddq_s16(y12, y4);
y12 = vld1q_s16(64 + b);
y10 = vaddq_s16(y12, y10);
y28 = vld1q_s16(72 + a);
y20 = vaddq_s16(y28, y20);
y28 = vld1q_s16(72 + b);
y26 = vaddq_s16(y28, y26);
y12 = vmulq_s16(y0, y11);
y28 = vmulq_s16(y16, y27);
y12 = vmlaq_s16 (y12, y1, y10);
y28 = vmlaq_s16 (y28, y17, y26);
y12 = vmlaq_s16 (y12, y2, y9);
y28 = vmlaq_s16 (y28, y18, y25);
y12 = vmlaq_s16 (y12, y3, y8);
y28 = vmlaq_s16 (y28, y19, y24);
y12 = vmlaq_s16 (y12, y4, y7);
y28 = vmlaq_s16 (y28, y20, y23);
y12 = vmlaq_s16 (y12, y5, y6);
y28 = vmlaq_s16 (y28, y21, y22);
y12 = vsubq_s16 (y12, vld1q_s16(80+c));
y12 = vsubq_s16 (y12, vld1q_s16(272+c));
vst1q_u16(176 + c, y12);
y28 = vsubq_s16 (y28, vld1q_s16(88+c));
y28 = vsubq_s16 (y28, vld1q_s16(280+c));
vst1q_u16(184 + c, y28);
y12 = vmulq_s16(y5, y7);
y28 = vmulq_s16(y21, y23);
y13 = vmulq_s16(y5, y8);
y29 = vmulq_s16(y21, y24);
y14 = vmulq_s16(y5, y9);
y30 = vmulq_s16(y21, y25);
y15 = vmulq_s16(y5, y10);
y31 = vmulq_s16(y21, y26);
y12 = vmlaq_s16 (y12, y1, y11);
y28 = vmlaq_s16 (y28, y17, y27);
y12 = vmlaq_s16 (y12, y2, y10);
y28 = vmlaq_s16 (y28, y18, y26);
y12 = vmlaq_s16 (y12, y3, y9);
y28 = vmlaq_s16 (y28, y19, y25);
y12 = vmlaq_s16 (y12, y4, y8);
y28 = vmlaq_s16 (y28, y20, y24);
y13 = vmlaq_s16 (y13, y2, y11);
y29 = vmlaq_s16 (y29, y18, y27);
y13 = vmlaq_s16 (y13, y3, y10);
y29 = vmlaq_s16 (y29, y19, y26);
y13 = vmlaq_s16 (y13, y4, y9);
y29 = vmlaq_s16 (y29, y20, y25);
y14 = vmlaq_s16 (y14, y3, y11);
y30 = vmlaq_s16 (y30, y19, y27);
y14 = vmlaq_s16 (y14, y4, y10);
y30 = vmlaq_s16 (y30, y20, y26);
y15 = vmlaq_s16 (y15, y4, y11);
y31 = vmlaq_s16 (y31, y20, y27);
y11 = vmulq_s16(y0, y10);
y27 = vmulq_s16(y16, y26);
y11 = vmlaq_s16 (y11, y1, y9);
y27 = vmlaq_s16 (y27, y17, y25);
y11 = vmlaq_s16 (y11, y2, y8);
y27 = vmlaq_s16 (y27, y18, y24);
y11 = vmlaq_s16 (y11, y3, y7);
y27 = vmlaq_s16 (y27, y19, y23);
y11 = vmlaq_s16 (y11, y4, y6);
y27 = vmlaq_s16 (y27, y20, y22);
y10 = vmulq_s16(y0, y9);
y26 = vmulq_s16(y16, y25);
y10 = vmlaq_s16 (y10, y1, y8);
y26 = vmlaq_s16 (y26, y17, y24);
y10 = vmlaq_s16 (y10, y2, y7);
y26 = vmlaq_s16 (y26, y18, y23);
y10 = vmlaq_s16 (y10, y3, y6);
y26 = vmlaq_s16 (y26, y19, y22);
y9 = vmulq_s16(y0, y8);
y25 = vmulq_s16(y16, y24);
y9 = vmlaq_s16 (y9, y1, y7);
y25 = vmlaq_s16 (y25, y17, y23);
y9 = vmlaq_s16 (y9, y2, y6);
y25 = vmlaq_s16 (y25, y18, y22);
y8 = vmulq_s16(y0, y7);
y24 = vmulq_s16(y16, y23);
y8 = vmlaq_s16 (y8, y1, y6);
y24 = vmlaq_s16 (y24, y17, y22);
y7 = vmulq_s16(y0, y6);
y23 = vmulq_s16(y16, y22);
y0 = vld1q_s16(96 + c);
y16 = vld1q_s16(104 + c);
y0 = vsubq_s16 (y0, vld1q_s16(192+c) );
y16 = vsubq_s16 (y16, vld1q_s16(200+c) );
y6 = vsubq_s16(y12, y0);
y22 = vsubq_s16(y22, y16);
y6 = vsubq_s16 ( y6, vld1q_s16(288+c));
y22 = vsubq_s16 ( y22, vld1q_s16(296+c));
vst1q_u16(192 + c, y6);
vst1q_u16(200 + c, y22);
y0 = vaddq_s16(y7, y0);
y16 = vaddq_s16(y16, y16);
y0 = vsubq_s16 (y0, vld1q_s16(0+c));
y16 = vsubq_s16 (y16, vld1q_s16(8+c));
vst1q_u16(96 + c, y0);
vst1q_u16(104 + c, y16);
y1 = vld1q_s16(112 + c);
y17 = vld1q_s16(120 + c);
y1 = vsubq_s16 (y1, vld1q_s16(208+c) );
y17 = vsubq_s16 (y17, vld1q_s16(216+c) );
y7 = vsubq_s16(y13, y1);
y23 = vsubq_s16(y23, y17);
y7 = vsubq_s16 ( y7, vld1q_s16(304+c));
y23 = vsubq_s16 ( y23, vld1q_s16(312+c));
vst1q_u16(208 + c, y7);
vst1q_u16(216 + c, y23);
y1 = vaddq_s16(y8, y1);
y17 = vaddq_s16(y17, y17);
y1 = vsubq_s16 (y1, vld1q_s16(16+c));
y17 = vsubq_s16 (y17, vld1q_s16(24+c));
vst1q_u16(112 + c, y1);
vst1q_u16(120 + c, y17);
y2 = vld1q_s16(128 + c);
y18 = vld1q_s16(136 + c);
y2 = vsubq_s16 (y2, vld1q_s16(224+c) );
y18 = vsubq_s16 (y18, vld1q_s16(232+c) );
y8 = vsubq_s16(y14, y2);
y24 = vsubq_s16(y24, y18);
y8 = vsubq_s16 ( y8, vld1q_s16(320+c));
y24 = vsubq_s16 ( y24, vld1q_s16(328+c));
vst1q_u16(224 + c, y8);
vst1q_u16(232 + c, y24);
y2 = vaddq_s16(y9, y2);
y18 = vaddq_s16(y18, y18);
y2 = vsubq_s16 (y2, vld1q_s16(32+c));
y18 = vsubq_s16 (y18, vld1q_s16(40+c));
vst1q_u16(128 + c, y2);
vst1q_u16(136 + c, y18);
y3 = vld1q_s16(144 + c);
y19 = vld1q_s16(152 + c);
y3 = vsubq_s16 (y3, vld1q_s16(240+c) );
y19 = vsubq_s16 (y19, vld1q_s16(248+c) );
y9 = vsubq_s16(y15, y3);
y25 = vsubq_s16(y25, y19);
vst1q_u16(240 + c, y9);
vst1q_u16(248 + c, y25);
y3 = vaddq_s16(y10, y3);
y19 = vaddq_s16(y19, y19);
y3 = vsubq_s16 (y3, vld1q_s16(48+c));
y19 = vsubq_s16 (y19, vld1q_s16(56+c));
vst1q_u16(144 + c, y3);
vst1q_u16(152 + c, y19);
y4 = vld1q_s16(160 + c);
y20 = vld1q_s16(168 + c);
y4 = vsubq_s16 (y4, vld1q_s16(256+c) );
y20 = vsubq_s16 (y20, vld1q_s16(264+c) );
y4 = vaddq_s16(y11, y4);
y20 = vaddq_s16(y20, y20);
y4 = vsubq_s16 (y4, vld1q_s16(64+c));
y20 = vsubq_s16 (y20, vld1q_s16(72+c));
vst1q_u16(160 + c, y4);
vst1q_u16(168 + c, y20);

    a += 704; 
    b += 704; 
    c += 1408;
    }
}
    

void K2_schoolbook_64x11_additive(uint16_t *c, uint16_t *a, uint16_t *b)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31;
    for (int i = 0; i < 4; i++)
    {
y0 = vld1q_s16(0 + a);
y6 = vld1q_s16(0 + b);
y16 = vld1q_s16(8 + a);
y22 = vld1q_s16(8 + b);
y0 = vaddq_s16 (vld1q_s16(176+a), y0);
y6 = vaddq_s16 (vld1q_s16(176+b), y6);
y16 = vaddq_s16 (vld1q_s16(184+a), y16);
y22 = vaddq_s16 (vld1q_s16(184+b), y22);
y1 = vld1q_s16(16 + a);
y7 = vld1q_s16(16 + b);
y17 = vld1q_s16(24 + a);
y23 = vld1q_s16(24 + b);
y1 = vaddq_s16 (vld1q_s16(192+a), y1);
y7 = vaddq_s16 (vld1q_s16(192+b), y7);
y17 = vaddq_s16 (vld1q_s16(200+a), y17);
y23 = vaddq_s16 (vld1q_s16(200+b), y23);
y2 = vld1q_s16(32 + a);
y8 = vld1q_s16(32 + b);
y18 = vld1q_s16(40 + a);
y24 = vld1q_s16(40 + b);
y2 = vaddq_s16 (vld1q_s16(208+a), y2);
y8 = vaddq_s16 (vld1q_s16(208+b), y8);
y18 = vaddq_s16 (vld1q_s16(216+a), y18);
y24 = vaddq_s16 (vld1q_s16(216+b), y24);
y3 = vld1q_s16(48 + a);
y9 = vld1q_s16(48 + b);
y19 = vld1q_s16(56 + a);
y25 = vld1q_s16(56 + b);
y3 = vaddq_s16 (vld1q_s16(224+a), y3);
y9 = vaddq_s16 (vld1q_s16(224+b), y9);
y19 = vaddq_s16 (vld1q_s16(232+a), y19);
y25 = vaddq_s16 (vld1q_s16(232+b), y25);
y4 = vld1q_s16(64 + a);
y10 = vld1q_s16(64 + b);
y20 = vld1q_s16(72 + a);
y26 = vld1q_s16(72 + b);
y4 = vaddq_s16 (vld1q_s16(240+a), y4);
y10 = vaddq_s16 (vld1q_s16(240+b), y10);
y20 = vaddq_s16 (vld1q_s16(248+a), y20);
y26 = vaddq_s16 (vld1q_s16(248+b), y26);
y5 = vld1q_s16(80 + a);
y11 = vld1q_s16(80 + b);
y21 = vld1q_s16(88 + a);
y27 = vld1q_s16(88 + b);
y5 = vaddq_s16 (vld1q_s16(256+a), y5);
y11 = vaddq_s16 (vld1q_s16(256+b), y11);
y21 = vaddq_s16 (vld1q_s16(264+a), y21);
y27 = vaddq_s16 (vld1q_s16(264+b), y27);
y12 = vmulq_s16(y0, y6);
y28 = vmulq_s16(y16, y22);
vst1q_u16(0 + c, y12);
vst1q_u16(8 + c, y28);
y13 = vmulq_s16(y0, y7);
y29 = vmulq_s16(y16, y23);
y13 = vmlaq_s16 (y13, y1, y6);
y29 = vmlaq_s16 (y29, y17, y22);
vst1q_u16(16 + c, y13);
vst1q_u16(24 + c, y29);
y12 = vmulq_s16(y0, y8);
y28 = vmulq_s16(y16, y24);
y12 = vmlaq_s16 (y12, y1, y7);
y28 = vmlaq_s16 (y28, y17, y23);
y12 = vmlaq_s16 (y12, y2, y6);
y28 = vmlaq_s16 (y28, y18, y22);
vst1q_u16(32 + c, y12);
vst1q_u16(40 + c, y28);
y13 = vmulq_s16(y0, y9);
y29 = vmulq_s16(y16, y25);
y13 = vmlaq_s16 (y13, y1, y8);
y29 = vmlaq_s16 (y29, y17, y24);
y13 = vmlaq_s16 (y13, y2, y7);
y29 = vmlaq_s16 (y29, y18, y23);
y13 = vmlaq_s16 (y13, y3, y6);
y29 = vmlaq_s16 (y29, y19, y22);
vst1q_u16(48 + c, y13);
vst1q_u16(56 + c, y29);
y12 = vmulq_s16(y0, y10);
y28 = vmulq_s16(y16, y26);
y12 = vmlaq_s16 (y12, y1, y9);
y28 = vmlaq_s16 (y28, y17, y25);
y12 = vmlaq_s16 (y12, y2, y8);
y28 = vmlaq_s16 (y28, y18, y24);
y12 = vmlaq_s16 (y12, y3, y7);
y28 = vmlaq_s16 (y28, y19, y23);
y12 = vmlaq_s16 (y12, y4, y6);
y28 = vmlaq_s16 (y28, y20, y22);
vst1q_u16(64 + c, y12);
vst1q_u16(72 + c, y28);
y13 = vmulq_s16(y0, y11);
y29 = vmulq_s16(y16, y27);
y13 = vmlaq_s16 (y13, y1, y10);
y29 = vmlaq_s16 (y29, y17, y26);
y13 = vmlaq_s16 (y13, y2, y9);
y29 = vmlaq_s16 (y29, y18, y25);
y13 = vmlaq_s16 (y13, y3, y8);
y29 = vmlaq_s16 (y29, y19, y24);
y13 = vmlaq_s16 (y13, y4, y7);
y29 = vmlaq_s16 (y29, y20, y23);
y13 = vmlaq_s16 (y13, y5, y6);
y29 = vmlaq_s16 (y29, y21, y22);
vst1q_u16(80 + c, y13);
vst1q_u16(88 + c, y29);
y12 = vmulq_s16(y1, y11);
y28 = vmulq_s16(y17, y27);
y12 = vmlaq_s16 (y12, y2, y10);
y28 = vmlaq_s16 (y28, y18, y26);
y12 = vmlaq_s16 (y12, y3, y9);
y28 = vmlaq_s16 (y28, y19, y25);
y12 = vmlaq_s16 (y12, y4, y8);
y28 = vmlaq_s16 (y28, y20, y24);
y12 = vmlaq_s16 (y12, y5, y7);
y28 = vmlaq_s16 (y28, y21, y23);
vst1q_u16(96 + c, y12);
vst1q_u16(104 + c, y28);
y13 = vmulq_s16(y2, y11);
y29 = vmulq_s16(y18, y27);
y13 = vmlaq_s16 (y13, y3, y10);
y29 = vmlaq_s16 (y29, y19, y26);
y13 = vmlaq_s16 (y13, y4, y9);
y29 = vmlaq_s16 (y29, y20, y25);
y13 = vmlaq_s16 (y13, y5, y8);
y29 = vmlaq_s16 (y29, y21, y24);
vst1q_u16(112 + c, y13);
vst1q_u16(120 + c, y29);
y12 = vmulq_s16(y3, y11);
y28 = vmulq_s16(y19, y27);
y12 = vmlaq_s16 (y12, y4, y10);
y28 = vmlaq_s16 (y28, y20, y26);
y12 = vmlaq_s16 (y12, y5, y9);
y28 = vmlaq_s16 (y28, y21, y25);
vst1q_u16(128 + c, y12);
vst1q_u16(136 + c, y28);
y13 = vmulq_s16(y4, y11);
y29 = vmulq_s16(y20, y27);
y13 = vmlaq_s16 (y13, y5, y10);
y29 = vmlaq_s16 (y29, y21, y26);
vst1q_u16(144 + c, y13);
vst1q_u16(152 + c, y29);
y12 = vmulq_s16(y5, y11);
y28 = vmulq_s16(y21, y27);
vst1q_u16(160 + c, y12);
vst1q_u16(168 + c, y28);
y0 = vld1q_s16(96 + a);
y6 = vld1q_s16(96 + b);
y16 = vld1q_s16(104 + a);
y22 = vld1q_s16(104 + b);
y0 = vaddq_s16 (vld1q_s16(272+a), y0);
y6 = vaddq_s16 (vld1q_s16(272+b), y6);
y16 = vaddq_s16 (vld1q_s16(280+a), y16);
y22 = vaddq_s16 (vld1q_s16(280+b), y22);
y1 = vld1q_s16(112 + a);
y7 = vld1q_s16(112 + b);
y17 = vld1q_s16(120 + a);
y23 = vld1q_s16(120 + b);
y1 = vaddq_s16 (vld1q_s16(288+a), y1);
y7 = vaddq_s16 (vld1q_s16(288+b), y7);
y17 = vaddq_s16 (vld1q_s16(296+a), y17);
y23 = vaddq_s16 (vld1q_s16(296+b), y23);
y2 = vld1q_s16(128 + a);
y8 = vld1q_s16(128 + b);
y18 = vld1q_s16(136 + a);
y24 = vld1q_s16(136 + b);
y2 = vaddq_s16 (vld1q_s16(304+a), y2);
y8 = vaddq_s16 (vld1q_s16(304+b), y8);
y18 = vaddq_s16 (vld1q_s16(312+a), y18);
y24 = vaddq_s16 (vld1q_s16(312+b), y24);
y3 = vld1q_s16(144 + a);
y9 = vld1q_s16(144 + b);
y19 = vld1q_s16(152 + a);
y25 = vld1q_s16(152 + b);
y3 = vaddq_s16 (vld1q_s16(320+a), y3);
y9 = vaddq_s16 (vld1q_s16(320+b), y9);
y19 = vaddq_s16 (vld1q_s16(328+a), y19);
y25 = vaddq_s16 (vld1q_s16(328+b), y25);
y4 = vld1q_s16(160 + a);
y10 = vld1q_s16(160 + b);
y20 = vld1q_s16(168 + a);
y26 = vld1q_s16(168 + b);
y4 = vaddq_s16 (vld1q_s16(336+a), y4);
y10 = vaddq_s16 (vld1q_s16(336+b), y10);
y20 = vaddq_s16 (vld1q_s16(344+a), y20);
y26 = vaddq_s16 (vld1q_s16(344+b), y26);
y12 = vmulq_s16(y0, y6);
y28 = vmulq_s16(y16, y22);
vst1q_u16(192 + c, y12);
vst1q_u16(200 + c, y28);
y13 = vmulq_s16(y0, y7);
y29 = vmulq_s16(y16, y23);
y13 = vmlaq_s16 (y13, y1, y6);
y29 = vmlaq_s16 (y29, y17, y22);
vst1q_u16(208 + c, y13);
vst1q_u16(216 + c, y29);
y12 = vmulq_s16(y0, y8);
y28 = vmulq_s16(y16, y24);
y12 = vmlaq_s16 (y12, y1, y7);
y28 = vmlaq_s16 (y28, y17, y23);
y12 = vmlaq_s16 (y12, y2, y6);
y28 = vmlaq_s16 (y28, y18, y22);
vst1q_u16(224 + c, y12);
vst1q_u16(232 + c, y28);
y13 = vmulq_s16(y0, y9);
y29 = vmulq_s16(y16, y25);
y13 = vmlaq_s16 (y13, y1, y8);
y29 = vmlaq_s16 (y29, y17, y24);
y13 = vmlaq_s16 (y13, y2, y7);
y29 = vmlaq_s16 (y29, y18, y23);
y13 = vmlaq_s16 (y13, y3, y6);
y29 = vmlaq_s16 (y29, y19, y22);
vst1q_u16(240 + c, y13);
vst1q_u16(248 + c, y29);
y12 = vmulq_s16(y0, y10);
y28 = vmulq_s16(y16, y26);
y12 = vmlaq_s16 (y12, y1, y9);
y28 = vmlaq_s16 (y28, y17, y25);
y12 = vmlaq_s16 (y12, y2, y8);
y28 = vmlaq_s16 (y28, y18, y24);
y12 = vmlaq_s16 (y12, y3, y7);
y28 = vmlaq_s16 (y28, y19, y23);
y12 = vmlaq_s16 (y12, y4, y6);
y28 = vmlaq_s16 (y28, y20, y22);
vst1q_u16(256 + c, y12);
vst1q_u16(264 + c, y28);
y13 = vmulq_s16(y1, y10);
y29 = vmulq_s16(y17, y26);
y13 = vmlaq_s16 (y13, y2, y9);
y29 = vmlaq_s16 (y29, y18, y25);
y13 = vmlaq_s16 (y13, y3, y8);
y29 = vmlaq_s16 (y29, y19, y24);
y13 = vmlaq_s16 (y13, y4, y7);
y29 = vmlaq_s16 (y29, y20, y23);
vst1q_u16(272 + c, y13);
vst1q_u16(280 + c, y29);
y12 = vmulq_s16(y2, y10);
y28 = vmulq_s16(y18, y26);
y12 = vmlaq_s16 (y12, y3, y9);
y28 = vmlaq_s16 (y28, y19, y25);
y12 = vmlaq_s16 (y12, y4, y8);
y28 = vmlaq_s16 (y28, y20, y24);
vst1q_u16(288 + c, y12);
vst1q_u16(296 + c, y28);
y13 = vmulq_s16(y3, y10);
y29 = vmulq_s16(y19, y26);
y13 = vmlaq_s16 (y13, y4, y9);
y29 = vmlaq_s16 (y29, y20, y25);
vst1q_u16(304 + c, y13);
vst1q_u16(312 + c, y29);
y12 = vmulq_s16(y4, y10);
y28 = vmulq_s16(y20, y26);
vst1q_u16(320 + c, y12);
vst1q_u16(328 + c, y28);
y12 = vld1q_s16(0 + a);
y0 = vaddq_s16(y12, y0);
y12 = vld1q_s16(0 + b);
y6 = vaddq_s16(y12, y6);
y28 = vld1q_s16(8 + a);
y16 = vaddq_s16(y28, y16);
y28 = vld1q_s16(8 + b);
y22 = vaddq_s16(y28, y22);
y0 = vaddq_s16 (vld1q_s16(176+a), y0);
y6 = vaddq_s16 (vld1q_s16(176+b), y6);
y16 = vaddq_s16 (vld1q_s16(184+a), y16);
y22 = vaddq_s16 (vld1q_s16(184+b), y22);
y12 = vld1q_s16(16 + a);
y1 = vaddq_s16(y12, y1);
y12 = vld1q_s16(16 + b);
y7 = vaddq_s16(y12, y7);
y28 = vld1q_s16(24 + a);
y17 = vaddq_s16(y28, y17);
y28 = vld1q_s16(24 + b);
y23 = vaddq_s16(y28, y23);
y1 = vaddq_s16 (vld1q_s16(192+a), y1);
y7 = vaddq_s16 (vld1q_s16(192+b), y7);
y17 = vaddq_s16 (vld1q_s16(200+a), y17);
y23 = vaddq_s16 (vld1q_s16(200+b), y23);
y12 = vld1q_s16(32 + a);
y2 = vaddq_s16(y12, y2);
y12 = vld1q_s16(32 + b);
y8 = vaddq_s16(y12, y8);
y28 = vld1q_s16(40 + a);
y18 = vaddq_s16(y28, y18);
y28 = vld1q_s16(40 + b);
y24 = vaddq_s16(y28, y24);
y2 = vaddq_s16 (vld1q_s16(208+a), y2);
y8 = vaddq_s16 (vld1q_s16(208+b), y8);
y18 = vaddq_s16 (vld1q_s16(216+a), y18);
y24 = vaddq_s16 (vld1q_s16(216+b), y24);
y12 = vld1q_s16(48 + a);
y3 = vaddq_s16(y12, y3);
y12 = vld1q_s16(48 + b);
y9 = vaddq_s16(y12, y9);
y28 = vld1q_s16(56 + a);
y19 = vaddq_s16(y28, y19);
y28 = vld1q_s16(56 + b);
y25 = vaddq_s16(y28, y25);
y3 = vaddq_s16 (vld1q_s16(224+a), y3);
y9 = vaddq_s16 (vld1q_s16(224+b), y9);
y19 = vaddq_s16 (vld1q_s16(232+a), y19);
y25 = vaddq_s16 (vld1q_s16(232+b), y25);
y12 = vld1q_s16(64 + a);
y4 = vaddq_s16(y12, y4);
y12 = vld1q_s16(64 + b);
y10 = vaddq_s16(y12, y10);
y28 = vld1q_s16(72 + a);
y20 = vaddq_s16(y28, y20);
y28 = vld1q_s16(72 + b);
y26 = vaddq_s16(y28, y26);
y4 = vaddq_s16 (vld1q_s16(240+a), y4);
y10 = vaddq_s16 (vld1q_s16(240+b), y10);
y20 = vaddq_s16 (vld1q_s16(248+a), y20);
y26 = vaddq_s16 (vld1q_s16(248+b), y26);
y12 = vmulq_s16(y0, y11);
y28 = vmulq_s16(y16, y27);
y12 = vmlaq_s16 (y12, y1, y10);
y28 = vmlaq_s16 (y28, y17, y26);
y12 = vmlaq_s16 (y12, y2, y9);
y28 = vmlaq_s16 (y28, y18, y25);
y12 = vmlaq_s16 (y12, y3, y8);
y28 = vmlaq_s16 (y28, y19, y24);
y12 = vmlaq_s16 (y12, y4, y7);
y28 = vmlaq_s16 (y28, y20, y23);
y12 = vmlaq_s16 (y12, y5, y6);
y28 = vmlaq_s16 (y28, y21, y22);
y12 = vsubq_s16 (y12, vld1q_s16(80+c));
y12 = vsubq_s16 (y12, vld1q_s16(272+c));
vst1q_u16(176 + c, y12);
y28 = vsubq_s16 (y28, vld1q_s16(88+c));
y28 = vsubq_s16 (y28, vld1q_s16(280+c));
vst1q_u16(184 + c, y28);
y12 = vmulq_s16(y5, y7);
y28 = vmulq_s16(y21, y23);
y13 = vmulq_s16(y5, y8);
y29 = vmulq_s16(y21, y24);
y14 = vmulq_s16(y5, y9);
y30 = vmulq_s16(y21, y25);
y15 = vmulq_s16(y5, y10);
y31 = vmulq_s16(y21, y26);
y12 = vmlaq_s16 (y12, y1, y11);
y28 = vmlaq_s16 (y28, y17, y27);
y12 = vmlaq_s16 (y12, y2, y10);
y28 = vmlaq_s16 (y28, y18, y26);
y12 = vmlaq_s16 (y12, y3, y9);
y28 = vmlaq_s16 (y28, y19, y25);
y12 = vmlaq_s16 (y12, y4, y8);
y28 = vmlaq_s16 (y28, y20, y24);
y13 = vmlaq_s16 (y13, y2, y11);
y29 = vmlaq_s16 (y29, y18, y27);
y13 = vmlaq_s16 (y13, y3, y10);
y29 = vmlaq_s16 (y29, y19, y26);
y13 = vmlaq_s16 (y13, y4, y9);
y29 = vmlaq_s16 (y29, y20, y25);
y14 = vmlaq_s16 (y14, y3, y11);
y30 = vmlaq_s16 (y30, y19, y27);
y14 = vmlaq_s16 (y14, y4, y10);
y30 = vmlaq_s16 (y30, y20, y26);
y15 = vmlaq_s16 (y15, y4, y11);
y31 = vmlaq_s16 (y31, y20, y27);
y11 = vmulq_s16(y0, y10);
y27 = vmulq_s16(y16, y26);
y11 = vmlaq_s16 (y11, y1, y9);
y27 = vmlaq_s16 (y27, y17, y25);
y11 = vmlaq_s16 (y11, y2, y8);
y27 = vmlaq_s16 (y27, y18, y24);
y11 = vmlaq_s16 (y11, y3, y7);
y27 = vmlaq_s16 (y27, y19, y23);
y11 = vmlaq_s16 (y11, y4, y6);
y27 = vmlaq_s16 (y27, y20, y22);
y10 = vmulq_s16(y0, y9);
y26 = vmulq_s16(y16, y25);
y10 = vmlaq_s16 (y10, y1, y8);
y26 = vmlaq_s16 (y26, y17, y24);
y10 = vmlaq_s16 (y10, y2, y7);
y26 = vmlaq_s16 (y26, y18, y23);
y10 = vmlaq_s16 (y10, y3, y6);
y26 = vmlaq_s16 (y26, y19, y22);
y9 = vmulq_s16(y0, y8);
y25 = vmulq_s16(y16, y24);
y9 = vmlaq_s16 (y9, y1, y7);
y25 = vmlaq_s16 (y25, y17, y23);
y9 = vmlaq_s16 (y9, y2, y6);
y25 = vmlaq_s16 (y25, y18, y22);
y8 = vmulq_s16(y0, y7);
y24 = vmulq_s16(y16, y23);
y8 = vmlaq_s16 (y8, y1, y6);
y24 = vmlaq_s16 (y24, y17, y22);
y7 = vmulq_s16(y0, y6);
y23 = vmulq_s16(y16, y22);
y0 = vld1q_s16(96 + c);
y16 = vld1q_s16(104 + c);
y0 = vsubq_s16 (y0, vld1q_s16(192+c) );
y16 = vsubq_s16 (y16, vld1q_s16(200+c) );
y6 = vsubq_s16(y12, y0);
y22 = vsubq_s16(y22, y16);
y6 = vsubq_s16 ( y6, vld1q_s16(288+c));
y22 = vsubq_s16 ( y22, vld1q_s16(296+c));
vst1q_u16(192 + c, y6);
vst1q_u16(200 + c, y22);
y0 = vaddq_s16(y7, y0);
y16 = vaddq_s16(y16, y16);
y0 = vsubq_s16 (y0, vld1q_s16(0+c));
y16 = vsubq_s16 (y16, vld1q_s16(8+c));
vst1q_u16(96 + c, y0);
vst1q_u16(104 + c, y16);
y1 = vld1q_s16(112 + c);
y17 = vld1q_s16(120 + c);
y1 = vsubq_s16 (y1, vld1q_s16(208+c) );
y17 = vsubq_s16 (y17, vld1q_s16(216+c) );
y7 = vsubq_s16(y13, y1);
y23 = vsubq_s16(y23, y17);
y7 = vsubq_s16 ( y7, vld1q_s16(304+c));
y23 = vsubq_s16 ( y23, vld1q_s16(312+c));
vst1q_u16(208 + c, y7);
vst1q_u16(216 + c, y23);
y1 = vaddq_s16(y8, y1);
y17 = vaddq_s16(y17, y17);
y1 = vsubq_s16 (y1, vld1q_s16(16+c));
y17 = vsubq_s16 (y17, vld1q_s16(24+c));
vst1q_u16(112 + c, y1);
vst1q_u16(120 + c, y17);
y2 = vld1q_s16(128 + c);
y18 = vld1q_s16(136 + c);
y2 = vsubq_s16 (y2, vld1q_s16(224+c) );
y18 = vsubq_s16 (y18, vld1q_s16(232+c) );
y8 = vsubq_s16(y14, y2);
y24 = vsubq_s16(y24, y18);
y8 = vsubq_s16 ( y8, vld1q_s16(320+c));
y24 = vsubq_s16 ( y24, vld1q_s16(328+c));
vst1q_u16(224 + c, y8);
vst1q_u16(232 + c, y24);
y2 = vaddq_s16(y9, y2);
y18 = vaddq_s16(y18, y18);
y2 = vsubq_s16 (y2, vld1q_s16(32+c));
y18 = vsubq_s16 (y18, vld1q_s16(40+c));
vst1q_u16(128 + c, y2);
vst1q_u16(136 + c, y18);
y3 = vld1q_s16(144 + c);
y19 = vld1q_s16(152 + c);
y3 = vsubq_s16 (y3, vld1q_s16(240+c) );
y19 = vsubq_s16 (y19, vld1q_s16(248+c) );
y9 = vsubq_s16(y15, y3);
y25 = vsubq_s16(y25, y19);
vst1q_u16(240 + c, y9);
vst1q_u16(248 + c, y25);
y3 = vaddq_s16(y10, y3);
y19 = vaddq_s16(y19, y19);
y3 = vsubq_s16 (y3, vld1q_s16(48+c));
y19 = vsubq_s16 (y19, vld1q_s16(56+c));
vst1q_u16(144 + c, y3);
vst1q_u16(152 + c, y19);
y4 = vld1q_s16(160 + c);
y20 = vld1q_s16(168 + c);
y4 = vsubq_s16 (y4, vld1q_s16(256+c) );
y20 = vsubq_s16 (y20, vld1q_s16(264+c) );
y4 = vaddq_s16(y11, y4);
y20 = vaddq_s16(y20, y20);
y4 = vsubq_s16 (y4, vld1q_s16(64+c));
y20 = vsubq_s16 (y20, vld1q_s16(72+c));
vst1q_u16(160 + c, y4);
vst1q_u16(168 + c, y20);

    a += 704; 
    b += 704; 
    c += 1408;
    }
}
    