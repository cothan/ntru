from pysnooper import snoop

p = print

def vload(dst, address, src):
    p("y{} = vld1q_u16({} + {});".format(dst, address, src))

def vstore(address, dst, src):
    p("vst1q_u16({} + {}, y{});".format(address, dst, src))

def vadd(c, a, b):
    # c =  a + b
    p("y{} = vaddq_u16(y{}, y{});".format(c, a, b))

def vaddd(c, a, b):
    # c =  a + b
    p("y{} = vaddq_u32(y{}, y{});".format(c, a, b))

def vsub(c, a, b):
    # c = a - b
    p("y{} = vsubq_u16(y{}, y{});".format(c, a, b))

def vsubd(c, a, b):
    # c = a - b
    p("y{} = vsubq_u32(y{}, y{});".format(c, a, b))


def vmul(c, a, b):
    # c = low(a * b)
    p("y{} = vmulq_n_u16(y{}, {});".format(c, a, b))

def vxor(c, a, b):
    # c = a ^ b 
    p("y{} = veorq_u16(y{}, y{});".format(c, a, b))

def vld(dst, address):
    p("y{} = vld1q_u16({});".format(dst, address))

def vconst(dst, value):
    p("y{} = vdupq_n_u16({});".format(dst, value))

def vsl(c, a, b):
    # c = each a shift left by b
    p("y{} = vshlq_n_u16(y{}, {});".format(c, a, b))

def vsld(c, a, b):
    # c = each a shift left by b
    p("y{} = vshlq_n_u32(y{}, {});".format(c, a, b))

def vsr(c, a, b):
    # c = each a shift right by b
    p("y{} = vshrq_n_u16(y{}, {});".format(c, a, b))

def vsrd(c, a, b):
    # c = each a shift right by b
    p("y{} = vshrq_n_u32(y{}, {});".format(c, a, b))

def vand(c, a, b):
    # c = a & b
    p("y{} = vandq_u16(y{}, y{});".format(c, a, b))

def vext(c, a, b, n):
    # extract/rotate 
    # c = (a | b)[n:]
    p("y{} = vextq_u16(y{}, y{}, {});".format(c, a, b, n))


registers = [i for i in range(29, -1, -1)]

def free(*regs):
    for index, x in enumerate(regs):
        if x in registers:
            raise Exception("This register {}:{} is already freed".format(index,x))
        registers.append(x)

def alloc():
    return registers.pop()

def freelist(l):
    for i in l:
        free(i)

def check():
    return len(registers)


def karatsuba_eval(dst, dst_off, coeff, src, t0, t1, slide=0):

    vstore( (dst_off+4*0+coeff)*16 + slide, dst, src[0])
    vstore( (dst_off+4*1+coeff)*16 + slide, dst, src[1])
    vadd(t0, src[0], src[1])

    vstore( (dst_off+4*2+coeff)*16 + slide, dst, t0)
    vstore( (dst_off+4*3+coeff)*16 + slide, dst, src[2])
    vstore( (dst_off+4*4+coeff)*16 + slide, dst, src[3])
    vadd(t0, src[2], src[3])

    vstore( (dst_off+4*5+coeff)*16 + slide, dst, t0)
    vadd(t0, src[2], src[0])

    vstore( (dst_off+4*6+coeff)*16 + slide, dst, t0)
    vadd(t1, src[1], src[3])

    vstore( (dst_off+4*7+coeff)*16 + slide, dst, t1)
    vadd(t0, t1, t0)

    vstore( (dst_off+4*8+coeff)*16 + slide, dst, t0)

