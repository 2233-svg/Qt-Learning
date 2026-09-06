# QHCandlestickModelMapper

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“HCandlestick模型Mapper”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QHCandlestickModelMapper` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QHCandlestickModelMapper>`
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

- `closeColumn : int`
- `firstSetRow : int`
- `highColumn : int`
- `lastSetRow : int`
- `lowColumn : int`
- `openColumn : int`
- `timestampColumn : int`

### 公有函数

- `QHCandlestickModelMapper(QObject *parent = nullptr)`
- `int closeColumn() const`
- `int firstSetRow() const`
- `int highColumn() const`
- `int lastSetRow() const`
- `int lowColumn() const`
- `int openColumn() const`
- `void setCloseColumn(int closeColumn)`
- `void setFirstSetRow(int firstSetRow)`
- `void setHighColumn(int highColumn)`
- `void setLastSetRow(int lastSetRow)`
- `void setLowColumn(int lowColumn)`
- `void setOpenColumn(int openColumn)`
- `void setTimestampColumn(int timestampColumn)`
- `int timestampColumn() const`

### 重实现的公有函数

- `virtual Qt::Orientation orientation() const override`

### 信号

- `void closeColumnChanged()`
- `void firstSetRowChanged()`
- `void highColumnChanged()`
- `void lastSetRowChanged()`
- `void lowColumnChanged()`
- `void openColumnChanged()`
- `void timestampColumnChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `closeColumn : int`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项收盘值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `closeColumn()` 读取当前值；它不会修改应用状态。

### `firstSetRow : int`

**作用与语义：**

该属性包含作为第一个项目数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 调用 `firstSetRow()` 读取当前值；它不会修改应用状态。

### `highColumn : int`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最高值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `highColumn()` 读取当前值；它不会修改应用状态。

### `lastSetRow : int`

**作用与语义：**

该属性包含作为最后一项数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 调用 `lastSetRow()` 读取当前值；它不会修改应用状态。

### `lowColumn : int`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最低值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `lowColumn()` 读取当前值；它不会修改应用状态。

### `openColumn : int`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的开盘值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `openColumn()` 读取当前值；它不会修改应用状态。

### `timestampColumn : int`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的时间戳值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `timestampColumn()` 读取当前值；它不会修改应用状态。

### `[explicit] QHCandlestickModelMapper::QHCandlestickModelMapper(QObject *parent = nullptr)`

**作用与语义：**

构建一个水平模型映射对象，该对象是`parent`的子节点。

### `[signal] void QHCandlestickModelMapper::closeColumnChanged()`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项收盘值的列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `closeColumn` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QHCandlestickModelMapper::firstSetRowChanged()`

**作用与语义：**

该属性包含作为第一个项目数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `firstSetRow` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QHCandlestickModelMapper::highColumnChanged()`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最高值的列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `highColumn` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QHCandlestickModelMapper::lastSetRowChanged()`

**作用与语义：**

该属性包含作为最后一项数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `lastSetRow` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QHCandlestickModelMapper::lowColumnChanged()`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最低值的列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `lowColumn` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QHCandlestickModelMapper::openColumnChanged()`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的开盘值的列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `openColumn` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] Qt::Orientation QHCandlestickModelMapper::orientation() const`

**作用与语义：**

重装：`QCandlestickModelMapper::orientation()` const.
返回`Qt::Horizontal`。这意味着从行中读取该项的值。
返回`QCandlestickModelMapper`访问模型时使用的方向。这决定了连续的集合值是从行（`Qt::Horizontal`）读取还是列（`Qt::Vertical`）。

### `[signal] void QHCandlestickModelMapper::timestampColumnChanged()`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的时间戳值的列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `timestampColumn` 的变化，不要把它当作普通函数主动调用。

### `int closeColumn() const`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项收盘值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `closeColumn()` 读取当前值；它不会修改应用状态。

### `int firstSetRow() const`

**作用与语义：**

该属性包含作为第一个项目数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 调用 `firstSetRow()` 读取当前值；它不会修改应用状态。

### `int highColumn() const`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最高值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `highColumn()` 读取当前值；它不会修改应用状态。

### `int lastSetRow() const`

**作用与语义：**

该属性包含作为最后一项数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 调用 `lastSetRow()` 读取当前值；它不会修改应用状态。

### `int lowColumn() const`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最低值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `lowColumn()` 读取当前值；它不会修改应用状态。

### `int openColumn() const`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的开盘值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `openColumn()` 读取当前值；它不会修改应用状态。

### `void setCloseColumn(int closeColumn)`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项收盘值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setCloseColumn(...)` 修改 `closeColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFirstSetRow(int firstSetRow)`

**作用与语义：**

该属性包含作为第一个项目数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setFirstSetRow(...)` 修改 `firstSetRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHighColumn(int highColumn)`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最高值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setHighColumn(...)` 修改 `highColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLastSetRow(int lastSetRow)`

**作用与语义：**

该属性包含作为最后一项数据源的模型行。
默认值为-1（映射无效）。

**如何使用：** 调用 `setLastSetRow(...)` 修改 `lastSetRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLowColumn(int lowColumn)`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的最低值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setLowColumn(...)` 修改 `lowColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpenColumn(int openColumn)`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的开盘值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setOpenColumn(...)` 修改 `openColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTimestampColumn(int timestampColumn)`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的时间戳值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setTimestampColumn(...)` 修改 `timestampColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int timestampColumn() const`

**作用与语义：**

该属性保存模型中包含序列中蜡烛图项的时间戳值的列。
默认值为-1（无效映射）。

**如何使用：** 调用 `timestampColumn()` 读取当前值；它不会修改应用状态。

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

`QHCandlestickModelMapper` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
