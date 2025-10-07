#include "string_utils.h"
#include <algorithm>
#include <cctype>

std::string to_upper(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::toupper);
    return result;
}

std::string to_lower(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}

std::string reverse_string(const std::string& str) {
    std::string result = str;
    std::reverse(result.begin(), result.end());
    return result;
}

bool is_palindrome(const std::string& str) {
    std::string clean_str;
    std::copy_if(str.begin(), str.end(), std::back_inserter(clean_str), ::isalnum);
    std::transform(clean_str.begin(), clean_str.end(), clean_str.begin(), ::tolower);
    
    std::string reversed = clean_str;
    std::reverse(reversed.begin(), reversed.end());
    
    return clean_str == reversed;
}

int count_vowels(const std::string& str) {
    int count = 0;
    std::string vowels = "aeiouAEIOU";
    for (char c : str) {
        if (vowels.find(c) != std::string::npos) {
            count++;
        }
    }
    return count;
}