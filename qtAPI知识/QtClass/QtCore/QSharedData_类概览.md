# Qt QSharedData：隐式共享数据对象的引用计数基类

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSharedData>`  
> 所属模块：`Qt6::Core`  
> 类型性质：供共享私有数据类继承的轻量基类  
> 关联类型：`QSharedDataPointer`、`QExplicitlySharedDataPointer`

## 1. 它解决什么问题

`QSharedData` 为自定义共享数据对象提供一个原子引用计数成员。数据类继承它后，可以交给：

- `QSharedDataPointer<T>` 实现隐式共享和 copy-on-write；
- `QExplicitlySharedDataPointer<T>` 实现引用计数共享，并由调用方显式决定何时复制。

典型目标是让一个外层业务类表现为便宜可复制的值类型：

```cpp
class DocumentData : public QSharedData
{
public:
    QString title;
    QByteArray content;
};

class Document
{
    QSharedDataPointer<DocumentData> d;
};
```

复制 `Document` 时只复制 d pointer 并增加引用计数；真正修改共享数据时，`QSharedDataPointer` 才创建副本。

`QSharedData` 自己不是完整的智能指针，也不会自动调用 copy-on-write。它只提供共享数据对象内部所需的引用计数基础设施。

## 2. 引用计数模型

`QSharedData` 公开保存：

```cpp
mutable QAtomicInt ref;
```

默认构造和复制构造都会把新对象的 `ref` 初始化为 `0`。真正将数据对象交给普通 `QSharedDataPointer<T>(data)` 构造时，指针才会建立第一份引用：

```text
new DocumentData                 ref == 0
QSharedDataPointer(data)         ref == 1
复制 QSharedDataPointer          ref == 2
一个指针析构                     ref == 1
最后一个指针析构                 ref == 0，然后删除数据对象
```

应用代码通常不应直接调用 `ref.ref()` 或 `ref.deref()`。这些计数操作应由共享数据指针统一管理，否则实际 owner 数量和计数可能失配。

## 3. 数据类的正确写法

```cpp
#include <QSharedData>
#include <QString>

class DocumentData : public QSharedData
{
public:
    DocumentData() = default;

    DocumentData(const DocumentData &other)
        : QSharedData(other),
          title(other.title),
          content(other.content)
    {
    }

