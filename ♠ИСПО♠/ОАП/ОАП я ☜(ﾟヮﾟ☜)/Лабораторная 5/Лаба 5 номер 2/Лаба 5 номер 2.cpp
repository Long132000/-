#include <iostream>
using namespace std;

int main() {
	setlocale(LC_ALL, "rus");
	int m, n;
	cout << "Введите количество строк m: ";
	cin >> m;
	cout << "Введите количество столбцов n: ";
	cin >> n;

	int a[100][100];
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout << "Введите элемент a[" << i << "][" << j << "]: ";
			cin >> a[i][j];
		}
	}

	int sumMax = 0;

	for (int i = 0; i < m; i++) {
		int max = *(*(a + i));
		for (int j = 1; j < n; j++) {
			if (*(*(a + i) + j) > max) {
				max = *(*(a + i) + j);

			}
		}

		cout << "Максимальное значение в " << i + 1 << "-й строке: " << max << endl;
		sumMax += max;

	}
	cout << "Сумма всех максимальных значений: " << sumMax << endl;
	return 0;
}
