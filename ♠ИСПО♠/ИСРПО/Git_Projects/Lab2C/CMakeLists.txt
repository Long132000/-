cmake_minimum_required(VERSION 3.15)
project(MathOperations)

message(STATUS "==========================================")
message(STATUS "Лабораторная работа 2C - Математические операции")
message(STATUS "==========================================")

# 1. Определяем переменные, которые можно менять в CMake GUI
set(A 15 CACHE STRING "Первое число")
set(B 5 CACHE STRING "Второе число")
set(OPERATION "*" CACHE STRING "Математическая операция: +, -, *, /")

message(STATUS "")
message(STATUS "Текущие значения:")
message(STATUS "  A = ${A}")
message(STATUS "  B = ${B}") 
message(STATUS "  OPERATION = ${OPERATION}")
message(STATUS "")

# 2. Проверка корректности ввода
if(NOT A MATCHES "^[0-9]+$")
    message(FATAL_ERROR "❌ Ошибка: A должно быть целым числом!")
endif()

if(NOT B MATCHES "^[0-9]+$")
    message(FATAL_ERROR "❌ Ошибка: B должно быть целым числом!")
endif()

# 3. Выполнение математических операций
message(STATUS "📊 РЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ:")
message(STATUS "================================")

if(OPERATION STREQUAL "+")
    math(EXPR RESULT "${A} + ${B}")
    message(STATUS "Сложение: ${A} + ${B} = ${RESULT}")
    
elseif(OPERATION STREQUAL "-")
    math(EXPR RESULT "${A} - ${B}")
    message(STATUS "Вычитание: ${A} - ${B} = ${RESULT}")
    
elseif(OPERATION STREQUAL "*")
    math(EXPR RESULT "${A} * ${B}")
    message(STATUS "Умножение: ${A} * ${B} = ${RESULT}")
    
elseif(OPERATION STREQUAL "/")
    if(B EQUAL 0)
        message(FATAL_ERROR "❌ Ошибка: Деление на ноль невозможно!")
    endif()
    math(EXPR RESULT "${A} / ${B}")
    message(STATUS "Деление: ${A} / ${B} = ${RESULT}")
    
else()
    message(FATAL_ERROR "❌ Неизвестная операция: '${OPERATION}'. Используйте: +, -, *, /")
endif()

# 4. Дополнительные вычисления для демонстрации
message(STATUS "")
message(STATUS "📈 ДОПОЛНИТЕЛЬНЫЕ ВЫЧИСЛЕНИЯ:")
message(STATUS "================================")

math(EXPR SUM "${A} + ${B}")
math(EXPR DIFF "${A} - ${B}") 
math(EXPR MULT "${A} * ${B}")

if(NOT B EQUAL 0)
    math(EXPR DIV "${A} / ${B}")
    message(STATUS "A + B = ${SUM}")
    message(STATUS "A - B = ${DIFF}")
    message(STATUS "A × B = ${MULT}")
    message(STATUS "A ÷ B = ${DIV}")
else()
    message(STATUS "A + B = ${SUM}")
    message(STATUS "A - B = ${DIFF}")
    message(STATUS "A × B = ${MULT}")
    message(STATUS "A ÷ B = невозможно (деление на ноль)")
endif()

# 5. Инструкция для пользователя
message(STATUS "")
message(STATUS "💡 ИНСТРУКЦИЯ:")
message(STATUS "================================")
message(STATUS "Чтобы изменить вычисления:")
message(STATUS "1. Измените значения A, B, OPERATION в CMake GUI")
message(STATUS "2. Нажмите кнопку 'Configure'")
message(STATUS "3. Наблюдайте новые результаты в логе")
message(STATUS "")
message(STATUS "Доступные операции: +, -, *, /")
message(STATUS "==========================================")