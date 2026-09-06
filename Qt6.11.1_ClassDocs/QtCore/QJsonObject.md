# QJsonObject

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** JSON 对象容器，负责按键保存和访问 JSON 值。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJsonObject`：JSON 对象容器，负责按键保存和访问 JSON 值。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QJsonObject>`
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
- `(since 6.10) const_key_value_iterator`
- `key_type`
- `(since 6.10) key_value_iterator`
- `mapped_type`
- `size_type`

### 公有函数

- `QJsonObject()`
- `QJsonObject(std::initializer_list<std::pair<QString, QJsonValue>> args)`
- `QJsonObject(const QJsonObject &other)`
- `QJsonObject(QJsonObject &&other)`
- `~QJsonObject()`
- `(since 6.10) auto asKeyValueRange() &&`
- `(since 6.10) auto asKeyValueRange() &`
- `(since 6.10) auto asKeyValueRange() const &&`
- `(since 6.10) auto asKeyValueRange() const &`
- `QJsonObject::iterator begin()`
- `QJsonObject::const_iterator begin() const`
- `QJsonObject::const_iterator constBegin() const`
- `QJsonObject::const_iterator constEnd() const`
- `QJsonObject::const_iterator constFind(const QString &key) const`
- `QJsonObject::const_iterator constFind(QLatin1StringView key) const`
- `QJsonObject::const_iterator constFind(QStringView key) const`
- `(since 6.10) QJsonObject::const_key_value_iterator constKeyValueBegin() const`
- `(since 6.10) QJsonObject::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const QString &key) const`
- `bool contains(QLatin1StringView key) const`
- `bool contains(QStringView key) const`
- `qsizetype count() const`
- `bool empty() const`
- `QJsonObject::iterator end()`
- `QJsonObject::const_iterator end() const`
- `QJsonObject::iterator erase(QJsonObject::iterator it)`
- `QJsonObject::iterator find(const QString &key)`
- `QJsonObject::iterator find(QLatin1StringView key)`
- `QJsonObject::iterator find(QStringView key)`
- `QJsonObject::const_iterator find(QLatin1StringView key) const`
- `QJsonObject::const_iterator find(QStringView key) const`
- `QJsonObject::const_iterator find(const QString &key) const`
- `QJsonObject::iterator insert(const QString &key, const QJsonValue &value)`
- `QJsonObject::iterator insert(QLatin1StringView key, const QJsonValue &value)`
- `QJsonObject::iterator insert(QStringView key, const QJsonValue &value)`
- `bool isEmpty() const`
- `(since 6.10) QJsonObject::key_value_iterator keyValueBegin()`
- `(since 6.10) QJsonObject::const_key_value_iterator keyValueBegin() const`
- `(since 6.10) QJsonObject::key_value_iterator keyValueEnd()`
- `(since 6.10) QJsonObject::const_key_value_iterator keyValueEnd() const`
- `QStringList keys() const`
- `qsizetype length() const`
- `void remove(const QString &key)`
- `void remove(QLatin1StringView key)`
- `void remove(QStringView key)`
- `qsizetype size() const`
- `void swap(QJsonObject &other)`
- `QJsonValue take(const QString &key)`
- `QJsonValue take(QLatin1StringView key)`
- `QJsonValue take(QStringView key)`
- `QVariantHash toVariantHash() const`
- `QVariantMap toVariantMap() const`
- `QJsonValue value(const QString &key) const`
- `QJsonValue value(QLatin1StringView key) const`
- `QJsonValue value(QStringView key) const`
- `QJsonObject & operator=(QJsonObject &&other)`
- `QJsonObject & operator=(const QJsonObject &other)`
- `QJsonValueRef operator[](const QString &key)`
- `QJsonValue operator[](const QString &key) const`
- `QJsonValueRef operator[](QLatin1StringView key)`
- `QJsonValueRef operator[](QStringView key)`
- `QJsonValue operator[](QLatin1StringView key) const`
- `QJsonValue operator[](QStringView key) const`

