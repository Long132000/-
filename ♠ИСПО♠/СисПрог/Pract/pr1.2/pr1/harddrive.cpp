#include "harddrive.h"
#include <iostream>
#include <cmath>

using namespace std;

HardDrive::HardDrive() : model(""), capacity(0), speed(0), interface(""), readSpeed(0) {}

HardDrive::HardDrive(const string& mod, double cap, int spd, const string& intf, int read) {
    setProperties(mod, cap, spd, intf, read);
}

bool HardDrive::setProperties(const string& mod, double cap, int spd, const string& intf, int read) {
    if (cap > 0 && read > 0 && (intf == "SATA" || intf == "NVMe" || intf == "PCIe")) {
        model = mod;
        capacity = cap;
        speed = spd;
        interface = intf;
        readSpeed = read;
        return true;
    }
    cout << "Ошибка: недопустимые параметры жесткого диска" << endl;
    return false;
}

double HardDrive::calculateAccessTime() const {
    if (!isValid()) return 0;

    if (interface == "NVMe") {
        return 0.01;
    }
    else {
        return speed > 0 ? (4.17 + 60000.0 / speed) : 0.1;
    }
}

bool HardDrive::checkInterfaceSupport(const string& moboInterface) const {
    if (!isValid()) return false;

    if (moboInterface == "SATA") {
        return interface == "SATA";
    }
    else if (moboInterface == "NVMe" || moboInterface == "PCIe") {
        return interface == "NVMe";
    }
    return false;
}

double HardDrive::calculateEffectiveSpeed() const {
    if (!isValid()) return 0;

    double efficiency = 1.0;
    if (interface == "SATA") efficiency = 0.8;
    else if (interface == "NVMe") efficiency = 0.95;

    return readSpeed * efficiency;
}

void HardDrive::optimize() {
    if (isValid()) {
        if (interface == "SATA" && speed > 0) {
            cout << "Проведена дефрагментация HDD" << endl;
        }
        else if (interface == "NVMe") {
            cout << "Выполнена оптимизация TRIM для SSD" << endl;
        }
        readSpeed = static_cast<int>(readSpeed * 1.05);
    }
}

void HardDrive::display() const {
    cout << "Жесткий диск " << model << ": " << capacity << " ТБ, ";
    if (speed > 0) {
        cout << speed << " об/мин, ";
    }
    else {
        cout << "SSD, ";
    }
    cout << interface << ", чтение: " << readSpeed << " МБ/с" << endl;
}

bool HardDrive::isValid() const {
    return !model.empty() && capacity > 0 && readSpeed > 0 && !interface.empty();
}