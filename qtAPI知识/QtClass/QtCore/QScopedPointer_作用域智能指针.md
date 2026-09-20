# Qt QScopedPointer：把堆对象绑定到当前作用域

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScopedPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：独占所有权、RAII 智能指针  
> 继承关系：`QScopedArrayPointer` 使用它提供的基础指针操作

## 1. 它解决什么问题

`QScopedPointer<T, Cleanup>` 把一个动态分配对象的所有权放进栈上的包装对象中。包装对象离开作用域时，调用 `Cleanup::cleanup()` 清理所拥有的指针。

它主要解决手工 `delete` 在多返回路径、异常路径和早退路径中容易遗漏的问题：

```cpp
void process()
{
    QScopedPointer<Worker> worker(new Worker);

    if (!prepare())
        return;             // 自动清理 worker

    run(worker.data());
}                           // 自动清理 worker
```

它表达的是**一个明确的独占 owner**，不是共享指针，也不是可移动的值类型：

- 不能复制；
- 不能移动；
- 不能把一个已经存在的 owner 移动转交给另一个 `QScopedPointer`；
- 适合对象只在当前作用域内使用的情况。

Qt 6.2 起，Qt 文档建议新代码优先考虑 `std::unique_ptr`。在维护已有 Qt 代码、需要 Qt 提供的清理器，或项目已经统一使用 `QScopedPointer` 时，仍然需要理解它的语义。

## 2. 所有权和删除策略

默认模板参数是 `QScopedPointerDeleter<T>`，使用 `delete`：

```cpp
QScopedPointer<Widget> widget(new Widget);
```

分配方式必须和删除器匹配：

| 创建方式 | 匹配的清理器 |
| --- | --- |
| `new T` | `QScopedPointerDeleter<T>`，默认值 |
| `new T[n]` | `QScopedPointerArrayDeleter<T>`，使用 `QScopedArrayPointer` 更直接 |
| `malloc()` | `QScopedPointerPodDeleter` |
| QObject 且需要事件循环延迟销毁 | `QScopedPointerDeleteLater` |
| 自定义资源 API | 自定义含 `static void cleanup(T *)` 的清理器 |

不要把 `new[]` 的结果交给普通 `QScopedPointer<T>` 默认删除器：

```cpp
QScopedPointer<int> wrong(new int[10]); // 错误：默认是 delete，不是 delete[]
```

这会产生未定义行为。数组应写成：

```cpp
QScopedArrayPointer<int> values(new int[10]);
```

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QScopedPointer>

class Parser
{
public:
    void parse();
};

void run()
{
    QScopedPointer<Parser> parser(new Parser);
    parser->parse();
}
```

`parser` 是栈对象，`Parser` 是堆对象。`run()` 返回时，`QScopedPointer` 析构并调用默认删除器。

## 4. 实际使用场景

### 4.1 多个出口和异常路径

```cpp
QScopedPointer<Buffer> buffer(new Buffer);

if (!load(buffer.data()))
    return false;

validate(*buffer);
return commit(*buffer);
```

无论 `load()` 失败、`validate()` 抛出异常，还是 `commit()` 正常返回，所有权都不会遗漏。

### 4.2 PImpl 成员

前置声明类型可以作为 `QScopedPointer` 的模板参数，但包含该成员的类必须在需要清理它的地方看到完整类型：

```cpp
class PrivateData;

class PublicClass
{
public:
    PublicClass();
    ~PublicClass();

private:
    QScopedPointer<PrivateData> d;
};
```

`PublicClass` 的析构函数应在包含 `PrivateData` 完整定义的 `.cpp` 文件中实现，不能随意写成头文件内联析构。否则默认删除器无法对不完整类型执行正确的 `delete`。

### 4.3 自定义清理器

```cpp
struct MallocDeleter
{
    static void cleanup(char *pointer)
    {
        std::free(pointer);
    }
};

QScopedPointer<char, MallocDeleter> bytes(
    static_cast<char *>(std::malloc(256))
);
```

自定义清理器必须提供公开的静态 `cleanup(T *)`。清理器中的释放操作必须与资源的创建 API 匹配。

### 4.4 QObject 的延迟销毁

```cpp
#include <QScopedPointer>

QScopedPointer<QObject, QScopedPointerDeleteLater> object(new QObject);
```

析构时会调用 `deleteLater()`，而不是直接 `delete`。这只适合对象参与了有效的 Qt 事件循环，并且对象的线程归属和销毁时机符合 `deleteLater()` 的约束。它不是无条件更安全的删除方式。

## 5. 不可复制和不可移动

`QScopedPointer` 有意禁用复制构造、复制赋值、移动构造和移动赋值。这样可以让所有权始终清楚地绑定到一个作用域：

```cpp
void take(QScopedPointer<Parser> parser); // 不能从另一个 QScopedPointer 复制调用

