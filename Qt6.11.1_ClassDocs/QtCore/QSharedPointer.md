# QSharedPointer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“SharedPointer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSharedPointer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSharedPointer>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
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

- `QSharedPointer()`
- `QSharedPointer(QSharedPointer<X> &&other)`
- `QSharedPointer(X *ptr)`
- `QSharedPointer(const QWeakPointer<T> &other)`
- `QSharedPointer(std::nullptr_t)`
- `QSharedPointer(X *ptr, Deleter d)`
- `QSharedPointer(std::nullptr_t, Deleter d)`
- `QSharedPointer(const QSharedPointer<T> &other)`
- `QSharedPointer(QSharedPointer<T> &&other)`
- `~QSharedPointer()`
- `void clear()`
- `QSharedPointer<X> constCast() const &`
- `(since 6.9) QSharedPointer<X> constCast() &&`
- `T * data() const`
- `QSharedPointer<X> dynamicCast() const &`
- `(since 6.9) QSharedPointer<X> dynamicCast() &&`
- `T * get() const`
- `bool isNull() const`
- `QSharedPointer<X> objectCast() const &`
- `(since 6.9) QSharedPointer<X> objectCast() &&`
- `(since 6.7) bool owner_before(const QSharedPointer<X> &other) const`
- `(since 6.7) bool owner_before(const QWeakPointer<X> &other) const`
- `(since 6.7) bool owner_equal(const QSharedPointer<X> &other) const`
- `(since 6.7) bool owner_equal(const QWeakPointer<X> &other) const`
- `(since 6.7) size_t owner_hash() const`
- `void reset()`
- `void reset(T *t)`
- `void reset(T *t, Deleter deleter)`
- `QSharedPointer<X> staticCast() const &`
- `(since 6.9) QSharedPointer<X> staticCast() &&`
- `void swap(QSharedPointer<T> &other)`
- `QWeakPointer<T> toWeakRef() const`
- `operator bool() const`
- `bool operator!() const`
- `T & operator*() const`
- `T * operator->() const`
- `QSharedPointer<T> & operator=(QSharedPointer<T> &&other)`
- `QSharedPointer<T> & operator=(QSharedPointer<X> &&other)`
- `QSharedPointer<T> & operator=(const QSharedPointer<T> &other)`
- `QSharedPointer<T> & operator=(const QWeakPointer<T> &other)`

### 静态公有成员

- `QSharedPointer<T> create(Args &&... args)`

### 相关非成员函数

- `size_t qHash(const QSharedPointer<T> &key, size_t seed = 0)`
- `QSharedPointer<X> qSharedPointerCast(const QSharedPointer<T> &other)`
- `(since 6.9) QSharedPointer<X> qSharedPointerCast(QSharedPointer<T> &&other)`
- `QSharedPointer<X> qSharedPointerCast(const QWeakPointer<T> &other)`
- `QSharedPointer<X> qSharedPointerConstCast(const QSharedPointer<T> &src)`
- `(since 6.9) QSharedPointer<X> qSharedPointerConstCast(QSharedPointer<T> &&src)`
- `QSharedPointer<X> qSharedPointerConstCast(const QWeakPointer<T> &src)`
- `QSharedPointer<X> qSharedPointerDynamicCast(const QSharedPointer<T> &src)`
- `(since 6.9) QSharedPointer<X> qSharedPointerDynamicCast(QSharedPointer<T> &&src)`
- `QSharedPointer<X> qSharedPointerDynamicCast(const QWeakPointer<T> &src)`
- `QSharedPointer<X> qSharedPointerObjectCast(const QSharedPointer<T> &src)`
- `(since 6.9) QSharedPointer<X> qSharedPointerObjectCast(QSharedPointer<T> &&src)`
- `QSharedPointer<X> qSharedPointerObjectCast(const QWeakPointer<T> &src)`
- `std::shared_ptr<X> qSharedPointerObjectCast(const std::shared_ptr<T> &src)`
- `std::shared_ptr<X> qSharedPointerObjectCast(std::shared_ptr<T> &&src)`
- `std::shared_ptr<X> qobject_pointer_cast(const std::shared_ptr<T> &src)`
- `std::shared_ptr<X> qobject_pointer_cast(std::shared_ptr<T> &&src)`
- `bool operator!=(const QSharedPointer<T> &lhs, const QSharedPointer<X> &rhs)`
- `bool operator!=(const QSharedPointer<T> &lhs, const X *rhs)`
- `bool operator!=(const QSharedPointer<T> &lhs, std::nullptr_t)`
- `bool operator!=(const T *lhs, const QSharedPointer<X> &rhs)`
- `bool operator!=(std::nullptr_t, const QSharedPointer<T> &rhs)`
- `QDebug operator<<(QDebug debug, const QSharedPointer<T> &ptr)`
- `bool operator==(const QSharedPointer<T> &lhs, const QSharedPointer<X> &rhs)`
- `bool operator==(const QSharedPointer<T> &lhs, const X *rhs)`
- `bool operator==(const QSharedPointer<T> &lhs, std::nullptr_t)`
- `bool operator==(const T *lhs, const QSharedPointer<X> &rhs)`
- `bool operator==(std::nullptr_t, const QSharedPointer<T> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSharedPointer::QSharedPointer()`

