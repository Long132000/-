#ifndef RECTANGLE_H
#define RECTANGLE_H

#include <iostream>
#include <algorithm>

class Rectangle {
private:
    double x1, y1; // левый нижний угол
    double x2, y2; // правый верхний угол

public:
    // Конструкторы
    Rectangle(); // по умолчанию
    Rectangle(double left, double bottom, double right, double top); // с параметрами
    Rectangle(const Rectangle& other); // копирования

    // Деструктор
    ~Rectangle();

    // Методы доступа
    double getLeft() const { return x1; }
    double getBottom() const { return y1; }
    double getRight() const { return x2; }
    double getTop() const { return y2; }
    double getWidth() const { return x2 - x1; }
    double getHeight() const { return y2 - y1; }
    double getArea() const { return getWidth() * getHeight(); }

    // Проверка валидности
    bool isValid() const;
    bool isEmpty() const;

    // Метод вывода информации
    void display(const std::string& name = "") const;

    // Перегрузка операторов
    Rectangle& operator=(const Rectangle& other); // оператор присваивания

    // Бинарный оператор несимметрической разности
    Rectangle operator-(const Rectangle& other) const;

    // Унарный оператор симметричного отображения
    Rectangle operator-() const;

    // Дополнительные операторы для демонстрации
    bool operator==(const Rectangle& other) const;
    bool operator!=(const Rectangle& other) const;

private:
    void normalize(); // нормализация координат
};

#endif