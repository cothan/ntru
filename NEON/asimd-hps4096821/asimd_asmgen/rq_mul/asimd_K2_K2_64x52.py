from asimd_schoolbook_64x13 import schoolbook_64x13 as mul_64x13
from asimd_transpose import transpose_64x16_to_16x52, transpose_16x128_to_128x16
from goto import with_goto

p = print

def vload(dst, address, src):
    p("y{} = vld1q_u16({} + {});".format(dst, address, src))

def vstore(address, dst, src):
    p("vst1q_u16({} + {}, y{});".format(address, dst, src))

def vadd(c, a, b):
    # c =  a + b
    p("y{} = vaddq_u16(y{}, y{});".format(c, a, b))

def vsub(c, a, b):
    # c = a - b
    p("y{} = vsubq_u16(y{}, y{});".format(c, a, b))

def vmul(c, a, b):
    # c = low(a * b)
    p("y{} = vmulq_u16(y{}, y{});".format(c, a, b))

def vmula(d, a, b, c):
    # d = a*b + c
    p("y{} = vmlaq_u16 (y{}, y{}, y{});".format(d, a, b, c))

def vxor(c, a, b):
    # c = a ^ b 
    p("y{} = veorq_u16(y{}, y{});".format(c, a, b))

a_transpose = 0
b_transpose = a_transpose + 52
r_transpose = b_transpose + 52
a_b_summed = r_transpose + 128
a_in_rsp = a_b_summed + 26
b_in_rsp = a_in_rsp + 26
t2_in_rsp = b_in_rsp + 26
coeffs = 52

a_off, b_off, r_off = "--", "--", "--"
a_mem, b_mem, r_mem = "--", "--", "--"
a_real, b_real, r_real = "--", "--", "--"
ecx = 4


def karatsuba_loop(transpose=True):
    global a_off, b_off, r_off
    global a_mem, b_mem, r_mem
    global coeffs
    global a_transpose, b_transpose, r_transpose

    if transpose:
        a_off = a_transpose
        b_off = b_transpose 
        r_off = r_transpose 

        p("r9 = rsp;")
        p("r10 = rsp;")
        a_mem = b_mem = "r9"
        r_mem = "r10"

        transpose_64x16_to_16x52(dst=a_mem, src=a_real, dst_off=a_off)
        transpose_64x16_to_16x52(dst=b_mem, src=b_real, dst_off=b_off)

        coeffs = 64
    else:
        a_off = b_off = r_off = 0
        a_mem = a_real
        b_mem = b_real
        r_mem = r_real

def innerloop(t0, t1, t2):
    global a_off, b_off, r_off
    global a_mem, b_mem, r_mem

    p("// {} {}".format(a_off, b_off))

    mul_64x13(r_mem, a_mem, b_mem, r_off, a_off, b_off)
    mul_64x13(r_mem, a_mem, b_mem, r_off+26, a_off+13, b_off+13)
    mul_64x13('rsp', a_mem, b_mem, a_b_summed, a_off, b_off, additive=True)

    slide = 0
    for j in range(2):
        vload(t0[j], 16*(12+a_b_summed) + slide, "rsp")
        vload(t1[j], 16*(12+r_off) + slide, r_mem)
        vload(t2[j], 16*(38+r_off) + slide, r_mem)

        vsub(t0[j], t0[j], t1[j])
        vsub(t0[j], t0[j], t2[j])

        vstore(16*(25+r_off) + slide, r_mem, t0[j])

        slide = 8

    for i in range(12):
        slide = 0
        for j in range(2):
            vload(t0[j], 16*(13+i+r_off) + slide, r_mem)
            vload(t1[j], 16*(26+i+r_off) + slide, r_mem)
            vsub(t0[j], t0[j], t1[j])

            vload(t1[j], 16*(13+i+a_b_summed) + slide, "rsp")
            vsub(t1[j], t1[j], t0[j])

            vload(t2[j], 16*(39+i+r_off) + slide, r_mem)
            vsub(t1[j], t1[j], t2[j])

            #t2 is free, t0, t1 are busy
            vload(t2[j], 16*(i+r_off) + slide, r_mem)
            vsub(t0[j], t0[j], t2[j])

            # t2 is free, t0, t1 are busy
            vload(t2[j], 16*(i+a_b_summed) + slide, "rsp")
            vadd(t0[j], t0[j], t2[j])
            vstore(16*(13+i+r_off) + slide, r_mem, t0[j])
            vstore(16*(26+i+r_off) + slide, r_mem, t1[j])

            slide = 8

