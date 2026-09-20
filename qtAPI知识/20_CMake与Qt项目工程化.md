# CMake 与 Qt 项目工程化

> Qt 6 的现代 CMake 集成围绕“目标”组织：目标声明源文件、链接依赖、QML 模块和安装规则。理解目标边界后，自动 moc/uic/rcc、QML 编译、测试注册和部署脚本都能成为可重复的构建步骤。

## 1. 最小 Qt 6 CMake 骨架

```cmake
cmake_minimum_required(VERSION 3.21)
project(HelloQt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_standard_project_setup()

qt_add_executable(HelloQt
    main.cpp
)

target_link_libraries(HelloQt PRIVATE Qt6::Widgets)
```

`find_package(Qt6 ...)` 查找 Qt 安装并导入模块目标；`qt_standard_project_setup()` 设置常用默认值，包括 `CMAKE_AUTOMOC`、`CMAKE_AUTOUIC` 等；`qt_add_executable()` 是带 Qt 平台处理逻辑的可执行目标封装。

## 2. 目标、链接和可见性

### 2.1 PRIVATE、PUBLIC、INTERFACE

```cmake
qt_add_library(businesslogic STATIC
    controller.cpp
    controller.h
)
target_link_libraries(businesslogic
    PUBLIC Qt6::Core
)

qt_add_executable(app main.cpp)
target_link_libraries(app PRIVATE businesslogic Qt6::Widgets)
```

- `PRIVATE`：只有当前目标需要；
- `PUBLIC`：当前目标和依赖它的目标都需要；
- `INTERFACE`：当前目标不编译，但依赖者需要。

库的头文件若暴露 Qt 类型，通常需要把对应 Qt 模块放在 `PUBLIC`；只在 `.cpp` 内部使用的模块可放 `PRIVATE`。错误地使用全局 `include_directories()` 或 `link_libraries()` 会让依赖边界失真。

### 2.2 目录拆分

```cmake
add_subdirectory(src)
add_subdirectory(tests)
```

顶层负责版本、策略和全局选项；子目录负责目标。跨目录共享的变量应尽量改成目标属性、接口库或安装导出目标。

## 3. 自动代码生成：moc、uic、rcc

### 3.1 AUTOMOC

类中包含 `Q_OBJECT`、`Q_GADGET` 等宏时，需要 moc 生成元对象代码。开启 `CMAKE_AUTOMOC` 后，CMake 会扫描目标源文件并自动生成：

```cmake
set(CMAKE_AUTOMOC ON)
qt_add_library(core STATIC person.h person.cpp)
```

现代 Qt 项目通常由 `qt_standard_project_setup()` 设置该选项。头文件应加入目标的源列表，便于 CMake 发现宏和 IDE 展示；不要手写 `#include "moc_xxx.cpp"`，除非使用特殊的单文件实现模式。

### 3.2 AUTOUIC

```cmake
set(CMAKE_AUTOUIC ON)
qt_add_executable(editor
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
)
```

`mainwindow.cpp` 中可包含生成的 `ui_mainwindow.h`。UI 文件路径和目标源列表要一致，否则 uic 可能未运行或生成文件找不到。

### 3.3 AUTORCC 与 qt_add_resources

```cmake
qt_add_resources(app "app_resources"
    PREFIX "/"
    FILES
        assets/logo.png
        qml/Main.qml
)
```

推荐使用目标形式的 `qt_add_resources()`，资源会绑定到目标并在构建中生成。C++ 访问路径为 `:/assets/logo.png`（具体取决于前缀和文件别名）；QML 通常使用 `qrc:/...` URL。

## 4. QML 应用与 qt_add_qml_module

### 4.1 基本写法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
qt_standard_project_setup(REQUIRES 6.5)

qt_add_executable(qmlapp main.cpp)

qt_add_qml_module(qmlapp
    URI Demo.App
    VERSION 1.0
    QML_FILES
        Main.qml
        SettingsPage.qml
    RESOURCES
        assets/logo.png
)

