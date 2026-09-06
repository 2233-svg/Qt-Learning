# QRegularExpressionValidator

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRegularExpressionValidator` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRegularExpressionValidator>`
- 继承自：QValidator
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
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

- `regularExpression : QRegularExpression`

### 公有函数

- `QRegularExpressionValidator(QObject *parent = nullptr)`
- `QRegularExpressionValidator(const QRegularExpression &re, QObject *parent = nullptr)`
- `virtual ~QRegularExpressionValidator()`
- `QRegularExpression regularExpression() const`

### 重实现的公有函数

- `virtual QValidator::State validate(QString &input, int &pos) const override`

### 公有槽函数

- `void setRegularExpression(const QRegularExpression &re)`

### 信号

- `void regularExpressionChanged(const QRegularExpression &re)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `regularExpression : QRegularExpression`

**作用与语义：**

该属性包含用于验证的正则表达式。
默认情况下，该属性包含一个空模式的正则表达式（因此与任意字符串匹配）。

**如何使用：** 调用 `regularExpression()` 读取当前值；它不会修改应用状态。

### `[explicit] QRegularExpressionValidator::QRegularExpressionValidator(QObject *parent = nullptr)`

**作用与语义：**

构造一个带有`parent`对象的验证器，接受任意字符串（包括空字符串）为有效。

### `[explicit] QRegularExpressionValidator::QRegularExpressionValidator(const QRegularExpression &re, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有`parent`对象的验证器，接受所有与正则表达式`re`匹配的字符串。

### `[virtual noexcept] QRegularExpressionValidator::~QRegularExpressionValidator()`

**作用与语义：**

摧毁验证器。

### `[override virtual] QValidator::State QRegularExpressionValidator::validate(QString &input, int &pos) const`

**作用与语义：**

重实现自：`QValidator::validate`（QString & input， int and pos） const.
如果`input`被该验证子的正则表达式匹配，返回`Acceptable`，`Intermediate`是否部分匹配（即添加更多有效字符时可能为有效匹配），如果`input`未匹配，返回`Invalid`。
如果`input`不匹配，`pos`参数设为`input`参数的长度;否则不修改。
例如，如果正则表达式是 \w\d\d（字-字符，数字，数字），那么“A57”是`Acceptable`，“E5”是`Intermediate`，“9”是`Invalid`。
如果`input`根据该验证者的规则无效，`Intermediate`如果稍作编辑能使输入可接受（例如用户在接受整数介于 10 到 99 的小部件中输入“4”），以及`Acceptable`输入是否有效，该虚拟函数会返回`Invalid`。
该函数可以同时改变`input`和`pos`（光标位置）。

### `QRegularExpression regularExpression() const`

**作用与语义：**

该属性包含用于验证的正则表达式。
默认情况下，该属性包含一个空模式的正则表达式（因此与任意字符串匹配）。

**如何使用：** 调用 `regularExpression()` 读取当前值；它不会修改应用状态。

### `void setRegularExpression(const QRegularExpression &re)`

**作用与语义：**

该属性包含用于验证的正则表达式。
默认情况下，该属性包含一个空模式的正则表达式（因此与任意字符串匹配）。

**如何使用：** 调用 `setRegularExpression(...)` 修改 `regularExpression`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void regularExpressionChanged(const QRegularExpression &re)`

**作用与语义：**

该属性包含用于验证的正则表达式。
默认情况下，该属性包含一个空模式的正则表达式（因此与任意字符串匹配）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `regularExpression` 的变化，不要把它当作普通函数主动调用。

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

`QRegularExpressionValidator` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
