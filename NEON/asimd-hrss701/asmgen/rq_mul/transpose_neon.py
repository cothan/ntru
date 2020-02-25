
p = print


def _transpose_16x16_to_16x16(dst, src, src_off=0, dst_off=0, src_gap=3, dst_gap=1, dst_limit=None):
    s = [0, None, 1, None, 2, None, 3, None]
    ss = [16, None, 17, None, 18, None, 19, None]
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(0*2)+src_off), src, s[0]))
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(1*2)+src_off), src, s[2]))
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(2*2)+src_off), src, s[4]))
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(3*2)+src_off), src, s[6]))

    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(0*2)+src_off), src, s[0]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(1*2)+src_off), src, s[2]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(2*2)+src_off), src, s[4]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(3*2)+src_off), src, s[6]))
    
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(0*2)+src_off) + 8, src, ss[0]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(1*2)+src_off) + 8, src, ss[2]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(2*2)+src_off) + 8, src, ss[4]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(3*2)+src_off) + 8, src, ss[6]))

    t = list(range(4,12)) + [None] * 8
    tt = list(range(16 + 4, 16 + 12)) + [None] * 8

    # Interleave word, 2 bytes
    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*1+src_off), src, s[0], t[0]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*1+src_off), src, s[0], t[1]))
    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*3+src_off), src, s[2], t[2]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*3+src_off), src, s[2], t[3]))
    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*5+src_off), src, s[4], t[4]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*5+src_off), src, s[4], t[5]))
    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*7+src_off), src, s[6], t[6]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*7+src_off), src, s[6], t[7]))

    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*1+src_off), src, s[0], t[0]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*1+src_off), src, s[0], t[1]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*3+src_off), src, s[2], t[2]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*3+src_off), src, s[2], t[3]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*5+src_off), src, s[4], t[4]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*5+src_off), src, s[4], t[5]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*7+src_off), src, s[6], t[6]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*7+src_off), src, s[6], t[7]))

    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*1+src_off) + 8, src, ss[0], tt[0]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*1+src_off) + 8, src, ss[0], tt[1]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*3+src_off) + 8, src, ss[2], tt[2]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*3+src_off) + 8, src, ss[2], tt[3]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*5+src_off) + 8, src, ss[4], tt[4]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*5+src_off) + 8, src, ss[4], tt[5]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*7+src_off) + 8, src, ss[6], tt[6]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*7+src_off) + 8, src, ss[6], tt[7]))

    r = list(range(0,4)) + list(range(12, 16))
    rr = list(range(16 + 0, 16 + 4)) + list(range(16 + 12, 16 + 16))

    # Interleave double word, 4 bytes
    # p("vpunpckldq y{}, y{}, y{}".format(t[2], t[0], r[0]))
    # p("vpunpckhdq y{}, y{}, y{}".format(t[2], t[0], r[1]))
    # p("vpunpckldq y{}, y{}, y{}".format(t[3], t[1], r[2]))
    # p("vpunpckhdq y{}, y{}, y{}".format(t[3], t[1], r[3]))
    # p("vpunpckldq y{}, y{}, y{}".format(t[6], t[4], r[4]))
    # p("vpunpckhdq y{}, y{}, y{}".format(t[6], t[4], r[5]))
    # p("vpunpckldq y{}, y{}, y{}".format(t[7], t[5], r[6]))
    # p("vpunpckhdq y{}, y{}, y{}".format(t[7], t[5], r[7]))

    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[2], t[0], r[0]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[2], t[0], r[1]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[3], t[1], r[2]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[3], t[1], r[3]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[6], t[4], r[4]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[6], t[4], r[5]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[7], t[5], r[6]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[7], t[5], r[7]))

    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[2], tt[0], rr[0]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[2], tt[0], rr[1]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[3], tt[1], rr[2]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[3], tt[1], rr[3]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[6], tt[4], rr[4]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[6], tt[4], rr[5]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[7], tt[5], rr[6]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[7], tt[5], rr[7]))

    # p("vpunpcklqdq y{}, y{}, y{}".format(r[4], r[0], t[0]))
    # p("vpunpckhqdq y{}, y{}, y{}".format(r[4], r[0], t[1]))
    # p("vpunpcklqdq y{}, y{}, y{}".format(r[5], r[1], t[2]))
    # p("vpunpckhqdq y{}, y{}, y{}".format(r[5], r[1], t[3]))
    # p("vpunpcklqdq y{}, y{}, y{}".format(r[6], r[2], t[4]))
    # p("vpunpckhqdq y{}, y{}, y{}".format(r[6], r[2], t[5]))
    # p("vpunpcklqdq y{}, y{}, y{}".format(r[7], r[3], t[6]))
    # p("vpunpckhqdq y{}, y{}, y{}".format(r[7], r[3], t[7]))

    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[4], r[0], t[0]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[4], r[0], t[1]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[5], r[1], t[2]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[5], r[1], t[3]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[6], r[2], t[4]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[6], r[2], t[5]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[7], r[3], t[6]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[7], r[3], t[7]))

    p("vzip1q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[4], rr[0], tt[0]))
    p("vzip2q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[4], rr[0], tt[1]))
    p("vzip1q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[5], rr[1], tt[2]))
    p("vzip2q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[5], rr[1], tt[3]))
    p("vzip1q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[6], rr[2], tt[4]))
    p("vzip2q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[6], rr[2], tt[5]))
    p("vzip1q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[7], rr[3], tt[6]))
    p("vzip2q_s64 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(rr[7], rr[3], tt[7]))


    # this is where it gets nasty because we only have 16 registers
    t[8:12] = [12, 13, 14, 15]
    tt[8:12] = [16 + 12, 16 + 13, 16 + 14, 16 + 15]
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(4*2)+src_off), src, s[0]))
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(5*2)+src_off), src, s[2]))
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(6*2)+src_off), src, s[4]))
    # p("vmovdqa {}({}), y{}".format(32*(src_gap*(7*2)+src_off), src, s[6]))

    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(4*2)+src_off), src, s[0]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(5*2)+src_off), src, s[2]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(6*2)+src_off), src, s[4]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(7*2)+src_off), src, s[6]))

    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(4*2)+src_off) + 8, src, ss[0]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(5*2)+src_off) + 8, src, ss[2]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(6*2)+src_off) + 8, src, ss[4]))
    p("vld1q_s16 ({}+{}) = y{}".format(16*(src_gap*(7*2)+src_off) + 8, src, ss[6]))

    

    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*9+src_off), src, s[0], t[8]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*9+src_off), src, s[0], t[9]))

    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*9+src_off), src, s[0], t[8]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*9+src_off) + 8, src, ss[0], tt[8]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*9+src_off), src, s[0], t[9]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*9+src_off) + 8, src, ss[0], tt[9]))

    t[12] = s[0]
    tt[12] = ss[0]

    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*11+src_off), src, s[2], t[10]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*11+src_off), src, s[2], t[11]))
    
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*11+src_off), src, s[2], t[10]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*11+src_off) + 8, src, ss[2], tt[10]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*11+src_off), src, s[2], t[11]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*11+src_off) + 8, src, ss[2], tt[11]))
    
    t[13] = s[2]
    tt[13] = ss[0]

    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*13+src_off), src, s[4], t[12]))
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*13+src_off), src, s[4], t[13]))

    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*13+src_off), src, s[4], t[12]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*13+src_off) + 8, src, ss[4], tt[12]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*13+src_off), src, s[4], t[13]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*13+src_off) + 8, src, ss[4], tt[13]))



    t[14] = s[4]
    tt[14] = ss[4]

    # p("vpunpcklwd {}({}), y{}, y{}".format(32*(src_gap*15+src_off), src, s[6], t[14]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*15+src_off), src, s[6], t[14]))
    p("vzip1q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*15+src_off) + 8, src, ss[6], tt[14]))

    t[15] = s[6]  # this is a super tight fit, but it still works out
    tt[15] = ss[6]
    
    # p("vpunpckhwd {}({}), y{}, y{}".format(32*(src_gap*15+src_off), src, s[6], t[15]))

    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*15+src_off), src, s[6], t[15]))
    p("vzip2q_s16 (vld1q_s16({}+{}), y{}) = y{}".format(16*(src_gap*15+src_off) + 8, src, ss[6], tt[15]))

    # .. but now we really do need extra storage space
    # p("vmovdqa y{}, 0(%rsp)".format(t[7]))
    p("vst1q_s16 ({}+{}, y{});".format(0, "rsp", t[7]))
    p("vst1q_s16 ({}+{}, y{});".format(16, "rsp", tt[7]))

    r[0] = t[7]
    rr[0] = tt[7]

    # p("vpunpckldq y{}, y{}, y{}".format(t[10], t[8], r[0]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[10], t[8], r[0]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[10], tt[8], rr[0]))

    r[1] = t[8]  # .. and it's still continuously a tight squeeze
    rr[1] = tt[8]

    # p("vpunpckhdq y{}, y{}, y{}".format(t[10], t[8], r[1]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[10], t[8], r[1]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[10], tt[8], rr[1]))

    r[2] = t[10]
    rr[2] = tt[10]

    # p("vpunpckldq y{}, y{}, y{}".format(t[11], t[9], r[2]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[ 11], t[ 9], r [2]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[11], tt[9], rr[2]))
    
    r[3] = t[11]
    rr[3] = tt[11]

    # p("vpunpckhdq y{}, y{}, y{}".format(t[11], t[9], r[3]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[ 11], t[ 9], r[ 3]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[11], tt[9], rr[3]))

    r[4] = t[9]
    rr[4] = tt[9]

    # p("vpunpckldq y{}, y{}, y{}".format(t[14], t[12], r[4]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[ 14], t[ 12], r [4]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[14], tt[12], rr[4]))

    r[5] = t[12]
    rr[5] = tt[12]

    # p("vpunpckhdq y{}, y{}, y{}".format(t[14], t[12], r[5]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[ 14], t[ 12], r[ 5]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[14], tt[12], rr[5]))

    r[6] = t[14]
    rr[6] = tt[14]

    # p("vpunpckldq y{}, y{}, y{}".format(t[15], t[13], r[6]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[ 15], t[ 13], r [6]))
    p("vzip1q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[15], tt[13], rr[6]))

    r[7] = t[13]
    rr[7] = tt[13]

    # p("vpunpckhdq y{}, y{}, y{}".format(t[15], t[13], r[7]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(t[ 15], t[ 13], r[ 7]))
    p("vzip2q_s32 ((int32x4_t) y{}, (int32x4_t) y{}) = y{}".format(tt[15], tt[13], rr[7]))

    t[8] = t[15]
    tt[8] = tt[15]

    # p("vpunpcklqdq y{}, y{}, y{}".format(r[4], r[0], t[8]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[4], r[0], t[8]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[4], rr[0], tt[8]))

    t[9] = r[4]
    tt[9] = rr[4] 
    
    #p("vpunpckhqdq y{}, y{}, y{}".format(r[4], r[0], t[9]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[4], r[0], t[9]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[4], rr[0], tt[9]))

    t[10] = r[0]
    tt[10] = rr[0]

    # p("vpunpcklqdq y{}, y{}, y{}".format(r[5], r[1], t[10]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[ 5], r[ 1], t[ 10]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[5], rr[1], tt[10]))

    t[11] = r[5]
    tt[11] = rr[5]

    # p("vpunpckhqdq y{}, y{}, y{}".format(r[5], r[1], t[11]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[ 5], r[ 1], t[ 11]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[5], rr[1], tt[11]))


    t[12] = r[1]
    tt[12] = rr[1]

    # p("vpunpcklqdq y{}, y{}, y{}".format(r[6], r[2], t[12]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[ 6], r[ 2], t[ 12]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[6], rr[2], tt[12]))


    t[13] = r[6]
    tt[13] = rr[6]

    # p("vpunpckhqdq y{}, y{}, y{}".format(r[6], r[2], t[13]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[ 6], r[ 2], t[ 13]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[6], rr[2], tt[13]))


    t[14] = r[2]
    tt[14] = rr[2]
    # p("vpunpcklqdq y{}, y{}, y{}".format(r[7], r[3], t[14]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[ 7], r[ 3], t[ 14]))
    p("vzip1q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[7], rr[3], tt[14]))

    
    t[15] = r[7]
    tt[15] = rr[7]

    # p("vpunpckhqdq y{}, y{}, y{}".format(r[7], r[3], t[15]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(r[ 7], r[ 3], t[ 15]))
    p("vzip2q_s64 ((int64x2_t) y{}, (int64x2_t) y{}) = y{}".format(rr[7], rr[3], tt[15]))


    # now r[3] is free, t[7] is still in memory
    free = r[3]
    freee = rr[3]

    for i in range(7):  # t[7] is tricky
        # p("vinserti128 $1, %xmm{}, y{}, y{}".format(t[8+i], t[i], free))
        # No need to concat register, store directly
        
        # p("vmovdqa y{}, {}({})".format(free, 32*(dst_gap*i+dst_off), dst))
        p("vst1q_s16 ({}+{}, y{});".format( 16*(dst_gap*i+dst_off), dst, t[i]))
        p("vst1q_s16 ({}+{}, y{});".format( 16*(dst_gap*i+dst_off)+8, dst, t[8+i]))

    for i in range(7):  # t[7] still tricky
        # permute 78 [0b10, 0b11, 0b00, 0b01], 
        # p("vpermq ${}, y{}, y{}".format(int('01001110', 2), t[i], t[i]))
        # 4,3,2,1 -> 3, 4, 1, 2, swap high vs low
        p("y{} = y_free".format(t[i])) # store low
        p("y{} = y{}".format(t[i], tt[i])) # high <= low
        p("y_free = y{}".format(t[i])) # low <= y_free


    for i in range(8, 15):  # t[7] is tricky
        if dst_limit is None or i < dst_limit:
            #p("vinserti128 $0, %xmm{}, y{}, y{}".format(t[i-8], t[i], free))
            # No need to concat register 
            
            # p("vmovdqa y{}, {}({})".format(free, 32*(dst_gap*i+dst_off), dst))
            # store directly
            p("vst1q_s16 ({}+{}, y{});".format( 16*(dst_gap*i+dst_off), dst, t[i-8]))
            p("vst1q_s16 ({}+{}, y{});".format( 16*(dst_gap*i+dst_off)+8, dst, tt[i]))


    # p("vst1q_s16 ({}+{}, y{});".format(0, "rsp", t[7]))
    # p("vst1q_s16 ({}+{}, y{});".format(16, "rsp", tt[7]))
    # p("vmovdqa 0(%rsp), y{}".format(t[7]))
    p("vld1q_s16 ({} + {}) = y{}".format(0, "rsp" t[7]))
    p("vld1q_s16 ({} + {}) = y{}".format(16, "rsp" tt[7]))

    # p("vinserti128 $1, %xmm{}, y{}, y{}".format(t[15], t[7], t[14]))

    # store directly
    # p("vmovdqa y{}, {}({})".format(t[14], 32*(dst_gap*7+dst_off), dst))
    p("vst1q_s16 ({} + {}, y{});".format(16*(dst_gap*7+dst_off), dst, t[7]))
    p("vst1q_s16 ({} + {}, y{});".format(16*(dst_gap*7+dst_off) + 8, dst, t[15]))


    if dst_limit is None or 15 < dst_limit:
        # 
        # p("vpermq ${}, y{}, y{}".format(int('01001110', 2), t[7], t[7]))
        # p("vinserti128 $0, %xmm{}, y{}, y{}".format(t[7], t[15], t[15]))
        # p("vmovdqa y{}, {}({})".format(t[15], 32*(dst_gap*15+dst_off), dst))
        p("vst1q_s16 ({} + {}, y{});".format(16*(dst_gap*15+dst_off), dst, tt[7]))
        p("vst1q_s16 ({} + {}, y{});".format(16*(dst_gap*15+dst_off) + 8, dst, tt[15]))


def transpose_48x16_to_16x44(dst, src, src_off=0, dst_off=0):
    p("subq $32, %rsp")
    if src == '%rsp':
        src_off += 1
    if dst == '%rsp':
        dst_off += 1
    for n in range(3):
        dst_limit = 12 if n == 2 else None
        _transpose_16x16_to_16x16(dst, src, src_off=n+src_off,
                                  dst_off=dst_off+n*16,
                                  src_gap=3, dst_limit=dst_limit)
    p("addq $32, %rsp")


def transpose_16x96_to_96x16(dst, src, src_off=0, dst_off=0):
    """ It turns out to be tricky to make this 16x88 to 96x16 because of
        divisibility in 32-byte blocks. """
    p("subq $32, %rsp")
    if src == '%rsp':
        src_off += 1
    if dst == '%rsp':
        dst_off += 1
    for n in range(6):
        # artificially create a gap after every 44 coefficients
        # this is very useful when interpolating multiple outputs in Karatsuba
        gap44 = 0 if n < 3 else 4
        _transpose_16x16_to_16x16(dst, src, src_off=src_off+n*16-gap44, dst_off=dst_off+n,
                                  src_gap=1, dst_gap=6)
    p("addq $32, %rsp")


if __name__ == '__main__':
    p(".data")
    p(".section .rodata")
    p(".align 32")

    p(".text")
    p(".hidden transpose_48x16_to_16x44")
    p(".global transpose_48x16_to_16x44")
    p(".hidden transpose_48x16_to_16x44_stackbased")
    p(".global transpose_48x16_to_16x44_stackbased")
    p(".hidden transpose_16x96_to_96x16")
    p(".global transpose_16x96_to_96x16")
    p(".hidden transpose_16x96_to_96x16_stackbased")
    p(".global transpose_16x96_to_96x16_stackbased")
    p(".att_syntax prefix")

    p("transpose_48x16_to_16x44:")
    p("mov %rsp, %r8")  # Use r8 to store the old stack pointer during execution.
    p("andq $-32, %rsp")  # Align rsp to the next 32-byte value, for vmovdqa.

    transpose_48x16_to_16x44('%rdi', '%rsi')

    p("mov %r8, %rsp")
    p("ret")

    p("transpose_16x96_to_96x16:")
    p("mov %rsp, %r8")  # Use r8 to store the old stack pointer during execution.
    p("andq $-32, %rsp")  # Align rsp to the next 32-byte value, for vmovdqa.

    transpose_16x96_to_96x16('%rdi', '%rsi')

    p("mov %r8, %rsp")
    p("ret")

    p("transpose_48x16_to_16x44_stackbased:")
    p("mov %rsp, %r8")  # Use r8 to store the old stack pointer during execution.
    p("andq $-32, %rsp")  # Align rsp to the next 32-byte value, for vmovdqa.

    p("subq ${}, %rsp".format(32 * (37 + 44)))  # allocate some stack space
    dst_off = 37
    transpose_48x16_to_16x44(dst='%rsp', src='%rsi', dst_off=dst_off)
    for i in range(44):
        p("vmovdqa {}(%rsp), y0".format((i+dst_off)*32))
        p("vmovdqa y0, {}(%rdi)".format(i*32))

    p("mov %r8, %rsp")
    p("ret")

    p("transpose_16x96_to_96x16_stackbased:")
    p("mov %rsp, %r8")  # Use r8 to store the old stack pointer during execution.
    p("andq $-32, %rsp")  # Align rsp to the next 32-byte value, for vmovdqa.

    p("subq ${}, %rsp".format(32 * (11 + 96)))  # allocate some stack space
    src_off = 11
    for i in range(96):
        p("vmovdqa {}(%rsi), y0".format(i*32))
        p("vmovdqa y0, {}(%rsp)".format((i + src_off)*32))
    transpose_16x96_to_96x16(dst='%rdi', src='%rsp', src_off=src_off)

    p("mov %r8, %rsp")
    p("ret")
