#include <iostream>
#include <string>

using namespace std;

// Условное включение заголовочных файлов
#ifdef HAVE_MATH_LIB
#include "math_utils.h"
#endif

#ifdef HAVE_STRING_LIB
#include "string_utils.h"
#endif

#ifdef HAVE_FILE_LIB
#include "file_utils.h"
#endif

void demonstrate_math_lib() {
#ifdef HAVE_MATH_LIB
    cout << "🧮 МАТЕМАТИЧЕСКАЯ БИБЛИОТЕКА:" << endl;
    cout << "================================" << endl;
    cout << "5 + 3 = " << add(5, 3) << endl;
    cout << "5 * 3 = " << multiply(5, 3) << endl;
    cout << "2^4 = " << power(2, 4) << endl;
    cout << "5! = " << factorial(5) << endl;
    cout << "17 - простое число: " << (is_prime(17) ? "да" : "нет") << endl;
#else
    cout << "🧮 МАТЕМАТИЧЕСКАЯ БИБЛИОТЕКА: ОТКЛЮЧЕНА" << endl;
#endif
    cout << endl;
}

void demonstrate_string_lib() {
#ifdef HAVE_STRING_LIB
    cout << "🔤 СТРОКОВАЯ БИБЛИОТЕКА:" << endl;
    cout << "================================" << endl;
    string test_str = "Hello World!";
    cout << "Исходная строка: " << test_str << endl;
    cout << "В верхнем регистре: " << to_upper(test_str) << endl;
    cout << "В нижнем регистре: " << to_lower(test_str) << endl;
    cout << "Перевернутая: " << reverse_string(test_str) << endl;
    cout << "Количество гласных: " << count_vowels(test_str) << endl;
    cout << "'radar' - палиндром: " << (is_palindrome("radar") ? "да" : "нет") << endl;
#else
    cout << "🔤 СТРОКОВАЯ БИБЛИОТЕКА: ОТКЛЮЧЕНА" << endl;
#endif
    cout << endl;
}

void demonstrate_file_lib() {
#ifdef HAVE_FILE_LIB
    cout << "📁 ФАЙЛОВАЯ БИБЛИОТЕКА:" << endl;
    cout << "================================" << endl;
    
    string filename = "test_file.txt";
    create_test_file(filename, "Это тестовый файл для демонстрации.");
    
    cout << "Файл '" << filename << "' существует: " << (file_exists(filename) ? "да" : "нет") << endl;
    cout << "Расширение файла: " << get_file_extension("document.pdf") << endl;
    cout << "Имя файла: " << get_file_name("C:/folder/document.txt") << endl;
    cout << "Размер файла: " << get_file_size(filename) << " байт" << endl;
#else
    cout << "📁 ФАЙЛОВАЯ БИБЛИОТЕКА: ОТКЛЮЧЕНА" << endl;
#endif
    cout << endl;
}

int main() {
    cout << "==========================================" << endl;
    cout << "   ЛАБОРАТОРНАЯ РАБОТА 2D - РЕЗУЛЬТАТЫ" << endl;
    cout << "==========================================" << endl;
    cout << endl;
    
    // Демонстрация работы библиотек
    demonstrate_math_lib();
    demonstrate_string_lib();
    demonstrate_file_lib();
    
    cout << "==========================================" << endl;
    cout << "💡 Для изменения конфигурации:" << endl;
    cout << "1. Измените BUILD_*_LIB опции в CMake GUI" << endl;
    cout << "2. Нажмите Configure" << endl;
    cout << "3. Пересоберите проект" << endl;
    cout << "==========================================" << endl;
    
    return 0;
}