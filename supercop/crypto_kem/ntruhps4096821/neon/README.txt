This implementation is based on NTRU latest commit at: https://github.com/jschanck/ntru

Any pull requests, issues are welcome at: https://github.com/cothan/ntru/

Best regards, 
-----
Duc Tri Nguyen (CERG GMU)



.
├── api_bytes.h
├── api.h
├── architectures
├── cpucycles.c
├── cpucycles.h
├── crypto_hash_sha3256.h
├── crypto_sort_int32.c
├── crypto_sort_int32.h
├── fips202.c
├── fips202.h
├── implementors
├── kem.c
├── kem.h
├── Makefile
├── Makefile-NIST
├── neon_poly_mod.c
├── neon_poly_rq_mul.c
├── owcpa.c
├── owcpa.h
├── pack3.c
├── packq.c
├── params.h
├── poly.c
├── poly.h
├── poly_lift.c
├── poly_r2_inv.c
├── poly_s3_inv.c
├── PQCgenKAT_kem.c
├── randombytes.c
├── randombytes.h
├── README.txt
├── rng.c
├── rng.h
├── rq_mul
│   ├── neon_batch_multiplication.c
│   ├── neon_batch_multiplication.h
│   ├── neon_matrix_transpose.c
│   ├── neon_matrix_transpose.h
│   ├── neon_poly_rq_mul.c
│   └── neon_poly_rq_mul.h
├── sample.c
├── sample.h
├── sample_iid.c
├── verify.c
└── verify.h

1 directory, 43 files
25e200c4d1f661a4935e7ce83a737168  ./randombytes.c
b6582be88dd57af0ceb0af2b30ad9f73  ./rng.h
19949d219c449857c755dab16b717706  ./params.h
afa3dc30017b49a81ff3fd1d572e90c6  ./randombytes.h
532f481786028c9e051987c3fa4117ef  ./crypto_hash_sha3256.h
dac7d03de534caebd10fcbb905ed5e38  ./neon_poly_rq_mul.c
38f6e78435cf30a562b4ebfe8ec878ea  ./owcpa.c
d5df9db931abbbf22e58d1d44750ff23  ./owcpa.h
b55f33e63837bd734c8603a8a62850b0  ./api.h
df25acbfd62af425a16bed1cf1f6e923  ./Makefile-NIST
2c9fa5877a3815e1736f48cedd44755e  ./verify.c
2528b2860721dadf4d9b42ffbf21d9d3  ./sample.h
2814a16ed66c85c1d487c46d9dc001b1  ./fips202.h
a8f27ad8127194670a1525da2627a924  ./sample_iid.c
faf0a4482e72714fcf3608eb6314971f  ./Makefile
fde0e879d85af0ab44b7ed1c02a377bd  ./cpucycles.c
ada339a819cc97874a3de6c9f8c52528  ./crypto_sort_int32.c
9bee9edfd6973d0f8f042c9be649101b  ./crypto_sort_int32.h
ff63ec365b42b553ed603d5b642762ef  ./api_bytes.h
08eb70977885e30c3487bbd002d2c558  ./implementors
a5ee6edbdb29baa97c94293a4621cdf8  ./packq.c
dc2401aac4bb5c95019f2760fe36bada  ./cpucycles.h
c4b12cd8d1f3c328fe10bd01c88cd9f0  ./architectures
5822ca6494ff6f21be0b5c53db7f6269  ./poly_r2_inv.c
940e0ad84d1d62cdc0490050a3a4aa55  ./sample.c
7789171a88deb3f806214dd71943ebdc  ./fips202.c
9b74a1ca21184f838bca228290c40d02  ./poly_lift.c
2b781c0665f2c0f6183fadc7bb7f84fc  ./rq_mul/neon_poly_rq_mul.c
dabd97b103209cf624472a0d94af52b3  ./rq_mul/neon_matrix_transpose.c
78780469c2988a357803925d71544372  ./rq_mul/neon_matrix_transpose.h
13fdc0cde498b80687a490a914deaceb  ./rq_mul/neon_batch_multiplication.h
fdc3526e3a8e4ab2c00c0701ab36c18c  ./rq_mul/neon_poly_rq_mul.h
47b9c418f0f09890b9e1b60a170ed9ae  ./rq_mul/neon_batch_multiplication.c
b0302140479f271a90fe2ada6e218cce  ./poly_s3_inv.c
e8804edee5585be385bc4ad0ac2f4599  ./poly.c
12481066c57bcde8ecf09ac2fb9f524c  ./PQCgenKAT_kem.c
6af1c6ab4969d9bfcf07bf3279d2d1d2  ./poly.h
ebe4130b4cce08b6150dcd9b50c18e5d  ./rng.c
cac39c2b918edc8c912b08b05a844f90  ./kem.c
bf69ea50f554f85d3a0d5f214b812a82  ./neon_poly_mod.c
03d52993b4afce10aee17325b655d4b4  ./pack3.c
2960e46aa2db04584264c18ab93d1bfa  ./verify.h
1341a74a4963d6e675d3a77843537609  ./kem.h
