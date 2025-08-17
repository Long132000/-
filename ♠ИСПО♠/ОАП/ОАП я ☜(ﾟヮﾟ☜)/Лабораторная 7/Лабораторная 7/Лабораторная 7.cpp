#include <iostream>
using namespace std;

void inputMatrix(int a[100][100], int m, int n) {
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout << "Введите элемент a[" << i << "][" << j << "]: ";
			cin >> a[i][j];
		}
	}
}

int calculateMaxForRow(int row[], int n) {
	int max = row[0];
	for (int j = 1; j < n; j++) {
		if (row[j] > max) {
			max = row[j];
		}
	}
	return max;
}

int sumOfMaxValues(int a[100][100], int m, int n) {
	int sumMax = 0;
	for (int i = 0; i < m; i++) {
		int max = calculateMaxForRow(a[i], n);
		cout << "Максимальное значение в " << i + 1 << "-й строке: " << max << endl;
		sumMax += max;
	}
	return sumMax;
}

int main() {
	setlocale(LC_ALL, "rus");
	int m, n;
	cout << "Введите количество строк m: ";
	cin >> m;
	cout << "Введите количество столбцов n: ";
	cin >> n;

	int a[100][100];
	inputMatrix(a, m, n);

	int sumMax = sumOfMaxValues(a, m, n);

	cout << "Сумма всех максимальных значений: " << sumMax << endl;

	return 0;
}

//Дана действительная матрица размера m*n. Найти сумму наибольших значений элементов ее строк
//через Функции

//Я вынес расчет максимального значения строки и суммы максимальных значений в отдельные функции
//Теперь код разбит на функции для ввода матрицы, нахождения максимального значения строки и подсчета суммы максимальных значений