def done(t0, t1, t2):
    global ecx 
    for i in range(26):
        slide = 0
        for j in range(2):
            vload(t0[j], 16*(i+a_off) + slide, a_mem)
            vload(t1[j], 16*(26 + i + a_off) + slide, a_mem)
            vadd(t0[j], t0[j], t1[j])
            vstore(16*(a_in_rsp + i) + slide, "rsp", t0[j])

            vload(t0[j], 16*(i+b_off) + slide, b_mem)
            vload(t1[j], 16*(26 + i + b_off) + slide, b_mem)
            vadd(t0[j], t0[j], t1[j])
            vstore(16*(b_in_rsp + i) + slide, "rsp", t0[j])

            slide = 8

    mul_64x13('rsp', 'rsp', 'rsp', t2_in_rsp, a_in_rsp, b_in_rsp)
    mul_64x13('rsp', 'rsp', 'rsp', t2_in_rsp + 26, a_in_rsp + 13, b_in_rsp + 13)
    mul_64x13('rsp', 'rsp', 'rsp', a_b_summed, a_in_rsp, b_in_rsp, additive=True)

    # [4,....27] : 24 regs
    save = []

    for i in range(12):
        slide = 0
        for j in range(2):
            vload(t0[j], 16*(t2_in_rsp+13+i) + slide, "rsp")
            vload(t1[j], 16*(t2_in_rsp+26+i) + slide, "rsp")
            vsub(t0[j], t0[j], t1[j])

            vload(t1[j], 16*(13+i+a_b_summed) + slide, "rsp")
            vsub(t1[j], t1[j], t0[j])

            vload(t2[j], 16*(t2_in_rsp+39+i) + slide, "rsp")
            if j == 0:
                vsub(4 + i, t1, t2[j])
                save.append(4 + i)
            else:
                vsub(12 + 4 + i, t1, t2[j])
                save.append(16 + 4 + i)
            
            # t2 is free
            vload(t2[j], 16*(t2_in_rsp + i) + slide, "rsp")
            vsub(t0[j], t0[j], t2[j])

            vload(t2[j], 16*(i+a_b_summed) + slide, "rsp")
            vadd(t0[j], t0[j], t2[j])
            vstore(16*(t2_in_rsp+13+i) + slide, "rsp", t0[j])

            slide = 8

    slide = 0
    for j in range(2):
        vload(t0[j], 16*(12+a_b_summed) + slide, "rsp")
        vload(t1[j], 16*(t2_in_rsp + 12) + slide, "rsp")
        vsub(t0[j], t0[j], t1[j])

        vload(t2[j], 16*(t2_in_rsp + 38) + slide, "rsp")
        vsub(t0[j], t0[j], t2[j])

        vload(t1[j], 16*(25+r_off) + slide, r_mem)
        vsub(t0[j], t0[j], t1[j])
        vload(t2[j], 16*(77+r_off) + slide, r_mem)
        vsub(t0[j], t0[j], t2[j])
        vstore(16*(51+r_off) + slide, r_mem, t0[j])

        slide = 8
    
    # use 28 
    for i in range(25):
        slide = 0
        for j in range(2):
            vload(t0[j], 16*(26+i+r_off) + slide, r_mem)
            vload(t1[j], 16*(52+i+r_off) + slide, r_mem)
            vsub(t0[j], t0[j], t1[j])

            if i < 12:
                if j == 0:
                    tt1 = 4 + i
                else:
                    tt1 = 12 + 4 + i
            else:
                tt1 = 28
                vload(t1, 16*(t2_in_rsp+26+i) + slide, "rsp")

            vsub(tt1, tt1, t0[j])

            vload(t1[j], 16*(i+r_off) + slide, r_mem)
            vsub(t0[j], t0[j], t1[j])

            vload(t2[j], 16*(t2_in_rsp+i) + slide, "rsp")
            vadd(t0[j], t0[j], t2[j])
            vstore(16*(26+i+r_off) + slide, r_mem, t0)
            vstore(16*(52+i+r_off) + slide, r_mem, tt1)

            slide = 8
    
    vxor(tt1, tt1, tt1)
    vstore(16*(103+r_off), r_mem, tt1)
    vstore(16*(103+r_off) + 8, r_mem, tt1)

    if transpose:
        transpose_16x128_to_128x16(dst=r_real, src=r_mem, src_off=r_transpose)

    p("{} += {};".format(a_real, 16 * coeffs))
    p("{} += {};".format(b_real, 16 * coeffs))
    p("{} += {};".format(r_real, 2*16 * coeffs))

    ecx -= 1


def K2_K2_transpose_64x52(r_real_in='c', a_real_in='a', b_real_in='b', coeffs_input=52, transpose_input=True, offset=33280):
    global coeffs
    global transpose 
    global r_real, a_real, b_real

    coeffs = coeffs_input
    transpose = transpose_input
    r_real, a_real, b_real = r_real_in, a_real_in, b_real_in

    p("uint16_t *rsp = sharestack + {};".format(offset//2))
    p("uint16_t *r9 = NULL;")
    p("uint16_t *r10 = NULL;")

    t0 = (0, 1)
    t1 = (2, 3)
    t2 = (29, 30)

    p("for (int i = 0; i < 4; i++){")
    p("// karatsuba loop")
    karatsuba_loop(transpose_input)
    p("// innnerloop 1")
    innerloop(t0, t1, t2)
    p("// adjust add")
    
    p("{} += {};".format(a_mem, 16 * 26))
    if a_mem != b_mem:
        p("{} += {};".format(b_mem, 16 * 26))
    p("{} += {};".format(r_mem, 16 * 52))
    
    p("// innnerloop 2")
    innerloop(t0, t1, t2)
    p("// adjust sub")

    p("{} -= {};".format(a_mem, 16 * 26))
    if a_mem != b_mem:
        p("{} -= {};".format(b_mem, 16 * 26))
    p("{} -= {};".format(r_mem, 16 * 52))

    done(t0, t1, t2)
    p("}")

    assert(ecx == 3)



if __name__ == '__main__':
    p("""#include <arm_neon.h>
#include <stdio.h>

void K2_K2_schoolbook_64x52coef(uint16_t *c, uint16_t *a, uint16_t *b, uint16_t *sharestack)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31;
    """)
    K2_K2_transpose_64x52('c', 'a', 'b', transpose_input=True)
    p("{} -= {};".format(r_real, 2 * (2*16 * coeffs*2)))
    p("}")


    
    
