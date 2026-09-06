# QTextTableCellFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextTableCellFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextTableCellFormat>`
- 继承自：QTextCharFormat
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

- `QTextTableCellFormat()`
- `qreal bottomBorder() const`
- `QBrush bottomBorderBrush() const`
- `QTextFrameFormat::BorderStyle bottomBorderStyle() const`
- `qreal bottomPadding() const`
- `bool isValid() const`
- `qreal leftBorder() const`
- `QBrush leftBorderBrush() const`
- `QTextFrameFormat::BorderStyle leftBorderStyle() const`
- `qreal leftPadding() const`
- `qreal rightBorder() const`
- `QBrush rightBorderBrush() const`
- `QTextFrameFormat::BorderStyle rightBorderStyle() const`
- `qreal rightPadding() const`
- `void setBorder(qreal width)`
- `void setBorderBrush(const QBrush &brush)`
- `void setBorderStyle(QTextFrameFormat::BorderStyle style)`
- `void setBottomBorder(qreal width)`
- `void setBottomBorderBrush(const QBrush &brush)`
- `void setBottomBorderStyle(QTextFrameFormat::BorderStyle style)`
- `void setBottomPadding(qreal padding)`
- `void setLeftBorder(qreal width)`
- `void setLeftBorderBrush(const QBrush &brush)`
- `void setLeftBorderStyle(QTextFrameFormat::BorderStyle style)`
- `void setLeftPadding(qreal padding)`
- `void setPadding(qreal padding)`
- `void setRightBorder(qreal width)`
- `void setRightBorderBrush(const QBrush &brush)`
- `void setRightBorderStyle(QTextFrameFormat::BorderStyle style)`
- `void setRightPadding(qreal padding)`
- `void setTopBorder(qreal width)`
- `void setTopBorderBrush(const QBrush &brush)`
- `void setTopBorderStyle(QTextFrameFormat::BorderStyle style)`
- `void setTopPadding(qreal padding)`
- `qreal topBorder() const`
- `QBrush topBorderBrush() const`
- `QTextFrameFormat::BorderStyle topBorderStyle() const`
- `qreal topPadding() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTextTableCellFormat::QTextTableCellFormat()`

**作用与语义：**

构建一个新的表单元格格式对象。

### `qreal QTextTableCellFormat::bottomBorder() const`

**作用与语义：**

返回表单元格的底部边界宽度。

### `QBrush QTextTableCellFormat::bottomBorderBrush() const`

**作用与语义：**

返回表格单元底部边框刷。

### `QTextFrameFormat::BorderStyle QTextTableCellFormat::bottomBorderStyle() const`

**作用与语义：**

返回表单元格的底部边框样式。

### `qreal QTextTableCellFormat::bottomPadding() const`

**作用与语义：**

它得到了桌面单元的底部填充物。

### `bool QTextTableCellFormat::isValid() const`

**作用与语义：**

如果此表格单元格格式有效，则返回 `true`；否则返回 `false`。

### `qreal QTextTableCellFormat::leftBorder() const`

**作用与语义：**

返回表单元格的左边边界宽度。

### `QBrush QTextTableCellFormat::leftBorderBrush() const`

**作用与语义：**

返回表单元格的左边边框刷。

### `QTextFrameFormat::BorderStyle QTextTableCellFormat::leftBorderStyle() const`

**作用与语义：**

返回表单元格的左边边界样式。

### `qreal QTextTableCellFormat::leftPadding() const`

**作用与语义：**

获得表格单元的左侧填充。

### `qreal QTextTableCellFormat::rightBorder() const`

**作用与语义：**

返回表单元格的右边边界宽度。

### `QBrush QTextTableCellFormat::rightBorderBrush() const`

**作用与语义：**

返回表单元的右边边框刷。

### `QTextFrameFormat::BorderStyle QTextTableCellFormat::rightBorderStyle() const`

**作用与语义：**

返回表单元格的右边框样式。

### `qreal QTextTableCellFormat::rightPadding() const`

**作用与语义：**

能获得正确的桌格缓冲。

### `void QTextTableCellFormat::setBorder(qreal width)`

**作用与语义：**

设置表格单元格的左、右、上、下边界`width`。

### `void QTextTableCellFormat::setBorderBrush(const QBrush &brush)`

**作用与语义：**

设置表格单元格的左、右、上、下边界`brush`。

### `void QTextTableCellFormat::setBorderStyle(QTextFrameFormat::BorderStyle style)`

**作用与语义：**

设置表格单元格的左、右、上、下边界`style`。

### `void QTextTableCellFormat::setBottomBorder(qreal width)`

**作用与语义：**

设置表格单元格`width`底部边界。

### `void QTextTableCellFormat::setBottomBorderBrush(const QBrush &brush)`

**作用与语义：**

设置表格单元格的底部边界`brush`。

### `void QTextTableCellFormat::setBottomBorderStyle(QTextFrameFormat::BorderStyle style)`

**作用与语义：**

将表格单元格的底部边界设置`style`。

### `void QTextTableCellFormat::setBottomPadding(qreal padding)`

**作用与语义：**

设置表格单元的底部 `padding`。

### `void QTextTableCellFormat::setLeftBorder(qreal width)`

**作用与语义：**

设置表格单元格`width`左边边界。

### `void QTextTableCellFormat::setLeftBorderBrush(const QBrush &brush)`

**作用与语义：**

设置表格单元格`brush`左边边界。

### `void QTextTableCellFormat::setLeftBorderStyle(QTextFrameFormat::BorderStyle style)`

**作用与语义：**

设置表单元格`style`左边边界。

### `void QTextTableCellFormat::setLeftPadding(qreal padding)`

**作用与语义：**

设置表格单元的左侧`padding`。

### `void QTextTableCellFormat::setPadding(qreal padding)`

**作用与语义：**

设置表格单元的左、右、上、下四`padding`。

### `void QTextTableCellFormat::setRightBorder(qreal width)`

**作用与语义：**

设置表单元格`width`右边边界。

### `void QTextTableCellFormat::setRightBorderBrush(const QBrush &brush)`

**作用与语义：**

设置表单元格`brush`右边边界。

### `void QTextTableCellFormat::setRightBorderStyle(QTextFrameFormat::BorderStyle style)`

**作用与语义：**

设置表单元格`style`右边边界。

### `void QTextTableCellFormat::setRightPadding(qreal padding)`

**作用与语义：**

设置表单元的右侧`padding`。

### `void QTextTableCellFormat::setTopBorder(qreal width)`

**作用与语义：**

设置表格单元格`width`顶部边界。

### `void QTextTableCellFormat::setTopBorderBrush(const QBrush &brush)`

**作用与语义：**

设置表格单元格的顶部边界`brush`。

### `void QTextTableCellFormat::setTopBorderStyle(QTextFrameFormat::BorderStyle style)`

**作用与语义：**

设置表格单元格`style`顶部边界。

### `void QTextTableCellFormat::setTopPadding(qreal padding)`

**作用与语义：**

设置桌面单元格的顶部 `padding`。

### `qreal QTextTableCellFormat::topBorder() const`

**作用与语义：**

返回表单元格的顶部边框宽度。

### `QBrush QTextTableCellFormat::topBorderBrush() const`

**作用与语义：**

返回表格单元的顶部边框刷。

### `QTextFrameFormat::BorderStyle QTextTableCellFormat::topBorderStyle() const`

**作用与语义：**

返回表格单元的顶部边框样式。

### `qreal QTextTableCellFormat::topPadding() const`

**作用与语义：**

它得到了桌面单元的顶部填充物。

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

`QTextTableCellFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