### 静态公有成员

- `QJsonObject fromVariantHash(const QVariantHash &hash)`
- `QJsonObject fromVariantMap(const QVariantMap &map)`

### 相关非成员函数

- `bool operator!=(const QJsonObject &lhs, const QJsonObject &rhs)`
- `bool operator==(const QJsonObject &lhs, const QJsonObject &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QJsonObject::ConstIterator`

**作用与语义：**

Qt风格的`QJsonObject::const_iterator`同义词。

### `QJsonObject::Iterator`

**作用与语义：**

Qt风格的`QJsonObject::iterator`同义词。

### `[since 6.10] QJsonObject::const_key_value_iterator`

**作用与语义：**

QJsonObject：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于 `QJsonObject`。
QJsonObject：：const_key_value_iterator 本质上与 `QJsonObject::const_iterator` 相同，区别在于运算符*() 返回的是键值对而非值。
这种类型防御是在Qt 6.10中引入的。

### `QJsonObject::key_type`

**作用与语义：**

Typedef 用于`QString`。提供 STL 兼容性。

### `[since 6.10] QJsonObject::key_value_iterator`

**作用与语义：**

QJsonObject：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QJsonObject`。
QJsonObject：：key_value_iterator 本质上与 `QJsonObject::iterator` 相同，区别在于 operator*() 返回的是键值对而非值。
这种类型防御是在Qt 6.10中引入的。

### `QJsonObject::mapped_type`

**作用与语义：**

Typedef 用于`QJsonValue`。提供 STL 兼容性。

### `QJsonObject::size_type`

**作用与语义：**

qsizetype 的 Typedef。为 STL 兼容性提供。

### `QJsonObject::QJsonObject()`

**作用与语义：**

构造一个空的JSON对象。

### `QJsonObject::QJsonObject(std::initializer_list<std::pair<QString, QJsonValue>> args)`

**作用与语义：**

构建一个从初始化列表初始化`args` QJsonObject实例。例如：

**官方示例：**

```cpp
 QJsonObject object
 {
     {"property1", 1},
     {"property2", 2}
 };
```

### `[noexcept] QJsonObject::QJsonObject(const QJsonObject &other)`

**作用与语义：**

创建`other`的副本。
由于QJsonObject是隐式共享的，只要对象不被修改，复制内容就很浅。

### `[noexcept] QJsonObject::QJsonObject(QJsonObject &&other)`

**作用与语义：**

Move-构造一个 QJsonObject，`other`。

### `[noexcept] QJsonObject::~QJsonObject()`

**作用与语义：**

摧毁了该物体。

### `[since 6.10] auto QJsonObject::asKeyValueRange() const &&`

**作用与语义：**

返回一个范围对象，允许对该对象作为键值对进行循环。例如，该范围对象可以在基于范围的for循环中使用，并结合结构化绑定声明：
注意，通过这种方式获得的值是对对象中值的引用。具体来说，变更该值会修改对象本身。
当在r值上调用该方法时（例如在某个范围for循环的初始化器中创建的临时节点），物体将被捕获在该范围内。

**官方示例：**

```cpp
 QJsonObject obj{
     { "something", "is" },
     { "in", "this" },
     { "object", 42 },
 };

 for (auto [key, value] : obj.asKeyValueRange()) {
     qDebug() << key << "->" << value;
     if (key == "object")
         value = "!"; // modify the object at this key
 }
 qDebug() << obj["object"]; // QJsonValue(string, "!")
```

### `QJsonObject::iterator QJsonObject::begin()`

**作用与语义：**

返回一个STL风格的迭代器，指向对象中的第一个项。

### `QJsonObject::const_iterator QJsonObject::begin() const`

**作用与语义：**

返回一个STL风格的迭代器，指向对象中的第一个项。

### `QJsonObject::const_iterator QJsonObject::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向对象中的第一个项。

### `QJsonObject::const_iterator QJsonObject::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向对象最后一个项之后的虚数项。

