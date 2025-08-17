#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");
	srand(time(NULL));
	const int N = 5;
	int arr[10];
	int arrl[N];
	for (int i = 0; i < 10; i++) {
		arr[i] = 20 + rand() % (100 - 20);

		cout << arr[i] << " ";
	}
    std::cout << "Hello World!\n";
}
