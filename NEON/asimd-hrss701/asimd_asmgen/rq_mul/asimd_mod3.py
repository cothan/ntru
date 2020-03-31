p = print


def mod3(a, r, t, c, xff, xf, x3, length):
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

    # p("vdupq_n_u16(0xff) = y{}".format(T[0]))
    for i in range(length):
        # R = a >> 8
        p("y{} = vshrq_n_u16 (y{}, {});".format(R[i], A[i], 8))
        # A = a & 0xff
        p("y{} = vandq_u16 (y{}, y{});".format(A[i], A[i], xff))
        # R = A + R
        p("y{} = vaddq_u16 (y{}, y{});".format(R[i], A[i], R[i]))

    # p("vpsrlw $8, %ymm{}, %ymm{}".format(a, r))
    # p("vpand mask_ff(%rip), %ymm{}, %ymm{}".format(a, a))
    # p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(r, a, r))

    # r = (r >> 4) + (r & 0xf); // r' mod 15 == r mod 15

    # p("vdupq_n_u16(0xf) = y{}".format(T[0]))
    for i in range(length):
        # A = r >> 4
        p("y{} = vshrq_n_u16 (y{}, {});".format(A[i], R[i], 4))
        # R = r & 0xf
        p("y{} = vandq_u16 (y{}, y{});".format(R[i], R[i], xf))
        # R = A + R
        p("y{} = vaddq_u16 (y{}, y{});".format(R[i], A[i], R[i]))

    # p("vpand mask_f(%rip), %ymm{}, %ymm{}".format(r, a))
    # p("vpsrlw $4, %ymm{}, %ymm{}".format(r, r))
    # p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(r, a, r))

    # r = (r >> 2) + (r & 0x3); // r' mod 3 == r mod 3
    # r = (r >> 2) + (r & 0x3); // r' mod 3 == r mod 3
    # p("vdupq_n_u16(0x3) = y{}".format(T[0]))
    for _ in range(2):
        for i in range(length):
            # A = r >> 2
            p("y{} = vshrq_n_u16 (y{}, {});".format(A[i], R[i], 2))
            # R = r & 0x3
            p("y{} = vandq_u16 (y{}, y{});".format(R[i], R[i], x3))
            # R = A + R
            p("y{} = vaddq_u16 (y{}, y{});".format(R[i], A[i], R[i]))

    # p("vpand mask_3(%rip), %ymm{}, %ymm{}".format(r, a))
    # p("vpsrlw $2, %ymm{}, %ymm{}".format(r, r))
    # p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(r, a, r))

    #   t = r - 3;
    for i in range(length):
        p("y{} = vsubq_s16 (y{}, y{});".format(T[i], R[i], x3))

    #   c = t >> 15;  t is signed, so shift arithmetic
    for i in range(length):
        p("y{} = vshrq_n_s16 (y{}, {});".format(C[i], T[i], 15))

    #   return (c&r) ^ (~c&t);
    for i in range(length):
        # A = C & R
        p("y{} = vandq_u16 (y{}, y{});".format(A[i], C[i], R[i]))
        # C = ~C
        p("y{} = vmvnq_s16 (y{});".format(C[i], C[i]))
        # T = C & T
        p("y{} = vandq_s16 (y{}, y{});".format(T[i], C[i], T[i]))
        # R = A ^ T
        p("y{} = veorq_u16 (y{}, y{});".format(R[i], A[i], T[i]))

    # p("vpandn %ymm{}, %ymm{}, %ymm{}".format(t, c, a))
    # p("vpand %ymm{}, %ymm{}, %ymm{}".format(c, r, t))
    # p("vpxor %ymm{}, %ymm{}, %ymm{}".format(t, a, r))


