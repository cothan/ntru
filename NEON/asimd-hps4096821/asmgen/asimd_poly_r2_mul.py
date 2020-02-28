p = print


def mult_128x128(out, x, y, t1, t2, t3):
    # Guarantee not modify x, y registers
    p("// mult128x128 BEGIN")
    xxyy, xy = out

    p("vmull_p64 (y{}, y{}) = y{}".format(x, y, xy))  # x0, y0 -> t0

    p("vmull_high_p64 (y{}, y{}) = y{}".format(x, y, xxyy))  # x1 * y1 -> t2
    #####################
    # y1| y0 -> y0| y1
    p("vextq_p64(y{}, y{}, 1) = y{}".format(y, y, t3))
    # t3 = y0|y1
    p("vmull_p64 ( y{}, y{} ) = y{}".format(x, t3, t1))  # x0 *  y1 -> t1

    p("vmull_high_p64 (y{}, y{}) = y{}".format(x, t3, t2))  # x1 * y0 -> t2

    # t1 = t1 + t2
    p("vaddq_p64(y{}, y{}) = y{}".format(t1, t2, t1))
    # t2 is free
    p("0 = y{}".format(t2))

    #####################
    # t3 is free
    # Aligned t3 = (t2, t1)
    p("vextq_p64(y{}, y{}, 1) = y{}".format(t1, t2, t3))

    #  xy = t2(16) + xy
    p("vaddq_p64(y{}, y{}) = y{}".format(t3, xy, xy))  # out_low

    # Aligned t2(16) = (t1, t2)
    p("vextq_p64(y{}, y{}, 1) = y{}".format(t2, t1, t3))

    # xxyy = t2(16) + xxyy
    p("vaddq_p64(y{}, y{}) = y{}".format(t3, xxyy, xxyy))  # out_high

    # out = (xxyy, xy)
    p("// mult128x128 END")


def karatsuba_256x256(ab, a_in, b_in, t0, t1, t2, t3, t4, t5, t6):
    """output: assumes a and b are two xmm low registers"""
    """output: assumes aa and bb are two xmm high registers"""

    p("// karatsuba_256x256 BEGIN")

    # z00, z0 = a
    # z22, z2 = b
    z00, z0, z22, z2 = ab

    aa, a = a_in
    bb, b = b_in

    t22 = t5
    t33 = t6

    # aa, bb = high(a), high(b)
    # b = low(out); t22 = high(out)
    mult_128x128((z22, z2), aa, bb, t2, t3, t4)

    p("vaddq_p128 (y{}, y{}) = y{}".format(aa, a, t0))
    p("vaddq_p128 (y{}, y{}) = y{}".format(bb, b, t1))

    mult_128x128((t22, t2), t0, t1, t3, t33, t4)
    mult_128x128((z00, z0), a, b, t3, t33, t4)

    p("vaddq_p128  (y{}, y{}) = y{}".format(t22, z22, t22))
    p("vaddq_p128  (y{}, y{}) = y{}".format(t2, z2, t2))

    p("vaddq_p128  (y{}, y{}) = y{}".format(t22, z00, t22))
    p("vaddq_p128  (y{}, y{}) = y{}".format(t2, z0, t2))

    # p("vpxor y{}, y{}, y{}".format(z1, a, z1))
    p("vaddq_p128  (y{}, y{}) = y{}".format(z22, t22, z22))
    p("vaddq_p128  (y{}, y{}) = y{}".format(z00, t2, z00))

    # ab = (z00, z0, z22, z2)
    p("// karatsuba_256x256 END")


