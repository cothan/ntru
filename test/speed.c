#include "../kem.h"
#include "../params.h"
//  #include "../cpucycles.h"
#include "../randombytes.h"
#include "../poly.h"
#include "../sample.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "../../test/print.h"

#define NTESTS 1000000

#define TIME(s) clock_gettime(CLOCK_MONOTONIC_RAW, &s);
// Result is nanosecond per call
#define CALC(start, stop) \
  ((double)((stop.tv_sec - start.tv_sec) * 1000000000 + (stop.tv_nsec - start.tv_nsec))) / NTESTS;

int main()
{

  unsigned char key_a[32], key_b[32];
  poly r, a, b;
  unsigned char *pks = (unsigned char *)malloc(NTRU_PUBLICKEYBYTES);
  unsigned char *sks = (unsigned char *)malloc(NTRU_SECRETKEYBYTES);
  unsigned char *cts = (unsigned char *)malloc(NTRU_CIPHERTEXTBYTES);
  unsigned char fgbytes[NTRU_SAMPLE_FG_BYTES];
  unsigned char rmbytes[NTRU_SAMPLE_RM_BYTES];
  uint16_t a1 = 0;
  int i;
  struct timespec start, stop;
  long ns;

  printf("-- api --\n\n");

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    crypto_kem_keypair(pks, sks);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("crypto_kem_keypair:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    crypto_kem_enc(cts, key_b, pks);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("crypto_kem_enc:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    crypto_kem_dec(key_a, cts, sks);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("crypto_kem_dec:", ns);


  printf("-- internals --\n\n");

  randombytes(fgbytes, sizeof(fgbytes));
  sample_fg(&a, &b, fgbytes);
  poly_Z3_to_Zq(&a);
  poly_Z3_to_Zq(&b);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_mul(&r, &a, &b);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_Rq_mul:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_mul(&r, &a, &b);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_S3_mul:", ns);

  // a as generated in test_polymul
  for (i = 0; i < NTRU_N; i++)
    a1 += a.coeffs[i];
  a.coeffs[0] = (a.coeffs[0] + (1 ^ (a1 & 1))) & 3;

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_inv(&r, &a);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_Rq_inv:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_inv(&r, &a);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_S3_inv:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    randombytes(fgbytes, NTRU_SAMPLE_FG_BYTES);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("randombytes:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    randombytes(rmbytes, NTRU_SAMPLE_RM_BYTES);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("randombytes:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    sample_iid(&a, fgbytes);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("sample_iid:", ns);

#ifdef NTRU_HRSS
  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    sample_iid_plus(&a, fgbytes);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("sample_iid_plus:", ns);
#endif

#ifdef NTRU_HPS

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    sample_fixed_type(&a, fgbytes);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("sample_fixed_type:", ns);

#endif

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_lift(&a, &b);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_lift:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_to_S3(&a, &b);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_Rq_to_S3:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_sum_zero_tobytes(cts, &a);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_Rq_sum_zero_tobytes:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_sum_zero_frombytes(&a, cts);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_Rq_sum_zero_frombytes:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_tobytes(cts, &b);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_S3_tobytes:", ns);

  TIME(start);
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_frombytes(&b, cts);
  }
  TIME(stop);
  ns = CALC(start, stop);
  print("poly_S3_frombytes:", ns);

  free(pks);
  free(sks);
  free(cts);

  return 0;
}
