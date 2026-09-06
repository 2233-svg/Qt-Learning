# QUndoCommand

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QUndoCommand` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QUndoCommand>`
- 继承自：未在类页中列出
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

- `QUndoCommand(QUndoCommand *parent = nullptr)`
- `QUndoCommand(const QString &text, QUndoCommand *parent = nullptr)`
- `virtual ~QUndoCommand()`
- `QString actionText() const`
- `const QUndoCommand * child(int index) const`
- `int childCount() const`
- `virtual int id() const`
- `bool isObsolete() const`
- `virtual bool mergeWith(const QUndoCommand *command)`
- `virtual void redo()`
- `void setObsolete(bool obsolete)`
- `void setText(const QString &text)`
- `QString text() const`
- `virtual void undo()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QUndoCommand::QUndoCommand(QUndoCommand *parent = nullptr)`

**作用与语义：**

构造一个带有父`parent`的QUndoCommand对象。
如果 `parent` 未被`nullptr`，该命令会附加到父命令的子列表中。父命令随后拥有该命令，并会在其 destructor 中删除它。

### `[explicit] QUndoCommand::QUndoCommand(const QString &text, QUndoCommand *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`和`text`的QUndoCommand对象。
如果`parent`未`nullptr`，该命令会附加到父命令的子列表。父命令拥有该命令，并会在其解构器中删除该命令。

### `[virtual noexcept] QUndoCommand::~QUndoCommand()`

**作用与语义：**

销毁`QUndoCommand`对象和所有子命令。

### `QString QUndoCommand::actionText() const`

**作用与语义：**

返回一个简短的文本字符串，描述该命令的作用;例如，“插入文本”。
当栈的撤销和重做操作的文本属性更新时，文本就会被使用。

### `const QUndoCommand *QUndoCommand::child(int index) const`

**作用与语义：**

返回子命令 `index`。

### `int QUndoCommand::childCount() const`

**作用与语义：**

返回该命令中的子命令数量。

### `[virtual] int QUndoCommand::id() const`

**作用与语义：**

返回该命令的ID。
命令 ID 用于命令压缩。它必须是该命令类唯一的整数，或者如果命令不支持压缩，则为 -1。
如果命令支持压缩，必须在派生类中覆盖该函数以返回正确的ID。基础实现返回-1。
`QUndoStack::push()`只有在两个命令的ID相同且ID不是-1时才会尝试合并。

### `bool QUndoCommand::isObsolete() const`

**作用与语义：**

返回命令是否过时。
布尔用于自动移除堆栈中不再需要的命令。isObsolete函数在函数`QUndoStack::push()`、`QUndoStack::undo()`、`QUndoStack::redo()`和`QUndoStack::setIndex()`中检查。

### `[virtual] bool QUndoCommand::mergeWith(const QUndoCommand *command)`

**作用与语义：**

尝试将该命令与`command`合并。成功时返回`true`;否则返回`false`。
如果该函数返回`true`，调用该命令的`redo()`必须具有相同的效果，必须与重新执行该命令和`command`相同的效果。同样，调用该命令的`undo()`也必须与撤销`command`和该命令的效果相同。
`QUndoStack`只有当两个命令的 ID 相同且 id 不是 -1 时才会尝试合并它们。
默认实现返回`false`。

**官方示例：**

```cpp
 bool AppendText::mergeWith(const QUndoCommand *other)
 {
     if (other->id() != id()) // make sure other is also an AppendText command
         return false;
     m_text += static_cast<const AppendText*>(other)->m_text;
     return true;
 }
```

### `[virtual] void QUndoCommand::redo()`

**作用与语义：**

对文档进行更改。该函数必须在派生类中实现。调用该函数的`QUndoStack::push()`、`QUndoStack::undo()`或`QUndoStack::redo()`会导致未定义的 beahavior。
默认实现对所有子命令调用 redo()。

### `void QUndoCommand::setObsolete(bool obsolete)`

**作用与语义：**

设置该命令是否对`obsolete`过时。

### `void QUndoCommand::setText(const QString &text)`

**作用与语义：**

将命令文本设置为指定的`text`。
指定的文本应是简短且用户可读的字符串，描述该命令的作用。
如果你需要为`text()`和`actionText()`使用两个不同的字符串，用“\n”分隔，然后进入这个函数。即使你在开发时不使用这个功能用于英语字符串，你仍然可以允许翻译者使用两个不同的字符串，以满足特定语言的需求。上述功能和功能`actionText()`自Qt 4.8起就已可用。

### `QString QUndoCommand::text() const`

**作用与语义：**

返回一个简短的文本字符串，描述该命令的作用;例如，“插入文本”。
文本用于`QUndoView`中物品名称。

### `[virtual] void QUndoCommand::undo()`

**作用与语义：**

还原文档的更改。调用 undo() 后，文档状态应与调用前相同`redo()`。该函数必须在派生类中实现。调用该函数的 `QUndoStack::push()`、`QUndoStack::undo()` 或 `QUndoStack::redo()` 会导致 beahavior 未定义。
默认实现会对所有子命令逆序调用 undo()。

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

`QUndoCommand` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
