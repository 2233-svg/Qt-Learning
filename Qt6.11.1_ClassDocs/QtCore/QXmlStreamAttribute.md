# QXmlStreamAttribute

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QXmlStreamAttribute` 是结构化文档类型，负责 JSON/XML 节点、值、解析状态或流式读写。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QXmlStreamAttribute` 是 结构化文本解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QXmlStreamAttribute>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

### 状态、生命周期和线程

**生命周期：** 解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

**状态与结果：** 先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

**线程与事件循环：** 值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

## 3. 直接使用

接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QXmlStreamAttribute()`
- `QXmlStreamAttribute(const QString &qualifiedName, const QString &value)`
- `QXmlStreamAttribute(const QString &namespaceUri, const QString &name, const QString &value)`
- `bool isDefault() const`
- `QStringView name() const`
- `QStringView namespaceUri() const`
- `QStringView prefix() const`
- `QStringView qualifiedName() const`
- `QStringView value() const`

### 相关非成员函数

- `bool operator!=(const QXmlStreamAttribute &lhs, const QXmlStreamAttribute &rhs)`
- `bool operator==(const QXmlStreamAttribute &lhs, const QXmlStreamAttribute &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QXmlStreamAttribute::QXmlStreamAttribute()`

**作用与语义：**

生成一个空属性。

### `QXmlStreamAttribute::QXmlStreamAttribute(const QString &qualifiedName, const QString &value)`

**作用与语义：**

构造带有限定名称`qualifiedName`和值`value`的属性。

### `QXmlStreamAttribute::QXmlStreamAttribute(const QString &namespaceUri, const QString &name, const QString &value)`

**作用与语义：**

在命名空间中构造一个属性，`namespaceUri` 为 `name`，值为 `value`。

### `bool QXmlStreamAttribute::isDefault() const`

**作用与语义：**

如果解析器在DTD中以默认值添加该属性，则返回`true`;否则返回`false`。

### `QStringView QXmlStreamAttribute::name() const`

**作用与语义：**

返回属性的本地名称。

### `QStringView QXmlStreamAttribute::namespaceUri() const`

**作用与语义：**

返回属性解析后的 namespaceUri，或者如果属性没有定义命名空间，则返回空字符串引用。

### `QStringView QXmlStreamAttribute::prefix() const`

**作用与语义：**

返回属性的命名空间前缀。

### `QStringView QXmlStreamAttribute::qualifiedName() const`

**作用与语义：**

返回属性的限定名称。
限定名称是XML数据中属性的原始名称。它由命名空间`prefix()`、冒号和属性的本地 `name()`组成。由于命名空间前缀不唯一（同一个前缀可能指向不同的命名空间，不同前缀也可能指向同一命名空间），你不应使用qualifiedName()，而应使用已解析的`namespaceUri()`和属性的本地 `name()`。

### `QStringView QXmlStreamAttribute::value() const`

**作用与语义：**

返回属性的值。

### `[noexcept] bool operator!=(const QXmlStreamAttribute &lhs, const QXmlStreamAttribute &rhs)`

**作用与语义：**

比较`lhs`属性与`rhs`，如果不相等则返回`true`;否则返回`false`。

### `[noexcept] bool operator==(const QXmlStreamAttribute &lhs, const QXmlStreamAttribute &rhs)`

**作用与语义：**

将 `lhs` 属性与 `rhs` 进行比较，如果相等则返回 `true`；否则返回 `false`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

### 状态和错误边界

先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

### 线程边界

值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

### 最容易出现的错误

不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QXmlStreamAttribute` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
