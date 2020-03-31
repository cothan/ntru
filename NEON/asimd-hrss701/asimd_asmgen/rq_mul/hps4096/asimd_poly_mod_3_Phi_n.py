from params import *
from asimd_mod3 import mod3

p = print

r = (0, 1)
retval = (2, 3)
t = (4, 5)
c = (6, 7)

x3 = 8

xf = 13
xff = 14
last = 15

p('#include "../../poly.h"')
p("#include <arm_neon.h>\n")

p("void poly_mod_3_Phi_n(poly *r){")

p(" uint16x8_t y0, y1, y2, y3; ")
p(" int16x8_t y4, y5, y6, y7, y8;")
p(" uint16x8_t y9, y10, y11, y12, y13, y14, y15; ")


# three = 3
p("vdupq_n_s16(0x3) = y{}".format(x3))
# xff 
p("vdupq_n_u16(0xff) = y{}".format(xff))
# xf 
p("vdupq_n_u16(0xf) = y{}".format(xf))

# Get last
p("vld1q_u16 ({} + {}) = y{}".format((NTRU_N32//8 - 1)*8, "r->coeffs", last))
# Extract 5th from last and duplicate all register
p("vdupq_laneq_u16 (y{}, {}) = y{}".format(last, 5, last))
# last = last << 1
p("vshlq_n_u16 (y{}, {}) = y{}".format(last, 1, last))

for i in range(0, NTRU_N32//16):
    p("// {} -> {}".format(i*16, (i+1)*16))
    # Load
    p("vld1q_u16 ({} + {}) = y{}".format(i*16, "r->coeffs", r[0]))
    p("vld1q_u16 ({} + {}) = y{}".format(i*16 + 8, "r->coeffs", r[1]))
    # r = r + last 
    p("vaddq_u16 (y{}, y{}) = y{}".format(r[0], last, r[0]))
    p("vaddq_u16 (y{}, y{}) = y{}".format(r[1], last, r[1]))
    # r = mod3(r)
    p("// MOD3 ")
    mod3(r, retval, t, c, xff, xf, x3, length=2)
    p("// DONE MOD3 ")
    p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , retval[0]))
    p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", retval[1]))

# 701 -> 704
for i in range(NTRU_N, NTRU_N32):
    # 701
    # 702
    # 703
    p("0 = r->coeffs[{}]".format(i))

p("}")

