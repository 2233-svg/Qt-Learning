cmake_minimum_required(VERSION 3.21)

project(BasicQtWindow VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

qt_add_executable(BasicQtWindow
    WIN32
    main.cpp
    MainWindow.cpp
    MainWindow.h
)

target_link_libraries(BasicQtWindow PRIVATE Qt6::Widgets)

if(WIN32)
    set(QT_WINDEPLOYQT "D:/QTforGui/qt/6.11.1/mingw_64/bin/windeployqt.exe")

    if(EXISTS "${QT_WINDEPLOYQT}")
        add_custom_command(TARGET BasicQtWindow POST_BUILD
            COMMAND "${QT_WINDEPLOYQT}"
                --no-translations
                --dir "$<TARGET_FILE_DIR:BasicQtWindow>"
                "$<TARGET_FILE:BasicQtWindow>"
            VERBATIM
        )
    endif()
endif()

