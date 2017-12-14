#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>

int isPrime(int n);

int main(int argc, char *argv[]){
	if(argc < 2) return 1;
	int size = strtol(argv[1], NULL, 10);
	int id; /* Process rank, from 0 to np-1 */
	int np; /* Number of processes */
	int prime = 0;
	int count = 0;
	int global_count;
	double* rbuf;
	double timer;

	MPI_Init (&argc, &argv);
	MPI_Comm_size (MPI_COMM_WORLD, &np);
	MPI_Comm_rank (MPI_COMM_WORLD, &id);
	MPI_Barrier(MPI_COMM_WORLD);
	timer = -MPI_Wtime();
	int n = (size-1)/2;
	int istart = (float)id*n / np;
	int iend = (float)(id + 1)*n / np - 1;
	istart = 3+2*istart;
	iend = 3+2*(iend+1);
	for(int i=istart; i<=iend; i+=2){
		int new = isPrime(i);
		count += prime&new;
		prime = new;
	}
	timer += MPI_Wtime();
	if (id==0)
	{
		rbuf = (double*)malloc(np*sizeof(double));
	}
	MPI_Gather(&timer, 1, MPI_DOUBLE, rbuf, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
	MPI_Reduce(&count, &global_count, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
	if (id==0)
	{
		printf("num = %d\n", global_count);
		fflush(stdout);
		for (int i = 0; i < np; ++i)
		{
			printf("time[%d] = %f\n", i, rbuf[i]);
			fflush(stdout);
		}
	}
	MPI_Finalize();
	return 0;
}

int isPrime(int n){
	int notPrime = 0;
	if(n == 2) return 1;
	if(n%2 == 0) return 0;
	for(int i=3; i<=(int)sqrt(n); i+=2){
		notPrime = (n%i == 0);
		if(notPrime) return 0;
	}
	return !notPrime;	
}
