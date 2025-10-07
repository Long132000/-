# Главное приложение
add_executable(main_app main.cpp)

# Условное связывание с библиотеками и добавление определений
if(BUILD_MATH_LIB)
    target_link_libraries(main_app math_lib)
    target_compile_definitions(main_app PRIVATE HAVE_MATH_LIB)
endif()

if(BUILD_STRING_LIB)
    target_link_libraries(main_app string_lib)
    target_compile_definitions(main_app PRIVATE HAVE_STRING_LIB)
endif()

if(BUILD_FILE_LIB)
    target_link_libraries(main_app file_lib)
    target_compile_definitions(main_app PRIVATE HAVE_FILE_LIB)
endif()

message(STATUS "Приложение связано с библиотеками:")
message(STATUS "  MATH: ${BUILD_MATH_LIB}")
message(STATUS "  STRING: ${BUILD_STRING_LIB}")
message(STATUS "  FILE: ${BUILD_FILE_LIB}")