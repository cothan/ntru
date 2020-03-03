p = print

from params import *
from asimd_mod3 import mod3

LOGQ = 0
while 2**LOGQ < NTRU_Q: LOGQ +=1


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

if __name__ == '__main__':
    p(".data")
    p(".section .rodata")
    p(".align 32")

    p("const_3_repeating:")
    for i in range(16):
        p(".word 0x3")

    p("shuf_b8_to_low_doubleword:")
    for j in range(16):
        p(".byte 8")
        p(".byte 255")

    p("mask_modq:")
    for i in range(16):
        p(".word {}".format(NTRU_Q-1))


    p(".text")
    p(".hidden poly_Rq_to_S3")
    p(".global poly_Rq_to_S3")
    p(".att_syntax prefix")

    p("poly_Rq_to_S3:")

    r = (0, 1)
    a = (2, 3)
    threes = 4
    
    last = (6, 7)
    retval = (8, 9)
    modq = 10
    

    
    
    # three = 3 
    p("vdupq_n_u16(0x3) = y{}".format(threes))
    # modq = 4095 = 0xfff
    p("vdupq_n_u16(0xfff) = y{}".format(modq))
    
    # Load 
    p("vld1q_u16 ({} + {}) = y{}".format( (NTRU_N32//16 - 2)*16, "a->coeffs", last[0])
    p("vld1q_u16 ({} + {}) = y{}".format( (NTRU_N32//16 - 1)*16, "a->coeffs", last[1])
    # last = modQ(last)
    p("vandq_u16 (y{}, y{}) = y{}".format(modq, last[0], last[0]))
    p("vandq_u16 (y{}, y{}) = y{}".format(modq, last[1], last[1]))

    # r = last >> logq1 = last >> 11
    p("vshrq_n_u16 (y{}, {}) = y{}".format(last[0], LOGQ-1, r[0])) 
    p("vshrq_n_u16 (y{}, {}) = y{}".format(last[1], LOGQ-1, r[1])) 

    # r = r ^ 3 
    p("veorq_u16 (y{}, y{}) = y{}".format(threes, r[0], r[0]))
    p("veorq_u16 (y{}, y{}) = y{}".format(threes, r[1], r[1]))


    # r = r << 12
    p("vshlq_n_u16 (y{}, {}) = y{}".format(r[0], LOGQ, r[0]))
    p("vshlq_n_u16 (y{}, {}) = y{}".format(r[1], LOGQ, r[1]))

    # r = r + last 
    p("vaddq_u16 (y{}, y{}) = y{}".format( r[0], last[0], r[0])) 
    p("vaddq_u16 (y{}, y{}) = y{}".format( r[1], last[1], r[1])) 

    mod3(last, retval)
    #retval = mod3(last )

    # p("vpsllw $1, %ymm{}, %ymm{}".format(retval, last))
    p("vshlq_n_u16 (y{}, 1) = y{}".format(retval[0], last[0]))
    p("vshlq_n_u16 (y{}, 1) = y{}".format(retval[1], last[1]))

    # Drop last[0]
    # p("vextracti128 $1, %ymm{}, %xmm{}".format(last, last))

    # TODO: extract last individually.

    p("vpshufb shuf_b8_to_low_doubleword(%rip), %ymm{}, %ymm{}".format(last, last))
    
    
    p("vinserti128 $1, %xmm{}, %ymm{}, %ymm{}".format(last, last, last))

    for i in range(NTRU_N32 // 16):
        p("vmovdqa {}(%rsi), %ymm{}".format(i*32, a))
        p("vpand %ymm{}, %ymm{}, %ymm{}".format(modq, a, a));
        p("vpsrlw ${}, %ymm{}, %ymm{}".format(LOGQ-1, a, r))
        p("vpxor %ymm{}, %ymm{}, %ymm{}".format(threes, r, r))
        p("vpsllw ${}, %ymm{}, %ymm{}".format(LOGQ, r, r))
        p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(a, r, r))
        p("vpaddw %ymm{}, %ymm{}, %ymm{}".format(last, r, r))
        mod3(r, retval)
        p("vmovdqa %ymm{}, {}(%rdi)".format(retval, i*32))

    p("ret")
