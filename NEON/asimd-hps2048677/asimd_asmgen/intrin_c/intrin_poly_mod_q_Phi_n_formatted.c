#include "../../poly.h"
#include <arm_neon.h>

void poly_mod_q_Phi_n(poly *r) {
  uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7;
  y3 = vdupq_n_u16(0);
  y2 = vld1q_u16(672 + r->coeffs);
  y2 = vdupq_laneq_u16(y2, 5);
  // 0 -> 16
  y0 = vld1q_u16(0 + r->coeffs);
  y1 = vld1q_u16(8 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(0 + r->coeffs, y0);
  vst1q_u16(8 + r->coeffs, y1);
  // 16 -> 32
  y0 = vld1q_u16(16 + r->coeffs);
  y1 = vld1q_u16(24 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(16 + r->coeffs, y0);
  vst1q_u16(24 + r->coeffs, y1);
  // 32 -> 48
  y0 = vld1q_u16(32 + r->coeffs);
  y1 = vld1q_u16(40 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(32 + r->coeffs, y0);
  vst1q_u16(40 + r->coeffs, y1);
  // 48 -> 64
  y0 = vld1q_u16(48 + r->coeffs);
  y1 = vld1q_u16(56 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(48 + r->coeffs, y0);
  vst1q_u16(56 + r->coeffs, y1);
  // 64 -> 80
  y0 = vld1q_u16(64 + r->coeffs);
  y1 = vld1q_u16(72 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(64 + r->coeffs, y0);
  vst1q_u16(72 + r->coeffs, y1);
  // 80 -> 96
  y0 = vld1q_u16(80 + r->coeffs);
  y1 = vld1q_u16(88 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(80 + r->coeffs, y0);
  vst1q_u16(88 + r->coeffs, y1);
  // 96 -> 112
  y0 = vld1q_u16(96 + r->coeffs);
  y1 = vld1q_u16(104 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(96 + r->coeffs, y0);
  vst1q_u16(104 + r->coeffs, y1);
  // 112 -> 128
  y0 = vld1q_u16(112 + r->coeffs);
  y1 = vld1q_u16(120 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(112 + r->coeffs, y0);
  vst1q_u16(120 + r->coeffs, y1);
  // 128 -> 144
  y0 = vld1q_u16(128 + r->coeffs);
  y1 = vld1q_u16(136 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(128 + r->coeffs, y0);
  vst1q_u16(136 + r->coeffs, y1);
  // 144 -> 160
  y0 = vld1q_u16(144 + r->coeffs);
  y1 = vld1q_u16(152 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(144 + r->coeffs, y0);
  vst1q_u16(152 + r->coeffs, y1);
  // 160 -> 176
  y0 = vld1q_u16(160 + r->coeffs);
  y1 = vld1q_u16(168 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(160 + r->coeffs, y0);
  vst1q_u16(168 + r->coeffs, y1);
  // 176 -> 192
  y0 = vld1q_u16(176 + r->coeffs);
  y1 = vld1q_u16(184 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(176 + r->coeffs, y0);
  vst1q_u16(184 + r->coeffs, y1);
  // 192 -> 208
  y0 = vld1q_u16(192 + r->coeffs);
  y1 = vld1q_u16(200 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(192 + r->coeffs, y0);
  vst1q_u16(200 + r->coeffs, y1);
  // 208 -> 224
  y0 = vld1q_u16(208 + r->coeffs);
  y1 = vld1q_u16(216 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(208 + r->coeffs, y0);
  vst1q_u16(216 + r->coeffs, y1);
  // 224 -> 240
  y0 = vld1q_u16(224 + r->coeffs);
  y1 = vld1q_u16(232 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(224 + r->coeffs, y0);
  vst1q_u16(232 + r->coeffs, y1);
  // 240 -> 256
  y0 = vld1q_u16(240 + r->coeffs);
  y1 = vld1q_u16(248 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(240 + r->coeffs, y0);
  vst1q_u16(248 + r->coeffs, y1);
  // 256 -> 272
  y0 = vld1q_u16(256 + r->coeffs);
  y1 = vld1q_u16(264 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(256 + r->coeffs, y0);
  vst1q_u16(264 + r->coeffs, y1);
  // 272 -> 288
  y0 = vld1q_u16(272 + r->coeffs);
  y1 = vld1q_u16(280 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(272 + r->coeffs, y0);
  vst1q_u16(280 + r->coeffs, y1);
  // 288 -> 304
  y0 = vld1q_u16(288 + r->coeffs);
  y1 = vld1q_u16(296 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(288 + r->coeffs, y0);
  vst1q_u16(296 + r->coeffs, y1);
  // 304 -> 320
  y0 = vld1q_u16(304 + r->coeffs);
  y1 = vld1q_u16(312 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(304 + r->coeffs, y0);
  vst1q_u16(312 + r->coeffs, y1);
  // 320 -> 336
  y0 = vld1q_u16(320 + r->coeffs);
  y1 = vld1q_u16(328 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(320 + r->coeffs, y0);
  vst1q_u16(328 + r->coeffs, y1);
  // 336 -> 352
  y0 = vld1q_u16(336 + r->coeffs);
  y1 = vld1q_u16(344 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(336 + r->coeffs, y0);
  vst1q_u16(344 + r->coeffs, y1);
  // 352 -> 368
  y0 = vld1q_u16(352 + r->coeffs);
  y1 = vld1q_u16(360 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(352 + r->coeffs, y0);
  vst1q_u16(360 + r->coeffs, y1);
  // 368 -> 384
  y0 = vld1q_u16(368 + r->coeffs);
  y1 = vld1q_u16(376 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(368 + r->coeffs, y0);
  vst1q_u16(376 + r->coeffs, y1);
  // 384 -> 400
  y0 = vld1q_u16(384 + r->coeffs);
  y1 = vld1q_u16(392 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(384 + r->coeffs, y0);
  vst1q_u16(392 + r->coeffs, y1);
  // 400 -> 416
  y0 = vld1q_u16(400 + r->coeffs);
  y1 = vld1q_u16(408 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(400 + r->coeffs, y0);
  vst1q_u16(408 + r->coeffs, y1);
  // 416 -> 432
  y0 = vld1q_u16(416 + r->coeffs);
  y1 = vld1q_u16(424 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(416 + r->coeffs, y0);
  vst1q_u16(424 + r->coeffs, y1);
  // 432 -> 448
  y0 = vld1q_u16(432 + r->coeffs);
  y1 = vld1q_u16(440 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(432 + r->coeffs, y0);
  vst1q_u16(440 + r->coeffs, y1);
  // 448 -> 464
  y0 = vld1q_u16(448 + r->coeffs);
  y1 = vld1q_u16(456 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(448 + r->coeffs, y0);
  vst1q_u16(456 + r->coeffs, y1);
  // 464 -> 480
  y0 = vld1q_u16(464 + r->coeffs);
  y1 = vld1q_u16(472 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(464 + r->coeffs, y0);
  vst1q_u16(472 + r->coeffs, y1);
  // 480 -> 496
  y0 = vld1q_u16(480 + r->coeffs);
  y1 = vld1q_u16(488 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(480 + r->coeffs, y0);
  vst1q_u16(488 + r->coeffs, y1);
  // 496 -> 512
  y0 = vld1q_u16(496 + r->coeffs);
  y1 = vld1q_u16(504 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(496 + r->coeffs, y0);
  vst1q_u16(504 + r->coeffs, y1);
  // 512 -> 528
  y0 = vld1q_u16(512 + r->coeffs);
  y1 = vld1q_u16(520 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(512 + r->coeffs, y0);
  vst1q_u16(520 + r->coeffs, y1);
  // 528 -> 544
  y0 = vld1q_u16(528 + r->coeffs);
  y1 = vld1q_u16(536 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(528 + r->coeffs, y0);
  vst1q_u16(536 + r->coeffs, y1);
  // 544 -> 560
  y0 = vld1q_u16(544 + r->coeffs);
  y1 = vld1q_u16(552 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(544 + r->coeffs, y0);
  vst1q_u16(552 + r->coeffs, y1);
  // 560 -> 576
  y0 = vld1q_u16(560 + r->coeffs);
  y1 = vld1q_u16(568 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(560 + r->coeffs, y0);
  vst1q_u16(568 + r->coeffs, y1);
  // 576 -> 592
  y0 = vld1q_u16(576 + r->coeffs);
  y1 = vld1q_u16(584 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(576 + r->coeffs, y0);
  vst1q_u16(584 + r->coeffs, y1);
  // 592 -> 608
  y0 = vld1q_u16(592 + r->coeffs);
  y1 = vld1q_u16(600 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(592 + r->coeffs, y0);
  vst1q_u16(600 + r->coeffs, y1);
  // 608 -> 624
  y0 = vld1q_u16(608 + r->coeffs);
  y1 = vld1q_u16(616 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(608 + r->coeffs, y0);
  vst1q_u16(616 + r->coeffs, y1);
  // 624 -> 640
  y0 = vld1q_u16(624 + r->coeffs);
  y1 = vld1q_u16(632 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(624 + r->coeffs, y0);
  vst1q_u16(632 + r->coeffs, y1);
  // 640 -> 656
  y0 = vld1q_u16(640 + r->coeffs);
  y1 = vld1q_u16(648 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(640 + r->coeffs, y0);
  vst1q_u16(648 + r->coeffs, y1);
  // 656 -> 672
  y0 = vld1q_u16(656 + r->coeffs);
  y1 = vld1q_u16(664 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(656 + r->coeffs, y0);
  vst1q_u16(664 + r->coeffs, y1);
  // 672 -> 688
  y0 = vld1q_u16(672 + r->coeffs);
  y1 = vld1q_u16(680 + r->coeffs);
  y0 = vsubq_u16(y0, y2);
  y1 = vsubq_u16(y1, y2);
  vst1q_u16(672 + r->coeffs, y0);
  vst1q_u16(680 + r->coeffs, y1);
  vst1q_u16(85 + r->coeffs, y3);
  vst1q_u16(86 + r->coeffs, y3);
  vst1q_u16(87 + r->coeffs, y3);
  r->coeffs[677] = 0;
  r->coeffs[678] = 0;
  r->coeffs[679] = 0;
  r->coeffs[680] = 0;
  r->coeffs[681] = 0;
  r->coeffs[682] = 0;
  r->coeffs[683] = 0;
  r->coeffs[684] = 0;
  r->coeffs[685] = 0;
  r->coeffs[686] = 0;
  r->coeffs[687] = 0;
  r->coeffs[688] = 0;
  r->coeffs[689] = 0;
  r->coeffs[690] = 0;
  r->coeffs[691] = 0;
  r->coeffs[692] = 0;
  r->coeffs[693] = 0;
  r->coeffs[694] = 0;
  r->coeffs[695] = 0;
  r->coeffs[696] = 0;
  r->coeffs[697] = 0;
  r->coeffs[698] = 0;
  r->coeffs[699] = 0;
  r->coeffs[700] = 0;
  r->coeffs[701] = 0;
  r->coeffs[702] = 0;
  r->coeffs[703] = 0;
}
