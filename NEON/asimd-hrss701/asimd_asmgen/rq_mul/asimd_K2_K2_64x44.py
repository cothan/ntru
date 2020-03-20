from asimd_K2_schoolbook_64x11 import K2_schoolbook_64x11 as mul_64x11
from asimd_tranpose import transpose48x16_to_16x44, transpose16x96_to_96x16

def K2_K2_transpose_64x44(r_real='%rdi', a_real='%rsi', b_real='%rdx', coeffs=44, transpose=True):