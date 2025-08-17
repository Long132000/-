#include<iostream>

using namespace std;

int main()
{
	int x, y;
	cin >> x >> y;

	int sum = x + y;
	int raz = x - y;
	int pro = x * y;
	int otn = x / y;

	setlocale(LC_ALL, "Russian");

	cout << "Сумма x+y=" << sum << endl;
	cout << "Разность x-y=" << raz << endl;
	cout << "Произведение x*y=" << pro << endl;
	cout << "Отношение x/y=" << otn << endl;

	return 0;
}