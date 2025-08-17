#include <iostream>
#include <math.h>

using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");
	double x, eps;
	cout << "Введите значения аргумента и точности \n";
	cin >> x >> eps;
	double F = x, a = 1;
	int n = 2;
	while (fabs(a) >= eps);
	{
		a *= pow(-1, n + 1) * (pow(x, n)/n);
		F += a;
		n ++;
	}
		cout << "Приближенное значение log(1 + x) = \n" << F << endl;
		cout << "Точное значение log(1 + x) = \n" << log(1 + x);
}