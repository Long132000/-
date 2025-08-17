#include <iostream>
#include <string>
#include <sstream>
#include <windows.h>

int main() {
	setlocale(LC_ALL, "ru");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	std::string text;
	std::cout << "Введите произвольный текст: "; //типа ввод текста
	std::getline(std::cin, text);
	std::stringstream ss(text); //поток
	std::string firstWord, secondWord, thirdWord; //переменные для хранения
	ss >> firstWord; //мусорное слово сорииии
	ss >> secondWord;//извлекаем уже норм слово и тд
	ss >> thirdWord;

	std::stringstream ssreader(text);
	std::string word;
	int count = 0;
	while (ssreader >> word) {
		/*for (char i : word) {*/
			if (word[0] == 'g' || word[0] == 'G') {
			/*	count++;
			}*/
				std::cout << word << "\n";
		}
	}

		
	std::cout << "Количество букв 'g' в строке: " << std::endl;


	std::cout << "Второе слово: " << //Пора пожалуй их вывести
		secondWord << std::endl;
	std::cout << "Третье слво: " <<
		thirdWord << std::endl;

	return 0;
}