target_link_libraries(qmlapp PRIVATE Qt6::Quick)
```

`qt_add_qml_module()` 会把 QML/JS 文件加入资源，生成 `qmldir` 和类型信息，并运行 QML 编译与 `qmllint` 相关步骤。目标为可执行文件时，QML 模块可直接随应用加载，不必额外创建插件库。

### 4.2 URI、目录和资源前缀

URI 的点号对应模块路径，例如 `Demo.App` 对应 `Demo/App`。源目录结构最好与 URI 的目标路径一致，避免 CMake 发出警告。Qt 6.5 以后 `QTP0001` 新策略下，默认资源前缀为 `/qt/qml/`，模块可通过默认 QML import path 找到。

需要自定义资源布局时显式指定：

```cmake
qt_add_qml_module(qmlapp
    URI Demo.App
    RESOURCE_PREFIX "/custom"
    QML_FILES Main.qml
)
```

不要同时使用多个模块的相同 URI 和版本；这会导致导入解析和插件加载冲突。

### 4.3 QML 单例

```cmake
set_source_files_properties(AppConfig.qml PROPERTIES
    QT_QML_SINGLETON_TYPE TRUE
)

qt_add_qml_module(qmlapp
    URI Demo.App
    QML_FILES AppConfig.qml Main.qml
)
```

`AppConfig.qml` 还需要声明：

```qml
pragma Singleton
import QtQml

QtObject {
    readonly property string apiBase: "https://example.invalid"
}
```

文件属性必须在 `qt_add_qml_module()` 调用前设置。单例适合只读配置和稳定服务，不要把所有可变业务状态都塞进全局单例。

## 5. C++ 标准、编译选项和配置

```cmake
target_compile_features(app PRIVATE cxx_std_17)

target_compile_definitions(app PRIVATE
    APP_VERSION=\"1.0\"
)

target_compile_options(app PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall;-Wextra>
)
```

优先使用目标级配置和生成器表达式，避免修改全局 `CMAKE_CXX_FLAGS`。Debug/Release 差异用 `CMAKE_BUILD_TYPE`（单配置生成器）或 `--config`（Visual Studio 多配置生成器）表达。

## 6. 测试目标与 CTest

```cmake
find_package(Qt6 REQUIRED COMPONENTS Test)
include(CTest)
enable_testing()

qt_add_executable(tst_parser tst_parser.cpp)
target_link_libraries(tst_parser PRIVATE Qt6::Core Qt6::Test)
add_test(NAME parser COMMAND tst_parser)
```

测试目标应与生产目标分离，但可链接同一个业务逻辑库。`include(CTest)` 生成 `test` 目标，之后可用 `ctest --test-dir build --output-on-failure` 执行并显示失败输出。

## 7. 安装和部署

### 7.1 安装目标

```cmake
include(GNUInstallDirs)