def karatsuba_512x512(w, ab_in, xy_in, t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10):
    """ w: 4 ymm reg. ab: 2 ymm reg. xy: 2 ymm reg. t*: 1 ymm reg """
    """ w: 8 xmm reg. ab: 4 xmm reg. xy: 4 xmm reg. t*: 1 ymm reg """

    p("// karatsuba_512x512 BEGIN")
    
    (w00, w0), (w11, w1), (w22, w2), (w33, w3) = w

    (aa, a), (bb, b) = ab_in
    (xx, x), (yy, y) = xy_in

    t55 = t9
    t66 = t10

    p("vaddq_p128 (y{}, y{}) = y{}".format(a, b, t5))
    p("vaddq_p128 (y{}, y{}) = y{}".format(aa, bb, t55))

    p("vaddq_p128 (y{}, y{}) = y{}".format(x, y, t6))
    p("vaddq_p128 (y{}, y{}) = y{}".format(xx, yy, t66))

    karatsuba_256x256((w00, w0, w11, w1), (aa, a),
                      (xx, x), t0, t1, t2, t3, t4, t7, t8)
    karatsuba_256x256((w22, w2, w33, w3), (bb, b),
                      (yy, y), t0, t1, t2, t3, t4, t7, t8)
    karatsuba_256x256((aa, a, bb, b), (t55, t5), (t66, t6),
                      t0, t1, t2, t3, t4, t7, t8)

    p("vaddq_p128 (y{}, y{}) = y{}".format(w00, aa, aa))
    p("vaddq_p128 (y{}, y{}) = y{}".format(w0, a, a))
    p("vaddq_p128 (y{}, y{}) = y{}".format(w11, bb, bb))
    p("vaddq_p128 (y{}, y{}) = y{}".format(w1, b, b))

    p("vaddq_p128 (y{}, y{}) = y{}".format(w22, aa, aa))
    p("vaddq_p128 (y{}, y{}) = y{}".format(w2, a, a))
    p("vaddq_p128 (y{}, y{}) = y{}".format(w33, bb, bb))
    p("vaddq_p128 (y{}, y{}) = y{}".format(w3, b, b))

    p("vaddq_p128 (y{}, y{}) = y{}".format(aa, w11, w11))
    p("vaddq_p128 (y{}, y{}) = y{}".format(a, w1, w1))

    p("vaddq_p128 (y{}, y{}) = y{}".format(bb, w22, w22))
    p("vaddq_p128 (y{}, y{}) = y{}".format(b, w2, w2))

    # w = (w00, w0, w11, w1, w22, w2, w33, w3)
    p("// karatsuba_512x512 END")


def store_1024(w, ptr="%rdi"):
    p("// store_1024 BEGIN")

    (w00, w0), (w11, w1), (w22, w2), (w33, w3) = w
    p("vst1q_p16 ({} + {}, y{});".format(16*0, ptr, w00))
    p("vst1q_p16 ({} + {}, y{});".format(16*1, ptr, w0))
    p("vst1q_p16 ({} + {}, y{});".format(16*2, ptr, w11))
    p("vst1q_p16 ({} + {}, y{});".format(16*3, ptr, w1))

    p("vst1q_p16 ({} + {}, y{});".format(16*4, ptr, w22))
    p("vst1q_p16 ({} + {}, y{});".format(16*5, ptr, w2))
    p("vst1q_p16 ({} + {}, y{});".format(16*6, ptr, w33))
    p("vst1q_p16 ({} + {}, y{});".format(16*7, ptr, w3))

    # w = (w00, w0, w11, w1, w22, w2, w33, w3)
    p("// store_1024 END")

def load_1024(w, ptr="%rdi"):
    p("// load_1024 BEGIN")

    (w00, w0), (w11, w1), (w22, w2), (w33, w3) = w
    p("vld1q_p16 ({} + {}) = y{}".format(16*0, ptr, w00))
    p("vld1q_p16 ({} + {}) = y{}".format(16*1, ptr, w0))
    p("vld1q_p16 ({} + {}) = y{}".format(16*2, ptr, w11))
    p("vld1q_p16 ({} + {}) = y{}".format(16*3, ptr, w1))
    p("vld1q_p16 ({} + {}) = y{}".format(16*4, ptr, w22))
    p("vld1q_p16 ({} + {}) = y{}".format(16*5, ptr, w2))
    p("vld1q_p16 ({} + {}) = y{}".format(16*6, ptr, w33))
    p("vld1q_p16 ({} + {}) = y{}".format(16*7, ptr, w3))

    # w = (w00, w0, w11, w1, w22, w2, w33, w3)
    p("// load_1024 END")


def vec256_sr53(r_out, a_in, t0, t1):
    p("// vec256_sr53 BEGIN")
    rr, r = r_out
    aa, a = a_in

    p("0xffffffffffffffff0000000000000000 = y{}".format(t0))
    p("vandq_u16 (y{}, y{}) = y{}".format(a, t0, r))

    # No choice, shift left by 11
    # rr = aa
    p("y{} << 11 = y{}".format(aa, rr))
    p("y{} << 11 = y{}".format(r, r))

    # t0 = a3|a2 , t1 = a1|a4
    p("vextq_p64 (y{}, y{}, 1) = y{}".format(r, rr, t0))
    p("vextq_p64 (y{}, y{}, 1) = y{}".format(rr, r, t1))

    p("y{} >> 53 = y{}".format(a, r))
    p("y{} >> 53 = y{}".format(aa, rr))

    p("vaddq_p128  (y{}, y{}) = y{}".format(r, t0, r))
    p("vaddq_p128  (y{}, y{}) = y{}".format(rr, t1, rr))

    # r_out = (rr, r)
    p("// vec256_sr53 END")

