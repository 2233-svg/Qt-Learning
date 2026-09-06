# QMimeType

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MimeType”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMimeType` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMimeType>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `aliases : const QStringList`
- `allAncestors : const QStringList`
- `comment : const QString`
- `filterString : const QString`
- `genericIconName : const QString`
- `globPatterns : const QStringList`
- `iconName : const QString`
- `isDefault : const bool`
- `name : const QString`
- `parentMimeTypes : const QStringList`
- `preferredSuffix : const QString`
- `suffixes : const QStringList`
- `valid : const bool`

### 公有函数

- `QMimeType()`
- `QMimeType(const QMimeType &other)`
- `~QMimeType()`
- `QStringList aliases() const`
- `QStringList allAncestors() const`
- `QString comment() const`
- `QString filterString() const`
- `QString genericIconName() const`
- `QStringList globPatterns() const`
- `QString iconName() const`
- `bool inherits(const QString &mimeTypeName) const`
- `bool isDefault() const`
- `bool isValid() const`
- `QString name() const`
- `QStringList parentMimeTypes() const`
- `QString preferredSuffix() const`
- `QStringList suffixes() const`
- `void swap(QMimeType &other)`
- `QMimeType & operator=(QMimeType &&other)`
- `QMimeType & operator=(const QMimeType &other)`

### 相关非成员函数

- `size_t qHash(const QMimeType &key, size_t seed = 0)`
- `bool operator!=(const QMimeType &lhs, const QMimeType &rhs)`
- `bool operator==(const QMimeType &lhs, const QMimeType &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] aliases : const QStringList`

**作用与语义：**

该属性包含该拟态的别名列表。
例如，对于文本/csv，返回的列表会是：text/x-csv，text/x-逗号分隔值。
请注意，所有`QMimeType`实例都指向正规拟态类型，从未直接指代别名。
列表中别名的顺序未明确。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `aliases()` 读取当前值；它不会修改应用状态。

### `[read-only] allAncestors : const QStringList`

**作用与语义：**

该属性保存直接和间接父 MIME 类型的名称。
返回此 MIME 类型的所有父 MIME 类型，包括直接和间接父类型。这包括其父类型的父类型，依此类推。
例如，对于 image/svg xml，列表为：application/xml、text/plain、application/octet-stream。
请注意，application/octet-stream 是所有类型文件的最终父类型（但不包括目录）。
虽然该属性是在 5.10 中引入的，相应的访问方法一直都存在。

**如何使用：** 调用 `allAncestors()` 读取当前值；它不会修改应用状态。

### `[read-only] comment : const QString`

**作用与语义：**

此属性保存用于用户界面显示的 MIME 类型描述。
返回根据用户当前语言设置本地化的 MIME 类型描述。
虽然此属性在 5.10 中引入，但相应的访问方法一直存在。

**如何使用：** 调用 `comment()` 读取当前值；它不会修改应用状态。

### `[read-only] filterString : const QString`

**作用与语义：**

该属性包含可用于文件对话的过滤字符串。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `filterString()` 读取当前值；它不会修改应用状态。

### `[read-only] genericIconName : const QString`

**作用与语义：**

该属性包含代表MIME类型的通用图标的文件名。
如果系统中找不到`iconName()`返回的图标，应使用该格式。该规范用于类似类型的类别（如电子表格或档案），这些类别可以使用共同图标。freedesktop.org 图标命名规范列出了一组此类图标名称。
图标名称可以被赋予`QIcon::fromTheme()`以加载该图标。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `genericIconName()` 读取当前值；它不会修改应用状态。

### `[read-only] globPatterns : const QStringList`

**作用与语义：**

该属性包含了球状匹配模式的列表。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `globPatterns()` 读取当前值；它不会修改应用状态。

### `[read-only] iconName : const QString`

**作用与语义：**

该属性包含代表MIME类型的图标图像的文件名。
图标名称可以被赋予`QIcon::fromTheme()`以加载图标。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `iconName()` 读取当前值；它不会修改应用状态。

### `[read-only] isDefault : const bool`

**作用与语义：**

`true`如果这个MIME类型是适用于所有文件的默认MIME类型：application/octet-stream。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `isDefault()` 读取当前值；它不会修改应用状态。

### `[read-only] name : const QString`

**作用与语义：**

该属性包含了MIME类型的名称。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[read-only] parentMimeTypes : const QStringList`

