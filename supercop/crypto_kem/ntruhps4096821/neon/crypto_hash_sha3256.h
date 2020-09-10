/*=============================================================================
This file has been adapted from the implementation 
(available at, CC0-1.0 License https://github.com/jschanck/ntru) 
of "NTRU:A submission to the NIST post-quantum standardization effort"
by : Cong Chen, Oussama Danba, Jeffrey Hoffstein, Andreas Hülsing, 
Joost Rijneveld, Tsunekazu Saito, John M. Schanck, Peter Schwabe, 
William Whyte,Keita Xagawa, Takashi Yamakawa, Zhenfei Zhang.
=============================================================================*/

#ifndef CRYPTO_HASH_SHA3256
#define CRYPTO_HASH_SHA3256

#include "fips202.h"

#define crypto_hash_sha3256 sha3_256
#define crypto_hash_sha3512 sha3_512
#define crypto_hash_shake256 shake256

#endif
