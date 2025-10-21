#ifndef GRAPHICSCARD_H
#define GRAPHICSCARD_H

#include <iostream>
#include <string>

class GraphicsCard {
private:
    std::string model;
    int vram; // GB
    int gpuFrequency; // MHz
    int processors;
    double power; // W

public:
    // Конструкторы
    GraphicsCard();
    GraphicsCard(const std::string& mod, int vr, int gpuFreq, int proc, double pwr);

    // Методы установки свойств
    bool setProperties(const std::string& mod, int vr, int gpuFreq, int proc, double pwr);

    // Операции
    double calculatePerformance() const;   // расчет производительности
    bool checkPSURequirements(double psuPower) const; // проверка требований к БП
    double calculateHeatOutput() const;    // расчет тепловыделения
    void overclock(int boost);             // разгон видеокарты

    // Вспомогательные методы
    void display() const;
    bool isValid() const;

    // Геттеры
    std::string getModel() const { return model; }
    int getVRAM() const { return vram; }
    int getGPUFrequency() const { return gpuFrequency; }
    int getProcessors() const { return processors; }
    double getPower() const { return power; }
};

#endif