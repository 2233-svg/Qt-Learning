# QAdoptSharedDataTag 深入笔记

> 适用版本：Qt 6.0 及之后（本文按 Qt 6.11.1 编写）  
> 头文件：`#include <QAdoptSharedDataTag>`  
> 模块：`Qt6::Core`  
> 定位：隐式共享实现中的“接管已有共享引用”标记类型

## 它解决什么问题

`QAdoptSharedDataTag` 不是一个保存数据的容器，也不是通常意义上的智能指针。它是一个空的 tag 类型，用来告诉 `QSharedDataPointer<T>` 或 `QExplicitlySharedDataPointer<T>`：

> 传入的 `T *` 已经代表一个有效的共享引用；请直接接管它，不要再给引用计数加一。

Qt 的隐式共享类型通常把真正的数据放在继承 `QSharedData` 的私有数据对象中，再通过 `QSharedDataPointer<T>` 管理。普通指针构造会建立一个新的共享引用：

```cpp
QSharedDataPointer<T> pointer(data); // 内部会对 data->ref 做 ref()
```

而带 `QAdoptSharedDataTag` 的构造不增加引用计数：

```cpp
QSharedDataPointer<T> pointer(data, QAdoptSharedDataTag{});
```

这解决的是实现内部的“引用已经建立，现在只转移这一个引用的归属”问题。它能少一次原子引用计数操作，更重要的是准确表达所有权正在转移，而不是复制一份共享所有权。

对绝大多数应用代码而言，你不会直接使用它。它面向实现 Qt 风格隐式共享类、封装共享数据工厂或维护底层库的人。

## 先理解 `QSharedData` 的引用计数

典型数据类如下：

```cpp
#include <QSharedData>
#include <QSharedDataPointer>

class DocumentData : public QSharedData
{
public:
    QString title;
};

class Document
{
public:
    Document() : d(new DocumentData) {}

private:
    QSharedDataPointer<DocumentData> d;
};
```

`new DocumentData` 刚创建时，`QSharedData::ref` 的初始值是 `0`。普通的 `QSharedDataPointer<DocumentData>(new DocumentData)` 构造会把它增加为一个有效引用；之后复制 `Document` 时会继续增加引用，最后一个指针析构时再递减到零并删除数据。

因此，下面是正常的公共代码写法：

```cpp
QSharedDataPointer<DocumentData> d(new DocumentData);
```

不要为了“看起来更高效”而改成：

```cpp
// 错误示例：刚 new 出来的 DocumentData 的 ref 初始为 0。
QSharedDataPointer<DocumentData> d(
    new DocumentData, QAdoptSharedDataTag{});
```

后者跳过了本应建立的第一个引用。随后析构时会递减一个并不存在的引用，引用计数和真实所有权不再对应，结果可能是泄漏、过早销毁或悬挂访问。`QAdoptSharedDataTag` 的正确前提是：调用方确实持有一个已经反映在 `ref` 中、现在要移交给指针对象的引用。

## 它在什么场景出现

### 1. 隐式共享类的底层实现

某段底层代码已经创建或拿到一个“带一个有效引用”的 `T *`，接下来需要把这份引用转入 `QSharedDataPointer<T>`。此时普通构造会多加一次引用，接管构造则保持计数不变。

这是一种**所有权转移**，不是借用。转移后，原来的生产者不能再按“自己仍有一份引用”来释放或递减它。

### 2. `QSharedDataPointer` 与 `QExplicitlySharedDataPointer` 的通用实现

两个指针类都支持该 tag，因为它们都管理继承 `QSharedData` 的对象，但复制时机不同：

- `QSharedDataPointer<T>`：写入时会自动 detach，适合值语义对象。
- `QExplicitlySharedDataPointer<T>`：不会自动 detach，需要调用者显式决定何时 `detach()`。

不论采用哪一种指针，`QAdoptSharedDataTag` 的含义都一样：不递增计数，直接接管已有的一份共享引用。

### 3. 库内部避免多余的 ref/deref 配对

在精确控制创建、克隆和转移流程的内部代码中，先加引用再立刻交给另一个所有者会造成没有语义价值的 `ref()` / `deref()` 配对。tag 构造可以省掉它，但只有在引用计数契约被完整证明时才值得使用。