**作用与语义：**

创建一个空的QSharedPoint （对象持有对`nullptr`的引用）。

### `[noexcept] template <typename X> QSharedPointer::QSharedPointer(QSharedPointer<X> &&other)`

**作用与语义：**

Move构建一个QSharedPointer实例，使其指向`other`指向的同一个对象。
只有当`X*`隐式转换为`T*`时，才参与重载决议。

### `[explicit] template <typename X> QSharedPointer::QSharedPointer(X *ptr)`

**作用与语义：**

创建指向`ptr`的QSharedPointer。指针`ptr`由该QSharedPointer管理，且不得传递给其他QSharedPointer对象或在该对象外部删除。
自Qt 5.8起，当对该QSharedPointer的最后一次引用被销毁时，`ptr`将通过调用`X`的解构器被删除（即使`X`与QSharedPointer的模板参数`T`不同）。此前，`T`的重构器被调用。

### `QSharedPointer::QSharedPointer(const QWeakPointer<T> &other)`

**作用与语义：**

通过将弱引用 `other` 提升为强引用并共享其指针，创建 QSharedPointer。
如果`T`是该类模板参数的派生类型，QSharedPointer 会自动执行 cast。否则，编译器会出错。

### `QSharedPointer::QSharedPointer(std::nullptr_t)`

**作用与语义：**

创建一个空的 QSharedPointer。这相当于 QSharedPointer 的默认构造函数。

### `template <typename X, typename Deleter> QSharedPointer::QSharedPointer(X *ptr, Deleter d)`

**作用与语义：**

创建指向`ptr`的QSharedPointer。指针`ptr`由该QSharedPointer管理，且不得传递给其他QSharedPointer对象或在该对象外部删除。
删除器参数`d`指定该对象的自定义删除器。当强引用计数降至0时，调用自定义删除器代替 delete()。例如，这对于调用`QObject`上的 `deleteLater()` 非常有用：
注意，即使QSharedPointer模板参数`T`不同，自定义删除器函数也会通过指向类型`X`的指针被调用。
也可以直接指定成员函数，例如：

**官方示例：**

```cpp
 static void doDeleteLater(MyObject *obj)
 {
     obj->deleteLater();
 }

 void otherFunction()
 {
     QSharedPointer<MyObject> obj =
         QSharedPointer<MyObject>(new MyObject, doDeleteLater);

     // continue using obj
     obj.clear();    // calls obj->deleteLater();
 }
```

### `template <typename Deleter> QSharedPointer::QSharedPointer(std::nullptr_t, Deleter d)`

**作用与语义：**

创建一个空的 QSharedPointer。这相当于 QSharedPointer 的默认构造函数。
删除器参数`d`指定该对象的自定义删除器。当强引用计数降至0时，调用自定义删除器代替运算符delete()。

