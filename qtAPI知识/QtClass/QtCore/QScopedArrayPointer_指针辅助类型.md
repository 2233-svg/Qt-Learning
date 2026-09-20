# Qt QScopedArrayPointer：自动使用 delete[] 的数组所有者

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScopedArrayPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制、不可移动的数组 RAII 指针  
> 基类：`QScopedPointer`

## 1. 它解决什么问题

`QScopedArrayPointer<T, Cleanup>` 是一个专门保存 `new T[n]` 数组的作用域指针。它继承 `QScopedPointer` 的生命周期管理和查询接口，但默认清理器是 `QScopedPointerArrayDeleter<T>`，离开作用域时使用 `delete[]`。

它还提供 `operator[](qsizetype)`，因此可以像数组一样访问元素：

```cpp
void fill()
{
    QScopedArrayPointer<int> values(new int[4]);
    values[0] = 10;
    values[1] = 20;
} // 自动执行 delete[]
```

它解决的是两件事：

1. 让数组的释放路径具备 RAII 异常安全；
2. 避免把 `new[]` 错误交给使用 `delete` 的普通 `QScopedPointer`。

Qt 6.2 起，文档建议新代码优先使用 `std::unique_ptr<T[]>`。`QScopedArrayPointer` 主要出现在旧 Qt 代码和需要保持既有 API 的项目中。

## 2. 数组所有权模型

构造时传入的数组指针会被当前对象独占：

```cpp
QScopedArrayPointer<Record> records(new Record[8]);
```

不要再对 `records.data()` 调用 `delete[]`，也不要把它交给另一个 owner。`QScopedArrayPointer` 不记录数组长度，因此它无法检查索引范围：

```cpp
QScopedArrayPointer<int> values(new int[4]);
values[4] = 1; // 越界，行为未定义
```

如果需要长度、迭代器、边界检查或动态扩容，应使用 `QVector`、`QList`、`std::vector` 或 `std::unique_ptr<T[]>` 配合单独的长度变量。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QScopedArrayPointer>

QScopedArrayPointer<char> makeBuffer(qsizetype size)
{
    return QScopedArrayPointer<char>(new char[size]);
}
```

上面的 C++17 纯右值返回依赖保证复制消除，可以直接构造调用方的返回对象；但一个已经存在的 `QScopedArrayPointer` 仍不能移动转交。需要普遍地返回、保存或转移数组所有权时，优先考虑 `std::unique_ptr<char[]>`。

## 4. 实际使用场景

### 4.1 临时数组和异常安全

```cpp
void encode(qsizetype count)
{
    QScopedArrayPointer<char> buffer(new char[count]);
    fillBuffer(buffer.data(), count);
    writeBuffer(buffer.data(), count);
} // 正常返回和异常退出都会 delete[]
```

它适合数组只在一个作用域内使用，且不需要把所有权传给另一个函数的场景。

### 4.2 C 风格接口的临时输出缓冲区

```cpp
QScopedArrayPointer<std::byte> bytes(new std::byte[capacity]);
if (readInto(bytes.data(), capacity) < 0)
    return;

consume(bytes.data());
```

传给 C 风格接口的是借用指针，调用方必须确认该接口不会保存或释放它。`data()` 不会转移数组所有权。

### 4.3 有继承关系的数组类型

数组元素类型和模板参数必须匹配。不要把 `Derived[]` 当成 `Base[]` 交给 `QScopedArrayPointer<Base>`，因为数组元素步长、析构方式和指针类型转换都可能不成立。

## 5. 继承来的接口

`QScopedArrayPointer` 继承或复用 `QScopedPointer` 的：

- `data()`、`get()`；
- `isNull()`、`operator bool()`、`operator!()`；
- `operator*()`、`operator->()`；
- `reset()`；
- 比较运算符。

它不改变这些接口的空指针和所有权语义。`operator[]` 只是新增的数组索引访问，不会增加边界信息。

`QScopedArrayPointer` 自己禁用复制和移动，因此不能放进要求可移动元素的普通值容器，也不能像 `QVector<T>` 一样按值传递。

## 6. 类型匹配和删除边界

默认模板定义为：

```cpp
template <typename T,
          typename Cleanup = QScopedPointerArrayDeleter<T>>
