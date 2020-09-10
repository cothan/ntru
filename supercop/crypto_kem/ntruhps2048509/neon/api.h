/*=============================================================================
This file has been adapted from the implementation 
(available at, CC0-1.0 License https://github.com/jschanck/ntru) 
of "NTRU:A submission to the NIST post-quantum standardization effort"
by : Cong Chen, Oussama Danba, Jeffrey Hoffstein, Andreas Hülsing, 
Joost Rijneveld, Tsunekazu Saito, John M. Schanck, Peter Schwabe, 
William Whyte,Keita Xagawa, Takashi Yamakawa, Zhenfei Zhang.
=============================================================================*/

#ifndef API_H
#define API_H

#include "params.h"

#define CRYPTO_SECRETKEYBYTES NTRU_SECRETKEYBYTES
#define CRYPTO_PUBLICKEYBYTES NTRU_PUBLICKEYBYTES
#define CRYPTO_CIPHERTEXTBYTES NTRU_CIPHERTEXTBYTES
#define CRYPTO_BYTES NTRU_SHAREDKEYBYTES

#define CRYPTO_ALGNAME "ntruhps2048509"

int crypto_kem_keypair(unsigned char *pk, unsigned char *sk);

int crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);

int crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);


#endif
