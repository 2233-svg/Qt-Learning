# Qt QExplicitlySharedDataPointer 深入笔记

> 适用版本：Qt 6.11.1  
> 模板：`template <typename T> class QExplicitlySharedDataPointer`  
> 头文件：`#include <QExplicitlySharedDataPointer>`  
> 所属模块：`Qt6::Core`  
> 继承：`QSharedDataPointerBase`  
> 关键协作类型：`QSharedData`、`QSharedDataPointer`、`QAdoptSharedDataTag`

## 1. 它解决什么问题

`QExplicitlySharedDataPointer<T>` 是 Qt 的显式共享数据指针。它把多个指针包装器连接到同一个 `T` 数据对象，并使用线程安全的引用计数管理数据对象生命周期。

它和 `QSharedDataPointer<T>` 的核心区别只有一个，但会改变整个使用方式：

- `QSharedDataPointer` 在通过非 const 成员访问共享数据时自动执行 copy-on-write；
- `QExplicitlySharedDataPointer` **不会自动 detach**，需要调用方在准备修改前显式调用 `detach()`。

因此，显式共享更接近“带引用计数的普通指针”：

- 复制指针很便宜；
- 最后一个指针销毁时删除共享数据；
- 多个指针默认仍然指向同一份数据；
- 是否创建副本，由业务代码在明确的修改边界决定。

如果一段代码几乎每次修改前都要调用 `detach()`，通常说明 `QSharedDataPointer` 的隐式共享模型更适合它。

## 2. 数据对象的基本要求

`T` 通常继承 `QSharedData`，因为 Qt 的指针实现需要访问其中的引用计数：

```cpp
#include <QExplicitlySharedDataPointer>
#include <QSharedData>
#include <QString>
#include <utility>

class DocumentData : public QSharedData
{
public:
    DocumentData() = default;

    DocumentData(const DocumentData &other)
        : QSharedData(other),
          text(other.text)
    {
    }

    QString text;
};
```

`QSharedData` 的复制构造函数会把新对象的引用计数重新初始化为独立数据对象的状态。自定义复制构造函数时，应正确复制业务字段，并初始化 `QSharedData` 基类。

不要把栈对象地址传给 `QExplicitlySharedDataPointer`：

```cpp
DocumentData data;
QExplicitlySharedDataPointer<DocumentData> pointer(&data); // 错误
```

指针最终会在引用计数归零时销毁数据对象，因此正常用法是传入动态创建的 `T`，或使用 `reset(new T)`。

## 3. 最小可用模式

```cpp
QExplicitlySharedDataPointer<DocumentData> first(new DocumentData);
first->text = QStringLiteral("draft");

auto second = first; // first 和 second 共享同一个 DocumentData

second.detach();     // 引用计数大于 1 时深拷贝
second->text = QStringLiteral("published");

Q_ASSERT(first->text == QStringLiteral("draft"));
Q_ASSERT(second->text == QStringLiteral("published"));
```

`second->text = ...` 本身不会触发分离。真正保证 `first` 不受影响的是之前显式调用的 `second.detach()`。

如果有意让多个包装器看到同一份可变数据，则可以不调用 `detach()`；这正是显式共享和隐式 copy-on-write 的设计差异。但这种共享写入必须有清晰的业务约定，否则很容易出现一个值对象被另一个值对象意外修改的问题。

## 4. 封装成显式共享值类型

实际项目通常不会把 `QExplicitlySharedDataPointer` 直接暴露给所有调用方，而是把它作为自定义值类型的私有数据成员：

```cpp
class Document
{
public:
    Document()
        : d(new DocumentData)
    {
    }

    QString text() const
    {
        return d->text;
    }

    void setText(QString text)
    {
        d.detach();
        d->text = std::move(text);
    }

    void shareMutableStateWith(const Document &other)
    {
        d = other.d;
    }

private:
    QExplicitlySharedDataPointer<DocumentData> d;
};
```

这个类型的语义是：

- 普通复制只复制共享指针；
- `setText()` 明确表示“修改前创建自己的数据副本”；
- 如果业务代码需要多个 `Document` 共享后续修改，则可以设计专门的共享操作，而不是让所有非 const 成员函数隐式分离。

## 5. 实际使用场景

### 5.1 明确控制快照分裂

编辑器、配置快照或版本对象可能先共享一个大型数据结构，直到某个事务真正开始修改时才复制。`detach()` 可以放在事务开始处，避免每一次成员访问都隐式检查和分裂。

### 5.2 读多写少的数据对象

多个线程或多个值对象可以各自持有一个指针包装器，共享同一个只读数据快照。需要写入时，由写入方显式 `detach()`，读取方继续使用旧快照。