**作用与语义：**

此属性保存父 MIME 类型的名称。
如果第一类型的任何实例也是第二类型的实例，则该类型是另一类型的子类。例如，所有 image/svg xml 文件也是 text/xml、text/plain 和 application/octet-stream 文件。子类化是关于格式的，而不是数据类别（例如，没有所有电子表格继承的“通用电子表格”类）。相反，image/svg xml 的父 mimetype 是 text/xml。
一个 mimetype 可以有多个父类型。例如，application/x-perl 有两个父类型：application/x-executable 和 text/plain。这使得既可以执行 perl 脚本，也可以在文本编辑器中打开它们。
虽然该属性在 5.10 中引入，但相应的访问方法一直存在。

**如何使用：** 调用 `parentMimeTypes()` 读取当前值；它不会修改应用状态。

### `[read-only] preferredSuffix : const QString`

**作用与语义：**

该属性保留了 MIME 类型的首选后缀。
不包含前置点，例如application/pdf会返回“pdf”。对于没有后缀的mime类型，返回值可以为空。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `preferredSuffix()` 读取当前值；它不会修改应用状态。

### `[read-only] suffixes : const QStringList`

**作用与语义：**

该属性保留了MIME类型的已知后缀。
没有前置点，比如这样会返回“jpg”、“jpeg”（图片/jpeg）。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `suffixes()` 读取当前值；它不会修改应用状态。

### `[read-only] valid : const bool`

**作用与语义：**

`true`如果`QMimeType`对象包含有效数据，否则`false`。
有效的MIME类型具有非空的 `name()`。无效的 MIME 类型是默认构造的`QMimeType`。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `valid()` 读取当前值；它不会修改应用状态。

### `QMimeType::QMimeType()`

**作用与语义：**

构建该QMimeType对象，初始化为默认属性值，表示MIME类型无效。

### `QMimeType::QMimeType(const QMimeType &other)`

**作用与语义：**

构建该QMimeType对象作为`other`的副本。

### `[noexcept] QMimeType::~QMimeType()`

**作用与语义：**

摧毁`QMimeType`对象，释放D指针。

### `[invokable] bool QMimeType::inherits(const QString &mimeTypeName) const`

**作用与语义：**

