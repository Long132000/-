#include <iostream>
#include <vector>
#include <string>

std::vector<std::string> findFilePaths(const std::string &fileNameToFind) {
	// здесь должен быть ваш код для поиска пути к файлам
	// например, можно использовать функции для поиска файлов в файловой системе
	// и добавить найденные пути в вектор
	std::vector<std::string> paths;
	// пример заполнения вектора
	paths.push_back("/boot/default/grub.d");
	paths.push_back("/etc/grub.d");

	return paths;
}

int main() {
	setlocale(LC_ALL, "rus");
	std::string fileName;
	std::cout << "Введите имя файла для поиска: ";
	std::getline(std::cin, fileName);

	std::vector<std::string> paths = findFilePaths(fileName);

	if (paths.empty()) {
		std::cout << "Файл не найден" << std::endl;
	}
	else {
		std::cout << "Найденные пути:" << std::endl;
		for (const std::string &path : paths) {
			std::cout << path << std::endl;
		}
	}

	return 0;
}