    QString title;
    QByteArray content;
};
```

复制构造函数必须复制业务字段。调用 `QSharedData(other)` 不会复制旧引用计数，而是为新副本建立 `ref == 0` 的独立计数状态。

这正是 detach 所需的语义：副本是一个新的数据对象，不能继承原对象已有的 owner 数量。

## 4. 为什么复制时引用计数必须归零

假设原数据已由三个外层对象共享：

```text
原数据 ref == 3
```

copy-on-write 创建新数据时，新副本还没有被任何指针正式接管。如果复制构造把 `3` 一起复制，新对象的计数会虚构出三个不存在的 owner，最终无法正确删除。

因此：

```cpp
QSharedData(const QSharedData &) noexcept
    : ref(0)
{
}
```

构造参数中的基类部分会被忽略。只有派生类的业务字段需要复制。

## 5. 赋值为何被禁用

Qt 6.11.1 的 `QSharedData` 删除了复制赋值：

```cpp
QSharedData &operator=(const QSharedData &) = delete;
```

直接给基类赋值会让引用计数语义变得危险。派生数据类若需要赋值，应只复制自己的业务字段，不能覆盖基类中的 `ref`：

```cpp
DocumentData &DocumentData::operator=(const DocumentData &other)
{
    if (this == &other)
        return *this;

    title = other.title;
    content = other.content;
    return *this;
}
```

不过多数隐式共享数据对象只需要复制构造供 `clone()` 使用，并不需要公开赋值操作。

## 6. 实际使用场景

### 6.1 自定义隐式共享值类型

`QSharedData` 最典型的用途，是把较大的私有状态移到共享数据对象中，使外层类复制便宜，同时保持修改后的值语义。

### 6.2 PImpl 与 ABI 隔离

公共头文件只前置声明私有数据类，并保存 `QSharedDataPointer<Private>`，可以减少实现细节暴露和头文件依赖。相关构造、析构和复制成员通常在私有类型完整可见的 `.cpp` 中定义。

### 6.3 显式共享可变状态

如果多个外层对象应继续看到同一份修改，可以把 `QSharedData` 派生类交给 `QExplicitlySharedDataPointer`。此时非 const 访问不会自动 detach。

## 7. 线程边界

`QSharedData` 提供线程安全的引用计数。不同线程各自复制和销毁自己的共享数据指针时，计数增减不会因普通数据竞争而损坏。

这不意味着派生数据类的业务字段线程安全：

- `ref` 的原子性只保护计数；
- `title`、`content` 等成员仍可能发生数据竞争；
- 同一个外层包装对象被多个线程同时写入仍需同步；
- copy-on-write 不等于任意并发写入安全。

常见可靠模式是在线程之间传递值对象副本，然后把每个副本当作各自线程拥有的值；一旦某个线程准备修改，其非 const 访问会先 detach。即便如此，跨线程传递和同时写同一个包装对象仍要遵守外层类型自己的同步契约。

## 8. 生命周期和析构边界

`QSharedData` 的析构函数本身不负责检查引用计数。正常情况下，数据对象应只在引用计数由最后一个共享数据指针递减到零时删除。

不要：

- 对仍被共享数据指针持有的对象手工 `delete`；
- 把栈对象地址交给 `QSharedDataPointer`；
- 手工修改 `ref` 来“修复”生命周期；
- 对刚 `new` 且 `ref == 0` 的对象错误使用 `QAdoptSharedDataTag`。

`QAdoptSharedDataTag` 只接管一份已经计入 `ref` 的有效引用，通常与 `take()` 配对使用。

## 9. 常见错误

### 9.1 忘记继承 QSharedData

`QSharedDataPointer<T>` 需要通过 `T::ref` 管理引用。普通数据类没有这套契约。

### 9.2 复制构造遗漏业务字段

detach 默认使用 `new T(*d)`。复制构造不完整会让分离后的值丢失状态。

### 9.3 试图复制 ref

新副本必须从 `ref == 0` 开始。不要在派生复制构造中手工复制引用计数。

### 9.4 直接操作 ref

引用计数和实际包装器数量必须一致。除实现底层共享指针机制外，不应手工增减。

### 9.5 把引用计数线程安全当作数据线程安全

原子 `ref` 只保证生命周期计数，不保护派生类字段。

## 10. 逐项 API 语义

### `QSharedData() noexcept`

构造共享数据基类，并把引用计数初始化为 `0`。此时对象还没有被普通共享数据指针正式持有。

### `QSharedData(const QSharedData &) noexcept`

为一个数据副本构造基类，参数中的原引用计数被忽略，新对象的 `ref` 仍初始化为 `0`。派生类复制构造应另外复制自己的业务字段。

### `QSharedData &operator=(const QSharedData &) = delete`

禁止复制赋值基类，避免覆盖正在使用中的引用计数。派生类若实现赋值，只处理自身业务成员。

### `~QSharedData()`

销毁基类。正常情况下由共享数据指针在引用计数归零后删除完整派生对象；不要手工销毁仍被引用的数据。

### `mutable QAtomicInt ref`

保存共享数据对象的原子引用计数。`mutable` 允许 const 包装操作调整生命周期计数。它是共享指针实现契约的一部分，不是普通业务 API。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSharedData()` | 创建引用计数为 0 的共享数据基类。 | 第一份引用由普通共享数据指针构造建立。 |
| 复制构造 | `QSharedData(const QSharedData &)` | 为数据副本建立独立计数。 | 忽略源 ref，新对象仍从 0 开始。 |
| 赋值 | `operator=` | 禁止给基类复制赋值。 | 派生赋值不能覆盖 ref。 |
| 析构 | `~QSharedData()` | 销毁引用计数基类。 | 通常由最后一个共享数据指针触发完整对象删除。 |
| 计数 | `ref` | 保存原子引用计数。 | 不要在普通业务代码中手工增减。 |
| 隐式共享 | `QSharedDataPointer<T>` | 自动 copy-on-write。 | 非 const 访问可能 detach。 |
| 显式共享 | `QExplicitlySharedDataPointer<T>` | 引用计数共享。 | 修改前是否 detach 由调用方决定。 |

---

### 一句话总结

`QSharedData` 是 Qt 自定义共享数据对象的引用计数基类：默认和复制构造都从 `ref == 0` 开始，计数由共享数据指针管理；它只保证引用计数安全，不保证派生数据字段的线程安全。
