#include <arm_neon.h>
#include <stdio.h>

#define SIZE 48*16

int main()
{
	uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31, y32, y33, y34, y35;
	uint16_t in[SIZE] ={0}; 
    uint16_t out[SIZE] ={0}; 
	for (uint16_t i = 0; i < SIZE; i++)
	{
		in[i] = i;
	}
for (uint16_t i = 0; i < SIZE; i++)
	{
		if (i % 16 == 0)
		printf("\n");

		printf("%4d ", in[i]);
	}

// -------------- n = 0
// 16x16: LD A1
y0 = vld1q_u16(in + 0);
y1 = vld1q_u16(in + 48);
y2 = vld1q_u16(in + 96);
y3 = vld1q_u16(in + 144);
y4 = vld1q_u16(in + 192);
y5 = vld1q_u16(in + 240);
y6 = vld1q_u16(in + 288);
y7 = vld1q_u16(in + 336);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y17 = vtrn2q_u16(y0, y1);
y18 = vtrn1q_u16(y2, y3);
y19 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y17);
y25 = vtrn2q_u32(y16, y17);
y26 = vtrn1q_u32(y18, y19);
y27 = vtrn2q_u32(y18, y19);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y17 = vtrn2q_u16(y4, y5);
y18 = vtrn1q_u16(y6, y7);
y19 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y17);
y25 = vtrn2q_u32(y16, y17);
y26 = vtrn1q_u32(y18, y19);
y27 = vtrn2q_u32(y18, y19);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y17 = vtrn2q_u64(y8, y12);
y18 = vtrn1q_u64(y10, y14);
y19 = vtrn2q_u64(y10, y14);
y20 = vtrn1q_u64(y9, y13);
y21 = vtrn2q_u64(y9, y13);
y22 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: STR A1
vst1q_u16(out + 0, y16);
vst1q_u16(out + 16, y18);
vst1q_u16(out + 32, y20);
vst1q_u16(out + 48, y22);
vst1q_u16(out + 64, y17);
vst1q_u16(out + 80, y19);
vst1q_u16(out + 96, y21);
vst1q_u16(out + 112, y23);
// 16x16: LD A4
y0 = vld1q_u16(in + 408);
y1 = vld1q_u16(in + 456);
y2 = vld1q_u16(in + 504);
y3 = vld1q_u16(in + 552);
y4 = vld1q_u16(in + 600);
y5 = vld1q_u16(in + 648);
y6 = vld1q_u16(in + 696);
y7 = vld1q_u16(in + 744);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y18 = vtrn2q_u16(y0, y1);
y20 = vtrn1q_u16(y2, y3);
y22 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y18);
y25 = vtrn2q_u32(y16, y18);
y26 = vtrn1q_u32(y20, y22);
y27 = vtrn2q_u32(y20, y22);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y18 = vtrn2q_u16(y4, y5);
y20 = vtrn1q_u16(y6, y7);
y22 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y18);
y25 = vtrn2q_u32(y16, y18);
y26 = vtrn1q_u32(y20, y22);
y27 = vtrn2q_u32(y20, y22);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y18 = vtrn2q_u64(y8, y12);
y20 = vtrn1q_u64(y10, y14);
y22 = vtrn2q_u64(y10, y14);
y17 = vtrn1q_u64(y9, y13);
y19 = vtrn2q_u64(y9, y13);
y21 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: STR A4
vst1q_u16(out + 392, y16);
vst1q_u16(out + 408, y20);
vst1q_u16(out + 424, y17);
vst1q_u16(out + 440, y21);
vst1q_u16(out + 456, y18);
vst1q_u16(out + 472, y22);
vst1q_u16(out + 488, y19);
vst1q_u16(out + 504, y23);
// 16x16: LD A2
y0 = vld1q_u16(in + 24);
y1 = vld1q_u16(in + 72);
y2 = vld1q_u16(in + 120);
y3 = vld1q_u16(in + 168);
y4 = vld1q_u16(in + 216);
y5 = vld1q_u16(in + 264);
y6 = vld1q_u16(in + 312);
y7 = vld1q_u16(in + 360);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y20 = vtrn2q_u16(y0, y1);
y17 = vtrn1q_u16(y2, y3);
y21 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y20);
y25 = vtrn2q_u32(y16, y20);
y26 = vtrn1q_u32(y17, y21);
y27 = vtrn2q_u32(y17, y21);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y20 = vtrn2q_u16(y4, y5);
y17 = vtrn1q_u16(y6, y7);
y21 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y20);
y25 = vtrn2q_u32(y16, y20);
y26 = vtrn1q_u32(y17, y21);
y27 = vtrn2q_u32(y17, y21);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y20 = vtrn2q_u64(y8, y12);
y17 = vtrn1q_u64(y10, y14);
y21 = vtrn2q_u64(y10, y14);
y18 = vtrn1q_u64(y9, y13);
y22 = vtrn2q_u64(y9, y13);
y19 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: LD A3
y0 = vld1q_u16(in + 384);
y1 = vld1q_u16(in + 432);
y2 = vld1q_u16(in + 480);
y3 = vld1q_u16(in + 528);
y4 = vld1q_u16(in + 576);
y5 = vld1q_u16(in + 624);
y6 = vld1q_u16(in + 672);
y7 = vld1q_u16(in + 720);
// Transpose 8x8
y28 = vtrn1q_u16(y0, y1);
y29 = vtrn2q_u16(y0, y1);
y30 = vtrn1q_u16(y2, y3);
y31 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y28, y29);
y25 = vtrn2q_u32(y28, y29);
y26 = vtrn1q_u32(y30, y31);
y27 = vtrn2q_u32(y30, y31);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y28 = vtrn1q_u16(y4, y5);
y29 = vtrn2q_u16(y4, y5);
y30 = vtrn1q_u16(y6, y7);
y31 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y28, y29);
y25 = vtrn2q_u32(y28, y29);
y26 = vtrn1q_u32(y30, y31);
y27 = vtrn2q_u32(y30, y31);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y28 = vtrn1q_u64(y8, y12);
y29 = vtrn2q_u64(y8, y12);
y30 = vtrn1q_u64(y10, y14);
y31 = vtrn2q_u64(y10, y14);
y32 = vtrn1q_u64(y9, y13);
y33 = vtrn2q_u64(y9, y13);
y34 = vtrn1q_u64(y11, y15);
y35 = vtrn2q_u64(y11, y15);
// 16x16: STR A2<-A3
vst1q_u16(out + 8, y28);
vst1q_u16(out + 24, y30);
vst1q_u16(out + 40, y32);
vst1q_u16(out + 56, y34);
vst1q_u16(out + 72, y29);
vst1q_u16(out + 88, y31);
vst1q_u16(out + 104, y33);
vst1q_u16(out + 120, y35);
// 16x16: STR A3<-A2
vst1q_u16(out + 384, y16);
vst1q_u16(out + 400, y17);
vst1q_u16(out + 416, y18);
vst1q_u16(out + 432, y19);
vst1q_u16(out + 448, y20);
vst1q_u16(out + 464, y21);
vst1q_u16(out + 480, y22);
vst1q_u16(out + 496, y23);
// -------------- n = 1
// 16x16: LD A1
y0 = vld1q_u16(in + 8);
y1 = vld1q_u16(in + 56);
y2 = vld1q_u16(in + 104);
y3 = vld1q_u16(in + 152);
y4 = vld1q_u16(in + 200);
y5 = vld1q_u16(in + 248);
y6 = vld1q_u16(in + 296);
y7 = vld1q_u16(in + 344);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y17 = vtrn2q_u16(y0, y1);
y18 = vtrn1q_u16(y2, y3);
y19 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y17);
y25 = vtrn2q_u32(y16, y17);
y26 = vtrn1q_u32(y18, y19);
y27 = vtrn2q_u32(y18, y19);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y17 = vtrn2q_u16(y4, y5);
y18 = vtrn1q_u16(y6, y7);
y19 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y17);
y25 = vtrn2q_u32(y16, y17);
y26 = vtrn1q_u32(y18, y19);
y27 = vtrn2q_u32(y18, y19);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y17 = vtrn2q_u64(y8, y12);
y18 = vtrn1q_u64(y10, y14);
y19 = vtrn2q_u64(y10, y14);
y20 = vtrn1q_u64(y9, y13);
y21 = vtrn2q_u64(y9, y13);
y22 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: STR A1
vst1q_u16(out + 128, y16);
vst1q_u16(out + 144, y18);
vst1q_u16(out + 160, y20);
vst1q_u16(out + 176, y22);
vst1q_u16(out + 192, y17);
vst1q_u16(out + 208, y19);
vst1q_u16(out + 224, y21);
vst1q_u16(out + 240, y23);
// 16x16: LD A4
y0 = vld1q_u16(in + 416);
y1 = vld1q_u16(in + 464);
y2 = vld1q_u16(in + 512);
y3 = vld1q_u16(in + 560);
y4 = vld1q_u16(in + 608);
y5 = vld1q_u16(in + 656);
y6 = vld1q_u16(in + 704);
y7 = vld1q_u16(in + 752);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y18 = vtrn2q_u16(y0, y1);
y20 = vtrn1q_u16(y2, y3);
y22 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y18);
y25 = vtrn2q_u32(y16, y18);
y26 = vtrn1q_u32(y20, y22);
y27 = vtrn2q_u32(y20, y22);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y18 = vtrn2q_u16(y4, y5);
y20 = vtrn1q_u16(y6, y7);
y22 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y18);
y25 = vtrn2q_u32(y16, y18);
y26 = vtrn1q_u32(y20, y22);
y27 = vtrn2q_u32(y20, y22);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y18 = vtrn2q_u64(y8, y12);
y20 = vtrn1q_u64(y10, y14);
y22 = vtrn2q_u64(y10, y14);
y17 = vtrn1q_u64(y9, y13);
y19 = vtrn2q_u64(y9, y13);
y21 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: STR A4
vst1q_u16(out + 520, y16);
vst1q_u16(out + 536, y20);
vst1q_u16(out + 552, y17);
vst1q_u16(out + 568, y21);
vst1q_u16(out + 584, y18);
vst1q_u16(out + 600, y22);
vst1q_u16(out + 616, y19);
vst1q_u16(out + 632, y23);
// 16x16: LD A2
y0 = vld1q_u16(in + 32);
y1 = vld1q_u16(in + 80);
y2 = vld1q_u16(in + 128);
y3 = vld1q_u16(in + 176);
y4 = vld1q_u16(in + 224);
y5 = vld1q_u16(in + 272);
y6 = vld1q_u16(in + 320);
y7 = vld1q_u16(in + 368);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y20 = vtrn2q_u16(y0, y1);
y17 = vtrn1q_u16(y2, y3);
y21 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y20);
y25 = vtrn2q_u32(y16, y20);
y26 = vtrn1q_u32(y17, y21);
y27 = vtrn2q_u32(y17, y21);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y20 = vtrn2q_u16(y4, y5);
y17 = vtrn1q_u16(y6, y7);
y21 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y20);
y25 = vtrn2q_u32(y16, y20);
y26 = vtrn1q_u32(y17, y21);
y27 = vtrn2q_u32(y17, y21);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y20 = vtrn2q_u64(y8, y12);
y17 = vtrn1q_u64(y10, y14);
y21 = vtrn2q_u64(y10, y14);
y18 = vtrn1q_u64(y9, y13);
y22 = vtrn2q_u64(y9, y13);
y19 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: LD A3
y0 = vld1q_u16(in + 392);
y1 = vld1q_u16(in + 440);
y2 = vld1q_u16(in + 488);
y3 = vld1q_u16(in + 536);
y4 = vld1q_u16(in + 584);
y5 = vld1q_u16(in + 632);
y6 = vld1q_u16(in + 680);
y7 = vld1q_u16(in + 728);
// Transpose 8x8
y28 = vtrn1q_u16(y0, y1);
y29 = vtrn2q_u16(y0, y1);
y30 = vtrn1q_u16(y2, y3);
y31 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y28, y29);
y25 = vtrn2q_u32(y28, y29);
y26 = vtrn1q_u32(y30, y31);
y27 = vtrn2q_u32(y30, y31);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y28 = vtrn1q_u16(y4, y5);
y29 = vtrn2q_u16(y4, y5);
y30 = vtrn1q_u16(y6, y7);
y31 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y28, y29);
y25 = vtrn2q_u32(y28, y29);
y26 = vtrn1q_u32(y30, y31);
y27 = vtrn2q_u32(y30, y31);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y28 = vtrn1q_u64(y8, y12);
y29 = vtrn2q_u64(y8, y12);
y30 = vtrn1q_u64(y10, y14);
y31 = vtrn2q_u64(y10, y14);
y32 = vtrn1q_u64(y9, y13);
y33 = vtrn2q_u64(y9, y13);
y34 = vtrn1q_u64(y11, y15);
y35 = vtrn2q_u64(y11, y15);
// 16x16: STR A2<-A3
vst1q_u16(out + 136, y28);
vst1q_u16(out + 152, y30);
vst1q_u16(out + 168, y32);
vst1q_u16(out + 184, y34);
vst1q_u16(out + 200, y29);
vst1q_u16(out + 216, y31);
vst1q_u16(out + 232, y33);
vst1q_u16(out + 248, y35);
// 16x16: STR A3<-A2
vst1q_u16(out + 512, y16);
vst1q_u16(out + 528, y17);
vst1q_u16(out + 544, y18);
vst1q_u16(out + 560, y19);
vst1q_u16(out + 576, y20);
vst1q_u16(out + 592, y21);
vst1q_u16(out + 608, y22);
vst1q_u16(out + 624, y23);
// -------------- n = 2
// 16x16: LD A1
y0 = vld1q_u16(in + 16);
y1 = vld1q_u16(in + 64);
y2 = vld1q_u16(in + 112);
y3 = vld1q_u16(in + 160);
y4 = vld1q_u16(in + 208);
y5 = vld1q_u16(in + 256);
y6 = vld1q_u16(in + 304);
y7 = vld1q_u16(in + 352);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y17 = vtrn2q_u16(y0, y1);
y18 = vtrn1q_u16(y2, y3);
y19 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y17);
y25 = vtrn2q_u32(y16, y17);
y26 = vtrn1q_u32(y18, y19);
y27 = vtrn2q_u32(y18, y19);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y17 = vtrn2q_u16(y4, y5);
y18 = vtrn1q_u16(y6, y7);
y19 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y17);
y25 = vtrn2q_u32(y16, y17);
y26 = vtrn1q_u32(y18, y19);
y27 = vtrn2q_u32(y18, y19);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y17 = vtrn2q_u64(y8, y12);
y18 = vtrn1q_u64(y10, y14);
y19 = vtrn2q_u64(y10, y14);
y20 = vtrn1q_u64(y9, y13);
y21 = vtrn2q_u64(y9, y13);
y22 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: STR A1
vst1q_u16(out + 256, y16);
vst1q_u16(out + 272, y18);
vst1q_u16(out + 288, y20);
vst1q_u16(out + 304, y22);
vst1q_u16(out + 320, y17);
vst1q_u16(out + 336, y19);
vst1q_u16(out + 352, y21);
vst1q_u16(out + 368, y23);
// 16x16: LD A4
y0 = vld1q_u16(in + 424);
y1 = vld1q_u16(in + 472);
y2 = vld1q_u16(in + 520);
y3 = vld1q_u16(in + 568);
y4 = vld1q_u16(in + 616);
y5 = vld1q_u16(in + 664);
y6 = vld1q_u16(in + 712);
y7 = vld1q_u16(in + 760);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y18 = vtrn2q_u16(y0, y1);
y20 = vtrn1q_u16(y2, y3);
y22 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y18);
y25 = vtrn2q_u32(y16, y18);
y26 = vtrn1q_u32(y20, y22);
y27 = vtrn2q_u32(y20, y22);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y18 = vtrn2q_u16(y4, y5);
y20 = vtrn1q_u16(y6, y7);
y22 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y18);
y25 = vtrn2q_u32(y16, y18);
y26 = vtrn1q_u32(y20, y22);
y27 = vtrn2q_u32(y20, y22);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y18 = vtrn2q_u64(y8, y12);
y20 = vtrn1q_u64(y10, y14);
y22 = vtrn2q_u64(y10, y14);
y17 = vtrn1q_u64(y9, y13);
y19 = vtrn2q_u64(y9, y13);
y21 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: STR A4
vst1q_u16(out + 648, y16);
vst1q_u16(out + 664, y20);
vst1q_u16(out + 680, y17);
vst1q_u16(out + 696, y21);
// 16x16: LD A2
y0 = vld1q_u16(in + 40);
y1 = vld1q_u16(in + 88);
y2 = vld1q_u16(in + 136);
y3 = vld1q_u16(in + 184);
y4 = vld1q_u16(in + 232);
y5 = vld1q_u16(in + 280);
y6 = vld1q_u16(in + 328);
y7 = vld1q_u16(in + 376);
// Transpose 8x8
y16 = vtrn1q_u16(y0, y1);
y20 = vtrn2q_u16(y0, y1);
y17 = vtrn1q_u16(y2, y3);
y21 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y16, y20);
y25 = vtrn2q_u32(y16, y20);
y26 = vtrn1q_u32(y17, y21);
y27 = vtrn2q_u32(y17, y21);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u16(y4, y5);
y20 = vtrn2q_u16(y4, y5);
y17 = vtrn1q_u16(y6, y7);
y21 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y16, y20);
y25 = vtrn2q_u32(y16, y20);
y26 = vtrn1q_u32(y17, y21);
y27 = vtrn2q_u32(y17, y21);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y16 = vtrn1q_u64(y8, y12);
y20 = vtrn2q_u64(y8, y12);
y17 = vtrn1q_u64(y10, y14);
y21 = vtrn2q_u64(y10, y14);
y18 = vtrn1q_u64(y9, y13);
y22 = vtrn2q_u64(y9, y13);
y19 = vtrn1q_u64(y11, y15);
y23 = vtrn2q_u64(y11, y15);
// 16x16: LD A3
y0 = vld1q_u16(in + 400);
y1 = vld1q_u16(in + 448);
y2 = vld1q_u16(in + 496);
y3 = vld1q_u16(in + 544);
y4 = vld1q_u16(in + 592);
y5 = vld1q_u16(in + 640);
y6 = vld1q_u16(in + 688);
y7 = vld1q_u16(in + 736);
// Transpose 8x8
y28 = vtrn1q_u16(y0, y1);
y29 = vtrn2q_u16(y0, y1);
y30 = vtrn1q_u16(y2, y3);
y31 = vtrn2q_u16(y2, y3);
y24 = vtrn1q_u32(y28, y29);
y25 = vtrn2q_u32(y28, y29);
y26 = vtrn1q_u32(y30, y31);
y27 = vtrn2q_u32(y30, y31);
y8 = vtrn1q_u32(y24, y26);
y10 = vtrn2q_u32(y24, y26);
y9 = vtrn1q_u32(y25, y27);
y11 = vtrn2q_u32(y25, y27);
y28 = vtrn1q_u16(y4, y5);
y29 = vtrn2q_u16(y4, y5);
y30 = vtrn1q_u16(y6, y7);
y31 = vtrn2q_u16(y6, y7);
y24 = vtrn1q_u32(y28, y29);
y25 = vtrn2q_u32(y28, y29);
y26 = vtrn1q_u32(y30, y31);
y27 = vtrn2q_u32(y30, y31);
y12 = vtrn1q_u32(y24, y26);
y14 = vtrn2q_u32(y24, y26);
y13 = vtrn1q_u32(y25, y27);
y15 = vtrn2q_u32(y25, y27);
y28 = vtrn1q_u64(y8, y12);
y29 = vtrn2q_u64(y8, y12);
y30 = vtrn1q_u64(y10, y14);
y31 = vtrn2q_u64(y10, y14);
y32 = vtrn1q_u64(y9, y13);
y33 = vtrn2q_u64(y9, y13);
y34 = vtrn1q_u64(y11, y15);
y35 = vtrn2q_u64(y11, y15);
// 16x16: STR A2<-A3
vst1q_u16(out + 264, y28);
vst1q_u16(out + 280, y30);
vst1q_u16(out + 296, y32);
vst1q_u16(out + 312, y34);
vst1q_u16(out + 328, y29);
vst1q_u16(out + 344, y31);
vst1q_u16(out + 360, y33);
vst1q_u16(out + 376, y35);
// 16x16: STR A3<-A2
vst1q_u16(out + 640, y16);
vst1q_u16(out + 656, y17);
vst1q_u16(out + 672, y18);
vst1q_u16(out + 688, y19);

printf("\n=======================\n");

for (uint16_t i = 0; i < SIZE; i++)
	{
		if (i % 16 == 0)
		printf("\n");

		printf("%4d ", out[i]);
	}
printf("\n=======================\n");
}

