#include "../kem.h"
#include "../params.h"
 #include "../cpucycles.h"
#include "../randombytes.h"
#include "../poly.h"
#include "../sample.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "print.h"

#if __aarch64__
// #include <papi.h>
#endif 

#define NTESTS 1000000
// #define NTESTS 1000

// static int cmp_llu(const void *a, const void *b) {
//   if (*(unsigned long long *)a < *(unsigned long long *)b)
//     return -1;
//   if (*(unsigned long long *)a > *(unsigned long long *)b)
//     return 1;
//   return 0;
// }

// static unsigned long long median(unsigned long long *l, size_t llen) {
//   qsort(l, llen, sizeof(unsigned long long), cmp_llu);

//   if (llen % 2)
//     return l[llen / 2];
//   else
//     return (l[llen / 2 - 1] + l[llen / 2]) / 2;
// }

// static double average(unsigned long long *t, size_t tlen) {
//   unsigned long long acc = 0;
//   size_t i;
//   for (i = 0; i < tlen; i++)
//     acc += t[i];
//   return ((double)acc) / (tlen);
// }

// static void print_results(const char *s, unsigned long long *t, size_t tlen) {
//   size_t i;
//   printf("%s", s);

//   unsigned long long mint = LONG_MAX;
//   unsigned long long maxt = 0LL;
//   for (i = 0; i < tlen - 1; i++) {
//     t[i] = t[i + 1] - t[i];

//     if (t[i] < mint)
//       mint = t[i];
//     if (t[i] > maxt)
//       maxt = t[i];
//   }
//   printf("\n");
//   printf("median: %'llu\n", median(t, tlen));
//   printf("average: %'lf\n", average(t, tlen - 1));
//   printf("\n");
// }

// void handle_error(int retval) {
//   printf("PAPI error %d: %s\n", retval, PAPI_strerror(retval));
//   exit(1);
// }


int main()
{

  unsigned char key_a[32], key_b[32];
  poly r, a, b;
  unsigned char* pks = (unsigned char*) malloc(NTRU_PUBLICKEYBYTES);
  unsigned char* sks = (unsigned char*) malloc(NTRU_SECRETKEYBYTES);
  unsigned char* cts = (unsigned char*) malloc(NTRU_CIPHERTEXTBYTES);
  unsigned char fgbytes[NTRU_SAMPLE_FG_BYTES];
  unsigned char rmbytes[NTRU_SAMPLE_RM_BYTES];
  uint16_t a1 = 0;
  int i;
  // int retval;
  clock_t start, end;

  printf("-- api --\n\n");
  #if __aarch64__
  // retval = PAPI_hl_region_begin("keypair");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    crypto_kem_keypair(pks,
                       sks);
  }
  end = clock() - start;
  print("crypto_kem_keypair:", ((double) end)/NTESTS);

  // print_results("ntru_keypair: ", t, NTESTS);

  #if __aarch64__
  // retval = PAPI_hl_region_end("keypair");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }

  // retval = PAPI_hl_region_begin("encaps");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 
  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    crypto_kem_enc(cts, key_b, pks);
  }
  end = clock() - start;
  print("crypto_kem_enc:", ((double) end)/NTESTS);
  // print_results("ntru_encaps: ", t, NTESTS);

  #if __aarch64__
  // retval = PAPI_hl_region_end("encaps");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }

  // retval = PAPI_hl_region_begin("decaps");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 
  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    crypto_kem_dec(key_a, cts, sks);
  }
  end = clock() - start;
  print("crypto_kem_dec:", ((double) end)/NTESTS);
  // print_results("ntru_decaps: ", t, NTESTS);
  #if __aarch64__
  // retval = PAPI_hl_region_end("decaps");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 
  printf("-- internals --\n\n");

  randombytes(fgbytes, sizeof(fgbytes));
  sample_fg(&a, &b, fgbytes);
  poly_Z3_to_Zq(&a);
  poly_Z3_to_Zq(&b);
  #if __aarch64__
  // retval = PAPI_hl_region_begin("rq_mul");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_Rq_mul(&r, &a, &b);
  }
  end = clock() - start;
  print("poly_Rq_mul:", ((double) end)/NTESTS);
  // print_results("poly_Rq_mul: ", t, NTESTS);
  #if __aarch64__
  // retval = PAPI_hl_region_end("rq_mul");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 
  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_S3_mul(&r, &a, &b);
  }
  end = clock() - start;
  print("poly_S3_mul:", ((double) end)/NTESTS);
  // print_results("poly_S3_mul: ", t, NTESTS);

  // a as generated in test_polymul
  for(i=0; i<NTRU_N; i++)
    a1 += a.coeffs[i];
  a.coeffs[0] = (a.coeffs[0] + (1 ^ (a1&1))) & 3;

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_Rq_inv(&r, &a);
  }
  end = clock() - start;
  print("poly_Rq_inv:", ((double) end)/NTESTS);
  // print_results("poly_Rq_inv: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_S3_inv(&r, &a);
  }
  end = clock() - start;
  print("poly_S3_inv:", ((double) end)/NTESTS);
  // print_results("poly_S3_inv: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    randombytes(fgbytes, NTRU_SAMPLE_FG_BYTES);
  }
  end = clock() - start;
  print("randombytes:", ((double) end)/NTESTS);
  // print_results("randombytes for fg: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    randombytes(rmbytes, NTRU_SAMPLE_RM_BYTES);
  }
  end = clock() - start;
  print("randombytes:", ((double) end)/NTESTS);
  // print_results("randombytes for rm: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    sample_iid(&a, fgbytes);
  }
  end = clock() - start;
  print("sample_iid:", ((double) end)/NTESTS);
  // print_results("sample_iid: ", t, NTESTS);

