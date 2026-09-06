# QDoubleValidator

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QDoubleValidator` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDoubleValidator>`
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

### 公有类型

- `enum Notation { StandardNotation, ScientificNotation }`

### 属性

- `bottom : double`
- `decimals : int`
- `notation : Notation`
- `top : double`

### 公有函数

- `QDoubleValidator(QObject *parent = nullptr)`
- `QDoubleValidator(double bottom, double top, int decimals, QObject *parent = nullptr)`
- `virtual ~QDoubleValidator()`
- `double bottom() const`
- `int decimals() const`
- `QDoubleValidator::Notation notation() const`
- `void setBottom(double)`
- `void setDecimals(int)`
- `void setNotation(QDoubleValidator::Notation)`
- `void setRange(double minimum, double maximum, int decimals)`
- `void setRange(double minimum, double maximum)`
- `void setTop(double)`
- `double top() const`

### 重实现的公有函数

- `(since 6.3) virtual void fixup(QString &input) const override`
- `virtual QValidator::State validate(QString &input, int &pos) const override`

### 信号

- `void bottomChanged(double bottom)`
- `void decimalsChanged(int decimals)`
- `void notationChanged(QDoubleValidator::Notation notation)`
- `void topChanged(double top)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDoubleValidator::Notation`

**作用与语义：**

该枚举定义了输入 double 的允许表示法。
- `QDoubleValidator::StandardNotation`: `0`；字符串以标准格式书写，整数部分可选后跟分隔符和小数部分，例如 `"0.015"`。
- `QDoubleValidator::ScientificNotation`: `1`；字符串以科学记数法书写，可选择在标准格式后附加指数部分，例如 `"1.5E-2"`。
整数部分可以像平常一样包含符号。分数部分、指数和任何数字分组的分隔符依赖于区域设置。`QDoubleValidator` 不检查它发现的任何数字分组分隔符的放置位置（这也依赖于区域设置），但如果 `QLocale::RejectGroupSeparator` 在 `locale().numberOptions()` 中设置，它将拒绝包含这些分隔符的输入。

### `bottom : double`

**作用与语义：**

该属性表示验证者的最小可接受值。
默认情况下，该属性包含一个-无穷大的值。

**如何使用：** 调用 `bottom()` 读取当前值；它不会修改应用状态。

### `decimals : int`

**作用与语义：**

该属性表示验证者小数点后最大数字数。
默认情况下，该属性包含 -1 的值，这意味着任意数字都被接受。

**如何使用：** 调用 `decimals()` 读取当前值；它不会修改应用状态。

### `notation : Notation`

**作用与语义：**

此属性保存字符串描述数字的记法。
默认情况下，该属性设置为 `ScientificNotation`。

**如何使用：** 调用 `notation()` 读取当前值；它不会修改应用状态。

### `top : double`

**作用与语义：**

该属性包含验证者的最大可接受值。
默认情况下，该属性包含一个无穷大的值。

**如何使用：** 调用 `top()` 读取当前值；它不会修改应用状态。

### `[explicit] QDoubleValidator::QDoubleValidator(QObject *parent = nullptr)`

**作用与语义：**

构造一个验证对象，包含一个接受任意双重的`parent`对象。

### `QDoubleValidator::QDoubleValidator(double bottom, double top, int decimals, QObject *parent = nullptr)`

**作用与语义：**

用`parent`对象构造验证对象。该验证器接受从`bottom`到`top`含双倍，小数点后最多`decimals`位。

### `[virtual noexcept] QDoubleValidator::~QDoubleValidator()`

**作用与语义：**

摧毁验证器。

### `[override virtual, since 6.3] void QDoubleValidator::fixup(QString &input) const`

**作用与语义：**

重构：`QValidator::fixup`（QString & input） const.
尝试将`input`字符串固定到`Acceptable`的双重表示上。
号码的格式由`notation()`、`decimals()`、`locale()`以及后者的 `numberOptions()` 决定。
为了符合`notation()`，使用`ScientificNotation`时，固定值会以归一化的形式表示，这意味着任何非零值在小数点前都会有一个非零数字。
为符合`decimals()`，`-1`时使用的数字数由`QLocale::FloatingPointShortest`确定。否则，如果数字长度超过`decimals()`，则对小数部分进行截断（适当四舍五入）。当`notation()`被`ScientificNotation`时，是在数字归一化后进行的。
注意：如果`decimals()`设置为，且字符串提供超过`std::numeric_limits<double>::digits10`，分数部分的数字可能会被更改。解析为`double`时，生成字符串应编码相同的浮点数。
该函数尝试根据验证者的规则将`input`更改为有效。它不一定生成有效字符串：调用该函数的人必须事后重新测试;默认值不做任何事。
该函数的重实现即使不产生有效字符串，也可能`input`变化。例如，ISBN验证器可能希望删除除数字和“-”以外的所有字符，即使结果仍不是有效的ISBN;姓氏验证器可能希望移除字符串开头和结尾的空白，即使最终字符串不在接受的姓氏列表中。

