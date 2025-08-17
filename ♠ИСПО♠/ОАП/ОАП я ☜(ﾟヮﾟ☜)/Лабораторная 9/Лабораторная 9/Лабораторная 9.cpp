#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

void swapAdjacentWords(std::vector<std::string>& words) {
	for (size_t i = 0; i < words.size() - 1; i += 2) {
		std::swap(words[i], words[i + 1]);
	}
}

int main() {
	setlocale(LC_ALL, "rus");

	std::ofstream outFile("output.txt", std::ios::app); // Открываем файл для дозаписи

	if (!outFile.is_open()) {
		std::cerr << "Ошибка при открытии файла\n";
		return 1;
	}

	std::string input;
	while (true) {
		std::cout << "Введите строку (для завершения введите пустую строку): ";
		std::getline(std::cin, input);

		if (input.empty()) {
			break; // Выход из цикла если строка пустая
		}

		outFile << input << std::endl; // Запись строки в файл
	}

	outFile.close();

	std::cout << "Введенные строки сохранены в файл output.txt\n";

	return 0;
}
