from params import *

p = print

r = (0, 1)
last = 2
zero = 3

p("#include <arm_neon.h>\n")

p("void poly_mod_q_Phi_n(poly *r){")

p(" uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7; ")

# 0 
p("vdupq_n_u16(0) = y{}".format(zero))


# Get last
p("vld1q_u16 ({} + {}) = y{}".format((NTRU_N32//16 - 1)*16, "r->coeffs", last))
# Extract 5th from last and duplicate all register
p("vdupq_laneq_u16 (y{}, {}) = y{}".format(last, 5, last))

for i in range(0, NTRU_N32//16):
    p("// {} -> {}".format(i*16, (i+1)*16))
    if i == NTRU_N32//16 - 1:
        # Load
        p("vld1q_u16 ({} + {}) = y{}".format(i*16, "r->coeffs", r[0]))
        # r = r - last 
        p("vsubq_u16 (y{}, y{}) = y{}".format(r[0], last, r[0]))
        
        p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , r[0]))
    else:
        # Load
        p("vld1q_u16 ({} + {}) = y{}".format(i*16, "r->coeffs", r[0]))
        p("vld1q_u16 ({} + {}) = y{}".format(i*16 + 8, "r->coeffs", r[1]))
        # r = r - last 
        p("vsubq_u16 (y{}, y{}) = y{}".format(r[0], last, r[0]))
        p("vsubq_u16 (y{}, y{}) = y{}".format(r[1], last, r[1]))
        
        p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , r[0]))
        p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", r[1]))

# 824 -> 832
p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", zero))
for i in range(NTRU_N, NTRU_N32 - 8):
    # 821
    # 822
    # 823
    p("0 = r->coeffs[{}]".format(i))

p("}")

