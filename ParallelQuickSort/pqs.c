#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <cilk/cilk.h>
#include <time.h>

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}

void print_array(int a[], int n){
	for (int i = 0; i < n; ++i)
	{
		printf("%d ", a[i]);
	}
	printf("\n");
}

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
			a[i+2*j-1] += a[i+j-1];
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
		cilk_for (int i = (n-1); i >= k; i -= 2*k)
		{
			a[i] += a[i-k];
		}
	}
}

void par_down(int a[], int n){
	for (int j = (int)log2(n); j >= 0; j--)
	{
		int k = exp2(j);
		cilk_for (int i = (n-1); i >= k; i -= 2*k)
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


int partition(int a[], int left, int right){
	int n = right - left + 1;
	int pivot = a[rand() % n + left];
	int* FL = (int*)malloc(sizeof(int)*n);
	int* KL = (int*)malloc(sizeof(int)*n);
	int* FR = (int*)malloc(sizeof(int)*n);
	int* KR = (int*)malloc(sizeof(int)*n);
	cilk_for (int i=0; i<n; i++)
	{
		FL[i] = (a[i+left]<=pivot)?1:0;
		KL[i] = FL[i];
		FR[i] = (a[i+left]>pivot)?1:0;
		KR[i] = FR[i];
	}
	int flagL = (KL[n-1]==0)?0:1;
	int flagR = (KR[n-1]==0)?0:1;
	ex_pref_sum(KL, n);
	ex_pref_sum(KR, n);
	int l_len = KL[n-1] + flagL;
	int r_len = KR[n-1] + flagR;
	if(!(l_len+r_len == n)){
		printf("error!\n");
		exit(1);
	}
	int* L = NULL;
	int* R = NULL;
	if (l_len > 0)
	{
		L = (int*)malloc(sizeof(int)*l_len);
	}
	if(r_len > 0){
		R = (int*)malloc(sizeof(int)*r_len);
	}

	cilk_for (int i=0; i<n; i++)
	{
		if(FL[i]){
			L[KL[i]]=a[i + left];
		}
		if(FR[i]){
			R[KR[i]]=a[i + left];
		}
	}
	cilk_for (int i = 0; i < l_len; ++i)
	{
		a[i + left] = L[i];
	}
	cilk_for (int i = 0; i < r_len; ++i)
	{
		a[i + left + l_len] = R[i];
	}
	free(FL);
	free(KL);
	free(FR);
	free(KR);
	if(L){free(L);}
	if(R){free(R);}
	return left+l_len-1;
}

void insertsort(int a[], int left, int right)
{
  int i, j;
  for(i=left+1; i<=right; i++)
  {
    int temp = a[i];
    for(j=i;(j>=1)&&(temp<a[j-1]);j--)
    {
      a[j]=a[j-1];
    }
    a[j] = temp;
  }
}

void para_quick_sort(int a[], int left, int right){
	if((right-left)<5){ //cutoff, use insertsort
		insertsort(a, left, right);
		return;
	}
	
	int mid = partition(a, left, right);
	cilk_spawn para_quick_sort(a, left, mid);
	para_quick_sort(a, mid+1, right);
	cilk_sync;
}


int main(int argc, char const *argv[])
{
	struct timespec tstart, tend;
	float time;
	srand((unsigned)0);
	int n = atoi(argv[1]);
	if (argc!=2 || n==0)
	{
		printf("Wrong parameters. Use command %s 1000", argv[0]);
	}
	int* a = (int*)malloc(sizeof(int) * n);
	int* a_s = (int*)malloc(sizeof(int) * n);
	cilk_for (int i = 0; i < n; i++)
	{
		a[i] = rand() % 10000;
		a_s[i] = a[i];
	}
	clock_gettime(CLOCK_MONOTONIC, &tstart);
	para_quick_sort(a, 0, n-1);
	clock_gettime(CLOCK_MONOTONIC, &tend);
	time = (tend.tv_sec-tstart.tv_sec) + (tend.tv_nsec-tstart.tv_nsec)*1.0e-9;
	printf("parallel quick sort time in s: %f\n", time);
	clock_gettime(CLOCK_MONOTONIC, &tstart);
	qsort(a_s, n, sizeof(int), cmpfunc);
	clock_gettime(CLOCK_MONOTONIC, &tend);
	time = (tend.tv_sec-tstart.tv_sec) + (tend.tv_nsec-tstart.tv_nsec)*1.0e-9;
	printf("sequential quick sort time in s: %f\n", time);
	int i;
	for (i = 0; i < n; ++i)
	{
		if(a[i]!=a_s[i]){
			printf("Wrong result.\n");
			break;
		}
	}
	if (i==n)
	{
		printf("Correct result.\n");
	}
	free(a);
	free(a_s);
	return 0;
}
