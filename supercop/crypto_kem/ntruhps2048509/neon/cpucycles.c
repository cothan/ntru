/*=============================================================================
This file has been adapted from the implementation 
(available at, CC0-1.0 License https://github.com/jschanck/ntru) 
of "NTRU:A submission to the NIST post-quantum standardization effort"
by : Cong Chen, Oussama Danba, Jeffrey Hoffstein, Andreas Hülsing, 
Joost Rijneveld, Tsunekazu Saito, John M. Schanck, Peter Schwabe, 
William Whyte,Keita Xagawa, Takashi Yamakawa, Zhenfei Zhang.
=============================================================================*/

#include "cpucycles.h"

#if __aarch64__

#include <papi.h>

long long cpucycles(void)
{
  long long result = PAPI_get_real_usec();
  return result;
}


#else
/*
cpucycles/armv8.c version 20190803
D. J. Bernstein
Public domain.
*/

long long cpucycles(void)
{
  unsigned long long result;
  asm volatile(".byte 15;.byte 49;shlq $32,%%rdx;orq %%rdx,%%rax"
    : "=a" (result) ::  "%rdx");

  return result;
}

#endif