### `QSharedPointer::QSharedPointer(const QSharedPointer<T> &other)`

**作用与语义：**

创建一个共享`other`指针的QSharedPointer对象。
如果`T`是该类模板参数的派生类型，QSharedPoint 将自动执行 cast。否则，编译器将出现错误。

### `[noexcept] QSharedPointer::QSharedPointer(QSharedPointer<T> &&other)`

**作用与语义：**

Move-构造一个QSharedPointer实例，使其指向`other`指向的同一个对象。

### `QSharedPointer::~QSharedPointer()`

**作用与语义：**

销毁该`QSharedPointer`对象。如果它是对该指针的最后引用，也会删除该指针。

### `void QSharedPointer::clear()`

**作用与语义：**

清除该`QSharedPointer`对象，丢弃它可能指向指针的引用。如果这是最后一个引用，那么指针本身将被删除。

### `template <typename X> QSharedPointer<X> QSharedPointer::constCast() const &`

**作用与语义：**

从该指针类型`const_cast`到`X`，并返回共享引用的`QSharedPointer`。该函数可用于上投和下投，但更适合上投。

### `[since 6.9] template <typename X> QSharedPointer<X> QSharedPointer::constCast() &&`

**作用与语义：**

归还的`QSharedPointer`与`*this`相同的共同所有者共同拥有所有权。
这一职能`resets` `*this`以成功`nullptr`。
注意：该功能会让`QSharedPointer::constCast()`重载。

### `[static] template <typename... Args> QSharedPointer<T> QSharedPointer::create(Args &&... args)`

**作用与语义：**

创建`QSharedPointer`对象并分配一个类型为`T`的新项。`QSharedPointer`内部和对象被分配到一个内存分配中，这有助于减少长时间运行应用中的内存碎片。
该函数将尝试调用一个类型为`T`的构造函数，该构造函数能够接受所有传递的参数（`args`）。参数将被完美转发。

### `T *QSharedPointer::data() const`

**作用与语义：**

返回该对象所引用指针的值。
注意：不要删除该函数返回的指针，也不要将其传递给可能删除该指针的其他函数，包括创建`QSharedPointer`或`QWeakPointer`对象。

### `template <typename X> QSharedPointer<X> QSharedPointer::dynamicCast() const &`

**作用与语义：**

从该指针类型对`X`进行动态投射，返回共享引用的`QSharedPointer`。如果使用该函数进行上投，`QSharedPointer`将执行`dynamic_cast`，这意味着如果该`QSharedPointer`指向的对象不是类型`X`，返回的对象将为空。
注意：模板类型`X`必须与该对象模板相同的const和volatile限定词，否则cast会失败。如果需要去掉这些限定词，请使用`constCast()`。

### `[since 6.9] template <typename X> QSharedPointer<X> QSharedPointer::dynamicCast() &&`

**作用与语义：**

归还的`QSharedPointer`与`*this`相同的共同所有者共同拥有所有权。
这个功能`resets` `*this` `nullptr`成功。
注意：该功能会让`QSharedPointer::dynamicCast()`重载。

### `T *QSharedPointer::get() const`

**作用与语义：**

和`data()`一样。
此功能是为了与`std::shared_ptr`的API兼容性而提供。

### `bool QSharedPointer::isNull() const`

**作用与语义：**

如果该对象指代 `nullptr`，返回`true`。

### `template <typename X> QSharedPointer<X> QSharedPointer::objectCast() const &`

**作用与语义：**

从该指针类型`qobject_cast()`到`X`，返回共享引用的`QSharedPointer`。如果使用该函数进行上抛，`QSharedPointer`将执行`qobject_cast`，这意味着如果该`QSharedPointer`指向的对象类型不是`X`，返回的对象为空。
注意：模板类型`X`必须与该对象模板的const和volatile限定符相同，否则cast会失败。如果需要去掉这些限定符，请使用`constCast()`。

### `[since 6.9] template <typename X> QSharedPointer<X> QSharedPointer::objectCast() &&`

**作用与语义：**

