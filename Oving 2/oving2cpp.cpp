//Compiler:
//g++ -std=c++11 -pthread file_name.cpp

#include<iostream>
#include <thread>
#include <mutex>


using namespace std;

static int i = 0;
mutex mutex_1; //std::mutex  er en klasse av type mutex, kan lockes og unlockes 


void threadfunction_1() {
	for (int n = 0; n < 1000000; n++) {
		mutex_1.lock(); // låser i slik at kun denne funksjonen har den
		i++;
		mutex_1.unlock(); // helt til den kommer hit, da unlockes den slik at andre kan bruke i
	}
}

void threadfunction_2() {
	for (int n = 0; n < 1000000; n++) {
		mutex_1.lock(); 
		i--;
		mutex_1.unlock();
	}
}

int main() {
	thread thread_1(threadfunction_1);
	thread thread_2(threadfunction_2);
	thread_1.join();
	thread_2.join();
	cout << i << endl;
	return 0;
}