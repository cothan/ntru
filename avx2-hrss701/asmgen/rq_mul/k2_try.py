p = print


def K2_schoolbook_64x11(r_mem, a_mem, b_mem, r_off=0, a_off=0, b_off=0, additive=False):
    for i in range(6):
        p("vld1q_s16 ({}+{}) = y{}".format(16*(i + a_off), a_mem, i)) # move aligned, LOAD
        p("vld1q_s16 ({}+{}) = y{}".format(16*(i + b_off), b_mem, i+6)) # move aligned, LOAD
        if additive:
            p("vaddq_s16 {}({}), y{}, y{}".format(16*(i + a_off + 11), a_mem, i, i)) # add packed integer
            p("vaddq_s16 {}({}), y{}, y{}".format(16*(i + b_off + 11), b_mem, i+6, i+6)) # add packed integer
    for i in range(11):
        first = True
        for j in range(min(i+1, 6)):
            if i - j < 6:
                if first:
                    # Multiply Packed Signed Integers and Store Low 16-bit Result
                    p("vmulq_s16 (y{}, y{}) = y{}".format(j, 6+ i-j, 12 + (i % 2))) 

                    first = False
                else:
                    # Multiply Packed Signed Integers and Store Low 16-bit Result and ADD
                    p("vmlaq_s16 (y{}, y{}, y{}) = y{}".format(12 + (i % 2), j, 6+ i-j, 12 + (i % 2))) 
                    # p("vpmullw y{}, y{}, y{}".format(j, 6+ i-j, 15)) 
                    # p("vpaddw y{}, y{}, y{}".format(12 + (i % 2), 15, 12 + (i % 2)))
        p("vst1q_s16 ({}+{}, y{})".format( 16*(i + r_off), r_mem, 12 + (i % 2))) #move aligned, STORE

    for i in range(5):
        p("vld1q_s16 ({}+{}) = y{}".format(16*(6+i + a_off), a_mem, i)) # move aligned, LOAD
        p("vld1q_s16 ({}+{}) = y{}".format(16*(6+i + b_off), b_mem, i+6)) # move aligned, LOAD
        if additive:
            p("vaddq_s16 ({}+{}, y{}) = y{}".format(16*(6+i + a_off + 11), a_mem, i, i))
            p("vaddq_s16 ({}+{}, y{}) = y{}".format(16*(6+i + b_off + 11), b_mem, i+6, i+6))
    for i in range(9):
        first = True
        for j in range(min(i+1, 5)):
            if i - j < 5:
                if first:
                    # MUL LOW
                    p("vmulq_s16 (y{}, y{}) = y{}".format(j, 6+ i-j, 12 + (i % 2))) 
                    first = False
                else:
                    # MUL LOW and ADD
                    p("vmlaq_s16 (y{}, y{}, y{}) = y{}".format(12 + (i % 2), j, 6+ i-j, 12 + (i % 2))) 
                    # p("vpmullw y{}, y{}, y{}".format(j, 6+ i-j, 15))
                    # p("vpaddw y{}, y{}, y{}".format(12 + (i % 2), 15, 12 + (i % 2)))
        # p("vmovdqa y{}, {}({})".format(12 + (i % 2), 16*(12+i + r_off), r_mem)) # move aligned, STORE
        p("vst1q_s16 ({}+{}, y{})".format( 16*(12+i + r_off), r_mem, 12 + (i % 2))) # move aligned, STORE
    for i in range(5):  # i == 5 is still in place as a[5] resp. b[5]
        p("vaddq_s16 ({}+{}, y{}) = y{}".format(16*(i + a_off), a_mem, i, i)) #ADD mem, ymm
        p("vaddq_s16 ({}+{}, y{}) = y{}".format(16*(i + b_off), b_mem, i+6, i+6)) #ADD mem, ymm
        # these additions should not be strictly necessary, as we already computed this earlier
        # recomputing seems more convenient than storing them
        if additive:
            p("vaddq_s16 ({}+{}, y{}) = y{}".format(16*(i + a_off + 11), a_mem, i, i)) # ADD mem, ymm
            p("vaddq_s16 ({}+{}, y{}) = y{}".format(16*(i + b_off + 11), b_mem, i+6, i+6)) # ADD mem, ymm

    # peel apart the third schoolbook mult so we end with (a+b)(c+d) in registers
    # this prevents us from having to touch the stack at all for t2
    i = 5
    target = 12
    free = 15
    for j in range(6):
        if j == 0:
            # MUL LOW
            p("vmulq_s16 (y{}, y{}) = y{}".format(j, 6+ i-j, target)) 
        else:
            # MUL LOW and ADD
            p("vmlaq_s16 (y{}, y{}, y{}) = y{}".format(target, j, 6+ i-j, target)) 
            # p("vpmullw y{}, y{}, y{}".format(j, 6+ i-j, free))   
            # p("vpaddw y{}, y{}, y{}".format(free, target, target))
    # weird centerpiece, deal with this straight away to free up a register

    # SUB mem, ymm then STORE

    p("vsubq_s16 (y{}, {}+{}) = y{}".format(target, 16*(5 + r_off), r_mem,   target))
    p("vsubq_s16 (y{}, {}+{}) = y{}".format(target, 16*(17 + r_off), r_mem,  target))
    p("vst1q_s16 ({}+{}, y{})".format(16*(11 + r_off), r_mem, target))

    # MUL ymm
    # use a[5] for all products we need it for
    for j in range(1, 5):  # note again that we do not compute [10]
        p("vmulq_s16 (y{}, y{}) = y{}".format(5, 6+ j, 12+j-1))
    # this frees up register y5 which held a[5]
    free = 5
    # finish up [6] to [9] (in registers 12 to 15)
    for i in range(6, 10):
        target = 12 + i-6  # already contains one product
        for j in range(min(i+1, 6)):
            if j == 5:
                continue  # we've already used a[5]
            if i - j < 6:
                # MUL LOW and ADD
                p("vmlaq_s16 (y{}, y{}, y{}) = y{}".format(target, j, 6+ i-j, target)) 
                # p("vpmullw y{}, y{}, y{}".format(j, 6+ i-j, free))
                # p("vpaddw y{}, y{}, y{}".format(free, target, target))

    # can now start overwriting b[5], b[4] etc.
    for i in range(4, -1, -1):
        target = 6+i+1  # b[5], b[4], b[3] ..
        first = True
        for j in range(min(i+1, 6)):
            if i - j < 6:
                if first:
                    # MUL LOW
                    p("vmulq_s16 (y{}, y{}) = y{}".format(j, 6+ i-j, target))
                    first = False
                else:
                    # MUL LOW and ADD
                    p("vmlaq_s16 (y{}, y{}, y{}) = y{}".format(target, j, 6+ i-j, target)) 
                    # p("vpmullw y{}, y{}, y{}".format(j, 6+ i-j, free))
                    # p("vpaddw y{}, y{}, y{}".format(free, target, target))

    # t2 is now spread all over the registers: (i.e. t[0] in register ymm7)
    t2 = [7, 8, 9, 10, 11, None, 12, 13, 14, 15]

    for i in range(5):
        p("vld1q_s16 ({}+{}) = y{}".format(16*(6+i + r_off), r_mem, i)) # LOAD mem to ymm
        # p("vpsubw {}({}), y{}, y{}".format(16*(12+i + r_off), r_mem, i, i)) # SUB mem, ymm
        p("vsubq_s16 (y{}, {}+{} ) = y{}".format(i, 16*(12+i + r_off), r_mem, i)) # SUB mem, ymm
        if i < 4:
            p("vsubq_s16 (y{}, y{}) = y{}".format(t2[6 + i], i, i+6)) # SUB ymm, ymm
            if i < 3:
                p("vsubq_s16 ( y{}, {}+{})) = y{}".format( i+6, 16*(18+i + r_off), r_mem, i+6)) # SUB ymm, ymm
            p("vst1q_s16 ({}+{}, y{})".format( 16*(12+i + r_off), r_mem, i+6)) # STORE ymm to mem
        # ADD, SUB and STORE
        p("vaddq_s16 (y{}, y{}) = y{}".format(t2[i], i, i))
        p("vsubq_s16 (y{}, {}+{}) = y{}".format(i, 16*(i + r_off), r_mem, i))
        p("vst1q_s16 ({}+{}, y{})".format(16*(6+i + r_off), r_mem, i ))


if __name__ == '__main__':
    p(".data")
    p(".section .rodata")
    p(".align 32")

    p(".text")
    p(".hidden K2_schoolbook_64x11")
    p(".global K2_schoolbook_64x11")
    p(".hidden K2_schoolbook_64x11_additive")
    p(".global K2_schoolbook_64x11_additive")
    p(".att_syntax prefix")

    p("K2_schoolbook_64x11:")
    p("mov $4, %ecx")

    p("karatsuba_64x11_loop:")
    K2_schoolbook_64x11('%rdi', '%rsi', '%rdx')
    p("add $1408, %rsi")
    p("add $1408, %rdx")
    p("add $2816, %rdi")
    p("dec %ecx")
    p("jnz karatsuba_64x11_loop")

    p("ret")

    p("K2_schoolbook_64x11_additive:")
    p("mov $4, %ecx")

    p("karatsuba_64x11_loop_additive:")
    K2_schoolbook_64x11('%rdi', '%rsi', '%rdx', additive=True)
    p("add $1408, %rsi")
    p("add $1408, %rdx")
    p("add $2816, %rdi")
    p("dec %ecx")
    p("jnz karatsuba_64x11_loop_additive")

    p("ret")