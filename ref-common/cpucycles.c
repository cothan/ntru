#include "cpucycles.h"

#if __aarch64__

/*
cpucycles/armv8.c version 20190803
D. J. Bernstein
Public domain.
*/

#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/sysctl.h>

long long cpucycles(void)
{
  long long result = clock();
  //asm volatile("mrs %0, PMCCNTR_EL0" : "=r" (result));
  return result;
}


#else

long long cpucycles(void)
{
  unsigned long long result;
  asm volatile(".byte 15;.byte 49;shlq $32,%%rdx;orq %%rdx,%%rax"
    : "=a" (result) ::  "%rdx");

  return result;
}


#endif 