# QTextFrameFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextFrameFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextFrameFormat>`
- 继承自：QTextFormat
- 直接派生类：QTextTableFormat

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

- `enum BorderStyle { BorderStyle_None, BorderStyle_Dotted, BorderStyle_Dashed, BorderStyle_Solid, BorderStyle_Double, …, BorderStyle_Outset }`
- `enum Position { InFlow, FloatLeft, FloatRight }`

### 公有函数

- `QTextFrameFormat()`
- `qreal border() const`
- `QBrush borderBrush() const`
- `QTextFrameFormat::BorderStyle borderStyle() const`
- `qreal bottomMargin() const`
- `QTextLength height() const`
- `bool isValid() const`
- `qreal leftMargin() const`
- `qreal margin() const`
- `qreal padding() const`
- `QTextFormat::PageBreakFlags pageBreakPolicy() const`
- `QTextFrameFormat::Position position() const`
- `qreal rightMargin() const`
- `void setBorder(qreal width)`
- `void setBorderBrush(const QBrush &brush)`
- `void setBorderStyle(QTextFrameFormat::BorderStyle style)`
- `void setBottomMargin(qreal margin)`
- `void setHeight(const QTextLength &height)`
- `void setHeight(qreal height)`
- `void setLeftMargin(qreal margin)`
- `void setMargin(qreal margin)`
- `void setPadding(qreal width)`
- `void setPageBreakPolicy(QTextFormat::PageBreakFlags policy)`
- `void setPosition(QTextFrameFormat::Position policy)`
- `void setRightMargin(qreal margin)`
- `void setTopMargin(qreal margin)`
- `void setWidth(const QTextLength &width)`
- `void setWidth(qreal width)`
- `qreal topMargin() const`
- `QTextLength width() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextFrameFormat::BorderStyle`

**作用与语义：**

该枚举描述了文本框架的不同边框样式。
- `QTextFrameFormat::BorderStyle_None`：`0`
- `QTextFrameFormat::BorderStyle_Dotted`：`1`
- `QTextFrameFormat::BorderStyle_Dashed`：`2`
- `QTextFrameFormat::BorderStyle_Solid`：`3`
- `QTextFrameFormat::BorderStyle_Double`：`4`
- `QTextFrameFormat::BorderStyle_DotDash`：`5`
- `QTextFrameFormat::BorderStyle_DotDotDash`：`6`
- `QTextFrameFormat::BorderStyle_Groove`：`7`
- `QTextFrameFormat::BorderStyle_Ridge`：`8`
- `QTextFrameFormat::BorderStyle_Inset`：`9`
- `QTextFrameFormat::BorderStyle_Outset`：`10`

### `enum QTextFrameFormat::Position`

**作用与语义：**

该枚举描述了框架相对于周围文本的位置。
- `QTextFrameFormat::InFlow`：`0`
- `QTextFrameFormat::FloatLeft`：`1`
- `QTextFrameFormat::FloatRight`：`2`

### `QTextFrameFormat::QTextFrameFormat()`

**作用与语义：**

构建带有默认属性的文本框架格式对象。

### `qreal QTextFrameFormat::border() const`

**作用与语义：**

返回边框宽度（像素单位）。

### `QBrush QTextFrameFormat::borderBrush() const`

**作用与语义：**

退还用于画框边框的画笔。

### `QTextFrameFormat::BorderStyle QTextFrameFormat::borderStyle() const`

**作用与语义：**

恢复了框架边框的样式。

### `qreal QTextFrameFormat::bottomMargin() const`

**作用与语义：**

返回画面底部边界的宽度（像素单位）。

### `QTextLength QTextFrameFormat::height() const`

**作用与语义：**

返回帧边框矩形的高度。

### `bool QTextFrameFormat::isValid() const`

**作用与语义：**

如果格式描述有效，返回`true`;否则返回`false`。

### `qreal QTextFrameFormat::leftMargin() const`

**作用与语义：**

返回画面左侧边界的宽度（像素单位）。

### `qreal QTextFrameFormat::margin() const`

**作用与语义：**

返回画面外部边界的宽度（像素单位）。

### `qreal QTextFrameFormat::padding() const`

**作用与语义：**

返回帧内部填充的像素宽度。

### `QTextFormat::PageBreakFlags QTextFrameFormat::pageBreakPolicy() const`

**作用与语义：**

返回当前设置的分页策略。默认是`QTextFormat::PageBreak_Auto`。

### `QTextFrameFormat::Position QTextFrameFormat::position() const`

**作用与语义：**

返回采用该帧格式的帧的定位策略。

### `qreal QTextFrameFormat::rightMargin() const`

**作用与语义：**

返回画面右边距的宽度（像素单位）。

### `void QTextFrameFormat::setBorder(qreal width)`

**作用与语义：**

设置帧边界的像素`width`。

### `void QTextFrameFormat::setBorderBrush(const QBrush &brush)`

**作用与语义：**

设置框架边框所用的`brush`。

### `void QTextFrameFormat::setBorderStyle(QTextFrameFormat::BorderStyle style)`

**作用与语义：**

设定画面边界的边界`style`。

### `void QTextFrameFormat::setBottomMargin(qreal margin)`

**作用与语义：**

将画面底部`margin`以像素单位设定。

### `void QTextFrameFormat::setHeight(const QTextLength &height)`

**作用与语义：**

设定了框架的 `height`。

### `void QTextFrameFormat::setHeight(qreal height)`

**作用与语义：**

设定了框架的 `height`。

### `void QTextFrameFormat::setLeftMargin(qreal margin)`

**作用与语义：**

它会将帧的左侧`margin`以像素单位设置。

### `void QTextFrameFormat::setMargin(qreal margin)`

**作用与语义：**

设置帧的像素数`margin`。该方法还将帧的左、右、上、下边距设置为相同值。单个边距覆盖一般边距。

### `void QTextFrameFormat::setPadding(qreal width)`

**作用与语义：**

以像素为单位设定帧内部填充的`width`。

### `void QTextFrameFormat::setPageBreakPolicy(QTextFormat::PageBreakFlags policy)`

**作用与语义：**

将帧/表格的分页策略设置为`policy`。

### `void QTextFrameFormat::setPosition(QTextFrameFormat::Position policy)`

**作用与语义：**

用这种帧格式设置帧定位的 `policy`。

### `void QTextFrameFormat::setRightMargin(qreal margin)`

**作用与语义：**

它能将画面的右侧正值设定在像素`margin`。

### `void QTextFrameFormat::setTopMargin(qreal margin)`

**作用与语义：**

将画面顶部`margin`设为像素。

### `void QTextFrameFormat::setWidth(const QTextLength &width)`

**作用与语义：**

设置框架边界矩形的`width`。

### `void QTextFrameFormat::setWidth(qreal width)`

**作用与语义：**

方便方法，将帧边框矩形宽度设置为指定的固定`width`。

### `qreal QTextFrameFormat::topMargin() const`

**作用与语义：**

返回画面顶部边缘的宽度（像素单位）。

### `QTextLength QTextFrameFormat::width() const`

**作用与语义：**

返回帧边框矩形的宽度。

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

`QTextFrameFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
