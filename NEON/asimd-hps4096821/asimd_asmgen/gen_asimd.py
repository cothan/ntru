from os import system 


filename = ['asimd_poly_mod_3_Phi_n.py','asimd_poly_mod_q_Phi_n.py','asimd_poly_rq_to_s3.py','asimd_sample_iid.py',]




# for i in filename:
#     name, extension = i.split('.')
#     # print (name, extension)
#     system("python3 {} > intrin_{}.c".format(i, name[6:]))

# for i in filename:
#     name, extension = i.split('.')
#     system("code intrin_{}.c".format(name))

for i in filename:
    name, extension = i.split('.')
    system("clang-format intrin_{}.c > intrin_c/intrin_{}_formated.c".format(name, name[6:]))