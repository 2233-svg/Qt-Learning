# QTextBlockFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextBlockFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextBlockFormat>`
- 继承自：QTextFormat
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

- `enum LineHeightTypes { SingleHeight, ProportionalHeight, FixedHeight, MinimumHeight, LineDistanceHeight }`
- `enum class MarkerType { NoMarker, Unchecked, Checked }`

### 公有函数

- `QTextBlockFormat()`
- `Qt::Alignment alignment() const`
- `qreal bottomMargin() const`
- `int headingLevel() const`
- `int indent() const`
- `bool isValid() const`
- `qreal leftMargin() const`
- `qreal lineHeight() const`
- `qreal lineHeight(qreal scriptLineHeight, qreal scaling = 1.0) const`
- `int lineHeightType() const`
- `QTextBlockFormat::MarkerType marker() const`
- `bool nonBreakableLines() const`
- `QTextFormat::PageBreakFlags pageBreakPolicy() const`
- `qreal rightMargin() const`
- `void setAlignment(Qt::Alignment alignment)`
- `void setBottomMargin(qreal margin)`
- `void setHeadingLevel(int level)`
- `void setIndent(int indentation)`
- `void setLeftMargin(qreal margin)`
- `void setLineHeight(qreal height, int heightType)`
- `void setMarker(QTextBlockFormat::MarkerType marker)`
- `void setNonBreakableLines(bool b)`
- `void setPageBreakPolicy(QTextFormat::PageBreakFlags policy)`
- `void setRightMargin(qreal margin)`
- `void setTabPositions(const QList<QTextOption::Tab> &tabs)`
- `void setTextIndent(qreal indent)`
- `void setTopMargin(qreal margin)`
- `QList<QTextOption::Tab> tabPositions() const`
- `qreal textIndent() const`
- `qreal topMargin() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextBlockFormat::LineHeightTypes`

**作用与语义：**

这个列举描述了支持段落可以拥有的各种行距类型。
- `QTextBlockFormat::SingleHeight`：`0`;这是默认的行高：单行间距。
- `QTextBlockFormat::ProportionalHeight`：`1`;此方法将间距与行数成比例（百分比）。例如，双倍间距设为200。
- `QTextBlockFormat::FixedHeight`：`2`;将线高设置为固定的线高（以像素为单位）。
- `QTextBlockFormat::MinimumHeight`：`3`;这设定了最小线高度（像素数）。
- `QTextBlockFormat::LineDistanceHeight`：`4`;这会将线之间的高度（像素单位）相加。

### `enum class QTextBlockFormat::MarkerType`

**作用与语义：**

该枚举描述了列表项可以拥有的标记类型。如果某个列表项（`QTextBlock::textList()`返回列表的段落）有标记，则用它来替代普通的项目符号。这样，可检查的列表项可以在同一列表中与普通列表项混合使用，覆盖`QTextListFormat::style()`为整个列表指定的项目符号类型。
- `QTextBlockFormat::MarkerType::NoMarker`：`0`;这是默认设置：列表项目的要点会显示。
- `QTextBlockFormat::MarkerType::Unchecked`：`1`;列表项目的项目符号将显示一个未勾选的复选框。
- `QTextBlockFormat::MarkerType::Checked`：`2`;列表中的项目符号不是项目符号，而是显示勾选的复选框。
未来，这一定义可能会扩展到其他类型的段落装饰。

### `QTextBlockFormat::QTextBlockFormat()`

**作用与语义：**

构建一个新的QTextBlockFormat。

### `Qt::Alignment QTextBlockFormat::alignment() const`

**作用与语义：**

返回段落的对齐。

### `qreal QTextBlockFormat::bottomMargin() const`

**作用与语义：**

返回段落的下页距。

### `int QTextBlockFormat::headingLevel() const`

**作用与语义：**

如果段落有标题，则返回标题级别，若不是，则返回0。

### `int QTextBlockFormat::indent() const`

**作用与语义：**

返回段落的缩进。

### `bool QTextBlockFormat::isValid() const`

**作用与语义：**

如果该分组格式有效，返回`true`;否则返回false。

### `qreal QTextBlockFormat::leftMargin() const`

**作用与语义：**

返回段落的左边距。

### `qreal QTextBlockFormat::lineHeight() const`

**作用与语义：**

这会返回该段落的 LineHeight 属性。

