#include "mystring.h"
#include <iostream>
#include <cstring>
#include <fstream>
#include <cctype>

using namespace std;

// Конструктор без параметров
MyString::MyString() : str(nullptr), length(0) {
    cout << "Вызван конструктор по умолчанию" << endl;
}

// Конструктор с параметрами
MyString::MyString(const char* s) {
    cout << "Вызван конструктор с параметрами" << endl;
    if (s != nullptr) {
        length = static_cast<int>(strlen(s)); // явное преобразование в int
        allocateMemory(length + 1);
        // Безопасное копирование
        if (str != nullptr) {
            strcpy_s(str, length + 1, s); // используем безопасную версию
        }
        cout << "Создана строка: \"" << str << "\" (длина: " << length << ")" << endl;
    }
    else {
        str = nullptr;
        length = 0;
        cout << "Создана пустая строка" << endl;
    }
}

// Конструктор копирования
MyString::MyString(const MyString& other) {
    cout << "Вызван конструктор копирования" << endl;
    if (other.str != nullptr) {
        length = other.length;
        allocateMemory(length + 1);
        // Безопасное копирование
        if (str != nullptr && other.str != nullptr) {
            strcpy_s(str, length + 1, other.str);
        }
        cout << "Скопирована строка: \"" << str << "\"" << endl;
    }
    else {
        str = nullptr;
        length = 0;
    }
}

// Деструктор
MyString::~MyString() {
    cout << "Вызван деструктор для строки: ";
    if (str != nullptr) {
        cout << "\"" << str << "\"";
    }
    else {
        cout << "null";
    }
    cout << endl;
    deallocateMemory();
}

// Оператор присваивания
MyString& MyString::operator=(const MyString& other) {
    cout << "Вызван оператор присваивания" << endl;
    if (this != &other) {
        deallocateMemory();
        if (other.str != nullptr) {
            length = other.length;
            allocateMemory(length + 1);
            // Безопасное копирование
            if (str != nullptr && other.str != nullptr) {
                strcpy_s(str, length + 1, other.str);
            }
        }
        else {
            str = nullptr;
            length = 0;
        }
    }
    return *this;
}

// Метод ввода строки
void MyString::set(const char* s) {
    cout << "Вызван метод set()" << endl;
    deallocateMemory();
    if (s != nullptr) {
        length = static_cast<int>(strlen(s)); // явное преобразование
        allocateMemory(length + 1);
        // Безопасное копирование
        if (str != nullptr) {
            strcpy_s(str, length + 1, s);
        }
        cout << "Установлена строка: \"" << str << "\"" << endl;
    }
    else {
        str = nullptr;
        length = 0;
        cout << "Установлена пустая строка" << endl;
    }
}

// Метод изменения строки (Вариант 1: удаление среднего символа для нечетной длины)
void MyString::update() {
    cout << "Вызван метод update()" << endl;

    if (str == nullptr || length == 0) {
        cout << "Строка пустая, изменений нет" << endl;
        return;
    }

    // Сохраняем исходную строку в файл
    saveToFile("Исходная строка");

    // Вариант 1: Если длина нечетная - удаляем средний символ
    if (length % 2 != 0) {
        int middle = length / 2;
        char* newStr = new char[length]; // на 1 символ меньше

        // Безопасное копирование первой части
        if (newStr != nullptr) {
            strncpy_s(newStr, length, str, middle);
            // Безопасное копирование второй части (после удаленного символа)
            strncpy_s(newStr + middle, length - middle, str + middle + 1, length - middle - 1);
            newStr[length - 1] = '\0';

            deallocateMemory();
            str = newStr;
            length--;

            cout << "Удален средний символ. Новая строка: \"" << str << "\"" << endl;
        }
    }
    else {
        cout << "Длина четная, строка не изменена" << endl;
    }

    // Сохраняем измененную строку в файл
    saveToFile("Измененная строка");
}

// Метод вывода строки
void MyString::print() const {
    cout << "Вызван метод print()" << endl;
    cout << "Строка: \"" << (str != nullptr ? str : "null")
        << "\", Длина: " << length << endl;
}

// Вспомогательный метод для выделения памяти
void MyString::allocateMemory(int size) {
    str = new char[size];
    if (str != nullptr) {
        str[0] = '\0'; // инициализируем пустой строкой
    }
}

// Вспомогательный метод для освобождения памяти
void MyString::deallocateMemory() {
    if (str != nullptr) {
        delete[] str;
        str = nullptr;
    }
    length = 0;
}

// Вспомогательный метод для сохранения в файл
void MyString::saveToFile(const char* description) const {
    ofstream file("strings.txt", ios::app);
    if (file.is_open()) {
        file << description << ": \"" << (str != nullptr ? str : "null") << "\"" << endl;
        file.close();
    }
}