## 这个类型本身有什么

Qt 头文件中的定义非常小：

```cpp
struct QAdoptSharedDataTag {
    explicit constexpr QAdoptSharedDataTag() = default;
};
```

它没有成员变量、没有运行时状态，也不会自己修改引用计数。真正的行为发生在接收该 tag 的两个指针构造函数中。`explicit` 表示不能把无关值隐式转换成 tag；`constexpr` 表示它可在常量表达式上下文构造。

文档说明这个 struct 的函数是线程安全的。这里的含义仅限 tag 对象自身没有共享可变状态；它不等于你可以无条件在多个线程并发读写同一个共享数据对象。数据本身的线程安全仍取决于 `T` 的实现和外部同步。

## 正确性检查清单

在使用 tag 构造前，至少确认以下问题：

1. `T` 继承自 `QSharedData`，并且指针确实由与该共享数据模型兼容的方式创建。
2. 当前引用计数中已经有且只有一份“准备移交给这个指针对象”的有效引用。
3. 转移完成后，旧持有者不会再次对同一份引用做 `deref()`，也不会把它当作仍由自己拥有。
4. 没有把普通 `new T` 得到、引用计数仍为 `0` 的裸指针直接 adopt。
5. 如果数据可能跨线程访问，另行设计读写同步；引用计数正确不代表业务数据线程安全。

若无法逐条确认，使用普通 `QSharedDataPointer<T>(data)` 构造，或者重新设计接口让所有权更清晰。这个 tag 的价值是表达一个已经成立的底层契约，不是替应用代码“自动修复”所有权。

## 它和相关类型如何配合

```text
QSharedData
  └─ YourData
       ├─ QSharedDataPointer<YourData>
       └─ QExplicitlySharedDataPointer<YourData>
              └─ 可用 QAdoptSharedDataTag 接管已有共享引用
```

- `QSharedData`：提供原子引用计数成员 `ref`，是共享私有数据类的基类。
- `QSharedDataPointer<T>`：隐式共享指针；非 const 写访问可能自动分离数据。
- `QExplicitlySharedDataPointer<T>`：显式共享指针；是否分离由调用者决定。
- `QAdoptSharedDataTag`：只影响上述两个指针的特定构造路径，不改变它们之后的复制、析构和 detach 规则。

## 常见误区

- 把它理解成“接管裸指针并负责 `delete`”。它接管的是**一份已计入引用计数的共享所有权**，不是普通独占裸指针。
- 直接将 `new T` 与 tag 一起传入。普通新对象通常还没有任何引用，应使用不带 tag 的构造。
- 以为 tag 能绕过 `QSharedDataPointer` 的 detach 行为。它只影响构造时是否 `ref()` 一次，之后的语义不变。
- 因为 tag 自身线程安全，就忽略共享数据的并发读写。引用计数与数据竞争是两件不同的事。
- 把它暴露为普通业务 API 的默认选项。多数调用者无法验证引用计数前提，接口应优先提供更安全的普通构造或工厂函数。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAdoptSharedDataTag()` | 构造一个无状态标记对象，选择“接管已有共享引用”的构造重载。 | 仅是语义标记，不会自行增加引用计数。 |
| 相关构造 | `QSharedDataPointer<T>(T *data, QAdoptSharedDataTag)` | 让隐式共享指针直接接管 `data` 所代表的一份已有共享引用。 | `data->ref` 必须已包含这份待转移引用；不要对普通 `new T` 直接使用。 |
| 相关构造 | `QExplicitlySharedDataPointer<T>(T *data, QAdoptSharedDataTag)` | 让显式共享指针直接接管 `data` 所代表的一份已有共享引用。 | 不会自动建立第一份引用；后续 detach 也仍由显式共享指针的规则决定。 |
| 版本 | `QAdoptSharedDataTag` | Qt 6.0 引入的共享数据辅助类型。 | 为兼容 Qt 5 的库代码编写条件编译或替代实现时，要确认目标版本是否提供该类型。 |

## 一句话总结

`QAdoptSharedDataTag` 是共享数据引用计数的“交接凭证”：它告诉 Qt 指针不要再 `ref()`，因为调用方正在移交一份已经存在的有效共享引用。不能证明这份引用存在时，就不要使用它。
