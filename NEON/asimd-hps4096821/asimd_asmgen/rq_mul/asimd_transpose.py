p = print

def vload(dst, address, src):
    p("y{} = vld1q_u16({} + {});".format(dst, address, src))

def vstore(address, dst, src):
    p("vst1q_u16({} + {}, y{});".format(address, dst, src))


def flatten(l): return [item for sublist in l for item in sublist]


def transpose(t1, t2, r1, r2, size=1):
    if size == 1:
        print("y{} = vtrn1q_u16(y{}, y{});".format(t1, r1, r2))
        print("y{} = vtrn2q_u16(y{}, y{});".format(t2, r1, r2))
        pass
    elif size == 2:
        print("y{} = vtrn1q_u32(y{}, y{});".format(t1, r1, r2))
        print("y{} = vtrn2q_u32(y{}, y{});".format(t2, r1, r2))
        pass
    elif size == 4:
        print("y{} = vtrn1q_u64(y{}, y{});".format(t1, r1, r2))
        print("y{} = vtrn2q_u64(y{}, y{});".format(t2, r1, r2))
        pass
    else:
        assert(False)


def transpose4x4x1(t, r):
    assert(len(t) == len(r) == 4)
    assert(list(set(t).intersection(r)) == [])
    transpose(t[0], t[1], r[0], r[1], 1)
    transpose(t[2], t[3], r[2], r[3], 1)


def transpose4x4x2(n, m, t):
    assert(len(n) == len(m) == 4)
    assert(len(t) == 4)
    assert(list(set(t).intersection(m)) == [])
    assert(list(set(n).intersection(t)) == [])

    transpose(t[0], t[1], m[0], m[1], 2)
    transpose(t[2], t[3], m[2], m[3], 2)

    transpose(n[0], n[2], t[0], t[2], 2)
    transpose(n[1], n[3], t[1], t[3], 2)

    n = n[0], n[2], n[1], n[3]

    return n


def transpose4x4x4(n, m):
    assert(len(m) == len(n) == 8)
    assert(list(set(n).intersection(m)) == [])

    transpose(n[0], n[1], m[0], m[1], 4)
    transpose(n[2], n[3], m[2], m[3], 4)

    transpose(n[4 + 0], n[4 + 1], m[4 + 0], m[4 + 1], 4)
    transpose(n[4 + 2], n[4 + 3], m[4 + 2], m[4 + 3], 4)

    n = n[::2] + n[1::2]

    return n


def transpose8x8(o, n, m, t):
    assert(len(n) == len(m) == 8)
    assert(list(set(o).intersection(m)) == [])
    assert(list(set(n).intersection(o)) == [])
    assert(list(set(o).intersection(t)) == [])

    assert(len(o) == 8)
    assert(len(t) == 4)

    transpose4x4x1(o[:4], m[:4])
    tmp_n_03 = transpose4x4x2(n[:4], o[:4], t)

    transpose4x4x1(o[:4], m[4:])
    tmp_n_47 = transpose4x4x2(n[4:], o[:4], t)

    n = flatten(list(zip(tmp_n_03, tmp_n_47)))

    o = transpose4x4x4(o, n)

    return o


def load_8(dst, src, srcoff=0, src_gap=1, length=8):
    for i in range(length):
        vload(dst[i], src,   16*(src_gap*i) + srcoff)


def store_8(dst, src, dstoff=0, dst_gap=1, length=8):
    for i in range(0, length):
        vstore(dst,16*(i*dst_gap) + dstoff, src[i])


def transpose16x16_2(dst, src, dstoff=0, srcoff=0, src_gap=1, dst_gap=1, length=8, dst_limit = None):
    i = 0
    m = list(range(i, i + 8))
    i += 8
    n = list(range(i, i+8))
    i += 8
    o = list(range(i, i + 8))
    i += 8
    t = list(range(i, i + 4))
    i += 4
    u = list(range(i, i+8))
    i += 8

    # A1
    p("// 16x16: LD A1")
    load_8(m, src,  srcoff, src_gap)
    p("// Transpose 8x8")
    o = transpose8x8(o, n, m, t)
    p("// 16x16: STR A1")
    store_8(dst, o, dstoff, dst_gap)

    # # A4
    p("// 16x16: LD A4")
    load_8(m, src, 136*src_gap + srcoff, src_gap)
    p("// Transpose 8x8")
    o = transpose8x8(o, n, m, t)
    p("// 16x16: STR A4")
    store_8(dst, o, 128*dst_gap + dstoff + 8, dst_gap, length)

    # A2
    p("// 16x16: LD A2")
    load_8(m, src, 8*src_gap + srcoff, src_gap)
    p("// Transpose 8x8")
    o = transpose8x8(o, n, m, t)

    # # A3
    p("// 16x16: LD A3")
    load_8(m, src, 128*src_gap + srcoff, src_gap)
    p("// Transpose 8x8")
    u = transpose8x8(u, n, m, t)

    # store A3 to A2
    p("// 16x16: STR A2<-A3")
    store_8(dst, u, 8 + dstoff, dst_gap)

    # store A2 to A3
    p("// 16x16: STR A3<-A2")
    store_8(dst, o, 128*dst_gap + dstoff, dst_gap, length)


def transpose_64x16_to_16x52(dst, src, src_off=0, dst_off=0):
    if src == "rsp":
        src_off += 1
    if dst == "rsp":
        dst_off += 1

    for n in range(4):
        dst_limit = 4 if n == 3 else None
        transpose16x16_2(dst, src, dstoff=dst_off + n*16, srcoff=n +
                         src_off, src_gap=4, dst_gap=1, dst_limit=dst_limit)


def transpose_16x128_to_128x16(dst, src, src_off=0, dst_off=0):
    if src == "rsp":
        src_off += 1
    if dst == "rsp":
        dst_off += 1

    for n in range(9):
        if n < 6:
            l = 8
        else:
            l = 4
        gap52 = 0 if n < 4 else 12
        p("// -------------- n = {}".format(n))
        transpose16x16_2(dst, src, dstoff=dst_off + n, srcoff=src_off+n*16-gap52, src_gap=1, dst_gap=8, length=l)


# TODO: test transpose 