这里的“引用计数线程安全”只保证共享数据对象的计数更新安全，不保证 `DocumentData::text` 等业务字段可以无锁并发读写。共享只读快照和并发修改是两个不同问题。

### 5.3 需要普通指针风格访问的数据

某些底层算法希望明确地看到“当前指针指向哪份数据”，并由调用方决定何时复制。`QExplicitlySharedDataPointer` 的 `data()`、`get()` 和 `operator->()` 不会偷偷 detach，适合这类显式生命周期和显式写入边界。

## 6. 与 `QSharedDataPointer` 的核心区别

| 行为 | `QExplicitlySharedDataPointer<T>` | `QSharedDataPointer<T>` |
| --- | --- | --- |
| 复制包装器 | 增加共享数据引用计数 | 增加共享数据引用计数 |
| 非 const `operator->()` | 不自动 detach | 自动 detach |
| 非 const `operator*()` | 不自动 detach | 自动 detach |
| 非 const `data()` / `get()` | 不自动 detach | 自动 detach |
| `detach()` | 必须由调用方调用 | 可以显式调用，也会被非 const 访问自动调用 |
| 数据修改默认影响 | 可能影响所有共享者 | 先分离后只影响当前指针 |
| 适用倾向 | 显式共享、快照、事务边界 | 类值类型的隐式共享和 copy-on-write |

一个重要判断是：`const` 修饰的是包装器，不一定让共享数据变成 const。`QExplicitlySharedDataPointer` 的 `data() const` 和 `get() const` 仍返回 `T *`，`operator*() const` 仍返回 `T &`。如果需要只读指针，应使用 `constData()`。

## 7. 引用计数和生命周期

### 7.1 普通构造和复制

```cpp
QExplicitlySharedDataPointer<DocumentData> a(new DocumentData);
QExplicitlySharedDataPointer<DocumentData> b(a);
```

传入 `T *` 的构造函数会增加 `data` 的引用计数。复制构造和复制赋值也会增加新共享对象的引用计数，并减少原对象的引用计数。

当最后一个包装器销毁、重置或被替换时，引用计数归零，数据对象被删除。共享的是 `DocumentData`，不是每个 `QExplicitlySharedDataPointer` 包装器本身。

### 7.2 移动

移动构造和移动赋值转移内部指针，不需要为同一个数据对象额外创建一份共享引用。移动后的源包装器处于空状态，适合用于返回值和容器搬移。

### 7.3 `reset()`

```cpp
pointer.reset(new DocumentData);
pointer.reset();
```

`reset(ptr)` 把当前内部指针替换为 `ptr`；新指针非空时先增加其引用计数，旧数据的引用计数减少，旧数据在计数归零时删除。`reset()` 的默认参数是 `nullptr`，因此可以用来清空包装器。

### 7.4 `take()` 和 adopt tag

`take()` 返回当前数据指针，并把包装器置空，但**不会减少返回对象的引用计数**：

```cpp
auto raw = pointer.take();
Q_ASSERT(!pointer);
```

如果要把这个共享数据对象无额外原子操作地交给另一个 `QExplicitlySharedDataPointer`，可以使用 Qt 6.0 提供的 `QAdoptSharedDataTag` 构造：

```cpp
QExplicitlySharedDataPointer<DocumentData> adopted(
    raw, QAdoptSharedDataTag{});
```

adopt 构造不会递增引用计数，因为 `take()` 已经把原包装器的那一份引用转移出来。这个构造只适用于你明确知道 `raw` 来自同一套共享数据引用计数的转移场景。不能对普通 `new DocumentData` 随意使用 adopt tag，也不能在 `take()` 后直接 `delete raw` 再让其他包装器继续使用它。

## 8. 关键 API 语义与边界

### 8.1 `detach()`

当共享数据对象的引用计数大于 1 时，`detach()` 使用 `clone()` 创建深拷贝，并让当前包装器指向副本；引用计数为 1 或数据指针为空时不会复制。

```cpp
auto before = first.data();
second.detach();
auto after = second.data();

Q_ASSERT(before != after);
```

`detach()` 只复制 `T` 的业务数据。`T` 的复制构造函数必须正确实现深层资源复制或共享策略；Qt 不会替你猜测自定义裸资源该如何复制。

### 8.2 `clone()`

`clone()` 是 protected 扩展点，默认行为相当于：

```cpp
return new T(*d);
```

它由 `detach()` 在需要分裂共享数据时调用。普通数据类使用可复制的 `T` 即可；涉及多态数据或特殊复制策略时，应按 `QSharedDataPointer` 文档中的模板特化方案设计，不要在业务代码中直接调用这个 protected 函数。

### 8.3 `data()`、`get()` 和 `constData()`

