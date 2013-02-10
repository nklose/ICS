// python style indenting:
// :tabSize=4:indentSize=4:noTabs=true:

/* This file contains the loop needed in the core_1 function in
 * the triple.py file. This is a multithreaded implementation,
 * and requires a C compiler that supports OpenMP and C99.
 */

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <omp.h>

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

#define MULTI_THREAD 1

typedef complex double c128;

/* See the core function of loop_reg.py for a description
 * of this function and its arguments and return values.
 */
void core(r1,sr,sg,tb,side,lim)
	void *r1,*sr,*sg,*tb;
	int lim,side;
{
    int na = side/2;
    int nb = lim/2;
    int lowlim = na-nb;
    int low = lowlim-na;
    int high = na-lowlim;
    c128 (*restrict ir1)[lim][lim][lim] = r1;
    c128 (*restrict isr)[side] = sr;
    c128 (*restrict isg)[side] = sg;
    c128 (*restrict itb)[side] = tb;
    if (lim <= side/2){
#if defined(MULTI_THREAD)
#pragma omp parallel for schedule(static)
#endif
        for (int v1=low; v1<high; v1++){
            int mlow = low-MIN(v1-1,0);
            int mhigh = high-MAX(v1,0);
            for (int u1=mlow; u1<mhigh; u1++){
                for (int v2=low; v2<high; v2++){
                    for (int u2=low; u2<high; u2++){
                        ir1[nb+v1][nb+u1][nb+v2][nb+u2] =
                        isr[na+u1][na+u2] *
                        isg[na+v1][na+v2] *
                        itb[na+u1+v1][na+u2+v2];
    }}}}}
    return;
#if defined(MULTI_THREAD)
#pragma omp parallel for schedule(static)
#endif
    for (int v1=low; v1<high; v1++){
        int mlow = low-MIN(v1-1,0);
        int mhigh = high-MAX(v1,0);
        for (int u1=mlow; u1<mhigh; u1++){
            for (int v2=low; v2<high; v2++){
                for (int u2=low; u2<high; u2++){
                    if (abs(u2+v2) < na){
                        ir1[nb+v1][nb+u1][nb+v2][nb+u2] =
                        isr[na+u1][na+u2] *
                        isg[na+v1][na+v2] *
                        itb[na+u1+v1][na+u2+v2];
    }}}}}
    return;
}
