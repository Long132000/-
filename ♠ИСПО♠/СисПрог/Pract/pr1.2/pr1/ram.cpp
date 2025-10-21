#include "ram.h"
#include <iostream>
#include <cmath>

using namespace std;

RAM::RAM() : model(""), capacity(0), frequency(0), type(""), timings(0) {}

RAM::RAM(const string& mod, int cap, int freq, const string& tp, int tim) {
    setProperties(mod, cap, freq, tp, tim);
}

bool RAM::setProperties(const string& mod, int cap, int freq, const string& tp, int tim) {
    if (cap > 0 && freq > 0 && tim > 0 && (tp == "DDR4" || tp == "DDR5" || tp == "DDR3")) {
        model = mod;
        capacity = cap;
        frequency = freq;
        type = tp;
        timings = tim;
        return true;
    }
    cout << "Ошибка: недопустимые параметры оперативной памяти" << endl;
    return false;
}

double RAM::calculateBandwidth() const {
    if (!isValid()) return 0;
    return (frequency * 8) / 1000.0; // ГБ/с
}

bool RAM::checkCompatibility(const string& moboType) const {
    if (!isValid()) return false;
    return type == moboType;
}

double RAM::calculateLatency() const {
    if (!isValid()) return 0;
    return (static_cast<double>(timings) / frequency) * 2000; // нс
}

void RAM::overclock(int boost) {
    if (boost > 0 && isValid()) {
        frequency += boost;
        timings += 2;
        cout << "Память разогнана на " << boost << " МГц" << endl;
    }
    else {
        cout << "Ошибка: недопустимое значение boost" << endl;
    }
}

void RAM::display() const {
    cout << "Оперативная память " << model << ": " << capacity << " ГБ, "
        << frequency << " МГц, " << type << ", CL" << timings << endl;
}

bool RAM::isValid() const {
    return !model.empty() && capacity > 0 && frequency > 0 && !type.empty() && timings > 0;
}