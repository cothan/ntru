#include "cpucycles.h"
#include <time.h>

long long cpucycles(void)
{
  #ifdef __arm__
    clock_t result = clock();
  #else
  unsigned long long result;
  asm volatile(".byte 15;.byte 49;shlq $32,%%rdx;orq %%rdx,%%rax"
    : "=a" (result) ::  "%rdx");
  #endif
  return result;
}
