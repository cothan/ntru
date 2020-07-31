/*=============================================================================
 * Copyright (c) 2020 by Cryptographic Engineering Research Group (CERG)
 * ECE Department, George Mason University
 * Fairfax, VA, U.S.A.
 * Author: Duc Tri Nguyen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

=============================================================================*/
#include <arm_neon.h>

#include "../params.h"
#include "neon_batch_multiplication.h"
#include "neon_matrix_transpose.h"

#define SB0 (NTRU_N_PAD / 2) // 256
#define SB1 (SB0 / 4)        // 64
#define SB2 (SB1 / 2)        // 32
#define SB3 (SB2 / 2)        // 16

#define SB0_RES (2 * SB0) // 512
#define SB1_RES (2 * SB1) // 128
#define SB2_RES (2 * SB2) // 64
#define SB3_RES (2 * SB3) // 32

// load c <= a
#define vload(c, a) c = vld1q_u16_x4(a);

// store c <= a
#define vstore(c, a) vst1q_u16_x4(c, a);

#define inv3 43691
#define inv15 61167

// c = a << value
#define vsl(c, a, value)                     \
    c.val[0] = vshlq_n_u16(a.val[0], value); \
    c.val[1] = vshlq_n_u16(a.val[1], value); \
    c.val[2] = vshlq_n_u16(a.val[2], value); \
    c.val[3] = vshlq_n_u16(a.val[3], value);

// c = a >> value
#define vsr(c, a, value)                     \
    c.val[0] = vshrq_n_u16(a.val[0], value); \
    c.val[1] = vshrq_n_u16(a.val[1], value); \
    c.val[2] = vshrq_n_u16(a.val[2], value); \
    c.val[3] = vshrq_n_u16(a.val[3], value);

// c = a + b
#define vadd(c, a, b)                         \
    c.val[0] = vaddq_u16(a.val[0], b.val[0]); \
    c.val[1] = vaddq_u16(a.val[1], b.val[1]); \
    c.val[2] = vaddq_u16(a.val[2], b.val[2]); \
    c.val[3] = vaddq_u16(a.val[3], b.val[3]);

// c = a - b
#define vsub(c, a, b)                         \
    c.val[0] = vsubq_u16(a.val[0], b.val[0]); \
    c.val[1] = vsubq_u16(a.val[1], b.val[1]); \
    c.val[2] = vsubq_u16(a.val[2], b.val[2]); \
    c.val[3] = vsubq_u16(a.val[3], b.val[3]);

// c = a * value
#define vmuln(c, a, value)                   \
    c.val[0] = vmulq_n_u16(a.val[0], value); \
    c.val[1] = vmulq_n_u16(a.val[1], value); \
    c.val[2] = vmulq_n_u16(a.val[2], value); \
    c.val[3] = vmulq_n_u16(a.val[3], value);

// c = a ^ b
#define vxor(c, a, b)                         \
    c.val[0] = veorq_u16(a.val[0], b.val[0]); \
    c.val[1] = veorq_u16(a.val[1], b.val[1]); \
    c.val[2] = veorq_u16(a.val[2], b.val[2]); \
    c.val[3] = veorq_u16(a.val[3], b.val[3]);

// c = ~a
#define vnot(c, a)                  \
    c.val[0] = vmvnq_u16(a.val[0]); \
    c.val[1] = vmvnq_u16(a.val[1]); \
    c.val[2] = vmvnq_u16(a.val[2]); \
    c.val[3] = vmvnq_u16(a.val[3]);

// c = a
#define vdup(c, a) c = vdupq_n_u16(a);

// c = c + a_const
#define vadd_const(c, a, b_const)            \
    c.val[0] = vaddq_u16(a.val[0], b_const); \
    c.val[1] = vaddq_u16(a.val[1], b_const); \
    c.val[2] = vaddq_u16(a.val[2], b_const); \
    c.val[3] = vaddq_u16(a.val[3], b_const);

// load c <= a
#define vload_x2(c, a) c = vld1q_u16_x2(a);

