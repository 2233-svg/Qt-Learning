# Qt QSharedDataPointer：为自定义值类型实现隐式共享

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSharedDataPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：带线程安全引用计数和 copy-on-write 的共享数据指针  
> 关联类型：`QSharedData`、`QExplicitlySharedDataPointer`、`QAdoptSharedDataTag`

## 1. 它解决什么问题

`QSharedDataPointer<T>` 用来实现 Qt 风格的隐式共享值类型。多个外层对象复制后先共享同一份 `T` 数据；当其中一个外层对象通过非 const 路径访问数据时，如果引用计数大于 1，指针会先复制数据再返回可写访问。

这就是 copy-on-write：

```text
复制外层值对象
    -> 只增加引用计数，数据暂时共享

其中一个对象准备写入
    -> detach
    -> 创建 T 的副本
    -> 当前对象修改自己的副本
```

它适合：

- 自定义便宜可复制的值类型；
- 数据较大、复制频繁、修改相对较少的对象；
- PImpl 数据隐藏和 ABI 隔离；
- 希望复制后逻辑上互不影响，但不想每次复制都立即深拷贝。

它不同于 `QSharedPointer<T>`。`QSharedPointer` 表示多个 owner 共同拥有同一个对象，修改通常对所有 owner 可见；`QSharedDataPointer` 通常服务于外层值语义，非 const 访问会自动分离。

## 2. 完整使用模型

先定义继承 `QSharedData` 的数据类：

```cpp
#include <QSharedData>
#include <QString>

class EmployeeData : public QSharedData
{
public:
    EmployeeData() = default;

    EmployeeData(const EmployeeData &other)
        : QSharedData(other),
          id(other.id),
          name(other.name)
    {
    }

    int id = -1;
    QString name;
};
```

再让外层值类型只保存一个 d pointer：

```cpp
#include <QSharedDataPointer>

class Employee
{
public:
    Employee()
        : d(new EmployeeData)
    {
    }

    int id() const
    {
        return d->id;          // const operator->，不 detach
    }

    void setId(int id)
    {
        d->id = id;            // 非 const operator->，必要时 detach
    }

private:
    QSharedDataPointer<EmployeeData> d;
};
```

默认复制成员通常已经足够：

```cpp
Employee first;
Employee second = first;  // 暂时共享 EmployeeData

second.setId(42);         // second 自动 detach
```

写入后 `first` 和 `second` 分别持有不同数据，符合普通值类型“修改副本不影响原值”的直觉。

## 3. 自动 detach 的触发点

以下**非 const** API 会先调用 `detach()`：

- `T *data()`；
- `T *get()`；
- `T *operator->()`；
- `T &operator*()`；
- 非 const `operator T *()`。

以下 const API 不 detach：

- `const T *data() const`；
- `const T *get() const`；
- `const T *constData() const`；
- `const T *operator->() const`；
- `const T &operator*() const`；
- `operator const T *() const`。

detach 由 C++ 重载选择触发，不会分析你最终是否真的写入：

```cpp
QSharedDataPointer<Data> d(new Data);
auto copy = d;

inspect(d.data()); // d 是非 const，data() 会先 detach，即使 inspect 只读
```

纯读取时应保持 const：

```cpp
inspect(d.constData());

const auto &readOnly = d;
inspect(readOnly.data());
```

这既避免无意义的深拷贝，也能让接口明确表达只读意图。

## 4. `detach()` 的语义

当数据为空或引用计数正好为 1 时，`detach()` 不复制。引用计数不是 1 时，它调用 `clone()` 创建新的 `T`，让当前包装器改指向副本：

```cpp
QSharedDataPointer<Data> first(new Data);
QSharedDataPointer<Data> second = first;

second.detach();

Q_ASSERT(first.data() != second.data());
```

上面的断言写法本身会对非 const `first.data()` 和 `second.data()` 调用 detach；由于两者已经独占，不会再次复制。若只想观察地址，使用 `constData()` 更清晰。

默认 `clone()` 相当于：

```cpp
return new T(*d);
```

因此 `T` 的复制构造函数决定 detach 后的业务状态。复制构造遗漏字段、浅拷贝独占裸资源或错误复制内部 owner，都会直接破坏外层值语义。

