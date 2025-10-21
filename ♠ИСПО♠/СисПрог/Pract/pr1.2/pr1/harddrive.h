#ifndef HARDDRIVE_H
#define HARDDRIVE_H

#include <iostream>
#include <string>

class HardDrive {
private:
    std::string model;
    double capacity; // TB
    int speed; // RPM (для HDD) или 0 для SSD
    std::string interface;
    int readSpeed; // MB/s

public:
    // Конструкторы
    HardDrive();
    HardDrive(const std::string& mod, double cap, int spd, const std::string& intf, int read);

    // Методы установки свойств
    bool setProperties(const std::string& mod, double cap, int spd, const std::string& intf, int read);

    // Операции
    double calculateAccessTime() const;    // расчет времени доступа
    bool checkInterfaceSupport(const std::string& moboInterface) const; // проверка поддержки интерфейса
    double calculateEffectiveSpeed() const; // расчет эффективной скорости
    void optimize();                       // оптимизация диска

    // Вспомогательные методы
    void display() const;
    bool isValid() const;

    // Геттеры
    std::string getModel() const { return model; }
    double getCapacity() const { return capacity; }
    int getSpeed() const { return speed; }
    std::string getInterface() const { return interface; }
    int getReadSpeed() const { return readSpeed; }
};

#endif