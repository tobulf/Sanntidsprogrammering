
// gcc 4.7.2 +
// gcc -std=gnu99 -Wall -g -o helloworld_c helloworld_c.c -lpthread


#include <pthread.h>
#include <stdio.h>
#include <unistd.h>


static int i = 0;
pthread_mutex_t lock;

void* threadfuntion_1() {
    for (int n = 0; n<1000000; n++) {
        pthread_mutex_lock(&lock);
        i++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

void* threadfunction_2() {
    for (int n = 0; n<1000000; n++) {
        pthread_mutex_lock(&lock);
        i--;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}



int main() {
    pthread_t thread_1;
    pthread_t thread_2;
    pthread_create(&thread_1, NULL, threadfuntion_1, NULL);
    pthread_create(&thread_2, NULL, threadfunction_2, NULL);
    

    pthread_join(thread_1, NULL);
    pthread_join(thread_2, NULL);

    pthread_mutex_destroy(&lock);
    printf("%d\n", i);
    return 0;
}