## 5. 实际使用场景

### 5.1 读多写少的大型值对象

配置快照、解析结果、文档元数据和图形描述对象常常被大量传值，但真正修改次数不多。隐式共享可以让复制只增加引用计数，直到首次写入才承担深拷贝成本。

### 5.2 PImpl 与头文件隔离

```cpp
class DocumentData;

class Document
{
public:
    Document();
    Document(const Document &);
    Document &operator=(const Document &);
    ~Document();

private:
    QSharedDataPointer<DocumentData> d;
};
```

私有数据类可以只定义在 `.cpp` 或私有头文件中。外层类需要实例化共享数据指针析构、复制等操作的成员函数，应放在 `DocumentData` 完整可见的位置。

### 5.3 Qt 容器中的自定义值

外层类只有一个 d pointer 时，可考虑用 `Q_DECLARE_TYPEINFO` 把它声明为 relocatable 类型，帮助 Qt 容器更高效地搬移元素。前提是类型确实满足宏所声明的性质，不能只为性能盲目标记。

## 6. 隐式共享与显式共享的选择

| 行为 | `QSharedDataPointer<T>` | `QExplicitlySharedDataPointer<T>` |
| --- | --- | --- |
| 复制包装器 | 共享数据并增加 ref | 共享数据并增加 ref |
| 非 const 访问 | 自动 detach | 不自动 detach |
| 修改副本默认效果 | 只影响当前外层值 | 可能影响所有共享者 |
| `detach()` | 通常自动发生，也可显式调用 | 必须由调用方决定 |
| 典型语义 | 值类型、copy-on-write | 明确共享的可变状态 |

如果“复制后修改一个对象，不应改变另一个对象”，使用 `QSharedDataPointer`。如果多个句柄本来就应该看到同一份修改，使用 `QExplicitlySharedDataPointer` 或更直接的共享对象模型。

## 7. 引用计数和所有权

### 7.1 从裸数据指针构造

```cpp
QSharedDataPointer<Data> d(new Data);
```

`new Data` 的 `QSharedData::ref` 初始为 0；普通构造会增加为 1。此后数据对象由共享数据指针体系管理，不要手工 `delete`。

### 7.2 复制和移动

复制构造、复制赋值会增加新数据的引用计数，并释放当前旧引用。移动构造、移动赋值只转移 d pointer，源对象变为空。

### 7.3 `reset()`

`reset(ptr)` 为非空 `ptr` 增加引用，然后释放旧数据引用；旧计数归零时删除旧对象。传入当前已经保存的同一地址时不会重复调整。

### 7.4 `take()` 与 adopt

Qt 6.0 起，`take()` 取出 d pointer 并清空包装器，但**不递减**返回对象的引用计数：

```cpp
Data *raw = d.take();
Q_ASSERT(!d);
```

可把这一份已经计数的引用直接交给 adopt 构造：

```cpp
QSharedDataPointer<Data> adopted(raw, QAdoptSharedDataTag{});
```

adopt 构造不会再次增加 ref。它通常只与 `take()` 或同等严格的底层引用转移协议配对，不能直接接管一个刚 `new`、ref 仍为 0 的对象。

## 8. 多态复制和 `clone()`

默认 `clone()` 使用静态类型 `T` 的复制构造。如果 d pointer 实际保存 `T` 的派生对象，默认复制可能发生切片。

需要多态复制时，可以为具体 `QSharedDataPointer<T>` 特化 protected `clone()`，转调数据基类的虚拟克隆接口：

```cpp
template <>
BaseData *QSharedDataPointer<BaseData>::clone()
{
    return d->clone();
}
```

这种设计还要求多态基类具备正确的虚析构，否则最后通过 `T *` 删除派生对象时可能产生未定义行为。普通非多态共享数据类不需要特化。

## 9. 空状态、比较与哈希

默认构造和 `reset()` 后可以为空。空指针上使用 `operator->()` 或 `operator*()` 是未定义行为：

```cpp
QSharedDataPointer<Data> d;
if (!d)
    d.reset(new Data);
```

比较运算比较的是内部 d pointer 地址，不是 `T` 的字段值：

```cpp
auto second = first;
Q_ASSERT(first == second);

second.detach();
Q_ASSERT(first != second); // 即使字段值仍完全相同
```

