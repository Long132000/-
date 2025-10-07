cmake_minimum_required(VERSION 3.15)
project(Lab2D)

message(STATUS "==========================================")
message(STATUS "Лабораторная работа 2D - Опциональные библиотеки")
message(STATUS "==========================================")

# Опции для включения/выключения библиотек (появляются в CMake GUI)
option(BUILD_MATH_LIB "Построить математическую библиотеку" ON)
option(BUILD_STRING_LIB "Построить строковую библиотеку" ON)
option(BUILD_FILE_LIB "Построить файловую библиотеку" ON)

message(STATUS "Конфигурация сборки:")
message(STATUS "  MATH_LIB: ${BUILD_MATH_LIB}")
message(STATUS "  STRING_LIB: ${BUILD_STRING_LIB}")
message(STATUS "  FILE_LIB: ${BUILD_FILE_LIB}")
message(STATUS "")

# Добавление подпроектов в зависимости от опций
if(BUILD_MATH_LIB)
    add_subdirectory(math_lib)
    message(STATUS "✓ Математическая библиотека включена")
else()
    message(STATUS "✗ Математическая библиотека отключена")
endif()

if(BUILD_STRING_LIB)
    add_subdirectory(string_lib)
    message(STATUS "✓ Строковая библиотека включена")
else()
    message(STATUS "✗ Строковая библиотека отключена")
endif()

if(BUILD_FILE_LIB)
    add_subdirectory(file_lib)
    message(STATUS "✓ Файловая библиотека включена")
else()
    message(STATUS "✗ Файловая библиотека отключена")
endif()

# Главное приложение всегда строится
add_subdirectory(app)

message(STATUS "")
message(STATUS "💡 ИНСТРУКЦИЯ:")
message(STATUS "Измените BUILD_*_LIB опции в CMake GUI и нажмите Configure")
message(STATUS "==========================================")