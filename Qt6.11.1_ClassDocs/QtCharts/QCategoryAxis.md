# QCategoryAxis

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“Category坐标轴”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QCategoryAxis` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCategoryAxis>`
- 继承自：QValueAxis
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

### 公有类型

- `enum AxisLabelsPosition { AxisLabelsPositionCenter, AxisLabelsPositionOnValue }`

### 属性

- `categoriesLabels : QStringList`
- `count : int`
- `labelsPosition : AxisLabelsPosition`
- `startValue : qreal`

### 公有函数

- `QCategoryAxis(QObject *parent = nullptr)`
- `virtual ~QCategoryAxis()`
- `void append(const QString &categoryLabel, qreal categoryEndValue)`
- `QStringList categoriesLabels()`
- `int count() const`
- `qreal endValue(const QString &categoryLabel) const`
- `QCategoryAxis::AxisLabelsPosition labelsPosition() const`
- `void remove(const QString &categoryLabel)`
- `void replaceLabel(const QString &oldLabel, const QString &newLabel)`
- `void setLabelsPosition(QCategoryAxis::AxisLabelsPosition position)`
- `void setStartValue(qreal min)`
- `qreal startValue(const QString &categoryLabel = QString()) const`

### 重实现的公有函数

- `virtual QAbstractAxis::AxisType type() const override`

### 信号

- `void categoriesChanged()`
- `void labelsPositionChanged(QCategoryAxis::AxisLabelsPosition position)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCategoryAxis::AxisLabelsPosition`

**作用与语义：**

该枚举描述了范畴标签的位置。
- `QCategoryAxis::AxisLabelsPositionCenter`：`0x0`;标签置中于类别。
- `QCategoryAxis::AxisLabelsPositionOnValue`：`0x1`;标签定位到类别的最高端。

### `[read-only] categoriesLabels : QStringList`

**作用与语义：**

该属性将类别标签作为字符串列表保存。

**如何使用：** 调用 `categoriesLabels()` 读取当前值；它不会修改应用状态。

### `[read-only] count : int`

**作用与语义：**

此属性保存类别数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `labelsPosition : AxisLabelsPosition`

**作用与语义：**

此属性保存类别标签的位置。在轴开始和结束处的标签在以值定位时可能会与其他轴的标签重叠。

**如何使用：** 调用 `labelsPosition()` 读取当前值；它不会修改应用状态。

### `startValue : qreal`

**作用与语义：**

该属性在轴上保持第一类的下端。

**如何使用：** 调用 `startValue()` 读取当前值；它不会修改应用状态。

### `[explicit] QCategoryAxis::QCategoryAxis(QObject *parent = nullptr)`

**作用与语义：**

构造一个轴对象，该轴对象是`parent`的子节点。

### `[virtual noexcept] QCategoryAxis::~QCategoryAxis()`

**作用与语义：**

摧毁了该物体。

### `void QCategoryAxis::append(const QString &categoryLabel, qreal categoryEndValue)`

**作用与语义：**

在轴上附加一个新范畴，标签为`categoryLabel`。范畴标签必须是唯一的。`categoryEndValue`指定了范畴的最高极限。它必须大于前一个范畴的最高极限。否则，方法返回时不添加新范畴。

### `[signal] void QCategoryAxis::categoriesChanged()`

**作用与语义：**

当轴的范畴发生变化时，该信号会发出。

### `QStringList QCategoryAxis::categoriesLabels()`

**作用与语义：**

返回类别标签列表。
注意：属性分类标签的获取函数。

### `int QCategoryAxis::count() const`

**作用与语义：**

返回类别数量。
注意：属性计数的获取函数。

### `qreal QCategoryAxis::endValue(const QString &categoryLabel) const`

**作用与语义：**

返回`categoryLabel`指定类别的最高上限。

### `void QCategoryAxis::remove(const QString &categoryLabel)`

**作用与语义：**

移除由标签`categoryLabel`指定的一个范畴。

### `void QCategoryAxis::replaceLabel(const QString &oldLabel, const QString &newLabel)`

**作用与语义：**

用`newLabel`替换`oldLabel`指定的现有类别标签。如果旧标签不存在，方法返回时不做任何更改。

### `void QCategoryAxis::setStartValue(qreal min)`

**作用与语义：**

该属性在轴上保持第一类的下端。

**如何使用：** 调用 `setStartValue(...)` 修改 `startValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `qreal QCategoryAxis::startValue(const QString &categoryLabel = QString()) const`

**作用与语义：**

返回`categoryLabel`指定类别的最低限值。
注意：属性 startValue 的 Getter 函数。

### `[override virtual] QAbstractAxis::AxisType QCategoryAxis::type() const`

**作用与语义：**

重装：`QValueAxis::type()` const.
返回轴的类型。

### `QCategoryAxis::AxisLabelsPosition labelsPosition() const`

**作用与语义：**

此属性保存类别标签的位置。在轴开始和结束处的标签在以值定位时可能会与其他轴的标签重叠。

**如何使用：** 调用 `labelsPosition()` 读取当前值；它不会修改应用状态。

### `void setLabelsPosition(QCategoryAxis::AxisLabelsPosition position)`

**作用与语义：**

此属性保存类别标签的位置。在轴开始和结束处的标签在以值定位时可能会与其他轴的标签重叠。

**如何使用：** 调用 `setLabelsPosition(...)` 修改 `labelsPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void labelsPositionChanged(QCategoryAxis::AxisLabelsPosition position)`

**作用与语义：**

此属性保存类别标签的位置。在轴开始和结束处的标签在以值定位时可能会与其他轴的标签重叠。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsPosition` 的变化，不要把它当作普通函数主动调用。

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

`QCategoryAxis` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