**官方示例：**

```cpp
 QString input = "0.98765e2";
 QDoubleValidator val;
 val.setLocale(QLocale::C);
 val.setNotation(QDoubleValidator::ScientificNotation);
 val.fixup(input); // input == "9.8765e+01"
```

### `void QDoubleValidator::setRange(double minimum, double maximum, int decimals)`

**作用与语义：**

设置验证器接受从`minimum`到`maximum`含的双数，小数点后最多`decimals`位。
注意：将小数点设为-1实际上使其为无限。这也是默认构造验证者使用的值。

### `void QDoubleValidator::setRange(double minimum, double maximum)`

**作用与语义：**

设置验证器接受从`minimum`到`maximum`包含的双倍，且不更改小数点后的数字数。

### `[override virtual] QValidator::State QDoubleValidator::validate(QString &input, int &pos) const`

**作用与语义：**

重实现自：`QValidator::validate`（QString & input， int and pos） const.
如果字符串`input`格式正确且包含在有效范围内的双重，返回`Acceptable`。
如果`input`格式错误或包含超出范围的双重信号，返回`Intermediate`。
如果`input`不代表双数或小数点后数字过多，返回`Invalid`。
注意：如果有效范围仅由正双倍组成（例如0.0到100.0），且`input`为负双倍，则返回`Invalid`。如果`notation()`设为`StandardNotation`，且输入小数点前的数字比有效范围内的双倍数字更多，则返回`Invalid`。如果`notation()` `ScientificNotation`且输入不在有效范围内，则返回`Intermediate`。通过改变指数，这个值仍可能变得有效。
默认情况下，该验证者不使用 `pos` 参数。
如果`input`根据验证者的规则无效，`Intermediate`如果稍作编辑后输入可接受（例如用户在接受整数介于10到99的小部件中输入“4”），`Acceptable`输入是否有效，该虚拟函数会返回`Invalid`。
该函数可以根据需要同时改变`input`和`pos`（光标位置）。

### `double bottom() const`

**作用与语义：**

该属性表示验证者的最小可接受值。
默认情况下，该属性包含一个-无穷大的值。

**如何使用：** 调用 `bottom()` 读取当前值；它不会修改应用状态。

### `int decimals() const`

**作用与语义：**

该属性表示验证者小数点后最大数字数。
默认情况下，该属性包含 -1 的值，这意味着任意数字都被接受。

**如何使用：** 调用 `decimals()` 读取当前值；它不会修改应用状态。

### `QDoubleValidator::Notation notation() const`

**作用与语义：**

此属性保存字符串描述数字的记法。
默认情况下，该属性设置为 `ScientificNotation`。

**如何使用：** 调用 `notation()` 读取当前值；它不会修改应用状态。

### `void setBottom(double)`

**作用与语义：**

该属性表示验证者的最小可接受值。
默认情况下，该属性包含一个-无穷大的值。

**如何使用：** 调用 `setBottom(...)` 修改 `bottom`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDecimals(int)`

**作用与语义：**

该属性表示验证者小数点后最大数字数。
默认情况下，该属性包含 -1 的值，这意味着任意数字都被接受。

**如何使用：** 调用 `setDecimals(...)` 修改 `decimals`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNotation(QDoubleValidator::Notation)`

**作用与语义：**

此属性保存字符串描述数字的记法。
默认情况下，该属性设置为 `ScientificNotation`。

**如何使用：** 调用 `setNotation(...)` 修改 `notation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTop(double)`

**作用与语义：**

该属性包含验证者的最大可接受值。
默认情况下，该属性包含一个无穷大的值。

**如何使用：** 调用 `setTop(...)` 修改 `top`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `double top() const`

**作用与语义：**

该属性包含验证者的最大可接受值。
默认情况下，该属性包含一个无穷大的值。

**如何使用：** 调用 `top()` 读取当前值；它不会修改应用状态。

### `void bottomChanged(double bottom)`

**作用与语义：**

该属性表示验证者的最小可接受值。
默认情况下，该属性包含一个-无穷大的值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bottom` 的变化，不要把它当作普通函数主动调用。

### `void decimalsChanged(int decimals)`

**作用与语义：**

该属性表示验证者小数点后最大数字数。
默认情况下，该属性包含 -1 的值，这意味着任意数字都被接受。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `decimals` 的变化，不要把它当作普通函数主动调用。

### `void notationChanged(QDoubleValidator::Notation notation)`

**作用与语义：**

此属性保存字符串描述数字的记法。
默认情况下，该属性设置为 `ScientificNotation`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `notation` 的变化，不要把它当作普通函数主动调用。

### `void topChanged(double top)`

**作用与语义：**

该属性包含验证者的最大可接受值。
默认情况下，该属性包含一个无穷大的值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `top` 的变化，不要把它当作普通函数主动调用。

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

`QDoubleValidator` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
