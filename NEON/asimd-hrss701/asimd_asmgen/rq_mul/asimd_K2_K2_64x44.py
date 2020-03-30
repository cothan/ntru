from asimd_K2_schoolbook_64x11 import K2_schoolbook_64x11 as mul_64x11
from asimd_tranpose import transpose48x16_to_16x44, transpose16x96_to_96x16
from goto import with_goto

p = print

a_transpose = 0
b_transpose = a_transpose + 44
r_transpose = b_transpose + 44
a_b_summed = r_transpose + 96
a_in_rsp = a_b_summed + 22
b_in_rsp = a_in_rsp + 22
t2_in_rsp = b_in_rsp + 22
coeffs = 44

a_off, b_off, r_off = "", "", ""
a_mem, b_mem, r_mem = "", "", ""
a_real, b_real, r_real = "a", "b", "r"
ecx = 4



def karatsuba_loop(transpose=True, **kargs):
    global a_transpose, b_transpose, r_transpose
    global a_off, b_off, r_off
    global a_mem, b_mem, r_mem
    global a_real, b_real, r_real
    global coeffs

    if transpose:
        a_off = a_transpose
        b_off = b_transpose
        r_off = r_transpose

        p("uint16_t *r9 = rsp;")
        a_mem = b_mem = "r9"
        p("uint16_t *r10 = rsp;")
        r_mem = "r10"

        transpose48x16_to_16x44(dst=a_mem, src=a_real, dst_off=a_off)
        transpose48x16_to_16x44(dst=b_mem, src=b_real, dst_off=b_off)

        coeffs = 48
    else:
        a_off = b_off = r_off = 0
        a_mem = a_real
        b_mem = b_real
        r_mem = r_real

