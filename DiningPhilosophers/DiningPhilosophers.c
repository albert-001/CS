#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <semaphore.h>


int n = 5; //total number of philosophers

sem_t forks[5];

void pickup_forks(int id){
	if (id%2==0){
		sem_wait(&forks[(id-1+5)%n]);
		sem_wait(&forks[id]);
	} else
	{
		sem_wait(&forks[id]);
		sem_wait(&forks[(id-1+5)%n]);
	}
}

void return_forks(int id){
	sem_post(&forks[id]);
	sem_post(&forks[(id-1+5)%n]);
}

void* philosophers(void* args) {
    int id = *(int*)args;
    free(args);
    while(1) {
    	printf("philosopher %d is thinking.\n", id);
    	sleep(2); //thinking
    	printf("philosopher %d is hungry.\n", id);
    	pickup_forks(id);
    	printf("philosopher %d is eating.\n", id);
    	sleep(2); //eating
    	printf("philosopher %d return forks.\n", id);
    	return_forks(id);
    }
}


int main(int argc, char** argv)
{
	int i;
	for(i=0; i<n; i++) {
		sem_init(&forks[i],0,1);
	}

	//create philosopher threads.
	pthread_t* philosopher_t = (pthread_t*)malloc(sizeof(pthread_t)*n);
	for(i=0; i<n; i++) {
		int *args = (int*)malloc(sizeof(int));
        *args=i;
		pthread_create(&philosopher_t[i], NULL, philosophers, args);
	}

	for(i=0; i<n; i++){
        pthread_join(philosopher_t[i], NULL);
    }

	for(i=0; i<n; i++) {
		sem_destroy(&forks[i]);
	}

    free(philosopher_t);

	return(0);
}
