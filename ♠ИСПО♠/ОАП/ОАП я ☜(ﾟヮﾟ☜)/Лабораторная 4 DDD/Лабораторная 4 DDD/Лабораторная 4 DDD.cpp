#include <iostream>

int main() {
	setlocale (LC_ALL, "rus");
	const int size = 10;
	double numbers[size];

	// Ввод чисел
	std::cout << "Введите 10 вещественных чисел:\n";
	for (int i = 0; i < size; i++) {
		std::cin >> numbers[i];
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

	// Вывод результатов
	std::cout << "Количество чисел, равных нулю: " << zeroCount << std::endl;
	std::cout << "Сумма чисел в диапазоне [-15, 15]: " << sumInRange << std::endl;

	return 0;
}