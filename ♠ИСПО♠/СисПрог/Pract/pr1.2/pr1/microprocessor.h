#ifndef MICROPROCESSOR_H
#define MICROPROCESSOR_H

#include <iostream>
#include <string>

class Microprocessor {
private:
    std::string model;
    double frequency; // GHz
    int cores;
    double cache; // MB
    double power; // W

public:
    // Конструкторы
    Microprocessor();
    Microprocessor(const std::string& mod, double freq, int cr, double cach, double pwr);

    // Методы установки свойств
    bool setProperties(const std::string& mod, double freq, int cr, double cach, double pwr);

    // Операции
    double calculatePerformance() const;  // вычисление производительности
    bool checkCompatibility(const std::string& socket) const;  // проверка совместимости
    double calculateHeatOutput() const;   // расчет тепловыделения
    void upgradeFrequency(double boost);  // увеличение частоты

    // Вспомогательные методы
    void display() const;
    bool isValid() const;

    // Геттеры
    std::string getModel() const { return model; }
    double getFrequency() const { return frequency; }
    int getCores() const { return cores; }
    double getCache() const { return cache; }
    double getPower() const { return power; }
};

#endif