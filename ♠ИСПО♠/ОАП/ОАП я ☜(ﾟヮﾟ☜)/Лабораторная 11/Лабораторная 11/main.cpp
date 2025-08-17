#include <iostream>
#include <time.h>

template <typename T, typename U, typename V, typename W>
U subtractAndReturn(T a, U b, V c, W d);

int main() {
	int a = 5;
	double b = 2.5;
	float c = 1.5;
	int d = 10;

	double Result = subtractAndReturn(a, b, c, d);

	std::cout << "Result: " << Result << std::endl;

	return 0;
}

template <typename T, typename U, typename V, typename W>
U subtractAndReturn(T a, U b, V c, W d) {
	return d - (a + b + c);
}
