#ifndef MYSTRING_H
#define MYSTRING_H

#include <iostream>
#include <cstring>
#include <fstream>

class MyString {
private:
    char* str;    // указатель на строку в динамической памяти
    int length;   // длина строки

public:
    // Конструкторы
    MyString();                               // без параметров
    MyString(const char* s);                  // с параметрами
    MyString(const MyString& other);          // копирования

    // Деструктор
    ~MyString();

    // Методы
    void set(const char* s);                  // ввод строки
    void update();                            // изменение строки по варианту
    void print() const;                       // вывод строки

    // Оператор присваивания
    MyString& operator=(const MyString& other);

    // Вспомогательные методы
    int getLength() const { return length; }
    const char* getString() const { return str; }
    bool isEmpty() const { return str == nullptr || length == 0; }

private:
    void allocateMemory(int size);            // выделение памяти
    void deallocateMemory();                  // освобождение памяти
    void saveToFile(const char* description) const; // сохранение в файл
};

// ВСЕ РЕАЛИЗАЦИИ ПЕРЕНЕСЕМ В .CPP ФАЙЛ

#endif