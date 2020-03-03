p = print


def mod3(a, r=13, t=14, c=15, length=2):
    # R is output
    A = []
    R = []
    T = []
    C = []
    # A[0] is low, A[1] is high
    # R[0] is low, R[1] is high
    for i in range(length):
        A.append(a[i])
        R.append(r[i])
        T.append(t[i])
        C.append(c[i])
    # r = (a >> 8) + (a & 0xff); // r mod 255 == a mod 255

    p("vdupq_n_u16(0xff) = y{}".format(T[0]))
    for i in range(length):
        # R = a >> 8
        p("vshrq_n_u16 (y{}, {}) = y{}".format(A[i], 8, R[i]))
        # A = a & 0xff
        p("vandq_u16 (y{}, y{}) = y{}".format(A[i], T[0], A[i]))
        # R = A + R
        p("vaddq_u16 (y{}, y{}) = y{}".format(A[i], R[i], R[i]))

    # p("vpsrlw $8, %ymm{}, %ymm{}".format(a, r))
    # p("vpand mask_ff(%rip), %ymm{}, %ymm{}".format(a, a))
    # p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(r, a, r))

    # r = (r >> 4) + (r & 0xf); // r' mod 15 == r mod 15

    p("vdupq_n_u16(0xf) = y{}".format(T[0]))
    for i in range(length):
        # A = r >> 4
        p("vshrq_n_u16 (y{}, {}) = y{}".format(R[i], 4, A[i]))
        # R = r & 0xf
        p("vandq_u16 (y{}, y{}) = y{}".format(R[i], T[0], R[i]))
        # R = A + R
        p("vaddq_u16 (y{}, y{}) = y{}".format(A[i], R[i], R[i]))

    # p("vpand mask_f(%rip), %ymm{}, %ymm{}".format(r, a))
    # p("vpsrlw $4, %ymm{}, %ymm{}".format(r, r))
    # p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(r, a, r))

    # r = (r >> 2) + (r & 0x3); // r' mod 3 == r mod 3
    # r = (r >> 2) + (r & 0x3); // r' mod 3 == r mod 3
    p("vdupq_n_u16(0x3) = y{}".format(T[0]))
    for _ in range(2):
        for i in range(length):
            # A = r >> 2
            p("vshrq_n_u16 (y{}, {}) = y{}".format(R[i], 2, A[i]))
            # R = r & 0x3
            p("vandq_u16 (y{}, y{}) = y{}".format(R[i], T[0], R[i]))
            # R = A + R
            p("vaddq_u16 (y{}, y{}) = y{}".format(A[i], R[i], R[i]))

    # p("vpand mask_3(%rip), %ymm{}, %ymm{}".format(r, a))
    # p("vpsrlw $2, %ymm{}, %ymm{}".format(r, r))
    # p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(r, a, r))

    #   t = r - 3;
    # p("vpsubw mask_3(%rip), %ymm{}, %ymm{}".format(r, t))
    # for i in range(length):
    if length == 2:
        p("vsubq_s16 (y{}, y{}) = y{}".format(R[1], T[0], T[1]))
        p("vsubq_s16 (y{}, y{}) = y{}".format(R[0], T[0], T[0]))
    else:
        p("vsubq_s16 (y{}, y{}) = y{}".format(R[0], T[0], T[0]))

    #   c = t >> 15;  t is signed, so shift arithmetic
    # p("vpsraw $15, %ymm{}, %ymm{}".format(t, c))
    for i in range(length):
        p("vshrq_n_s16 (y{}, {}) = y{}".format(T[i], 15, C[i]))
    # p("vshrq_n_s16 (y{}, {}) = y{}".format(T[1], 15, C[1]))

    #   return (c&r) ^ (~c&t);
    for i in range(length):
        # A = C & R
        p("vandq_u16 (y{}, y{}) = y{}".format(C[i], R[i], A[i]))
        # C = ~C
        p("vmvnq_s16 (y{}) = y{}".format(C[i], C[i]))
        # T = C & T
        p("vandq_u16 (y{}, y{}) = y{}".format(C[i], T[i], T[i]))
        # R = A ^ T
        p("veorq_u16 (y{}, y{}) = y{}".format(A[i], T[i], R[i]))

    # p("vpandn %ymm{}, %ymm{}, %ymm{}".format(t, c, a))
    # p("vpand %ymm{}, %ymm{}, %ymm{}".format(c, r, t))
    # p("vpxor %ymm{}, %ymm{}, %ymm{}".format(t, a, r))
