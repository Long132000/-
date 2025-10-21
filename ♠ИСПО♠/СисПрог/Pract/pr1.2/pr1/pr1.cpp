#include <iostream>
#include <vector>
#include <clocale>
#include <limits>
#include "microprocessor.h"
#include "ram.h"
#include "harddrive.h"
#include "graphicscard.h"
#include "motherboard.h"



using namespace std;

void displayMenu() {
    cout << "\n=== СИСТЕМА УПРАВЛЕНИЯ КОМПОНЕНТАМИ ЭЛЕКТРОНИКИ ===" << endl;
    cout << "1. Микропроцессоры" << endl;
    cout << "2. Оперативная память" << endl;
    cout << "3. Жесткие диски" << endl;
    cout << "4. Видеокарты" << endl;
    cout << "5. Материнские платы" << endl;
    cout << "6. Показать все компоненты" << endl;
    cout << "7. Тест совместимости" << endl;
    cout << "8. Выход" << endl;
    cout << "Выберите категорию: ";
}

void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

void demonstrateMicroprocessors() {
    vector<Microprocessor> cpus = {
        Microprocessor("Intel Core i9-13900K", 5.8, 24, 36, 125),
        Microprocessor("AMD Ryzen 9 7950X", 5.7, 16, 64, 170),
        Microprocessor("Apple M2 Max", 3.5, 12, 48, 45),
        Microprocessor("Qualcomm Snapdragon 8 Gen 2", 3.2, 8, 8, 5),
        Microprocessor("Intel Core i5-13400", 4.6, 10, 20, 65),
        Microprocessor("AMD Ryzen 5 7600X", 5.3, 6, 32, 105),
        Microprocessor("NVIDIA Tegra X1", 2.0, 8, 2.5, 15)
    };

    cout << "\n=== МИКРОПРОЦЕССОРЫ ===" << endl;
    for (size_t i = 0; i < cpus.size(); i++) {
        cout << "\n[" << i + 1 << "] ";
        cpus[i].display();
        cout << "Производительность: " << cpus[i].calculatePerformance() << " усл.ед." << endl;
        cout << "Тепловыделение: " << cpus[i].calculateHeatOutput() << "°C" << endl;
        cout << "Совместимость с LGA1700: " << (cpus[i].checkCompatibility("LGA1700") ? "Да" : "Нет") << endl;
    }
}

void demonstrateRAM() {
    vector<RAM> rams = {
        RAM("Corsair Vengeance LPX", 16, 3200, "DDR4", 16),
        RAM("Kingston Fury Beast", 32, 5600, "DDR5", 36),
        RAM("G.Skill Trident Z", 64, 6000, "DDR5", 30),
        RAM("Samsung DDR4", 8, 2666, "DDR4", 19),
        RAM("Crucial Ballistix", 16, 3600, "DDR4", 16),
        RAM("Team Group T-Force", 32, 5200, "DDR5", 38),
        RAM("HyperX Predator", 8, 4133, "DDR4", 19)
    };

    cout << "\n=== ОПЕРАТИВНАЯ ПАМЯТЬ ===" << endl;
    for (size_t i = 0; i < rams.size(); i++) {
        cout << "\n[" << i + 1 << "] ";
        rams[i].display();
        cout << "Пропускная способность: " << rams[i].calculateBandwidth() << " ГБ/с" << endl;
        cout << "Задержка: " << rams[i].calculateLatency() << " нс" << endl;
        cout << "Совместимость с DDR4: " << (rams[i].checkCompatibility("DDR4") ? "Да" : "Нет") << endl;
    }
}

void demonstrateHardDrives() {
    vector<HardDrive> drives = {
        HardDrive("WD Black SN850X", 2, 0, "NVMe", 7300),
        HardDrive("Seagate Barracuda", 4, 5400, "SATA", 190),
        HardDrive("Samsung 980 Pro", 1, 0, "NVMe", 7000),
        HardDrive("Toshiba P300", 3, 7200, "SATA", 210),
        HardDrive("Crucial P5 Plus", 2, 0, "NVMe", 6600),
        HardDrive("Seagate FireCuda", 2, 7200, "SATA", 220),
        HardDrive("Kingston NV2", 1, 0, "NVMe", 3500)
    };

    cout << "\n=== ЖЕСТКИЕ ДИСКИ ===" << endl;
    for (size_t i = 0; i < drives.size(); i++) {
        cout << "\n[" << i + 1 << "] ";
        drives[i].display();
        cout << "Время доступа: " << drives[i].calculateAccessTime() << " мс" << endl;
        cout << "Эффективная скорость: " << drives[i].calculateEffectiveSpeed() << " МБ/с" << endl;
        cout << "Поддержка SATA: " << (drives[i].checkInterfaceSupport("SATA") ? "Да" : "Нет") << endl;
    }
}

