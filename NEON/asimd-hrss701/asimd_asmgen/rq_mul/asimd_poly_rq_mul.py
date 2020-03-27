from asimd_K2_K2_64x44 import K2_K2_transpose_64x44

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
    p("y{} = vdupq_n_u16({})".format(dst, value))

def vand(c, a, b):
    # c = a & b 
    p("y{} = vandq_u16({}, {});".format(c, a, b))

def vsl(c, a, b):
    # c = each a shift left by b 
    p("y{} = vshlq_s16(y{}, y{});".format(c, a, b))

def vsr(c, a, b):
    # c = each a shift right by b
    p("y{} = vshrq_n_u16(y{}, y{});".format(c, a, b))

def vmul(c, a, b):
    # c = low(a * b)
    p("y{} = vmulq_u16(y{}, y{});".format(c, a, b))


def karatsuba_eval(dst, dst_off, coeff, src, t0, t1, slide=0):

    vstore((dst_off+3*0+coeff)*16 + slide, dst, src[0] )
    vstore((dst_off+3*1+coeff)*16 + slide, dst, src[1] )
    vadd(t0, src[0], src[1] )
    
    vstore((dst_off+3*2+coeff)*16 + slide, dst, t0 )
    vstore((dst_off+3*3+coeff)*16 + slide, dst, src[2] )
    vstore((dst_off+3*4+coeff)*16 + slide, dst, src[3] )
    vadd(t0, src[2], src[3] )
    
    vstore((dst_off+3*5+coeff)*16 + slide, dst, t0 )
    vadd(t0, src[2], src[0] )
    
    vstore((dst_off+3*6+coeff)*16 + slide, dst, t0)
    vadd(t1, src[1], src[3])
    
    vstore((dst_off+3*7+coeff)*16 + slide, dst, t1)
    vadd(t0, t1, t0 )
    
    vstore((dst_off+3*8+coeff)*16 + slide, dst, t0)

def karatsuba_interpolate(dst, dst_off, src, src_off, coeff, t0, t1, t2):
    def addr(i, off, type=0):
        if type == 0:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16, src)
        else:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16 + 8, src)

    def vld(dst, address):
        p("y{} = vld1q_u16({});".format(dst, address))


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
        
        vld(t0 , add(1, 44, i))
        vld(t1 , add(0, 0, i) )
        vld(t2 , add(2, 0, i) )

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

        vld(t0 , add(4, 44, i))
        vld(t1 , add(3, 0, i) )
        vld(t2 , add(5, 0, i) )

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

        vstore( (dst_off+2*0+0)*16 + slide, dst, out0_0 )
        vstore( (dst_off+2*0+1)*16 + slide, dst, out0_44 )
        vstore( (dst_off+2*1+0)*16 + slide, dst, out1_0 )
        vstore( (dst_off+2*1+1)*16 + slide, dst, out1_44 )
        vstore( (dst_off+2*2+0)*16 + slide, dst, out2_0 )
        vstore( (dst_off+2*2+1)*16 + slide, dst, out2_44 )
        vstore( (dst_off+2*3+0)*16 + slide, dst, out3_0 )
        vstore( (dst_off+2*3+1)*16 + slide, dst, out3_44 )

        slide = 8 