// store c <= a
#define vstore_x2(c, a) vst1q_u16_x2(c, a);

// c = a << value
#define vsl_x2(c, a, value)                  \
    c.val[0] = vshlq_n_u16(a.val[0], value); \
    c.val[1] = vshlq_n_u16(a.val[1], value);

// c = a >> value
#define vsr_x2(c, a, value)                  \
    c.val[0] = vshrq_n_u16(a.val[0], value); \
    c.val[1] = vshrq_n_u16(a.val[1], value);

// c = a + b
#define vadd_x2(c, a, b)                      \
    c.val[0] = vaddq_u16(a.val[0], b.val[0]); \
    c.val[1] = vaddq_u16(a.val[1], b.val[1]);

// c = a - b
#define vsub_x2(c, a, b)                      \
    c.val[0] = vsubq_u16(a.val[0], b.val[0]); \
    c.val[1] = vsubq_u16(a.val[1], b.val[1]);

// c = a * value
#define vmuln_x2(c, a, value)                \
    c.val[0] = vmulq_n_u16(a.val[0], value); \
    c.val[1] = vmulq_n_u16(a.val[1], value);

// c = a ^ b
#define vxor_x2(c, a, b)                      \
    c.val[0] = veorq_u16(a.val[0], b.val[0]); \
    c.val[1] = veorq_u16(a.val[1], b.val[1]);

// Evaluate and copy
void karat_neon_evaluate_SB0(uint16_t **restrict w, uint16_t *restrict poly)
{
    uint16_t *c0 = poly,
             *c1 = &poly[SB0],
             *w0_mem = w[0],
             *w1_mem = w[1],
             *w2_mem = w[2];
    uint16x8x4_t r0, r1, r2;
    for (uint16_t addr = 0; addr < SB0; addr += 32)
    {
        vload(r0, &c0[addr]);
        vload(r1, &c1[addr]);
        vstore(&w0_mem[addr], r0);
        vstore(&w2_mem[addr], r1);

        vadd(r2, r0, r1);
        vstore(&w1_mem[addr], r2);
    }
}

// Evaluate and Copy, this go to TMP
// static inline
void karat_neon_evaluate_combine(uint16_t **restrict w, uint16_t *restrict poly)
{
    uint16_t *c0 = poly,
             *c1 = &poly[SB3],
             *c2 = &poly[2 * SB3],
             *c3 = &poly[3 * SB3],
             *w0_mem = w[0],
             *w1_mem = w[1],
             *w2_mem = w[2],
             *w3_mem = w[3],
             *w4_mem = w[4],
             *w5_mem = w[5],
             *w6_mem = w[6],
             *w7_mem = w[7],
             *w8_mem = w[8];

    uint16x8x2_t r0, r1, r2, r3, tmp1, tmp2, tmp3;
    for (uint16_t addr = 0; addr < SB3; addr += 16)
    {
        vload_x2(r0, &c0[addr]);
        vload_x2(r1, &c1[addr]);
        vload_x2(r2, &c2[addr]);
        vload_x2(r3, &c3[addr]);

        vstore_x2(&w0_mem[addr], r0);
        vstore_x2(&w2_mem[addr], r1);
        vstore_x2(&w6_mem[addr], r2);
        vstore_x2(&w8_mem[addr], r3);

        vadd_x2(tmp1, r0, r1);
        vstore_x2(&w1_mem[addr], tmp1);

        vadd_x2(tmp2, r2, r3);
        vstore_x2(&w7_mem[addr], tmp2);

        vadd_x2(tmp1, r0, r2);
        vstore_x2(&w3_mem[addr], tmp1);

        vadd_x2(tmp2, r1, r3);
        vstore_x2(&w5_mem[addr], tmp2);

        vadd_x2(tmp3, tmp1, tmp2);
        vstore_x2(&w4_mem[addr], tmp3);
    }
}

