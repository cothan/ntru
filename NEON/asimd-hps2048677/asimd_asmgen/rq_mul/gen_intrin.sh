#!/bin/bash

python3 asimd_K2_K2_64x44.py > intrin_c/intrin_K2_K2_64x44.c
clang-format intrin_c/intrin_K2_K2_64x44.c > intrin_c/intrin_K2_K2_64x44_formatted.c
rm intrin_c/intrin_K2_K2_64x44.c

python3 asimd_poly_rq_mul.py > intrin_c/intrin_poly_rq_mul.c
clang-format intrin_c/intrin_poly_rq_mul.c > intrin_c/intrin_poly_rq_mul_formatted.c
rm intrin_c/intrin_poly_rq_mul.c