Qt 6.11.1 还提供与 `T *`、`nullptr` 的强序比较，以及按 d pointer 地址计算的 `qHash()`。这些操作都不会触发 detach。需要深值相等时，应为外层值类型实现字段语义的比较。

## 10. 线程边界

引用计数操作是线程安全的，因此不同线程各自复制或销毁自己的 `QSharedDataPointer` 包装器，不会破坏 ref。

但这不提供完整的数据并发安全：

- 同一个包装器变量不能被多个线程无锁读写；
- `T` 的业务字段仍可能发生数据竞争；
- 一个线程正在复制 `T`，另一个线程同时修改同一份 `T`，仍可能竞争；
- 自动 detach 只提供值语义，不是互斥锁或事务。

最稳妥的用法是把外层对象作为值在线程边界上传递，并避免多个线程同时修改同一个外层实例。若必须共享可变数据，增加专门同步。

## 11. 常见错误

### 11.1 只读代码走非 const API

非 const `data()` / `get()` / 解引用会自动 detach。只读路径使用 `constData()` 或 const 包装器。

### 11.2 数据类没有正确复制构造

detach 依赖 `T(*oldData)`。所有需要保留的业务状态都必须正确复制。

### 11.3 把它当作 QSharedPointer

`QSharedDataPointer` 的非 const 访问会分裂数据，目标通常是值语义。真正需要共同修改一个对象时不要使用隐式共享。

### 11.4 手工删除 data() 返回值

d pointer 由引用计数管理。手工删除会让其他包装器持有悬空指针。

### 11.5 错误使用 QAdoptSharedDataTag

adopt 要求指针已经携带一份待转移的有效 ref。普通 `new T` 应使用不带 tag 的构造。

### 11.6 以为原子 ref 保护所有数据

引用计数线程安全不等于业务字段线程安全。

## 12. 逐项 API 语义

### 成员类型

#### `using Type = T`

表示共享数据对象类型。内部 d pointer 指向 `T`。

#### `using pointer = T *`

表示数据对象指针类型，供泛型代码使用。

### 构造、析构与赋值

#### `QSharedDataPointer()`

构造空 d pointer。

#### `explicit QSharedDataPointer(T *data)`

保存 `data` 并增加其引用计数。`data` 通常是动态创建的 `QSharedData` 派生对象。

#### `QSharedDataPointer(T *data, QAdoptSharedDataTag)`

Qt 6.0 起，不增加 ref 地接管一份已经计数的共享引用。通常与 `take()` 配对。

#### `QSharedDataPointer(const QSharedDataPointer<T> &o)`

复制 d pointer 并增加共享数据引用计数，不深拷贝 `T`。

#### `QSharedDataPointer(QSharedDataPointer<T> &&o)`

移动 d pointer，源对象变为空，不额外增减同一数据的 ref。

#### `~QSharedDataPointer()`

减少共享数据引用计数。计数归零时删除 `T`。

#### `operator=(const QSharedDataPointer<T> &o)`

共享 `o` 的数据并正确更新新旧引用计数，不立即深拷贝。

#### `operator=(QSharedDataPointer<T> &&other)`

移动赋值，接收 d pointer，源对象变为空。

#### `operator=(T *o)`

切换到 `o`，增加新对象 ref，减少旧对象 ref；旧计数归零时删除旧对象。

### 访问与分离

#### `detach()`

引用计数不是 1 时，通过 `clone()` 创建副本并让当前指针独占新数据。空指针时不复制。非 const 访问 API 会自动调用它。

#### `clone()`

protected 扩展点。默认执行 `new T(*d)`，供 detach 创建深拷贝；多态数据可通过模板特化转调虚拟 clone。

#### `data()`

返回可写 `T *`，调用前会自动 detach。即使调用方最终只读，也可能产生深拷贝。

#### `data() const`

返回 `const T *`，不 detach。

#### `get()`

Qt 6.0 起，与非 const `data()` 相同，先 detach 再返回可写指针。

#### `get() const`

Qt 6.0 起，与 const `data()` 相同，不 detach。

#### `constData() const`

返回 `const T *`，明确表示只读且不 detach。

#### `operator T *()`