// Interpolate
void karat_neon_interpolate_SB0(uint16_t *restrict poly, uint16_t **restrict w)
{
    uint16x8x4_t r0, r1, r2, tmp;
    uint16_t *w0_mem = w[0],
             *w1_mem = w[1],
             *w2_mem = w[2];
    for (uint16_t i = 0; i < SB0_RES; i += 32)
    {
        vload(r0, &w0_mem[i]);
        vload(r1, &w1_mem[i]);
        vload(r2, &w2_mem[i]);

        vload(tmp, &poly[i]);
        vadd(tmp, r0, tmp);
        vstore(&poly[i], tmp);

        vload(tmp, &poly[2 * SB0 + i]);
        vadd(tmp, r2, tmp);
        vstore(&poly[2 * SB0 + i], tmp);

        vload(tmp, &poly[SB0 + i]);
        vadd(r0, r0, r2);
        vadd(tmp, tmp, r1);
        vsub(tmp, tmp, r0);
        vstore(&poly[1 * SB0 + i], tmp);
    }
}

// Combine Karatsuba Interpolation
// static inline
void karat_neon_interpolate_combine(uint16_t *restrict poly, uint16_t **restrict w)
{
    uint16x8x2_t r0, r1, r2, r3, r4, r5, r6, r7, // 8x2 = 16
        r8, sum0, sum1, sum2,                    // 4x2 = 8
        w01, w20, w21, tmp;                      // 4x2 = 8
    uint16_t *w0_mem = w[0],
             *w1_mem = w[1],
             *w2_mem = w[2],
             *w3_mem = w[3],
             *w4_mem = w[4],
             *w5_mem = w[5],
             *w6_mem = w[6],
             *w7_mem = w[7],
             *w8_mem = w[8];
    for (uint16_t addr = 0; addr < SB3_RES; addr += 16)
    {
        vload_x2(r0, &w0_mem[addr]); // a
        vload_x2(r1, &w1_mem[addr]); // b
        vload_x2(r2, &w2_mem[addr]); // c
        vload_x2(r3, &w3_mem[addr]); // d
        vload_x2(r4, &w4_mem[addr]); // e
        vload_x2(r5, &w5_mem[addr]); // f
        vload_x2(r6, &w6_mem[addr]); // g
        vload_x2(r7, &w7_mem[addr]); // h
        vload_x2(r8, &w8_mem[addr]); // i

        // a + c
        vadd_x2(sum0, r0, r2);
        // sum0 = b - (a + c)
        vsub_x2(sum0, r1, sum0);

        // d + f
        vadd_x2(sum1, r3, r5);
        // sum1 = e - (d + f)
        vsub_x2(sum1, r4, sum1);

        // g + i
        vadd_x2(sum2, r6, r8);
        // sum2 = h - (g + i)
        vsub_x2(sum2, r7, sum2);

        // a + g
        vadd_x2(w01, r0, r6);
        // d - (a + g)
        vsub_x2(w01, r3, w01);

        // w11 = -sum0 + sum1 - sum2
        vadd_x2(tmp, sum0, sum2);
        vsub_x2(sum1, sum1, tmp);

        // w20
        vadd_x2(w20, w01, r2);

        // w21 = g + f - (c + i)
        vadd_x2(tmp, r2, r8);
        vadd_x2(w21, r5, r6);
        vsub_x2(w21, w21, tmp);

        vload_x2(tmp, &poly[addr + 0 * SB3]);
        vadd_x2(r0, tmp, r0);
        vstore_x2(&poly[addr + 0 * SB3], r0);

        vload_x2(tmp, &poly[addr + 1 * SB3]);
        vadd_x2(sum0, tmp, sum0);
        vstore_x2(&poly[addr + 1 * SB3], sum0);

        vload_x2(tmp, &poly[addr + 2 * SB3]);
        vadd_x2(w20, tmp, w20);
        vstore_x2(&poly[addr + 2 * SB3], w20);

        vload_x2(tmp, &poly[addr + 3 * SB3]);
        vadd_x2(sum1, tmp, sum1);
        vstore_x2(&poly[addr + 3 * SB3], sum1);

        vload_x2(tmp, &poly[addr + 4 * SB3]);
        vadd_x2(w21, tmp, w21);
        vstore_x2(&poly[addr + 4 * SB3], w21);

        vload_x2(tmp, &poly[addr + 5 * SB3]);
        vadd_x2(sum2, tmp, sum2);
        vstore_x2(&poly[addr + 5 * SB3], sum2);

        vload_x2(tmp, &poly[addr + 6 * SB3]);
        vadd_x2(r8, tmp, r8);
        vstore_x2(&poly[addr + 6 * SB3], r8);
    }
}

