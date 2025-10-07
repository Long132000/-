#include <iostream>
#include <vector>
#include <clocale>  // для setlocale
#include <limits>   // для numeric_limits
#include "triangle.h"

using namespace std;

void displayMenu() {
    cout << "\n=== МЕНЮ РАБОТЫ С ТРЕУГОЛЬНИКАМИ ===" << endl;
    cout << "1. Добавить треугольник" << endl;
    cout << "2. Показать все треугольники" << endl;
    cout << "3. Изменить размер треугольника" << endl;
    cout << "4. Вычислить периметр треугольника" << endl;
    cout << "5. Вычислить площадь треугольника" << endl;
    cout << "6. Определить углы треугольника" << endl;
    cout << "7. Определить тип треугольника" << endl;
    cout << "8. Выход" << endl;
    cout << "Выберите действие: ";
}

void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

int main() {
    // Установка русской локали
    setlocale(LC_ALL, "rus");

    cout << "ПРАКТИЧЕСКАЯ РАБОТА №1: ПРОЕКТИРОВАНИЕ КЛАССОВ" << endl;
    cout << "Класс: Triangle (Треугольник)" << endl;

    vector<Triangle> triangles;
    int choice;

    do {
        displayMenu();
        cin >> choice;

        // Очистка буфера после ввода числа
        if (cin.fail()) {
            cout << "Ошибка ввода! Пожалуйста, введите число от 1 до 8." << endl;
            clearInputBuffer();
            continue;
        }
        clearInputBuffer();

        switch (choice) {
        case 1: {
            double s1, s2, s3;
            cout << "Введите три стороны треугольника: ";
            cin >> s1 >> s2 >> s3;

            if (cin.fail()) {
                cout << "Ошибка ввода! Пожалуйста, введите числа." << endl;
                clearInputBuffer();
                break;
            }

            Triangle t(s1, s2, s3);
            triangles.push_back(t);
            cout << "Треугольник добавлен в массив. Всего треугольников: "
                << triangles.size() << endl;
            break;
        }

        case 2: {
            if (triangles.empty()) {
                cout << "Массив треугольников пуст!" << endl;
            }
            else {
                cout << "\nСПИСОК ТРЕУГОЛЬНИКОВ:" << endl;
                for (size_t i = 0; i < triangles.size(); i++) {
                    cout << "Треугольник #" << (i + 1) << ":" << endl;
                    triangles[i].display();
                }
            }
            break;
        }

        case 3: {
            if (triangles.empty()) {
                cout << "Массив треугольников пуст!" << endl;
                break;
            }

            int index;
            cout << "Введите номер треугольника (1-" << triangles.size() << "): ";
            cin >> index;

            if (cin.fail() || index < 1 || index > static_cast<int>(triangles.size())) {
                cout << "Неверный номер!" << endl;
                clearInputBuffer();
                break;
            }

            double factor;
            cout << "Введите коэффициент изменения (например, 2 для увеличения в 2 раза): ";
            cin >> factor;

            if (cin.fail()) {
                cout << "Ошибка ввода! Пожалуйста, введите число." << endl;
                clearInputBuffer();
                break;
            }

            triangles[index - 1].scale(factor);
            cout << "Треугольник изменен:" << endl;
            triangles[index - 1].display();
            break;
        }

        case 4: {
            if (triangles.empty()) {
                cout << "Массив треугольников пуст!" << endl;
                break;
            }

            int index;
            cout << "Введите номер треугольника (1-" << triangles.size() << "): ";
            cin >> index;

            if (cin.fail() || index < 1 || index > static_cast<int>(triangles.size())) {
                cout << "Неверный номер!" << endl;
                clearInputBuffer();
                break;
            }

            cout << "Периметр треугольника: " << triangles[index - 1].perimeter() << endl;
            break;
        }

        case 5: {
            if (triangles.empty()) {
                cout << "Массив треугольников пуст!" << endl;
                break;
            }

            int index;
            cout << "Введите номер треугольника (1-" << triangles.size() << "): ";
            cin >> index;

            if (cin.fail() || index < 1 || index > static_cast<int>(triangles.size())) {
                cout << "Неверный номер!" << endl;
                clearInputBuffer();
                break;
            }

            cout << "Площадь треугольника: " << triangles[index - 1].area() << endl;
            break;
        }

        case 6: {
            if (triangles.empty()) {
                cout << "Массив треугольников пуст!" << endl;
                break;
            }

            int index;
            cout << "Введите номер треугольника (1-" << triangles.size() << "): ";
            cin >> index;

            if (cin.fail() || index < 1 || index > static_cast<int>(triangles.size())) {
                cout << "Неверный номер!" << endl;
                clearInputBuffer();
                break;
            }

            double a, b, c;
            triangles[index - 1].calculateAngles(a, b, c);
            cout << "Углы треугольника: " << a << "°, " << b << "°, " << c << "°" << endl;
            break;
        }

        case 7: {
            if (triangles.empty()) {
                cout << "Массив треугольников пуст!" << endl;
                break;
            }

            int index;
            cout << "Введите номер треугольника (1-" << triangles.size() << "): ";
            cin >> index;

            if (cin.fail() || index < 1 || index > static_cast<int>(triangles.size())) {
                cout << "Неверный номер!" << endl;
                clearInputBuffer();
                break;
            }

            cout << "Тип по сторонам: " << triangles[index - 1].getTriangleTypeBySides() << endl;
            cout << "Тип по углам: " << triangles[index - 1].getTriangleTypeByAngles() << endl;
            break;
        }

        case 8:
            cout << "Выход из программы..." << endl;
            break;

        default:
            cout << "Неверный выбор! Пожалуйста, введите число от 1 до 8." << endl;
        }

    } while (choice != 8);

    return 0;
}