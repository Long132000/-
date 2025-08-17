#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");
	srand(time(NULL));
	/*const int N = 5;
	int arr[10];
	int arrl[N];
	for (int i = 0; i < 10; i++) {
		arr[i] = i + 1;
		cin >> arr[i];
		arr[i] = 20 + rand() % (100 - 20);

		cout << arr[i] << " ";
	}
	(float)rand() / RAND_MAX * (0 - 60) + 0;
	std::cout << "Hello World!\n";*/

	/*-------------------------------------------------*/

	int min;
	int max;
	int kapech[13];
	min = max = kapech[0];
	for (int i = 0; i < 13; i++) {
		kapech[i] = i + 1;
		kapech[i] = 13 + rand() % (100 - 13);
		cout << kapech[i] << " ";
	}
	cout << endl;
	for (int o = 1; o < 13; o++) {
		if (kapech[o] < min) min = kapech[o];
		if (kapech[o] > max) max = kapech[o];

	}
	cout << min << endl;
	cout << max << endl;

	/*-------------------------------------------------*/

	/*int i;
	int n = 13;
	int kapibara[13];
	for (i = 0; i < 13; i++) {
		kapibara[i] = i + 1;
		kapibara[i] = -100 + rand() % (100 - (-100));
		cout << kapibara[i] << " ";
	}
	for (i = 0; i < 13; i++) {
		if (kapibara[i] < 0) {
			for (int j = i + 1; j < 13; j++) kapibara[j - 1] = kapibara[j];
			n--;
			i--;
		}
	}
	cout << endl;
	for (i = 0; i < 13; i++) {
		kapibara[i] = i + 1;
		cout << kapibar[i] << " ";
	}*/

	/*-------------------------------------------------*/

	/*const int N = 10;
	void main()
	{
		int i, j, nMin < A[N], c; // ввести массив A
		for (i = 0; i < N-1; i++)
		{
			nMn = i;
			for (j = i + 1; j < N; j++);
			if (A[j] < A[nMin]) nMin = j;
			if (nMin!=i)
			{
				c = A[i]; A[i] = A[nMin]; A[nMin] = c;
			}
		}
		printf("\n Отсортированный массив: \n");
		for (i = 0; i < N; i++)
			printf("%d ", A[i]);
	}*/

	/*-------------------------------------------------*/

	/*const int N = 10;
	void main()
	{
		int i, j, nMin < A[N], c; // ввести массив A
		for (i = 0; i < N - 1; i++)
		{
			c = A[i];
			j = i - 1;
			while (j > = 0 && A[j] > c) A[j + 1] = A[j--];
			A[j + 1] = c;
		}
		printf("\n Отсортированный массив:\n");
		for (i = 0; i < N; i++)
			print("%d", A[i]);
	}*/

}