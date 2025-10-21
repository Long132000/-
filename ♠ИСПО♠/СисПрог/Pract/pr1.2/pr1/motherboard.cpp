#include "motherboard.h"
#include <iostream>
#include <cmath>

using namespace std;

Motherboard::Motherboard() : model(""), formFactor(""), socket(""), ramSlots(0), maxRAM(0) {}

Motherboard::Motherboard(const string& mod, const string& form, const string& sock, int slots, int maxRam) {
    setProperties(mod, form, sock, slots, maxRam);
}

bool Motherboard::setProperties(const string& mod, const string& form, const string& sock, int slots, int maxRam) {
    if (slots > 0 && maxRam > 0 &&
        (form == "ATX" || form == "mATX" || form == "ITX") &&
        (sock == "LGA1700" || sock == "AM5" || sock == "AM4" || sock == "LGA1200")) {
        model = mod;
        formFactor = form;
        socket = sock;
        ramSlots = slots;
        maxRAM = maxRam;
        return true;
    }
    cout << "Ошибка: недопустимые параметры материнской платы" << endl;
    return false;
}

bool Motherboard::checkComponentCompatibility(const string& cpuSocket, const string& ramType) const {
    if (!isValid()) return false;

    bool socketCompat = (socket == cpuSocket);

    bool ramCompat = true;
    if (socket.find("LGA1700") != string::npos || socket.find("LGA1200") != string::npos) {
        ramCompat = (ramType == "DDR4" || ramType == "DDR5");
    }
    else if (socket.find("AM5") != string::npos) {
        ramCompat = (ramType == "DDR5");
    }
    else if (socket.find("AM4") != string::npos) {
        ramCompat = (ramType == "DDR4");
    }

    return socketCompat && ramCompat;
}

int Motherboard::calculateMaxConfiguration(int ramSize) const {
    if (!isValid()) return 0;
    return ramSlots * ramSize;
}

bool Motherboard::checkInterfaceSupport(const string& interface) const {
    if (!isValid()) return false;

    if (interface == "NVMe") {
        return formFactor == "ATX" || formFactor == "mATX";
    }
    else if (interface == "SATA") {
        return true;
    }
    else if (interface == "PCIe5") {
        return socket == "LGA1700" || socket == "AM5";
    }
    return false;
}

void Motherboard::upgradeBIOS() {
    if (isValid()) {
        cout << "BIOS материнской платы обновлен до последней версии" << endl;
        maxRAM = static_cast<int>(maxRAM * 1.1);
    }
}

void Motherboard::display() const {
    cout << "Материнская плата " << model << ": " << formFactor << ", "
        << socket << ", " << ramSlots << " слотов RAM, макс. "
        << maxRAM << " ГБ" << endl;
}

bool Motherboard::isValid() const {
    return !model.empty() && !formFactor.empty() && !socket.empty() &&
        ramSlots > 0 && maxRAM > 0;
}