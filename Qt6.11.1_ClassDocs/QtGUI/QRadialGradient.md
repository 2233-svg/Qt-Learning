# QRadialGradient

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRadialGradient` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRadialGradient>`
- 继承自：QGradient
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

### 公有函数

- `QRadialGradient()`
- `QRadialGradient(const QPointF &center, qreal radius)`
- `QRadialGradient(const QPointF &center, qreal radius, const QPointF &focalPoint)`
- `QRadialGradient(qreal cx, qreal cy, qreal radius)`
- `QRadialGradient(const QPointF &center, qreal centerRadius, const QPointF &focalPoint, qreal focalRadius)`
- `QRadialGradient(qreal cx, qreal cy, qreal radius, qreal fx, qreal fy)`
- `QRadialGradient(qreal cx, qreal cy, qreal centerRadius, qreal fx, qreal fy, qreal focalRadius)`
- `QPointF center() const`
- `qreal centerRadius() const`
- `QPointF focalPoint() const`
- `qreal focalRadius() const`
- `qreal radius() const`
- `void setCenter(const QPointF &center)`
- `void setCenter(qreal x, qreal y)`
- `void setCenterRadius(qreal radius)`
- `void setFocalPoint(const QPointF &focalPoint)`
- `void setFocalPoint(qreal x, qreal y)`
- `void setFocalRadius(qreal radius)`
- `void setRadius(qreal radius)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QRadialGradient::QRadialGradient()`

**作用与语义：**

构造一个以中心和焦点为（0， 0）为中心的简单径向梯度，半径为1。

### `QRadialGradient::QRadialGradient(const QPointF &center, qreal radius)`

**作用与语义：**

构造一个简单的径向梯度，`center`、`radius`和圆心的焦点。

### `QRadialGradient::QRadialGradient(const QPointF &center, qreal radius, const QPointF &focalPoint)`

**作用与语义：**

构造一个简单的径向梯度，给定`center`、`radius`和`focalPoint`。
注意：如果给定焦点位于`center`点和`radius`定义的圆之外，则会重新调整，使其位于圆与`center`至`focalPoint`线相交的点。

### `QRadialGradient::QRadialGradient(qreal cx, qreal cy, qreal radius)`

**作用与语义：**

构造一个简单的径向梯度，中心为（`cx`， `cy`），`radius`指定。焦点位于圆心。

### `QRadialGradient::QRadialGradient(const QPointF &center, qreal centerRadius, const QPointF &focalPoint, qreal focalRadius)`

**作用与语义：**

构造一个扩展的径向梯度，包含给定的`center`、`centerRadius`、`focalPoint`和`focalRadius`。

### `QRadialGradient::QRadialGradient(qreal cx, qreal cy, qreal radius, qreal fx, qreal fy)`

**作用与语义：**

构造一个简单的径向梯度，中心为给定中心（`cx`，`cy`）、`radius`和焦点（`fx`，`fy`）。
注意：如果给定的焦点位于中心（`cx`、`cy`）与`radius`所定义的圆之外，则会重新调整到从中心到焦点的直线与圆的交点。

### `QRadialGradient::QRadialGradient(qreal cx, qreal cy, qreal centerRadius, qreal fx, qreal fy, qreal focalRadius)`

**作用与语义：**

构造一个扩展径向梯度，中心半径为给定中心（`cx`，`cy`）、中心半径、`centerRadius`、焦点（`fx`，`fy`）和焦半径`focalRadius`。

### `QPointF QRadialGradient::center() const`

**作用与语义：**

返回该径向梯度的中心，映射逻辑坐标。

### `qreal QRadialGradient::centerRadius() const`

**作用与语义：**

返回该径向梯度的中心半径，映射逻辑坐标。

### `QPointF QRadialGradient::focalPoint() const`

**作用与语义：**

返回该径向梯度的焦点，映射逻辑坐标。

### `qreal QRadialGradient::focalRadius() const`

**作用与语义：**

返回该径向梯度的焦半径，映射逻辑坐标。

### `qreal QRadialGradient::radius() const`

**作用与语义：**

返回该径向梯度在逻辑坐标中的半径。
相当于`centerRadius()`。

### `void QRadialGradient::setCenter(const QPointF &center)`

**作用与语义：**

将该径向梯度的中心在逻辑坐标中设为`center`。

### `void QRadialGradient::setCenter(qreal x, qreal y)`

**作用与语义：**

将该径向梯度的中心在逻辑坐标中设置为（`x`， `y`）。

### `void QRadialGradient::setCenterRadius(qreal radius)`

**作用与语义：**

将该径向梯度的中心半径在逻辑坐标中设为`radius`。

### `void QRadialGradient::setFocalPoint(const QPointF &focalPoint)`

**作用与语义：**

将该径向梯度的焦点设为逻辑坐标的 `focalPoint`。

### `void QRadialGradient::setFocalPoint(qreal x, qreal y)`

**作用与语义：**

将该径向梯度的焦点设为逻辑坐标中的 （`x`， `y`）。

### `void QRadialGradient::setFocalRadius(qreal radius)`

**作用与语义：**

将该径向梯度的焦半径在逻辑坐标中设为`radius`。

### `void QRadialGradient::setRadius(qreal radius)`

**作用与语义：**

将该径向梯度在逻辑坐标下的半径设为`radius`。
相当于`setCenterRadius()`。

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

`QRadialGradient` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