def idx2off(i):
    return (i * 32 - (8 * (i//3)))/2


def poly_Rq_mul(c, a, b):
    r_real, a_real, b_real = c, a, b

    p("uint16_t rsp[{}];".format( ((64 * 48 // 16)*2 + (64 * 96 // 16))*16 + 16*16 ))

    # p("int *r12, *rax, *r11;")


    p("uint16_t *rax = rsp;")
    a_prep = "rax"

    p("uint16_t *r11 = rsp + {};".format((64 * 48 // 16)))
    b_prep = "r11"

    p("uint16_t *r12 = rsp + {};".format(((64 * 48 // 16)*2)))
    r_out = "r12"

    p("uint16_t low9words[8] = {0xffff, 0, 0, 0, 0, 0, 0, 0};")

    # Evaluate Toom4 / K2 / K2 
    const_3 = 3
    vconst(const_3, 3)
    mask_low9words = 31
    vload(31, 0, "low9words")

    for (prep, real) in [(a_prep, a_real), (b_prep, b_real)]:
        for coeff in range(3):
            f0 = [0, 1, 2, 12]
            f00 = [16, 17, 18, 28]
            assert (f0 == f00)
            for i in range(len(f0)):
                r = f0[i]
                rr = f00[i]
                vload(r,  0*11*16+idx2off(i*3+coeff), real)
                vload(rr, 0*11*16+idx2off(i*3+coeff) + 8, real)

            f3 = [4, 5, 6, 7]
            f33 = [20, 21, 22, 23]
            for i in range(len(f3)):
                r = f3[i]
                rr = f33[i]
                vload(r,  3*11*16+idx2off(i*3+coeff), real)
                vload(rr, 3*11*16+idx2off(i*3+coeff) + 8, real)
            
            if coeff == 2:
                # and the high 
                vand(f33[3], f33[3], mask_low9words)
            
            f1 = [8, 9, 10, 11]
            f11 = [24, 25, 26, 27]
            for i in range(len(f1)):
                r = f1[i]
                rr = f11[i]
                vload(r,  1*11*16+idx2off(i*3+coeff), real)
                vload(rr, 1*11*16+idx2off(i*3+coeff) + 8, real)

            t0 = 14 
            t1 = 15
            karatsuba_eval(prep, dst_off=0*9*3, src=f0, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=0*9*3, src=f00, t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=6*9*3, src=f3, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=6*9*3, src=f33, t0=t0, t1=t1, coeff=coeff, slide=8)
 
            for i in range(len(f0)):
                r = f0[i]
                rr = f00[i]
                vstore( (0*4+i)*16, "rsp", r)
                vstore( (0*4+i)*16 + 8, "rsp", rr)

            for i in range(len(f1)):
                r = f1[i]
                rr = f11[i]
                vstore( (1*4+i)*16, "rsp", r)
                vstore( (1*4+i)*16 + 8, "rsp", rr)

            # 
            # 

            x1 = [8, 9, 10, 11]
            x11 = [24, 25, 26, 27]

            x2 = [12, 13, 14, 15]
            x22 = [28, 29, 30, 31]
            # low9mask is gone

            for i in range(4):
                f2_i = 0
                f2_ii = 16
                vload(f2_i,  2*11*16+idx2off(i*3+coeff), real)
                vload(f2_ii, 2*11*16+idx2off(i*3+coeff) + 8, real)

                f0f2_i = 1
                f0f2_ii = 17 
                # TODO: find register for t0, t00
                t0 = 19
                vload(t0, (0*4+i)*16, "rsp")
                vadd(f0f2_i, f2_i, t0)
                vload(t0, (0*4+i)*16 + 8, "rsp")
                vadd(f0f2_ii, f2_ii, t0)

                f1f3_i = 2
                f1f3_ii = 18
                vload(t0,  (1*4+i)*16, "rsp")
                vadd(f1f3_i, f3[i], t0)
                vload(t0, (1*4+i)*16 + 8, "rsp")
                vadd(f1f3_ii, f33[i], t0)

                vadd(x1[i], f0f2_i, f1f3_i)
                vadd(x11[i], f0f2_ii, f1f3_ii)

                vsub(x2[i], f0f2_i, f1f3_i)
                vsub(x22[i], f0f2_ii, f1f3_ii)

                vstore( (2*4+i)*16, "rsp", f2_i)
                vstore( (2*4+i)*16 + 8, "rsp", f2_ii)

            
            t0 = 0 
            t1 = 1 
            karatsuba_eval(prep, dst_off=1*9*3, src=x1, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=1*9*3, src=x1, t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=2*9*3, src=x2, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=2*9*3, src=x2, t0=t0, t1=t1, coeff=coeff, slide=8)

            x3 = [8, 9, 10, 11]
            x33 = [24, 25, 26, 27]

            x4 = [12, 13, 14, 15]
            x44 = [28, 29, 30, 31]

            const_2 = 19
            vconst(const_2, 2)
            const_1 = 20
            vconst(const_1, 1)

            for i in range(4):
                f2_i = 0
                f2_ii = 16
                vload(f2_i, (2*4+i)*16, "rsp")
                vload(f2_ii, (2*4+i)*16 + 8, "rsp")

                f2_4_i = 0
                f2_4_ii = 16

                vsl(f2_4_i, f2_i, const_2)
                vsl(f2_4_ii, f2_ii, const_2)

                f0f2_4_i = 0
                f0f2_4_ii = 16
                t0 = 1
                t00 = 17 
                vload(t0, (0*4+i)*16, "rsp")
                vload(t00, (0*4+i)*16 + 8, "rsp")
                vadd(f0f2_4_i, f2_4_i, t0)
                vadd(f0f2_4_ii, f2_4_ii, t00)

                f3_4_i = 1 
                f3_4_ii = 17 
                vsl(f3_4_i, f3[i], const_2)
                vsl(f3_4_ii, f33[i], const_2)

                f1f3_4_i = 1
                f1f3_4_ii = 17
                t0 = 2
                t00 = 18 
                vload(t0, (1*4+i)*16, "rsp")
                vload(t00, (1*4+i)*16 + 8, "rsp")
                vadd(f1f3_4_i, f3_4_i, t0)
                vadd(f1f3_4_ii, f3_4_ii, t00)

                f1_2f3_8_i = 1
                f1_2f3_8_ii = 17
                vsl(f1_2f3_8_i, f1f3_4_i, const_1)
                vsl(f1_2f3_8_ii, f1f3_4_ii, const_1)

                vadd(x3[i], f0f2_4_i, f1_2f3_8_i)
                vadd(x33[i], f0f2_4_ii, f1_2f3_8_ii)

                vsub(x4[i], f0f2_4_i, f1_2f3_8_i)
                vsub(x44[i], f0f2_4_ii, f1_2f3_8_ii)

            t0 = 0
            t1 = 1 
            karatsuba_eval(prep, dst_off=3*9*3, src=x3, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=3*9*3, src=x33, t0=t0, t1=t1, coeff=coeff, slide=8)

            karatsuba_eval(prep, dst_off=4*9*3, src=x4, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=4*9*3, src=x44, t0=t0, t1=t1, coeff=coeff, slide=8)

            x5 = [12, 13, 14, 15]
            x55 = [28, 29, 30, 31]

            for i in range(4):
                f3_3_i = 0
                f3_3_ii = 16 
                vmul(f3_3_i, f3[i], const_3)
                vmul(f3_3_ii, f33[i], const_3)

                f2f3_3_i = 0
                f2f3_3_ii = 16
                t0 = 19 
                vload(t0, (2*4+i)*16, "rsp")
                vadd(f2f3_3_i, f3_3_i, t0)
                vload(t0, (2*4+i)*16 + 8, "rsp")
                vadd(f2f3_3_ii, f3_3_ii, t0)

                f2_3f3_9_i = 0
                f2_3f3_9_ii = 16 
                vmul(f2_3f3_9_i, f2f3_3_i, const_3)
                vmul(f2_3f3_9_ii, f2f3_3_ii, const_3)

                f1f2_3f3_9_i = 0
                f1f2_3f3_9_ii = 16
                vload(t0, (1*4+i)*16, "rsp")
                vadd(f1f2_3f3_9_i, f2_3f3_9_i, t0)
                vload(t0, (1*4+i)*16 + 8, "rsp")
                vadd(f1f2_3f3_9_ii, f2_3f3_9_ii, t0)

                f1_3f2_9f3_27_i = 0 
                f1_3f2_9f3_27_ii = 16
                vmul(f1_3f2_9f3_27_i, f1f2_3f3_9_i, const_3)
                vmul(f1_3f2_9f3_27_ii, f1f2_3f3_9_ii, const_3)

                vload(t0, (0*4+i)*16, "rsp")
                vadd(x5[i], f1_3f2_9f3_27_i, t0)
                vload(t0, (0*4+i)*16 + 8, "rsp")
                vadd(x55[i], f1_3f2_9f3_27_ii, t0)

            t0 = 0
            t1 = 1
            karatsuba_eval(prep, dst_off=5*9*3, src=x5, t0=t0, t1=t1, coeff=coeff)
            karatsuba_eval(prep, dst_off=5*9*3, src=x55, t0=t0, t1=t1, coeff=coeff, slide=8)

    K2_K2_transpose_64x44(r_out, a_prep, b_prep)

    # TODO: line 360 forward





                


