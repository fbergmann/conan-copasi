PROJECT(CopasiPackageTest)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

ADD_EXECUTABLE(CopasiSE CopasiSE.cpp)
TARGET_LINK_LIBRARIES(CopasiSE ${CONAN_LIBS})
