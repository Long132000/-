#include <iostream>

int main() {
	setlocale(LC_ALL, "rus");
	double number;
	int zeroCount = 0;
	double sumInRange = 0;

	// Ввод чисел и обработка
	std::cout << "Введите 10 вещественных чисел:\n";
	for (int i = 0; i < 10; i++) {
		std::cin >> number;

		if (number == 0) {
			zeroCount++;
		}
		if (number >= -15 && number <= 15) {
			sumInRange += number;
		}
	}

	// Вывод результатов
	std::cout << "Количество чисел, равных нулю: " << zeroCount << std::endl;
	std::cout << "Сумма чисел в диапазоне [-15, 15]: " << sumInRange << std::endl;

	return 0;
}