# @snoop()
def karatsuba_interpolate(dst, dst_off, src, src_off, coeff, t0, t1, t2):
    def addr(i, off, type=0):
        if type == 0:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16, src)
        else:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16 + 8, src)

    p('// karatsuba_interpolate: {}'.format(check()))
    slide = 0
    for i in range(2):
        r0_52 = alloc()
        vld(r0_52,  addr(0, 52, i))
        out0_52 = r0_52
        vld(t0, addr(1, 0, i))
        vsub(out0_52, r0_52, t0)
        r2_52 = alloc()
        vld(r2_52, addr(2, 52, i))
        out1_0 = r2_52
        vsub(out1_0, r2_52, out0_52)
        vld(t1, addr(1, 52, i))
        vsub(out1_0, out1_0, t1)
        vld(t2, addr(0, 0, i))
        vsub(out0_52, out0_52, t2)
        vld(t0, addr(2, 0, i))
        vadd(out0_52, out0_52, t0)

        
        r3_52 = alloc()
        vld(r3_52, addr(3, 52, i))
        out2_52 = r3_52
        vld(t1, addr(4, 0, i))
        vsub(out2_52, r3_52, t1)
        r5_52 = alloc()
        vld(r5_52, addr(5, 52, i))
        out3_0 = r5_52
        vsub(out3_0, r5_52, out2_52)
        vld(t2, addr(4, 52, i))
        vsub(out3_0, out3_0, t2)
        vld(t0, addr(3, 0))
        vsub(out2_52, out2_52, t0)
        vld(t1, addr(5, 0, i))
        vadd(out2_52, out2_52, t1)

        r6_52 = alloc()
        vld(r6_52, addr(6, 52, i))
        vld(t2, addr(7, 0, i))
        vsub(r6_52, r6_52, t2)
        r8_52 = alloc()
        vld(r8_52, addr(8, 52, i))
        r7_0 = r8_52
        vsub(r7_0, r8_52, r6_52)
        vld(t0, addr(7, 52, i))
        vsub(r7_0, r7_0, t0)
        vld(t1, addr(6, 0, i))
        vsub(r6_52, r6_52, t1)
        vld(t2, addr(8, 0, i))
        vadd(r6_52, r6_52, t2)

        vld(t0, addr(3, 0, i))
        vsub(out1_0, out1_0, t0)
        out2_0 = r7_0
        vsub(out2_0, r7_0, out1_0)
        vsub(out2_0, out2_0, out3_0)
        vld(t1, addr(0, 0, i))
        vsub(out1_0, out1_0, t1)
        vld(t2, addr(6, 0, i))
        vadd(out1_0, out1_0, t2)

        r1_52 = alloc()
        vld(r1_52, addr(1, 52, i))
        out1_52 = alloc()
        vsub(out1_52, r1_52, out2_52)
        r7_52 = out2_52
        vld(r7_52, addr(7, 52, i))
        vsub(out2_52, r7_52, out1_52)
        vld(t0, addr(4, 52, i))
        vsub(out2_52, out2_52, t0)
        vsub(out1_52, out1_52, out0_52)
        vadd(out1_52, out1_52, r6_52)

        out0_0 =  alloc()
        out3_52 = alloc()

        vld(out0_0, addr(0, 0, i))
        vld(out3_52, addr(4, 52, i))

        vstore( (dst_off+2*0+0)*16 + slide, dst, out0_0)
        vstore( (dst_off+2*0+1)*16 + slide, dst, out0_52)
        vstore( (dst_off+2*1+0)*16 + slide, dst, out1_0)
        vstore( (dst_off+2*1+1)*16 + slide, dst, out1_52)
        vstore( (dst_off+2*2+0)*16 + slide, dst, out2_0)
        vstore( (dst_off+2*2+1)*16 + slide, dst, out2_52)
        vstore( (dst_off+2*3+0)*16 + slide, dst, out3_0)
        vstore( (dst_off+2*3+1)*16 + slide, dst, out3_52)

        free(out0_0)
        free(out0_52)
        free(out1_0)
        free(out1_52)
        free(out2_0)
        free(out2_52)
        free(out3_0)
        free(out3_52)
        free(r6_52)
        free(r1_52)

        slide = 8

    p('// karatsuba_interpolate: {}'.format(check()))

    
# karatsuba_interpolate('r', 0, 'a', 0, alloc(), alloc(), alloc())
# t0, t1, t2 = alloc(), alloc(), alloc()
# karatsuba_interpolate('r', 0, 'a', 0, 0, t0, t1, t2)
# free(t0, t1, t2)
# p('// {}'.format(check()))