### `qreal QTextBlockFormat::lineHeight(qreal scriptLineHeight, qreal scaling = 1.0) const`

**作用与语义：**

返回段落中行的高度，基于由`scriptLineHeight`给出的文字行高度和指定的`scaling`因子。
返回的值还取决于段落的给定 LineHeightType 以及该段落设置的 LineHeight。
对于包含固定像素数量的高度，需要缩放以适配打印。

### `int QTextBlockFormat::lineHeightType() const`

**作用与语义：**

这会返回段落的 LineHeightType 属性。

### `QTextBlockFormat::MarkerType QTextBlockFormat::marker() const`

**作用与语义：**

如果已设置，返回段落标记，未设置则返回`NoMarker`。

### `bool QTextBlockFormat::nonBreakableLines() const`

**作用与语义：**

如果段落中的行不可断开，返回`true`;否则返回`false`。

### `QTextFormat::PageBreakFlags QTextBlockFormat::pageBreakPolicy() const`

**作用与语义：**

返回当前段落的分页策略。默认是`QTextFormat::PageBreak_Auto`。

### `qreal QTextBlockFormat::rightMargin() const`

**作用与语义：**

返回段落右边框。

### `void QTextBlockFormat::setAlignment(Qt::Alignment alignment)`

**作用与语义：**

为段落设定了整体的 `alignment`。

### `void QTextBlockFormat::setBottomMargin(qreal margin)`

**作用与语义：**

设定段落底部`margin`。

### `void QTextBlockFormat::setHeadingLevel(int level)`

**作用与语义：**

设置段落标题`level`，其中1是最高级别的标题类型（通常标题字体大小最大），递增的值则在文档中逐渐更深处（通常字体大小较小）。例如，阅读HTML的H1标签时，标题级别设置为1。设置标题级别不会自动改变字体大小;但`QTextDocumentFragment::fromHtml()`会同时设置标题级别和字体大小。
如果段落不是标题，则应将等级设置为0（默认值）。

### `void QTextBlockFormat::setIndent(int indentation)`

**作用与语义：**

设置段落的 `indentation`。边距与缩进独立设置，`setLeftMargin()` 和 `setTextIndent()`。`indentation` 是一个整数，乘以文档标准缩进，最终得到段落的实际缩进。

### `void QTextBlockFormat::setLeftMargin(qreal margin)`

**作用与语义：**

设置段落的左侧`margin`。缩进可以单独应用，`setIndent()`。

### `void QTextBlockFormat::setLineHeight(qreal height, int heightType)`

**作用与语义：**

将段落的行高设置为`height`的值，该值依赖于`LineHeightTypes`枚举描述的`heightType`。

### `void QTextBlockFormat::setMarker(QTextBlockFormat::MarkerType marker)`

**作用与语义：**

将应与段落一同渲染的装饰类型设置为`marker`。例如，列表项目可以用复选框装饰，勾选或取消勾选，作为其项目符号的替代。默认是`NoMarker`。

### `void QTextBlockFormat::setNonBreakableLines(bool b)`

**作用与语义：**

如果`b`为真，段落中的行被视为不可断开;否则它们是可断开的。

### `void QTextBlockFormat::setPageBreakPolicy(QTextFormat::PageBreakFlags policy)`

**作用与语义：**

将段落的分页规则设定为`policy`。

### `void QTextBlockFormat::setRightMargin(qreal margin)`

**作用与语义：**

这会让段落的正`margin`。

### `void QTextBlockFormat::setTabPositions(const QList<QTextOption::Tab> &tabs)`

**作用与语义：**

将文本块的制表符位置设置为`tabs`指定的位置。

### `void QTextBlockFormat::setTextIndent(qreal indent)`

**作用与语义：**

为该块的第一行设置`indent`。这使得段落的第一行可以与其他行不同地缩进，从而提升文本的可读性。

### `void QTextBlockFormat::setTopMargin(qreal margin)`

**作用与语义：**

设定段落的顶部`margin`。

### `QList<QTextOption::Tab> QTextBlockFormat::tabPositions() const`

**作用与语义：**

返回文本块定义的制表符位置列表。

### `qreal QTextBlockFormat::textIndent() const`

**作用与语义：**

返回段落的文本缩进。

### `qreal QTextBlockFormat::topMargin() const`

**作用与语义：**

返回段落的顶部边距。

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

`QTextBlockFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
