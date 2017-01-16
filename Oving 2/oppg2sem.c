
// gcc 4.7.2 +
// gcc -std=gnu99 -Wall -g -o helloworld_c helloworld_c.c -lpthread


#include <pthread.h>
#include <stdio.h>
#include<semaphore.h>

static int i = 0;
sem_t mutex; // Declare a global variable mutex


void* threadfuntion_1() {
	for (int n = 0; n<1000000; n++) {
		sem_wait(&mutex);
		i++;
		sem_post(&mutex);
	}
	return NULL;
}

void* threadfunction_2() {
	for (int n = 0; n<1000000; n++) {
		sem_wait(&mutex);
		i--;
		sem_post(&mutex);
	}
	return NULL;
}



int main() {
	sem_init(&mutex, 0, 1); //Initialize mutex

	pthread_t thread_1;
	pthread_t thread_2;
	pthread_create(&thread_1, NULL, threadfuntion_1, NULL);
	pthread_create(&thread_2, NULL, threadfunction_2, NULL);


	pthread_join(thread_1, NULL);
	pthread_join(thread_2, NULL);

	sem_destroy(&mutex); //Deletes mutex

	printf("%d\n", i);
	return 0;
}



