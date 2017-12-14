#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <cilk/cilk.h>
#include <time.h>
#include <string.h>

int isPowerOf2(int n){
	while(n){
		if(n & 1)
			break;
		n >>= 1;
	}
	return (1 == n? 1:0);
}

void up(int a[], int n){
	for (int k = 0; k < log2(n); k++)
	{
		int j = exp2(k);
		int m = 2*j;
		cilk_for (int i = 0; i < n; i += m)
		{
			a[i+m-1] += a[i+j-1];
		}
	}
}

void down(int a[], int n){
	for (int k = log2(n)-1; k >= 0; k--){
		int x = exp2(k);
		int y = 2*x;
		cilk_for(int i = 0; i < n; i += y)
		{
			int tmp = a[i + x - 1];
			a[i + x - 1] = a[i + y - 1];
			a[i + y - 1] += tmp;
		}
	}
}

void par_up(int a[], int n){
	for (int j = 0; j <= (int)log2(n); j++)
	{
		int k = exp2(j);
		int m = 2*k;
		cilk_for (int i = (n-1); i >= k; i -= m)
		{
			a[i] += a[i-k];
		}
	}
}

void par_down(int a[], int n){
	for (int j = (int)log2(n); j >= 0; j--)
	{
		int k = exp2(j);
		int m = 2*k;
		cilk_for (int i = (n-1); i >= k; i -= m)
		{
			 int left = a[i-k];
			 a[i-k] = a[i];
			 a[i] += left;
		}
	}
}

void ex_pref_sum(int a[], int n){
	if(isPowerOf2(n)){
		up(a,n);
		a[n-1]=0;
		down(a,n);
	}
	else{
		par_up(a,n);
		a[n-1]=0;
		par_down(a,n);
	}
}


//Sequencial Prefix Sum
void prefixOnHost(int a[], int n){
	int* b = (int*)malloc(sizeof(int)*n);
	memcpy(b,a,sizeof(int)*n);
	int sum = 0;
	for(int i=0; i<n; i++){
		sum += b[i];
		b[i] = sum;
		a[i] = b[i] - a[i];
	}
	free(b);
}


//gcc -fcilkplus Blelloch_PrefixSum.c -O2 -lrt -o Blelloch_PrefixSum
int main(int argc, char const *argv[])
{
	struct timespec tstart, tend;
	float time;
	int n = atoi(argv[1]);
	srand((unsigned)0);
	int* a_s = (int*)malloc(sizeof(int)*n);
	int* a_p = (int*)malloc(sizeof(int)*n);
	for (int i = 0; i < n; ++i)
	{
		a_s[i] = rand() % 100;
		a_p[i] = a_s[i];
	}

	//sequential prefix sum for verification and timing
	clock_gettime(CLOCK_MONOTONIC, &tstart);
	prefixOnHost(a_s, n);
	clock_gettime(CLOCK_MONOTONIC, &tend);
	time = (tend.tv_sec-tstart.tv_sec) + (tend.tv_nsec-tstart.tv_nsec)*1.0e-9;
	printf("sequential prefix sum time in s: %f\n", time);

	clock_gettime(CLOCK_MONOTONIC, &tstart);
	ex_pref_sum(a_p,n);
	clock_gettime(CLOCK_MONOTONIC, &tend);

	time = (tend.tv_sec-tstart.tv_sec) + (tend.tv_nsec-tstart.tv_nsec)*1.0e-9;
	printf("parallel prefix sum time in s: %f\n", time);

	int i;
	for (i = 0; i < n; ++i)
	{
		if (a_s[i]!=a_p[i])
		{
			printf("wrong result.\n");
			break;
		}
	}
	if (i == n)
	{
		printf("correct result.\n");
	}

	free(a_s);
	free(a_p);

	return 0;
}