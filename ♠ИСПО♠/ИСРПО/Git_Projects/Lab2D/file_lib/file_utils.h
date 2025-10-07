#ifndef FILE_UTILS_H
#define FILE_UTILS_H

#include <string>

// Файловые операции
bool file_exists(const std::string& filename);
std::string get_file_extension(const std::string& filename);
std::string get_file_name(const std::string& filepath);
long get_file_size(const std::string& filename);
bool create_test_file(const std::string& filename, const std::string& content);

#endif