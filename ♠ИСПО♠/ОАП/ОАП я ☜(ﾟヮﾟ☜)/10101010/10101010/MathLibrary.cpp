
// pch.cpp: файл исходного кода, соответствующий предварительно скомпилированному заголовочному файлу

#include "pch.h"

namespace MathLibrary
{
	double Arithmetic::Add(double a, double b)
	{
		return a + b;
	}

	double Arithmetic::Subtract(double a, double b)
	{
		return a - b;
	}

	double Arithmetic::Multiply(double a, double b)
	{
		return a * b;
	}

	double Arithmetic::Divide(double a, double b)
	{
		return a / b;
	}
}

// При использовании предварительн