class QScopedArrayPointer;
```

默认删除器执行 `delete[]`。构造函数对传入元素类型有同类型约束，避免把不同元素类型的数组地址伪装成当前模板类型。

这两种分配方式不能混用：

```cpp
QScopedArrayPointer<int> array(new int[4]); // 正确
QScopedPointer<int> scalar(new int);        // 正确
```

```cpp
QScopedPointer<int> wrong(new int[4]);      // 错误：默认 delete
QScopedArrayPointer<int> alsoWrong(new int); // 错误：默认 delete[]
```

## 7. 索引参数与版本边界

Qt 6.5 起，`operator[]` 的索引类型是 `qsizetype`：

```cpp
values[static_cast<qsizetype>(index)]
```

Qt 6.5 以前的文档签名使用 `int`，在 64 位平台上把大索引传入旧 API 可能发生截断。升级代码时不要假设 `int` 与 `qsizetype` 在所有版本中等价。

`operator[]` 不做负数检查。负索引和超出实际数组长度的索引都属于未定义行为。

## 8. 生命周期、线程和前置声明

数组只在 `QScopedArrayPointer` 存活期间保证由它拥有。`data()` 返回的裸指针不能跨越 owner 的 `reset()` 或析构：

```cpp
char *borrowed = buffer.data();
buffer.reset(); // borrowed 立即失效
```

它不是线程共享容器。不同线程使用同一数组内容仍需自行同步；同一个 `QScopedArrayPointer` 变量也不能被线程并发读写而不加同步。

如果数组元素是前置声明类型，默认 `delete[]` 需要在清理点看到完整类型。包含该成员的类通常应把析构函数放到元素类型完整可见的实现文件中。

## 9. 常见错误

### 9.1 用普通 QScopedPointer 管理数组

普通默认清理器使用 `delete`，与 `new[]` 不匹配。使用 `QScopedArrayPointer` 或显式 `QScopedPointerArrayDeleter<T>`。

### 9.2 把数组长度交给指针猜

`QScopedArrayPointer` 不保存长度，不会检查边界。长度必须由业务代码单独保存。

### 9.3 从不同元素类型的数组构造

数组协变规则不像单个对象指针那样简单。`Derived[]` 与 `Base[]` 不能安全地互换 owner。

### 9.4 对 data() 调用 delete[]

`data()` 只是借用访问。数组仍由 QScopedArrayPointer 管理，手工释放会导致重复释放。

### 9.5 试图复制或移动已有 owner

该类型明确禁用复制和移动。除 C++17 保证复制消除的直接纯右值构造外，不能转交已有 owner；需要常规所有权转移时，`std::unique_ptr<T[]>` 更适合。

### 9.6 把它当作 QVector

它没有 size、迭代器、插入、删除或自动扩容能力。只在必须管理裸数组且作用域清晰时使用。

## 10. 逐项 API 语义

### 本类新增 API

#### `QScopedArrayPointer()`

构造空数组指针，继承的 `data()` 返回 `nullptr`，析构时不执行有效数组删除。

#### `QScopedArrayPointer(D *p)`

接管 `p` 指向的数组。模板约束要求 `D` 与 `T` 是同一去 cv 类型，避免把不兼容元素数组交给 `delete[]`。

#### `operator[](qsizetype i)`

返回数组第 `i` 个元素的可修改引用。函数不记录长度、不检查 `i`，当前指针为空、索引为负或索引超界时行为未定义。Qt 6.5 起参数为 `qsizetype`。

#### `operator[](qsizetype i) const`

返回数组第 `i` 个元素的 const 引用。边界规则与非 const 重载相同。

#### `~QScopedArrayPointer()`

继承的数组所有权在析构时结束，默认调用 `QScopedPointerArrayDeleter<T>::cleanup()`，也就是 `delete[]`。

### 从 QScopedPointer 继承的常用 API

#### `data() const` / `get() const`

返回数组首元素指针，仍由当前 QScopedArrayPointer 所有。调用者不能手工释放。

#### `isNull() const` / `operator bool()` / `operator!() const`

查询数组首指针是否为空，不表示数组长度或元素内容有效。

#### `operator*() const` / `operator->() const`

提供对首元素的对象式访问。空数组指针上使用是未定义行为；访问数组元素通常应使用 `operator[]`。

#### `reset(T *other = nullptr)`

继承的重置操作。它会先使用当前 Cleanup 对原数组执行 `delete[]`，再接管 `other`。不能传入已由其他 owner 管理的地址。

#### `take()`

自 Qt 6.1 起弃用的基类接口。它会取出首地址并放弃数组所有权，但调用者必须以 `delete[]` 兼容的方式接管。新代码使用 `std::unique_ptr<T[]>::release()`。

#### `swap(QScopedArrayPointer &other)`

自 Qt 6.2 起弃用。交换两个同类型数组 owner；新代码优先使用 `std::unique_ptr<T[]>`。

### 相关类型和非成员 API

#### `QScopedPointerArrayDeleter<T>`

数组默认清理器，执行 `delete[]`。只匹配 `new T[]`。

#### 比较运算符 `==` / `!=`

继承的比较按首指针地址或空状态进行，不比较数组长度和元素内容。

#### `swap(lhs, rhs)`

Qt 6.2 起弃用的非成员交换，与成员 `swap()` 相同。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QScopedArrayPointer()` | 创建空数组 owner。 | 不包含长度信息。 |
| 接管 | `QScopedArrayPointer(D *)` | 接管 `new D[n]` 数组。 | 元素类型必须匹配；默认使用 `delete[]`。 |
| 索引 | `operator[](qsizetype)` | 访问第 `i` 个元素。 | 无边界检查；Qt 6.5 起使用 `qsizetype`。 |
| 析构 | `~QScopedArrayPointer()` | 自动释放数组。 | 默认执行 `delete[]`。 |
| 查询 | `data()` / `get()` | 返回首元素借用指针。 | 不转移所有权。 |
| 查询 | `isNull()` / `operator bool()` | 判断首指针是否为空。 | 不表示长度和边界安全。 |
| 首元素访问 | `operator*()` / `operator->()` | 访问第一个元素。 | 空指针上行为未定义。 |
| 替换 | `reset(other)` | 释放旧数组并接管新数组。 | 新地址必须是当前 Cleanup 可释放的数组。 |
| 取出 | `take()` | 放弃所有权并返回裸指针。 | Qt 6.1 起弃用；新代码用 `unique_ptr<T[]>::release()`。 |
| 交换 | `swap(other)` | 交换两个数组 owner。 | Qt 6.2 起弃用；新代码用 `std::unique_ptr<T[]>`。 |
| 删除器 | `QScopedPointerArrayDeleter<T>` | 执行 `delete[]`。 | 不能释放单对象或 malloc 内存。 |
| 比较 | `==` / `!=` | 比较首指针值或空状态。 | 不比较数组内容和长度。 |

---

### 一句话总结

`QScopedArrayPointer` 是 `new[]` 数组的独占 RAII 包装：默认用 `delete[]`，支持 `qsizetype` 索引但不保存长度、不做边界检查；需要转移所有权或更丰富的数组能力时，应优先考虑 `std::unique_ptr<T[]>` 或容器。
