p = print

def vload(dst, address, src):
    p("y{} = vld1q_u16({} + {});".format(dst, address, src))

def vstore(address, dst, src):
    p("vst1q_u16({} + {}, y{});".format(address, dst, src))

def vadd(c, a, b):
    # c =  a + b
    p("y{} = vaddq_u16(y{}, y{});".format(c, a, b))

def vsub(c, a, b):
    # c = a - b
    p("y{} = vsubq_u16(y{}, y{});".format(c, a, b))

def vmul(c, a, b):
    # c = low(a * b)
    p("y{} = vmulq_u16(y{}, y{});".format(c, a, b))

def vmula(d, a, b, c):
    # d = a*b + c
    p("y{} = vmlaq_u16 (y{}, y{}, y{});".format(d, a, b, c))

def vxor(c, a, b):
    # c = a ^ b 
    p("y{} = veorq_u16(y{}, y{});".format(c, a, b))

def schoolbook_64x13(r_mem, a_mem, b_mem, r_off=0, a_off=0, b_off=0, additive=False):
    registers = [i for i in range(31, -1, -1)]
    
    def free(*regs):
        for index, x in enumerate(regs):
            if x in registers:
                raise Exception("This register {}:{} is already freed".format(index,x))
            registers.append(x)

    def alloc():
        # print('// {:2d}'.format(len(registers)))
        return registers.pop()

    def freelist(l):
        for i in l:
            free(i)

    def check():
        return len(registers)

    a_regs = []
    b_regs = []

    t0 = alloc()
    t1 = alloc()

    for i in range(7):
        slide = 0
        for j in range(2):
            a_reg, b_reg = alloc(), alloc()

            vload(a_reg, 16*(i + a_off) + slide, a_mem)
            vload(b_reg, 16*(i + b_off) + slide, b_mem)

            if additive:
                vload(t0, 16*(i + a_off + 13) + slide, a_mem)
                vload(t1, 16*(i + b_off + 13) + slide, b_mem)
                vadd(a_reg, a_reg, t0)
                vadd(b_reg, b_reg, t1)

            a_regs.append(a_reg)
            b_regs.append(b_reg)

            slide = 8

    p("// remain: {}".format(check()))
    # print(a_regs)
    # print(b_regs)

    for i in range(13):
        first = True
        for j in range(min(i+1, 7)):
            if i - j < 7:
                if first:
                    vmul(t0, a_regs[j], b_regs[i-j])
                    vmul(t1, a_regs[7 + j], b_regs[7 + i-j])
                    first = False
                else:
                    vmula(t0, a_regs[j], b_regs[i-j], t0)
                    vmula(t1, a_regs[7+j], b_regs[7 + i - j], t1)
        
        vstore(16*(i + r_off), r_mem, t0)
        vstore(16*(i + r_off) + 8, r_mem, t1)


    for i in range(6):
        vload(b_regs[i] , 16*(7+i + b_off), b_mem)
        vload(b_regs[7+i] , 16*(7+i + b_off) + 8, b_mem)
        if additive:
            vload(t0, 16*(7+i + b_off + 13), b_mem)
            vload(t1, 16*(7+i + b_off + 13) + 8, b_mem)
            vadd(b_regs[i], b_regs[i], t0)
            vadd(b_regs[i+7], b_regs[7+i], t1)
    
    for i in range(12):
        first = True
        for j in range(min(i+1, 7)):
            if i - j < 6:
                if first and 7+i < 13:
                    vload(t0, 16*(7+i + r_off), r_mem)
                    vload(t1, 16*(7+i + r_off) + 8, r_mem)
                    first = False
                if first and 7 + i >=13:
                    vxor(t0, t0, t0)
                    vxor(t1, t1, t1)
                    first = False
                
                vmula(t0, a_regs[j], b_regs[i-j], t0)
                vmula(t1, a_regs[7+j], b_regs[7+i-j], t1)
        vstore(16*(7+i + r_off), r_mem, t0)
        vstore(16*(7+i + r_off) + 8, r_mem, t1)

    for i in range(6):
        vload(a_regs[i], 16*(7+i + a_off), a_mem)
        vload(a_regs[7+i], 16*(7+i + a_off) +8, a_mem)
        if additive:
            vload(t0, 16*(7+i + a_off + 13), a_mem)
            vload(t1, 16*(7+i + a_off + 13) + 8, a_mem)
            vadd(a_regs[i], a_regs[i], t0)
            vadd(a_regs[7+i], a_regs[7+i], t1)

    for i in range(11):
        first = True
        for j in range(min(i+1, 6)):
            if i - j < 6:
                if first and 14 + i < 19:
                    vload(t0, 16*(14+i + r_off), r_mem)
                    vload(t1, 16*(14+i + r_off) + 8, r_mem)
                    first = False
                if first and 14 + i >=19:
                    vxor(t0, t0, t0)
                    vxor(t1, t1, t1)
                    first = False
                vmula(t0, a_regs[j], b_regs[j], t0)
                vmula(t1, a_regs[7+j], b_regs[7+j], t1)
        vstore( 16*(14+i + r_off), r_mem, t0)
        vstore( 16*(14+i + r_off) + 8, r_mem, t1)

    for i in range(6):
        vload(b_regs[i] ,   16*(i + b_off), b_mem)
        vload(b_regs[7+i] , 16*(i + b_off) + 8, b_mem)
        if additive:
            vload(t0, 16*(i + b_off + 13), b_mem)
            vload(t1, 16*(i + b_off + 13) + 8, b_mem)
            vadd(b_regs[i], b_regs[i], t0)
            vadd(b_regs[i+7], b_regs[7+i], t1)

    for i in range(12):
        first = True
        for j in range(min(i+1, 6)):
            if i - j < 7:
                if first:
                    vload(t0, 16*(7+i + r_off), r_mem)
                    vload(t1, 16*(7+i + r_off) + 8, r_mem)
                    first = False
                
                vmula(t0, a_regs[j], b_regs[i-j], t0)
                vmula(t1, a_regs[7+j], b_regs[7+i-j], t1)
        vstore(16*(7+i + r_off), r_mem, t0)
        vstore(16*(7+i + r_off) + 8, r_mem, t1)

    free(t0, t1)
    freelist(a_regs)
    freelist(b_regs)

    p("// check {}".format(check()))

if __name__ == '__main__':
    p("""#include <arm_neon.h>
#include <stdio.h>

void schoolbook_64x13(uint16_t *c, uint16_t *a, uint16_t *b)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31;
    for (int i = 0; i < 4; i++)
    {
    """)

    schoolbook_64x13("c", "a", "b")

    p("""
    a += 832; 
    b += 832; 
    c += 1664;
    }
}
    """)

    p("""
void karatsuba_64x13_loop_additive(uint16_t *c, uint16_t *a, uint16_t *b)
{
    uint16x8_t y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28, y29, y30, y31;
    for (int i = 0; i < 4; i++)
    {""")

    schoolbook_64x13('c', 'a', 'b', additive=True)
    p("""
    a += 832; 
    b += 832; 
    c += 1664;
    }
}
    """)