如果该拟态类型是`mimeTypeName`的，还是继承了`mimeTypeName`（见`parentMimeTypes()`），或者`mimeTypeName`是该模仿类型的别名，返回`true`。
自5.10版本起，该方法已可从QML调用。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[noexcept] void QMimeType::swap(QMimeType &other)`

**作用与语义：**

将哑剧类型与`other`互换。这个操作非常快速，从未失败过。
swap() 方法有助于以例外安全的方式实现赋值操作符。欲了解更多信息，请参阅更多 C 语言 - 复制与交换。

### `[noexcept] QMimeType &QMimeType::operator=(QMimeType &&other)`

**作用与语义：**

Move-assign `other` 到该`QMimeType`实例。

### `QMimeType &QMimeType::operator=(const QMimeType &other)`

**作用与语义：**

将`other`的数据分配给该`QMimeType`对象，并返回对该对象的引用。

### `[noexcept] size_t qHash(const QMimeType &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QMimeType &lhs, const QMimeType &rhs)`

**作用与语义：**

如果`QMimeType` `lhs`不等于`QMimeType` `rhs`，则返回`true`，否则返回`false`。

### `[noexcept] bool operator==(const QMimeType &lhs, const QMimeType &rhs)`

**作用与语义：**

返回`true`如果`lhs` 等于 `rhs` `QMimeType`对象，否则返回`false`名称是 mimetype 的唯一标识符，因此两个具有相同名称的 mimetype 是相等的。

### `QStringList aliases() const`

**作用与语义：**

该属性包含该拟态的别名列表。
例如，对于文本/csv，返回的列表会是：text/x-csv，text/x-逗号分隔值。
请注意，所有`QMimeType`实例都指向正规拟态类型，从未直接指代别名。
列表中别名的顺序未明确。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `aliases()` 读取当前值；它不会修改应用状态。

### `QStringList allAncestors() const`

**作用与语义：**

该属性保存直接和间接父 MIME 类型的名称。
返回此 MIME 类型的所有父 MIME 类型，包括直接和间接父类型。这包括其父类型的父类型，依此类推。
例如，对于 image/svg xml，列表为：application/xml、text/plain、application/octet-stream。
请注意，application/octet-stream 是所有类型文件的最终父类型（但不包括目录）。
虽然该属性是在 5.10 中引入的，相应的访问方法一直都存在。

**如何使用：** 调用 `allAncestors()` 读取当前值；它不会修改应用状态。

### `QString comment() const`

**作用与语义：**

此属性保存用于用户界面显示的 MIME 类型描述。
返回根据用户当前语言设置本地化的 MIME 类型描述。
虽然此属性在 5.10 中引入，但相应的访问方法一直存在。

**如何使用：** 调用 `comment()` 读取当前值；它不会修改应用状态。

### `QString filterString() const`

**作用与语义：**

该属性包含可用于文件对话的过滤字符串。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `filterString()` 读取当前值；它不会修改应用状态。

### `QString genericIconName() const`

**作用与语义：**

该属性包含代表MIME类型的通用图标的文件名。
如果系统中找不到`iconName()`返回的图标，应使用该格式。该规范用于类似类型的类别（如电子表格或档案），这些类别可以使用共同图标。freedesktop.org 图标命名规范列出了一组此类图标名称。
图标名称可以被赋予`QIcon::fromTheme()`以加载该图标。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `genericIconName()` 读取当前值；它不会修改应用状态。

### `QStringList globPatterns() const`

**作用与语义：**

该属性包含了球状匹配模式的列表。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `globPatterns()` 读取当前值；它不会修改应用状态。

### `QString iconName() const`

**作用与语义：**

该属性包含代表MIME类型的图标图像的文件名。
图标名称可以被赋予`QIcon::fromTheme()`以加载图标。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `iconName()` 读取当前值；它不会修改应用状态。

### `bool isDefault() const`

**作用与语义：**

`true`如果这个MIME类型是适用于所有文件的默认MIME类型：application/octet-stream。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `isDefault()` 读取当前值；它不会修改应用状态。

### `bool isValid() const`

**作用与语义：**

`true`如果`QMimeType`对象包含有效数据，否则`false`。
有效的MIME类型具有非空的 `name()`。无效的 MIME 类型是默认构造的`QMimeType`。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `isValid()` 读取当前值；它不会修改应用状态。

### `QString name() const`

**作用与语义：**

该属性包含了MIME类型的名称。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `QStringList parentMimeTypes() const`

**作用与语义：**

此属性保存父 MIME 类型的名称。
如果第一类型的任何实例也是第二类型的实例，则该类型是另一类型的子类。例如，所有 image/svg xml 文件也是 text/xml、text/plain 和 application/octet-stream 文件。子类化是关于格式的，而不是数据类别（例如，没有所有电子表格继承的“通用电子表格”类）。相反，image/svg xml 的父 mimetype 是 text/xml。
一个 mimetype 可以有多个父类型。例如，application/x-perl 有两个父类型：application/x-executable 和 text/plain。这使得既可以执行 perl 脚本，也可以在文本编辑器中打开它们。
虽然该属性在 5.10 中引入，但相应的访问方法一直存在。

**如何使用：** 调用 `parentMimeTypes()` 读取当前值；它不会修改应用状态。

### `QString preferredSuffix() const`

**作用与语义：**

该属性保留了 MIME 类型的首选后缀。
不包含前置点，例如application/pdf会返回“pdf”。对于没有后缀的mime类型，返回值可以为空。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `preferredSuffix()` 读取当前值；它不会修改应用状态。

### `QStringList suffixes() const`

**作用与语义：**

该属性保留了MIME类型的已知后缀。
没有前置点，比如这样会返回“jpg”、“jpeg”（图片/jpeg）。
虽然该属性在5.10中引入，但对应的访问器方法一直存在。

**如何使用：** 调用 `suffixes()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMimeType` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
