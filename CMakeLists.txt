cmake_minimum_required(VERSION 3.22)
project(KUSB448BInit)


set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake_modules/")

# Libusb stuff
find_package(LibUSB)
include_directories(${LIBUSB_1_INCLUDE_DIRS})
link_libraries(${LIBUSB_1_LIBRARIES})

add_executable(kusb448binit main.cpp KUSB448BInit.hpp)
