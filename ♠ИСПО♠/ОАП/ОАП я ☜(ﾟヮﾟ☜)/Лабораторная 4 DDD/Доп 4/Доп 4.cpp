#include <iostream>

using namespace std;
int main() {
	setlocale(LC_ALL, "rus");
	const int size =10;
	double numbers[size];

	// Ввод чисел
	cout << "Введите 10 вещественных чисел:\n";
	for (int i = 0; i < size; i++) {
		cin >> numbers[i];
	}

	int zeroCount = 0;
	double sumInRange = 0;

	// Подсчет количества чисел, равных нулю, и суммы чисел в диапазоне [-15, 15]
	for (int i = 0; i < size; i++) {
		if (numbers[i] == 0) {
			zeroCount++;
		}
		if (numbers[i] >= -15 && numbers[i] <= 15) {
			sumInRange += numbers[i];
		}
	}

	int cnt = 0;
	int max;
	max = numbers[0];
	for (int o = 0; o <  size; o++) {
		if (numbers[o] > max) {
			max = numbers[o];
			//numbers[o] = 1;
			//cnt++; 

		}
		
	}
	for (int o = 0; o < size; o++) {
           if (numbers[o] == max) {
			cnt++;
			numbers[o] = 1;
		}
	}


	for (int i = 0; i < 10; i++) {
		cout << numbers[i] << " ";
	}
	cout << endl;
	cout << cnt << endl;

	// Вывод результатов
	cout << "Количество чисел, равных нулю: " << zeroCount << endl;
	cout << "Сумма чисел в диапазоне [-15, 15]: " << sumInRange << endl;

	return 0;
}