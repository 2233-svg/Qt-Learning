# QJsonArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** JSON 数组容器，负责按顺序保存和访问 JSON 值。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJsonArray`：JSON 数组容器，负责按顺序保存和访问 JSON 值。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QJsonArray>`
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

接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class const_iterator`
- `class iterator`
- `ConstIterator`
- `Iterator`
- `const_pointer`
- `const_reference`
- `difference_type`
- `pointer`
- `reference`
- `size_type`
- `value_type`

### 公有函数

- `QJsonArray()`
- `QJsonArray(std::initializer_list<QJsonValue> args)`
- `QJsonArray(const QJsonArray &other)`
- `QJsonArray(QJsonArray &&other)`
- `~QJsonArray()`
- `void append(const QJsonValue &value)`
- `QJsonValue at(qsizetype i) const`
- `QJsonArray::iterator begin()`
- `QJsonArray::const_iterator begin() const`
- `QJsonArray::const_iterator cbegin() const`
- `QJsonArray::const_iterator cend() const`
- `QJsonArray::const_iterator constBegin() const`
- `QJsonArray::const_iterator constEnd() const`
- `bool contains(const QJsonValue &value) const`
- `qsizetype count() const`
- `bool empty() const`
- `QJsonArray::iterator end()`
- `QJsonArray::const_iterator end() const`
- `QJsonArray::iterator erase(QJsonArray::iterator it)`
- `QJsonValue first() const`
- `QJsonArray::iterator insert(QJsonArray::iterator before, const QJsonValue &value)`
- `void insert(qsizetype i, const QJsonValue &value)`
- `bool isEmpty() const`
- `QJsonValue last() const`
- `void pop_back()`
- `void pop_front()`
- `void prepend(const QJsonValue &value)`
- `void push_back(const QJsonValue &value)`
- `void push_front(const QJsonValue &value)`
- `void removeAt(qsizetype i)`
- `void removeFirst()`
- `void removeLast()`
- `void replace(qsizetype i, const QJsonValue &value)`
- `qsizetype size() const`
- `void swap(QJsonArray &other)`
- `QJsonValue takeAt(qsizetype i)`
- `QVariantList toVariantList() const`
- `QJsonArray operator+(const QJsonValue &value) const`
- `QJsonArray & operator+=(const QJsonValue &value)`
- `QJsonArray & operator<<(const QJsonValue &value)`
- `QJsonArray & operator=(QJsonArray &&other)`
- `QJsonArray & operator=(const QJsonArray &other)`
- `QJsonValueRef operator[](qsizetype i)`
- `QJsonValue operator[](qsizetype i) const`

### 静态公有成员

- `QJsonArray fromStringList(const QStringList &list)`
- `QJsonArray fromVariantList(const QVariantList &list)`

### 相关非成员函数

- `bool operator!=(const QJsonArray &lhs, const QJsonArray &rhs)`
- `bool operator==(const QJsonArray &lhs, const QJsonArray &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QJsonArray::ConstIterator`

**作用与语义：**

Qt风格的同义词`QJsonArray::const_iterator`。

### `QJsonArray::Iterator`

**作用与语义：**

Qt风格的同义词`QJsonArray::iterator`。

### `QJsonArray::const_pointer`

**作用与语义：**

Typedef 用于 const `QJsonValue` *。提供 STL 兼容性。

### `QJsonArray::const_reference`

**作用与语义：**

Typedef 用于 const 的 const `QJsonValue` &。为 STL 兼容性提供了支持。

### `QJsonArray::difference_type`

**作用与语义：**

qsizetype 的 Typedef。为 STL 兼容性提供。

### `QJsonArray::pointer`

**作用与语义：**

Typedef 用于 `QJsonValue` *。提供 STL 兼容性。

### `QJsonArray::reference`

**作用与语义：**

Typedef 用于 `QJsonValue` 和。提供以兼容 STL 的。

### `QJsonArray::size_type`

**作用与语义：**

qsizetype 的 Typedef。为 STL 兼容性提供。

### `QJsonArray::value_type`

**作用与语义：**

Typedef 用于`QJsonValue`。提供 STL 兼容性。

### `QJsonArray::QJsonArray()`

**作用与语义：**

创建一个空数组。

### `QJsonArray::QJsonArray(std::initializer_list<QJsonValue> args)`

**作用与语义：**

从初始化列表创建`args`数组。
QJson数组的构造方式类似于JSON符号，例如：

**官方示例：**

```cpp
 QJsonArray array = { 1, 2.2, QString() };
```

### `[noexcept] QJsonArray::QJsonArray(const QJsonArray &other)`

**作用与语义：**

创建`other`的副本。
由于QJsonArray是隐式共享的，只要对象不被修改，复制内容就很浅。

### `[noexcept] QJsonArray::QJsonArray(QJsonArray &&other)`

**作用与语义：**

从`other`中移动构建一个QJson数组。

### `[noexcept] QJsonArray::~QJsonArray()`

**作用与语义：**

删除了数组。

### `void QJsonArray::append(const QJsonValue &value)`

**作用与语义：**

插入 `value` 在数组末端。

### `QJsonValue QJsonArray::at(qsizetype i) const`

**作用与语义：**

返回一个`QJsonValue`，表示索引`i`的值。
如果`i`出界，回`QJsonValue`为`Undefined`。

### `QJsonArray::iterator QJsonArray::begin()`

**作用与语义：**

返回一个STL风格的迭代器，指向数组中的第一个项。

### `QJsonArray::const_iterator QJsonArray::begin() const`

**作用与语义：**

返回一个STL风格的迭代器，指向数组中的第一个项。

### `QJsonArray::const_iterator QJsonArray::cbegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向数组中的第一个项。

### `QJsonArray::const_iterator QJsonArray::cend() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向数组最后一个项之后的虚数项。

### `QJsonArray::const_iterator QJsonArray::constBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向数组中的第一个项。

### `QJsonArray::const_iterator QJsonArray::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代子，指向数组最后一个项之后的虚数项。

### `bool QJsonArray::contains(const QJsonValue &value) const`

**作用与语义：**

如果数组中出现`value`，返回`true`，否则返回`false`。

### `qsizetype QJsonArray::count() const`

**作用与语义：**

和`size()`一样。

### `bool QJsonArray::empty() const`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`isEmpty()`，如果数组为空，返回`true`。

### `QJsonArray::iterator QJsonArray::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向数组最后一个项之后的虚数项。

### `QJsonArray::const_iterator QJsonArray::end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向数组最后一个项之后的虚数项。

### `QJsonArray::iterator QJsonArray::erase(QJsonArray::iterator it)`

**作用与语义：**

移除`it`指向的项目，返回指向下一个项目的迭代器。

### `QJsonValue QJsonArray::first() const`

**作用与语义：**

返回数组中存储的第一个值。
和`at(0)`一样。

### `[static] QJsonArray QJsonArray::fromStringList(const QStringList &list)`

**作用与语义：**

将字符串列表`list`转换为`QJsonArray`。
`list`中的数值将转换为JSON值。

### `[static] QJsonArray QJsonArray::fromVariantList(const QVariantList &list)`

**作用与语义：**

将变体列表`list`转换为`QJsonArray`。
`list`中的`QVariant`数值将转换为JSON值。
注意：从`QVariant`转换并非完全无损。更多信息请参见`QJsonValue::fromVariant()`文档。

### `QJsonArray::iterator QJsonArray::insert(QJsonArray::iterator before, const QJsonValue &value)`

**作用与语义：**

插入`value` `before` 指向的位置之前，并返回指向新插入项的迭代器。

### `void QJsonArray::insert(qsizetype i, const QJsonValue &value)`

**作用与语义：**

在数组的索引位置插入`value` `i`。如果`i` `0`，则该值会被附加到数组前。如果`i` `size()`，则将该值附加到数组中。

### `bool QJsonArray::isEmpty() const`

**作用与语义：**

如果对象为空，返回`true`。这与 `size()` == 0 相同。

### `QJsonValue QJsonArray::last() const`

**作用与语义：**

返回数组中存储的最后一个值。
和`at(size() - 1)`一样。

### `void QJsonArray::pop_back()`

**作用与语义：**

该函数是为了STL兼容性而提供的。它等价于`removeLast()`。数组不能为空。如果数组可以为空，调用`isEmpty()`再调用该函数。

### `void QJsonArray::pop_front()`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`removeFirst()`。数组不能是空的。如果数组可以空，调用`isEmpty()`再调用该函数。

### `void QJsonArray::prepend(const QJsonValue &value)`

**作用与语义：**

插入`value`在数组开头。
这和 `insert(0, value)` 相同，会在数组前加 `value`。

### `void QJsonArray::push_back(const QJsonValue &value)`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`append`（值），并会将`value`附加到数组中。

### `void QJsonArray::push_front(const QJsonValue &value)`

**作用与语义：**

该函数是为了STL兼容性而提供。它等价于`prepend`（值），并会在数组前加上`value`。

### `void QJsonArray::removeAt(qsizetype i)`

**作用与语义：**

去除索引位置`i`的值。`i`必须是数组中的有效索引位置（即`0 <= i < size()`）。

### `void QJsonArray::removeFirst()`

**作用与语义：**

移除数组中的第一个项。调用该函数等同于调用`removeAt(0)`。数组不能为空。如果数组可以为空，调用`isEmpty()`再调用该函数。

### `void QJsonArray::removeLast()`

**作用与语义：**

移除数组中的最后一项。调用该函数等同于调用 `removeAt(size() - 1)`。数组不得为空。如果数组为空，调用 `isEmpty()` 再调用该函数。

### `void QJsonArray::replace(qsizetype i, const QJsonValue &value)`

**作用与语义：**

用 `value` 替换索引位置 `i` 的项。`i` 必须是数组中的有效索引位置（即 `0 <= i < size()`）。

### `qsizetype QJsonArray::size() const`

**作用与语义：**

返回数组中存储的值数量。

### `[noexcept] void QJsonArray::swap(QJsonArray &other)`

**作用与语义：**

将该阵列与`other`交换。此操作非常快速且从未失败。

### `QJsonValue QJsonArray::takeAt(qsizetype i)`

**作用与语义：**

移除索引位置`i`的项并返回。`i` 必须是数组中的有效索引位置（即 `0 <= i < size()`）。
如果不使用返回值，`removeAt()`效率更高。

### `QVariantList QJsonArray::toVariantList() const`

**作用与语义：**

将该物体转换为`QVariantList`。
返回已创建的地图。

### `QJsonArray QJsonArray::operator+(const QJsonValue &value) const`

**作用与语义：**

返回包含该数组中所有项的数组，后面跟随提供的`value`。

### `QJsonArray &QJsonArray::operator+=(const QJsonValue &value)`

**作用与语义：**

将`value`附加到数组中，并返回数组本身的引用。

### `QJsonArray &QJsonArray::operator<<(const QJsonValue &value)`

**作用与语义：**

将`value`附加到数组中，并返回数组本身的引用。

### `[noexcept] QJsonArray &QJsonArray::operator=(QJsonArray &&other)`

**作用与语义：**

移动分配`other`到该数组。

### `[noexcept] QJsonArray &QJsonArray::operator=(const QJsonArray &other)`

**作用与语义：**

将`other`分配到该数组。

### `QJsonValueRef QJsonArray::operator[](qsizetype i)`

**作用与语义：**

返回索引位置的值，`i` 作为可修改的引用。`i` 必须是数组中的有效索引位置（即 `0 <= i < size()`）。
返回值类型为`QJsonValueRef`，是`QJsonArray`和`QJsonObject`的辅助类。当你获得类型为`QJsonValueRef`的对象时，可以将其视为对`QJsonValue`的引用。如果你赋值，赋值将应用到你获得引用的`QJsonObject` `QJsonArray`中的字符。

### `QJsonValue QJsonArray::operator[](qsizetype i) const`

**作用与语义：**

和`at()`一样。

### `[noexcept] bool operator!=(const QJsonArray &lhs, const QJsonArray &rhs)`

**作用与语义：**

如果 `lhs` 数组不等于 `rhs`，则返回 `true`，否则返回 `false`。

### `[noexcept] bool operator==(const QJsonArray &lhs, const QJsonArray &rhs)`

**作用与语义：**

如果 `lhs` 数组等于 `rhs`，则返回 `true`，否则返回 `false`。

### `class const_iterator`

**作用与语义：**

QJsonArray：：const_iterator 类为 QJsonArray 提供了一个 STL 风格的 const 迭代器。
`QJsonArray::const_iterator`允许你对`QJsonArray`进行迭代。如果你想在迭代时修改`QJsonArray`，可以用`QJsonArray::iterator`。通常在非const的`QJsonArray`上使用`QJsonArray::const_iterator`是个好习惯，除非你需要通过迭代器更改`QJsonArray`。Const迭代器速度稍快，且提高了代码的可读性。
默认的`QJsonArray::const_iterator`构造器会创建一个未初始化的迭代器。你必须用`QJsonArray`函数如`QJsonArray::constBegin()`、`QJsonArray::constEnd()`或`QJsonArray::insert()`初始化它，才能开始迭代。
大多数`QJsonArray`函数接受整数索引而非迭代器。因此，迭代器很少在`QJsonArray`中有用。STL式迭代器在一个合理的领域是作为通用算法的参数。
多个迭代器可以用于同一个数组。但请注意，任何对`QJsonArray`执行的非const函数调用都会使所有现有迭代器变得无定义。

### `class iterator`

**作用与语义：**

QJsonArray：：iterator 类为 QJsonArray 提供了一个 STL 风格的非const迭代器。
`QJsonArray::iterator`允许你对`QJsonArray`进行迭代，并修改与迭代器关联的数组项。如果你想对const的迭代`QJsonArray`，可以用`QJsonArray::const_iterator`。通常在非const的`QJsonArray`上使用`QJsonArray::const_iterator`是个好习惯，除非你需要通过迭代器更改`QJsonArray`。Const迭代器速度稍快，且提高了代码的可读性。
默认的 `QJsonArray::iterator` 构造器会创建一个未初始化的迭代器。你必须先用 `QJsonArray::begin()`、`QJsonArray::end()` 或 `QJsonArray::insert()` 等`QJsonArray`函数初始化它，才能开始迭代。
大多数`QJsonArray`函数接受整数索引而非迭代器。因此，迭代器很少在`QJsonArray`相关方面有用。STL式迭代器在一个合理的地方是作为通用算法的参数。
多个迭代器可以用于同一个数组。但请注意，任何对`QJsonArray`执行的非const函数调用都会使所有现有迭代器未定义。

### `ConstIterator`

**作用与语义：**

Qt风格的同义词`QJsonArray::const_iterator`。

### `Iterator`

**作用与语义：**

Qt风格的同义词`QJsonArray::iterator`。

### `const_pointer`

**作用与语义：**

Typedef 用于 const `QJsonValue` *。提供 STL 兼容性。

### `const_reference`

**作用与语义：**

Typedef 用于 const 的 const `QJsonValue` &。为 STL 兼容性提供了支持。

### `difference_type`

**作用与语义：**

qsizetype 的 Typedef。为 STL 兼容性提供。

### `pointer`

**作用与语义：**

Typedef 用于 `QJsonValue` *。提供 STL 兼容性。

### `reference`

**作用与语义：**

Typedef 用于 `QJsonValue` 和。提供以兼容 STL 的。

### `size_type`

**作用与语义：**

qsizetype 的 Typedef。为 STL 兼容性提供。

### `value_type`

**作用与语义：**

Typedef 用于`QJsonValue`。提供 STL 兼容性。

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

`QJsonArray` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
