#ifndef MOTHERBOARD_H
#define MOTHERBOARD_H

#include <iostream>
#include <string>

class Motherboard {
private:
    std::string model;
    std::string formFactor;
    std::string socket;
    int ramSlots;
    int maxRAM; // GB

public:
    // Конструкторы
    Motherboard();
    Motherboard(const std::string& mod, const std::string& form, const std::string& sock, int slots, int maxRam);

    // Методы установки свойств
    bool setProperties(const std::string& mod, const std::string& form, const std::string& sock, int slots, int maxRam);

    // Операции
    bool checkComponentCompatibility(const std::string& cpuSocket, const std::string& ramType) const; // проверка совместимости
    int calculateMaxConfiguration(int ramSize) const; // расчет максимальной конфигурации
    bool checkInterfaceSupport(const std::string& interface) const; // проверка поддержки интерфейсов
    void upgradeBIOS();                   // обновление BIOS

    // Вспомогательные методы
    void display() const;
    bool isValid() const;

    // Геттеры
    std::string getModel() const { return model; }
    std::string getFormFactor() const { return formFactor; }
    std::string getSocket() const { return socket; }
    int getRamSlots() const { return ramSlots; }
    int getMaxRAM() const { return maxRAM; }
};

#endif