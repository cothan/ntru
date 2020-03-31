from asimd_K2_K2_64x44 import K2_K2_transpose_64x44
from pysnooper import snoop
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


def vconst(dst, value):
    p("y{} = vdupq_n_u16({});".format(dst, value))


def vand(c, a, b):
    # c = a & b
    p("y{} = vandq_u16(y{}, y{});".format(c, a, b))


def vsl(c, a, b):
    # c = each a shift left by b
    p("y{} = vshlq_u16(y{}, y{});".format(c, a, b))


def vsr(c, a, b):
    # c = each a shift right by b
    p("y{} = vshrq_n_u16(y{}, {});".format(c, a, b))


def vmul(c, a, b):
    # c = low(a * b)
    p("y{} = vmulq_u16(y{}, y{});".format(c, a, b))

def vxor(c, a, b):
    # c = a ^ b 
    p("y{} = veorq_u16(y{}, y{});".format(c, a, b))

def vld(dst, address):
    p("y{} = vld1q_u16({});".format(dst, address))

def karatsuba_eval(dst, dst_off, coeff, src, t0, t1, slide=0):

    vstore((dst_off+3*0+coeff)*16 + slide, dst, src[0])
    vstore((dst_off+3*1+coeff)*16 + slide, dst, src[1])
    vadd(t0, src[0], src[1])

    vstore((dst_off+3*2+coeff)*16 + slide, dst, t0)
    vstore((dst_off+3*3+coeff)*16 + slide, dst, src[2])
    vstore((dst_off+3*4+coeff)*16 + slide, dst, src[3])
    vadd(t0, src[2], src[3])

    vstore((dst_off+3*5+coeff)*16 + slide, dst, t0)
    vadd(t0, src[2], src[0])

    vstore((dst_off+3*6+coeff)*16 + slide, dst, t0)
    vadd(t1, src[1], src[3])

    vstore((dst_off+3*7+coeff)*16 + slide, dst, t1)
    vadd(t0, t1, t0)

    vstore((dst_off+3*8+coeff)*16 + slide, dst, t0)


def karatsuba_interpolate(dst, dst_off, src, src_off, coeff, t0, t1, t2):
    def addr(i, off, type=0):
        if type == 0:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16, src)
        else:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16 + 8, src)


    slide = 0
    for i in range(2):
        r0_44 = 0
        vld(r0_44, addr(0, 44, i))
        out0_44 = r0_44
        vld(t0, addr(1, 0, i))
        vsub(out0_44, r0_44, t0)

        r2_44 = 1
        vld(r2_44, addr(2, 44, i))
        out1_0 = r2_44
        vsub(out1_0, r2_44, out0_44)

        vld(t0, addr(1, 44, i))
        vld(t1, addr(0, 0, i))
        vld(t2, addr(2, 0, i))

        vsub(out1_0, out1_0, t0)
        vsub(out0_44, out0_44, t1)
        vsub(out0_44, out0_44, t2)

        r3_44 = 2
        vld(r3_44, addr(3, 44, i))
        out2_44 = r3_44
        vld(t0, addr(4, 0, i))
        vsub(out2_44, r3_44, t0)

        r5_44 = 3
        vld(r5_44, addr(5, 44, i))
        out3_0 = r5_44
        vsub(out3_0, r5_44, out2_44)

        vld(t0, addr(4, 44, i))
        vld(t1, addr(3, 0, i))
        vld(t2, addr(5, 0, i))

        vsub(out3_0, out3_0, t0)
        vsub(out2_44, out2_44, t1)
        vsub(out2_44, out2_44, t2)

        r6_44 = 4
        vld(r6_44, addr(6, 44, i))
        vld(t0, addr(7, 0, i))
        vsub(r6_44, r6_44, t0)

        r8_44 = 5
        vld(r8_44, addr(8, 44, i))
        r7_0 = r8_44
        vsub(r7_0, r8_44, r6_44)

        vld(t0, addr(7, 44, i))
        vld(t1, addr(6, 0, i))
        vld(t2, addr(8, 0, i))

        vsub(r7_0, r7_0, t0)
        vsub(r6_44, r6_44, t1)
        vsub(r6_44, r6_44, t2)

        vld(t0, addr(3, 0, i))
        vsub(out1_0, out1_0, t0)

        out2_0 = r7_0
        vsub(out2_0, r7_0, out1_0)
        vsub(out2_0, out2_0, out3_0)

        vld(t0, addr(0, 0, i))
        vld(t1, addr(6, 0, i))
        vsub(out1_0, out1_0, t0)
        vadd(out1_0, out1_0, t1)

        r1_44 = 6
        vld(r1_44, addr(1, 44, i))
        out1_44 = 7
        vsub(out1_44, r1_44, out2_44)
        r7_44 = out2_44
        vld(r7_44, addr(7, 44, i))

        vsub(out2_44, r7_44, out1_44)

        vld(t0, addr(4, 44, i))
        vsub(out2_44, out2_44, t0)
        vsub(out1_44, out1_44, out0_44)
        vsub(out1_44, out1_44, r6_44)

        out0_0 = 8
        out3_44 = 9

        vld(out0_0, addr(0, 0, i))
        vld(out3_44, addr(4, 44, i))

        vstore((dst_off+2*0+0)*16 + slide, dst, out0_0)
        vstore((dst_off+2*0+1)*16 + slide, dst, out0_44)
        vstore((dst_off+2*1+0)*16 + slide, dst, out1_0)
        vstore((dst_off+2*1+1)*16 + slide, dst, out1_44)
        vstore((dst_off+2*2+0)*16 + slide, dst, out2_0)
        vstore((dst_off+2*2+1)*16 + slide, dst, out2_44)
        vstore((dst_off+2*3+0)*16 + slide, dst, out3_0)
        vstore((dst_off+2*3+1)*16 + slide, dst, out3_44)

        slide = 8


