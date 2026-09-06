# QDomNamedNodeMap

> Qt 6.11.1 · Qt XML

## 1. 先建立直觉

**一句话定位：** `QDomNamedNodeMap` 是结构化文档类型，负责 JSON/XML 节点、值、解析状态或流式读写。

**模块背景：** Qt XML 提供 XML 文档和 DOM 风格 XML 数据处理能力。

### 这是什么

`QDomNamedNodeMap` 是 结构化文本解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QDomNamedNodeMap>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Xml)
target_link_libraries(mytarget PRIVATE Qt6::Xml)
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

- `QDomNamedNodeMap()`
- `QDomNamedNodeMap(const QDomNamedNodeMap &namedNodeMap)`
- `~QDomNamedNodeMap()`
- `bool contains(const QString &name) const`
- `int count() const`
- `bool isEmpty() const`
- `QDomNode item(int index) const`
- `int length() const`
- `QDomNode namedItem(const QString &name) const`
- `QDomNode namedItemNS(const QString &nsURI, const QString &localName) const`
- `QDomNode removeNamedItem(const QString &name)`
- `QDomNode removeNamedItemNS(const QString &nsURI, const QString &localName)`
- `QDomNode setNamedItem(const QDomNode &newNode)`
- `QDomNode setNamedItemNS(const QDomNode &newNode)`
- `int size() const`
- `bool operator!=(const QDomNamedNodeMap &other) const`
- `QDomNamedNodeMap & operator=(const QDomNamedNodeMap &other)`
- `bool operator==(const QDomNamedNodeMap &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QDomNamedNodeMap::QDomNamedNodeMap()`

**作用与语义：**

构造一个空的命名节点映射。

### `QDomNamedNodeMap::QDomNamedNodeMap(const QDomNamedNodeMap &namedNodeMap)`

**作用与语义：**

构建了一份`namedNodeMap`的复制品。

### `[noexcept] QDomNamedNodeMap::~QDomNamedNodeMap()`

**作用与语义：**

摧毁该物体并释放其资源。

### `bool QDomNamedNodeMap::contains(const QString &name) const`

**作用与语义：**

如果映射包含一个叫`name`的节点，返回`true`;否则返回`false`。
注意：该函数不考虑命名空间的存在。使用`namedItemNS()`测试映射是否包含具有特定命名空间URI和名称的节点。

### `int QDomNamedNodeMap::count() const`

**作用与语义：**

该函数用于保证 Qt API 一致性。它等同于 `length()`。

### `bool QDomNamedNodeMap::isEmpty() const`

**作用与语义：**

如果映射为空，返回`true`;否则返回`false`。该函数用于保证Qt API一致性。

### `QDomNode QDomNamedNodeMap::item(int index) const`

**作用与语义：**

检索位置`index`的节点。
这可以用来遍历映射。注意映射中的节点是任意排序的。

### `int QDomNamedNodeMap::length() const`

**作用与语义：**

返回映射中的节点数量。

### `QDomNode QDomNamedNodeMap::namedItem(const QString &name) const`

**作用与语义：**

返回名为 `name` 的节点。
如果命名节点映射中没有这样的节点，则返回一个空节点。节点的名称是`QDomNode::nodeName()`返回的名称。

### `QDomNode QDomNamedNodeMap::namedItemNS(const QString &nsURI, const QString &localName) const`

**作用与语义：**

返回与本地名称`localName`关联的节点和URI命名空间`nsURI`。
如果映射中不包含这样的节点，则返回一个空节点。

### `QDomNode QDomNamedNodeMap::removeNamedItem(const QString &name)`

**作用与语义：**

移除地图上的节点`name`。
该函数返回被移除的节点，或者如果映射中没有称为`name`的节点，则返回空节点。

### `QDomNode QDomNamedNodeMap::removeNamedItemNS(const QString &nsURI, const QString &localName)`

**作用与语义：**

将本地名为`localName`的节点和URI命名空间`nsURI`从地图中移除。
函数返回被移除的节点，或者如果映射中没有本地名称为`localName`且命名空间为URI的节点，则返回空节点`nsURI`。

### `QDomNode QDomNamedNodeMap::setNamedItem(const QDomNode &newNode)`

**作用与语义：**

将节点 `newNode` 插入到命名的节点映射中。映射使用的名称是 `QDomNode::nodeName()` 返回的 S 的节点名`newNode`。
如果新节点替换了已有节点，即映射中包含同名节点，则返回被替换的节点。

### `QDomNode QDomNamedNodeMap::setNamedItemNS(const QDomNode &newNode)`

**作用与语义：**

将节点`newNode`插入映射中。如果映射中已有具有相同命名空间URI且本地名称相同的节点，则被替换为`newNode`。如果新节点替换已有节点，则返回被替换的节点。

### `int QDomNamedNodeMap::size() const`

**作用与语义：**

该函数用于保证 Qt API 一致性。它等同于 `length()`。

### `bool QDomNamedNodeMap::operator!=(const QDomNamedNodeMap &other) const`

**作用与语义：**

如果 `other` 与该命名节点映射不相等，返回 `true`;否则返回 `false`。

### `QDomNamedNodeMap &QDomNamedNodeMap::operator=(const QDomNamedNodeMap &other)`

**作用与语义：**

将`other`分配到这个命名的节点映射。

### `bool QDomNamedNodeMap::operator==(const QDomNamedNodeMap &other) const`

**作用与语义：**

如果`other`和该命名节点映射相等，则返回`true`;否则返回`false`。

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

`QDomNamedNodeMap` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
