# QFontInfo

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QFontInfo` 是 Qt 的值类型，围绕“字体Info”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QFontInfo` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QFontInfo>`
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

### 公有函数

- `QFontInfo(const QFont &font)`
- `QFontInfo(const QFontInfo &fi)`
- `~QFontInfo()`
- `bool bold() const`
- `bool exactMatch() const`
- `QString family() const`
- `bool fixedPitch() const`
- `bool italic() const`
- `int pixelSize() const`
- `int pointSize() const`
- `qreal pointSizeF() const`
- `QFont::Style style() const`
- `QFont::StyleHint styleHint() const`
- `QString styleName() const`
- `void swap(QFontInfo &other)`
- `(since 6.9) QList<QFontVariableAxis> variableAxes() const`
- `int weight() const`
- `QFontInfo & operator=(const QFontInfo &fi)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QFontInfo::QFontInfo(const QFont &font)`

**作用与语义：**

为`font`构建一个字体信息对象。
字体必须兼容屏幕，即你在`widgets`或`pixmaps`中绘制文字时使用的字体，而非`QPicture`或`QPrinter`。
font info 对象保存在构建函数中传递的字体信息，如果字体属性后来被更改，则不会更新。
在绘制时使用`QPainter::fontInfo()`获取字体信息。这样在不兼容屏幕的绘画设备上绘制时也能获得正确的结果。

### `QFontInfo::QFontInfo(const QFontInfo &fi)`

**作用与语义：**

构建了一份`fi`的复制品。

### `[noexcept] QFontInfo::~QFontInfo()`

**作用与语义：**

它会破坏字体信息对象。

### `bool QFontInfo::bold() const`

**作用与语义：**

如果`weight()`返回的值大于`QFont::Normal`，则返回`true`;否则返回`false`。

### `bool QFontInfo::exactMatch() const`

**作用与语义：**

如果匹配的窗口系统字体与字体指定的字体完全相同，返回`true`;否则返回`false`。

### `QString QFontInfo::family() const`

**作用与语义：**

返回匹配窗口系统字体的族名。

### `bool QFontInfo::fixedPitch() const`

**作用与语义：**

返回匹配窗口系统字体的固定音高值。

### `bool QFontInfo::italic() const`

**作用与语义：**

返回匹配窗口系统字体的斜体值。

### `int QFontInfo::pixelSize() const`

**作用与语义：**

返回匹配窗口系统字体的像素大小。

### `int QFontInfo::pointSize() const`

**作用与语义：**

返回匹配窗口系统字体的点大小。

### `qreal QFontInfo::pointSizeF() const`

**作用与语义：**

返回匹配窗口系统字体的点大小。

### `QFont::Style QFontInfo::style() const`

**作用与语义：**

返回匹配窗口系统字体的样式值。

### `QFont::StyleHint QFontInfo::styleHint() const`

**作用与语义：**

返回匹配窗口系统字体的样式。
目前只返回`QFont`的风格提示。

### `QString QFontInfo::styleName() const`

**作用与语义：**

在支持该格式的系统上返回匹配窗口系统字体的样式名称。

### `[noexcept] void QFontInfo::swap(QFontInfo &other)`

**作用与语义：**

将这个字体信息实例与 `other` 交换。这个操作非常快，而且从未失败过。

### `[since 6.9] QList<QFontVariableAxis> QFontInfo::variableAxes() const`

**作用与语义：**

如果字体是可变字体，该函数会返回该字体支持的轴列表。
关于变轴的更多细节，请参见`setVariableAxis()`。

### `int QFontInfo::weight() const`

**作用与语义：**

返回匹配窗口系统字体的权重。

### `QFontInfo &QFontInfo::operator=(const QFontInfo &fi)`

**作用与语义：**

`fi`中分配字体信息。

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

`QFontInfo` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
