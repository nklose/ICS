// python style indenting
// :tabSize=4:indentSize=4:noTabs=true:

/*
 * Backend functions
 *
 * This file contains functions that are written in C and are called
 * from the backend python code in order to ensure that computationally
 * expensive sections are executed quickly and efficiently.
 *
 * Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
 * Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
 */

#include <stdlib.h>
#include <string.h>
#include <complex.h>
#include <fftw3.h>

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

typedef complex double c128;
typedef double f64;

static fftw_plan plan;

void core(data,sr,sg,sb,side,lim)
	void *data,*sr,*sg,*sb;
	int side,lim;
{
    int na = side/2;
    int nb = lim/2;
    int lowlim = na-nb;
    int low = lowlim-na;
    int high = na-lowlim;
    c128 (*restrict idata)[lim][lim][lim] = data;
    c128 (*restrict isr)[side] = sr;
    c128 (*restrict isg)[side] = sg;
    c128 (*restrict isb)[side] = sb;
    if (lim <= side/2){
        int factor = lim*lim*16;
        for (int i=0; i<nb+1; i++)
            memset(&idata[i][0][0][0],0,((nb+1)-i)*factor);
        for (int i=nb+1; i<lim; i++)
            memset(&idata[i][lim-(i-nb)][0][0],0,(i-nb)*factor);
        for (int v1=low; v1<high; v1++){
            int mlow = low-MIN(v1-1,0);
            int mhigh = high-MAX(v1,0);
            for (int u1=mlow; u1<mhigh; u1++){
                for (int v2=low; v2<high; v2++){
                    for (int u2=low; u2<high; u2++){
                        idata[nb+v1][nb+u1][nb+v2][nb+u2] =
                        isr[na+u1][na+u2] *
                        isg[na+v1][na+v2] *
                        isb[na+u1+v1][na+u2+v2];
    }}}}}
    return;
    memset(data,0,lim*lim*lim*lim*16);
    for (int v1=low; v1<high; v1++){
        int mlow = low-MIN(v1-1,0);
        int mhigh = high-MAX(v1,0);
        for (int u1=mlow; u1<mhigh; u1++){
            for (int v2=low; v2<high; v2++){
                for (int u2=low; u2<high; u2++){
                    if (abs(u2+v2) < na){
                        idata[nb+v1][nb+u1][nb+v2][nb+u2] =
                        isr[na+u1][na+u2] *
                        isg[na+v1][na+v2] *
                        isb[na+u1+v1][na+u2+v2];
    }}}}}
    return;
}

void init(int lim, void *data)
{
    int dim[] = {lim,lim,lim,lim};
    plan = fftw_plan_dft(4,dim,
        (c128 *)data,(c128 *)data,
        FFTW_BACKWARD,FFTW_ESTIMATE);
}

void execute()
{
    fftw_execute(plan);
}

void destroy()
{
    fftw_destroy_plan(plan);
}
