p = print

def mult_128x128(xy, xxyy, x, y, t1, t2, t3):
    # Guarantee not modify x, y registers
    t01 = xy  # careful about pipelining here
    t02 = xxyy
    t22 = t3 

    p("vmull_p64 (y{}, y{}) = y{}".format(x, y, t01)) # x0, y0 -> t0

    p("vmull_high_p64 (y{}, y{}) = y{}".format(x, y, t02)) # x1 * y1 -> t2 

    # y0|y1 -> y1| y0
    p("vextq_p64(y{}, y{}, 8) = y{}".format(y, y, t22))
    
    p("vmull_p64 ( y{}, y{} ) = y{}".format(x, t22, t1)) # x0 *  y1 -> t1

    p("vmull_high_p64 (y{}, y{}) = y{}".format(x, t22, t2)) # x1 * y0 -> t2

    # t1 = t1 + t2
    p("vaddq_p64(y{}, y{}) = y{}".format(t1, t2, t1))

    # temporary register, t2 = 0
    p("0 = y{}".format(t2))

    # Aligned t2(16) = (t2, t1)
    p("vextq_p64(y{}, y{}, 8) = y{}".format(t2, t1, t22))

    #  t01 = t2(16) + t01
    p("vaddq_p64(y{}, y{}) = y{}".format(t22, t01, xy)) # out_low

    # Aligned t2(16) = (t1, t2)
    p("vextq_p64(y{}, y{}, 8) = y{}".format(t1, t2, t22))

    # t02 = t2(16) + t02
    p("vaddq_p64(y{}, y{}) = y{}".format(t22, t02, xxyy)) # out_high


def karatsuba_256x256(ab, aabb, t0, t1, t2, t3, t4):
    """assumes a and b are two xmm low registers"""
    """assumes aa and bb are two xmm high registers"""

    a, b = ab
    aa, bb = aabb
    a_mix, b_mix = t0, t0 + 16
    
    z1, z11 = t1, t1 + 16

    # Calling convention
    # a,b: 256 avx2 register (ymm)
    # aa: is high(a) 
    # bb: is high(b)
    # a is low(a)
    # b is low(b)
    
    # aa = a1 = high(a)
    # bb = b1 = high(b)
    # p("vextracti128 $1, y{}, %xmm{}".format(a, a1))
    # p("vextracti128 $1, y{}, %xmm{}".format(b, b1))

    # aa, bb = high(a), high(b)
    # b = low(out); bb = high(out)
    mult_128x128(b, bb, aa, bb, t2, t3, t4)

    # high(a) + low(a)
    # p("vpxor %xmm{}, %xmm{}, %xmm{}".format(a0, a1, a1))  # a1 contains [0][a0 xor a1]
    p("vaddq_p64 (y{}, y{}) = y{}".format(aa, a, a_mix))

    # p("vpxor %xmm{}, %xmm{}, %xmm{}".format(b0, b1, b1))
    p("vaddq_p64 (y{}, y{}) = y{}".format(bb, b, b_mix))

    mult_128x128(z1, z11, a_mix, b_mix, t2, t3, t4)
    # Copy
    p("y{} = y{}".format(aa, a_mix))
    mult_128x128(a, aa, a_mix, b, t2, t3, t4)

    # p("vpxor y{}, y{}, y{}".format(z1, b, z1))
    p("vaddq_p128  (y{}, y{}) = y{}".format(a, z1, z1))
    p("vaddq_p128  (y{}, y{}) = y{}".format(b, z1, z1))
    
    # p("vpxor y{}, y{}, y{}".format(z1, a, z1))
    p("vaddq_p128  (y{}, y{}) = y{}".format(aa, z11, z11))
    p("vaddq_p128  (y{}, y{}) = y{}".format(bb, z11, z11))

    p("vaddq_p128 (y{}, y{}) = y{}".format(b, z11, b))
    p("vaddq_p128 (y{}, y{}) = y{}".format(a, z1, a))

    ab = (a, b)
    aabb = (aa, bb)



