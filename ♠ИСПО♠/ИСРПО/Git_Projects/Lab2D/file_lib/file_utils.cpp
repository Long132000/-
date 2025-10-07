#include "file_utils.h"
#include <fstream>
#include <filesystem>

bool file_exists(const std::string& filename) {
    std::ifstream file(filename);
    return file.good();
}

std::string get_file_extension(const std::string& filename) {
    size_t dot_pos = filename.find_last_of('.');
    if (dot_pos != std::string::npos) {
        return filename.substr(dot_pos + 1);
    }
    return "";
}

std::string get_file_name(const std::string& filepath) {
    size_t slash_pos = filepath.find_last_of("/\\");
    if (slash_pos != std::string::npos) {
        return filepath.substr(slash_pos + 1);
    }
    return filepath;
}

long get_file_size(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary | std::ios::ate);
    if (!file) return -1;
    return file.tellg();
}

bool create_test_file(const std::string& filename, const std::string& content) {
    std::ofstream file(filename);
    if (!file) return false;
    file << content;
    return true;
}