### `QJsonObject::const_iterator QJsonObject::constFind(const QString &key) const`

**作用与语义：**

返回一个函数迭代器，指向映射中键为`key`的项目。
如果映射中没有键为`key`的项，函数返回`constEnd()`。

### `QJsonObject::const_iterator QJsonObject::constFind(QLatin1StringView key) const`

**作用与语义：**

返回一个函数迭代器，指向映射中键为`key`的项目。
如果映射中没有键为`key`的项，函数返回`constEnd()`。

### `QJsonObject::const_iterator QJsonObject::constFind(QStringView key) const`

**作用与语义：**

返回一个函数迭代器，指向映射中键为`key`的项目。
如果映射中没有键为`key`的项，函数返回`constEnd()`。

### `[since 6.10] QJsonObject::const_key_value_iterator QJsonObject::constKeyValueBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向对象的第一个条目。

### `[since 6.10] QJsonObject::const_key_value_iterator QJsonObject::constKeyValueEnd() const`

**作用与语义：**

返回一个const型STL风格的迭代器，指向下一个元素之后的虚数元素。

### `bool QJsonObject::contains(const QString &key) const`

**作用与语义：**

如果对象包含密钥`key`，返回`true`。

### `bool QJsonObject::contains(QLatin1StringView key) const`

**作用与语义：**

如果对象包含密钥`key`，返回`true`。

### `bool QJsonObject::contains(QStringView key) const`

**作用与语义：**

如果对象包含密钥`key`，返回`true`。

### `qsizetype QJsonObject::count() const`

**作用与语义：**

和`size()`一样。

### `bool QJsonObject::empty() const`

**作用与语义：**

该函数旨在满足STL兼容性。它等价于`isEmpty()`，如果对象为空，返回`true`;否则返回`false`。

### `QJsonObject::iterator QJsonObject::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向对象中最后一个项之后的虚数项。

### `QJsonObject::const_iterator QJsonObject::end() const`

**作用与语义：**

返回一个STL风格的迭代器，指向对象中最后一个项之后的虚数项。

### `QJsonObject::iterator QJsonObject::erase(QJsonObject::iterator it)`

**作用与语义：**

从映射中移除迭代器`it`指向的（键、值）对，并返回迭代器到映射中的下一个项。

### `QJsonObject::iterator QJsonObject::find(const QString &key)`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `QJsonObject::iterator QJsonObject::find(QLatin1StringView key)`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `QJsonObject::iterator QJsonObject::find(QStringView key)`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `QJsonObject::const_iterator QJsonObject::find(QLatin1StringView key) const`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `QJsonObject::const_iterator QJsonObject::find(QStringView key) const`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `QJsonObject::const_iterator QJsonObject::find(const QString &key) const`

**作用与语义：**

返回一个迭代器，指向地图中键`key`的物品。
如果映射中没有键为`key`的项，函数返回`end()`。

### `[static] QJsonObject QJsonObject::fromVariantHash(const QVariantHash &hash)`

**作用与语义：**

将变体哈希`hash`转换为`QJsonObject`。
`hash`中的键将作为 JSON 对象中的键使用，`QVariant`值会转换为 JSON 值。
注意：从`QVariant`转换并非完全无损。更多信息请参见`QJsonValue::fromVariant()`文档。

### `[static] QJsonObject QJsonObject::fromVariantMap(const QVariantMap &map)`

**作用与语义：**

将变体地图`map`转换为`QJsonObject`。
`map`中的键将作为 JSON 对象中的键使用，`QVariant`值会转换为 JSON 值。
注意：从`QVariant`转换并非完全无损。更多信息请参见`QJsonValue::fromVariant()`文档。

### `QJsonObject::iterator QJsonObject::insert(const QString &key, const QJsonValue &value)`

**作用与语义：**

插入一个键为`key`、值为`value`的新项。
如果已经有带有密钥`key`的项目，则该项的值被替换为`value`。
返回指向插入项的迭代器。
如果该值被`QJsonValue::Undefined`，关键字将从对象中移除。返回的迭代器随后会指向`end()`。

