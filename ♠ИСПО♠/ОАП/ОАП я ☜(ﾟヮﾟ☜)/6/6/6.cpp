#include <iostream>
#include <string>
using namespace std;
int main() {
	setlocale(LC_ALL, "Russian");
	string text = "Аллея, сад, апельсин, арбуз, зонт";

	string word;
	for (int i = 0;i<text.length();i++){
		if (text[i] != ' '&&text[i] != ','&& text[i] != '.'&& text[i] != '!'&& text[i] != '?') {
			word+=text[i];
		}
		else {
			if (word.length() > 0 && (word[0] == 'А' or word[0]== 'а')) {
				cout<<word<<endl;
				 
			}
			word = "";
		}
		
	}
	return 0;
}