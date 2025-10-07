// Добавьте эту строку в САМОМ НАЧАЛЕ файла для отключения предупреждений безопасности
#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include "mystring.h"

using namespace std;

void displayMenu() {
    cout << "\n=== ДЕМОНСТРАЦИЯ КЛАССА MyString ===" << endl;
    cout << "1. Создать строку конструктором с параметрами" << endl;
    cout << "2. Создать строку конструктором копирования" << endl;
    cout << "3. Изменить строку методом set()" << endl;
    cout << "4. Применить метод update() к строке" << endl;
    cout << "5. Вывести строку методом print()" << endl;
    cout << "6. Показать работу оператора присваивания" << endl;
    cout << "7. Демонстрация всех возможностей" << endl;
    cout << "8. Выход" << endl;
    cout << "Выберите действие: ";
}

void demonstration() {
    cout << "\n*** ПОЛНАЯ ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА ***" << endl;

    cout << "\n1. Создание строк конструктором с параметрами:" << endl;
    MyString str1("Hello World!");
    MyString str2("Programming");

    cout << "\n2. Создание строки конструктором копирования:" << endl;
    MyString str3 = str1;

    cout << "\n3. Изменение строки методом set():" << endl;
    str2.set("New String Value");

    cout << "\n4. Вывод всех строк:" << endl;
    str1.print();
    str2.print();
    str3.print();

    cout << "\n5. Применение метода update():" << endl;
    cout << "Для str1 (нечетная длина):" << endl;
    str1.update();
    cout << "Для str2 (четная длина):" << endl;
    str2.update();

    cout << "\n6. Работа оператора присваивания:" << endl;
    MyString str4;
    str4 = str1;
    str4.print();

    cout << "\n7. Проверка файла strings.txt:" << endl;
    cout << "Все операции сохранены в файл strings.txt" << endl;
}

int main() {
    setlocale(LC_ALL, "rus");

    cout << "ПРАКТИЧЕСКАЯ РАБОТА №3: КОНСТРУКТОРЫ И ДЕСТРУКТОРЫ" << endl;
    cout << "Класс: MyString" << endl;

    // Очистка файла при запуске
    ofstream file("strings.txt", ios::trunc);
    file.close();

    MyString* currentString = nullptr;
    int choice;

    do {
        displayMenu();
        cin >> choice;
        cin.ignore(); // очистка буфера

        switch (choice) {
        case 1: {
            char input[256];
            cout << "Введите строку: ";
            cin.getline(input, 256);

            if (currentString != nullptr) {
                delete currentString;
            }
            currentString = new MyString(input);
            break;
        }

        case 2: {
            if (currentString == nullptr) {
                cout << "Сначала создайте исходную строку!" << endl;
            }
            else {
                MyString* copy = new MyString(*currentString);
                cout << "Создана копия:" << endl;
                copy->print();
                delete copy;
            }
            break;
        }

        case 3: {
            if (currentString == nullptr) {
                cout << "Сначала создайте строку!" << endl;
            }
            else {
                char input[256];
                cout << "Введите новую строку: ";
                cin.getline(input, 256);
                currentString->set(input);
            }
            break;
        }

        case 4: {
            if (currentString == nullptr) {
                cout << "Сначала создайте строку!" << endl;
            }
            else {
                currentString->update();
                cout << "Результат:" << endl;
                currentString->print();
            }
            break;
        }

        case 5: {
            if (currentString == nullptr) {
                cout << "Строка не создана!" << endl;
            }
            else {
                currentString->print();
            }
            break;
        }

        case 6: {
            if (currentString == nullptr) {
                cout << "Сначала создайте строку!" << endl;
            }
            else {
                MyString assigned;
                assigned = *currentString;
                cout << "Результат присваивания:" << endl;
                assigned.print();
            }
            break;
        }

        case 7: {
            demonstration();
            break;
        }

        case 8:
            cout << "Выход из программы..." << endl;
            break;

        default:
            cout << "Неверный выбор! Попробуйте снова." << endl;
        }

    } while (choice != 8);

    if (currentString != nullptr) {
        delete currentString;
    }

    return 0;
}