### `QJsonObject::iterator QJsonObject::insert(QLatin1StringView key, const QJsonValue &value)`

**作用与语义：**

插入一个键为`key`、值为`value`的新项。
如果已经有带有密钥`key`的项目，则该项的值被替换为`value`。
返回指向插入项的迭代器。
如果该值被`QJsonValue::Undefined`，关键字将从对象中移除。返回的迭代器随后会指向`end()`。

### `QJsonObject::iterator QJsonObject::insert(QStringView key, const QJsonValue &value)`

**作用与语义：**

插入一个键为`key`、值为`value`的新项。
如果已经有带有密钥`key`的项目，则该项的值被替换为`value`。
返回指向插入项的迭代器。
如果该值被`QJsonValue::Undefined`，关键字将从对象中移除。返回的迭代器随后会指向`end()`。

### `bool QJsonObject::isEmpty() const`

**作用与语义：**

如果对象为空，返回`true`。这与 `size()` == 0 相同。

### `[since 6.10] QJsonObject::key_value_iterator QJsonObject::keyValueBegin()`

**作用与语义：**

返回一个STL风格的迭代器，指向对象中的第一个条目。

### `[since 6.10] QJsonObject::const_key_value_iterator QJsonObject::keyValueBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向对象的第一个条目。

### `[since 6.10] QJsonObject::key_value_iterator QJsonObject::keyValueEnd()`

**作用与语义：**

返回一个STL风格的迭代子，指向对象最后一个条目之后的虚数条目。

### `[since 6.10] QJsonObject::const_key_value_iterator QJsonObject::keyValueEnd() const`

**作用与语义：**

返回一个const型STL式迭代器，指向对象最后一个条目之后的虚数条目。

### `QStringList QJsonObject::keys() const`

**作用与语义：**

返回该对象中所有键的列表。
列表按字母顺序排列。

### `qsizetype QJsonObject::length() const`

**作用与语义：**

和`size()`一样。

### `void QJsonObject::remove(const QString &key)`

**作用与语义：**

去除物体上的 `key`。

### `void QJsonObject::remove(QLatin1StringView key)`

**作用与语义：**

去除物体上的 `key`。

### `void QJsonObject::remove(QStringView key)`

**作用与语义：**

去除物体上的 `key`。

### `qsizetype QJsonObject::size() const`

**作用与语义：**

返回对象中存储的（键、值）对数。

### `[noexcept] void QJsonObject::swap(QJsonObject &other)`

**作用与语义：**

将该对象与`other`交换。此操作非常快速且从未失败。

### `QJsonValue QJsonObject::take(const QString &key)`

**作用与语义：**

移除物体上的`key`。
返回包含`key`引用值的`QJsonValue`。如果对象中不包含`key`，返回的`QJsonValue`将被`QJsonValue::Undefined`。

### `QJsonValue QJsonObject::take(QLatin1StringView key)`

**作用与语义：**

移除物体上的`key`。
返回包含`key`引用值的`QJsonValue`。如果对象中不包含`key`，返回的`QJsonValue`将被`QJsonValue::Undefined`。

### `QJsonValue QJsonObject::take(QStringView key)`

**作用与语义：**

移除物体上的`key`。
返回包含`key`引用值的`QJsonValue`。如果对象中不包含`key`，返回的`QJsonValue`将被`QJsonValue::Undefined`。

### `QVariantHash QJsonObject::toVariantHash() const`

**作用与语义：**

将该对象转换为`QVariantHash`。
返回已生成的哈希值。

### `QVariantMap QJsonObject::toVariantMap() const`

**作用与语义：**

将该对象转换为`QVariantMap`。
返回已创建的地图。

### `QJsonValue QJsonObject::value(const QString &key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
如果密钥不存在，返回的`QJsonValue` `QJsonValue::Undefined`。

### `QJsonValue QJsonObject::value(QLatin1StringView key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
如果密钥不存在，返回的`QJsonValue` `QJsonValue::Undefined`。

