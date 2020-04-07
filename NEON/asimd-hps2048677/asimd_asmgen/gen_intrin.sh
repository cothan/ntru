#!/bin/bash

python3 asimd_poly_mod_3_Phi_n.py > intrin_c/intrin_poly_mod_3_Phi_n.c
clang-format intrin_c/intrin_poly_mod_3_Phi_n.c > intrin_c/intrin_poly_mod_3_Phi_n_formatted.c
rm intrin_c/intrin_poly_mod_3_Phi_n.c

python3 asimd_poly_mod_q_Phi_n.py > intrin_c/intrin_poly_mod_q_Phi_n.c
clang-format intrin_c/intrin_poly_mod_q_Phi_n.c > intrin_c/intrin_poly_mod_q_Phi_n_formatted.c
rm intrin_c/intrin_poly_mod_q_Phi_n.c

python3 asimd_poly_rq_to_s3.py > intrin_c/intrin_poly_rq_to_s3.c
clang-format intrin_c/intrin_poly_rq_to_s3.c > intrin_c/intrin_poly_rq_to_s3_formatted.c 
rm intrin_c/intrin_poly_rq_to_s3.c

python3 asimd_sample_iid.py > intrin_c/intrin_sample_iid.c
clang-format intrin_c/intrin_sample_iid.c > intrin_c/intrin_sample_iid_formatted.c
rm intrin_c/intrin_sample_iid.c