归还`QSharedPointer`与`*this`相同的共同所有者共同拥有所有权。
这个职能`resets` `*this`以成功`nullptr`。
注意：该功能会`QSharedPointer::objectCast()`重载。

### `[noexcept, since 6.7] template <typename X> bool QSharedPointer::owner_before(const QWeakPointer<X> &other) const`

**作用与语义：**

返回 `true`当且仅当该智能指针在实现定义的基于所有者的排序中先于`other`。该排序使得两个智能指针如果都是空的，或者它们都拥有同一对象（即使它们的表观类型和指针不同），则视为等价的。

### `[noexcept, since 6.7] template <typename X> bool QSharedPointer::owner_equal(const QWeakPointer<X> &other) const`

**作用与语义：**

回报`true`当且仅当该智能指针和`other`持股时才会有回报。

### `[noexcept, since 6.7] size_t QSharedPointer::owner_hash() const`

**作用与语义：**

返回基于所有者的该智能指针对象的哈希值。比较相等（如`owner_equal`）的智能指针将拥有相同的基于所有者的哈希值。

### `void QSharedPointer::reset()`

**作用与语义：**

和`clear()`一样。关于性病：：shared_ptr兼容性。

### `void QSharedPointer::reset(T *t)`

**作用与语义：**

将该`QSharedPointer`对象重置为指向`t`。等价于：

**官方示例：**

```cpp
 QSharedPointer<T> other(t); this->swap(other);
```

### `template <typename Deleter> void QSharedPointer::reset(T *t, Deleter deleter)`

**作用与语义：**

将该`QSharedPointer`对象重置为指向`t`，并使用删除器`deleter`。等价于：

**官方示例：**

```cpp
 QSharedPointer<T> other(t, deleter); this->swap(other);
```

### `template <typename X> QSharedPointer<X> QSharedPointer::staticCast() const &`

**作用与语义：**

从该指针类型执行静态投射到 `X`，并返回共享引用的`QSharedPointer`。该函数可用于上投和下投，但更适合上投。
注意：模板类型`X`必须与该对象模板相同的const和volatile限定词，否则cast会失败。如果需要去掉这些限定词，请使用`constCast()`。

### `[since 6.9] template <typename X> QSharedPointer<X> QSharedPointer::staticCast() &&`

**作用与语义：**

归还`QSharedPointer`与`*this`相同的共同所有者共同拥有所有权。
这一职能`resets` `*this`以成功`nullptr`。
注意：该功能会让`QSharedPointer::staticCast()`重载。

### `[noexcept] void QSharedPointer::swap(QSharedPointer<T> &other)`

**作用与语义：**

将共享指针实例与`other`交换。该操作非常快且从未失败。

### `QWeakPointer<T> QSharedPointer::toWeakRef() const`

**作用与语义：**

返回一个弱参考对象，该对象共享该对象所引用的指针。

### `QSharedPointer::operator bool() const`

**作用与语义：**

如果包含的指针不`nullptr`，返回`true`。该函数适用于`if-constructs`，例如：

**官方示例：**

```cpp
 if (sharedptr) { /*...*/ }
```

### `bool QSharedPointer::operator!() const`

**作用与语义：**

如果该对象指向`nullptr`，返回`true`。该函数适合用于`if-constructs`，如：

**官方示例：**

```cpp
 if (!sharedptr) { /*...*/ }
```

### `T &QSharedPointer::operator*() const`

**作用与语义：**

提供对共享指针成员的访问。
如果包含的指针是`nullptr`的，则行为未定义。

### `T *QSharedPointer::operator->() const`

**作用与语义：**

提供对共享指针成员的访问。
如果包含的指针是`nullptr`的，则行为未定义。

### `[noexcept] QSharedPointer<T> &QSharedPointer::operator=(QSharedPointer<T> &&other)`

**作用与语义：**

Move-assign `other`到该`QSharedPointer`实例。

### `[noexcept] template <typename X> QSharedPointer<T> &QSharedPointer::operator=(QSharedPointer<X> &&other)`

**作用与语义：**

Move-assign `other`到这个`QSharedPointer`实例。
只有当`X*`隐式转换为`T*`时，才参与重载决议。

