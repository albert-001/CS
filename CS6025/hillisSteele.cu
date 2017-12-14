#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>

//Hillis Steele scan in one block;
__global__ void prefixOnDevice(int *a, int *b, int n){
	int id = threadIdx.x;
	int *s;
	for(int j=1; j<n; j<<=1){
		if(id >=j)
			b[id] = a[id-j] + a[id];
		else
			b[id] = a[id];
		s = a;
		a = b;
		b = s;
		__syncthreads();
	}	
}

void prefixOnHost(int *a, int n){
	int sum =0;
	for(int i=0; i<n; i++){
		sum += a[i];
		a[i] = sum;
	}
}

//one value per thread, with power of two number of threads
int main(int argc, char **argv){
	int blockSize = 128;
	int nBlocks = 1;
	int n = blockSize;
	int size = n*sizeof(int);
	int *a = (int*) malloc(size);
	int *b = (int*) malloc(size);
	int *a_d, *b_d;
	cudaMalloc((void**) &a_d, size);
	cudaMalloc((void**) &b_d, size);
	for(int i=0; i<n; i++)
		a[i] = i+1;
	cudaMemcpy(a_d, a, size, cudaMemcpyHostToDevice);

	prefixOnHost(a, n);
	
	prefixOnDevice <<<nBlocks, blockSize>>> (a_d, b_d, n);

	if((int)log2((double)n)%2 == 0)
		cudaMemcpy(b, a_d, size, cudaMemcpyDeviceToHost);
	else
		cudaMemcpy(b, b_d, size, cudaMemcpyDeviceToHost);

	for(int i=0; i<n; i++)
		//printf("%d %d\n", a[i], b[i]);
		assert(a[i] == b[i]);
	return 0;
}
