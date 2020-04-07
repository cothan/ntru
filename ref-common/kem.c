#include "randombytes.h"
#include "crypto_hash_sha3256.h"
#include "params.h"
#include "verify.h"
#include "sample.h"
#include "owcpa.h"

#if __aarch64__
#include <libkeccak.a.headers/SimpleFIPS202.h>
#endif

// API FUNCTIONS 
int crypto_kem_keypair(unsigned char *pk, unsigned char *sk)
{
  unsigned char seed[NTRU_SAMPLE_FG_BYTES];

  randombytes(seed, NTRU_SAMPLE_FG_BYTES);
  owcpa_keypair(pk, sk, seed);

  randombytes(sk+NTRU_OWCPA_SECRETKEYBYTES, NTRU_PRFKEYBYTES);

  return 0;
}

int crypto_kem_enc(unsigned char *c, unsigned char *k, const unsigned char *pk)
{
  poly r, m;
  unsigned char rm[NTRU_OWCPA_MSGBYTES];
  unsigned char rm_seed[NTRU_SAMPLE_RM_BYTES];

  randombytes(rm_seed, NTRU_SAMPLE_RM_BYTES);

  sample_rm(&r, &m, rm_seed);

  poly_S3_tobytes(rm, &r);
  poly_S3_tobytes(rm+NTRU_PACK_TRINARY_BYTES, &m);

#if __aarch64__
  SHA3_256(k, rm, NTRU_OWCPA_MSGBYTES);
#else 
  crypto_hash_sha3256(k, rm, NTRU_OWCPA_MSGBYTES);
#endif 

  poly_Z3_to_Zq(&r); // XXX: Should be in owcpa_enc
  owcpa_enc(c, &r, &m, pk);

  return 0;
}

int crypto_kem_dec(unsigned char *k, const unsigned char *c, const unsigned char *sk)
{
  int i, fail;
  unsigned char rm[NTRU_OWCPA_MSGBYTES];
  unsigned char buf[NTRU_PRFKEYBYTES+NTRU_CIPHERTEXTBYTES];

  fail = 0;

  /* Check that unused bits of last byte of ciphertext are zero */
  fail |= c[NTRU_CIPHERTEXTBYTES-1] & (0xff << (8 - (7 & (NTRU_LOGQ*NTRU_PACK_DEG))));

  fail |= owcpa_dec(rm, c, sk);
  /* If fail = 0 then c = Enc(h, rm), there is no need to re-encapsulate. */
  /* See comment in owcpa_dec for details.                                */
#if __aarch64__
  SHA3_256(k, rm, NTRU_OWCPA_MSGBYTES);
#else 
  crypto_hash_sha3256(k, rm, NTRU_OWCPA_MSGBYTES);
#endif 

  /* shake(secret PRF key || input ciphertext) */
  for(i=0;i<NTRU_PRFKEYBYTES;i++)
    buf[i] = sk[i+NTRU_OWCPA_SECRETKEYBYTES];
  for(i=0;i<NTRU_CIPHERTEXTBYTES;i++)
    buf[NTRU_PRFKEYBYTES + i] = c[i];
  
#if __aarch64__
  SHA3_256(rm, buf, NTRU_PRFKEYBYTES+NTRU_CIPHERTEXTBYTES);
#else
  crypto_hash_sha3256(rm, buf, NTRU_PRFKEYBYTES+NTRU_CIPHERTEXTBYTES);
#endif 
  cmov(k, rm, NTRU_SHAREDKEYBYTES, fail);

  return 0;
}
