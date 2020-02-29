#include <arm_neon.h>

void poly_R2_mul(unsigned char *c, unsigned char *a, unsigned char *b)
{
    poly8x16_t y0, y1, y2, y3, y4, y5, y6, y7;
    poly8x16_t y8, y9, y10, y11, y12, y13, y14, y15;
    poly8x16_t y16, y17, y18, y19, y20, y21, y22, y23;
    poly8x16_t y24, y25, y26, y27, y28, y29, y30, y31;
    y8 = vld1q_p8(0 + a);
    y9 = vld1q_p8(16 + a);
    y10 = vld1q_p8(32 + a);
    y11 = vld1q_p8(48 + a);
    y12 = vld1q_p8(0 + b);
    y13 = vld1q_p8(16 + b);
    y14 = vld1q_p8(32 + b);
    y15 = vld1q_p8(48 + b);
    // karatsuba_512x512 BEGIN
    y21 = vaddq_p128(y9, y11);
    y25 = vaddq_p128(y8, y10);
    y22 = vaddq_p128(y13, y15);
    y26 = vaddq_p128(y12, y14);
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y3 = vmull_p64(y8, y12);
    y2 = vmull_high_p64(y8, y12);
    y20 = vextq_p64(y12, y12, 1);
    y18 = vmull_p64(y8, y20);
    y19 = vmull_high_p64(y8, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y3 = vaddq_p64(y20, y3);
    y20 = vextq_p64(y19, y18, 1);
    y2 = vaddq_p64(y20, y2);
    // mult128x128 END
    y16 = vaddq_p128(y8, y9);
    y17 = vaddq_p128(y12, y13);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y1 = vmull_p64(y9, y13);
    y0 = vmull_high_p64(y9, y13);
    y20 = vextq_p64(y13, y13, 1);
    y19 = vmull_p64(y9, y20);
    y24 = vmull_high_p64(y9, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y1 = vaddq_p64(y20, y1);
    y20 = vextq_p64(y24, y19, 1);
    y0 = vaddq_p64(y20, y0);
    // mult128x128 END
    y23 = vaddq_p128(y23, y2);
    y18 = vaddq_p128(y18, y3);
    y23 = vaddq_p128(y23, y0);
    y18 = vaddq_p128(y18, y1);
    y2 = vaddq_p128(y2, y23);
    y0 = vaddq_p128(y0, y18);
    // karatsuba_256x256 END
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y7 = vmull_p64(y10, y14);
    y6 = vmull_high_p64(y10, y14);
    y20 = vextq_p64(y14, y14, 1);
    y18 = vmull_p64(y10, y20);
    y19 = vmull_high_p64(y10, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y7 = vaddq_p64(y20, y7);
    y20 = vextq_p64(y19, y18, 1);
    y6 = vaddq_p64(y20, y6);
    // mult128x128 END
    y16 = vaddq_p128(y10, y11);
    y17 = vaddq_p128(y14, y15);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y5 = vmull_p64(y11, y15);
    y4 = vmull_high_p64(y11, y15);
    y20 = vextq_p64(y15, y15, 1);
    y19 = vmull_p64(y11, y20);
    y24 = vmull_high_p64(y11, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y5 = vaddq_p64(y20, y5);
    y20 = vextq_p64(y24, y19, 1);
    y4 = vaddq_p64(y20, y4);
    // mult128x128 END
    y23 = vaddq_p128(y23, y6);
    y18 = vaddq_p128(y18, y7);
    y23 = vaddq_p128(y23, y4);
    y18 = vaddq_p128(y18, y5);
    y6 = vaddq_p128(y6, y23);
    y4 = vaddq_p128(y4, y18);
    // karatsuba_256x256 END
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y11 = vmull_p64(y25, y26);
    y10 = vmull_high_p64(y25, y26);
    y20 = vextq_p64(y26, y26, 1);
    y18 = vmull_p64(y25, y20);
    y19 = vmull_high_p64(y25, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y11 = vaddq_p64(y20, y11);
    y20 = vextq_p64(y19, y18, 1);
    y10 = vaddq_p64(y20, y10);
    // mult128x128 END
    y16 = vaddq_p128(y25, y21);
    y17 = vaddq_p128(y26, y22);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y9 = vmull_p64(y21, y22);
    y8 = vmull_high_p64(y21, y22);
    y20 = vextq_p64(y22, y22, 1);
    y19 = vmull_p64(y21, y20);
    y24 = vmull_high_p64(y21, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y9 = vaddq_p64(y20, y9);
    y20 = vextq_p64(y24, y19, 1);
    y8 = vaddq_p64(y20, y8);
    // mult128x128 END
    y23 = vaddq_p128(y23, y10);
    y18 = vaddq_p128(y18, y11);
    y23 = vaddq_p128(y23, y8);
    y18 = vaddq_p128(y18, y9);
    y10 = vaddq_p128(y10, y23);
    y8 = vaddq_p128(y8, y18);
    // karatsuba_256x256 END
    y8 = vaddq_p128(y0, y8);
    y9 = vaddq_p128(y1, y9);
    y10 = vaddq_p128(y2, y10);
    y11 = vaddq_p128(y3, y11);
    y8 = vaddq_p128(y4, y8);
    y9 = vaddq_p128(y5, y9);
    y10 = vaddq_p128(y6, y10);
    y11 = vaddq_p128(y7, y11);
    y2 = vaddq_p128(y8, y2);
    y3 = vaddq_p128(y9, y3);
    y4 = vaddq_p128(y10, y4);
    y5 = vaddq_p128(y11, y5);
    // karatsuba_512x512 END
    // vec256_sr53 BEGIN
    y16 = 0xffffffffffffffff0000000000000000;
    y29 = vandq_u16(y7, y16);
    y28 = y6 << 11;
    y29 = y29 << 11;
    y16 = vextq_p64(y29, y28, 1);
    y17 = vextq_p64(y28, y29, 1);
    y29 = y7 >> 53;
    y28 = y6 >> 53;
    y29 = vaddq_p128(y29, y16);
    y28 = vaddq_p128(y28, y17);
    // vec256_sr53 END
    y28 = vaddq_p128(y0, y28);
    y29 = vaddq_p128(y1, y29);
    y25 = 0x1fffffffffffff;
    y30 = y25 & y6;
    y31 = y7;
    // store_1024 BEGIN
    vst1q_p8(0 + c, y28);
    vst1q_p8(16 + c, y29);
    vst1q_p8(32 + c, y2);
    vst1q_p8(48 + c, y3);
    vst1q_p8(64 + c, y4);
    vst1q_p8(80 + c, y5);
    vst1q_p8(96 + c, y30);
    vst1q_p8(112 + c, y31);
    // store_1024 END
    // load_1024 BEGIN
    y8 = vld1q_p8(0 + c);
    y9 = vld1q_p8(16 + c);
    y10 = vld1q_p8(32 + c);
    y11 = vld1q_p8(48 + c);
    y12 = vld1q_p8(64 + c);
    y13 = vld1q_p8(80 + c);
    y14 = vld1q_p8(96 + c);
    y15 = vld1q_p8(112 + c);
    // load_1024 END
    // mul512_and_accumulate BEGIN
    y12 = vaddq_p128(y0, y12);
    y13 = vaddq_p128(y1, y13);
    y22 = 0x1fffffffffffff;
    y23 = y3 & y22;
    y14 = vaddq_p128(y2, y14);
    y15 = vaddq_p128(y23, y15);
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y3, y23);
    y16 = y2 << 11;
    y17 = y17 << 11;
    y23 = vextq_p64(y17, y16, 1);
    y22 = vextq_p64(y16, y17, 1);
    y17 = y3 >> 53;
    y16 = y2 >> 53;
    y17 = vaddq_p128(y17, y23);
    y16 = vaddq_p128(y16, y22);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y5 & 0xffffffffffffffff;
    y23 = vextq_p64(y19, y18, 1);
    y22 = vextq_p64(y18, y19, 1);
    y19 = y23 << 11;
    y18 = y22 << 11;
    // vec256_sl203 END
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y21 = vandq_u16(y5, y23);
    y20 = y4 << 11;
    y21 = y21 << 11;
    y23 = vextq_p64(y21, y20, 1);
    y22 = vextq_p64(y20, y21, 1);
    y21 = y5 >> 53;
    y20 = y4 >> 53;
    y21 = vaddq_p128(y21, y23);
    y20 = vaddq_p128(y20, y22);
    // vec256_sr53 END
    y18 = vaddq_p128(y16, y18);
    y19 = vaddq_p128(y17, y19);
    y8 = vaddq_p128(y18, y8);
    y9 = vaddq_p128(y19, y9);
    // vec256_sl203 BEGIN
    y16 = 0;
    y17 = y7 & 0xffffffffffffffff;
    y23 = vextq_p64(y17, y16, 1);
    y22 = vextq_p64(y16, y17, 1);
    y17 = y23 << 11;
    y16 = y22 << 11;
    // vec256_sl203 END
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y19 = vandq_u16(y7, y23);
    y18 = y6 << 11;
    y19 = y19 << 11;
    y23 = vextq_p64(y19, y18, 1);
    y22 = vextq_p64(y18, y19, 1);
    y19 = y7 >> 53;
    y18 = y6 >> 53;
    y19 = vaddq_p128(y19, y23);
    y18 = vaddq_p128(y18, y22);
    // vec256_sr53 END
    y20 = vaddq_p128(y16, y20);
    y21 = vaddq_p128(y17, y21);
    y10 = vaddq_p128(y20, y10);
    y11 = vaddq_p128(y21, y11);
    y12 = vaddq_p128(y18, y12);
    y13 = vaddq_p128(y19, y13);
    // mul512_and_accumulate END
    // store_1024 BEGIN
    vst1q_p8(0 + c, y8);
    vst1q_p8(16 + c, y9);
    vst1q_p8(32 + c, y10);
    vst1q_p8(48 + c, y11);
    vst1q_p8(64 + c, y12);
    vst1q_p8(80 + c, y13);
    vst1q_p8(96 + c, y14);
    vst1q_p8(112 + c, y15);
    // store_1024 END
    y8 = vld1q_p8(64 + a);
    y9 = vld1q_p8(80 + a);
    y10 = vld1q_p8(96 + a);
    y11 = vld1q_p8(112 + a);
    y12 = vld1q_p8(64 + b);
    y13 = vld1q_p8(80 + b);
    y14 = vld1q_p8(96 + b);
    y15 = vld1q_p8(112 + b);
    // karatsuba_512x512 BEGIN
    y21 = vaddq_p128(y9, y11);
    y25 = vaddq_p128(y8, y10);
    y22 = vaddq_p128(y13, y15);
    y26 = vaddq_p128(y12, y14);
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y3 = vmull_p64(y8, y12);
    y2 = vmull_high_p64(y8, y12);
    y20 = vextq_p64(y12, y12, 1);
    y18 = vmull_p64(y8, y20);
    y19 = vmull_high_p64(y8, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y3 = vaddq_p64(y20, y3);
    y20 = vextq_p64(y19, y18, 1);
    y2 = vaddq_p64(y20, y2);
    // mult128x128 END
    y16 = vaddq_p128(y8, y9);
    y17 = vaddq_p128(y12, y13);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y1 = vmull_p64(y9, y13);
    y0 = vmull_high_p64(y9, y13);
    y20 = vextq_p64(y13, y13, 1);
    y19 = vmull_p64(y9, y20);
    y24 = vmull_high_p64(y9, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y1 = vaddq_p64(y20, y1);
    y20 = vextq_p64(y24, y19, 1);
    y0 = vaddq_p64(y20, y0);
    // mult128x128 END
    y23 = vaddq_p128(y23, y2);
    y18 = vaddq_p128(y18, y3);
    y23 = vaddq_p128(y23, y0);
    y18 = vaddq_p128(y18, y1);
    y2 = vaddq_p128(y2, y23);
    y0 = vaddq_p128(y0, y18);
    // karatsuba_256x256 END
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y7 = vmull_p64(y10, y14);
    y6 = vmull_high_p64(y10, y14);
    y20 = vextq_p64(y14, y14, 1);
    y18 = vmull_p64(y10, y20);
    y19 = vmull_high_p64(y10, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y7 = vaddq_p64(y20, y7);
    y20 = vextq_p64(y19, y18, 1);
    y6 = vaddq_p64(y20, y6);
    // mult128x128 END
    y16 = vaddq_p128(y10, y11);
    y17 = vaddq_p128(y14, y15);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y5 = vmull_p64(y11, y15);
    y4 = vmull_high_p64(y11, y15);
    y20 = vextq_p64(y15, y15, 1);
    y19 = vmull_p64(y11, y20);
    y24 = vmull_high_p64(y11, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y5 = vaddq_p64(y20, y5);
    y20 = vextq_p64(y24, y19, 1);
    y4 = vaddq_p64(y20, y4);
    // mult128x128 END
    y23 = vaddq_p128(y23, y6);
    y18 = vaddq_p128(y18, y7);
    y23 = vaddq_p128(y23, y4);
    y18 = vaddq_p128(y18, y5);
    y6 = vaddq_p128(y6, y23);
    y4 = vaddq_p128(y4, y18);
    // karatsuba_256x256 END
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y11 = vmull_p64(y25, y26);
    y10 = vmull_high_p64(y25, y26);
    y20 = vextq_p64(y26, y26, 1);
    y18 = vmull_p64(y25, y20);
    y19 = vmull_high_p64(y25, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y11 = vaddq_p64(y20, y11);
    y20 = vextq_p64(y19, y18, 1);
    y10 = vaddq_p64(y20, y10);
    // mult128x128 END
    y16 = vaddq_p128(y25, y21);
    y17 = vaddq_p128(y26, y22);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y9 = vmull_p64(y21, y22);
    y8 = vmull_high_p64(y21, y22);
    y20 = vextq_p64(y22, y22, 1);
    y19 = vmull_p64(y21, y20);
    y24 = vmull_high_p64(y21, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y9 = vaddq_p64(y20, y9);
    y20 = vextq_p64(y24, y19, 1);
    y8 = vaddq_p64(y20, y8);
    // mult128x128 END
    y23 = vaddq_p128(y23, y10);
    y18 = vaddq_p128(y18, y11);
    y23 = vaddq_p128(y23, y8);
    y18 = vaddq_p128(y18, y9);
    y10 = vaddq_p128(y10, y23);
    y8 = vaddq_p128(y8, y18);
    // karatsuba_256x256 END
    y8 = vaddq_p128(y0, y8);
    y9 = vaddq_p128(y1, y9);
    y10 = vaddq_p128(y2, y10);
    y11 = vaddq_p128(y3, y11);
    y8 = vaddq_p128(y4, y8);
    y9 = vaddq_p128(y5, y9);
    y10 = vaddq_p128(y6, y10);
    y11 = vaddq_p128(y7, y11);
    y2 = vaddq_p128(y8, y2);
    y3 = vaddq_p128(y9, y3);
    y4 = vaddq_p128(y10, y4);
    y5 = vaddq_p128(y11, y5);
    // karatsuba_512x512 END
    // load_1024 BEGIN
    y8 = vld1q_p8(0 + c);
    y9 = vld1q_p8(16 + c);
    y10 = vld1q_p8(32 + c);
    y11 = vld1q_p8(48 + c);
    y12 = vld1q_p8(64 + c);
    y13 = vld1q_p8(80 + c);
    y14 = vld1q_p8(96 + c);
    y15 = vld1q_p8(112 + c);
    // load_1024 END
    // mul512_and_accumulate BEGIN
    y12 = vaddq_p128(y0, y12);
    y13 = vaddq_p128(y1, y13);
    y22 = 0x1fffffffffffff;
    y23 = y3 & y22;
    y14 = vaddq_p128(y2, y14);
    y15 = vaddq_p128(y23, y15);
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y3, y23);
    y16 = y2 << 11;
    y17 = y17 << 11;
    y23 = vextq_p64(y17, y16, 1);
    y22 = vextq_p64(y16, y17, 1);
    y17 = y3 >> 53;
    y16 = y2 >> 53;
    y17 = vaddq_p128(y17, y23);
    y16 = vaddq_p128(y16, y22);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y5 & 0xffffffffffffffff;
    y23 = vextq_p64(y19, y18, 1);
    y22 = vextq_p64(y18, y19, 1);
    y19 = y23 << 11;
    y18 = y22 << 11;
    // vec256_sl203 END
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y21 = vandq_u16(y5, y23);
    y20 = y4 << 11;
    y21 = y21 << 11;
    y23 = vextq_p64(y21, y20, 1);
    y22 = vextq_p64(y20, y21, 1);
    y21 = y5 >> 53;
    y20 = y4 >> 53;
    y21 = vaddq_p128(y21, y23);
    y20 = vaddq_p128(y20, y22);
    // vec256_sr53 END
    y18 = vaddq_p128(y16, y18);
    y19 = vaddq_p128(y17, y19);
    y8 = vaddq_p128(y18, y8);
    y9 = vaddq_p128(y19, y9);
    // vec256_sl203 BEGIN
    y16 = 0;
    y17 = y7 & 0xffffffffffffffff;
    y23 = vextq_p64(y17, y16, 1);
    y22 = vextq_p64(y16, y17, 1);
    y17 = y23 << 11;
    y16 = y22 << 11;
    // vec256_sl203 END
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y19 = vandq_u16(y7, y23);
    y18 = y6 << 11;
    y19 = y19 << 11;
    y23 = vextq_p64(y19, y18, 1);
    y22 = vextq_p64(y18, y19, 1);
    y19 = y7 >> 53;
    y18 = y6 >> 53;
    y19 = vaddq_p128(y19, y23);
    y18 = vaddq_p128(y18, y22);
    // vec256_sr53 END
    y20 = vaddq_p128(y16, y20);
    y21 = vaddq_p128(y17, y21);
    y10 = vaddq_p128(y20, y10);
    y11 = vaddq_p128(y21, y11);
    y12 = vaddq_p128(y18, y12);
    y13 = vaddq_p128(y19, y13);
    // mul512_and_accumulate END
    // mul1024_and_accumulate BEGIN
    // vec256_sr53 BEGIN
    y21 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y7, y21);
    y16 = y6 << 11;
    y17 = y17 << 11;
    y21 = vextq_p64(y17, y16, 1);
    y20 = vextq_p64(y16, y17, 1);
    y17 = y7 >> 53;
    y16 = y6 >> 53;
    y17 = vaddq_p128(y17, y21);
    y16 = vaddq_p128(y16, y20);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y1 & 0xffffffffffffffff;
    y21 = vextq_p64(y19, y18, 1);
    y20 = vextq_p64(y18, y19, 1);
    y19 = y21 << 11;
    y18 = y20 << 11;
    // vec256_sl203 END
    y18 = vaddq_p128(y16, y18);
    y19 = vaddq_p128(y17, y19);
    y8 = vaddq_p128(y18, y8);
    y9 = vaddq_p128(y19, y9);
    // vec256_sr53 BEGIN
    y21 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y1, y21);
    y16 = y0 << 11;
    y17 = y17 << 11;
    y21 = vextq_p64(y17, y16, 1);
    y20 = vextq_p64(y16, y17, 1);
    y17 = y1 >> 53;
    y16 = y0 >> 53;
    y17 = vaddq_p128(y17, y21);
    y16 = vaddq_p128(y16, y20);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y3 & 0xffffffffffffffff;
    y21 = vextq_p64(y19, y18, 1);
    y20 = vextq_p64(y18, y19, 1);
    y19 = y21 << 11;
    y18 = y20 << 11;
    // vec256_sl203 END
    y18 = vaddq_p128(y16, y18);
    y19 = vaddq_p128(y17, y19);
    y10 = vaddq_p128(y18, y10);
    y11 = vaddq_p128(y19, y11);
    // vec256_sr53 BEGIN
    y21 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y3, y21);
    y16 = y2 << 11;
    y17 = y17 << 11;
    y21 = vextq_p64(y17, y16, 1);
    y20 = vextq_p64(y16, y17, 1);
    y17 = y3 >> 53;
    y16 = y2 >> 53;
    y17 = vaddq_p128(y17, y21);
    y16 = vaddq_p128(y16, y20);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y5 & 0xffffffffffffffff;
    y21 = vextq_p64(y19, y18, 1);
    y20 = vextq_p64(y18, y19, 1);
    y19 = y21 << 11;
    y18 = y20 << 11;
    // vec256_sl203 END
    y18 = vaddq_p128(y16, y18);
    y19 = vaddq_p128(y17, y19);
    y12 = vaddq_p128(y18, y12);
    y13 = vaddq_p128(y19, y13);
    // vec256_sr53 BEGIN
    y21 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y5, y21);
    y16 = y4 << 11;
    y17 = y17 << 11;
    y21 = vextq_p64(y17, y16, 1);
    y20 = vextq_p64(y16, y17, 1);
    y17 = y5 >> 53;
    y16 = y4 >> 53;
    y17 = vaddq_p128(y17, y21);
    y16 = vaddq_p128(y16, y20);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y7 & 0xffffffffffffffff;
    y21 = vextq_p64(y19, y18, 1);
    y20 = vextq_p64(y18, y19, 1);
    y19 = y21 << 11;
    y18 = y20 << 11;
    // vec256_sl203 END
    y10 = vaddq_p128(y18, y10);
    y11 = vaddq_p128(y19, y11);
    y14 = vaddq_p128(y18, y14);
    y15 = vaddq_p128(y19, y15);
    // mul1024_and_accumulate END
    // store_1024 BEGIN
    vst1q_p8(0 + c, y8);
    vst1q_p8(16 + c, y9);
    vst1q_p8(32 + c, y10);
    vst1q_p8(48 + c, y11);
    vst1q_p8(64 + c, y12);
    vst1q_p8(80 + c, y13);
    vst1q_p8(96 + c, y14);
    vst1q_p8(112 + c, y15);
    // store_1024 END
    // load_1024 BEGIN
    y8 = vld1q_p8(0 + a);
    y9 = vld1q_p8(16 + a);
    y10 = vld1q_p8(32 + a);
    y11 = vld1q_p8(48 + a);
    y20 = vld1q_p8(64 + a);
    y21 = vld1q_p8(80 + a);
    y22 = vld1q_p8(96 + a);
    y23 = vld1q_p8(112 + a);
    // load_1024 END
    // load_1024 BEGIN
    y12 = vld1q_p8(0 + b);
    y13 = vld1q_p8(16 + b);
    y14 = vld1q_p8(32 + b);
    y15 = vld1q_p8(48 + b);
    y24 = vld1q_p8(64 + b);
    y25 = vld1q_p8(80 + b);
    y14 = vld1q_p8(96 + b);
    y15 = vld1q_p8(112 + b);
    // load_1024 END
    y8 = vaddq_p128(y8, y20);
    y9 = vaddq_p128(y9, y21);
    y10 = vaddq_p128(y10, y22);
    y11 = vaddq_p128(y11, y23);
    y12 = vaddq_p128(y12, y24);
    y13 = vaddq_p128(y13, y25);
    y14 = vaddq_p128(y14, y26);
    y15 = vaddq_p128(y15, y27);
    // karatsuba_512x512 BEGIN
    y21 = vaddq_p128(y9, y11);
    y25 = vaddq_p128(y8, y10);
    y22 = vaddq_p128(y13, y15);
    y26 = vaddq_p128(y12, y14);
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y3 = vmull_p64(y8, y12);
    y2 = vmull_high_p64(y8, y12);
    y20 = vextq_p64(y12, y12, 1);
    y18 = vmull_p64(y8, y20);
    y19 = vmull_high_p64(y8, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y3 = vaddq_p64(y20, y3);
    y20 = vextq_p64(y19, y18, 1);
    y2 = vaddq_p64(y20, y2);
    // mult128x128 END
    y16 = vaddq_p128(y8, y9);
    y17 = vaddq_p128(y12, y13);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y1 = vmull_p64(y9, y13);
    y0 = vmull_high_p64(y9, y13);
    y20 = vextq_p64(y13, y13, 1);
    y19 = vmull_p64(y9, y20);
    y24 = vmull_high_p64(y9, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y1 = vaddq_p64(y20, y1);
    y20 = vextq_p64(y24, y19, 1);
    y0 = vaddq_p64(y20, y0);
    // mult128x128 END
    y23 = vaddq_p128(y23, y2);
    y18 = vaddq_p128(y18, y3);
    y23 = vaddq_p128(y23, y0);
    y18 = vaddq_p128(y18, y1);
    y2 = vaddq_p128(y2, y23);
    y0 = vaddq_p128(y0, y18);
    // karatsuba_256x256 END
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y7 = vmull_p64(y10, y14);
    y6 = vmull_high_p64(y10, y14);
    y20 = vextq_p64(y14, y14, 1);
    y18 = vmull_p64(y10, y20);
    y19 = vmull_high_p64(y10, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y7 = vaddq_p64(y20, y7);
    y20 = vextq_p64(y19, y18, 1);
    y6 = vaddq_p64(y20, y6);
    // mult128x128 END
    y16 = vaddq_p128(y10, y11);
    y17 = vaddq_p128(y14, y15);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y5 = vmull_p64(y11, y15);
    y4 = vmull_high_p64(y11, y15);
    y20 = vextq_p64(y15, y15, 1);
    y19 = vmull_p64(y11, y20);
    y24 = vmull_high_p64(y11, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y5 = vaddq_p64(y20, y5);
    y20 = vextq_p64(y24, y19, 1);
    y4 = vaddq_p64(y20, y4);
    // mult128x128 END
    y23 = vaddq_p128(y23, y6);
    y18 = vaddq_p128(y18, y7);
    y23 = vaddq_p128(y23, y4);
    y18 = vaddq_p128(y18, y5);
    y6 = vaddq_p128(y6, y23);
    y4 = vaddq_p128(y4, y18);
    // karatsuba_256x256 END
    // karatsuba_256x256 BEGIN
    // mult128x128 BEGIN
    y11 = vmull_p64(y25, y26);
    y10 = vmull_high_p64(y25, y26);
    y20 = vextq_p64(y26, y26, 1);
    y18 = vmull_p64(y25, y20);
    y19 = vmull_high_p64(y25, y20);
    y18 = vaddq_p64(y18, y19);
    y19 = vdupq_n_p64(0);
    y20 = vextq_p64(y18, y19, 1);
    y11 = vaddq_p64(y20, y11);
    y20 = vextq_p64(y19, y18, 1);
    y10 = vaddq_p64(y20, y10);
    // mult128x128 END
    y16 = vaddq_p128(y25, y21);
    y17 = vaddq_p128(y26, y22);
    // mult128x128 BEGIN
    y18 = vmull_p64(y16, y17);
    y23 = vmull_high_p64(y16, y17);
    y20 = vextq_p64(y17, y17, 1);
    y19 = vmull_p64(y16, y20);
    y24 = vmull_high_p64(y16, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y18 = vaddq_p64(y20, y18);
    y20 = vextq_p64(y24, y19, 1);
    y23 = vaddq_p64(y20, y23);
    // mult128x128 END
    // mult128x128 BEGIN
    y9 = vmull_p64(y21, y22);
    y8 = vmull_high_p64(y21, y22);
    y20 = vextq_p64(y22, y22, 1);
    y19 = vmull_p64(y21, y20);
    y24 = vmull_high_p64(y21, y20);
    y19 = vaddq_p64(y19, y24);
    y24 = vdupq_n_p64(0);
    y20 = vextq_p64(y19, y24, 1);
    y9 = vaddq_p64(y20, y9);
    y20 = vextq_p64(y24, y19, 1);
    y8 = vaddq_p64(y20, y8);
    // mult128x128 END
    y23 = vaddq_p128(y23, y10);
    y18 = vaddq_p128(y18, y11);
    y23 = vaddq_p128(y23, y8);
    y18 = vaddq_p128(y18, y9);
    y10 = vaddq_p128(y10, y23);
    y8 = vaddq_p128(y8, y18);
    // karatsuba_256x256 END
    y8 = vaddq_p128(y0, y8);
    y9 = vaddq_p128(y1, y9);
    y10 = vaddq_p128(y2, y10);
    y11 = vaddq_p128(y3, y11);
    y8 = vaddq_p128(y4, y8);
    y9 = vaddq_p128(y5, y9);
    y10 = vaddq_p128(y6, y10);
    y11 = vaddq_p128(y7, y11);
    y2 = vaddq_p128(y8, y2);
    y3 = vaddq_p128(y9, y3);
    y4 = vaddq_p128(y10, y4);
    y5 = vaddq_p128(y11, y5);
    // karatsuba_512x512 END
    // load_1024 BEGIN
    y8 = vld1q_p8(0 + c);
    y9 = vld1q_p8(16 + c);
    y10 = vld1q_p8(32 + c);
    y11 = vld1q_p8(48 + c);
    y12 = vld1q_p8(64 + c);
    y13 = vld1q_p8(80 + c);
    y14 = vld1q_p8(96 + c);
    y15 = vld1q_p8(112 + c);
    // load_1024 END
    // mul512_and_accumulate BEGIN
    y12 = vaddq_p128(y0, y12);
    y13 = vaddq_p128(y1, y13);
    y22 = 0x1fffffffffffff;
    y23 = y3 & y22;
    y14 = vaddq_p128(y2, y14);
    y15 = vaddq_p128(y23, y15);
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y17 = vandq_u16(y3, y23);
    y16 = y2 << 11;
    y17 = y17 << 11;
    y23 = vextq_p64(y17, y16, 1);
    y22 = vextq_p64(y16, y17, 1);
    y17 = y3 >> 53;
    y16 = y2 >> 53;
    y17 = vaddq_p128(y17, y23);
    y16 = vaddq_p128(y16, y22);
    // vec256_sr53 END
    // vec256_sl203 BEGIN
    y18 = 0;
    y19 = y5 & 0xffffffffffffffff;
    y23 = vextq_p64(y19, y18, 1);
    y22 = vextq_p64(y18, y19, 1);
    y19 = y23 << 11;
    y18 = y22 << 11;
    // vec256_sl203 END
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y21 = vandq_u16(y5, y23);
    y20 = y4 << 11;
    y21 = y21 << 11;
    y23 = vextq_p64(y21, y20, 1);
    y22 = vextq_p64(y20, y21, 1);
    y21 = y5 >> 53;
    y20 = y4 >> 53;
    y21 = vaddq_p128(y21, y23);
    y20 = vaddq_p128(y20, y22);
    // vec256_sr53 END
    y18 = vaddq_p128(y16, y18);
    y19 = vaddq_p128(y17, y19);
    y8 = vaddq_p128(y18, y8);
    y9 = vaddq_p128(y19, y9);
    // vec256_sl203 BEGIN
    y16 = 0;
    y17 = y7 & 0xffffffffffffffff;
    y23 = vextq_p64(y17, y16, 1);
    y22 = vextq_p64(y16, y17, 1);
    y17 = y23 << 11;
    y16 = y22 << 11;
    // vec256_sl203 END
    // vec256_sr53 BEGIN
    y23 = 0xffffffffffffffff0000000000000000;
    y19 = vandq_u16(y7, y23);
    y18 = y6 << 11;
    y19 = y19 << 11;
    y23 = vextq_p64(y19, y18, 1);
    y22 = vextq_p64(y18, y19, 1);
    y19 = y7 >> 53;
    y18 = y6 >> 53;
    y19 = vaddq_p128(y19, y23);
    y18 = vaddq_p128(y18, y22);
    // vec256_sr53 END
    y20 = vaddq_p128(y16, y20);
    y21 = vaddq_p128(y17, y21);
    y10 = vaddq_p128(y20, y10);
    y11 = vaddq_p128(y21, y11);
    y12 = vaddq_p128(y18, y12);
    y13 = vaddq_p128(y19, y13);
    // mul512_and_accumulate END
    // store_1024 BEGIN
    vst1q_p8(0 + c, y8);
    vst1q_p8(16 + c, y9);
    vst1q_p8(32 + c, y10);
    vst1q_p8(48 + c, y11);
    vst1q_p8(64 + c, y12);
    vst1q_p8(80 + c, y13);
    vst1q_p8(96 + c, y14);
    vst1q_p8(112 + c, y15);
    // store_1024 END
}