// Ultilize all 32 SIMD registers, no Copy
void tc_evaluate_neon_SB1(uint16_t *restrict w[7], uint16_t *restrict poly)
{
    uint16_t *c0 = poly,
             *c1 = &poly[SB1],
             *c2 = &poly[2 * SB1],
             *c3 = &poly[3 * SB1],
            //  *w0_mem = w[0],
            //  *w6_mem = w[6],
             *w1_mem = w[1],
             *w2_mem = w[2],
             *w3_mem = w[3],
             *w4_mem = w[4],
             *w5_mem = w[5];
    uint16x8x4_t r0, r1, r2, r3, tmp0, tmp1, tmp2, tmp3;
    for (uint16_t addr = 0; addr < SB1; addr += 32)
    {
        vload(r0, &c0[addr]);
        vload(r1, &c1[addr]);
        vload(r2, &c2[addr]);
        vload(r3, &c3[addr]);
        // vstore(&w0_mem[addr], r0); // Direct point when initialized
        // vstore(&w6_mem[addr], r3); // Direct point when initialized

        vadd(tmp0, r0, r2);
        vadd(tmp1, r1, r3);

        vadd(tmp2, tmp0, tmp1);
        vsub(tmp3, tmp0, tmp1);
        vstore(&w1_mem[addr], tmp2);
        vstore(&w2_mem[addr], tmp3);

        vsl(tmp2, r0, 2);
        vadd(tmp2, tmp2, r2);
        vsl(tmp2, tmp2, 1);
        vsl(tmp3, r1, 2);
        vadd(tmp3, tmp3, r3);

        vadd(tmp0, tmp2, tmp3);
        vsub(tmp1, tmp2, tmp3);
        vstore(&w3_mem[addr], tmp0);
        vstore(&w4_mem[addr], tmp1);

        vsl(tmp0, r3, 1);
        vadd(tmp0, tmp0, r2);
        vsl(tmp0, tmp0, 1);
        vadd(tmp0, tmp0, r1);
        vsl(tmp0, tmp0, 1);
        vadd(tmp0, tmp0, r0);
        vstore(&w5_mem[addr], tmp0);
    }
}

