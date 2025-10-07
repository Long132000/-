#ifndef TRIANGLE_H
#define TRIANGLE_H

#include <iostream>
#include <cmath>
#include <string>


// Определяем константу PI если она не определена
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

class Triangle {
private:
    double side1, side2, side3;

public:
    // Конструкторы
    Triangle();
    Triangle(double s1, double s2, double s3);

    // Методы установки свойств
    bool setSides(double s1, double s2, double s3);

    // Операции с треугольником
    void scale(double factor);  // увеличение/уменьшение сторон
    void scaleByPercent(double percent);  // изменение на процент
    double perimeter() const;   // вычисление периметра
    double area() const;        // вычисление площади
    void calculateAngles(double& angleA, double& angleB, double& angleC) const;  // углы
    std::string getTriangleTypeByAngles() const;  // тип по углам
    std::string getTriangleTypeBySides() const;   // тип по сторонам

    // Вспомогательные методы
    void display() const;
    bool isValid() const;

private:
    bool isValidTriangle(double a, double b, double c) const;
};

#endif
// Конструктор по умолчанию
Triangle::Triangle() : side1(0), side2(0), side3(0) {
    std::cout << "Создан треугольник по умолчанию" << std::endl;
}

// Конструктор с параметрами
Triangle::Triangle(double s1, double s2, double s3) {
    std::cout << "Создан треугольник с параметрами" << std::endl;
    if (setSides(s1, s2, s3)) {
        std::cout << "Треугольник успешно создан" << std::endl;
    }
    else {
        std::cout << "Треугольник создан с нулевыми сторонами" << std::endl;
    }
}

// Проверка валидности треугольника
bool Triangle::isValidTriangle(double a, double b, double c) const {
    return (a > 0 && b > 0 && c > 0) &&
        (a + b > c) && (a + c > b) && (b + c > a);
}

// Установка сторон треугольника
bool Triangle::setSides(double s1, double s2, double s3) {
    if (isValidTriangle(s1, s2, s3)) {
        side1 = s1;
        side2 = s2;
        side3 = s3;
        return true;
    }
    std::cout << "Ошибка: Недопустимые стороны треугольника ("
        << s1 << ", " << s2 << ", " << s3 << ")" << std::endl;
    return false;
}

// Увеличение/уменьшение размера сторон
void Triangle::scale(double factor) {
    if (factor > 0) {
        side1 *= factor;
        side2 *= factor;
        side3 *= factor;
        std::cout << "Стороны изменены в " << factor << " раз" << std::endl;
    }
    else {
        std::cout << "Ошибка: коэффициент должен быть положительным" << std::endl;
    }
}

// Изменение размера на процент
void Triangle::scaleByPercent(double percent) {
    double factor = 1.0 + percent / 100.0;
    if (factor > 0) {
        scale(factor);
    }
    else {
        std::cout << "Ошибка: недопустимый процент" << std::endl;
    }
}

// Вычисление периметра
double Triangle::perimeter() const {
    return side1 + side2 + side3;
}

// Вычисление площади по формуле Герона
double Triangle::area() const {
    if (!isValid()) return 0;
    double p = perimeter() / 2;
    return sqrt(p * (p - side1) * (p - side2) * (p - side3));
}

// Вычисление углов треугольника
void Triangle::calculateAngles(double& angleA, double& angleB, double& angleC) const {
    if (!isValid()) {
        angleA = angleB = angleC = 0;
        return;
    }

    // Угол A против стороны a (side1)
    angleA = acos((side2 * side2 + side3 * side3 - side1 * side1) / (2 * side2 * side3)) * 180 / M_PI;
    // Угол B против стороны b (side2)
    angleB = acos((side1 * side1 + side3 * side3 - side2 * side2) / (2 * side1 * side3)) * 180 / M_PI;
    // Угол C против стороны c (side3)
    angleC = 180 - angleA - angleB;
}

// Определение типа треугольника по углам
std::string Triangle::getTriangleTypeByAngles() const {
    if (!isValid()) return "Невалидный";

    double a, b, c;
    calculateAngles(a, b, c);

    if (a < 90 && b < 90 && c < 90) {
        return "Остроугольный";
    }
    else if (a == 90 || b == 90 || c == 90) {
        return "Прямоугольный";
    }
    else {
        return "Тупоугольный";
    }
}

// Определение типа треугольника по сторонам
std::string Triangle::getTriangleTypeBySides() const {
    if (!isValid()) return "Невалидный";

    if (side1 == side2 && side2 == side3) {
        return "Равносторонний";
    }
    else if (side1 == side2 || side1 == side3 || side2 == side3) {
        return "Равнобедренный";
    }
    else {
        return "Разносторонний";
    }
}

// Проверка валидности треугольника
bool Triangle::isValid() const {
    return isValidTriangle(side1, side2, side3);
}

// Вывод информации о треугольнике
void Triangle::display() const {
    std::cout << "Треугольник со сторонами: "
        << side1 << ", " << side2 << ", " << side3 << std::endl;

    if (isValid()) {
        std::cout << "Периметр: " << perimeter() << std::endl;
        std::cout << "Площадь: " << area() << std::endl;

        double angleA, angleB, angleC;
        calculateAngles(angleA, angleB, angleC);
        std::cout << "Углы: " << angleA << "°, " << angleB << "°, " << angleC << "°" << std::endl;
        std::cout << "Тип по сторонам: " << getTriangleTypeBySides() << std::endl;
        std::cout << "Тип по углам: " << getTriangleTypeByAngles() << std::endl;
    }
    else {
        std::cout << "Треугольник невалиден!" << std::endl;
    }
    std::cout << "------------------------" << std::endl;
}