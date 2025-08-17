#include <iostream>
#include <sstream>
#include <cmath>

// Функция для выполнения операции
double calculate(double num1, double num2, char op) {
	switch (op) {
	case '+':
		return num1 + num2;
	case '-':
		return num1 - num2;
	case '*':
		return num1 * num2;
	case '/':
		if (num2 != 0) {
			return num1 / num2;
		}
		else {
			throw "Деление на ноль!";
		}
	case '^':
		return pow(num1, num2);
	default:
		throw "Неверная операция!";
	}
}

int main() {
	setlocale(LC_ALL, "rus");
	char op;
	double num1, num2;
	std::string input;

	std::cout << "Введите операцию (например, 2 + 3): ";
	std::getline(std::cin, input);

	std::istringstream iss(input);
	iss >> num1 >> op >> num2;

	try {
		double result = calculate(num1, num2, op);
		std::cout << "Результат: " << result << std::endl;
	}
	catch (const char* error) {
		std::cerr << "Ошибка: " << error << std::endl;
	}

	return 0;
}