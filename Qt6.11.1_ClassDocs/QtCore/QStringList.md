# QStringList

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“String列表”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringList` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStringList>`
- 继承自：QList
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

### 公有函数

- `QStringList(const QList<QString> &other)`
- `QStringList(const QString &str)`
- `QStringList(QList<QString> &&other)`
- `bool contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.9) QStringList filter(const QLatin1StringMatcher &matcher) const`
- `QStringList filter(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QStringList filter(const QRegularExpression &re) const`
- `(since 6.7) QStringList filter(const QStringMatcher &matcher) const`
- `(since 6.7) QStringList filter(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QStringList filter(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(const QRegularExpression &re, qsizetype from = 0) const`
- `QString join(const QString &separator) const`
- `QString join(QChar separator) const`
- `QString join(QLatin1StringView separator) const`
- `QString join(QStringView separator) const`
- `qsizetype lastIndexOf(QLatin1StringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QStringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(const QString &str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(const QRegularExpression &re, qsizetype from = -1) const`
- `qsizetype removeDuplicates()`
- `QStringList & replaceInStrings(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList & replaceInStrings(const QRegularExpression &re, const QString &after)`
- `QStringList & replaceInStrings(QStringView before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList & replaceInStrings(QStringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList & replaceInStrings(const QString &before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `void sort(Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList operator+(const QStringList &other) const`
- `QStringList & operator<<(const QString &str)`
- `QStringList & operator<<(const QList<QString> &other)`
- `QStringList & operator<<(const QStringList &other)`
- `QStringList & operator=(const QList<QString> &other)`
- `QStringList & operator=(QList<QString> &&other)`

### 相关非成员函数

- `QMutableStringListIterator`
- `QStringListIterator`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 39 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QStringList::QStringList(const QList<QString> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QList<QString> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList::QStringList(const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList::QStringList(QList<QString> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QList<QString> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QStringList::contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QStringList::contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QStringList::contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QStringList QStringList::filter(const QLatin1StringMatcher &matcher) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 `matcher` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `matcher`：类型为 `const QLatin1StringMatcher &`。没有默认值，调用时必须提供。传入 `const QLatin1StringMatcher &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QStringList::filter(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 `str`、`cs` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QStringList::filter(const QRegularExpression &re) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 `re` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QStringList QStringList::filter(const QStringMatcher &matcher) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 `matcher` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `matcher`：类型为 `const QStringMatcher &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QStringList QStringList::filter(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 `str`、`cs` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QStringList::filter(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 `str`、`cs` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QStringList::indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QStringList::indexOf(const QRegularExpression &re, qsizetype from = 0) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `re`、`from` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QStringList::join(const QString &separator) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::join` 用于计算、查询或取得与“join”相关的操作。调用时要先确认当前状态和 `separator` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `separator`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QStringList::join(QChar separator) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::join` 用于计算、查询或取得与“join”相关的操作。调用时要先确认当前状态和 `separator` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `separator`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QStringList::join(QLatin1StringView separator) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::join` 用于计算、查询或取得与“join”相关的操作。调用时要先确认当前状态和 `separator` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `separator`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QStringList::join(QStringView separator) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::join` 用于计算、查询或取得与“join”相关的操作。调用时要先确认当前状态和 `separator` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `separator`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QStringList::lastIndexOf(QLatin1StringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QStringList::lastIndexOf(const QRegularExpression &re, qsizetype from = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `re`、`from` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QStringList::removeDuplicates()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeDuplicates`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::replaceInStrings(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::replaceInStrings` 用于计算、查询或取得与“替换、In、Strings”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QStringList &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `before`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::replaceInStrings(const QRegularExpression &re, const QString &after)`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::replaceInStrings` 用于计算、查询或取得与“替换、In、Strings”相关的操作。调用时要先确认当前状态和 `re`、`after` 的有效范围；返回类型是 `QStringList &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::replaceInStrings(QStringView before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::replaceInStrings` 用于计算、查询或取得与“替换、In、Strings”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QStringList &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `before`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::replaceInStrings(QStringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::replaceInStrings` 用于计算、查询或取得与“替换、In、Strings”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QStringList &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `before`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::replaceInStrings(const QString &before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::replaceInStrings` 用于计算、查询或取得与“替换、In、Strings”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QStringList &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `before`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QStringList::sort(Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QStringList::sort` 用于执行与“sort”相关的操作。调用时要先确认当前状态和 `cs` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QStringList::operator+(const QStringList &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `other`：类型为 `const QStringList &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::operator<<(const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::operator<<(const QList<QString> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `other`：类型为 `const QList<QString> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::operator<<(const QStringList &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `other`：类型为 `const QStringList &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::operator=(const QList<QString> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `other`：类型为 `const QList<QString> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList &QStringList::operator=(QList<QString> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStringList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QStringList &`。
- 参数 `other`：类型为 `QList<QString> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QMutableStringListIterator`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QStringList` 的 `Q、Mutable、字符串、List、Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QStringListIterator`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QStringList` 的 `Q、字符串、List、Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 公有函数

**中文解读：** `QStringList::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 公有函数

**中文解读：** `QStringList::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype lastIndexOf(QStringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 公有函数

**中文解读：** `QStringList::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype lastIndexOf(const QString &str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 公有函数

**中文解读：** `QStringList::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QStringList` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
