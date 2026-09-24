cmake_minimum_required(VERSION 3.21)

project(BasicQtWindow VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

file(GLOB_RECURSE BASIC_QT_WINDOW_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/project/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/project/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/project/*.ui"
    "${CMAKE_CURRENT_SOURCE_DIR}/PublicInterFace/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/QMyWidgets/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/QMyWidgets/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Qt-Learing/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Qt-Learing/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/resources/*.qrc"
)

qt_add_executable(BasicQtWindow
    WIN32
    ${BASIC_QT_WINDOW_SOURCES}
)

target_include_directories(BasicQtWindow PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/PublicInterFace"
    "${CMAKE_CURRENT_SOURCE_DIR}/QMyWidgets/WidgetsInterface"
    "${CMAKE_CURRENT_SOURCE_DIR}/Qt-Learing/LearningInterface"
)

target_link_libraries(BasicQtWindow PRIVATE Qt6::Widgets)

if(WIN32)
    get_target_property(QT6_QMAKE_EXECUTABLE Qt6::qmake IMPORTED_LOCATION)
    if(NOT QT6_QMAKE_EXECUTABLE)
        get_target_property(QT6_QMAKE_EXECUTABLE Qt6::qmake IMPORTED_LOCATION_RELEASE)
    endif()

    if(QT6_QMAKE_EXECUTABLE)
        get_filename_component(QT6_BIN_DIR "${QT6_QMAKE_EXECUTABLE}" DIRECTORY)
        set(QT_WINDEPLOYQT "${QT6_BIN_DIR}/windeployqt.exe")
    endif()

    if(QT_WINDEPLOYQT AND EXISTS "${QT_WINDEPLOYQT}")
        add_custom_command(TARGET BasicQtWindow POST_BUILD
            COMMAND "${QT_WINDEPLOYQT}"
                --no-translations
                --dir "$<TARGET_FILE_DIR:BasicQtWindow>"
                "$<TARGET_FILE:BasicQtWindow>"
            VERBATIM
        )
    endif()
endif()
