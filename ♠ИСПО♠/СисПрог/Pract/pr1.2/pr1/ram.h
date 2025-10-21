#ifndef RAM_H
#define RAM_H

#include <iostream>
#include <string>

class RAM {
private:
    std::string model;
    int capacity; // GB
    int frequency; // MHz
    std::string type;
    int timings;

public:
    // Конструкторы
    RAM();
    RAM(const std::string& mod, int cap, int freq, const std::string& tp, int tim);

    // Методы установки свойств
    bool setProperties(const std::string& mod, int cap, int freq, const std::string& tp, int tim);

    // Операции
    double calculateBandwidth() const;     // расчет пропускной способности
    bool checkCompatibility(const std::string& moboType) const; // проверка совместимости
    double calculateLatency() const;       // расчет задержки доступа
    void overclock(int boost);             // разгон памяти

    // Вспомогательные методы
    void display() const;
    bool isValid() const;

    // Геттеры
    std::string getModel() const { return model; }
    int getCapacity() const { return capacity; }
    int getFrequency() const { return frequency; }
    std::string getType() const { return type; }
    int getTimings() const { return timings; }
};

#endif