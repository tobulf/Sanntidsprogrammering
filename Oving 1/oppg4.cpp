//Compiler:
//g++ -std=c++11 -pthread file_name.cpp
	
#include<iostream>
#include <thread>


using namespace std;

static int i = 0;

void threadfunction_1() {
	for (int n = 0; n < 1000000; n++) {
		i++;
	}
}

void threadfunction_2() {
	for (int n = 0; n < 1000000; n++){
		i--;
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