def karatsuba_512x512(w, ab, xy, t0, t1, t2, t3, t4, t5, t6):
    """ w: 4 ymm reg. ab: 2 ymm reg. xy: 2 ymm reg. t*: 1 ymm reg """
    a, b = ab[0], ab[1]
    x, y = xy[0], xy[1]
    # a = 4, b = 5
    # x = 6, y = 7

    aPb = t5
    xPy = t6
    # aPb = y13 
    # xPy = y14 
    p("vpxor y{}, y{}, y{}".format(a, b, aPb))
    p("vpxor y{}, y{}, y{}".format(x, y, xPy))

    aTx = w[0], w[1]
    # aTx = (0, 1)
    # (0, 1) - 4 - 6- 8, 9, 10, 11, 12
    karatsuba_256x256(aTx, a, x, t0, t1, t2, t3, t4)

    bTy = w[2], w[3]
    # bTy = (2, 3)
    karatsuba_256x256(bTy, b, y, t0, t1, t2, t3, t4)

    aPbTxPy = ab
    # aPbTxPy = (4, 5)
    karatsuba_256x256(aPbTxPy, aPb, xPy, t0, t1, t2, t3, t4)

    p("vpxor y{}, y{}, y{}".format(aTx[0], aPbTxPy[0], aPbTxPy[0]))
    p("vpxor y{}, y{}, y{}".format(aTx[1], aPbTxPy[1], aPbTxPy[1]))
    p("vpxor y{}, y{}, y{}".format(bTy[0], aPbTxPy[0], aPbTxPy[0]))
    p("vpxor y{}, y{}, y{}".format(bTy[1], aPbTxPy[1], aPbTxPy[1]))
    p("vpxor y{}, y{}, y{}".format(aPbTxPy[0], w[1], w[1]))
    p("vpxor y{}, y{}, y{}".format(aPbTxPy[1], w[2], w[2]))

def store_1024(w, ptr="%rdi"):
    p("vmovdqa y{}, {}({})".format(w[0], 32*0, ptr))
    p("vmovdqa y{}, {}({})".format(w[1], 32*1, ptr))
    p("vmovdqa y{}, {}({})".format(w[2], 32*2, ptr))
    p("vmovdqa y{}, {}({})".format(w[3], 32*3, ptr))

def load_1024(w, ptr="%rdi"):
    p("vmovdqa {}({}), y{}".format(32*0, ptr, w[0]))
    p("vmovdqa {}({}), y{}".format(32*1, ptr, w[1]))
    p("vmovdqa {}({}), y{}".format(32*2, ptr, w[2]))
    p("vmovdqa {}({}), y{}".format(32*3, ptr, w[3]))

def vec256_sr53(r, a, t):
    p("vpand mask1110(%rip), y{}, y{}".format(a, r))
    p("vpsllq ${}, y{}, y{}".format(11, r, r))
    p("vpermq ${}, y{}, y{}".format(int('00''11''10''01', 2), r, r))
    p("vpsrlq ${}, y{}, y{}".format(53, a, t))
    p("vpxor y{}, y{}, y{}".format(t, r, r))

def vec256_sl203(r, a, t):
    p("vpand mask0001(%rip), y{}, y{}".format(a, r))
    p("vpermq ${}, y{}, y{}".format(int('00''11''10''01', 2), r, r))
    p("vpsllq ${}, y{}, y{}".format(11, r, r))

def mul512_and_accumulate(s, r, t):
    # multiply r by x^512, reduce mod x^821-1, add to s
    s1,s2,s3,s4 = s
    t5,t6,t7,t8 = t

    # r[0] is aligned with 512:767
    p("vpxor y{}, y{}, y{}".format(r[0], s3, s3))

    # the low 53 of r[1] are aligned with 768:820
    p("vpand low53(%rip), y{}, y{}".format(r[1], t8))
    p("vpxor y{}, y{}, y{}".format(t8, s4, s4))
    # align the high 203 of r[1] with 0:202
    vec256_sr53(t5, r[1], t8)

    # align low 53 of r[2] with 203:255
    vec256_sl203(t6, r[2], t8)
    # align high 203 of r[2] with 256:458
    vec256_sr53(t7, r[2], t8)
    p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
    p("vpxor y{}, y{}, y{}".format(t6, s1, s1))

    # align low 53 of r[3] with 459:511
    vec256_sl203(t5, r[3], t8)
    # align high 203 of r[3] with 512:714
    vec256_sr53(t6, r[3], t8)
    p("vpxor y{}, y{}, y{}".format(t5, t7, t7))
    p("vpxor y{}, y{}, y{}".format(t7, s2, s2))
    p("vpxor y{}, y{}, y{}".format(t6, s3, s3))