def idx2off(i):
    """ Produces
    [0, 32, 64, 96,   104, 136, 168, 200,   208, 240, 272, 304,   312, 344, 376, 408]
    These are the byte offsets when dividing into 52-coeff chunks"""
    return (i * 32 - (24 * (i//4)))//2


def poly_Rq_mul(r, a, b):
    p('// poly_Rq_mul: {}'.format(check()))

    p("const uint16_t mask_9_7[8] = {0xffff, 0, 0, 0, 0, 0, 0, 0};")

    p("const uint16_t mask32_to_16[8] = {0xffff, 0, 0xffff, 0, 0xffff, 0, 0xffff, 0};")

    p("const uint16_t mask_7_9[8] = {0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0};")

    r_real, a_real, b_real = r, a, b

    # TODO: modify this
    rsp_size = [(64 * 64 // 16) * 32, (64 * 64 // 16) * 32, (64 * 128 // 16) * 32, 16*32,
    (52 + 52 + 128 + 26 + 26 + 26 + 52) * 32, (7*8 - 16) * 32]
    rsp_size = sum(rsp_size)

    p("uint16_t rsp[{}];".format(rsp_size//2))

    p("uint16_t *rax = rsp + {};".format(0))
    a_prep = "rax"

    p("uint16_t *r11 = rax + {};".format( (64 * 64 // 16) * 16 ))
    b_prep = "r11"

    p("uint16_t *r12 = r11 + {};".format( (64 * 64 // 16) * 32 ))
    r_out = "r12"

    zero = alloc()
    vconst(zero, 0)
    for i in range(832//8):
        vstore(i*8, r_real, zero)

    free(zero)

    
    for (prep, real) in [(a_prep, a_real), (b_prep, b_real)]:
        for coeff in range(4):
            print("// register len {}".format(len(registers)))
            f0 = [alloc(), alloc(), alloc(), alloc()]
            f00 = [alloc(), alloc(), alloc(), alloc()]
            for i in range(len(f0)):
                r = f0[i]
                rr = f00[i]
                vload(r,  0*13*16+idx2off(i*4+coeff), real)
                vload(rr, 0*13*16+idx2off(i*4+coeff) + 8, real)

            f3 = [alloc(), alloc(), alloc(), alloc()]
            f33 = [alloc(), alloc(), alloc(), alloc()]
            for i in range(len(f3)):
                r = f3[i]
                rr = f33[i]
                vload(r,  3*13*16+idx2off(i*4+coeff), real)
                vload(rr, 3*13*16+idx2off(i*4+coeff) + 8, real)

            if coeff == 2:
                mask_9_7 = alloc()
                vload(mask_9_7, 0, "mask_9_7")
                vand(f33[3], f33[3], mask_9_7)
                free(mask_9_7)
            if coeff == 3:
                # replace 
                vxor(f3[3], f3[3], f3[3])
                vxor(f33[3], f33[3], f33[3])

            f1 = [alloc(), alloc(), alloc(), alloc()]
            f11 = [alloc(), alloc(), alloc(), alloc()]
            for i in range(len(f1)):
                r = f1[i]
                rr = f11[i]
                vload(r,  1*13*16+idx2off(i*4+coeff), real)
                vload(rr, 1*13*16+idx2off(i*4+coeff) + 8, real)

            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=0*9*4, src=f0,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=0*9*4, src=f00,t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=6*9*4, src=f3, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=6*9*4, src=f33,t0=t0, t1=t1, coeff=coeff, slide=8)

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
                vload(f2_i,  2*13*16+idx2off(i*4+coeff), real)
                vload(f2_ii, 2*13*16+idx2off(i*4+coeff) + 8, real)

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
            karatsuba_eval(prep, dst_off=1*9*4, src=x1,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=1*9*4, src=x11,t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=2*9*4, src=x2,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=2*9*4, src=x22,t0=t0, t1=t1, coeff=coeff, slide=8)

            free(t0, t1)
            freelist(x1)
            freelist(x11)
            freelist(x2)
            freelist(x22)

            x3 = [alloc(), alloc(), alloc(), alloc()]
            x33 = [alloc(), alloc(), alloc(), alloc()]

            x4 = [alloc(), alloc(), alloc(), alloc()]
            x44 = [alloc(), alloc(), alloc(), alloc()]

            for i in range(4):
                for j in range(2):
                    if j == 0:
                        f2_i = alloc()
                        vload(f2_i, (2*4+i)*16, "rsp")

                        free(f2_i)
                        f2_4_i = alloc()
                        vsl(f2_4_i, f2_i, 2)

                        free(f2_4_i)
                        f0f2_4_i = alloc()
                        t0 = alloc()

                        vload(t0, (0*4+i)*16, "rsp")
                        vadd(f0f2_4_i, f2_4_i, t0)
                        free(t0)

                        f3_4_i = alloc()
                        vsl(f3_4_i, f3[i], 2)
                        free(f3_4_i)

                        f1f3_4_i = alloc()
                        t0 = alloc()

                        vload(t0, (1*4+i)*16, "rsp")
                        vadd(f1f3_4_i, f3_4_i, t0)

                        free(f1f3_4_i)
                        free(t0)
                        f1_2f3_8_i = alloc()

                        vsl(f1_2f3_8_i, f1f3_4_i, 1)
                        vadd(x3[i], f0f2_4_i, f1_2f3_8_i)
                        vsub(x4[i], f0f2_4_i, f1_2f3_8_i)

                        free(f0f2_4_i)
                        free(f1_2f3_8_i)
                    else:
                        f2_ii = alloc()
                        vload(f2_ii, (2*4+i)*16 + 8, "rsp")

                        free(f2_ii)
                        f2_4_ii = alloc()
                        vsl(f2_4_ii, f2_ii, 2)

                        free(f2_4_ii)
                        f0f2_4_ii = alloc()
                        t00 = alloc()
                        vload(t00, (0*4+i)*16 + 8, "rsp")
                        vadd(f0f2_4_ii, f2_4_ii, t00)
                        free(t00)
                        f3_4_ii = alloc()
                        vsl(f3_4_ii, f33[i], 2)
                        free(f3_4_ii)
                        f1f3_4_ii = alloc()
                        t00 = alloc()
                        vload(t00, (1*4+i)*16 + 8, "rsp")
                        vadd(f1f3_4_ii, f3_4_ii, t00)
                        free(f1f3_4_ii)
                        free(t00)
                        f1_2f3_8_ii = alloc()
                        vsl(f1_2f3_8_ii, f1f3_4_ii, 1)
                        vadd(x33[i], f0f2_4_ii, f1_2f3_8_ii)
                        vsub(x44[i], f0f2_4_ii, f1_2f3_8_ii)
                        free(f0f2_4_ii)
                        free(f1_2f3_8_ii)            

            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=3*9*4, src=x3,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=3*9*4, src=x33,t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=4*9*4, src=x4,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=4*9*4, src=x44,t0=t0, t1=t1, coeff=coeff, slide=8)

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
                vmul(f3_3_i, f3[i], 3)
                vmul(f3_3_ii, f33[i], 3)
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
                vmul(f2_3f3_9_i, f2f3_3_i, 3)
                vmul(f2_3f3_9_ii, f2f3_3_ii, 3)
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
                vmul(f1_3f2_9f3_27_i, f1f2_3f3_9_i, 3)
                vmul(f1_3f2_9f3_27_ii, f1f2_3f3_9_ii, 3)
                free(f1_3f2_9f3_27_i, f1_3f2_9f3_27_ii)

                
                vload(t0, (0*4+i)*16, "rsp")
                vadd(x5[i], f1_3f2_9f3_27_i, t0)
                vload(t0, (0*4+i)*16 + 8, "rsp")
                vadd(x55[i], f1_3f2_9f3_27_ii, t0)
                free(t0)

            t0 = alloc()
            t1 = alloc()
            karatsuba_eval(prep, dst_off=5*9*4, src=x5,t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=5*9*4, src=x55,t0=t0, t1=t1, coeff=coeff, slide=8)
            free(t0, t1)
            freelist(x5)
            freelist(x55)
            freelist(f3)
            freelist(f33)

    # Calling external function will clear preset registers 
    p("K2_K2_schoolbook_64x52coef({}, {}, {}, rsp);".format(r_out, a_prep, b_prep))

    print('// remain {}'.format(check()))

    
    mask_mod4096 =  alloc()
    vconst(mask_mod4096, 4095)

    mask32_to_16 = alloc()
    vload(mask32_to_16, 0, "mask32_to_16")


    for coeff in range(4):
        t0, t1, t2 = alloc(), alloc(), alloc()
        for i in range(7):
            karatsuba_interpolate(dst='rsp', dst_off=i*4*2, src=r_out, src_off=i*9*8, coeff=coeff, t0=t0, t1=t1, t2=t2)
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
            vsld(h0_2lo, h0lo, 1)
            vsld(h0_2hi, h0hi, 1)
            
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
            vaddd(t11lo, t1lo, t2lo)
            vaddd(t11hi, t1hi, t2hi)

            free(t11lo, t11hi)
            free(h0_2lo, h0_2hi)
            
            t11c1lo = alloc()
            t11c1hi = alloc()

            vsubd(t11c1lo, t11lo, h0_2lo)
            vsubd(t11c1hi, t11hi, h0_2hi)

            free(t1lo, t1hi)
            free(t2lo, t2hi)

            t12lo = alloc()
            t12hi = alloc()

            vsubd(t12lo, t1lo, t2lo)
            vsubd(t12hi, t1hi, t2hi)

            vsrd(t12lo, t12lo, 1)
            vsrd(t12hi, t12hi, 1)

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
            vsld(h6_2lo, h6lo, 1)
            vsld(h6_2hi, h6hi, 1)

            # free(h6lo, h6hi)
            free(h6_2lo, h6_2hi)
            
            t11c2lo = alloc()
            t11c2hi = alloc()
            vsubd(t11c2lo, t11c1lo, h6_2lo)
            vsubd(t11c2hi, t11c1hi, h6_2hi)

            vsrd(t11c2lo, t11c2lo, 1)
            vsrd(t11c2hi, t11c2hi, 1)

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
            vmul(r22_1, e12s, 43691)
            vmul(r22_2, e12ss, 43691)

            h0_2 = alloc()
            h0_22 = alloc()
            vsl(h0_2, h0lo, 1)
            vsl(h0_22, h0hi, 1)

            free(t13, t133)
            free(h0_2, h0_22)

            t13c1 = alloc()
            t13c11 = alloc() 

            vsub(t13c1, t13, h0_2)
            vsub(t13c11, t133, h0_22)

            h6_128 = alloc()
            h6_1288 = alloc() 
            vsl(h6_128, h6lo, 7)
            vsl(h6_1288, h6hi, 7)
            
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

            vmul(h6_729, h6lo, 729)
            vmul(h6_7299, h6hi, 729)

            free(t5c1, t5c11)
            free(h6_729, h6_7299)

            t5c2 = alloc()
            t5c22 = alloc() 

            vsub(t5c2, t5c1, h6_729)
            vsub(t5c22, t5c11, h6_7299)

            free(e12, e122)

            h4 = alloc()
            h44 = alloc() 

            vmul(h4, e12, 43691)
            vmul(h44, e122, 43691)

            free(r11_1, r11_2)

            h2 = alloc()
            h22 = alloc()

            vsub(h2, r11_1, h4)
            vsub(h22, r11_2, h44)

            h4_9 = alloc()
            h4_99 = alloc()
            vmul(h4_9, h4, 9)
            vmul(h4_99, h44, 9)

            free(h4_9, h4_99)

            h2h4_9 = alloc() 
            h2h4_99 = alloc()

            vadd(h2h4_9, h2, h4_9)
            vadd(h2h4_99, h22, h4_99)

            free(h2h4_9, h2h4_99)

            h2_9h4_81 = alloc()
            h2_9h4_811 = alloc()
            vmul(h2_9h4_81, h2h4_9, 9)
            vmul(h2_9h4_811, h2h4_99, 9)

            free(t5c2, t5c22)
            free(h2_9h4_81, h2_9h4_811)

            t16 = alloc()
            t166 = alloc()

            vsub(t16, t5c2, h2_9h4_81)
            vsub(t166, t5c22, h2_9h4_811)

            free(t16, t166)

            r13 = alloc()
            r133 = alloc()
            vmul(r13, t16, 43691)
            vmul(r133, t166, 43691)

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

            vmul(h5, e23, 52429)
            vmul(h55, e233, 52429)

            free(im1, im11)

            h1 = alloc()
            h11 = alloc() 

            vsub(h1, im1, h5)
            vsub(h11, im11, h55)

            h_lo = [h0lo, h1, h2, h3, h4, h5, h6lo]
            h_hi = [h0hi, h11, h22, h33, h44, h55, h6hi]

            def get_limb(limbreg, i, j, slide=0, off=0):
                vload(limbreg, (off + i*208 + j * 52 + coeff*16) + slide, r_real)

            def store_limb(limbreg, i, j, off=0):
                if coeff == 3:
                    if i == 3 and j >= 4:  # this part exceeds 704
                        return
                    vand(limbreg[0], limbreg[0], mask_mod4096)
                    vand(limbreg[1], limbreg[1], mask_mod4096)
                    vstore(off + i*208 + j * 52 + coeff*16, r_real, limbreg[0])
                    vstore(off + i*208 + j * 52 + coeff*16 + 8, r_real, limbreg[1])

                else:
                    if i == 3 and j >= 4:  # this part exceeds 704
                        return

                    vand(limbreg[0], limbreg[0], mask_mod4096)
                    vand(limbreg[1], limbreg[1], mask_mod4096)
                    vstore(off + i*208 + j * 52 + coeff*16, r_real, limbreg[0])
                    vstore(off + i*208 + j * 52 + coeff*16 + 8, r_real, limbreg[1])
            
            tmp = alloc()
            tmpp = alloc()
            get_limb(tmp, 0, j, slide=0, off=0)
            get_limb(tmpp, 0, j, slide=8, off=0)
            vadd(tmp, h_lo[0], tmp)
            vadd(tmpp, h_hi[0], tmpp)
            store_limb((tmp, tmpp), 0, j, off= 0)

            get_limb(tmp, 1, j, slide=0, off=0)
            get_limb(tmpp, 1, j, slide=8, off=0)
            vadd(tmp, h_lo[1], tmp)
            vadd(tmpp, h_hi[1], tmpp)
            store_limb((tmp, tmpp), 1, j, off=0)

            if i < 7 or (j == 7 and coeff < 2):
                get_limb(tmp, 2, j, slide=0, off=0)
                get_limb(tmpp, 2, j, slide=8, off=0)
                vadd(tmp, h_lo[2], tmp)
                vadd(tmpp, h_hi[2], tmpp)
                store_limb((tmp, tmpp), 2, j, off=0)

            if j == 7 and coeff == 2:
                tmpp2 = alloc()
                mask_9_7 = alloc()
                
                vload(mask_9_7, 0, "mask_9_7")
                get_limb(tmp, 2, j, slide=0, off=0)
                get_limb(tmpp, 2, j, slide=8, off=0)
                vand(tmpp2, h_hi[2], mask_9_7)
                vadd(tmp, h_lo[2], tmp)
                vadd(tmpp, tmpp2, tmpp)

                free(tmpp2)
                free(mask_9_7)

                mask_7_9 = alloc()
                
                vload(mask_7_9, 0, "mask_7_9")
                vext(h_hi[2], h_hi[2], h_hi[2], 1)
                vand(h_hi[2], mask_7_9, h_hi[2])
                get_limb(tmp, 0, 0, slide=0,  off=(0-16*coeff))
                get_limb(tmpp, 0, 0, slide=8, off=(0-16*coeff))
                vadd(tmp, h_hi[2], tmp)
                store_limb((tmp, tmpp), 0, 0, off=(0-16*coeff))
                
                free(mask_7_9)
                
            if j == 7 and coeff == 3:
                get_limb(tmp, 0,  0, slide=0, off=(7-16*coeff))
                get_limb(tmpp, 0, 0, slide=8, off=(7-16*coeff))
                vadd(tmp, h_lo[2], tmp)
                vadd(tmpp, h_hi[2], tmpp)
                store_limb((tmp, tmpp), 0, 0, off=(7-16*coeff))

            if j < 3 or (j == 3 and coeff < 2):
                get_limb(tmp, 3, j, slide=0, off=0)
                get_limb(tmpp, 3, j, slide=8, off=0)
                vadd(tmp, h_lo[3], tmp)
                vadd(tmpp, h_hi[3], tmpp)
                store_limb((tmp, tmpp), 3, j, off=0)

            if j == 3 and coeff == 2:
                tmpp2 = alloc()
                mask_9_7 = alloc()
                
                vload(mask_9_7, 0, "mask_9_7")
                get_limb(tmp, 3, j, slide=0, off=0)
                get_limb(tmpp, 3, j, slide=8, off=0)
                vand(tmpp2, h_hi[3], mask_9_7)
                vadd(tmp, h_lo[3], tmp)
                vadd(tmpp, tmpp2, tmpp)

                free(tmpp2)
                free(mask_9_7)

                mask_7_9 = alloc()

                vload(mask_7_9, 0, "mask_7_9")
                vext(h_hi[3], h_hi[3], h_hi[3], 1)
                vand(h_hi[3], mask_7_9, h_hi[3])
                get_limb(tmp, 0, 0, slide=0,  off=(0-16*coeff))
                get_limb(tmpp, 0, 0, slide=8, off=(0-16*coeff))
                vadd(tmp, h_hi[3], tmp)
                store_limb((tmp, tmpp), 0, 0, off=(0-16*coeff))

                free(mask_7_9)

            if j == 3 and coeff == 3:
                get_limb(tmp, 0, 0, slide=0, off=(7-16*coeff))
                get_limb(tmpp, 0, 0, slide=8, off=(7-16*coeff))
                vadd(tmp, h_lo[3], tmp)
                vadd(tmpp, h_hi[3], tmpp)
                store_limb((tmp, tmpp), 0, 0, off=(7-16*coeff))

            if j >= 4:
                get_limb(tmp, 0,  j-4, slide=0, off=11)
                get_limb(tmpp, 0, j-4, slide=8, off=11)
                vadd(tmp, h_lo[3], tmp)
                vadd(tmpp, h_hi[3], tmpp)
                store_limb((tmp, tmpp), 0, j-4, off=11)

            get_limb(tmp,  0, j, slide=0, off=11)
            get_limb(tmpp, 0, j, slide=8, off=11)
            vadd(tmp, h_lo[4], tmp)
            vadd(tmpp, h_hi[4], tmpp)
            store_limb((tmp, tmpp), 0, j, off=11)

            get_limb(tmp,  1, j, slide=0, off=11)
            get_limb(tmpp, 1, j, slide=8, off=11)
            vadd(tmp, h_lo[5], tmp)
            vadd(tmpp, h_hi[5], tmpp)
            store_limb((tmp, tmpp), 1, j, off=11)

            if j < 7 or (j == 7 and coeff < 2):
                get_limb(tmp,  2, j, slide=0, off=11)
                get_limb(tmpp, 2, j, slide=8, off=11)
                vadd(tmp,  h_lo[6], tmp)
                vadd(tmpp, h_hi[6], tmpp)
                store_limb((tmp, tmpp), 2, j, off=11)

            free(tmp, tmpp)
            freelist(h_lo)
            freelist(h_hi)

    free(mask32_to_16, mask_mod4096)

    p('// poly_Rq_mul: {}'.format(check()))


if __name__ == "__main__":
    p("""#include <arm_neon.h>
#include <stdio.h>
#include "../../../poly.h"

void poly_Rq_mul(poly *c, const poly *a, const poly *b)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29;
    """)
    poly_Rq_mul('c->coeffs', 'a->coeffs', 'b->coeffs')
    p("}\n")
