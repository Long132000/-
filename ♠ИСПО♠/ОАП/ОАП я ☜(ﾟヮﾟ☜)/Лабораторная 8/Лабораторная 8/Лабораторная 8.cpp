#include <iostream>
#include <cmath>

using namespace std;

int factorial(int tyt, int k);
double calculateResult(int k, int tyt, int n);


int main() {
	setlocale(LC_ALL, "rus");
	int k, tyt, n;

	cout << "Введите значение k: ";
	cin >> k;
	cout << "Введите значение tyt: ";
	cin >> tyt;
	cout << "Введите значение n: ";
	cin >> n;

	double result = calculateResult(k, tyt, n);
	cout << "Результат вычисления: " << result << endl;

	return 0;
}
int factorial(int tyt, int k) {
	if (tyt <= 10) {
		return 5;
	}
	else {
		return pow(k, tyt) * factorial(tyt + 4, k);
	}
}

double calculateResult(int k, int tyt, int n) {
	return factorial(tyt, k) / n;
}


//Этот код содержит две функции с одинаковыми именами(`multiply` и `add`),
//но с разными параметрами.Функция `multiply` принимает три целых числа и возвращает их произведение, 
//в то время как функция `add` принимает два вещественных числа и возвращает их сумму.
//В функции `main` происходит вызов обеих функций для демонстрации перегрузки функции.