### `QSharedPointer<T> &QSharedPointer::operator=(const QSharedPointer<T> &other)`

**作用与语义：**

使该对象共享`other`的指针。当前指针引用被丢弃，如果是最后一个，指针也会被删除。
如果`T`是该类模板参数的派生类型，`QSharedPointer`会执行自动铸造。否则，编译器会出错。

### `QSharedPointer<T> &QSharedPointer::operator=(const QWeakPointer<T> &other)`

**作用与语义：**

将`other`提升为强引用，并使该对象共享指向其所引用指针的引用。当前指针引用被丢弃，如果是最后一个，该指针将被删除。
如果`T`是该类模板参数的派生类型，`QSharedPointer`会自动执行cast。否则，编译器会出错。

### `[noexcept] template <typename T> size_t qHash(const QSharedPointer<T> &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerCast(const QSharedPointer<T> &other)`

**作用与语义：**

返回一个共享指针，指向`other`持有的指针，投射为类型`X`。类型 `T` 和 `X` 必须属于一个层级结构，`static_cast`才能成功。
注意`X`必须拥有与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用`qSharedPointerConstCast`来消除一致性。

### `[since 6.9] template <typename X, typename T> QSharedPointer<X> qSharedPointerCast(QSharedPointer<T> &&other)`

**作用与语义：**

归还`QSharedPointer`与`other`相同的共同所有者共同拥有所有权。
这个功能`resets` `other`用来`nullptr`成功。
注意：该函数会超载 `QSharedPointer::qSharedPointerCast`（const QSharedPointer<T> 等）。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerCast(const QWeakPointer<T> &other)`

**作用与语义：**

返回一个共享指针，指向`other`持有的指针，投射为类型`X`。类型`T`和`X`必须属于一个层级结构，才能`static_cast`成功。
`other`对象首先被转换为强引用。如果转换失败（因为它指向的对象已被删除），该函数返回空`QSharedPointer`。
注意`X`必须拥有与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用`qSharedPointerConstCast`来去除一致性。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerConstCast(const QSharedPointer<T> &src)`

**作用与语义：**

返回一个共享指针，指向`src`持有的指针，投射为类型`X`。类型`T`和`X`必须属于一个层级结构，`const_cast`才能成功。忽略`T`和`X`之间的`const`和`volatile`差异。

### `[since 6.9] template <typename X, typename T> QSharedPointer<X> qSharedPointerConstCast(QSharedPointer<T> &&src)`

**作用与语义：**

归还`QSharedPointer`与`src`相同的共同所有者共同拥有所有权。
这个功能`resets` `src`以成功`nullptr`。
注意：该函数会超载 `QSharedPointer::qSharedPointerConstCast`（const QSharedPointer<T> &src）。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerConstCast(const QWeakPointer<T> &src)`

**作用与语义：**

返回一个共享指针，指向`src`持有的指针，投射为类型`X`。类型`T`和`X`必须属于一个层级结构，`const_cast`才能成功。忽略`T`和`X`之间的 `const` 和 `volatile` 差异。
`src`对象首先被转换为强引用。如果转换失败（因为它指向的对象已被删除），该函数返回空`QSharedPointer`。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerDynamicCast(const QSharedPointer<T> &src)`

**作用与语义：**

返回一个共享指向`src`持有的指针的指针，使用动态投射类型 `X` 以获得相应类型的内部指针。如果`dynamic_cast`失败，返回的对象将为空。
注意`X`必须拥有与`T`相同的cv修饰符（`const`和`volatile`），否则代码将无法编译。使用`qSharedPointerConstCast`来去除一致性。

### `[since 6.9] template <typename X, typename T> QSharedPointer<X> qSharedPointerDynamicCast(QSharedPointer<T> &&src)`

**作用与语义：**

