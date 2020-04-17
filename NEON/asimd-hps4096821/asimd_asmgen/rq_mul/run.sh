#!/bin/bash

python3 asimd_K2_K2_64x52.py > intrin_c/intrin_K2_K2_64x52.c
clang-format intrin_c/intrin_K2_K2_64x52.c > intrin_c/intrin_K2_K2_64x52_formated.c
rm intrin_c/intrin_K2_K2_64x52.c

python3 asimd_poly_rq_mul.py > intrin_c/intrin_poly_rq_mul.c
clang-format intrin_c/intrin_poly_rq_mul.c > intrin_c/intrin_poly_rq_mul_formated.c
rm intrin_c/intrin_poly_rq_mul.c