- `data() const` 返回 `T *`，不会 detach；
- `get() const` 是 Qt 6.0 起提供的 STL 兼容别名，等价于 `data()`，不会 detach；
- `constData() const` 返回 `const T *`，不会 detach。

因此在 `const QExplicitlySharedDataPointer<T>` 上仍可能通过 `data()` 得到可写指针。需要表达只读访问时使用 `constData()`，或者在自定义封装类型中只暴露 const 成员。

### 8.4 `operator*` 和 `operator->`

两个运算符只提供访问，不执行 copy-on-write：

```cpp
pointer->text = QStringLiteral("changed"); // 可能直接改到所有共享者
```

访问空包装器时解引用或使用 `operator->()` 是未定义行为。先用 `operator bool()`、`operator!()` 或 `data()` 检查是否为空。

### 8.5 比较是指针身份，不是深值相等

`operator==` 和 `operator!=` 比较的是内部 `d pointer`：

实际比较：

```cpp
QExplicitlySharedDataPointer<DocumentData> first(new DocumentData);
auto second = first;

Q_ASSERT(first == second); // 同一个共享数据对象
second.detach();
Q_ASSERT(first != second); // 内容可能相同，但已是两个数据对象
```

两个独立创建、字段值恰好相同的数据对象仍然不相等。需要深值比较时，为 `T` 或外层值类型提供明确的比较函数。

### 8.6 reentrant 不等于数据字段线程安全

Qt 文档把该类标为 reentrant。引用计数的增减是线程安全的，因此不同线程各自复制、销毁各自的指针包装器是可行的。但这不意味着：

- 同一个包装器对象可以无锁地被多个线程同时修改；
- `T` 的字段可以无锁读写；
- `detach()` 与另一个线程对同一 `T` 的业务修改自动形成同步。

如果多个线程要共享可变数据，需要在 `T` 内部或外层增加同步协议。

## 9. API 逐项说明

### 成员类型

#### `using Type = T`

表示共享数据对象的类型。内部 d pointer 指向 `T`。

#### `using pointer = T *`

表示数据对象的指针类型，适合泛型代码读取。

### 构造与析构

#### `QExplicitlySharedDataPointer()`

构造空指针，内部 d pointer 为 `nullptr`。

#### `explicit QExplicitlySharedDataPointer(T *data)`

让内部 d pointer 指向 `data`，并递增 `data` 的引用计数。`data` 应是由共享数据机制管理的动态对象。

#### `QExplicitlySharedDataPointer(T *data, QAdoptSharedDataTag)`

Qt 6.0 起提供的高级构造。接管一个已经包含当前引用计数的 `data`，不再递增引用计数。通常只和 `take()` 配对。

#### `template <typename X> QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<X> &o)`

从兼容的 `QExplicitlySharedDataPointer<X>` 构造，转换兼容的数据指针并递增引用计数。

#### `QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<T> &o)`

复制构造，指向同一个数据对象并递增引用计数。

#### `QExplicitlySharedDataPointer(QExplicitlySharedDataPointer<T> &&o)`

移动构造，转移内部 d pointer，源对象变为空。

#### `~QExplicitlySharedDataPointer()`

递减共享数据的引用计数；计数归零时删除数据对象。

### 访问、分离和所有权操作

#### `const T *constData() const`

返回只读数据指针，不会 detach。空指针时返回 `nullptr`。

#### `T *data() const`

返回可写数据指针，不会 detach。即使包装器本身是 const，返回类型仍是 `T *`。

#### `T *get() const`

Qt 6.0 起提供的 STL 兼容别名，语义等同于 `data()`，不会 detach。

#### `void detach()`

引用计数大于 1 时创建 `T` 的深拷贝，并让当前包装器指向副本；不自动调用。

#### `T *clone()`

protected 函数，默认通过 `new T(*d)` 深拷贝数据，供 `detach()` 使用。普通调用方不能直接访问。

#### `void reset(T *ptr = nullptr)`

Qt 6.0 起提供。替换内部 d pointer，并正确增减新旧数据的引用计数。

#### `T *take()`

取出内部数据指针并将当前包装器置空，但不递减返回对象的引用计数。通常与 `QAdoptSharedDataTag` 配对完成所有权转移。

#### `void swap(QExplicitlySharedDataPointer<T> &other)`

交换两个包装器的内部 d pointer。操作快速且不会失败。

### 访问运算符和赋值

#### `operator bool()` / `operator!()`

判断内部 d pointer 是否非空或为空。

#### `operator*()` / `operator->()`

访问共享数据对象，不自动 detach。空指针解引用是未定义行为。

#### `operator=(T *o)`

把内部 d pointer 设为 `o`，增加新对象引用并减少旧对象引用。

#### `operator=(const QExplicitlySharedDataPointer<T> &o)`

复制共享关系，并正确更新引用计数。