归还`QSharedPointer`与`src`相同的共同所有者共同拥有所有权。
这一职能`resets` `src`对成功的`nullptr`。
注意：该函数会超载 `QSharedPointer::qSharedPointerDynamicCast`（const QSharedPointer<T> & src）。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerDynamicCast(const QWeakPointer<T> &src)`

**作用与语义：**

返回一个共享指向`src`持有的指针的指针，使用动态投射方式，类型为`X`以获得相应类型的内部指针。如果`dynamic_cast`失败，返回的对象将为空。
`src`对象首先被转换为强引用。如果转换失败（因为它指向的对象已被删除），该函数也会返回空`QSharedPointer`。
注意`X`必须拥有与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用`qSharedPointerConstCast`来去除一致性。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerObjectCast(const QSharedPointer<T> &src)`

**作用与语义：**

qSharedPointerObjectCast函数用于投射共享指针。
返回一个共享指向`src`持有的指针的共享指针，使用类型`qobject_cast()` 以获得相应类型的内部指针 `X`。如果`qobject_cast`失败，返回的对象将为空。
注意`X`必须与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用`qSharedPointerConstCast`来去除一致性。

### `[since 6.9] template <typename X, typename T> QSharedPointer<X> qSharedPointerObjectCast(QSharedPointer<T> &&src)`

**作用与语义：**

返还的`QSharedPointer`与`src`相同的共同所有者共同拥有所有权。
这个功能`resets` `src` `nullptr`成功。
注意：该函数会超载 `QSharedPointer::qSharedPointerObjectCast`（const QSharedPointer<T> & src）。

### `template <typename X, typename T> QSharedPointer<X> qSharedPointerObjectCast(const QWeakPointer<T> &src)`

**作用与语义：**

qSharedPointerObjectCast函数用于投射共享指针。
返回一个共享指针指向`src`持有的指针，使用类型`qobject_cast()` 类型 到 `X` 以获得相应类型的内部指针。如果`qobject_cast`失败，返回的对象将为空。
`src`对象首先被转换为强引用。如果转换失败（因为它指向的对象已被删除），该函数也会返回空`QSharedPointer`。
注意`X`必须拥有与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用 `qSharedPointerConstCast` 来去除一致性。

### `template <typename X, typename T> std::shared_ptr<X> qSharedPointerObjectCast(const std::shared_ptr<T> &src)`

**作用与语义：**

返回一个共享指向`src`持有的指针的指针，使用类型`qobject_cast()` 类型 到 `X` 以获得相应类型的内部指针。如果`qobject_cast`失败，返回的对象将为空。
注意，`X`必须拥有与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用const_pointer_cast来消除一致性。

### `template <typename X, typename T> std::shared_ptr<X> qSharedPointerObjectCast(std::shared_ptr<T> &&src)`

**作用与语义：**

返回一个共享指针指向`src`持有的指针，使用类型 `qobject_cast()` 类型 `X` 以获得相应类型的内部指针。
如果`qobject_cast`成功，函数将返回一个有效的共享指针，`src`重置为空指针。如果`qobject_cast`失败，返回的对象将为空，且`src`不会被修改。
注意，`X`必须拥有与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用 const_pointer_cast 来去除一致性。

### `template <typename X, typename T> std::shared_ptr<X> qobject_pointer_cast(const std::shared_ptr<T> &src)`

**作用与语义：**

返回一个共享指针到`src`持有的指针。
与`qSharedPointerObjectCast()`相同。此功能是为了STL兼容性而提供。

### `template <typename X, typename T> std::shared_ptr<X> qobject_pointer_cast(std::shared_ptr<T> &&src)`

**作用与语义：**

与`qSharedPointerObjectCast()`相同。此功能旨在与STL兼容。

### `template <typename T, typename X> bool operator!=(const QSharedPointer<T> &lhs, const QSharedPointer<X> &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 指向不同的指针，则返回 `true`。
如果 `rhs` 的模板参数与 `lhs` 的不同，`QSharedPointer` 需要首先确保它们是兼容类型。它将尝试执行自动 `static_cast`，将类型 `T` 和 `X` 转换为它们的复合指针类型。如果 `rhs` 的模板参数既不是 `lhs` 的基类也不是派生类，则会出现编译器错误。

