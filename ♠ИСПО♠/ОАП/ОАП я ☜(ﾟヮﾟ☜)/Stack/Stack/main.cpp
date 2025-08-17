#include <stack>
#include <time.h>
#include <iostream>

int main() {
	std::stack<int> mystack;
	for (int i = 0; i != 5; i++) {
		int value = rand() % 9 + 1;
		mystack.push(value);
		std::cout << value << " ";
	}
	std::cout << "\n";
	std::cout << mystack.top() << std::endl;
	mystack.pop();
	std::cout << mystack.top() << std::endl;
	return 0;
}