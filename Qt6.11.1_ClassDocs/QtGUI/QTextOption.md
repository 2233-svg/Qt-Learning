# QTextOption

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QTextOption` 是 Qt 的值类型，围绕“文本Option”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextOption` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QTextOption>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct Tab`
- `enum Flag { IncludeTrailingSpaces, ShowTabsAndSpaces, ShowLineAndParagraphSeparators, ShowDocumentTerminator, ShowDefaultIgnorables, …, DisableEmojiParsing }`
- `flags Flags`
- `enum TabType { LeftTab, RightTab, CenterTab, DelimiterTab }`
- `enum WrapMode { NoWrap, WordWrap, ManualWrap, WrapAnywhere, WrapAtWordBoundaryOrAnywhere }`

### 公有函数

- `QTextOption()`
- `QTextOption(Qt::Alignment alignment)`
- `QTextOption(const QTextOption &other)`
- `~QTextOption()`
- `Qt::Alignment alignment() const`
- `QTextOption::Flags flags() const`
- `void setAlignment(Qt::Alignment alignment)`
- `void setFlags(QTextOption::Flags flags)`
- `void setTabArray(const QList<qreal> &tabStops)`
- `void setTabStopDistance(qreal tabStopDistance)`
- `void setTabs(const QList<QTextOption::Tab> &tabStops)`
- `void setTextDirection(Qt::LayoutDirection direction)`
- `void setUseDesignMetrics(bool enable)`
- `void setWrapMode(QTextOption::WrapMode mode)`
- `QList<qreal> tabArray() const`
- `qreal tabStopDistance() const`
- `QList<QTextOption::Tab> tabs() const`
- `Qt::LayoutDirection textDirection() const`
- `bool useDesignMetrics() const`
- `QTextOption::WrapMode wrapMode() const`
- `QTextOption & operator=(const QTextOption &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextOption::Flagflags QTextOption::Flags`

**作用与语义：**

- `QTextOption::IncludeTrailingSpaces`：`0x80000000`;当设置此选项时，`QTextLine::naturalTextWidth()` 和 naturalTextRect() 会返回包含文本尾部空格宽度的值;否则该宽度被排除。
- `QTextOption::ShowTabsAndSpaces`：`0x1`;用小点和带小箭头的标签符号来可视化。非断行空格的显示方式与切断空格不同。
- `QTextOption::ShowLineAndParagraphSeparators`：`0x2`;用适当的符号字符可视化行分隔符和段落分隔符。
- `QTextOption::ShowDocumentTerminator (since Qt 5.7)`：`0x10`;用章节符号可视化文档的结尾。
- `QTextOption::ShowDefaultIgnorables (since Qt 6.9)`：`0x20`;如果字体支持，则渲染通常非视觉字符。
- `QTextOption::AddSpaceForLineAndParagraphSeparators`：`0x4`;确定换行位置时，要考虑绘制分隔符字符时增加的空间。
- `QTextOption::SuppressColors`：`0x8`;抑制字符格式中的所有颜色变化（主选择除外）。
- `QTextOption::DisableEmojiParsing (since Qt 6.9)`：`0x40`;默认情况下，Qt 会检测输入字符串中的表情符号序列，并优先使用彩色字体来显示。如果事先知道不需要 DisableEmojiParsing 标志，可以通过设置 DisableEmojiParsing 来禁用此额外步骤。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QTextOption::TabType`

**作用与语义：**

该枚举包含不同类型的计表器。
- `QTextOption::LeftTab`：`0`;左边的标签
- `QTextOption::RightTab`：`1`;右指
- `QTextOption::CenterTab`：`2`;居中标签
- `QTextOption::DelimiterTab`：`3`;在某个分隔符处停止的制表符

### `enum QTextOption::WrapMode`

**作用与语义：**

该枚举描述了文本在文档中的包装方式。
- `QTextOption::NoWrap`：`0`;文本完全没有被包裹。
- `QTextOption::WordWrap`：`1`;文本在单词边界处被包裹。
- `QTextOption::ManualWrap`：`2`;与QTextOption：：NoWrap相同
- `QTextOption::WrapAnywhere`：`3`;文本可以在行中任意点被包裹，即使它出现在单词中间。
- `QTextOption::WrapAtWordBoundaryOrAnywhere`：`4`;如果可能，包裹发生在单词边界处;否则包裹会在行中适当位置发生，甚至在单词中间。

### `QTextOption::QTextOption()`

**作用与语义：**

构建带有文本默认属性的文本选项。文本对齐属性设置为`Qt::AlignLeft`。单词换行属性设置为`QTextOption::WordWrap`。设计指标的使用标志设置为false。

### `QTextOption::QTextOption(Qt::Alignment alignment)`

**作用与语义：**

用给定的文本`alignment`构造文本选项。单词包裹属性设置为`QTextOption::WordWrap`。设计指标的使用标记设置为false。

### `QTextOption::QTextOption(const QTextOption &other)`

**作用与语义：**

制作一份`other`文本选项的副本。

### `[noexcept] QTextOption::~QTextOption()`

**作用与语义：**

这会破坏文本选项。

### `Qt::Alignment QTextOption::alignment() const`

**作用与语义：**

返回由选项定义的文本对齐。

### `QTextOption::Flags QTextOption::flags() const`

**作用与语义：**

返回与该选项相关的标志。

### `void QTextOption::setAlignment(Qt::Alignment alignment)`

**作用与语义：**

将选项的文本对齐设置为指定的 `alignment`。

### `void QTextOption::setFlags(QTextOption::Flags flags)`

**作用与语义：**

将与该选项关联到给定`flags`的标志。

### `void QTextOption::setTabArray(const QList<qreal> &tabStops)`

**作用与语义：**

将文本布局的制表符位置设置为`tabStops`指定的位置。

### `void QTextOption::setTabStopDistance(qreal tabStopDistance)`

**作用与语义：**

将制表止音之间的默认距离设置为`tabStopDistance`指定的值。

### `void QTextOption::setTabs(const QList<QTextOption::Tab> &tabStops)`

**作用与语义：**

将文本布局的制表符位置设置为`tabStops`指定的位置。

### `void QTextOption::setTextDirection(Qt::LayoutDirection direction)`

**作用与语义：**

将由该选项定义的文本布局方向设定到给定`direction`。

### `void QTextOption::setUseDesignMetrics(bool enable)`

**作用与语义：**

如果`enable`成立，布局将使用设计指标;否则将使用绘图设备的指标（这是默认行为）。

### `void QTextOption::setWrapMode(QTextOption::WrapMode mode)`

**作用与语义：**

将选项的文本换行模式设置为给定的 `mode`。

### `QList<qreal> QTextOption::tabArray() const`

**作用与语义：**

返回文本布局定义的制表表位置列表。

### `qreal QTextOption::tabStopDistance() const`

**作用与语义：**

返回制表停止点之间的设备单位距离。

### `QList<QTextOption::Tab> QTextOption::tabs() const`

**作用与语义：**

返回文本布局定义的制表表位置列表。

### `Qt::LayoutDirection QTextOption::textDirection() const`

**作用与语义：**

返回由选项定义的文本布局方向。

### `bool QTextOption::useDesignMetrics() const`

**作用与语义：**

如果布局使用设计而非设备度量，返回`true`;否则返回`false`。

### `QTextOption::WrapMode QTextOption::wrapMode() const`

**作用与语义：**

返回由选项定义的文本换行模式。

### `QTextOption &QTextOption::operator=(const QTextOption &other)`

**作用与语义：**

如果文本选项与`other`文本选项相同，返回`true`;否则返回`false`。

### `struct Tab`

**作用与语义：**

每个标签定义都用这个结构体表示。

### `enum Flag { IncludeTrailingSpaces, ShowTabsAndSpaces, ShowLineAndParagraphSeparators, ShowDocumentTerminator, ShowDefaultIgnorables, …, DisableEmojiParsing }`

**作用与语义：**

- `QTextOption::IncludeTrailingSpaces`：`0x80000000`;当设置此选项时，`QTextLine::naturalTextWidth()` 和 naturalTextRect() 会返回包含文本尾部空格宽度的值;否则该宽度被排除。
- `QTextOption::ShowTabsAndSpaces`：`0x1`;用小点和带小箭头的标签符号来可视化。非断行空格的显示方式与切断空格不同。
- `QTextOption::ShowLineAndParagraphSeparators`：`0x2`;用适当的符号字符可视化行分隔符和段落分隔符。
- `QTextOption::ShowDocumentTerminator (since Qt 5.7)`：`0x10`;用章节符号可视化文档的结尾。
- `QTextOption::ShowDefaultIgnorables (since Qt 6.9)`：`0x20`;如果字体支持，则渲染通常非视觉字符。
- `QTextOption::AddSpaceForLineAndParagraphSeparators`：`0x4`;确定换行位置时，要考虑绘制分隔符字符时增加的空间。
- `QTextOption::SuppressColors`：`0x8`;抑制字符格式中的所有颜色变化（主选择除外）。
- `QTextOption::DisableEmojiParsing (since Qt 6.9)`：`0x40`;默认情况下，Qt 会检测输入字符串中的表情符号序列，并优先使用彩色字体来显示。如果事先知道不需要 DisableEmojiParsing 标志，可以通过设置 DisableEmojiParsing 来禁用此额外步骤。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

- `QTextOption::IncludeTrailingSpaces`：`0x80000000`;当设置此选项时，`QTextLine::naturalTextWidth()` 和 naturalTextRect() 会返回包含文本尾部空格宽度的值;否则该宽度被排除。
- `QTextOption::ShowTabsAndSpaces`：`0x1`;用小点和带小箭头的标签符号来可视化。非断行空格的显示方式与切断空格不同。
- `QTextOption::ShowLineAndParagraphSeparators`：`0x2`;用适当的符号字符可视化行分隔符和段落分隔符。
- `QTextOption::ShowDocumentTerminator (since Qt 5.7)`：`0x10`;用章节符号可视化文档的结尾。
- `QTextOption::ShowDefaultIgnorables (since Qt 6.9)`：`0x20`;如果字体支持，则渲染通常非视觉字符。
- `QTextOption::AddSpaceForLineAndParagraphSeparators`：`0x4`;确定换行位置时，要考虑绘制分隔符字符时增加的空间。
- `QTextOption::SuppressColors`：`0x8`;抑制字符格式中的所有颜色变化（主选择除外）。
- `QTextOption::DisableEmojiParsing (since Qt 6.9)`：`0x40`;默认情况下，Qt 会检测输入字符串中的表情符号序列，并优先使用彩色字体来显示。如果事先知道不需要 DisableEmojiParsing 标志，可以通过设置 DisableEmojiParsing 来禁用此额外步骤。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTextOption` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
