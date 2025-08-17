//#include <iostream>
//
//using namespace std;
//
//int main()
//{
//	setlocale(LC_ALL, "rus");
//
//	double x, y;
//	cout << "Введите координаты точки : \n";
//	cin >> x >> y;
//	if ((0 < y < 0.2) && (x*x + y * y < 1)) cout << "Точка принадлежит области/n";
//	else if ((y < 0 || y > 0.2) || (x*x + y * y > 1)) cout << "Точка не принадлежит области\n";
//	else cout << "Точка лежит на границе области\n";
//}

#include <iostream>

using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");

	double x, y;
	cout << "Введите координаты точки : \n";
	cin >> x >> y;
	if ((0 < y < 0.2) && (x*x + y * y < 1)) cout << "Точка принадлежит области/n";
	else if ((y < 0 || y > 0.2) || (x*x + y * y > 1)) cout << "Точка не принадлежит области\n";
	else cout << "Точка лежит на границе области\n";
}