非 const 指针转换，先 detach。隐式转换可能隐藏复制成本，命名访问 API 通常更清晰。

#### `operator const T *() const`

const 指针转换，不 detach。

#### `operator*()`

先 detach，再返回可写 `T &`。空指针上使用是未定义行为。

#### `operator*() const`

返回 `const T &`，不 detach。空指针上使用是未定义行为。

#### `operator->()`

先 detach，再返回可写 `T *`。

#### `operator->() const`

返回 `const T *`，不 detach。

### 所有权操作

#### `reset(T *ptr = nullptr)`

Qt 6.0 起替换 d pointer，正确增加新数据 ref、减少旧数据 ref。默认参数可清空指针。

#### `take()`

Qt 6.0 起取出 d pointer 并清空当前包装器，但不减少返回对象的 ref。调用者必须接管这份已有共享引用，通常使用 adopt 构造。

#### `swap(QSharedDataPointer<T> &other)`

快速交换两个 d pointer，不复制数据、不调整总引用数量。

#### `operator bool() const`

d pointer 非空时返回 `true`。

#### `operator!() const`

d pointer 为空时返回 `true`。

### 相关非成员 API

#### `swap(lhs, rhs)`

调用成员 `swap()`，交换两个共享数据指针。

#### 比较与排序运算

比较两个 `QSharedDataPointer`、d pointer 与 `T *`、或与 `nullptr` 的地址关系。不会 detach，也不比较数据字段。

#### `qHash(pointer, seed)`

按内部 d pointer 地址计算哈希，不会 detach。内容相同但数据副本不同的两个指针可能有不同哈希。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Type` / `pointer` | 表示 `T` 和 `T *`。 | 只是类型别名。 |
| 构造 | `QSharedDataPointer()` | 创建空 d pointer。 | 解引用前检查或初始化。 |
| 构造 | `QSharedDataPointer(T *)` | 建立一份共享引用。 | 会增加 ref；对象之后由共享体系管理。 |
| 接管 | `QSharedDataPointer(T *, QAdoptSharedDataTag)` | 接管已计数引用。 | Qt 6.0 起；不要直接 adopt 普通 `new T`。 |
| 复制 | `QSharedDataPointer(other)` | 共享数据并增加 ref。 | 不立即深拷贝。 |
| 移动 | `QSharedDataPointer(std::move(other))` | 转移 d pointer。 | 源对象变空。 |
| 析构 | `~QSharedDataPointer()` | 减少 ref，归零时删除数据。 | 不要手工删除 d pointer。 |
| 分离 | `detach()` | 必要时深拷贝并独占。 | 非 const 访问会自动调用。 |
| 克隆 | `clone()` | 为 detach 创建数据副本。 | protected；默认使用 `T` 复制构造。 |
| 可写访问 | `data()` / `get()` | 返回可写指针。 | 会先 detach；`get()` 自 Qt 6.0 起。 |
| 只读访问 | `data() const` / `get() const` / `constData()` | 返回只读指针。 | 不 detach。 |
| 可写解引用 | 非 const `operator*` / `operator->` | 访问可写数据。 | 会先 detach；空时行为未定义。 |
| 只读解引用 | const `operator*` / `operator->` | 访问只读数据。 | 不 detach。 |
| 替换 | `reset(ptr)` | 切换共享数据对象。 | Qt 6.0 起；正确更新新旧 ref。 |
| 取出 | `take()` | 取出指针但保留其引用计数。 | Qt 6.0 起；通常与 adopt 构造配对。 |
| 交换 | `swap()` / `swap(lhs, rhs)` | 交换 d pointer。 | 不复制 `T`。 |
| 空判断 | `operator bool()` / `operator!()` | 判断 d pointer 状态。 | 空指针不能解引用。 |
| 比较 | 比较与排序运算 | 比较 d pointer 地址。 | 不比较内容，也不 detach。 |
| 哈希 | `qHash()` | 按 d pointer 地址哈希。 | 内容相等不保证哈希相等。 |

---

### 一句话总结

`QSharedDataPointer` 让自定义类获得 Qt 风格的隐式共享：复制只增加引用计数，非 const 访问必要时自动 detach；正确性取决于 `T` 的复制构造、严格的 ref 所有权，以及只读代码是否真正走 const 路径。