#### `operator=(QExplicitlySharedDataPointer<T> &&other)`

移动共享关系，源包装器变为空。

### 相关非成员比较

`operator==` 和 `operator!=` 比较两个包装器的 d pointer 身份，也支持与 `T *` 和 `nullptr` 比较。它们不比较 `T` 的字段值，也不会因为比较而 detach。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `using Type = T` | 表示共享数据对象类型 | `T` 通常继承 `QSharedData` |
| 类型 | `using pointer = T *` | 表示数据对象指针类型 | 只是类型别名，不改变所有权 |
| 构造 | `QExplicitlySharedDataPointer()` | 创建空包装器 | `operator->`、`operator*` 之前要确认非空 |
| 构造 | `explicit QExplicitlySharedDataPointer(T *data)` | 接管 `data` 并递增引用计数 | `data` 应是动态创建且符合 `QSharedData` 机制的对象 |
| 构造 | `QExplicitlySharedDataPointer(T *data, QAdoptSharedDataTag)` | 在不递增计数的情况下接管已有共享数据引用 | 高级转移用法，通常只接 `take()` 返回值；Qt 6.0 起 |
| 构造 | `QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<T> &o)` | 复制共享关系并增加引用计数 | 共享的是数据对象，不是深拷贝 |
| 构造 | `QExplicitlySharedDataPointer(QExplicitlySharedDataPointer<T> &&o)` | 移动内部 d pointer | 移动后的源包装器为空 |
| 构造 | `QExplicitlySharedDataPointer<X> -> QExplicitlySharedDataPointer<T>` | 从兼容数据类型的包装器转换构造 | 需要 `X *` 可转换为 `T *`，并增加引用计数 |
| 析构 | `~QExplicitlySharedDataPointer()` | 减少引用计数并在归零时删除数据 | 不要再使用已经由最后一个包装器销毁的数据 |
| 访问 | `const T *constData() const` | 获取只读数据指针 | 不 detach；需要 const 访问时优先使用 |
| 访问 | `T *data() const` | 获取可写数据指针 | 不 detach；const 包装器也返回 `T *` |
| 访问 | `T *get() const` | `data()` 的 STL 兼容别名 | Qt 6.0 起；不 detach |
| 分离 | `void detach()` | 引用计数大于 1 时深拷贝并切换当前包装器 | 不会自动调用；修改前由调用方决定 |
| 扩展 | `protected T *clone()` | 为 `detach()` 创建数据副本 | 默认执行 `new T(*d)`；普通调用方不能直接调用 |
| 所有权 | `void reset(T *ptr = nullptr)` | 替换当前数据并更新引用计数 | Qt 6.0 起；传入的指针必须遵守同一共享数据协议 |
| 所有权 | `T *take()` | 取出数据并把包装器置空 | 不递减引用计数；通常与 adopt tag 配对 |
| 交换 | `void swap(QExplicitlySharedDataPointer<T> &other)` | 交换两个内部 d pointer | 快速且 `noexcept`，不复制数据 |
| 判断 | `operator bool() const` | 判断 d pointer 是否非空 | 只能说明指针状态，不说明数据字段有效 |
| 判断 | `operator!() const` | 判断 d pointer 是否为空 | 空指针不能解引用 |
| 访问运算符 | `T &operator*() const` | 访问共享数据对象 | 不 detach；const 包装器仍可能得到可写引用 |
| 访问运算符 | `T *operator->()` / `T *operator->() const` | 访问共享数据成员 | 不 detach；空包装器使用是未定义行为 |
| 指针转换 | `explicit operator T *()` / `explicit operator const T *() const` | 显式转换为数据指针 | 不执行隐式 copy-on-write；优先使用命名访问 API |
| 赋值 | `operator=(T *o)` | 替换为裸数据指针并更新计数 | 不要传入栈对象或不属于共享数据机制的指针 |
| 赋值 | `operator=(const QExplicitlySharedDataPointer<T> &o)` | 复制共享关系 | 不会深拷贝数据 |
| 赋值 | `operator=(QExplicitlySharedDataPointer<T> &&other)` | 移动共享关系 | 源包装器变为空 |
| 比较 | `operator==` / `operator!=` | 比较内部 d pointer 身份 | 不是深值相等，不会触发 detach |
| 比较 | 与 `T *` / `nullptr` 比较 | 判断是否指向指定数据或为空 | 只比较指针身份 |

## 11. 一句话总结

`QExplicitlySharedDataPointer<T>` 用线程安全引用计数共享 `QSharedData` 派生对象，但不会自动 copy-on-write；明确修改边界时调用 `detach()`，需要只读访问时用 `constData()`，并把 `take()` 与 adopt tag 仅用于真实的共享引用转移。
