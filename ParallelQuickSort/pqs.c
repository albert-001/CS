#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct STRU_ARR{
	int l;
	int* a;
} sub_arr_t;

void up(int a[], int n){
	int i,j,k;
	for (k = 0; k < log2(n); k++)
	{
		j = exp2(k);
		//cilk_for (i = j-1; i < n; i += 2*j)
		for (i = 0; i < n; i += 2*j)
		{
			a[i+2*j-1] += a[i+j-1];
		}
	}
}

void down(int a[], int n){
	int i,k;
	for (k = log2(n)-1; k >= 0; k--){
		int x = exp2(k);
		int y = exp2(k+1);
		//cilk_for(i = 0; i < n; i += y)
		for(i = 0; i < n; i += y)
		{
			int tmp = a[i + x -1];
			a[i + x -1] = a[i + y -1];
			a[i + y -1] += tmp;
		}
	}
}

void ex_pref_sum(int a[], int n){
	int k = log2(n);
	if(exp2(k) < n){
		int m = exp2(k+1);
		int* b = (int*)malloc(sizeof(int)*m);
		int i;
		for (i = 0; i < n; ++i)
		{
			b[i]=a[i];
		}
		for (i = n; i < m; ++i)
		{
			b[i]=0;
		}
		up(b,m);
		b[m-1]=0;
		down(b,m);
		for (i = 0; i < n; ++i)
		{
			a[i]=b[i];
		}
	}
	else{
		up(a,n);
		a[n-1]=0;
		down(a,n);
	}
}


sub_arr_t get_partition(int a[], int n, int p, int left){
	int i;
	int* F = (int*)malloc(sizeof(int)*n);
	int* K = (int*)malloc(sizeof(int)*n);
	for (i=0; i<n; i++)
	{
		F[i] = left? (a[i]<=p ? 1 : 0) : (a[i]>p ? 1 : 0);
		K[i] = F[i];
	}
	int flag = (K[n-1]==0)?0:1;
	ex_pref_sum(K, n);
	int kl = K[n-1] + flag;
	int* L = (int*)malloc(sizeof(int)*kl);
	//cilk_for (i=0; i<n; i++)
	for (i=0; i<n; i++)
	{
		if(F[i]){
			L[K[i]]=a[i];
		}
	}
	sub_arr_t sub_arr;
	sub_arr.a = L;
	sub_arr.l = kl;
	free(F);
	free(K);
	return sub_arr;
}

int* para_quick_sort(int a[], int n){
	if(n<=1){
		int* x = (int*)malloc(sizeof(int));
		x[0] = a[0];
		return x;
	}
	int p = a[rand()%n];
	sub_arr_t left = get_partition(a, n, p, 1);
	sub_arr_t right = get_partition(a, n, p, 0);
	int* L = para_quick_sort(left.a, left.l);
	int* R = para_quick_sort(right.a, right.l);
	int* ret = (int*)malloc(sizeof(int)*n);
	int i;
	for (i = 0; i < left.l; ++i)
	{
		ret[i] = L[i];
	}
	for (i = left.l; i < n; ++i)
	{
		ret[i] = R[i-left.l];
	}
	for (i = 0; i < n; ++i)
	{
		a[i] = ret[i];
	}
	free(left.a);
	free(right.a);
	free(L);
	free(R);
	return ret;
}


int main(int argc, char const *argv[])
{
	int i;
	srand((unsigned)0);
	int a[] = {14,9,3,11,8,7,5,16};
	int n = sizeof(a)/sizeof(int);
	printf("before sorted\n");
	for (i = 0; i < n; ++i)
	{
		printf("%d ", a[i]);
	}
	printf("\n");
	para_quick_sort(a, n);
	printf("after sorted\n");
	for (i = 0; i < n; ++i)
	{
		printf("%d ", a[i]);
	}
	printf("\n");
	return 0;
}