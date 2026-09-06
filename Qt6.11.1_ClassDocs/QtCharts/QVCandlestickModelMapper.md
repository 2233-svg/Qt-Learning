# QVCandlestickModelMapper

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“VCandlestick模型Mapper”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QVCandlestickModelMapper` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QVCandlestickModelMapper>`
- 继承自：QCandlestickModelMapper
- 直接派生类：未在类页中列出

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

- `closeRow : int`
- `firstSetColumn : int`
- `highRow : int`
- `lastSetColumn : int`
- `lowRow : int`
- `openRow : int`
- `timestampRow : int`

### 公有函数

- `QVCandlestickModelMapper(QObject *parent = nullptr)`
- `int closeRow() const`
- `int firstSetColumn() const`
- `int highRow() const`
- `int lastSetColumn() const`
- `int lowRow() const`
- `int openRow() const`
- `void setCloseRow(int closeRow)`
- `void setFirstSetColumn(int firstSetColumn)`
- `void setHighRow(int highRow)`
- `void setLastSetColumn(int lastSetColumn)`
- `void setLowRow(int lowRow)`
- `void setOpenRow(int openRow)`
- `void setTimestampRow(int timestampRow)`
- `int timestampRow() const`

### 重实现的公有函数

- `virtual Qt::Orientation orientation() const override`

### 信号

- `void closeRowChanged()`
- `void firstSetColumnChanged()`
- `void highRowChanged()`
- `void lastSetColumnChanged()`
- `void lowRowChanged()`
- `void openRowChanged()`
- `void timestampRowChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `closeRow : int`

**作用与语义：**

该属性包含模型中包含系列中接近蜡烛点数值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `closeRow()` 读取当前值；它不会修改应用状态。

### `firstSetColumn : int`

**作用与语义：**

该属性保存作为第一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `firstSetColumn()` 读取当前值；它不会修改应用状态。

### `highRow : int`

**作用与语义：**

该属性保留模型中包含系列中蜡烛柱项高值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `highRow()` 读取当前值；它不会修改应用状态。

### `lastSetColumn : int`

**作用与语义：**

该属性保存作为最后一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `lastSetColumn()` 读取当前值；它不会修改应用状态。

### `lowRow : int`

**作用与语义：**

该属性保留模型中包含系列中低点烛台项的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `lowRow()` 读取当前值；它不会修改应用状态。

### `openRow : int`

**作用与语义：**

该属性保留模型中包含系列中烛台项开值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `openRow()` 读取当前值；它不会修改应用状态。

### `timestampRow : int`

**作用与语义：**

该属性保留模型中包含该系列中烛台项目时间戳值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `timestampRow()` 读取当前值；它不会修改应用状态。

### `[explicit] QVCandlestickModelMapper::QVCandlestickModelMapper(QObject *parent = nullptr)`

**作用与语义：**

构建一个垂直模型映射对象，该对象是`parent`的子节点。

### `[signal] void QVCandlestickModelMapper::closeRowChanged()`

**作用与语义：**

该属性包含模型中包含系列中接近蜡烛点数值的行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `closeRow` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVCandlestickModelMapper::firstSetColumnChanged()`

**作用与语义：**

该属性保存作为第一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `firstSetColumn` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVCandlestickModelMapper::highRowChanged()`

**作用与语义：**

该属性保留模型中包含系列中蜡烛柱项高值的行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `highRow` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVCandlestickModelMapper::lastSetColumnChanged()`

**作用与语义：**

该属性保存作为最后一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `lastSetColumn` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVCandlestickModelMapper::lowRowChanged()`

**作用与语义：**

该属性保留模型中包含系列中低点烛台项的行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `lowRow` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVCandlestickModelMapper::openRowChanged()`

**作用与语义：**

该属性保留模型中包含系列中烛台项开值的行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `openRow` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] Qt::Orientation QVCandlestickModelMapper::orientation() const`

**作用与语义：**

重装：`QCandlestickModelMapper::orientation()` const.
返回`Qt::Vertical`。这意味着从列中读取该项的值。
返回`QCandlestickModelMapper`访问模型时使用的方向。这决定了连续集合的值是从行（`Qt::Horizontal`）读取还是从列（`Qt::Vertical`）读取。

### `[signal] void QVCandlestickModelMapper::timestampRowChanged()`

**作用与语义：**

该属性保留模型中包含该系列中烛台项目时间戳值的行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `timestampRow` 的变化，不要把它当作普通函数主动调用。

### `int closeRow() const`

**作用与语义：**

该属性包含模型中包含系列中接近蜡烛点数值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `closeRow()` 读取当前值；它不会修改应用状态。

### `int firstSetColumn() const`

**作用与语义：**

该属性保存作为第一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `firstSetColumn()` 读取当前值；它不会修改应用状态。

### `int highRow() const`

**作用与语义：**

该属性保留模型中包含系列中蜡烛柱项高值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `highRow()` 读取当前值；它不会修改应用状态。

### `int lastSetColumn() const`

**作用与语义：**

该属性保存作为最后一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `lastSetColumn()` 读取当前值；它不会修改应用状态。

### `int lowRow() const`

**作用与语义：**

该属性保留模型中包含系列中低点烛台项的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `lowRow()` 读取当前值；它不会修改应用状态。

### `int openRow() const`

**作用与语义：**

该属性保留模型中包含系列中烛台项开值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `openRow()` 读取当前值；它不会修改应用状态。

### `void setCloseRow(int closeRow)`

**作用与语义：**

该属性包含模型中包含系列中接近蜡烛点数值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setCloseRow(...)` 修改 `closeRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFirstSetColumn(int firstSetColumn)`

**作用与语义：**

该属性保存作为第一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setFirstSetColumn(...)` 修改 `firstSetColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHighRow(int highRow)`

**作用与语义：**

该属性保留模型中包含系列中蜡烛柱项高值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setHighRow(...)` 修改 `highRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLastSetColumn(int lastSetColumn)`

**作用与语义：**

该属性保存作为最后一个项数据源的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setLastSetColumn(...)` 修改 `lastSetColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLowRow(int lowRow)`

**作用与语义：**

该属性保留模型中包含系列中低点烛台项的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setLowRow(...)` 修改 `lowRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpenRow(int openRow)`

**作用与语义：**

该属性保留模型中包含系列中烛台项开值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setOpenRow(...)` 修改 `openRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTimestampRow(int timestampRow)`

**作用与语义：**

该属性保留模型中包含该系列中烛台项目时间戳值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setTimestampRow(...)` 修改 `timestampRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int timestampRow() const`

**作用与语义：**

该属性保留模型中包含该系列中烛台项目时间戳值的行。
默认值为-1（映射无效）。

**如何使用：** 调用 `timestampRow()` 读取当前值；它不会修改应用状态。

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

`QVCandlestickModelMapper` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
