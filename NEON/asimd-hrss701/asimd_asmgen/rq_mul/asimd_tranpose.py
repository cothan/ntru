p = print


"""
1. Load 32 registers 
2. Tranpose
3. Store it back 
"""

"""
Input: r1, r2
Output: t1, t2 
"""


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


def load_8(dst, src, start=0):
    for i in range(8):
        p("y{} = vld1q_u16({} + {});".format(dst[i], src, i*16 + start))


def store_8(dst, src, start=8):
    for i in range(8):
        p("vst1q_u16({} + {}, y{});".format(dst, i*16 + start, src[i]))


def transpose16x16(dst, src):
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

    

    load_8(m, "r->coeffs", start=0 + src)
    o = transpose8x8(o, n, m, t)
    store_8("r->coeffs", o, start=0 + dst)

    load_8(m, "r->coeffs", start=136 + src)
    o = transpose8x8(o, n, m, t)
    store_8("r->coeffs", o, start=136 + dst)

    load_8(m, "r->coeffs", start=8 + src)
    o = transpose8x8(o, n, m, t)

    load_8(m, "r->coeffs", start=128 + src)
    u = transpose8x8(u, n, m, t)

    store_8("r->coeffs", u, start=8 + dst)
    store_8("r->coeffs", o, start=128 + dst)


transpose16x16(0, 0)
