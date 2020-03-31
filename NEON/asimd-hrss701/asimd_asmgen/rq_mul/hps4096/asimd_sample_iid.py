from asimd_mod3 import mod3
from params import *
p = print

r = (0, 1)
retval = (2, 3)
x3 = 4 
xf = 5
xff = 6
t = (7, 8)
c = (9, 10)
zero = 11 

p('#include "../../sample.h"')
p("#include <arm_neon.h>\n")

p("void sample_iid(poly *r, const unsigned char uniformbytes[NTRU_SAMPLE_IID_BYTES]){")

p(" uint16x8_t y0, y1, y2, y3, y4, y5, y6; ")
p(" int16x8_t y7, y8, y9, y10; ")
p(" uint16x8_t y11, y12, y13, y14, y15; ")


# three = 3
p("y{} = vdupq_n_s16(0x3);".format(x3))
# xff 
p("y{} = vdupq_n_u16(0xff);".format(xff))
# xf 
p("y{} = vdupq_n_u16(0xf);".format(xf))
# 0 
p("y{} = vdupq_n_u16(0);".format(zero))


for i in range(NTRU_N32//16):
    p("// {} -> {}".format(i*16, (i+1)*16))
    p("y{} = vld1q_u16 ({} + {});".format(r[0], i*16, "uniformbytes"))
    p("y{} = vld1q_u16 ({} + {});".format(r[1], i*16 + 8, "uniformbytes"))
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
    p("r->coeffs[{}] = 0;".format(i))

p("}")
