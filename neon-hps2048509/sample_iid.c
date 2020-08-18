#include <arm_neon.h>
#include "sample.h"

// load c <= a
#define sp_vload(c, a) c = vld1q_u16_x4(a);

// store c <= a
#define sp_vstore(c, a) vst1q_u16_x4(c, a);

// c = a >> value
#define sp_vsr(c, a, value)                  \
    c.val[0] = vshrq_n_u16(a.val[0], value); \
    c.val[1] = vshrq_n_u16(a.val[1], value); \
    c.val[2] = vshrq_n_u16(a.val[2], value); \
    c.val[3] = vshrq_n_u16(a.val[3], value);

// c = a >> value
#define sp_vsr_sign(c, a, value)             \
    c.val[0] = vshrq_n_s16(a.val[0], value); \
    c.val[1] = vshrq_n_s16(a.val[1], value); \
    c.val[2] = vshrq_n_s16(a.val[2], value); \
    c.val[3] = vshrq_n_s16(a.val[3], value);

// c = a << value
#define sp_vsl(c, a, value)                  \
    c.val[0] = vshlq_n_u16(a.val[0], value); \
    c.val[1] = vshlq_n_u16(a.val[1], value); \
    c.val[2] = vshlq_n_u16(a.val[2], value); \
    c.val[3] = vshlq_n_u16(a.val[3], value);

// c = a & const
#define sp_vand_const(c, a, b)         \
    c.val[0] = vandq_u16(a.val[0], b); \
    c.val[1] = vandq_u16(a.val[1], b); \
    c.val[2] = vandq_u16(a.val[2], b); \
    c.val[3] = vandq_u16(a.val[3], b);

// c = a & b
#define sp_vand_sign(c, a, b)                 \
    c.val[0] = vandq_s16(a.val[0], b.val[0]); \
    c.val[1] = vandq_s16(a.val[1], b.val[1]); \
    c.val[2] = vandq_s16(a.val[2], b.val[2]); \
    c.val[3] = vandq_s16(a.val[3], b.val[3]);

// c = a + b
#define sp_vadd(c, a, b)                      \
    c.val[0] = vaddq_u16(a.val[0], b.val[0]); \
    c.val[1] = vaddq_u16(a.val[1], b.val[1]); \
    c.val[2] = vaddq_u16(a.val[2], b.val[2]); \
    c.val[3] = vaddq_u16(a.val[3], b.val[3]);

// c = a - b
#define sp_vsub_const_sign(c, a, b)    \
    c.val[0] = vsubq_s16(a.val[0], b); \
    c.val[1] = vsubq_s16(a.val[1], b); \
    c.val[2] = vsubq_s16(a.val[2], b); \
    c.val[3] = vsubq_s16(a.val[3], b);

// c = a - const
#define sp_vsub_const(c, a, b)         \
    c.val[0] = vsubq_u16(a.val[0], b); \
    c.val[1] = vsubq_u16(a.val[1], b); \
    c.val[2] = vsubq_u16(a.val[2], b); \
    c.val[3] = vsubq_u16(a.val[3], b);

// c = a ^ b
#define sp_vxor_sign(c, a, b)                 \
    c.val[0] = veorq_s16(a.val[0], b.val[0]); \
    c.val[1] = veorq_s16(a.val[1], b.val[1]); \
    c.val[2] = veorq_s16(a.val[2], b.val[2]); \
    c.val[3] = veorq_s16(a.val[3], b.val[3]);

// c = a ^ b
#define sp_vxor_const(c, a, b)         \
    c.val[0] = veorq_u16(a.val[0], b); \
    c.val[1] = veorq_u16(a.val[1], b); \
    c.val[2] = veorq_u16(a.val[2], b); \
    c.val[3] = veorq_u16(a.val[3], b);

// c = ~a
#define sp_vnot_sign(c, a)          \
    c.val[0] = vmvnq_s16(a.val[0]); \
    c.val[1] = vmvnq_s16(a.val[1]); \
    c.val[2] = vmvnq_s16(a.val[2]); \
    c.val[3] = vmvnq_s16(a.val[3]);

void sample_iid(poly *r, const unsigned char uniformbytes[NTRU_SAMPLE_IID_BYTES])
{
    // 35 SIMD registers
    uint16x8x4_t r0, r1, r2, r3;
    int16x8x4_t t, c, a, b;
    uint16x8_t hex_0x03, hex_0x0f, hex_0xff;
    poly_vdup_x1(hex_0x03, 0x03);
    poly_vdup_x1(hex_0xff, 0xff);
    poly_vdup_x1(hex_0x0f, 0x0f);

    for (uint16_t addr = 0; addr < NTRU_N_PAD; addr += 32)
    {
        sp_vload(r0, &uniformbytes[addr]);

        // r3 = (res >> 8) + (res & 0xff)
        sp_vsr(r1, r3, 8);
        sp_vand_const(r2, r3, hex_0xff);
        sp_vadd(r3, r1, r2);

        // r3 = (r3 >> 4) + (r3 & 0xf)
        sp_vsr(r1, r3, 4);
        sp_vand_const(r2, r3, hex_0x0f);
        sp_vadd(r3, r1, r2);

        // r3 = (r3 >> 2) + (r3 & 0x3)
        sp_vsr(r1, r3, 2);
        sp_vand_const(r2, r3, hex_0x03);
        sp_vadd(r3, r1, r2);

        // r3 = (r3 >> 2) + (r3 & 0x3)
        sp_vsr(r1, r3, 2);
        sp_vand_const(r2, r3, hex_0x03);
        sp_vadd(r3, r1, r2);

        // t = r3 - 3
        sp_vsub_const_sign(t, (int16x8x4_t)r3, (int16x8_t)hex_0x03);
        // c = t >> 15
        sp_vsr_sign(c, t, 15);

        // a = c & t
        sp_vand_sign(a, c, t);
        // b = ~c & t
        sp_vnot_sign(b, c);
        sp_vand_sign(b, b, t);
        // c = a ^ b
        sp_vxor_sign(c, a, b);

        sp_vstore(&r->coeffs[addr], (uint16x8x4_t)c);
    }
    r->coeffs[NTRU_N - 1] = 0;
}