import monkeyhex


def flatten(l): return [item for sublist in l for item in sublist]


m = [list(range(8*i, 8*i+8)) for i in range(32)]


def transpose(r1, r2, size=1):
    # assert(len(r1) == len(r2) == 8)

    n1, n2 = [], []
    for i in range(int(len(r2)/(2*size))):

        # TODO: Insert NEON ASM HERE, depend on SIZE
        n1.insert(2*i, r1[2*i*size: 2*i*size + size])
        n1.insert(2*i + 1, r2[2*i*size: 2*i*size + size])
        n2.insert(2*i, r1[2*i*size + size: 2*i*size + 2*size])
        n2.insert(2*i + 1, r2[2*i*size + size: 2*i*size + 2*size])

    return flatten(n1), flatten(n2)


for i in range(0, len(m), 2):
    print(m[i], m[i+1])


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
    # for i in range(0, len(m)):
    #     print(m[i])
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

    n = transpose8x8(m[0:16:2])
    k = transpose8x8(m[16::2])
    o = transpose8x8(m[1:16:2])
    j = transpose8x8(m[17::2])

    n = zip(n, k)
    o = zip(o, j)

    n = flatten(n) + flatten(o )

    return n


print("============")
for i in transpose8x8(m[0:16:2]):
    print(i)

print("============")
for i in transpose8x8(m[1:16:2]):
    print(i)

print("============")
for i in transpose8x8(m[16::2]):
    print(i)

print("============")
for i in transpose8x8(m[17::2]):
    print(i)

print("============")
out = transpose16x16(m)
for i in range(0, len(out), 2):
    print(out[i], out[i+1])