QScopedPointer<Parser> p(new Parser);
// QScopedPointer<Parser> q(std::move(p)); // 不可移动
```

在 C++17 保证复制消除的特定纯右值返回表达式中，可以直接构造返回值；但这不能移动一个已经存在的 `QScopedPointer` owner。只要接口需要普遍地返回、保存或转交独占所有权，`std::unique_ptr` 通常更合适，因为它明确支持移动和 `release()`。

旧版 `take()` 自 Qt 6.1 起弃用，旧版 `swap()` 自 Qt 6.2 起弃用，Qt 文档建议新代码使用 `std::unique_ptr` 的对应能力。现有代码中遇到它们时，要确认裸指针的 owner 已明确接管，否则会重新引入泄漏或悬空指针风险。

## 6. 生命周期、裸指针和重置边界

`data()` 和 `get()` 返回借用的裸指针，所有权仍属于 `QScopedPointer`：

```cpp
Parser *borrowed = parser.data();
use(borrowed);       // 只能在 parser 仍存活且未 reset 的范围内使用
```

调用 `reset(other)` 时，如果 `other` 与当前指针不同，旧对象会先由当前清理器释放，再由当前指针接管 `other`。传回同一个指针时实现会直接返回：

```cpp
parser.reset(parser.data()); // no-op，但通常没有这样写的必要
```

真正危险的是把当前 `data()` 交给另一个 owner，或先手工删除后再 `reset()`。

`operator->()` 和 `operator*()` 不会为 null 指针提供保护。空指针上访问是未定义行为；`operator*()` 的实现还会使用断言帮助开发期发现错误，但不能把断言当作运行时错误处理。

## 7. 线程边界

`QScopedPointer` 本身是一个普通的独占包装对象，不提供跨线程共享。它可以在线程内部作为局部变量使用，但不能让多个线程同时读写同一个 `QScopedPointer` 变量而不加同步。

如果被管理的是 QObject：

- 指针的独占所有权不改变 QObject 的线程归属；
- `operator->()` 调用仍必须遵守 QObject 的线程规则；
- `QScopedPointerDeleteLater` 依赖对象线程中的事件循环；
- 不要因为删除器是 `deleteLater()` 就把 QObject 随意交给其他线程操作。

## 8. 常见错误

### 8.1 用 `delete` 清理 `new[]`

普通 `QScopedPointer` 的默认清理器调用 `delete`。数组使用 `QScopedArrayPointer` 或显式的 `QScopedPointerArrayDeleter<T>`。

### 8.2 从栈对象建立 QScopedPointer

```cpp
Parser parser;
QScopedPointer<Parser> owner(&parser); // 错误：离开作用域会 delete 栈地址
```

`QScopedPointer` 要求它拥有的指针适合由对应清理器释放，不能把非拥有裸指针塞进去。

### 8.3 与其他 owner 重复管理

一个对象不能同时交给 `QScopedPointer`、`std::unique_ptr`、`QSharedPointer` 或 QObject parent 作为独立 owner。

### 8.4 前置声明类型的析构函数内联

包含 `QScopedPointer<Private>` 的类如果在完整类型不可见处内联析构，可能导致编译器无法实例化删除器。把析构函数和必要的构造/赋值操作放到完整类型可见的实现文件。

### 8.5 把 data() 当作所有权转移

`data()` / `get()` 只是借用访问，不会让调用者取得删除责任。需要释放所有权时不要把裸指针复制给另一个 owner。

## 9. 逐项 API 语义

### 构造、析构与访问

#### `QScopedPointer(T *p = nullptr)`

构造作用域指针并保存 `p`。默认值为空；构造本身不会复制对象。该构造函数是 `explicit`，不会把裸指针隐式转换成 `QScopedPointer`。

#### `~QScopedPointer()`

销毁包装对象，并调用 `Cleanup::cleanup()` 清理当前保存的指针。默认清理器使用 `delete`，自定义清理器可能执行其他资源释放动作。

#### `data() const`

返回当前保存的 `T *`。QScopedPointer 仍然拥有该对象，返回值只能借用。

#### `get() const`

与 `data()` 相同，为接近标准智能指针的命名提供兼容 API。

#### `isNull() const`

当前保存的是 `nullptr` 时返回 `true`。

#### `operator bool() const`

当前指针非空时返回 `true`，是显式布尔转换，适合用于 `if`，不会任意参与整数等隐式转换。

#### `operator!() const`

当前指针为空时返回 `true`。

#### `operator*() const`

返回所拥有对象的引用。当前指针为 null 时行为未定义。

#### `operator->() const`

返回所拥有对象的指针。当前指针为 null 时继续访问成员的行为未定义。

### 改变所有权关系

#### `reset(T *other = nullptr)`

先清理原对象，再保存 `other` 并接管它的所有权。如果清理器可能抛出异常，函数的 `noexcept` 取决于 `Cleanup::cleanup(T *)` 是否为 `noexcept`。使用默认删除器时通常不会抛出。

#### `take()`

自 Qt 6.1 起弃用。返回当前裸指针并把 QScopedPointer 置为空，调用者接管删除责任。新代码使用 `std::unique_ptr::release()`，并明确安排新的 owner。

#### `swap(QScopedPointer<T, Cleanup> &other)`

自 Qt 6.2 起弃用。交换两个同类型 QScopedPointer 保存的指针，可能让指针离开原作用域的所有权设计变得不清楚。新代码使用 `std::unique_ptr` 的移动或 `swap`。

### 清理器类型

#### `QScopedPointerDeleter<T>`

默认清理器，使用 `delete pointer`。要求 `T` 在清理点是完整类型。

#### `QScopedPointerArrayDeleter<T>`

使用 `delete[] pointer`。必须只用于 `new T[]` 创建的数组。

#### `QScopedPointerPodDeleter`

使用 `free(pointer)`，用于 `malloc()` 等 C 分配 API 返回的内存。不要用它释放 `new` 得到的对象。

#### `QScopedPointerObjectDeleteLater<T>` / `QScopedPointerDeleteLater`

对非空 QObject 指针调用 `deleteLater()`。需要对象参与有效事件循环，并遵守 QObject 的线程归属。

#### 自定义 Cleanup

自定义清理器至少应提供公开静态函数：

```cpp
static void cleanup(T *pointer);
```

它必须能处理清理时传入的指针，并与资源实际分配方式匹配。

### 相关非成员比较

#### `operator==(lhs, rhs)` / `operator!=(lhs, rhs)`

比较两个同类型 QScopedPointer 保存的裸指针值。比较不会转移所有权，也不会比较对象内容。

#### `operator==(pointer, nullptr)` / `operator!=(pointer, nullptr)`

判断当前 QScopedPointer 是否为空，等价于 `isNull()` 或其否定。

#### `swap(lhs, rhs)`

自 Qt 6.2 起弃用的非成员交换，与成员 `swap()` 相同。新代码优先使用 `std::unique_ptr`。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QScopedPointer(T *p = nullptr)` | 保存一个由当前作用域独占的裸指针。 | `p` 必须适合由 Cleanup 释放；不接受栈地址。 |
| 析构 | `~QScopedPointer()` | 调用 Cleanup 清理对象。 | 默认使用 `delete`；清理点要有完整类型。 |
| 查询 | `data()` / `get()` | 返回借用的裸指针。 | 不转移所有权，不要交给另一个 owner。 |
| 查询 | `isNull()` | 判断是否为空。 | 不代表对象业务状态。 |
| 查询 | `operator bool()` / `operator!()` | 在条件中判断空状态。 | 只是指针值检查。 |
| 访问 | `operator*()` | 返回对象引用。 | null 时行为未定义。 |
| 访问 | `operator->()` | 访问对象成员。 | null 时行为未定义。 |
| 替换 | `reset(other)` | 清理旧对象并接管新指针。 | 旧对象会立即交给 Cleanup。 |
| 取出 | `take()` | 取出裸指针并放弃所有权。 | Qt 6.1 起弃用；新代码用 `unique_ptr::release()`。 |
| 交换 | `swap(other)` | 交换两个独占指针。 | Qt 6.2 起弃用；新代码用 `std::unique_ptr`。 |
| 默认删除 | `QScopedPointerDeleter<T>` | 使用 `delete`。 | 不能用于数组或 malloc 内存。 |
| 数组删除 | `QScopedPointerArrayDeleter<T>` | 使用 `delete[]`。 | 只能匹配 `new[]`。 |
| C 内存删除 | `QScopedPointerPodDeleter` | 使用 `free()`。 | 只能匹配 malloc/calloc/realloc 体系。 |
| QObject 删除 | `QScopedPointerDeleteLater` | 调用 `deleteLater()`。 | 依赖对象线程和事件循环。 |
| 比较 | `==` / `!=` | 比较裸指针值或空状态。 | 不比较对象内容和所有权历史。 |

---

### 一句话总结

`QScopedPointer` 是不可复制、不可移动的独占 RAII 指针：作用域结束自动清理对象；使用它时最重要的是保持唯一 owner，并让分配方式与 Cleanup 的释放方式严格匹配。
