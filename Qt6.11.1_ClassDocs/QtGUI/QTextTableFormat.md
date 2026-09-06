# QTextTableFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextTableFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextTableFormat>`
- 继承自：QTextFrameFormat
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

- `QTextTableFormat()`
- `Qt::Alignment alignment() const`
- `bool borderCollapse() const`
- `qreal cellPadding() const`
- `qreal cellSpacing() const`
- `void clearColumnWidthConstraints()`
- `QList<QTextLength> columnWidthConstraints() const`
- `int columns() const`
- `int headerRowCount() const`
- `bool isValid() const`
- `void setAlignment(Qt::Alignment alignment)`
- `void setBorderCollapse(bool borderCollapse)`
- `void setCellPadding(qreal padding)`
- `void setCellSpacing(qreal spacing)`
- `void setColumnWidthConstraints(const QList<QTextLength> &constraints)`
- `void setHeaderRowCount(int count)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTextTableFormat::QTextTableFormat()`

**作用与语义：**

构建一个新的表格格式对象。

### `Qt::Alignment QTextTableFormat::alignment() const`

**作用与语义：**

返回表的对齐。

### `bool QTextTableFormat::borderCollapse() const`

**作用与语义：**

如果表格边框要合并，则返回 `true`。默认值是 `true`。

### `qreal QTextTableFormat::cellPadding() const`

**作用与语义：**

返回表的单元格填充。这描述了单元格边界与其内容之间的距离。

### `qreal QTextTableFormat::cellSpacing() const`

**作用与语义：**

返回表的单元格间距。这描述了相邻单元之间的距离。

### `void QTextTableFormat::clearColumnWidthConstraints()`

**作用与语义：**

清除表格的列宽限制。

### `QList<QTextLength> QTextTableFormat::columnWidthConstraints() const`

**作用与语义：**

返回该表格式用于控制表中列的约束列表。

### `int QTextTableFormat::columns() const`

**作用与语义：**

返回表格格式指定的列数。

### `int QTextTableFormat::headerRowCount() const`

**作用与语义：**

返回表中定义头部的行数。

### `bool QTextTableFormat::isValid() const`

**作用与语义：**

如果此表格格式有效，则返回 `true`；否则返回 `false`。

### `void QTextTableFormat::setAlignment(Qt::Alignment alignment)`

**作用与语义：**

摆好餐桌的正`alignment`。

### `void QTextTableFormat::setBorderCollapse(bool borderCollapse)`

**作用与语义：**

默认情况下，`borderCollapse()` 是`true`，这具有以下含义：
- 表格的边界和网格将按照CSS表`border-collapse`：`collapse`规则进行渲染
- 将`border`属性设置为最小值为`1`，将使用`borderBrush`属性和指定的外边框渲染一个像素实体的内表网格
- `QTextTableCellFormat` 的各种边框样式属性可用于自定义网格，并优先于表格的边界和网格
- `cellSpacing`属性将被忽略
- 用于印刷分页：
页面上的列继续不会渲染其顶部单元格边界。
重复的头部行总是会渲染其底部单元格的边界。
`borderCollapse`设置为`false`时，单元格边界仍可用`QTextTableCellFormat`样式，但样式只能在单元格框架内应用，这在实际中可能不太实用。
注意：在 6.8 之前的 Qt 版本中，默认值是 `false`。

### `void QTextTableFormat::setCellPadding(qreal padding)`

**作用与语义：**

为表设置单元格`padding`。这决定了单元格边界与其内容物之间的距离。

### `void QTextTableFormat::setCellSpacing(qreal spacing)`

**作用与语义：**

为表格设置单元格`spacing`。这决定了相邻单元之间的距离。
如果启用了`borderCollapse`，该属性将被忽略。

### `void QTextTableFormat::setColumnWidthConstraints(const QList<QTextLength> &constraints)`

**作用与语义：**

设置表格的列宽`constraints`。

### `void QTextTableFormat::setHeaderRowCount(int count)`

**作用与语义：**

将表的前`count`行声明为表头。当表被切开跨越页面边界时，表头的行会重复出现。

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

`QTextTableFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