def innerloop(t0, t1, t2):
    global a_transpose, b_transpose, r_transpose
    global a_off, b_off, r_off
    global a_mem, b_mem, r_mem
    global a_real, b_real, r_real
    global coeffs, ecx

    mul_64x11(r_mem, a_mem, b_mem, r_off, a_off, b_off)
    mul_64x11(r_mem, a_mem, b_mem, r_off + 22, a_off + 11, b_off + 11)
    mul_64x11("rsp", a_mem, b_mem, a_b_summed, a_off, b_off, additive=True)

    slide = 0
    for j in range(2):
        p("y{} = vld1q_u16({} + rsp);".format(t0[j], 16*(10 + a_b_summed) + slide))
        p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(10 + r_off) + slide, r_mem))
        p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(32 + r_off) + slide, r_mem))

        p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))
        p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

        p("vst1q_u16({} + {}, y{});".format(16*(21 + r_off), r_mem, t0[j]))

        slide = 8

    for i in range(10):
        slide = 0
        for j in range(2):
            p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(r_off + 11 + i) + slide, r_mem))
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(r_off + 22 + i) + slide, r_mem))
            p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            p("y{} = vld1q_u16({} + rsp);".format(t1[j], 16*(11 + i + a_b_summed) + slide))
            p("y{} = vsubq_u16(y{}, y{});".format(t1[j], t1[j], t0[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(r_off + 33 + i) + slide, r_mem))
            p("y{} = vsubq_u16(y{} ,y{});".format(t1[j], t1[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(r_off + i) + slide, r_mem))
            p("y{} = vsubq_u16(y{} ,y{});".format(t0[j], t0[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + rsp);".format(t2[j], 16*(a_b_summed + i) + slide))
            p("y{} = vaddq_u16(y{} ,y{});".format(t0[j], t0[j], t2[j]))

            p("vst1q_u16({} + {}, y{});".format(16 *(11 + i + r_off) + slide, r_mem, t0[j]))
            p("vst1q_u16({} + {}, y{});".format(16 *(22 + i + r_off) + slide, r_mem, t1[j]))

            slide = 8
    ecx = -ecx

def done(t0, t1, t2):
    global a_mem, b_mem, r_mem, a_off, b_off, r_off
    global a_real, b_real, r_real, a_b_summed
    global a_in_rsp, b_in_rsp, t2_in_rsp
    global ecx 

    save = []

    p("{} -= {};".format(a_mem, 16*22))
    if a_mem != b_mem:
        p("{} -= {};".format(b_mem, 16*22))
    p("{} -= {};".format(r_mem, 16*44))

    for i in range(22):
        slide = 0
        for j in range(2):
            p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(i + a_off) + slide, a_mem))
            p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(22 + i + a_off) + slide, a_mem))
            p("y{} = vaddq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))
            p("vst1q_u16({} + rsp, y{});".format(16*(a_in_rsp + i) + slide, t0[j]))
            # t0, t1 is free

            p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(i + b_off) + slide, b_mem))
            p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(22 + i + b_off) + slide, b_mem))
            p("y{} = vaddq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))
            p("vst1q_u16({} + rsp, y{});".format(16*(b_in_rsp + i) + slide, t0[j]))

            slide = 8 

    mul_64x11("rsp", "rsp", "rsp", t2_in_rsp, a_in_rsp, b_in_rsp)
    mul_64x11("rsp", "rsp", "rsp", t2_in_rsp + 22, a_in_rsp + 11, b_in_rsp + 11)
    mul_64x11("rsp", "rsp", "rsp", a_b_summed, a_in_rsp, b_in_rsp, additive=True)

    for i in range(10):
        slide = 0 
        for j in range(2):

            p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(t2_in_rsp + 11 + i) + slide, "rsp"))
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(t2_in_rsp + 22 + i) + slide, "rsp"))
            p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(11 + i + a_b_summed) + slide, "rsp"))
            p("y{} = vsubq_u16(y{}, y{});".format(t1[j], t1[j], t0[j]))


            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(t2_in_rsp + 33 + i), "rsp"))
            # 8 + 2*i + j save for later
            p("y{} = vsubq_u16(y{} ,y{});".format(8 + 2*i + j, t1[j], t2[j]))
            save.append(8 + 2*i + j)

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(t2_in_rsp + i), "rsp"))
            p("y{} = vsubq_u16(y{} ,y{});".format(t0[j], t0[j], t2[j]))

            # t2 free
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(a_b_summed + i), "rsp"))
            p("y{} = vaddq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            p("vst1q_u16({} + {}, y{});".format(16*(t2_in_rsp + 11 + i), "rsp", t0[j]))

            slide = 8 

    ####
    slide = 0 
    for j in range(2):
        p("y{} = vld1q_u16({} + rsp".format(t0[j], 16*(10 + a_b_summed) + slide))
        p("y{} = vld1q_u16({} + rsp".format(t1[j], 16*(10 + t2_in_rsp) + slide))
        p("y{} = vld1q_u16({} + rsp".format(t2[j], 16*(32 + t2_in_rsp) + slide))

        p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))
        p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

        p("y{} = vld1q_u16({} + {};".format(t1[j], 16*(21 + r_off) + slide, r_mem))
        p("y{} = vld1q_u16({} + {};".format(t2[j], 16*(65 + r_off) + slide, r_mem))

        p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))
        p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

        p("vst1q_u16({} + {}, y{});".format(16*(43 + r_off), r_mem, t0[j]))

        slide = 8 

    for i in range(21):
        slide = 0
        for j in range(2):
            p("y{} = vld1q_u16({} + {});".format(t0[j], 16*(22 + i + r_off) + slide, r_mem))
            p("y{} = vld1q_u16({} + {});".format(t1[j], 16*(44 + i + r_off) + slide, r_mem))
            
            # r->coeffs[22 + i] -= r->coeffs[44 + i];
            p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t1[j]))

            # r->coeffs[44 + i] = t2b.coeffs[22 + i] - r->coeffs[22 + i];
            # print (save, 2*i + j)
            if 2*i + j < 20: 
                p("y{} = vsubq_u16(y{}, y{});".format(t1[j], save[2*i + j], t0[j]))
            else:
                p("y{} = vld1q_u16({} + rsp);".format(t2[j], 16*(t2_in_rsp + 22 +i)))
                p("y{} = vsubq_u16(y{}, y{});".format(t1[j], t2[j], t0[j]))
                

            # r->coeffs[44 + i] -= r->coeffs[66 + i];
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(66 + i + r_off) + slide, r_mem))
            p("y{} = vsubq_u16(y{}, y{});".format(t1[j], t1[j], t2[j]))

            # r->coeffs[22 + i] -= r->coeffs[i];
            p("y{} = vld1q_u16({} + {});".format(t2[j], 16*(i + r_off) + slide, r_mem))
            p("y{} = vsubq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            # r->coeffs[22 + i] += t2b.coeffs[i];
            p("y{} = vld1q_u16({} + rsp);".format(t2[j], 16*(t2_in_rsp + i) + slide))
            p("y{} = vaddq_u16(y{}, y{});".format(t0[j], t0[j], t2[j]))

            p("vst1q_u16({} + {}, y{});".format(16*(22 + i + r_off) + slide, r_mem, t0[j] ))
            p("vst1q_u16({} + {}, y{});".format(16*(44 + i + r_off) + slide, r_mem, t1[j] ))


            slide = 8

    p("y{} = 0;".format(t2[0]))
    p("vst1q_u16({} + {}, y{});".format(16*(87 + r_off), r_mem, t2[0]))
    p("vst1q_u16({} + {}, y{});".format(16*(87 + r_off) + 8, r_mem, t2[0]))

    if transpose: 
        transpose16x96_to_96x16(dst=r_real, src=r_mem, src_off=r_transpose)

    p("{} += {};".format(a_real, 16*coeffs))
    p("{} += {};".format(b_real, 16*coeffs))
    p("{} += {};".format(r_real, 32*coeffs))

    ecx -= 1
    

@with_goto
def K2_K2_transpose_64x44(r_real_input='c', a_real_input='a', b_real_input='b', transpose_input=True):
    global transpose
    global r_real, a_real, b_real
    transpose = transpose_input
    r_real, a_real, b_real = r_real_input, a_real_input, b_real_input

    p("uint16_t tmp[{}/2];".format((44 + 44 + 96 + 22 + 22 + 22 + 44) * 32))
    p("uint16_t *rsp = tmp;")
    
    t0 = (0, 1)
    t1 = (2, 3)
    t2 = (4, 5)
    t3 = (6, 7)

    label .karatsuba_loop
    p("// Karatsuba_loop")
    karatsuba_loop(transpose_input)

    label .innerloop
    p("// Innerloop")
    innerloop(t0, t1, t2)

    if ecx >= 0:
        goto .done

    p("{} += {};".format(a_mem, 16*22))
    if a_mem != b_mem:
        p("{} += {};".format(b_mem, 16*22))
    p("{} += {};".format(r_mem, 16*44))
    goto .innerloop

    label .done
    p('// done')
    done(t0, t1, t2)
    

    if ecx != 0:
        goto .karatsuba_loop

    #TODO: Skips this 
    # p("{} -={};".format(r_real, 2 * (2*16 * coeffs*2)))
    # p("rsp += {}".format( (44 + 44 + 96 + 22 + 22 + 22 + 44) * 16))


if __name__ == "__main__":

    K2_K2_transpose_64x44(transpose_input=True)

