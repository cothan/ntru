from params import *

p = print

r = (0, 1)
last = 2
zero = 3

p(' #include "../../poly.h"')
p("#include <arm_neon.h>\n")

p("void poly_mod_q_Phi_n(poly *r){")

p(" uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7; ")

# 0 
p("y{} = vdupq_n_u16(0);".format(zero))


# Get last
p("y{} = vld1q_u16 ({} + {});".format(last, (NTRU_N32//8 - 1)*8, "r->coeffs"))
# Extract 5th from last and duplicate all register
p("y{} = vdupq_laneq_u16 (y{}, {});".format(last, last, 5))

for i in range(0, NTRU_N32//16):
    p("// {} -> {}".format(i*16, (i+1)*16))
    # Load
    p("y{} = vld1q_u16 ({} + {});".format(r[0], i*16, "r->coeffs"))
    p("y{} = vld1q_u16 ({} + {});".format(r[1], i*16 + 8, "r->coeffs"))
    # r = r - last 
    p("y{} = vsubq_u16 (y{}, y{});".format(r[0], r[0], last))
    p("y{} = vsubq_u16 (y{}, y{});".format(r[1], r[1], last))
    
    p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , r[0]))
    p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", r[1]))

# 701 -> 704
for i in range(NTRU_N, NTRU_N32):
    # 701
    # 702
    # 703
    p("r->coeffs[{}] = 0;".format(i))

p("}")