void demonstrateGraphicsCards() {
    vector<GraphicsCard> gpus = {
        GraphicsCard("NVIDIA RTX 4090", 24, 2520, 16384, 450),
        GraphicsCard("AMD RX 7900 XTX", 24, 2500, 6144, 355),
        GraphicsCard("NVIDIA RTX 4070", 12, 2475, 5888, 200),
        GraphicsCard("AMD RX 7600", 8, 2650, 2048, 165),
        GraphicsCard("Intel Arc A770", 16, 2400, 4096, 225),
        GraphicsCard("NVIDIA GTX 1660", 6, 1785, 1408, 120),
        GraphicsCard("AMD RX 6400", 4, 2321, 768, 53)
    };

    cout << "\n=== ВИДЕОКАРТЫ ===" << endl;
    for (size_t i = 0; i < gpus.size(); i++) {
        cout << "\n[" << i + 1 << "] ";
        gpus[i].display();
        cout << "Производительность: " << gpus[i].calculatePerformance() << " усл.ед." << endl;
        cout << "Тепловыделение: " << gpus[i].calculateHeatOutput() << "°C" << endl;
        cout << "Требуется БП 750W: " << (gpus[i].checkPSURequirements(750) ? "Да" : "Нет") << endl;
    }
}

void demonstrateMotherboards() {
    vector<Motherboard> mobos = {
        Motherboard("ASUS ROG Maximus Z790", "ATX", "LGA1700", 4, 128),
        Motherboard("Gigabyte B650 AORUS", "ATX", "AM5", 4, 128),
        Motherboard("MSI MPG B550", "ATX", "AM4", 4, 128),
        Motherboard("ASRock B760M", "mATX", "LGA1700", 2, 64),
        Motherboard("ASUS ROG Strix X670E", "ATX", "AM5", 4, 128),
        Motherboard("Gigabyte Z690", "ATX", "LGA1700", 4, 128),
        Motherboard("ASRock A520M", "mATX", "AM4", 2, 64)
    };

    cout << "\n=== МАТЕРИНСКИЕ ПЛАТЫ ===" << endl;
    for (size_t i = 0; i < mobos.size(); i++) {
        cout << "\n[" << i + 1 << "] ";
        mobos[i].display();
        cout << "Макс. конфигурация с 32ГБ модулями: " << mobos[i].calculateMaxConfiguration(32) << " ГБ" << endl;
        cout << "Совместимость с LGA1700/DDR5: " << (mobos[i].checkComponentCompatibility("LGA1700", "DDR5") ? "Да" : "Нет") << endl;
        cout << "Поддержка NVMe: " << (mobos[i].checkInterfaceSupport("NVMe") ? "Да" : "Нет") << endl;
    }
}

void testCompatibility() {
    cout << "\n=== ТЕСТ СОВМЕСТИМОСТИ ===" << endl;

    Microprocessor cpu("Intel Core i5-13400", 4.6, 10, 20, 65);
    RAM memory("Corsair Vengeance LPX", 16, 3200, "DDR4", 16);
    Motherboard mobo("ASUS ROG Maximus Z790", "ATX", "LGA1700", 4, 128);

    cout << "Конфигурация:" << endl;
    cpu.display();
    memory.display();
    mobo.display();

    bool compatible = mobo.checkComponentCompatibility(cpu.getModel().find("Intel") != string::npos ? "LGA1700" : "AM5",
        memory.getType());

    cout << "Результат проверки совместимости: " << (compatible ? "КОМПОНЕНТЫ СОВМЕСТИМЫ" : "НЕСОВМЕСТИМЫЕ КОМПОНЕНТЫ") << endl;
}

int main() {
    setlocale(LC_ALL, "rus");

    cout << "ПРАКТИЧЕСКАЯ РАБОТА №1: ПРОЕКТИРОВАНИЕ КЛАССОВ" << endl;
    cout << "Раздел 2.2 - Электроника (Вариант 5)" << endl;
    cout << "Демонстрация 5 классов электронных компонентов" << endl;

    int choice;

    do {
        displayMenu();
        cin >> choice;

        if (cin.fail()) {
            cout << "Ошибка ввода! Пожалуйста, введите число от 1 до 8." << endl;
            clearInputBuffer();
            continue;
        }
        clearInputBuffer();

        switch (choice) {
        case 1:
            demonstrateMicroprocessors();
            break;
        case 2:
            demonstrateRAM();
            break;
        case 3:
            demonstrateHardDrives();
            break;
        case 4:
            demonstrateGraphicsCards();
            break;
        case 5:
            demonstrateMotherboards();
            break;
        case 6:
            demonstrateMicroprocessors();
            demonstrateRAM();
            demonstrateHardDrives();
            demonstrateGraphicsCards();
            demonstrateMotherboards();
            break;
        case 7:
            testCompatibility();
            break;
        case 8:
            cout << "Выход из программы..." << endl;
            break;
        default:
            cout << "Неверный выбор! Пожалуйста, введите число от 1 до 8." << endl;
        }

    } while (choice != 8);

    return 0;
}