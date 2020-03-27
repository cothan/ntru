from asimd_K2_K2_64x44 import K2_K2_transpose_64x44

p = print 

def vload(dst, address):
    p("y{} = vld1q_u16({});".format(dst, address))

def vstore(address, dst, src):
    p("vst1q_u16({} + {}, y{});".format(address, dst, src))

def vadd(c, a, b):
    # c =  a + b 
    p("y{} = vaddq_u16(y{}, y{});".format(c, a, b))

def vsub(c, a, b):
    # c = a - b
    p("y{} = vsubq_u16(y{}, y{});".format(c, a, b))

def karatsuba_eval(dst, dst_off, coeff, src, t0, t1):
    slide = 0
    for i in range(2):
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

        slide = 8

def karatsuba_interpolate(dst, dst_off, src, src_off, coeff, t0, t1, t2):
    def addr(i, off, type=0):
        if type == 0:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16, src)
        else:
            return '{}+{}'.format((src_off+3*(2*i+off//44)+coeff)*16 + 8, src)

    for i in range(2):
        r0_44 = 0
        vload(r0_44, addr(0, 44, i))
        out0_44 = r0_44
        vload(t0, addr(1, 0, i))
        vsub(out0_44, r0_44, t0)

        r2_44 = 1
        vload(r2_44, addr(2, 44, i))
        out1_0 = r2_44
        vsub(out1_0, r2_44, out0_44)
        
        vload(t0 , add(1, 44, i))
        vload(t1 , add(0, 0, i) )
        vload(t2 , add(2, 0, i) )

        vsub(out1_0, out1_0, t0)
        vsub(out0_44, out0_44, t1)
        vsub(out0_44, out0_44, t2)

        r3_44 = 2
        vload(r3_44, addr(3, 44, i))
        out2_44 = r3_44
        vload(t0, addr(4, 0, i))
        vsub(out2_44, r3_44, t0)

        r5_44 = 3
        vload(r5_44, addr(5, 44, i))
        out3_0 = r5_44
        vsub(out3_0, r5_44, out2_44)

        vload(t0 , add(4, 44, i))
        vload(t1 , add(3, 0, i) )
        vload(t2 , add(5, 0, i) )

        vsub(out3_0, out3_0, t0)
        vsub(out2_44, out2_44, t1)
        vsub(out2_44, out2_44, t2)

        r6_44 = 4
        vload(r6_44, addr(6, 44, i))
        vload(t0, addr(7, 0, i))
        vsub(r6_44, r6_44, t0)
        
        r8_44 = 5
        vload(r8_44, addr(8, 44, i))
        r7_0 = r8_44
        vsub(r7_0, r8_44, r6_44)

        vload(t0, addr(7, 44, i))
        vload(t1, addr(6, 0, i))
        vload(t2, addr(8, 0, i))

        vsub(r7_0, r7_0, t0)
        vsub(r6_44, r6_44, t1)
        vsub(r6_44, r6_44, t2)

        vload(t0, addr(3, 0, i))
        vsub(out1_0, out1_0, t0)

        out2_0 = r7_0
        vsub(out2_0, r7_0, out1_0)
        vsub(out2_0, out2_0, out3_0)

        vload(t0, addr(0, 0, i))
        vload(t1, addr(6, 0, i))
        vsub(out1_0, out1_0, t0)
        vadd(out1_0, out1_0, t1)

        r1_44 = 6
        vload(r1_44, addr(1, 44, i))
        out1_44 = 7 
        vsub(out1_44, r1_44, out2_44)
        r7_44 = out2_44
        vload(r7_44, addr(7, 44, i))

        vsub(out2_44, r7_44, out1_44)

        vload(t0, addr(4, 44, i))
        vsub(out2_44, out2_44, t0)
        vsub(out1_44, out1_44, out0_44)
        vsub(out1_44, out1_44, r6_44)

        out0_0 = 8 
        out3_44 = 9 

        vload(out0_0, addr(0, 0, i))
        vload(out3_44, addr(4, 44, i))

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