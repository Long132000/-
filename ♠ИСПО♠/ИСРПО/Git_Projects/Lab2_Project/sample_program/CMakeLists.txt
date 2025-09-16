add_executable(sample_program main.cpp)
target_link_libraries(sample_program sample_lib)
target_include_directories(sample_program PRIVATE ../sample_lib)