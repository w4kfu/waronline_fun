include_directories(${CMAKE_SOURCE_DIR}/src/LibTomMath)

set(PATCHER_FILES_SRC
    patcher_file.c
    base64.c
    sha256.c
    patcher_test.c
    )

add_executable(patcher ${PATCHER_FILES_SRC})

target_link_libraries(patcher libtommath)

add_subdirectory(LibTomMath)