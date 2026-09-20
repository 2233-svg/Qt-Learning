cmake_minimum_required(VERSION 3.21)

project(Qt-assisiant VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(Qt-assisiant
    WIN32
    main.cpp
    MainWindow.cpp
    MainWindow.h
)

set_target_properties(Qt-assisiant PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/dist/Qt-assisiant"
)

set(QT_API_VIEWER_PACKAGE_DIR "D:/笔记/qtAPI知识/_viewer/Qt-assisiant-viewer")

target_link_libraries(Qt-assisiant PRIVATE Qt6::Widgets)
target_compile_definitions(Qt-assisiant PRIVATE
    QT_BUNDLED_DOCUMENT_DIRECTORY="${CMAKE_CURRENT_SOURCE_DIR}/Qt6.11.1_ClassDocs"
    QT_ASSISTANT_SOURCE_DIRECTORY="${CMAKE_CURRENT_SOURCE_DIR}"
)

add_custom_command(TARGET Qt-assisiant POST_BUILD
    COMMAND "${CMAKE_COMMAND}" -E copy_directory
        "${CMAKE_CURRENT_SOURCE_DIR}/Qt6.11.1_ClassDocs"
        "$<TARGET_FILE_DIR:Qt-assisiant>/Qt6.11.1_ClassDocs"
    VERBATIM
)

if(WIN32)
    set(QT_WINDEPLOYQT "C:/Qt/6.11.1/mingw_64/bin/windeployqt.exe")

    if(EXISTS "${QT_WINDEPLOYQT}")
        add_custom_command(TARGET Qt-assisiant POST_BUILD
            COMMAND "${QT_WINDEPLOYQT}"
                --no-translations
                --dir "$<TARGET_FILE_DIR:Qt-assisiant>"
                "$<TARGET_FILE:Qt-assisiant>"
            VERBATIM
        )
    endif()
endif()

add_custom_command(TARGET Qt-assisiant POST_BUILD
    COMMAND "${CMAKE_COMMAND}" -E copy_directory
        "$<TARGET_FILE_DIR:Qt-assisiant>"
        "${QT_API_VIEWER_PACKAGE_DIR}"
    VERBATIM
)
