#include <iostream>
using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");

	int number;
	cout << "Введите целое число: ";
	cin >> number;

	switch (number % 2) {

	case 0:
		cout << "Число " << number << " является чётным." << endl;
		break;
	case 1:
		cout << "Число " << number << " является нечётным." << endl;
		break;
	}

	return 0;
}