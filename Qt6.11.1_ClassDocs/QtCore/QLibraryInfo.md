# QLibraryInfo

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QLibraryInfo` 是 Qt 的值类型，围绕“LibraryInfo”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QLibraryInfo` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QLibraryInfo>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum LibraryPath { PrefixPath, DocumentationPath, HeadersPath, LibrariesPath, LibraryExecutablesPath, …, SettingsPath }`

### 静态公有成员

- `bool isDebugBuild()`
- `(since 6.5) bool isSharedBuild()`
- `(since 6.0) QString path(QLibraryInfo::LibraryPath p)`
- `(since 6.8) QStringList paths(QLibraryInfo::LibraryPath p)`
- `QVersionNumber version()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLibraryInfo::LibraryPath`

**作用与语义：**

该枚举类型用于查询特定路径：
- `QLibraryInfo::PrefixPath`：`0`;所有路径的默认前缀。
- `QLibraryInfo::DocumentationPath`：`1`;安装时通往文档的路径。
- `QLibraryInfo::HeadersPath`：`2`;通往所有头部的路径。
- `QLibraryInfo::LibrariesPath`：`3`;通往已安装库的路径。
- `QLibraryInfo::LibraryExecutablesPath`：`4`;运行时库所需的已安装可执行文件路径。
- `QLibraryInfo::BinariesPath`：`5`;通往已安装Qt二进制文件（工具和应用程序）的路径。
- `QLibraryInfo::PluginsPath`：`6`;通往已安装 Qt 插件的路径。
- `QLibraryInfo::QmlImportsPath`：`7`;导入已安装QML扩展的路径。
- `QLibraryInfo::Qml2ImportsPath`：`QmlImportsPath`;该值已被弃用。请使用 QmlImportsPath。
- `QLibraryInfo::ArchDataPath`：`8`;通往通用架构依赖Qt数据的路径。
- `QLibraryInfo::DataPath`：`9`;通往通用架构无关的Qt数据路径。
- `QLibraryInfo::TranslationsPath`：`10`;Qt弦翻译信息的路径。
- `QLibraryInfo::ExamplesPath`：`11`;安装后指向示例的路径。
- `QLibraryInfo::TestsPath`：`12`;通往已安装Qt测试用例的路径。
- `QLibraryInfo::SettingsPath`：`100`;通往 Qt 设置的路径。不适用于 Windows。

### `[static noexcept] bool QLibraryInfo::isDebugBuild()`

**作用与语义：**

如果本次 Qt 构建时启用调试，返回 `true`;如果是在发布模式构建，则返回 false。

### `[static noexcept, since 6.5] bool QLibraryInfo::isSharedBuild()`

**作用与语义：**

如果这是Qt的共享（动态）构建，返回`true`。

### `[static, since 6.0] QString QLibraryInfo::path(QLibraryInfo::LibraryPath p)`

**作用与语义：**

返回`p`指定的路径。
如果qt.conf中列出了多个路径，它只返回第一个路径。

### `[static, since 6.8] QStringList QLibraryInfo::paths(QLibraryInfo::LibraryPath p)`

**作用与语义：**

返回`p`指定的所有路径。

### `[static noexcept] QVersionNumber QLibraryInfo::version()`

**作用与语义：**

返回Qt库的版本。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLibraryInfo` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