#ifdef NTRU_HRSS
  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    sample_iid_plus(&a, fgbytes);
  }
  end = clock() - start;
  print("sample_iid_plus:", ((double) end)/NTESTS);
  // print_results("sample_iid_plus: ", t, NTESTS);
#endif

#ifdef NTRU_HPS
  
  #if __aarch64__
  // retval = PAPI_hl_region_begin("sample_fixed_type");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 
  
  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    sample_fixed_type(&a, fgbytes);
  }
  end = clock() - start;
  print("sample_fixed_type:", ((double) end)/NTESTS);
  // print_results("sample_fixed_type: ", t, NTESTS);
  #if __aarch64__
  // retval = PAPI_hl_region_end("sample_fixed_type");
  // if (retval != PAPI_OK)
  // {
  //   printf("PAPI_hl_region: Error\n");
  // }
  #endif 
#endif

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_lift(&a, &b);
  }
  end = clock() - start;
  print("poly_lift:", ((double) end)/NTESTS);
  // print_results("poly_lift: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_Rq_to_S3(&a, &b);
  }
  end = clock() - start;
  print("poly_Rq_to_S3:", ((double) end)/NTESTS);
  // print_results("poly_Rq_to_S3: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_Rq_sum_zero_tobytes(cts, &a);
  }
  end = clock() - start;
  print("poly_Rq_sum_zero_tobytes:", ((double) end)/NTESTS);
  // print_results("poly_Rq_sum_zero_tobytes: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_Rq_sum_zero_frombytes(&a, cts);
  }
  end = clock() - start;
  print("poly_Rq_sum_zero_frombytes:", ((double) end)/NTESTS);
  // print_results("poly_Rq_sum_zero_frombytes: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_S3_tobytes(cts, &b);
  }
  end = clock() - start;
  print("poly_S3_tobytes:", ((double) end)/NTESTS);
  // print_results("poly_S3_tobytes: ", t, NTESTS);

  start = clock();
  for(i=0; i<NTESTS; i++)
  {
    // t[i] = cpucycles();
    poly_S3_frombytes(&b, cts);
  }
  end = clock() - start;
  print("poly_S3_frombytes:", ((double) end)/NTESTS);
  // print_results("poly_S3_frombytes: ", t, NTESTS);

  free(pks);
  free(sks);
  free(cts);

  return 0;
}