// Ultilize all 32 SIMD registers
// void tc_interpolate_neon_sb1(uint16_t poly[512], uint16_t w[7][128])
void tc_interpolate_neon_SB1(uint16_t *restrict poly, uint16_t *restrict w[7])
{
    uint16x8x4_t r0, r1, r2, r3, r4, r5, r6, tmp;
    uint16x8_t one;
    vdup(one, 1);
    uint16_t *w0_mem = w[0],
             *w1_mem = w[1],
             *w2_mem = w[2],
             *w3_mem = w[3],
             *w4_mem = w[4],
             *w5_mem = w[5],
             *w6_mem = w[6];
    for (uint16_t addr = 0; addr < SB1_RES; addr += 32)
    {
        vload(r0, &w0_mem[addr]);
        vload(r1, &w1_mem[addr]);
        vload(r2, &w2_mem[addr]);
        vload(r3, &w3_mem[addr]);
        vload(r4, &w4_mem[addr]);
        vload(r5, &w5_mem[addr]);
        vload(r6, &w6_mem[addr]);

        vadd(r5, r5, r3);
        vadd(r4, r4, r3);
        vsr(r4, r4, 1);
        vadd(r2, r2, r1);
        vsr(r2, r2, 1);
        vsub(r3, r3, r4);
        vsub(r1, r1, r2);
        vsl(tmp, r2, 6);
        vadd(tmp, tmp, r2);
        vsub(r5, r5, tmp);
        vsub(r2, r2, r6);
        vsub(r2, r2, r0);
        vmuln(tmp, r2, 45);
        vadd(r5, tmp, r5);
        vsub(r4, r4, r6);
        vsr(r4, r4, 2);
        vsr(r3, r3, 1);
        vsl(tmp, r3, 2);
        vsub(r5, r5, tmp);
        vsub(r3, r3, r1);
        vmuln(r3, r3, inv3);
        vsl(tmp, r0, 4);
        vsub(r4, r4, tmp);
        vsl(tmp, r2, 2);
        vsub(r4, r4, tmp);
        vmuln(r4, r4, inv3);
        // vmuln(r4, r4, -1); // Avoid multiplication
        vnot(r4, r4);
        vadd_const(r4, r4, one);

        vsub(r2, r2, r4);
        vsr(r5, r5, 1);
        vmuln(r5, r5, inv15);
        vsub(r1, r1, r5);
        vsub(r1, r1, r3);
        vmuln(r1, r1, inv3);
        // vmuln(r1, r1, -1);
        vnot(r1, r1);
        vadd_const(r1, r1, one);

        vsl(tmp, r1, 2);
        vadd(tmp, tmp, r1);
        vsub(r3, r3, tmp);
        vadd(r5, r5, r1);

        vload(tmp, &poly[addr]);
        vadd(r0, tmp, r0);
        vstore(&poly[addr], r0);

        vload(tmp, &poly[SB1 + addr]);
        vadd(r1, tmp, r1);
        vstore(&poly[SB1 + addr], r1);

        vload(tmp, &poly[2 * SB1 + addr]);
        vadd(r2, tmp, r2);
        vstore(&poly[2 * SB1 + addr], r2);

        vload(tmp, &poly[3 * SB1 + addr]);
        vadd(r3, tmp, r3);
        vstore(&poly[3 * SB1 + addr], r3);

        vload(tmp, &poly[4 * SB1 + addr]);
        vadd(r4, tmp, r4);
        vstore(&poly[4 * SB1 + addr], r4);

        vload(tmp, &poly[5 * SB1 + addr]);
        vadd(r5, tmp, r5);
        vstore(&poly[5 * SB1 + addr], r5);

        vload(tmp, &poly[6 * SB1 + addr]);
        vadd(r6, tmp, r6);
        vstore(&poly[6 * SB1 + addr], r6);
    }
}

