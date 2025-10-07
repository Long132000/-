#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <string>

// Строковые функции
std::string to_upper(const std::string& str);
std::string to_lower(const std::string& str);
std::string reverse_string(const std::string& str);
bool is_palindrome(const std::string& str);
int count_vowels(const std::string& str);

#endif