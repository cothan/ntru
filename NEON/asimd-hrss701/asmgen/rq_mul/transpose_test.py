import pysnooper
import itertools

src = range(16*16)


# @pysnooper.snoop()
def interleave(a, b, size=2, low=True):
    # Interleave c = a | b
    length = int(len(a)/size)
    c = [0] * length
    i = 0
    if low == True:
        # Interleave low
        while i < int(length/size):
            for j in range(0, size, 2):
                c[size*i + j] = a[size*i:size*i+size]
            for j in range(0, size, 2):
                c[size*i + j + 1] = b[size*i:size*i+size]
            i += 1
    else:
        # Interleave high
        a = a[int(length/2):]
        b = b[int(length/2):]
        while i < int(length/size):
            for j in range(0, size, 2):
                c[size*i + j] = a[size*i:size*i+size]
                c[size*i + j + 1] = b[size*i:size*i+size]
            i += 1

    return list(itertools.chain.from_iterable(c))

def interleave_8(a, b, size=8, low=True):
    # Interleave c = a | b
    length = int(len(a)/size)
    c = [0] * length
    i = 0
    if low == True:
        # Interleave low
        for j in range(0, size, 2):
            c[size*i + j] = a[size*i:size*i+size]
            c[size*i + j + 1] = b[size*i:size*i+size]

    else:
        # Interleave high
        a = a[int(length/2):]
        b = b[int(length/2):]

        for j in range(0, size, 2):
            c[size*i + j] = a[size*i:size*i+size]
            c[size*i + j + 1] = b[size*i:size*i+size]


    return list(itertools.chain.from_iterable(c))

def transpose_16x16_to_16x16(src, src_off=0, dst_off=0, src_gap=3, dst_gap=1, dst_limit=None):
    s = [0, None, 1, None, 2, None, 3, None]
    s[0] = src[32*(src_gap*(0*2)+src_off): 32*(src_gap*(0*2)+src_off) + 32]
    s[2] = src[32*(src_gap*(1*2)+src_off): 32*(src_gap*(1*2)+src_off) + 32]
    s[4] = src[32*(src_gap*(2*2)+src_off): 32*(src_gap*(2*2)+src_off) + 32]
    s[6] = src[32*(src_gap*(3*2)+src_off): 32*(src_gap*(3*2)+src_off) + 32]

    assert len(s[0]) == len(s[2]) == len(s[4]) == len(s[6])

    t = list(range(4, 12)) + [None] * 8

    t[0] = interleave(src[32*(src_gap*1+src_off): 32 *
                          (src_gap*1+src_off) + 32], s[0], size=2, low=True)
    t[1] = interleave(src[32*(src_gap*1+src_off): 32 *
                          (src_gap*1+src_off) + 32], s[0], size=2, low=False)
    t[2] = interleave(src[32*(src_gap*3+src_off): 32 *
                          (src_gap*3+src_off) + 32], s[2], size=2, low=True)
    t[3] = interleave(src[32*(src_gap*3+src_off): 32 *
                          (src_gap*3+src_off) + 32], s[2], size=2, low=False)
    t[4] = interleave(src[32*(src_gap*5+src_off): 32 *
                          (src_gap*5+src_off) + 32], s[4], size=2, low=True)
    t[5] = interleave(src[32*(src_gap*5+src_off): 32 *
                          (src_gap*5+src_off) + 32], s[4], size=2, low=False)
    t[6] = interleave(src[32*(src_gap*7+src_off): 32 *
                          (src_gap*7+src_off) + 32], s[6], size=2, low=True)
    t[7] = interleave(src[32*(src_gap*7+src_off): 32 *
                          (src_gap*7+src_off) + 32], s[6], size=2, low=False)

    r = list(range(0, 4)) + list(range(12, 16))

    r[0] = interleave(t[2], t[0], size=4, low=True)
    r[1] = interleave(t[2], t[0], size=4, low=False)
    r[2] = interleave(t[3], t[1], size=4, low=True)
    r[3] = interleave(t[3], t[1], size=4, low=False)
    r[4] = interleave(t[6], t[4], size=4, low=True)
    r[5] = interleave(t[6], t[4], size=4, low=False)
    r[6] = interleave(t[7], t[5], size=4, low=True)
    r[7] = interleave(t[7], t[5], size=4, low=False)

    t[0] = interleave_8(r[4], r[0], size=8, low=True)
    t[1] = interleave_8(r[4], r[0], size=8, low=False)
    t[2] = interleave_8(r[5], r[1], size=8, low=True)
    t[3] = interleave_8(r[5], r[1], size=8, low=False)
    t[4] = interleave_8(r[6], r[2], size=8, low=True)
    t[5] = interleave_8(r[6], r[2], size=8, low=False)
    t[6] = interleave_8(r[7], r[3], size=8, low=True)
    t[7] = interleave_8(r[7], r[3], size=8, low=False)
    
    print(r[0])

    return None


transpose_16x16_to_16x16(range(32*32))
