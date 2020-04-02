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
p("y{} = vdupq_n_s16(0x0);".format(zero))
# x3 = 3
p("y{} = vdupq_n_u16(0x3);".format(x3))
# x33 = 3
p("y{} = vdupq_n_s16(0x3);".format(x33))
# MODQ = 4095 = 0xfff
p("y{} = vdupq_n_u16(0x1fff);".format(MODQ))
# xff 
p("y{} = vdupq_n_u16(0xff);".format(xff))
# xf 
p("y{} = vdupq_n_u16(0xf);".format(xf))

p("// Find Last")

# Load
p("y{} = vld1q_u16 ({} + {});".format(last, (NTRU_N32//8 - 1)*8, "a->coeffs"))

# last = MODQ(last)
p("y{} = vandq_u16 (y{}, y{});".format(last, MODQ, last))

# r = last >> logq1 = last >> 11
p("y{} = vshrq_n_u16 (y{}, {});".format(r[0], last, LOGQ-1))

# r = r ^ 3
p("y{} = veorq_u16 (y{}, y{});".format(r[0], x3, r[0]))

# r = r << 12
p("y{} = vshlq_n_u16 (y{}, {});".format(r[0], r[0], LOGQ))

# r = r + last
p("y{} = vaddq_u16 (y{}, y{});".format(r[0], r[0], last))

# Extract 
p("y{} = vdupq_laneq_u16 (y{}, {});".format(last, r[0], 5))

# last = last << 1
p("y{} = vshlq_n_u16 (y{}, {});".format(last, last, 1 ))

p("// Done Find Last")

for i in range(0, NTRU_N32 // 16):
    p("// {} -> {}".format(i*16, (i+1)*16))

    # Load
    p("y{} = vld1q_u16 ({} + {});".format(a[0], i*16, "a->coeffs"))
    p("y{} = vld1q_u16 ({} + {});".format(a[1], i*16 + 8, "a->coeffs"))
    # a = MODQ(a)
    p("y{} = vandq_u16 (y{}, y{});".format(a[0], MODQ, a[0]))
    p("y{} = vandq_u16 (y{}, y{});".format(a[1], MODQ, a[1]))
    # r = a >> LOGQ-1 
    p("y{} = vshrq_n_u16 (y{}, {});".format(r[0], a[0], LOGQ-1))
    p("y{} = vshrq_n_u16 (y{}, {});".format(r[1], a[1], LOGQ-1))
    # r = r ^ 3 
    p("y{} = veorq_u16 (y{}, y{});".format(r[0], x3, r[0]))
    p("y{} = veorq_u16 (y{}, y{});".format(r[1], x3, r[1]))
    # r = r << LOGQ 
    p("y{} = vshlq_n_u16 (y{}, {});".format(r[0], r[0], LOGQ ))
    p("y{} = vshlq_n_u16 (y{}, {});".format(r[1], r[1], LOGQ ))
    # r = r + a 
    p("y{} = vaddq_u16 (y{}, y{});".format(r[0], r[0], a[0]))
    p("y{} = vaddq_u16 (y{}, y{});".format(r[1], r[1], a[1]))
    # r = r + last
    p("y{} = vaddq_u16 (y{}, y{});".format(r[0], r[0], last))
    p("y{} = vaddq_u16 (y{}, y{});".format(r[1], r[1], last))
    # reval = mod3(r)
    
    p("// MOD3 ")
    mod3(r, retval, t, c, xff, xf, x33 ,length=2)
    p("// DONE MOD3 ")
    # Store retval 
    p("vst1q_u16 ({} + {}, y{});".format(i*16 , "r->coeffs"   , retval[0]))
    p("vst1q_u16 ({} + {}, y{});".format(i*16 + 8, "r->coeffs", retval[1]))

for i in range(NTRU_N, NTRU_N32):
    # 701
    # 702
    # 703
    p("r->coeffs[{}] = 0;".format(i))

p("}")