def vec256_sl203(r_out, a_in, t0, t1):
    p("// vec256_sl203 BEGIN")
    _, a = a_in
    rr, r = r_out

    # p("vpand mask0001(%rip), y{}, y{}".format(a, r))
    # rr| r = 0 | r & 0xf
    p("0 = y{}".format(rr))
    p("y{} & 0xffffffffffffffff = y{}".format(a, r))

    # p("vpermq ${}, y{}, y{}".format(int('00''11''10''01', 2), r, r))
    p("vextq_p64 (y{}, y{}, 1) = y{}".format(r, rr, t0))
    p("vextq_p64 (y{}, y{}, 1) = y{}".format(rr, r, t1))

    # p("vpsllq ${}, y{}, y{}".format(11, r, r))
    p("y{} << 11 = y{}".format(t0, r))
    p("y{} << 11 = y{}".format(t1, rr))

    # r_out = (rr, r)
    p("// vec256_sl203 END")


def mul512_and_accumulate(s, r, t):
    p("// mul512_and_accumulate BEGIN")

    # multiply r by x^512, reduce mod x^821-1, add to s
    (s11, s1), (s22, s2), (s33, s3), (s44, s4) = s
    t55, t5, t66, t6, t77, t7, t88, t8 = t

    (r00, r0), (r11, r1), (r22, r2), (r33, r3) = r

    # r[0] is aligned with 512:767
    # p("vpxor y{}, y{}, y{}".format(r[0], s3, s3))
    p("vaddq_p128(y{}, y{}) = y{}".format(r00, s33, s33))
    p("vaddq_p128(y{}, y{}) = y{}".format(r0, s3, s3))

    # TODO
    # the low 53 of r[1] are aligned with 768:820
    # p("vpand low53(%rip), y{}, y{}".format(r[1], t8))
    p("0x1fffffffffffff = y{}".format(t88))
    p("y{} & y{} = y{}".format(r1, t88, t8))
    # r11 = t88
    
    # p("vpxor y{}, y{}, y{}".format(t8, s4, s4))
    # r11 = t88
    p("vaddq_p128(y{}, y{}) = y{}".format(r11, s44, s44))
    p("vaddq_p128(y{}, y{}) = y{}".format(t8, s4, s4))
    
    # align the high 203 of r[1] with 0:202
    vec256_sr53((t55, t5), (r11, r1), t8, t88)

    # align low 53 of r[2] with 203:255
    vec256_sl203((t66, t6), (r22, r2), t8, t88)
    # align high 203 of r[2] with 256:458
    vec256_sr53((t77, t7), (r22, r2), t8, t88)
    
    # p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
    p("vaddq_p128(y{}, y{}) = y{}".format(t55, t66, t66))
    p("vaddq_p128(y{}, y{}) = y{}".format(t5, t6, t6))

    # p("vpxor y{}, y{}, y{}".format(t6, s1, s1))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s11, s11))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s1, s1))

    # align low 53 of r[3] with 459:511
    vec256_sl203((t55, t5), (r33, r3), t8, t88)
    # align high 203 of r[3] with 512:714
    vec256_sr53((t66, t6), (r33, r3), t8, t88)

    # p("vpxor y{}, y{}, y{}".format(t5, t7, t7))
    p("vaddq_p128(y{}, y{}) = y{}".format(t55, t77, t77))
    p("vaddq_p128(y{}, y{}) = y{}".format(t5, t7, t7))

    # p("vpxor y{}, y{}, y{}".format(t7, s2, s2))
    p("vaddq_p128(y{}, y{}) = y{}".format(t77, s22, s22))
    p("vaddq_p128(y{}, y{}) = y{}".format(t7, s2, s2))

    # p("vpxor y{}, y{}, y{}".format(t6, s3, s3))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s33, s33))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s3, s3))

    # assert s == (s11, s1), (s22, s2), (s33, s3), (s44, s4)
    p("// mul512_and_accumulate END")