### `QJsonValue QJsonObject::value(QStringView key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
如果密钥不存在，返回的`QJsonValue` `QJsonValue::Undefined`。

### `[noexcept] QJsonObject &QJsonObject::operator=(QJsonObject &&other)`

**作用与语义：**

Move-assign `other`该对象。

### `[noexcept] QJsonObject &QJsonObject::operator=(const QJsonObject &other)`

**作用与语义：**

为该对象分配`other`。

### `QJsonValueRef QJsonObject::operator[](const QString &key)`

**作用与语义：**

返回 `key` 的值。如果对象中没有键 `key` 的值，则创建一个 `QJsonValue::Null` 值，然后返回。
返回值类型为`QJsonValueRef`，是`QJsonArray`和`QJsonObject`的辅助类。当你获得类型为`QJsonValueRef`的对象时，可以将其作为引用`QJsonValue`使用。如果你赋值，赋值将应用到你获得引用的`QJsonArray`或`QJsonObject`元素上。

### `QJsonValue QJsonObject::operator[](const QString &key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
这和`value()`一样。
如果密钥不存在，返回的`QJsonValue`即为`QJsonValue::Undefined`。

### `QJsonValueRef QJsonObject::operator[](QLatin1StringView key)`

**作用与语义：**

返回 `key` 的值。如果对象中没有键 `key` 的值，则创建一个 `QJsonValue::Null` 值，然后返回。
返回值类型为`QJsonValueRef`，是`QJsonArray`和`QJsonObject`的辅助类。当你获得类型为`QJsonValueRef`的对象时，可以将其作为引用`QJsonValue`使用。如果你赋值，赋值将应用到你获得引用的`QJsonArray`或`QJsonObject`元素上。

### `QJsonValueRef QJsonObject::operator[](QStringView key)`

**作用与语义：**

返回 `key` 的值。如果对象中没有键 `key` 的值，则创建一个 `QJsonValue::Null` 值，然后返回。
返回值类型为`QJsonValueRef`，是`QJsonArray`和`QJsonObject`的辅助类。当你获得类型为`QJsonValueRef`的对象时，可以将其作为引用`QJsonValue`使用。如果你赋值，赋值将应用到你获得引用的`QJsonArray`或`QJsonObject`元素上。

### `QJsonValue QJsonObject::operator[](QLatin1StringView key) const`

**作用与语义：**

返回 `key` 的值。如果对象中没有键 `key` 的值，则创建一个 `QJsonValue::Null` 值，然后返回。
返回值类型为`QJsonValueRef`，是`QJsonArray`和`QJsonObject`的辅助类。当你获得类型为`QJsonValueRef`的对象时，可以将其作为引用`QJsonValue`使用。如果你赋值，赋值将应用到你获得引用的`QJsonArray`或`QJsonObject`元素上。

### `QJsonValue QJsonObject::operator[](QStringView key) const`

**作用与语义：**

返回 `key` 的值。如果对象中没有键 `key` 的值，则创建一个 `QJsonValue::Null` 值，然后返回。
返回值类型为`QJsonValueRef`，是`QJsonArray`和`QJsonObject`的辅助类。当你获得类型为`QJsonValueRef`的对象时，可以将其作为引用`QJsonValue`使用。如果你赋值，赋值将应用到你获得引用的`QJsonArray`或`QJsonObject`元素上。

### `[noexcept] bool operator!=(const QJsonObject &lhs, const QJsonObject &rhs)`

**作用与语义：**

如果 `lhs` 对象不等于 `rhs`，则返回 `true`，否则返回 `false`。

### `[noexcept] bool operator==(const QJsonObject &lhs, const QJsonObject &rhs)`

**作用与语义：**

如果`lhs`对象等于`rhs`，返回`true`，否则`false`返回。

### `class const_iterator`

**作用与语义：**

