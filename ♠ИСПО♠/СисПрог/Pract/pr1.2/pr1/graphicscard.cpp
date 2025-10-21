#include "graphicscard.h"
#include <iostream>
#include <cmath>

using namespace std;

GraphicsCard::GraphicsCard() : model(""), vram(0), gpuFrequency(0), processors(0), power(0) {}

GraphicsCard::GraphicsCard(const string& mod, int vr, int gpuFreq, int proc, double pwr) {
    setProperties(mod, vr, gpuFreq, proc, pwr);
}

bool GraphicsCard::setProperties(const string& mod, int vr, int gpuFreq, int proc, double pwr) {
    if (vr > 0 && gpuFreq > 0 && proc > 0 && pwr > 0) {
        model = mod;
        vram = vr;
        gpuFrequency = gpuFreq;
        processors = proc;
        power = pwr;
        return true;
    }
    cout << "Ошибка: недопустимые параметры видеокарты" << endl;
    return false;
}

double GraphicsCard::calculatePerformance() const {
    if (!isValid()) return 0;
    return (vram * gpuFrequency * processors) / 10000.0;
}

bool GraphicsCard::checkPSURequirements(double psuPower) const {
    if (!isValid()) return false;
    return psuPower >= (power * 1.2);
}

double GraphicsCard::calculateHeatOutput() const {
    if (!isValid()) return 0;
    return power * 0.7 + (gpuFrequency - 1500) * 0.1;
}

void GraphicsCard::overclock(int boost) {
    if (boost > 0 && isValid()) {
        gpuFrequency += boost;
        power *= 1.15;
        cout << "Видеокарта разогнана на " << boost << " МГц" << endl;
    }
    else {
        cout << "Ошибка: недопустимое значение boost" << endl;
    }
}

void GraphicsCard::display() const {
    cout << "Видеокарта " << model << ": " << vram << " ГБ, "
        << gpuFrequency << " МГц, " << processors << " процессоров, "
        << power << " Вт" << endl;
}

bool GraphicsCard::isValid() const {
    return !model.empty() && vram > 0 && gpuFrequency > 0 && processors > 0 && power > 0;
}