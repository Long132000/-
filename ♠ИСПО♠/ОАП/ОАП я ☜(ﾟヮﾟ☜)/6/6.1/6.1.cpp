#include <iostream>
#include <string>

int main() {

	setlocale(LC_ALL, "RUS");

	std::string text = "Алфавит Арбуз Автомобиль Банан Книга Апельсин";
	std::string word;

	for (size_t i = 0; i < text.length(); i++) {
		if (text[i] == 'А' or text[i] == 'а') {
			word = "";
			while (i < text.length() && text[i] != ' ') {
				word += text[i];
				i++;
			}
			std::cout << word << std::endl;
		}
	}

	return 0;
}