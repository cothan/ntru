#include "../kem.h"
#include "../params.h"
// #include "../cpucycles.h"
#include "../randombytes.h"
#include "../poly.h"
#include "../sample.h"
#include <stdlib.h>
#include <stdio.h>
#include <papi.h>


#define NTESTS 1000

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

  printf("-- api --\n\n");
  PAPI_hl_region_begin("keypair");
  for (i = 0; i < NTESTS; i++)
  {
    crypto_kem_keypair(pks, sks);
  }
  PAPI_hl_region_end("keypair");

  PAPI_hl_region_begin("encaps");
  for (i = 0; i < NTESTS; i++)
  {
    crypto_kem_enc(cts, key_b, pks);
  }
  PAPI_hl_region_end("encaps");

  PAPI_hl_region_begin("decaps");
  for (i = 0; i < NTESTS; i++)
  {
    crypto_kem_dec(key_a, cts, sks);
  }
  PAPI_hl_region_end("decaps");

  printf("-- internals --\n\n");

  randombytes(fgbytes, sizeof(fgbytes));
  sample_fg(&a, &b, fgbytes);
  poly_Z3_to_Zq(&a);
  poly_Z3_to_Zq(&b);

  PAPI_hl_region_begin("rq_mul");
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_mul(&r, &a, &b);
  }
  PAPI_hl_region_end("rq_mul");

  PAPI_hl_region_begin("poly_S3_mul");
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_mul(&r, &a, &b);
  }
  PAPI_hl_region_end("poly_S3_mul");

  // a as generated in test_polymul
  for (i = 0; i < NTRU_N; i++)
    a1 += a.coeffs[i];
  a.coeffs[0] = (a.coeffs[0] + (1 ^ (a1 & 1))) & 3;

  PAPI_hl_region_begin("poly_Rq_inv");
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_inv(&r, &a);
  }
  PAPI_hl_region_end("poly_Rq_inv");

  PAPI_hl_region_begin("poly_S3_inv");
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_inv(&r, &a);
  }
  PAPI_hl_region_end("poly_S3_inv");

  randombytes(fgbytes, NTRU_SAMPLE_FG_BYTES);

  randombytes(rmbytes, NTRU_SAMPLE_RM_BYTES);

  PAPI_hl_region_begin("sample_iid");
  for (i = 0; i < NTESTS; i++)
  {
    sample_iid(&a, fgbytes);
  }
  PAPI_hl_region_end("sample_iid");

#ifdef NTRU_HRSS
  PAPI_hl_region_begin("sample_iid_plus");
  for (i = 0; i < NTESTS; i++)
  {
    sample_iid_plus(&a, fgbytes);
  }
  PAPI_hl_region_end("sample_iid_plus");
#endif

#ifdef NTRU_HPS

  PAPI_hl_region_begin("sample_fixed_type");
  for (i = 0; i < NTESTS; i++)
  {
    sample_fixed_type(&a, fgbytes);
  }
  PAPI_hl_region_end("sample_fixed_type");

#endif

  PAPI_hl_region_begin("poly_lift");
  for (i = 0; i < NTESTS; i++)
  {
    poly_lift(&a, &b);
  }
  PAPI_hl_region_end("poly_lift");

  PAPI_hl_region_begin("poly_Rq_to_S3");
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_to_S3(&a, &b);
  }
  PAPI_hl_region_end("poly_Rq_to_S3");

  PAPI_hl_region_begin("poly_Rq_sum_zero_tobytes");
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_sum_zero_tobytes(cts, &a);
  }
  PAPI_hl_region_end("poly_Rq_sum_zero_tobytes");

  PAPI_hl_region_begin("poly_Rq_sum_zero_frombytes");
  for (i = 0; i < NTESTS; i++)
  {
    poly_Rq_sum_zero_frombytes(&a, cts);
  }
  PAPI_hl_region_end("poly_Rq_sum_zero_frombytes");

  PAPI_hl_region_begin("poly_S3_tobytes");
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_tobytes(cts, &b);
  }
  PAPI_hl_region_end("poly_S3_tobytes");

  PAPI_hl_region_begin("poly_S3_frombytes");
  for (i = 0; i < NTESTS; i++)
  {
    poly_S3_frombytes(&b, cts);
  }
  PAPI_hl_region_end("poly_S3_frombytes");

  free(pks);
  free(sks);
  free(cts);

  return 0;
}
