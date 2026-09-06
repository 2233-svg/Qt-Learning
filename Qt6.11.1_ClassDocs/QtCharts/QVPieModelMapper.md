# QVPieModelMapper

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“VPie模型Mapper”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QVPieModelMapper` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QVPieModelMapper>`
- 继承自：QPieModelMapper
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

- `firstRow : int`
- `labelsColumn : int`
- `model : QAbstractItemModel*`
- `rowCount : int`
- `series : QPieSeries*`
- `valuesColumn : int`

### 公有函数

- `QVPieModelMapper(QObject *parent = nullptr)`
- `int firstRow() const`
- `int labelsColumn() const`
- `QAbstractItemModel * model() const`
- `int rowCount() const`
- `QPieSeries * series() const`
- `void setFirstRow(int firstRow)`
- `void setLabelsColumn(int labelsColumn)`
- `void setModel(QAbstractItemModel *model)`
- `void setRowCount(int rowCount)`
- `void setSeries(QPieSeries *series)`
- `void setValuesColumn(int valuesColumn)`
- `int valuesColumn() const`

### 信号

- `void firstRowChanged()`
- `void labelsColumnChanged()`
- `void modelReplaced()`
- `void rowCountChanged()`
- `void seriesReplaced()`
- `void valuesColumnChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `firstRow : int`

**作用与语义：**

该属性保留了包含第一个切片值的模型行。
最低和默认值是0。

**如何使用：** 调用 `firstRow()` 读取当前值；它不会修改应用状态。

### `labelsColumn : int`

**作用与语义：**

该属性保存与饼图扇区标签同步的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `labelsColumn()` 读取当前值；它不会修改应用状态。

### `model : QAbstractItemModel*`

**作用与语义：**

该属性包含映射器所使用的模型。

**如何使用：** 调用 `model()` 读取当前值；它不会修改应用状态。

### `rowCount : int`

**作用与语义：**

该属性包含模型中被映射为饼系列数据的行数。
最小值和默认值为-1（受模型行数限制的数字）。

**如何使用：** 调用 `rowCount()` 读取当前值；它不会修改应用状态。

### `series : QPieSeries*`

**作用与语义：**

该属性包含映射器使用的饼系列。
当序列被映射器设置为映射器时，所有数据都会被丢弃。当指定新序列时，旧序列会被断开（但保持其数据）。

**如何使用：** 调用 `series()` 读取当前值；它不会修改应用状态。

### `valuesColumn : int`

**作用与语义：**

该属性保存与饼图扇区值同步的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `valuesColumn()` 读取当前值；它不会修改应用状态。

### `[explicit] QVPieModelMapper::QVPieModelMapper(QObject *parent = nullptr)`

**作用与语义：**

构造一个映射对象，它是`parent`的子对象。

### `[signal] void QVPieModelMapper::firstRowChanged()`

**作用与语义：**

该属性保留了包含第一个切片值的模型行。
最低和默认值是0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `firstRow` 的变化，不要把它当作普通函数主动调用。

### `int QVPieModelMapper::labelsColumn() const`

**作用与语义：**

返回与饼切片标签同步的模型列。
注意：属性labelsColumn的Getter函数。

### `[signal] void QVPieModelMapper::labelsColumnChanged()`

**作用与语义：**

该属性保存与饼图扇区标签同步的模型列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsColumn` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVPieModelMapper::modelReplaced()`

**作用与语义：**

该属性包含映射器所使用的模型。

**如何使用：** 调用 `modelReplaced()` 读取当前值；它不会修改应用状态。

### `[signal] void QVPieModelMapper::rowCountChanged()`

**作用与语义：**

该属性包含模型中被映射为饼系列数据的行数。
最小值和默认值为-1（受模型行数限制的数字）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `rowCount` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QVPieModelMapper::seriesReplaced()`

**作用与语义：**

该属性包含映射器使用的饼系列。
当序列被映射器设置为映射器时，所有数据都会被丢弃。当指定新序列时，旧序列会被断开（但保持其数据）。

**如何使用：** 调用 `seriesReplaced()` 读取当前值；它不会修改应用状态。

### `void QVPieModelMapper::setLabelsColumn(int labelsColumn)`

**作用与语义：**

该属性保存与饼图扇区标签同步的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setLabelsColumn(...)` 修改 `labelsColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QVPieModelMapper::setValuesColumn(int valuesColumn)`

**作用与语义：**

该属性保存与饼图扇区值同步的模型列。
默认值为-1（无效映射）。

**如何使用：** 调用 `setValuesColumn(...)` 修改 `valuesColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int QVPieModelMapper::valuesColumn() const`

**作用与语义：**

返回与饼的切片值保持同步的模型列。
注意：属性值列的获取函数。

### `[signal] void QVPieModelMapper::valuesColumnChanged()`

**作用与语义：**

该属性保存与饼图扇区值同步的模型列。
默认值为-1（无效映射）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `valuesColumn` 的变化，不要把它当作普通函数主动调用。

### `int firstRow() const`

**作用与语义：**

该属性保留了包含第一个切片值的模型行。
最低和默认值是0。

**如何使用：** 调用 `firstRow()` 读取当前值；它不会修改应用状态。

### `QAbstractItemModel * model() const`

**作用与语义：**

该属性包含映射器所使用的模型。

**如何使用：** 调用 `model()` 读取当前值；它不会修改应用状态。

### `int rowCount() const`

**作用与语义：**

该属性包含模型中被映射为饼系列数据的行数。
最小值和默认值为-1（受模型行数限制的数字）。

**如何使用：** 调用 `rowCount()` 读取当前值；它不会修改应用状态。

### `QPieSeries * series() const`

**作用与语义：**

该属性包含映射器使用的饼系列。
当序列被映射器设置为映射器时，所有数据都会被丢弃。当指定新序列时，旧序列会被断开（但保持其数据）。

**如何使用：** 调用 `series()` 读取当前值；它不会修改应用状态。

### `void setFirstRow(int firstRow)`

**作用与语义：**

该属性保留了包含第一个切片值的模型行。
最低和默认值是0。

**如何使用：** 调用 `setFirstRow(...)` 修改 `firstRow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setModel(QAbstractItemModel *model)`

**作用与语义：**

该属性包含映射器所使用的模型。

**如何使用：** 调用 `setModel(...)` 修改 `model`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRowCount(int rowCount)`

**作用与语义：**

该属性包含模型中被映射为饼系列数据的行数。
最小值和默认值为-1（受模型行数限制的数字）。

**如何使用：** 调用 `setRowCount(...)` 修改 `rowCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSeries(QPieSeries *series)`

**作用与语义：**

该属性包含映射器使用的饼系列。
当序列被映射器设置为映射器时，所有数据都会被丢弃。当指定新序列时，旧序列会被断开（但保持其数据）。

**如何使用：** 调用 `setSeries(...)` 修改 `series`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QVPieModelMapper` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