### `template <typename T, typename X> bool operator!=(const QSharedPointer<T> &lhs, const X *rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 指向不同的指针，则返回 `true`。
如果 `rhs` 的模板参数与 `lhs` 的不同，`QSharedPointer` 需要首先确保它们是兼容类型。它将尝试执行自动 `static_cast`，将类型 `T` 和 `X` 转换为它们的复合指针类型。如果 `rhs` 的模板参数既不是 `lhs` 的基类也不是派生类，则会出现编译器错误。

### `template <typename T> bool operator!=(const QSharedPointer<T> &lhs, std::nullptr_t)`

**作用与语义：**

如果`lhs`指的是有效（即非空）指针，返回`true`。

### `template <typename T, typename X> bool operator!=(const T *lhs, const QSharedPointer<X> &rhs)`

**作用与语义：**

如果指针`lhs`与`rhs`引用的指针不同，则返回`true`。
如果`rhs`的模板参数与`lhs`的不符，`QSharedPointer`首先需要确保它们的类型兼容。它会尝试执行自动`static_cast`，将`T`和`X`类型转换为复合指针类型。如果`rhs`的模板参数不是基于`lhs`的基或派生类型，编译器会出错。

### `template <typename T> bool operator!=(std::nullptr_t, const QSharedPointer<T> &rhs)`

**作用与语义：**

如果 `rhs` 指向一个有效（即非空）指针，则返回 `true`。

### `template <typename T> QDebug operator<<(QDebug debug, const QSharedPointer<T> &ptr)`

**作用与语义：**

将`ptr`追踪的指针写入调试对象 `debug` 以便调试。

### `template <typename T, typename X> bool operator==(const QSharedPointer<T> &lhs, const QSharedPointer<X> &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 指向同一个指针，则返回 `true`。
如果 `rhs` 的模板参数与 `lhs` 的不同，`QSharedPointer` 首先需要确保它们是兼容类型。它将尝试执行自动 `static_cast`，将 `T` 和 `X` 类型转换为它们的复合指针类型。如果 `rhs` 的模板参数既不是 `lhs` 的基类型也不是派生类型，则会得到编译器错误。

### `template <typename T, typename X> bool operator==(const QSharedPointer<T> &lhs, const X *rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 指向同一个指针，则返回 `true`。
如果 `rhs` 的模板参数与 `lhs` 的不同，`QSharedPointer` 首先需要确保它们是兼容类型。它将尝试执行自动 `static_cast`，将 `T` 和 `X` 类型转换为它们的复合指针类型。如果 `rhs` 的模板参数既不是 `lhs` 的基类型也不是派生类型，则会得到编译器错误。

### `template <typename T> bool operator==(const QSharedPointer<T> &lhs, std::nullptr_t)`

**作用与语义：**

如果`lhs`指`nullptr`，返回会`true`。

### `template <typename T, typename X> bool operator==(const T *lhs, const QSharedPointer<X> &rhs)`

**作用与语义：**

如果指针`lhs`与`rhs`引用的指针相同，返回`true`。
如果`rhs`的模板参数与`lhs`的不同，`QSharedPointer`首先需要确保它们的类型兼容。它会尝试执行自动的`static_cast`，将`T`和`X`类型转换为复合指针类型。如果`rhs`的模板参数不是基于`lhs`的基或派生类型，编译器会出错。

### `template <typename T> bool operator==(std::nullptr_t, const QSharedPointer<T> &rhs)`

**作用与语义：**

如果 `rhs` 指的是 `nullptr`，则返回 `true`。

### `(since 6.7) bool owner_before(const QSharedPointer<X> &other) const`

**作用与语义：**

返回 `true`当且仅当该智能指针在实现定义的基于所有者的排序中先于`other`。该排序使得两个智能指针如果都是空的，或者它们都拥有同一对象（即使它们的表观类型和指针不同），则视为等价的。

### `(since 6.7) bool owner_equal(const QSharedPointer<X> &other) const`

**作用与语义：**

回报`true`当且仅当该智能指针和`other`持股时才会有回报。

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

`QSharedPointer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
