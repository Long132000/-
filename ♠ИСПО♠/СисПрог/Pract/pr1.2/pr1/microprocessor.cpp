#include "microprocessor.h"
#include <iostream>
#include <cmath>

using namespace std;

Microprocessor::Microprocessor() : model(""), frequency(0), cores(0), cache(0), power(0) {}

Microprocessor::Microprocessor(const string& mod, double freq, int cr, double cach, double pwr) {
    setProperties(mod, freq, cr, cach, pwr);
}

bool Microprocessor::setProperties(const string& mod, double freq, int cr, double cach, double pwr) {
    if (freq > 0 && cr > 0 && cach > 0 && pwr > 0) {
        model = mod;
        frequency = freq;
        cores = cr;
        cache = cach;
        power = pwr;
        return true;
    }
    cout << "Ошибка: недопустимые параметры микропроцессора" << endl;
    return false;
}

double Microprocessor::calculatePerformance() const {
    if (!isValid()) return 0;
    return (frequency * cores * cache) / 100.0;
}

bool Microprocessor::checkCompatibility(const string& socket) const {
    if (!isValid()) return false;

    if (model.find("Intel") != string::npos) {
        return socket == "LGA1700" || socket == "LGA1200" || socket == "LGA1151";
    }
    else if (model.find("AMD") != string::npos) {
        return socket == "AM5" || socket == "AM4";
    }
    else if (model.find("Apple") != string::npos) {
        return socket == "Apple Silicon";
    }
    return false;
}

double Microprocessor::calculateHeatOutput() const {
    if (!isValid()) return 0;
    return power * 0.8 + (frequency - 2.0) * 10;
}

void Microprocessor::upgradeFrequency(double boost) {
    if (boost > 0 && isValid()) {
        frequency += boost;
        power *= 1.1;
        cout << "Частота увеличена на " << boost << " ГГц" << endl;
    }
    else {
        cout << "Ошибка: недопустимое значение boost" << endl;
    }
}

void Microprocessor::display() const {
    cout << "Микропроцессор " << model << ": " << frequency << " ГГц, "
        << cores << " ядер, " << cache << " МБ кэш, " << power << " Вт" << endl;
}

bool Microprocessor::isValid() const {
    return !model.empty() && frequency > 0 && cores > 0 && cache > 0 && power > 0;
}