#include <iostream>
#include<cmath>

int main()
{
	double A = 8;
	double B = 5.6;
	double pi = 3.14;
	double Y = 2 * A * asin(pi / B);
	std::cout << "Y = " << Y << std::endl;
	return 0;
}