from asimd_mod3 import mod3
from params import *
p = print


LOGQ = 0
while 2**LOGQ < NTRU_Q: LOGQ += 1


"""
  33   │ void poly_Rq_to_S3(poly *r, const poly *a)
  34   │ {
  35   │   /* NOTE: Assumes input is in [0,Q-1]^N */
  36   │   /*       Produces output in {0,1,2}^N */
  37   │   int i;
  38   │
  39   │   /* Center coeffs around 3Q: [0, Q-1] -> [3Q - Q/2, 3Q + Q/2) */
  40   │   for(i=0; i<NTRU_N; i++)
  41   │   {
  42   │     r->coeffs[i] = ((MODQ(a->coeffs[i]) >> (NTRU_LOGQ-1)) ^ 3) << NTRU_LOGQ;
  43   │     r->coeffs[i] += MODQ(a->coeffs[i]);
  44   │   }
  45   │
  22   │   for(i=0; i <NTRU_N; i++)
  23   │     r->coeffs[i] = mod3(r->coeffs[i] + 2*r->coeffs[NTRU_N-1]);
  47   │ }
  48   │

"""




r = (0, 1)
a = (2, 3)
t = (4, 5)
c = (6, 7)
x3 = 8
last = 9
MODQ = 10
retval = (11, 12)
xff, xf = 13, 14
zero = 15
x33 = 16

p('#include "../../poly.h"')
p("#include <arm_neon.h>\n")

p("void poly_Rq_to_S3(poly *r, const poly *a){")

p(" uint16x8_t y0, y1, y2, y3; ")
p(" int16x8_t y4, y5, y6, y7, y16;")
p(" uint16x8_t y8, y9, y10, y11, y12, y13, y14, y15; ")



# zero 
p("vdupq_n_s16(0x0) = y{}".format(zero))
# x3 = 3
p("vdupq_n_u16(0x3) = y{}".format(x3))
# x33 = 3
p("vdupq_n_s16(0x3) = y{}".format(x33))
# MODQ = 4095 = 0xfff
p("vdupq_n_u16(0xfff) = y{}".format(MODQ))
# xff 
p("vdupq_n_u16(0xff) = y{}".format(xff))
# xf 
p("vdupq_n_u16(0xf) = y{}".format(xf))

p("// Find Last")

# Load
p("vld1q_u16 ({} + {}) = y{}".format((NTRU_N32//16 - 1)*16, "a->coeffs", last))

# last = MODQ(last)
p("vandq_u16 (y{}, y{}) = y{}".format(MODQ, last, last))

# r = last >> logq1 = last >> 11
p("vshrq_n_u16 (y{}, {}) = y{}".format(last, LOGQ-1, r[0]))

# r = r ^ 3
p("veorq_u16 (y{}, y{}) = y{}".format(x3, r[0], r[0]))

# r = r << 12
p("vshlq_n_u16 (y{}, {}) = y{}".format(r[0], LOGQ, r[0]))

# r = r + last
p("vaddq_u16 (y{}, y{}) = y{}".format(r[0], last, r[0]))

# Extract 
p("vdupq_laneq_u16 (y{}, {}) = y{}".format(last, 5, last))

# last = last << 1
p("vshlq_n_u16 (y{}, {}) = y{}".format(last, 1, last))

p("// Done Find Last")

for i in range(0, NTRU_N32 // 16):
    p("// {} -> {}".format(i*16, (i+1)*16))
    if i == NTRU_N32//16 - 1:
        # Load
        p("vld1q_u16 ({} + {}) = y{}".format(i*16, "a->coeffs", a[0]))

        # a = MODQ(a)
        p("vandq_u16 (y{}, y{}) = y{}".format(MODQ, a[0], a[0]))

        # r = a >> LOGQ-1 
        p("vshrq_n_u16 (y{}, {}) = y{}".format(a[0], LOGQ-1, r[0]))

        # r = r ^ 3 
        p("veorq_u16 (y{}, y{}) = y{}".format(x3, r[0], r[0]))

        # r = r << LOGQ 
        p("vshlq_n_u16 (y{}, {}) = y{}".format(r[0], LOGQ, r[0]))

        # r = r + a 
        p("vaddq_u16 (y{}, y{}) = y{}".format(r[0], a[0], r[0]))

        # r = r + last
        p("vaddq_u16 (y{}, y{}) = y{}".format(r[0], last, r[0]))

        # reval = mod3(r)
        
        p("// MOD3 ")
        mod3(r, retval, t, c, xff, xf, x33 ,length=1)
        p("// DONE MOD3 ")
        # Store retval 
        p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , retval[0]))
        p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", zero))

    else:
        # Load
        p("vld1q_u16 ({} + {}) = y{}".format(i*16, "a->coeffs", a[0]))
        p("vld1q_u16 ({} + {}) = y{}".format(i*16 + 8, "a->coeffs", a[1]))
        # a = MODQ(a)
        p("vandq_u16 (y{}, y{}) = y{}".format(MODQ, a[0], a[0]))
        p("vandq_u16 (y{}, y{}) = y{}".format(MODQ, a[1], a[1]))
        # r = a >> LOGQ-1 
        p("vshrq_n_u16 (y{}, {}) = y{}".format(a[0], LOGQ-1, r[0]))
        p("vshrq_n_u16 (y{}, {}) = y{}".format(a[1], LOGQ-1, r[1]))
        # r = r ^ 3 
        p("veorq_u16 (y{}, y{}) = y{}".format(x3, r[0], r[0]))
        p("veorq_u16 (y{}, y{}) = y{}".format(x3, r[1], r[1]))
        # r = r << LOGQ 
        p("vshlq_n_u16 (y{}, {}) = y{}".format(r[0], LOGQ, r[0]))
        p("vshlq_n_u16 (y{}, {}) = y{}".format(r[1], LOGQ, r[1]))
        # r = r + a 
        p("vaddq_u16 (y{}, y{}) = y{}".format(r[0], a[0], r[0]))
        p("vaddq_u16 (y{}, y{}) = y{}".format(r[1], a[1], r[1]))
        # r = r + last
        p("vaddq_u16 (y{}, y{}) = y{}".format(r[0], last, r[0]))
        p("vaddq_u16 (y{}, y{}) = y{}".format(r[1], last, r[1]))
        # reval = mod3(r)
        
        p("// MOD3 ")
        mod3(r, retval, t, c, xff, xf, x33 ,length=2)
        p("// DONE MOD3 ")
        # Store retval 
        p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , retval[0]))
        p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", retval[1]))

for i in range(NTRU_N, NTRU_N32 - 8):
    # 821
    # 822
    # 823
    p("0 = r->coeffs[{}]".format(i))

p("}")