def mul1024_and_accumulate(s, r, t):
    # multiply r by x^1024 (= x^203), reduce mod x^821 - 1, add to s
    t5,t6,t7 = t

    for i in [0,1,2,3]:
      # s[i] <- s[i] + "high 203 of r[i-1] | low 53 of r[i]"
      vec256_sr53(t5, r[i-1], t7)
      vec256_sl203(t6, r[i], t7)
      p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
      p("vpxor y{}, y{}, y{}".format(t6, s[i], s[i]))

if __name__ == '__main__':
    p(".data")
    p(".section .rodata")
    p(".align 32")

    p("mask1100:")
    for i in [0]*8 + [65535]*8:
        p(".word {}".format(i))
    p("mask0110:")
    for i in [0]*4 + [65535]*8 + [0]*4:
        p(".word {}".format(i))
    p("mask0011:")
    for i in [65535]*8 + [0]*8:
        p(".word {}".format(i))
    p("mask0001:")
    for i in [65535]*4 + [0]*12:
        p(".word {}".format(i))
    p("mask1110:")
    for i in [0]*4 + [65535]*12:
        p(".word {}".format(i))
    p("low53:")
    for i in [65535]*3 + [31] + [0]*12:
        p(".word {}".format(i))

    p(".text")
    p(".hidden poly_R2_mul")
    p(".global poly_R2_mul")
    p(".att_syntax prefix")

    p("poly_R2_mul:")
    # rdi holds result, rsi holds a, rdx holds b
    # TODO: allow rdi=rsi

    r=0,1,2,3
    a,b=4,5
    w,x=6,7
    t1,t2,t3,t4=8,9,10,11
    t5,t6,t7,t8=12,13,14,15
    p("vmovdqa {}(%rsi), y{}".format( 0, a))
    p("vmovdqa {}(%rsi), y{}".format(32, b))
    p("vmovdqa {}(%rdx), y{}".format( 0, w))
    p("vmovdqa {}(%rdx), y{}".format(32, x))

    karatsuba_512x512(r, (a, b), (w, x), t1, t2, t3, t4, t5, t6, t7)

    # store r mod x^821-1, do not modify r
    vec256_sr53(t1, r[3], t7)
    p("vpxor y{}, y{}, y{}".format(r[0], t1, t1))
    p("vpand low53(%rip), y{}, y{}".format(r[3], t2))
    store_1024((t1,r[1],r[2],t2))

    # add r * x^512 mod x^821-1 to output
    s = (a,b,w,x)
    load_1024(s, "%rdi")
    mul512_and_accumulate(s, r, (t1,t2,t3,t4))
    store_1024(s, "%rdi")

    c, d, y, z = 4, 5, 6, 7
    p("vmovdqa {}(%rsi), y{}".format(64, c))
    p("vmovdqa {}(%rsi), y{}".format(96, d))
    p("vmovdqa {}(%rdx), y{}".format(64, y))
    p("vmovdqa {}(%rdx), y{}".format(96, z))

    karatsuba_512x512(r, (c, d), (y, z), t1, t2, t3, t4, t5, t6, t7)

    s = (c,d,y,z)
    load_1024(s, "%rdi")
    mul512_and_accumulate(s, r, (t1,t2,t3,t4))
    mul1024_and_accumulate(s, r, (t1,t2,t3))
    store_1024(s, "%rdi")

    # used all free registers during accumulate, reload inputs
    a,b,w,x=4,5,6,7
    c,d,y,z=8,9,10,11
    t5,t6,t7,t8=12,13,14,15
    load_1024((a,b,c,d), "%rsi")
    load_1024((w,x,y,z), "%rdx")

    p("vpxor y{}, y{}, y{}".format(a, c, a))
    p("vpxor y{}, y{}, y{}".format(b, d, b))
    p("vpxor y{}, y{}, y{}".format(w, y, w))
    p("vpxor y{}, y{}, y{}".format(x, z, x))

    karatsuba_512x512(r, (a,b), (w, x), c, d, y, z, t5, t6, t7)

    # multiply by 512 and reduce mod x^821 - 1
    s = (c,d,y,z)
    load_1024(s, "%rdi")
    mul512_and_accumulate(s, r, (a,b,w,x))
    store_1024(s, "%rdi")

    p("ret")
