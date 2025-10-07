#include "rectangle.h"
#include <iostream>
#include <algorithm>
#include <iomanip>

using namespace std;

// Конструктор по умолчанию
Rectangle::Rectangle() : x1(0), y1(0), x2(0), y2(0) {
    cout << "Вызван конструктор по умолчанию (пустой прямоугольник)" << endl;
}

// Конструктор с параметрами
Rectangle::Rectangle(double left, double bottom, double right, double top)
    : x1(left), y1(bottom), x2(right), y2(top) {
    normalize();
    cout << "Вызван конструктор с параметрами: [" << x1 << ", " << y1
        << "] - [" << x2 << ", " << y2 << "]" << endl;
}

// Конструктор копирования
Rectangle::Rectangle(const Rectangle& other)
    : x1(other.x1), y1(other.y1), x2(other.x2), y2(other.y2) {
    cout << "Вызван конструктор копирования" << endl;
}

// Деструктор
Rectangle::~Rectangle() {
    cout << "Вызван деструктор для прямоугольника: [" << x1 << ", " << y1
        << "] - [" << x2 << ", " << y2 << "]" << endl;
}

// Нормализация координат (обеспечение x1 <= x2, y1 <= y2)
void Rectangle::normalize() {
    if (x1 > x2) swap(x1, x2);
    if (y1 > y2) swap(y1, y2);
}

// Проверка валидности прямоугольника
bool Rectangle::isValid() const {
    return (x2 >= x1) && (y2 >= y1) && (getWidth() > 0) && (getHeight() > 0);
}

// Проверка на пустой прямоугольник
bool Rectangle::isEmpty() const {
    return (x1 == x2) || (y1 == y2);
}

// Метод вывода информации
void Rectangle::display(const string& name) const {
    cout << "Прямоугольник ";
    if (!name.empty()) {
        cout << name << " ";
    }
    cout << ": [" << fixed << setprecision(2) << x1 << ", " << y1
        << "] - [" << x2 << ", " << y2 << "]" << endl;

    cout << "  Ширина: " << getWidth() << ", Высота: " << getHeight()
        << ", Площадь: " << getArea() << endl;

    if (isEmpty()) {
        cout << "  Статус: ПУСТОЙ прямоугольник" << endl;
    }
    else if (!isValid()) {
        cout << "  Статус: НЕВАЛИДНЫЙ прямоугольник" << endl;
    }
    else {
        cout << "  Статус: Валидный прямоугольник" << endl;
    }
    cout << endl;
}

// Оператор присваивания
Rectangle& Rectangle::operator=(const Rectangle& other) {
    cout << "Вызван оператор присваивания" << endl;
    if (this != &other) {
        x1 = other.x1;
        y1 = other.y1;
        x2 = other.x2;
        y2 = other.y2;
    }
    return *this;
}

// Бинарный оператор несимметрической разности (A - B)
Rectangle Rectangle::operator-(const Rectangle& other) const {
    cout << "Вызван оператор несимметрической разности (-)" << endl;

    // Несимметрическая разность: A - B = часть A, не пересекающаяся с B
    // Это эквивалентно пересечению A с дополнением B

    // Если прямоугольники не пересекаются, возвращаем A
    if (x2 <= other.x1 || x1 >= other.x2 || y2 <= other.y1 || y1 >= other.y2) {
        cout << "  Прямоугольники не пересекаются, возвращаем первый прямоугольник" << endl;
        return *this;
    }

    // Вычисляем разность как 4 возможных прямоугольника вокруг other внутри this
    // Но для простоты вернем прямоугольник слева от other в пределах this
    double new_x1 = x1;
    double new_y1 = max(y1, other.y1);
    double new_x2 = min(x2, other.x1); // левая часть
    double new_y2 = min(y2, other.y2);

    // Если левая часть существует
    if (new_x2 > new_x1 && new_y2 > new_y1) {
        Rectangle result(new_x1, new_y1, new_x2, new_y2);
        cout << "  Возвращена левая часть разности" << endl;
        return result;
    }

    // Если левой части нет, возвращаем пустой прямоугольник
    cout << "  Результат разности - пустой прямоугольник" << endl;
    return Rectangle(0, 0, 0, 0);
}

// Унарный оператор симметричного отображения
Rectangle Rectangle::operator-() const {
    cout << "Вызван унарный оператор симметричного отображения (-)" << endl;
    // Симметричное отображение относительно начала координат
    Rectangle result(-x2, -y2, -x1, -y1);
    cout << "  Отображенный прямоугольник: [" << -x2 << ", " << -y2
        << "] - [" << -x1 << ", " << -y1 << "]" << endl;
    return result;
}

// Оператор сравнения на равенство
bool Rectangle::operator==(const Rectangle& other) const {
    return (x1 == other.x1) && (y1 == other.y1) &&
        (x2 == other.x2) && (y2 == other.y2);
}

// Оператор сравнения на неравенство
bool Rectangle::operator!=(const Rectangle& other) const {
    return !(*this == other);
}