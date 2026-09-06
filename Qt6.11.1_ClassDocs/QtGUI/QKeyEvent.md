# QKeyEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QKeyEvent` 是 Qt 的值类型，围绕“键事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QKeyEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QKeyEvent>`
- 继承自：QInputEvent
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

### 公有函数

- `QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1)`
- `QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, quint32 nativeScanCode, quint32 nativeVirtualKey, quint32 nativeModifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1, const QInputDevice *device = QInputDevice::primaryKeyboard())`
- `int count() const`
- `bool isAutoRepeat() const`
- `int key() const`
- `(since 6.0) QKeyCombination keyCombination() const`
- `bool matches(QKeySequence::StandardKey key) const`
- `Qt::KeyboardModifiers modifiers() const`
- `quint32 nativeModifiers() const`
- `quint32 nativeScanCode() const`
- `quint32 nativeVirtualKey() const`
- `QString text() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QKeyEvent::QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1)`

**作用与语义：**

构造一个按键事件对象。
`type`参数必须是`QEvent::KeyPress`、`QEvent::KeyRelease`或`QEvent::ShortcutOverride`。
Int `key` 是事件循环应监听的`Qt::Key`代码。如果 `key` 为 0，则该事件不是已知密钥的结果;例如，可能是 compose 序列或键盘宏的结果。`modifiers` 存储键盘修饰符，给定的`text`是密钥生成的 Unicode 文本。如果 `autorep` 为真，则 `isAutoRepeat()` 为真。`count` 是事件涉及的密钥数量。

### `QKeyEvent::QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, quint32 nativeScanCode, quint32 nativeVirtualKey, quint32 nativeModifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1, const QInputDevice *device = QInputDevice::primaryKeyboard())`

**作用与语义：**

构造一个按键事件对象。
`type`参数必须是`QEvent::KeyPress`、`QEvent::KeyRelease`或`QEvent::ShortcutOverride`。
整数`key`是事件循环应监听的`Qt::Key`代码。如果`key`为0，则该事件不是已知密钥的结果;例如，它可能是compose序列或键盘宏的结果。`modifiers`中存储键盘修饰符，给定`text`是密钥生成的Unicode文本。如果`autorep`为真，则`isAutoRepeat()`为真。`count`是事件涉及的密钥数量。
除了常规的密钥事件数据外，还包含`nativeScanCode`、`nativeVirtualKey`和`nativeModifiers`。这些额外数据被快捷方式系统用来决定触发哪些快捷方式。

### `int QKeyEvent::count() const`

**作用与语义：**

返回该事件涉及的密钥数量。如果`text()`不是空的，则仅为字符串长度。

### `bool QKeyEvent::isAutoRepeat() const`

**作用与语义：**

如果该事件来自自动重复键，返回`true`;如果来自初始按键，返回`false`。
注意，如果事件是一个多键压缩事件，且部分由自动重复导致，该函数可能会不确定地返回真或假。

### `int QKeyEvent::key() const`

**作用与语义：**

返回按下或释放的按键的代码。
请参阅 `Qt::Key` 获取键盘代码列表。这些代码与底层窗口系统无关。请注意，该函数不会区分大小写字母，如需区分，请使用 `text()` 函数（返回按键生成的 Unicode 文本）。
值为 0 或 `Qt::Key_unknown` 表示事件不是已知按键产生的；例如，它可能是组合序列、键盘宏或按键事件压缩导致的结果。

### `[since 6.0] QKeyCombination QKeyEvent::keyCombination() const`

**作用与语义：**

返回一个包含该事件携带`key()`和`modifiers()`的 `QKeyCombination`对象。

### `bool QKeyEvent::matches(QKeySequence::StandardKey key) const`

**作用与语义：**

如果按键事件符合给定标准`key`，返回`true`;否则返回`false`。

### `Qt::KeyboardModifiers QKeyEvent::modifiers() const`

**作用与语义：**

返回事件发生后立即存在的键盘修饰标志。
警告：此功能并非总是可信。用户可能会同时按下两个Shift键并松开其中一个来混淆它。

### `quint32 QKeyEvent::nativeModifiers() const`

**作用与语义：**

返回按键事件的本地修饰符。如果按键事件不包含该数据，则返回 0。
注意：即使密钥事件包含扩展信息，本地修饰符也可以为0。

### `quint32 QKeyEvent::nativeScanCode() const`

**作用与语义：**

返回密钥事件的本地扫描码。如果密钥事件不包含该数据，返回为0。
注意：本地扫描码可能为0，即使密钥事件包含扩展信息。

### `quint32 QKeyEvent::nativeVirtualKey() const`

**作用与语义：**

返回本地虚拟键，或键事件的键符号。如果键事件不包含该数据，则返回0。
注意：本地虚拟密钥可能为0，即使密钥事件包含扩展信息。

### `QString QKeyEvent::text() const`

**作用与语义：**

返回该密钥生成的Unicode文本。
文本不限于可打印的Unicode代码点范围，可能包含控制字符或其他Unicode类别字符，包括`QChar::Other_PrivateUse`。
文本也可能为空，例如当按下Shift、Control、Alt和Meta等修饰键（取决于平台）时。`key()`函数始终返回有效值。

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

`QKeyEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
