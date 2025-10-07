#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include "rectangle.h"

using namespace std;

void demonstrateConstructors() {
    cout << "=== ДЕМОНСТРАЦИЯ КОНСТРУКТОРОВ ===" << endl;

    cout << "\n1. Конструктор по умолчанию:" << endl;
    Rectangle rect1;
    rect1.display("rect1");

    cout << "2. Конструктор с параметрами:" << endl;
    Rectangle rect2(1, 1, 5, 4);
    rect2.display("rect2");

    cout << "3. Конструктор копирования:" << endl;
    Rectangle rect3 = rect2;
    rect3.display("rect3");

    cout << "4. Нормализация координат (автоматическая):" << endl;
    Rectangle rect4(5, 4, 1, 1); // координаты в неправильном порядке
    rect4.display("rect4");
}

void demonstrateAssignment() {
    cout << "\n=== ДЕМОНСТРАЦИЯ ОПЕРАТОРА ПРИСВАИВАНИЯ ===" << endl;

    Rectangle rect1(2, 2, 6, 5);
    Rectangle rect2;

    cout << "До присваивания:" << endl;
    rect1.display("rect1");
    rect2.display("rect2");

    cout << "После присваивания rect2 = rect1:" << endl;
    rect2 = rect1;
    rect1.display("rect1");
    rect2.display("rect2");

    cout << "Проверка равенства: " << (rect1 == rect2 ? "равны" : "не равны") << endl;
}

void demonstrateBinaryMinus() {
    cout << "\n=== ДЕМОНСТРАЦИЯ БИНАРНОГО ОПЕРАТОРА РАЗНОСТИ (-) ===" << endl;

    // Случай 1: Пересекающиеся прямоугольники
    cout << "1. Пересекающиеся прямоугольники:" << endl;
    Rectangle A(1, 1, 6, 5);
    Rectangle B(3, 2, 8, 4);
    A.display("A");
    B.display("B");

    Rectangle C = A - B;
    C.display("A - B (результат)");

    // Случай 2: Непересекающиеся прямоугольники
    cout << "2. Непересекающиеся прямоугольники:" << endl;
    Rectangle D(1, 1, 3, 3);
    Rectangle E(5, 5, 8, 8);
    D.display("D");
    E.display("E");

    Rectangle F = D - E;
    F.display("D - E (результат)");

    // Случай 3: Один внутри другого
    cout << "3. Один прямоугольник внутри другого:" << endl;
    Rectangle G(1, 1, 8, 6);
    Rectangle H(3, 2, 5, 4);
    G.display("G");
    H.display("H");

    Rectangle I = G - H;
    I.display("G - H (результат)");
}

void demonstrateUnaryMinus() {
    cout << "\n=== ДЕМОНСТРАЦИЯ УНАРНОГО ОПЕРАТОРА ОТОБРАЖЕНИЯ (-) ===" << endl;

    Rectangle rect1(2, 3, 5, 7);
    rect1.display("rect1 (оригинал)");

    Rectangle reflected = -rect1;
    reflected.display("-rect1 (отраженный)");

    // Двойное отражение должно вернуть оригинал
    cout << "Двойное отражение (-(-rect1)):" << endl;
    Rectangle doubleReflected = -(-rect1);
    doubleReflected.display("-(-rect1)");

    cout << "Проверка: rect1 == -(-rect1): "
        << (rect1 == doubleReflected ? "ДА" : "НЕТ") << endl;
}

void demonstrateComplexOperations() {
    cout << "\n=== КОМПЛЕКСНЫЕ ОПЕРАЦИИ ===" << endl;

    // Цепочка операций
    cout << "Цепочка операций: (A - B) - C" << endl;

    Rectangle A(0, 0, 10, 8);
    Rectangle B(2, 2, 7, 6);
    Rectangle C(5, 1, 8, 4);

    A.display("A");
    B.display("B");
    C.display("C");

    cout << "Вычисление (A - B) - C:" << endl;
    Rectangle result = (A - B) - C;
    result.display("(A - B) - C");

    // Комбинация унарного и бинарного операторов
    cout << "Комбинация: -(A - B)" << endl;
    Rectangle combo = -(A - B);
    combo.display("-(A - B)");
}

void interactiveDemo() {
    cout << "\n=== ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ ===" << endl;

    double x1, y1, x2, y2;

    cout << "Введите координаты первого прямоугольника (x1 y1 x2 y2): ";
    cin >> x1 >> y1 >> x2 >> y2;
    Rectangle rect1(x1, y1, x2, y2);

    cout << "Введите координаты второго прямоугольника (x1 y1 x2 y2): ";
    cin >> x1 >> y1 >> x2 >> y2;
    Rectangle rect2(x1, y1, x2, y2);

    cout << "\nРезультаты операций:" << endl;
    rect1.display("Прямоугольник 1");
    rect2.display("Прямоугольник 2");

    Rectangle diff = rect1 - rect2;
    diff.display("Разность (1 - 2)");

    Rectangle reflected1 = -rect1;
    Rectangle reflected2 = -rect2;
    reflected1.display("Отраженный 1");
    reflected2.display("Отраженный 2");
}

void displayMenu() {
    cout << "\n=== ДЕМОНСТРАЦИЯ ПЕРЕГРУЗКИ ОПЕРАТОРОВ ===" << endl;
    cout << "1. Демонстрация конструкторов" << endl;
    cout << "2. Демонстрация оператора присваивания" << endl;
    cout << "3. Демонстрация бинарного оператора разности (-)" << endl;
    cout << "4. Демонстрация унарного оператора отображения (-)" << endl;
    cout << "5. Комплексные операции" << endl;
    cout << "6. Интерактивная демонстрация" << endl;
    cout << "7. Полная демонстрация всех возможностей" << endl;
    cout << "8. Выход" << endl;
    cout << "Выберите действие: ";
}

void fullDemonstration() {
    demonstrateConstructors();
    demonstrateAssignment();
    demonstrateBinaryMinus();
    demonstrateUnaryMinus();
    demonstrateComplexOperations();
}

int main() {
    setlocale(LC_ALL, "rus");

    cout << "ПРАКТИЧЕСКАЯ РАБОТА №4: ПЕРЕГРУЗКА ОПЕРАЦИЙ" << endl;
    cout << "Класс: Rectangle (Прямоугольник)" << endl;
    cout << "Вариант 1: Несимметрическая разность и симметричное отображение" << endl;

    int choice;

    do {
        displayMenu();
        cin >> choice;

        switch (choice) {
        case 1:
            demonstrateConstructors();
            break;
        case 2:
            demonstrateAssignment();
            break;
        case 3:
            demonstrateBinaryMinus();
            break;
        case 4:
            demonstrateUnaryMinus();
            break;
        case 5:
            demonstrateComplexOperations();
            break;
        case 6:
            interactiveDemo();
            break;
        case 7:
            fullDemonstration();
            break;
        case 8:
            cout << "Выход из программы..." << endl;
            break;
        default:
            cout << "Неверный выбор! Попробуйте снова." << endl;
        }

    } while (choice != 8);

    return 0;
}