
#include <iostream>

#include "H:\ОАП\10101010\10101010\MathLibrary.h"

using namespace MathLibrary;

int main() {
	std::cout << Arithmetic::Add(1, 2) << std::endl;
	std::cout << Arithmetic::Subtract(2, 1) << std::endl;
	std::cout << Arithmetic::Add(2, 2) << std::endl;
	std::cout << Arithmetic::Divide(9, 3) << std::endl;
	return 0;
}