def idx2off(i):
    return int((i * 32 - (8 * (i//3)))/2)

# @snoop()
def poly_Rq_mul(c, a, b):
    r_real, a_real, b_real = c, a, b

    rsp_size = ((64 * 48 // 16)*2 +(64 * 96 // 16) + 16 + (56 - 16 + 4*8 + 3))*16

    p("uint16_t rsp[{}];".format(rsp_size))

    p("uint16_t *rax = rsp;")
    a_prep = "rax"

    p("uint16_t *r11 = rsp + {};".format((64 * 48 // 16)))
    b_prep = "r11"

    p("uint16_t *r12 = rsp + {};".format(((64 * 48 // 16)*2)))
    r_out = "r12"

    p("uint16_t low9words[8] = {0xffff, 0, 0, 0, 0, 0, 0, 0};")

    p("uint16_t mask32_to_16[8] = {0xffff, 0, 0xffff, 0, 0xffff, 0, 0xffff, 0};")

    p("uint16_t mask_mod8192[8] = {0x1fff,0x1fff,0x1fff,0x1fff,0x1fff,0x1fff,0x1fff,0x1fff};")

    p("uint16_t take6bytes[8] = {0xffff, 0xffff, 0xffff, 0, 0, 0, 0, 0};")

    p("unsigned char shuf48_16[8] = {10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};")

    p("uint16_t mask3_5_3_5[8] = {0xffff, 0xffff, 0xffff, 0, 0, 0, 0, 0};")

    p("uint16_t mask3_5_4_3_1[16] = {0xffff, 0xffff, 0xffff, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xffff, 0xffff, 0xffff, 0};")

    p("uint16_t mask5_3_5_3[16] = {0, 0, 0, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0, 0, 0, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff};")

    registers = list(range(32))

    def free(*regs):
        for index, x in enumerate(regs):
            if x in registers:
                raise Exception("This register {}:{} is already freed".format(index,x))
            registers.append(x)

    def alloc():
        # print('// {:2d}'.format(len(registers)))
        return registers.pop()

    def freelist(l):
        for i in l:
            free(i)

    def check():
        return len(registers)

    # Evaluate Toom4 / K2 / K2
    const_3 = alloc()
    vconst(const_3, 3)

    for (prep, real) in [(a_prep, a_real), (b_prep, b_real)]:
        for coeff in range(3):
            print("// register len {}".format(len(registers)))
            f0 = [alloc(), alloc(), alloc(), alloc()]
            f00 = [alloc(), alloc(), alloc(), alloc()]
            for i in range(len(f0)):
                r = f0[i]
                rr = f00[i]
                vload(r,  0*11*16+idx2off(i*3+coeff), real)
                vload(rr, 0*11*16+idx2off(i*3+coeff) + 8, real)

            f3 = [alloc(), alloc(), alloc(), alloc()]
            f33 = [alloc(), alloc(), alloc(), alloc()]
            for i in range(len(f3)):
                r = f3[i]
                rr = f33[i]
                vload(r,  3*11*16+idx2off(i*3+coeff), real)
                vload(rr, 3*11*16+idx2off(i*3+coeff) + 8, real)

            if coeff == 2:
                # and the high
                mask_low9words = alloc()
                vload(mask_low9words, 0, "low9words")
                vand(f33[3], f33[3], mask_low9words)
                free(mask_low9words)

            f1 = [alloc(), alloc(), alloc(), alloc()]
            f11 = [alloc(), alloc(), alloc(), alloc()]
            for i in range(len(f1)):
                r = f1[i]
                rr = f11[i]
                vload(r,  1*11*16+idx2off(i*3+coeff), real)
                vload(rr, 1*11*16+idx2off(i*3+coeff) + 8, real)

            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=0*9*3, src=f0,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=0*9*3, src=f00,t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=6*9*3, src=f3,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=6*9*3, src=f33,t0=t0, t1=t1, coeff=coeff, slide=8)

            free(t0, t1)

            for i in range(len(f0)):
                r = f0[i]
                rr = f00[i]
                vstore((0*4+i)*16, "rsp", r)
                vstore((0*4+i)*16 + 8, "rsp", rr)
            freelist(f0)
            freelist(f00)
            for i in range(len(f1)):
                r = f1[i]
                rr = f11[i]
                vstore((1*4+i)*16, "rsp", r)
                vstore((1*4+i)*16 + 8, "rsp", rr)
            freelist(f1)
            freelist(f11)

            x1 = [alloc(), alloc(), alloc(), alloc()]
            x11 = [alloc(), alloc(), alloc(), alloc()]

            x2 = [alloc(), alloc(), alloc(), alloc()]
            x22 = [alloc(), alloc(), alloc(), alloc()]

            for i in range(4):
                f2_i = alloc()
                f2_ii = alloc()
                vload(f2_i,  2*11*16+idx2off(i*3+coeff), real)
                vload(f2_ii, 2*11*16+idx2off(i*3+coeff) + 8, real)

                f0f2_i = alloc()
                f0f2_ii = alloc()
                t0 = alloc()
                vload(t0, (0*4+i)*16, "rsp")
                vadd(f0f2_i, f2_i, t0)
                vload(t0, (0*4+i)*16 + 8, "rsp")
                vadd(f0f2_ii, f2_ii, t0)
                free(t0)

                f1f3_i = alloc()
                f1f3_ii = alloc()
                vload(t0,  (1*4+i)*16, "rsp")
                vadd(f1f3_i, f3[i], t0)
                vload(t0, (1*4+i)*16 + 8, "rsp")
                vadd(f1f3_ii, f33[i], t0)

                vadd(x1[i], f0f2_i, f1f3_i)
                vadd(x11[i], f0f2_ii, f1f3_ii)

                vsub(x2[i], f0f2_i, f1f3_i)
                vsub(x22[i], f0f2_ii, f1f3_ii)

                vstore((2*4+i)*16, "rsp", f2_i)
                vstore((2*4+i)*16 + 8, "rsp", f2_ii)

                free(f2_i, f2_ii)
                free(f0f2_i, f0f2_ii)
                free(f1f3_i, f1f3_ii)

            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=1*9*3, src=x1,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=1*9*3, src=x11,t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=2*9*3, src=x2,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=2*9*3, src=x22,t0=t0, t1=t1, coeff=coeff, slide=8)

            free(t0, t1)
            freelist(x1)
            freelist(x11)
            freelist(x2)
            freelist(x22)

            x3 = [alloc(), alloc(), alloc(), alloc()]
            x33 = [alloc(), alloc(), alloc(), alloc()]

            x4 = [alloc(), alloc(), alloc(), alloc()]
            x44 = [alloc(), alloc(), alloc(), alloc()]

            const_2 = alloc()
            vconst(const_2, 2)
            const_1 = alloc()
            vconst(const_1, 1)

            for i in range(4):
                for j in range(2):
                    if j == 0:
                        f2_i = alloc()
                        vload(f2_i, (2*4+i)*16, "rsp")

                        free(f2_i)
                        f2_4_i = alloc()
                        vsl(f2_4_i, f2_i, const_2)

                        free(f2_4_i)
                        f0f2_4_i = alloc()
                        t0 = alloc()

                        vload(t0, (0*4+i)*16, "rsp")
                        vadd(f0f2_4_i, f2_4_i, t0)
                        free(t0)

                        f3_4_i = alloc()
                        vsl(f3_4_i, f3[i], const_2)
                        free(f3_4_i)

                        f1f3_4_i = alloc()
                        t0 = alloc()

                        vload(t0, (1*4+i)*16, "rsp")
                        vadd(f1f3_4_i, f3_4_i, t0)

                        free(f1f3_4_i)
                        free(t0)
                        f1_2f3_8_i = alloc()

                        vsl(f1_2f3_8_i, f1f3_4_i, const_1)
                        vadd(x3[i], f0f2_4_i, f1_2f3_8_i)
                        vsub(x4[i], f0f2_4_i, f1_2f3_8_i)

                        free(f0f2_4_i)
                        free(f1_2f3_8_i)
                    else:
                        f2_ii = alloc()
                        vload(f2_ii, (2*4+i)*16 + 8, "rsp")

                        free(f2_ii)
                        f2_4_ii = alloc()
                        vsl(f2_4_ii, f2_ii, const_2)

                        free(f2_4_ii)
                        f0f2_4_ii = alloc()
                        t00 = alloc()
                        vload(t00, (0*4+i)*16 + 8, "rsp")
                        vadd(f0f2_4_ii, f2_4_ii, t00)
                        free(t00)
                        f3_4_ii = alloc()
                        vsl(f3_4_ii, f33[i], const_2)
                        free(f3_4_ii)
                        f1f3_4_ii = alloc()
                        t00 = alloc()
                        vload(t00, (1*4+i)*16 + 8, "rsp")
                        vadd(f1f3_4_ii, f3_4_ii, t00)
                        free(f1f3_4_ii)
                        free(t00)
                        f1_2f3_8_ii = alloc()
                        vsl(f1_2f3_8_ii, f1f3_4_ii, const_1)
                        vadd(x33[i], f0f2_4_ii, f1_2f3_8_ii)
                        vsub(x44[i], f0f2_4_ii, f1_2f3_8_ii)
                        free(f0f2_4_ii)
                        free(f1_2f3_8_ii)


            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=3*9*3, src=x3,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=3*9*3, src=x33,t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=4*9*3, src=x4,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=4*9*3, src=x44,t0=t0, t1=t1, coeff=coeff, slide=8)

            free(t0, t1)
            freelist(x3)
            freelist(x33)
            freelist(x4)
            freelist(x44)

            x5 = [alloc(), alloc(), alloc(), alloc()]
            x55 = [alloc(), alloc(), alloc(), alloc()]

            for i in range(4):
                f3_3_i = alloc()
                f3_3_ii = alloc()
                vmul(f3_3_i, f3[i], const_3)
                vmul(f3_3_ii, f33[i], const_3)
                free(f3_3_i, f3_3_ii)

                f2f3_3_i = alloc()
                f2f3_3_ii =  alloc()
                t0 = alloc()
                vload(t0, (2*4+i)*16, "rsp")
                vadd(f2f3_3_i, f3_3_i, t0)
                vload(t0, (2*4+i)*16 + 8, "rsp")
                vadd(f2f3_3_ii, f3_3_ii, t0)
                free(t0)
                free(f2f3_3_i, f2f3_3_ii)

                f2_3f3_9_i = alloc()
                f2_3f3_9_ii =  alloc()
                vmul(f2_3f3_9_i, f2f3_3_i, const_3)
                vmul(f2_3f3_9_ii, f2f3_3_ii, const_3)
                free(f2_3f3_9_i, f2_3f3_9_ii)

                f1f2_3f3_9_i = alloc()
                f1f2_3f3_9_ii = alloc()
                t0 = alloc()
                vload(t0, (1*4+i)*16, "rsp")
                vadd(f1f2_3f3_9_i, f2_3f3_9_i, t0)
                vload(t0, (1*4+i)*16 + 8, "rsp")
                vadd(f1f2_3f3_9_ii, f2_3f3_9_ii, t0)
                free(f1f2_3f3_9_i, f1f2_3f3_9_ii)

                f1_3f2_9f3_27_i = alloc()
                f1_3f2_9f3_27_ii =  alloc()
                vmul(f1_3f2_9f3_27_i, f1f2_3f3_9_i, const_3)
                vmul(f1_3f2_9f3_27_ii, f1f2_3f3_9_ii, const_3)
                free(f1_3f2_9f3_27_i, f1_3f2_9f3_27_ii)

                
                vload(t0, (0*4+i)*16, "rsp")
                vadd(x5[i], f1_3f2_9f3_27_i, t0)
                vload(t0, (0*4+i)*16 + 8, "rsp")
                vadd(x55[i], f1_3f2_9f3_27_ii, t0)
                free(t0)

            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=5*9*3, src=x5,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=5*9*3, src=x55,t0=t0, t1=t1, coeff=coeff, slide=8)
            free(t0, t1)
            freelist(x5)
            freelist(x55)
            freelist(f3)
            freelist(f33)
            free(const_1, const_2)
    
    # Calling external function will clear preset registers 
    p("K2_K2_transpose_64x44({}, {}, {});".format(r_out, a_prep, b_prep))

    compose_offset = 56
    far_spill_offset = compose_offset + 4*8
    vxor(0, 0, 0)

    for i in range(4*8):
        slide = 0 
        for j in range(2):
            vstore((compose_offset+i)*32 + slide, "rsp", 0)
            slide = 8

    print('// remain {}'.format(check()))

    vconst(const_3, 3)

    const729 = alloc()
    vconst(const729, 729)

    const3_inv = alloc() 
    vconst(const3_inv, 43691)

    const5_inv = alloc()
    vconst(const5_inv, 52429)

    const9 = alloc()
    vconst(const9, 9)

    mask32_to_16 = alloc()
    vload(mask32_to_16, 0, "mask32_to_16")

    const_7 = alloc() 
    vconst(const_7, 7)

    mask_mod8192 = alloc()
    vconst(mask_mod8192, 8191)

    take6bytes = alloc() 
    vload(take6bytes, 0, "take6bytes")

    shuf48_16 = alloc()
    vload(shuf48_16, 0, "shuf48_16")

    mask3_5_3_5 = alloc()
    vload(mask3_5_3_5, 0, "mask3_5_3_5")

    mask5_3_5_3 = alloc()
    mask5_3_5_3_hi = alloc()
    vload(mask5_3_5_3, 0, "mask5_3_5_3")
    vload(mask5_3_5_3_hi, 8, "mask5_3_5_3")

    mask = [mask3_5_3_5, alloc(), alloc()]
    vload(mask[1], 0, "mask3_5_4_3_1")
    vload(mask[2], 8, "mask3_5_4_3_1")

    for coeff in range(3):
        print('// 557: {}'.format(check()))
        t0, t1, t2 = alloc(), alloc(), alloc()
        for i in range(7):
            karatsuba_interpolate(dst='rsp', dst_off=i*4*2, src=r_out, src_off=i*9*6, coeff=coeff, t0=t0, t1=t1, t2=t2)
        free(t0, t1, t2)

        for j in range(8):
            def limb(i, slide=0):
                return '{} + rsp'.format((i*8+j)*16 + slide)

            p("// {} 576: {}".format(j, check()))
            h0lo = alloc()
            h0hi = alloc()

            vld(h0lo, limb(0))
            vld(h0hi, limb(0, 8))

            h0_2lo = alloc()
            h0_2hi = alloc()
            vsl(h0_2lo, h0lo, const_1)
            vsl(h0_2hi, h0hi, const_1)
            
            # Use later
            # free(h0lo, h0hi)

            t1lo = alloc()
            t1hi = alloc()

            vld(t1lo, limb(1))
            vld(t1hi, limb(1, 8))

            t2lo = alloc()
            t2hi = alloc()

            t11lo = alloc()
            t11hi = alloc()
            vadd(t11lo, t1lo, t2lo)
            vadd(t11hi, t1hi, t2hi)

            free(t11lo, t11hi)
            free(h0_2lo, h0_2hi)
            
            t11c1lo = alloc()
            t11c1hi = alloc()

            vsub(t11c1lo, t11lo, h0_2lo)
            vsub(t11c1hi, t11hi, h0_2hi)

            free(t1lo, t1hi)
            free(t2lo, t2hi)

            t12lo = alloc()
            t12hi = alloc()

            vsub(t12lo, t1lo, t2lo)
            vsub(t12hi, t1hi, t2hi)

            vsr(t12lo, t12lo, 1)
            vsr(t12hi, t12hi, 1)

            vand(t12lo, t12lo, mask32_to_16)
            vand(t12hi, t12hi, mask32_to_16)

            free(t12lo, t12hi)

            r11s = alloc() 
            r11ss = alloc()

            p("y{} = vzip1q_u16(y{}, y{});".format(r11s, t12lo, t12hi))
            p("y{} = vzip2q_u16(y{}, y{});".format(r11ss, t12lo, t12hi))

            h6lo = alloc()
            h6hi = alloc()

            vld(h6lo, limb(6))
            vld(h6hi, limb(6, 8))

            h6_2lo = alloc()
            h6_2hi = alloc() 
            vsl(h6_2lo, h6lo, const_1)
            vsl(h6_2hi, h6hi, const_1)

            # free(h6lo, h6hi)
            free(h6_2lo, h6_2hi)
            
            t11c2lo = alloc()
            t11c2hi = alloc()
            vsub(t11c2lo, t11c1lo, h6_2lo)
            vsub(t11c2hi, t11c1hi, h6_2hi)

            vsr(t11c2lo, t11c2lo, 1)
            vsr(t11c2hi, t11c2hi, 1)

            free(t11c1lo, t11c1hi)

            r11_1 = alloc()
            r11_2 = alloc() 

            p("y{} = vzip1q_u16(y{}, y{});".format(r11_1, t11c2lo, t11c2hi))
            p("y{} = vzip2q_u16(y{}, y{});".format(r11_2, t11c2lo, t11c2hi))

            free(t11c2lo, t11c2hi)       

            t3 = alloc()
            t33 = alloc() 

            vld(t3, limb(3))
            vld(t33, limb(3, 8))

            t13 = alloc()
            t133 = alloc()

            l4 = alloc()
            l44 = alloc()
            vld(l4, limb(4))
            vld(l44, limb(4, 8))

            vadd(t13, t3, l4)
            vadd(t133, t33, l44)

            
            t14 = alloc()
            t144 = alloc() 
            vsub(t14, t3, l4)
            vsub(t144, t33, l44)

            free(t3, t33)
            free(l4, l44)
            free(t14, t144)

            r12s = alloc()
            r12ss = alloc() 
            
            vsr(r12s, t14,   2)
            vsr(r12ss, t144, 2)

            e12s = alloc()
            e12ss = alloc()

            vsub(e12s, r12s, r11s)
            vsub(e12ss, r12ss, r11ss)

            free(r12s, r12ss)
            free(e12s, e12ss)
            
            r22_1 = alloc()
            r22_2 = alloc()
            vmul(r22_1, e12s, const3_inv)
            vmul(r22_2, e12ss, const3_inv)

            h0_2 = alloc()
            h0_22 = alloc()
            vsl(h0_2, h0lo, const_1)
            vsl(h0_22, h0hi, const_1)

            free(t13, t133)
            free(h0_2, h0_22)

            t13c1 = alloc()
            t13c11 = alloc() 

            vsub(t13c1, t13, h0_2)
            vsub(t13c11, t133, h0_22)

            h6_128 = alloc()
            h6_1288 = alloc() 
            vsl(h6_128, h6lo, const_7)
            vsl(h6_1288, h6hi, const_7)
            
            free(t13c1, t13c11)
            free(h6_128, h6_1288)

            t13c2 = alloc() 
            t13c22 = alloc() 

            vsub(t13c2, t13c1, h6_128)
            vsub(t13c22, t13c11, h6_1288)

            free(t13c2, t13c22)

            r12 = alloc() 
            r122 = alloc() 
            vsr(r12, t13c2,   3)
            vsr(r122, t13c22, 3)

            free(r12, r122)

            e12 = alloc() 
            e122 = alloc()
            vsub(e12, r12, r11_1)
            vsub(e122, r122, r11_2)

            t5 = alloc()
            t55 = alloc()

            vld(t5, limb(5))
            vld(t55, limb(5, 8))

            free(t5, t55)
            t5c1 = alloc() 
            t5c11 = alloc()
            vsub(t5c1, t5, h0lo)
            vsub(t5c11, t55, h0hi)

            h6_729 = alloc()
            h6_7299 = alloc()

            vmul(h6_729, h6lo, const729)
            vmul(h6_7299, h6hi, const729)

            free(t5c1, t5c11)
            free(h6_729, h6_7299)

            t5c2 = alloc()
            t5c22 = alloc() 

            vsub(t5c2, t5c1, h6_729)
            vsub(t5c22, t5c11, h6_7299)

            free(e12, e122)

            h4 = alloc()
            h44 = alloc() 

            vmul(h4, e12, const3_inv)
            vmul(h44, e122, const3_inv)

            free(r11_1, r11_2)

            h2 = alloc()
            h22 = alloc()

            vsub(h2, r11_1, h4)
            vsub(h22, r11_2, h44)

            h4_9 = alloc()
            h4_99 = alloc()
            vmul(h4_9, h4, const9)
            vmul(h4_99, h44, const9)

            free(h4_9, h4_99)

            h2h4_9 = alloc() 
            h2h4_99 = alloc()

            vadd(h2h4_9, h2, h4_9)
            vadd(h2h4_99, h22, h4_99)

            free(h2h4_9, h2h4_99)

            h2_9h4_81 = alloc()
            h2_9h4_811 = alloc()
            vmul(h2_9h4_81, h2h4_9, const9)
            vmul(h2_9h4_811, h2h4_99, const9)

            free(t5c2, t5c22)
            free(h2_9h4_81, h2_9h4_811)

            t16 = alloc()
            t166 = alloc()

            vsub(t16, t5c2, h2_9h4_81)
            vsub(t166, t5c22, h2_9h4_811)

            free(t16, t166)

            r13 = alloc()
            r133 = alloc()
            vmul(r13, t16, const3_inv)
            vmul(r133, t166, const3_inv)

            free(r13, r133)

            e13 = alloc()
            e133 = alloc() 

            vsub(e13, r13, r11s)
            vsub(e133, r133, r11ss)

            free(e13, e133)

            r23 = alloc()
            r233 = alloc() 

            vsr(r23, e13,  3)
            vsr(r233, e13, 3)

            free(r23, r233)

            e23 = alloc() 
            e233 = alloc() 

            vsub(e23, r23, r22_1)
            vsub(e233, r233, r22_2)

            free(r22_1, r22_2)

            h3 = alloc() 
            h33 = alloc()

            vsub(h3, r22_1, e23)
            vsub(h33, r22_2, e233)

            free(r11s, r11ss)

            im1 =  alloc() 
            im11 = alloc() 
            vsub(im1, r11s, h3)
            vsub(im11, r11ss, h33)

            free(e23, e233)

            h5 = alloc() 
            h55 = alloc() 

            vmul(h5, e23, const5_inv)
            vmul(h55, e233, const5_inv)

            free(im1, im11)

            h1 = alloc()
            h11 = alloc() 

            vsub(h1, im1, h5)
            vsub(h11, im11, h55)

            h_lo = [h0lo, h1, h2, h3, h4, h5, h6lo]
            h_hi = [h0hi, h11, h22, h33, h44, h55, h6hi]

            def get_limb(limbreg, i, j, slide=0):
                vload(limbreg, (i*176 + j * 44 + coeff*16) + slide, r_real)

            def store_limb(limbreg, i, j):
                if coeff == 2:
                    if i == 3 and j >= 4:  # this part exceeds 704
                        return
                    vand(limbreg[0], limbreg[0], mask_mod8192)
                    vand(limbreg[1], limbreg[1], mask_mod8192)
                    vstore(i*176 + j * 44 + coeff*16, r_real, limbreg[0])
                    vstore(i*176 + j * 44 + coeff*16 + 8, r_real, limbreg[1])

                    if j == 3: 
                        # TODO: find a way to work this out
                        p("y{} = y{} >> 16;".format(limbreg[0], limbreg[0]))
                        vand(limbreg[0], limbreg[0], take6bytes)
                        vstore((compose_offset+0*8+j-(3-i))*16, "rsp", limbreg[0])

                else:
                    if i == 3 and j >= 4:  # this part exceeds 704
                        return

                    vand(limbreg[0], limbreg[0], mask_mod8192)
                    vand(limbreg[1], limbreg[1], mask_mod8192)
                    vstore(i*176 + j * 44 + coeff*16, r_real, limbreg[0])
                    vstore(i*176 + j * 44 + coeff*16 + 8, r_real, limbreg[1])

            if j == 7 and coeff == 2:
                for i in [2,3,4]:
                    tmp = alloc()
                    # TODO: find a way to work this out
                    p("y{} = y{} >> 16;".format(tmp, h_hi[i]))
                    vand(tmp, tmp, take6bytes)
                    vstore((far_spill_offset+i-2)*16, "rsp", tmp)
                    free(tmp)
            
            if j >= 4:
                p("// 930: {}".format(check()))    
                for ml in range(2):
                    if ml == 0:
                        h0_old = alloc()
                        h1_old = alloc()
                        h2_old = alloc()
                        get_limb(h0_old, 0, j)
                        get_limb(h1_old,  1, j)
                        get_limb(h2_old,  2, j)
                        vand(h_lo[0], h0_old, h_lo[0])
                        vand(h_lo[1], h1_old, h_lo[1])
                        vand(h_lo[2], h2_old, h_lo[2])
                        free(h0_old, h1_old, h2_old)
                    else: 
                        h0_oldd = alloc()
                        h1_oldd = alloc()
                        h2_oldd = alloc()
                        get_limb(h0_oldd, 0, j, slide=8)
                        get_limb(h1_oldd, 1, j, slide=8)
                        get_limb(h2_oldd, 2, j, slide=8)
                        vand(h_hi[0], h0_oldd, h_hi[0])
                        vand(h_hi[1], h1_oldd, h_hi[1])
                        vand(h_hi[2], h2_oldd, h_hi[2])
                        free(h0_oldd, h1_oldd, h2_oldd)
                p("// 950: {}".format(check()))    

            p("// 941: {}".format(check()))    
            if j < 8:
                # mask = [mask3_5_3_5, alloc(), alloc()]
                # vload(mask[1], 0, "mask3_5_4_3_1")
                # vload(mask[2], 8, "mask3_5_4_3_1")
                # mask5_3_5_3 = alloc()
                # mask5_3_5_3_hi = alloc()

                # vload(mask5_3_5_3, 0, "mask5_3_5_3")
                # vload(mask5_3_5_3_hi, 8, "mask5_3_5_3")
                for i in range(-1, 3):
                    p("// 960: {}".format(check()))
                    if j < 4 and i == -1:
                        continue
                    temp = alloc()
                    tempp = alloc()

                    p("y{} = vqtbl1q_u8(y{}, y{});".format(h_lo[i+4], h_lo[i+4], shuf48_16))
                    p("y{} = vqtbl1q_u8(y{}, y{});".format(h_hi[i+4], h_hi[i+4], shuf48_16))

                    if coeff < 2: 
                        # mask = [alloc()]*2
                        # vload(mask[0], 0, "mask3_5_3_5")
                        permutation = 1
                    elif coeff == 2:
                        # mask = [alloc(), alloc()]
                        permutation = 2

                    
                    if coeff < 2:
                        vand(temp, h_lo[i+4], mask[0])
                        vand(tempp, h_hi[i+4], mask[0])
                    elif coeff == 2:
                        vand(temp, h_lo[i+4], mask[1])
                        vand(tempp, h_hi[i+4], mask[2])
                    
                    vand(h_lo[i+4], h_lo[i+4], mask5_3_5_3)
                    vand(h_hi[i+4], h_hi[i+4], mask5_3_5_3_hi)

                    # TODO line 677
                    if permutation == 1:
                        # a4 | a1 = (a2 | a1) | (a4 | a3), 1
                        p("y{} = vextq_u64(y{}, y{}, {});".format(temp, tempp, temp, 1))
                        temp, tempp = tempp, temp
                    elif permutation == 2:
                        # a1 | a2 = (a2 | a1) | (a2 | a1), 1 
                        p("y{} = vextq_u64(y{}, y{}, {});".format(temp, temp, temp, 1))
                        # a3 | a1 = (a4 | a3) | (a1 | a2), 1
                        p("y{} = vextq_u64(y{}, y{}, {});".format(temp, temp, tempp, 1))
                        # a3 | a4 = (a4 | a3) | (a4 | a3)
                        p("y{} = vextq_u64(y{}, y{}, {});".format(tempp, tempp, tempp, 1))
                        # swap 
                        temp, tempp = tempp, temp

                    # only keep high bits
                    temp2 = tempp 
                    p("y{} = vorrq_u16(y{}, y{});".format(h_hi[i+4], temp2, h_hi[i+4]))
                    free(temp, tempp)

                    if i == -1:
                        dst = alloc()
                        dstt = alloc() 
                        get_limb(dst, 0, j-4)
                        get_limb(dstt, 0, j-4, slide=8)
                    else:
                        dst = h_lo[i] 
                        dstt = h_hi[i]
                    
                    if coeff > 0:
                        ltmp = alloc()
                        vload(ltmp, (compose_offset+(i+1)*8+j)*16, "rsp")
                        vadd(dst, dst, ltmp)
                        vload(ltmp, (compose_offset+(i+1)*8+j)*16 + 8, "rsp")
                        vadd(dst, dst, ltmp)
                        free(ltmp)
                    if i == -1:
                        store_limb((dst, dstt), 0, j -4)
                        free(dst, dstt)

                    vstore((compose_offset+(i+1)*8+j)*16, "rsp", temp)
            
                # freelist(mask[1:])
                # free(mask5_3_5_3, mask5_3_5_3_hi)

            for i in range(4):
                store_limb((h_lo[i],h_hi[i]), i, j)
                
            
            free(h0lo, h1, h2, h3, h4, h5, h6lo)
            free(h0hi, h11, h22, h33, h44, h55, h6hi)

    p("// remain 1031: {}".format(check()))
    coeff = 0
    for j in range(8):
        for i in range(3):
            htemp = alloc()
            htempp = alloc()
            get_limb(htemp, i, j)
            get_limb(htempp, i, j, slide=8)
            if not (i == 0 and j == 0):
                ltmp = alloc()
                vload(ltmp, (compose_offset+(i+1)*8+((j-1) % 8))*16, "rsp")
                vadd(htemp, htemp, ltmp)
                vload(ltmp, (compose_offset+(i+1)*8+((j-1) % 8))*16 + 8, "rsp")
                vadd(htempp, htempp, ltmp)
                free(ltmp)
            if i == 0 and 4<=j + 4 < 8:
                ltmp = alloc()
                vload(ltmp, (compose_offset+0*8+((j+4-1) % 8))*16, "rsp")
                vadd(htemp, htemp, ltmp)
                vload(ltmp, (compose_offset+0*8+((j+4-1) % 8))*16 + 8, "rsp")
                vadd(htempp, htempp, ltmp)
                free(ltmp)
            if j == 0 and i in [0, 1, 2]:
                ltmp = alloc()
                vload(ltmp, (far_spill_offset+i)*16, "rsp")
                vadd(htemp, htemp, ltmp)
                vload(ltmp, (far_spill_offset+i)*16 + 8, "rsp")
                vadd(htempp, htempp, ltmp)
                free(ltmp)
            vand(htemp, mask_mod8192, htemp)
            vand(htempp, mask_mod8192, htempp)
            vstore((i*176 + j * 44 + coeff*16) * 2, r_real, htemp)
            vstore((i*176 + j * 44 + coeff*16) * 2 + 8, r_real, htempp)
            free(htemp, htempp)

if __name__ == "__main__":
    p("""#include <arm_neon.h>
#include <stdio.h>
#include "../../../poly.h"

void poly_Rq_mul(poly *c, poly *a, poly *b)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31;
    """)
    poly_Rq_mul('c->coeffs', 'a->coeffs', 'b->coeffs')
    p("}\n")
    