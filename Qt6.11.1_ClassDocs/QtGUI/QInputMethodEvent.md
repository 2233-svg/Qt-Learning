# QInputMethodEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QInputMethodEvent` 是 Qt 的值类型，围绕“输入Method事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QInputMethodEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QInputMethodEvent>`
- 继承自：QEvent
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class Attribute`
- `enum AttributeType { TextFormat, Cursor, Language, Ruby, Selection, MimeData }`

### 公有函数

- `QInputMethodEvent()`
- `QInputMethodEvent(const QString &preeditText, const QList<QInputMethodEvent::Attribute> &attributes)`
- `const QList<QInputMethodEvent::Attribute> & attributes() const`
- `const QString & commitString() const`
- `const QString & preeditString() const`
- `int replacementLength() const`
- `int replacementStart() const`
- `void setCommitString(const QString &commitString, int replaceFrom = 0, int replaceLength = 0)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QInputMethodEvent::AttributeType`

**作用与语义：**

- `QInputMethodEvent::TextFormat`：`0`;预编辑字符串中由起始和长度指定的部分的`QTextCharFormat`。值包含一个类型为`QTextFormat`的`QVariant`，指定该部分的渲染。预编辑字符串的每个部分最多应有一种格式。如果字符串中任一字符指定多个格式，则行为未定义。符合规范的实现至少应尊重格式的背景色、文本色和fontUnderline属性。
- `QInputMethodEvent::Cursor`：`1`;如果设置，预编辑字符串中应显示一个光标，位置起始位置。长度变量决定光标是否可见。长度为0时光标不可见。如果值为`QColor`类型的`QVariant`，则该颜色用于渲染光标，否则使用周围文本的颜色。每个事件最多应有一个光标属性。如果指定多个，则行为未定义。
- `QInputMethodEvent::Language`：`2`;该变体包含一个`QLocale`对象，指定预编辑字符串某部分的语言。预编辑字符串的每个部分最多应设置一种语言。如果字符串中任一字符指定多个语言，则行为未定义。
- `QInputMethodEvent::Ruby`：`3`;预编辑字符串部分的 Ruby 文本。预编辑字符串的每个部分最多应设置一个 Ruby 文本。如果字符串中任一字符指定多个 Ruby 文本，则行为未定义。
- `QInputMethodEvent::Selection`：`4`;如果设置为，编辑光标应移动到编辑器文本内容中指定的位置。与`Cursor`不同，该属性不适用于预编辑文本，而是对周围文本生效。提交字符串提交后，光标会移动，预编辑字符串将位于新的编辑位置。起始位置指定新位置，长度变量可用于从该点开始设置选择。该值未被使用。
- `QInputMethodEvent::MimeData`：`5`;如果设置为，变体包含一个`QMimeData`对象表示已提交文本。`commitString()`仍然提供提交文本的明文表示。

### `QInputMethodEvent::QInputMethodEvent()`

**作用与语义：**

构造类型为`QEvent::InputMethod`的事件。`attributes()`、`preeditString()`、`commitString()`、`replacementStart()`和`replacementLength()`初始化为默认值。

### `QInputMethodEvent::QInputMethodEvent(const QString &preeditText, const QList<QInputMethodEvent::Attribute> &attributes)`

**作用与语义：**

构造类型为`QEvent::InputMethod`的事件。预编辑文本设置为`preeditText`，属性设置为`attributes`。
`commitString()`、`replacementStart()`和`replacementLength()`的数值可以用`setCommitString()`设置。

### `const QList<QInputMethodEvent::Attribute> &QInputMethodEvent::attributes() const`

**作用与语义：**

返回传递给`QInputMethodEvent`构造器的属性列表。属性控制预编辑字符串的视觉外观（预编辑字符串外文本的视觉外观仅由控件控制）。

### `const QString &QInputMethodEvent::commitString() const`

**作用与语义：**

返回应添加（或替换）编辑器控件文本部分内容的文本。这通常是输入操作的结果，必须直接插入到控件文本中，位于预编辑字符串之前。

### `const QString &QInputMethodEvent::preeditString() const`

**作用与语义：**

返回预编辑文本，即用户开始编辑前的文本。

### `int QInputMethodEvent::replacementLength() const`

**作用与语义：**

返回预编辑字符串中需要替换的字符数。

### `int QInputMethodEvent::replacementStart() const`

**作用与语义：**

返回从预编辑字符串起始位置，以相对位置替换字符。

### `void QInputMethodEvent::setCommitString(const QString &commitString, int replaceFrom = 0, int replaceLength = 0)`

**作用与语义：**

将提交字符串设置为`commitString`。
提交字符串是应添加（或替换）编辑器控件文本部分内容的文本。它通常是输入操作的结果，必须在预编辑字符串之前直接插入控件文本中。
如果提交字符串应替换编辑器中的部分文本，`replaceLength` 指定要替换的字符数。`replaceFrom` 指定从预编辑字符串起始起位置，替换字符的位置。

### `class Attribute`

**作用与语义：**

QInputMethodEvent：：Attribute 类存储输入法属性。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QInputMethodEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