// void toom_cook_422_combine(uint16_t polyC[512], uint16_t polyA[256], uint16_t polyB[256]) {
void toom_cook_422_combine(uint16_t *restrict polyC, uint16_t *restrict polyA, uint16_t *restrict polyB)
{
    // TC4
    uint16_t *aw[7], *bw[7], *cw[7];
    uint16_t tmp_ab[SB1 * 6], tmp_c[SB1_RES * 7];

    // TC4-2-2 Combine
    uint16_t *aaw[7][9], *bbw[7][9], *ccw[7][9];
    uint16_t tmp_aa[SB3 * 64], tmp_bb[SB3 * 64], tmp_cc[SB3_RES * 64];
    // Done
    uint16_t *tmp_aa_mem = tmp_aa,
             *tmp_bb_mem = tmp_bb,
             *tmp_cc_mem = tmp_cc;

    // TC4
    aw[0] = polyA;
    aw[1] = &polyA[64];
    aw[2] = &polyA[128];
    aw[3] = &tmp_ab[SB1 * 0];
    aw[4] = &tmp_ab[SB1 * 1];
    aw[5] = &tmp_ab[SB1 * 2];
    aw[6] = &polyA[192];

    bw[0] = polyB;
    bw[1] = &polyB[64];
    bw[2] = &polyB[128];
    bw[3] = &tmp_ab[SB1 * 3];
    bw[4] = &tmp_ab[SB1 * 4];
    bw[5] = &tmp_ab[SB1 * 5];
    bw[6] = &polyB[192];

    // DONE TC4

    for (uint16_t i = 0; i < 7; i++)
    {
        // TC4-2-2 Combine
        // Evaluate AA, Copy
        // Size: 64 to 16x9
        aaw[i][0] = &tmp_aa_mem[0 * SB3];
        aaw[i][1] = &tmp_aa_mem[1 * SB3];
        aaw[i][2] = &tmp_aa_mem[2 * SB3];
        aaw[i][3] = &tmp_aa_mem[3 * SB3];
        aaw[i][4] = &tmp_aa_mem[4 * SB3];
        aaw[i][5] = &tmp_aa_mem[5 * SB3];
        aaw[i][6] = &tmp_aa_mem[6 * SB3];
        aaw[i][7] = &tmp_aa_mem[7 * SB3];
        aaw[i][8] = &tmp_aa_mem[8 * SB3];

        // Evaluate BB, Copy
        // Size: 64 to 16x9
        bbw[i][0] = &tmp_bb_mem[0 * SB3];
        bbw[i][1] = &tmp_bb_mem[1 * SB3];
        bbw[i][2] = &tmp_bb_mem[2 * SB3];
        bbw[i][3] = &tmp_bb_mem[3 * SB3];
        bbw[i][4] = &tmp_bb_mem[4 * SB3];
        bbw[i][5] = &tmp_bb_mem[5 * SB3];
        bbw[i][6] = &tmp_bb_mem[6 * SB3];
        bbw[i][7] = &tmp_bb_mem[7 * SB3];
        bbw[i][8] = &tmp_bb_mem[8 * SB3];

        // Result
        // Size:
        ccw[i][0] = &tmp_cc_mem[0 * SB3_RES];
        ccw[i][1] = &tmp_cc_mem[1 * SB3_RES];
        ccw[i][2] = &tmp_cc_mem[2 * SB3_RES];
        ccw[i][3] = &tmp_cc_mem[3 * SB3_RES];
        ccw[i][4] = &tmp_cc_mem[4 * SB3_RES];
        ccw[i][5] = &tmp_cc_mem[5 * SB3_RES];
        ccw[i][6] = &tmp_cc_mem[6 * SB3_RES];
        ccw[i][7] = &tmp_cc_mem[7 * SB3_RES];
        ccw[i][8] = &tmp_cc_mem[8 * SB3_RES];
        // Done TC4-2

        // TC4
        cw[i] = &tmp_c[i * SB1_RES];

        tmp_aa_mem += 9 * SB3;
        tmp_bb_mem += 9 * SB3;
        tmp_cc_mem += 9 * SB3_RES;
    }

    uint16x8x4_t zero;
    vxor(zero, zero, zero);
    for (uint16_t addr = 0; addr < SB1_RES * 7; addr += 32)
    {
        vstore(&tmp_c[addr], zero);
    }

    // Evaluate A, No Copy
    // Size: 256 to 64x7
    tc_evaluate_neon_SB1(aw, polyA);

    // Evaluate B, No Copy
    // Size: 256 to 64x7
    tc_evaluate_neon_SB1(bw, polyB);

    karat_neon_evaluate_combine(aaw[0], aw[0]);
    karat_neon_evaluate_combine(aaw[1], aw[1]);
    karat_neon_evaluate_combine(aaw[2], aw[2]);
    karat_neon_evaluate_combine(aaw[3], aw[3]);
    karat_neon_evaluate_combine(aaw[4], aw[4]);
    karat_neon_evaluate_combine(aaw[5], aw[5]);
    karat_neon_evaluate_combine(aaw[6], aw[6]);

    karat_neon_evaluate_combine(bbw[0], bw[0]);
    karat_neon_evaluate_combine(bbw[1], bw[1]);
    karat_neon_evaluate_combine(bbw[2], bw[2]);
    karat_neon_evaluate_combine(bbw[3], bw[3]);
    karat_neon_evaluate_combine(bbw[4], bw[4]);
    karat_neon_evaluate_combine(bbw[5], bw[5]);
    karat_neon_evaluate_combine(bbw[6], bw[6]);

    // Transpose 8x8x16
    half_transpose_8x16(tmp_aa);
    half_transpose_8x16(tmp_bb);
    // Batch multiplication
    schoolbook_half_8x_neon(tmp_cc, tmp_aa, tmp_bb);
    // Transpose 8x8x32
    half_transpose_8x32(tmp_cc);

    karat_neon_interpolate_combine(cw[0], ccw[0]);
    karat_neon_interpolate_combine(cw[1], ccw[1]);
    karat_neon_interpolate_combine(cw[2], ccw[2]);
    karat_neon_interpolate_combine(cw[3], ccw[3]);
    karat_neon_interpolate_combine(cw[4], ccw[4]);
    karat_neon_interpolate_combine(cw[5], ccw[5]);
    karat_neon_interpolate_combine(cw[6], ccw[6]);

    // for (uint16_t i = 0; i < 7; i++)
    // {
    //     printf("%d, ::::", i);
    //     printArray(cw[i], SB1_RES, "cw[i]");
    // }

    // Interpolate C = A*B = CC
    // Size: 128*7 to 128*4 = 512
    tc_interpolate_neon_SB1(polyC, cw);
}

