#include <iostream>
using namespace std;

int main() {
	setlocale(LC_ALL, "rus");
	int choice;
	int a, b;

	do {
		cout << "Введите число : 1, 2, 4 или 6. Число 6 закроет программу : ";
		cin >> choice;

		if (choice > 6) {
			continue;
		}

		switch (choice) {
		case 1:
			cout << "Привет" << endl;
			break;
		case 2:
			cout << "Конец" << endl;
			break;
		case 4:
			cout << "Введите значение a : ";
			cin >> a;
			cout << "Введите значение b : ";
			cin >> b;
			cout << "Сумма a+b: " << a + b << endl;
			break;
		case 6:
			cout << "Закрыть программу" << endl;
			return 0;
		default:
			cout << "Неверный ввод, пожалуйста, попробуйте снова. Необходимо ввести 1, 2, 4 или 6." << endl;
			break;

		}
	} while (true);
		return 0;
}