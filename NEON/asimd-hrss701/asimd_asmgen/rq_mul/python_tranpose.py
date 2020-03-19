import monkeyhex


def flatten(l): return [item for sublist in l for item in sublist]

def transpose(r1, r2, size=1):
    # assert(len(r1) == len(r2) == 8)

    n1, n2 = [], []
    for i in range(int(len(r2)/(2*size))):

        n1.insert(2*i, r1[2*i*size: 2*i*size + size])
        n1.insert(2*i + 1, r2[2*i*size: 2*i*size + size])
        n2.insert(2*i, r1[2*i*size + size: 2*i*size + 2*size])
        n2.insert(2*i + 1, r2[2*i*size + size: 2*i*size + 2*size])

    return flatten(n1), flatten(n2)

def p(o):
    print("==========")
    for i in range(0, len(o), 2):
        if (i == 16):
            print("")
        print(o[i], o[i+1])



def transpose4x4x1(m):
    assert(len(m) == 4)
    n = [[] for i in range(len(m))]

    n[0], n[1] = transpose(m[0], m[1], 1)
    n[2], n[3] = transpose(m[2], m[3], 1)

    return n


def transpose4x4x2(m):
    assert(len(m) == 4)
    n = [[] for i in range(len(m))]

    n[0], n[1] = transpose(m[0], m[1], 2)
    n[2], n[3] = transpose(m[2], m[3], 2)
    # print(n[0], n[1])
    # print(n[2], n[3])

    n[0], n[2] = transpose(n[0], n[2], 2)
    n[1], n[3] = transpose(n[1], n[3], 2)

    n[1], n[2] = n[2], n[1]

    return n

def transpose4x4x4(m):
    assert(len(m) == 8)

    n = [[] for i in range(len(m))]

    n[0], n[1] = transpose(m[0], m[1], 4)
    n[2], n[3] = transpose(m[2], m[3], 4)

    n[4+0], n[4+1] = transpose(m[4+0], m[4+1], 4)
    n[4+2], n[4+3] = transpose(m[4+2], m[4+3], 4)

    return n[::2] + n[1::2]


def transpose8x8(m):
    print("m: {} -> {}".format(m[0], m[-1]))
    for i in range(0, len(m)):
        print("m{}: ".format(i), m[i])
    assert(len(m) == 8)
    n = range(4)
    o = range(4)

    n = transpose4x4x1(m[:4])
    n = transpose4x4x2(n)

    o = transpose4x4x1(m[4:])
    o = transpose4x4x2(o)

    input = (n[0], o[0], n[1], o[1], n[2], o[2], n[3], o[3])
    output = transpose4x4x4( input)

    return output

def transpose16x16(m):
    assert(len(m) == 32)

    n = range(8)
    o = range(8)
    k = range(8)
    j = range(8)

    print("========A1")
    n = transpose8x8(m[0:16:2])
    print("========A3")
    k = transpose8x8(m[16::2])
    print("========A2")
    o = transpose8x8(m[1:16:2])
    print("========A4")
    j = transpose8x8(m[17::2])

    n = zip(n, k)
    o = zip(o, j)

    n = flatten(n) + flatten(o )

    return n

m = [list(range(8*i, 8*i+8)) for i in range(192)]

# p(m[:32])
# p(transpose16x16(m[:32]))

def transpose48x16_to_16x44(m):
    assert(len(m) == 96)

    p(m[::3])
    print("==============")

    n = transpose16x16(m[::3])
    k = transpose16x16(m[1::3])
    o = transpose16x16(m[2::3])

    p(n)
    p(k)
    p(o)

    
transpose48x16_to_16x44(m[:96])

def transpose16x96_to_96x16(m):
    assert(len(m) == 192)

    for i in range(0, len(m), 32):
        print("==========")
        n = transpose16x16(m[i:i+32])
        p(n)

# transpose16x96_to_96x16(m)