QJsonObject：：const_iterator 类为 QJsonObject 提供了一个 STL 风格的 cont 迭代器。
`QJsonObject::const_iterator`允许你对一个`QJsonObject`进行叠加。如果你想在迭代时修改`QJsonObject`，必须用`QJsonObject::iterator`。通常在非const的`QJsonObject`上使用`QJsonObject::const_iterator`是个好习惯，除非你需要通过迭代器更改`QJsonObject`。Const迭代器速度稍快，且提高了代码的可读性。
默认的`QJsonObject::const_iterator`构造函数会创建一个未初始化的迭代器。你必须用`QJsonObject`函数如`QJsonObject::constBegin()`、`QJsonObject::constEnd()`或`QJsonObject::find()`初始化它，才能开始迭代。
多个迭代器可以用于同一个对象。不过，如果对象被修改，现有的迭代器会变得悬挂。

### `class iterator`

**作用与语义：**

QJsonObject：：iterator 类为 QJsonObject 提供了一个 STL 风格的非const 迭代器。
`QJsonObject::iterator`允许你对某个`QJsonObject`进行迭代，并修改某个特定键下存储的值（但不能修改键）。如果你想对const的某`QJsonObject`进行迭代，应该使用`QJsonObject::const_iterator`。通常在非const的`QJsonObject`上也使用`QJsonObject::const_iterator`是个好习惯，除非你需要通过迭代器更改`QJsonObject`。const迭代器速度稍快，并且提高了代码的可读性。
默认的 `QJsonObject::iterator` 构造器会创建一个未初始化的迭代器。你必须先用 `QJsonObject::begin()`、`QJsonObject::end()` 或 `QJsonObject::find()` 等`QJsonObject`函数初始化它，才能开始迭代。
多个迭代器可以用于同一个对象。然而，一旦对象被修改，现有的迭代器会变得悬浮。

### `ConstIterator`

**作用与语义：**

Qt风格的`QJsonObject::const_iterator`同义词。

### `Iterator`

**作用与语义：**

Qt风格的`QJsonObject::iterator`同义词。

### `(since 6.10) const_key_value_iterator`

**作用与语义：**

QJsonObject：：const_key_value_iterator typedef 提供了一个 STL 风格的迭代器用于 `QJsonObject`。
QJsonObject：：const_key_value_iterator 本质上与 `QJsonObject::const_iterator` 相同，区别在于运算符*() 返回的是键值对而非值。
这种类型防御是在Qt 6.10中引入的。

### `key_type`

**作用与语义：**

Typedef 用于`QString`。提供 STL 兼容性。

### `(since 6.10) key_value_iterator`

**作用与语义：**

QJsonObject：：key_value_iterator typedef 提供了一个 STL 风格的迭代器用于`QJsonObject`。
QJsonObject：：key_value_iterator 本质上与 `QJsonObject::iterator` 相同，区别在于 operator*() 返回的是键值对而非值。
这种类型防御是在Qt 6.10中引入的。

### `mapped_type`

**作用与语义：**

Typedef 用于`QJsonValue`。提供 STL 兼容性。

### `size_type`

**作用与语义：**

qsizetype 的 Typedef。为 STL 兼容性提供。

### `(since 6.10) auto asKeyValueRange() &&`

**作用与语义：**

返回一个范围对象，允许对该对象作为键值对进行循环。例如，该范围对象可以在基于范围的for循环中使用，并结合结构化绑定声明：
注意，通过这种方式获得的值是对对象中值的引用。具体来说，变更该值会修改对象本身。
当在r值上调用该方法时（例如在某个范围for循环的初始化器中创建的临时节点），物体将被捕获在该范围内。

**官方示例：**

```cpp
 QJsonObject obj{
     { "something", "is" },
     { "in", "this" },
     { "object", 42 },
 };

 for (auto [key, value] : obj.asKeyValueRange()) {
     qDebug() << key << "->" << value;
     if (key == "object")
         value = "!"; // modify the object at this key
 }
 qDebug() << obj["object"]; // QJsonValue(string, "!")
```

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

`QJsonObject` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
