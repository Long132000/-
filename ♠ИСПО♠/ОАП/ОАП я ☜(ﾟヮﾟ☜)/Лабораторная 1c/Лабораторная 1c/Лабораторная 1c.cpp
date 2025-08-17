#include <stdio.h>
#include<math.h>

int main()
{
	double A = 8;
	double B = 5.6;
	double pi = 3.14;
	double Y = 2 * A * asin(pi / B);
	printf("Y = %f\n", Y);
	return 0;
}