install(TARGETS qmlapp
    BUNDLE DESTINATION .
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
```

`qt_standard_project_setup()` 会间接准备常用 GNUInstallDirs 变量，但在独立模块中显式包含更清晰。安装规则描述“产物放在哪里”，不等于“Qt 运行库已经随应用部署”。

### 7.2 Qt 部署脚本

Widgets/普通 Qt 应用可使用：

```cmake
qt_generate_deploy_app_script(
    TARGET qmlapp
    OUTPUT_SCRIPT deploy_script
)
install(SCRIPT ${deploy_script})
```

包含 QML 模块时使用 QML 专用部署命令：

```cmake
qt_generate_deploy_qml_app_script(
    TARGET qmlapp
    OUTPUT_SCRIPT deploy_script
)
install(SCRIPT ${deploy_script})
```

部署脚本会在安装阶段收集 Qt 库、插件和 QML 依赖。插件路径、平台插件、TLS 后端和编解码器仍应在目标机器上做实际启动验证。

## 8. 资源、翻译和安装文件

资源文件适合随二进制发布的图标、QML 和内置模板；用户可替换的配置、缓存和下载内容不应写入 `qrc`。翻译可以通过 `qt_standard_project_setup(I18N_TRANSLATED_LANGUAGES ...)` 和 Qt Linguist 工具链纳入构建，但生成的 `.qm` 文件仍需正确安装或嵌入。

## 9. QML 工具链

`qt_add_qml_module()` 通常创建模块对应的 lint 目标。常见检查包括：

```text
cmake --build build --target all_qmllint
cmake --build build --target Demo_App_qmllint
```

`qmllint` 能发现未解析类型、信号处理器参数错误、缺少 required property 和部分绑定问题。它依赖模块的 `.qmltypes` 类型信息；C++ 类型注册和头文件没有正确加入目标时，lint 可能出现假阴性或假阳性。

## 10. Visual Studio 生成器使用要点

```text
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
```

Visual Studio 是多配置生成器，不能只依赖 `CMAKE_BUILD_TYPE=Debug`。Qt 安装架构、编译器 ABI 和目标架构必须一致；例如 MSVC x64 应链接 MSVC x64 Qt，不要混入 MinGW 构建的库。

## 11. 缓存、增量构建与清理

- 修改 Qt 路径、生成器或架构后，建议使用新的 build 目录；
- CMake 缓存保存了 Qt6_DIR、编译器和策略，不能只改环境变量期待自动迁移；
- 生成的 moc/uic/rcc/QML 缓存属于 build 目录，不要提交到源码仓库；
- “头文件改了但没重新 moc”通常是头文件未列入目标源列表或 AUTOMOC 被关闭。

## 12. 常见错误诊断

| 错误 | 常见原因 | 处理 |
| --- | --- | --- |
| `Could not find a package configuration file provided by Qt6` | `Qt6_DIR` 未指向安装目录 | 指定 Qt 的 `lib/cmake/Qt6` 路径并清理缓存 |
| undefined reference/vtable | 缺少 `Q_OBJECT` 的 moc 或未启用 AUTOMOC | 检查宏、头文件列表和目标属性 |
| QML module not found | URI、资源前缀或部署路径不匹配 | 使用 `qt_add_qml_module` 并检查 `qmldir` |
| Visual Studio 链接架构错误 | Qt 与生成器/架构不一致 | 统一 MSVC/MinGW、x86/x64 和 Debug/Release |
| AUTOUIC 找不到文件 | `.ui` 不在目标源列表或路径错误 | 添加到目标并检查相对路径 |
| 部署后缺少平台插件 | 未安装部署脚本或插件搜索路径错误 | 执行 install 并检查 `platforms` 目录 |
| qmllint 未解析 C++ 类型 | 类型未注册或 `.qmltypes` 未生成 | 将头源加入模块，确认 AUTOMOC 和注册宏 |

## 13. 一套推荐的目标结构

```cmake
qt_add_library(app_core STATIC
    src/controller.cpp
    src/controller.h
)
target_link_libraries(app_core PUBLIC Qt6::Core Qt6::Network)

qt_add_executable(app main.cpp)
target_link_libraries(app PRIVATE app_core Qt6::Quick)
qt_add_qml_module(app URI Demo.App VERSION 1.0 QML_FILES qml/Main.qml)

qt_add_executable(tst_controller tests/tst_controller.cpp)
target_link_libraries(tst_controller PRIVATE app_core Qt6::Test)
add_test(NAME controller COMMAND tst_controller)
```

业务逻辑库不依赖 UI，测试可以快速运行；应用目标负责 Quick/QML；部署和安装规则位于顶层或专用 `cmake/` 目录。这个结构也便于未来拆分插件和复用库。

## 14. 自测题

1. `qt_standard_project_setup()` 通常解决了哪些构建基础问题？
2. 为什么头文件应加入目标源列表？
3. `qt_add_qml_module()` 除了嵌入 QML，还会做什么？
4. Visual Studio 生成器为什么要使用 `--config Debug`？
5. 普通 Qt 部署脚本和 QML 应用部署脚本如何选择？

### 参考答案

1. 设置 AUTOMOC/AUTOUIC 等默认值、安装目录变量和 Qt 项目常用策略。
2. 便于 CMake 扫描 Q_OBJECT 等宏，也让 IDE 和增量构建正确感知依赖。
3. 生成 qmldir/类型信息，编译 QML 资源，并提供 qmllint 等工具目标。
4. Visual Studio 是多配置生成器，配置在构建阶段选择，而不是由单一 `CMAKE_BUILD_TYPE` 决定。
5. 不含 QML 的应用使用 `qt_generate_deploy_app_script()`；包含 QML 模块时使用 `qt_generate_deploy_qml_app_script()`。

## 15. 小结

现代 Qt 工程的核心是“目标化”：每个库和可执行文件明确自己的源文件、Qt 模块、编译选项、资源和测试。QML 项目再由 `qt_add_qml_module()` 管理模块和工具链，发布阶段用 Qt 部署 API 收集运行时依赖。掌握这些边界后，Visual Studio、命令行 CI 和其他生成器可以共享同一套可靠构建描述。