def mul1024_and_accumulate(s, r, t):
    p("// mul1024_and_accumulate BEGIN")

    # multiply r by x^1024 (= x^203), reduce mod x^821 - 1, add to s
    t55, t5, t66, t6, t77, t7 = t
    (s00, s0), (s11, s1), (s22, s2), (s33, s3) = s 
    (r00, r0), (r11, r1), (r22, r2), (r33, r3) = r 
    # 0
    # s[i] <- s[i] + "high 203 of r[i-1] | low 53 of r[i]"
    vec256_sr53((t55, t5), (r33, r3), t7, t77)
    vec256_sl203((t66, t6), (r00, r0), t7, t77)
    # p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
    p("vaddq_p128(y{}, y{}) = y{}".format(t55, t66, t66))
    p("vaddq_p128(y{}, y{}) = y{}".format(t5, t6, t6))

    # p("vpxor y{}, y{}, y{}".format(t6, s[i], s[i]))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s00, s00))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s0, s0))

    # 1 
    vec256_sr53((t55, t5), (r00, r0), t7, t77)
    vec256_sl203((t66, t6), (r11, r1), t7, t77)
    # p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
    p("vaddq_p128(y{}, y{}) = y{}".format(t55, t66, t66))
    p("vaddq_p128(y{}, y{}) = y{}".format(t5, t6, t6))

    # p("vpxor y{}, y{}, y{}".format(t6, s[i], s[i]))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s11, s11))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s1, s1))

    # 2 
    vec256_sr53((t55, t5), (r11, r1), t7, t77)
    vec256_sl203((t66, t6), (r22, r2), t7, t77)
    # p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
    p("vaddq_p128(y{}, y{}) = y{}".format(t55, t66, t66))
    p("vaddq_p128(y{}, y{}) = y{}".format(t5, t6, t6))

    # p("vpxor y{}, y{}, y{}".format(t6, s[i], s[i]))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s22, s22))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s2, s2))

    # 3 
    vec256_sr53((t55, t5), (r22, r2), t7, t77)
    vec256_sl203((t66, t6), (r33, r3), t7, t77)
    # p("vpxor y{}, y{}, y{}".format(t5, t6, t6))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s11, s11))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s1, s1))

    # p("vpxor y{}, y{}, y{}".format(t6, s[i], s[i]))
    p("vaddq_p128(y{}, y{}) = y{}".format(t66, s33, s33))
    p("vaddq_p128(y{}, y{}) = y{}".format(t6, s3, s3))

    p("// mul1024_and_accumulate END")

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

    R = (0, 1), (2, 3), (4, 5), (6, 7)
    A, B = (8, 9), (10, 11)
    W, X = (12, 13), (14, 15)
    t0, t3, t4, t5 = 16, 17, 18, 19
    t6, t7, t8, t9 = 20, 21, 22, 23
    t10, t11 , t12, t13 =24, 25, 26, 27
    T1 = (28, 29)
    T2 = (30, 31)

    C = (t6, t7)
    D = (t8, t9)
    Y = (t10, t11)
    Z = (t12, t13)

    # load a 
    p("vld1q_p16 ({} + {}) = y{}".format(0*16, "a->coeffs", A[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(1*16, "a->coeffs", A[1]))
    # load b 
    p("vld1q_p16 ({} + {}) = y{}".format(2*16, "a->coeffs", B[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(3*16, "a->coeffs", B[1]))
    # load w 
    p("vld1q_p16 ({} + {}) = y{}".format(0*16, "b->coeffs", W[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(1*16, "b->coeffs", W[1]))
    # load x 
    p("vld1q_p16 ({} + {}) = y{}".format(2*16, "b->coeffs", X[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(3*16, "b->coeffs", X[1]))

    # p("vmovdqa {}(%rsi), y{}".format(0, a))
    # p("vmovdqa {}(%rsi), y{}".format(32, b))
    # p("vmovdqa {}(%rdx), y{}".format(0, w))
    # p("vmovdqa {}(%rdx), y{}".format(32, x))

    karatsuba_512x512(R, (A, B), (W, X), t0, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)

    # store r mod x^821-1, do not modify r
    vec256_sr53(T1, R[3], t0, t3)

    # p("vpxor y{}, y{}, y{}".format(r[0], t1, t1))
    p("vaddq_p128  (y{}, y{}) = y{}".format(R[0][0], T1[0], T1[0]))
    p("vaddq_p128  (y{}, y{}) = y{}".format(R[0][1], T1[1], T1[1]))


    # p("vpand low53(%rip), y{}, y{}".format(r[3], t2))
    p("0x1fffffffffffff = y{}".format(t11))
    p("y{} & y{} = y{}".format(t11, R[3][0], T2[0]))
    p("y{} = y{}".format(R[3][1], T2[1]))


    # store_1024((t1, r[1], r[2], t2))
    store_1024((T1, R[1], R[2], T2), ptr="c->coeffs")

    # add r * x^512 mod x^821-1 to output
    S = (A, B, W, X)
    load_1024(S, ptr="c->coeffs")

    # mul512_and_accumulate(s, r, (t1, t2, t3, t4))
    mul512_and_accumulate(S, R, (t0, t3, t4, t5, t6, t7, t8, t9))
    store_1024(S, "c->coeffs")

    
    # p("vmovdqa {}(%rsi), y{}".format(64, c))
    # Load c 
    p("vld1q_p16 ({} + {}) = y{}".format(4*16, "a->coeffs", A[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(5*16, "a->coeffs", A[1]))

    # Load d 
    # p("vmovdqa {}(%rsi), y{}".format(96, d))
    p("vld1q_p16 ({} + {}) = y{}".format(6*16, "a->coeffs", B[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(7*16, "a->coeffs", B[1]))

    # Load y 
    # p("vmovdqa {}(%rdx), y{}".format(64, y))
    p("vld1q_p16 ({} + {}) = y{}".format(4*16, "b->coeffs", W[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(5*16, "b->coeffs", W[1]))

    # Load Z
    # p("vmovdqa {}(%rdx), y{}".format(96, z))
    p("vld1q_p16 ({} + {}) = y{}".format(6*16, "b->coeffs", X[0]))
    p("vld1q_p16 ({} + {}) = y{}".format(7*16, "b->coeffs", X[1]))

    karatsuba_512x512(R, (A, B), (W, X), t0, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)

    S = (A, B, W, X)
    load_1024(S, "c->coeffs")
    mul512_and_accumulate(S, R, (t0, t3, t4, t5, t6, t7, t8, t9))
    mul1024_and_accumulate(S, R, (t0, t3, t4, t5, t6, t7))
    store_1024(S, "c->coeffs")

    # used all free registers during accumulate, reload inputs
    ## a, b, w, x = 4, 5, 6, 7
    # A, B, W, X
    ## c, d, y, z = 8, 9, 10, 11
    # C, D, Y, Z
    ## t5, t6, t7, t8 = 12, 13, 14, 15
    # t0, t3, t4, t5 = 16, 17, 18, 19

    load_1024((A, B, C, D), "a->coeffs")
    load_1024((W, X, Y, X), "b->coeffs")

    # p("vpxor y{}, y{}, y{}".format(a, c, a))
    p("vaddq_p128(y{}, y{}) = y{}".format(A[0], C[0], A[0]))
    p("vaddq_p128(y{}, y{}) = y{}".format(A[1], C[1], A[1]))

    # p("vpxor y{}, y{}, y{}".format(b, d, b))
    p("vaddq_p128(y{}, y{}) = y{}".format(B[0], D[0], B[0]))
    p("vaddq_p128(y{}, y{}) = y{}".format(B[1], D[1], B[1]))

    # p("vpxor y{}, y{}, y{}".format(w, y, w))
    p("vaddq_p128(y{}, y{}) = y{}".format(W[0], Y[0], W[0]))
    p("vaddq_p128(y{}, y{}) = y{}".format(W[1], Y[1], W[1]))

    # p("vpxor y{}, y{}, y{}".format(x, z, x))
    p("vaddq_p128(y{}, y{}) = y{}".format(X[0], Z[0], X[0]))
    p("vaddq_p128(y{}, y{}) = y{}".format(X[1], Z[1], X[1]))

    karatsuba_512x512(R, (A, B), (W, X), t0, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12)

    # multiply by 512 and reduce mod x^821 - 1
    # s = (c, d, y, z)
    S = (A, B, W, X)
    load_1024(S, "c->coeffs")
    mul512_and_accumulate(S, R, (t0, t3, t4, t5, t6, t7, t8, t9))
    store_1024(S, "c->coeffs")

    # p("ret")