void poly_neon_reduction(uint16_t *poly, uint16_t *tmp)
{
    uint16x8x4_t res, tmp1, tmp2;
    for (uint16_t addr = 0; addr < NTRU_N_PAD; addr += 32)
    {
        vload(tmp2, &tmp[addr]);
        vload(tmp1, &tmp[addr + NTRU_N_PAD]);
        vadd(res, tmp1, tmp2);
        vstore(&poly[addr], res);
    }
}

/*
uint16_t polyC[1024]
uint16_t polyA[512]
uint16_t polyB[512]
*/

// void poly_mul_neon(uint16_t polyC[512], uint16_t polyA[512], uint16_t polyB[512])
void poly_mul_neon(uint16_t *polyC, uint16_t *polyA, uint16_t *polyB)
{
    uint16_t *kaw[3], *kbw[3], *kcw[3];
    uint16_t tmp_ab[256 * 6];
    uint16_t tmp_c[NTRU_N_PAD * 3];

    kaw[0] = &tmp_ab[0 * 256];
    kaw[1] = &tmp_ab[1 * 256];
    kaw[2] = &tmp_ab[2 * 256];

    kbw[0] = &tmp_ab[3 * 256];
    kbw[1] = &tmp_ab[4 * 256];
    kbw[2] = &tmp_ab[5 * 256];

    kcw[0] = tmp_c;
    kcw[1] = &tmp_c[NTRU_N_PAD];
    kcw[2] = &tmp_c[2 * NTRU_N_PAD];

    uint16x8x4_t zero;
    vxor(zero, zero, zero);
    for (uint16_t addr = 0; addr < NTRU_N_PAD * 3; addr += 32)
    {
        vstore(&tmp_c[addr], zero);
    }

    // Karatsuba Evaluate A
    karat_neon_evaluate_SB0(kaw, polyA);
    // Karatsuba Evaluate B
    karat_neon_evaluate_SB0(kbw, polyB);

    // Toom Cook 4-way combine
    toom_cook_422_combine(kcw[0], kaw[0], kbw[0]);

    // Toom Cook 4-way combine
    toom_cook_422_combine(kcw[1], kaw[1], kbw[1]);

    // Toom Cook 4-way combine
    toom_cook_422_combine(kcw[2], kaw[2], kbw[2]);

    // Karatsuba Interpolate
    // * Re-use tmp_ab
    for (uint16_t addr = 0; addr < NTRU_N_PAD * 2; addr += 32)
    {
        vstore(&tmp_ab[addr], zero);
    }
    karat_neon_interpolate_SB0(tmp_ab, kcw);

    // Ring reduction
    // Reduce from 1024 -> 512
    poly_neon_reduction(polyC, tmp_ab);
}
