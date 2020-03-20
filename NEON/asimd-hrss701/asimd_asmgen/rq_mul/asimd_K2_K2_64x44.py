from asimd_K2_schoolbook_64x11 import K2_schoolbook_64x11 as mul_64x11
from asimd_tranpose import transpose48x16_to_16x44, transpose16x96_to_96x16

p = print

def karatsuba_loop(a_mem, b_mem, r_mem, a_off, b_off, r_off, transpose=True):
  pass

def K2_K2_transpose_64x44(r_real='%rdi', a_real='%rsi', b_real='%rdx', coeffs=44, transpose=True):
  a_transpose = 0
  b_transpose = a_transpose + 44
  r_transpose = b_transpose + 44
  a_b_summed = r_transpose + 96
  a_in_rsp = a_b_summed + 22
  b_in_rsp = a_in_rsp + 22
  t2_in_rsp = b_in_rsp + 22

  print("uint16_t rsp[{}/2];".format((44 +
                                      44 + 96 + 22 + 22 + 22 + 44) * 32))

  t0 = (0, 1)
  t1 = (2, 3)
  t2 = (4, 5)
  t3 = (6, 7)

  karatsuba_loop = True
  innerloop = True

  for i in range(4):
    if karatsuba_loop == True:
      if transpose:
        a_off = a_transpose 
        b_off = b_transpose
        r_off = r_transpose

        transpose48x16_to_16x44(dst=a_mem, src=a_real, dst_off=a_off)
        transpose48x16_to_16x44(dst=b_mem, src=b_real, dst_off=b_off)
        
        # TODO: is this need 
        coeffs = 48 
      else:
        a_off = b_off = r_off = 0 
        a_mem = a_real
        b_mem = b_real
        r_mem = r_real 
      
      if innerloop == True:
        mul_64x11(r_mem, a_mem, b_mem, r_off, a_off, b_off)
        mul_64x11(r_mem, a_mem, b_mem, r_off + 22, a_off + 11, b_off + 11)
        mul_64x11("rsp", a_mem, b_mem, a_b_summed, a_off, b_off, additive=True)

        slide = 0
        for j in range(2):
          p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(10 + a_b_summed) + slide, "rsp"))
          p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(10 + r_off) + slide, r_mem))
          p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(32 + r_off) + slide, r_mem))

          p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))
          p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

          p("vst1q_u16({} + {}, y{});".format(16*(21 + r_off), r_mem, t0[j]))

          slide = 8

        for k in range(10):
          slide = 0
          for j in range(2):
            p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(r_off + 11 + i) + slide, r_mem))
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(r_off + 22 + i) + slide, r_mem))
            p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(11 + i + a_b_summed) + slide, "rsp"))
            p("y{} = vsubq_u16(y{}, y{});".format(t1[j], t1[j], t0[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(r_off + 33 + i) + slide, r_mem))
            p("y{} = vsubq_u16(y{} ,y{});".format(t1[j], t1[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(r_off + i) + slide, r_mem))
            p("y{} = vsubq_u16(y{} ,y{});".format(t0[j], t0[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(a_b_summed + i) + slide, "rsp"))
            p("y{} = vaddq_u16(y{} ,y{});".format(t0[j], t0[j], t2[j]))

            p("vst1q_u16({} + {}, y{});".format(16*(11 + i + r_off) + slide, r_mem, t0[j] ))
            p("vst1q_u16({} + {}, y{});".format(16*(22 + i + r_off) + slide, r_mem, t1[j] ))

            '''
            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(t2_in_rsp + 33 + i), "rsp"))
            # t3 save for later 
            p("y{} = vsubq_u16(y{} ,y{});".format(t3[j], t1[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(t2_in_rsp + i), "rsp"))
            p("y{} = vsubq_u16(y{} ,y{});".format(t0[j], t0[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(a_b_summed + i), "rsp"))
            p("y{} = vaddq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            p("vst1q_u16({} + {}, y{});".format(16*(t2_in_rsp + 11 + i), "rsp", t0[j]))
            '''
            slide = 8
        
        
