#include <iostream>
#include <string>

class Planer {
protected:
	std::string model;
	std::string constructor;
	int devel_year;
public:
	Planer(std::string model, std::string constructor, int devel_year) : model(model), constructor(constructor), devel_year(devel_year) {}
	virtual void print_info() {
		std::cout << "Планер:" << std::endl;
		std::cout << "Модель: "<< model << std::endl;
		std::cout << "Год разработки: " << devel_year << std::endl;
		std::cout << "Конструктор: " << constructor << "\n\n";
	}
};

class Plane : public Planer {
private:
	float max_speed;
	float max_flying_range;
protected:
	Plane(std::string model, std::string constructor, int devel_year) : Planer(model, constructor, devel_year) {}
public:
	Plane(std::string model, std::string constructor, int devel_year, float max_speed, float max_flying_range) : Planer(model, constructor, devel_year), max_speed(max_speed), max_flying_range(max_flying_range) {}
	void print_info() {
		std::cout << "Самолет:" << std::endl;
		std::cout << "Модель: " << model << std::endl;
		std::cout << "Год разработки: " << devel_year << std::endl;
		std::cout << "Конструктор: " << constructor << std::endl;
		std::cout << "Максимальная скорость: " << max_speed << std::endl;
		std::cout << "Максимальная дальность полета: " << max_flying_range << "\n\n";
	}
};

std::string isOrbital(bool orbital) {
	if (orbital) {
		return "Орбитальная";
	} else {
		return "Межпланетная";
	}
}

class Rocket : public Plane {
private:
	std::string purpose;
	std::string fuel;
	bool orbital;
public:
	Rocket(std::string model, std::string constructor, int devel_year, std::string purpose, std::string fuel, bool orbital) : Plane(model, constructor, devel_year), purpose(purpose), fuel(fuel), orbital(orbital) {}
	void print_info() {
		std::cout << "Рокета:" << std::endl;
		std::cout << "Модель: " << model << std::endl;
		std::cout << "Год разработки: " << devel_year << std::endl;
		std::cout << "Конструктор: " << constructor << std::endl;
		std::cout << "Назначение: " << purpose << std::endl;
		std::cout << "Топливо: " << fuel << std::endl;
		std::cout << "Орбитальная: " << isOrbital(orbital) << "\n\n";
	}
};


int main() {
	setlocale(LC_ALL, "RUS");
	Planer planer("1488z", "Denis", 2005);
	planer.print_info();
	Plane plane("1488z", "Denis", 2005, 34, 69);
	plane.print_info();
	Rocket rocket("1488z", "Denis", 2005, "Karolek", "redbull", true);
	rocket.print_info();
	return 0;
}