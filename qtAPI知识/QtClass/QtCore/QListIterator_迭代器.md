# Qt QListIterator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QListIterator>`  
> 所属模块：`Qt6::Core`  
> 类型性质：Java 风格、只读、双向遍历器  
> 相关类型：`QList`、`QQueue`、`QStack`、`QMutableListIterator`、`QList::const_iterator`

## 1. 它解决什么问题

`QListIterator<T>` 为 `QList<T>` 提供一种 Qt 传统的 **Java 风格只读迭代方式**。它适合把遍历位置封装成一个对象，并通过 `hasNext()`、`next()`、`hasPrevious()`、`previous()` 控制游标。

它解决的主要问题是：

- 不需要暴露整数索引，就能顺序或逆序遍历；
- 可以从当前位置向前或向后查找某个值；
- 可以通过 `toFront()`、`toBack()` 快速重置遍历方向；
- 迭代器对象自己持有一个列表副本，源列表后续修改时仍可继续遍历原来的共享数据；
- 用统一接口处理 `QList`、`QQueue` 和 `QStack` 的顺序访问。

它不是 STL 风格迭代器：

- STL 迭代器直接指向元素；
- `QListIterator` 的位置在元素之间；
- `next()` 返回游标前方的元素，并把游标越过该元素；
- `previous()` 返回游标后方的元素，并把游标退过该元素。

Qt 文档指出，STL 风格迭代器通常更高效，新的普通遍历代码应优先考虑 `QList::const_iterator`、范围 `for` 或索引访问。`QListIterator` 更适合需要“当前位置状态”和“前后双向查找”的旧 Qt 风格代码。

## 2. 实际使用场景

### 2.1 顺序读取而不修改列表

```cpp
QList<float> values{1.5f, 2.5f, 3.5f};
QListIterator<float> it(values);

while (it.hasNext()) {
    const float value = it.next();
    // 处理 value
}
```

### 2.2 从尾部反向遍历

```cpp
QList<QString> names{"Ada", "Grace", "Katherine"};
QListIterator<QString> it(names);
it.toBack();

while (it.hasPrevious())
    qDebug() << it.previous();
```

### 2.3 查找多个匹配项

```cpp
QList<int> values{4, 2, 4, 7, 4};
QListIterator<int> it(values);

while (it.findNext(4)) {
    qDebug() << "found 4";
}
```

每次 `findNext()` 成功后，游标位于匹配元素之后，因此下一次调用会继续向后搜索，不会重复返回同一个元素。

### 2.4 需要修改时切换到可变迭代器

`QListIterator` 的返回值是 `const T &`，不能通过它修改元素，也没有插入和删除 API。需要在遍历中修改时使用 `QMutableListIterator<T>`：

```cpp
QList<int> values{-2, 0, 3};
QMutableListIterator<int> it(values);

while (it.hasNext()) {
    const int value = it.next();
    if (value < 0)
        it.setValue(-value);
    else if (value == 0)
        it.remove();
}
```

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QList>
#include <QListIterator>
```

qmake 工程使用：

```qmake
QT += core
```

## 4. 核心模型：游标在元素之间

假设列表为：

```text
[ A ][ B ][ C ]
 ^     ^     ^     ^
front  1     2    back
```

更准确地说，游标有四个可能位置：

```text
front       between A/B   between B/C       back
  |              |             |              |
 [ A ]          [ B ]         [ C ]          end
```

构造后游标在 `front`：

```cpp
QListIterator<QString> it(list);
Q_ASSERT(it.hasNext());
```

第一次调用 `next()`：

1. 返回 `A`；
2. 游标移动到 `A` 和 `B` 之间。

继续调用 `next()` 会依次返回 `B`、`C`。返回 `C` 后，游标位于 `back`，此时 `hasNext()` 返回 `false`。

反向时，先调用 `toBack()`，然后 `previous()` 依次返回 `C`、`B`、`A`。

## 5. 保存列表副本和修改隔离

### 5.1 构造函数复制的是容器值

```cpp
QList<int> source{1, 2, 3};
QListIterator<int> it(source);
```

迭代器内部保存一个 `QList<T>` 副本。因为 `QList` 隐式共享，这个复制通常很便宜，不会立刻复制所有元素。

### 5.2 源列表修改后，迭代器继续看原数据

```cpp
QList<int> source{1, 2, 3};
QListIterator<int> it(source);

source.append(4);

while (it.hasNext())
    qDebug() << it.next(); // 仍遍历 1、2、3
```

当 `source` 修改并触发写时复制时，迭代器持有的副本仍然引用原数据块，因此它会忽略修改后的列表。

这是一种“值快照”式行为，但要理解它的边界：

- 元素本身会按 `QList` 的值语义共享或复制；
- 如果 `T` 是指针，指针指向的对象不会被深复制；
- 如果其他代码通过共享指针、全局状态或对象指针修改元素所指向的对象，迭代器仍可能观察到那些外部对象的变化；
- 迭代器持有列表副本，会延长底层元素数据的生命周期。

### 5.3 迭代器赋值会替换容器并回到开头

```cpp
QListIterator<int> it(first);
it.toBack();
it = second; // 改为遍历 second，并重置到 front
```

`operator=(const QList<T> &list)` 会让迭代器改为操作新的列表，并把位置设置为新列表的 `front`。

## 6. `next()`、`previous()` 的前置条件

### 6.1 调用 `next()` 前检查 `hasNext()`

```cpp
if (it.hasNext()) {
    const T &value = it.next();
}
```

如果迭代器已经在 `back`，直接调用 `next()` 会产生未定义结果。它不会返回一个安全的默认值，也不会自动停在最后一个元素。

### 6.2 调用 `previous()` 前检查 `hasPrevious()`

```cpp
it.toBack();
if (it.hasPrevious()) {
    const T &value = it.previous();
}
```

如果迭代器已经在 `front`，直接调用 `previous()` 会产生未定义结果。

### 6.3 `peek` 只观察，不移动游标

- `peekNext()` 返回下一个元素，但不移动游标；
- `peekPrevious()` 返回上一个元素，但不移动游标；
- 两者同样要求对应方向存在元素。

```cpp
if (it.hasNext()) {
    const QString &preview = it.peekNext();
    const QString &same = it.next();
    Q_ASSERT(preview == same);
}
```

返回的是对迭代器内部列表元素的 const 引用。不要把引用保存到会改变迭代器对象或其内部容器生命周期之外的地方。

## 7. 查找 API 的游标落点

### 7.1 `findNext()`

```cpp
QListIterator<int> it(QList<int>{1, 4, 2, 4});

const bool found = it.findNext(4);
```

`findNext(value)` 从当前游标位置向前搜索：

- 找到：返回 `true`，游标位于匹配元素之后；
- 找不到：返回 `false`，游标移动到 `back`。

因此可以用循环查找所有匹配值：

```cpp
while (it.findNext(4)) {
    // 当前匹配值位于游标之前，可用 peekPrevious() 读取
    qDebug() << it.peekPrevious();
}
```

### 7.2 `findPrevious()`

`findPrevious(value)` 从当前游标位置向后搜索：

- 找到：返回 `true`，游标位于匹配元素之前；
- 找不到：返回 `false`，游标移动到 `front`。

```cpp
it.toBack();
while (it.findPrevious(4)) {
    qDebug() << it.peekNext();
}
```

`findNext()` 和 `findPrevious()` 都要求 `T` 支持与搜索值进行相等比较。

## 8. 和其他迭代方式的选择

| 需求 | 推荐方式 | 原因 |
| --- | --- | --- |
| 普通只读遍历 | 范围 `for` 或 `QList::const_iterator` | 更直接，通常更高效 |
| 需要一个带状态的前后游标 | `QListIterator` | Java 风格位置模型清晰 |
| 遍历中修改、删除、插入 | `QMutableListIterator` | 修改操作由迭代器协调 |
| 已经有整数索引 | `at()`、const `operator[]` | 不需要额外迭代器对象 |
| 需要任意跳转和算法库 | `QList::const_iterator` | 支持随机访问迭代器运算 |
| 需要多个并行只读遍历 | 多个 `QListIterator` | 每个对象拥有自己的位置 |

### 8.1 不要把 Java 风格迭代器和 STL 迭代器混用

```cpp
QListIterator<int> javaIt(values);
auto stlIt = values.cbegin();
```

二者的游标含义完全不同：

- `javaIt` 位于元素之间；
- `stlIt` 直接指向元素或尾后位置；
- `javaIt.next()` 返回并跨过下一个元素；
- `++stlIt` 先把 STL 迭代器移动到下一个元素。

如果代码需要 `std::sort()`、`std::find()` 或任意随机访问运算，应直接使用 STL 风格迭代器。

### 8.2 `QListIterator` 和 `QMutableListIterator` 不能互换

`QListIterator`：

- 构造参数是 `const QList<T> &`；
- 返回 `const T &`；
- 没有 `insert()`、`remove()`、`setValue()`；
- 可以有多个只读迭代器。

`QMutableListIterator`：

- 构造参数是 `QList<T> &`；
- 返回 `T &`；
- 支持插入、删除和修改；
- 同一个列表上同一时间只能有一个可变迭代器活跃；
- 迭代器活跃期间不能直接修改列表，必须通过可变迭代器完成。

## 9. 常见误区

### 9.1 误以为构造后指向第一个元素

构造后在第一个元素之前，不是已经选中了第一个元素：

```cpp
QListIterator<int> it(values);
// it.peekNext() 是第一个元素
// it.peekPrevious() 此时非法
```

### 9.2 误以为 `next()` 在尾部会返回空值

`next()` 没有安全失败返回值。调用前必须检查 `hasNext()`，否则是未定义结果。

### 9.3 `peekNext()` 和 `next()` 的游标效果混淆

`peekNext()` 不改变位置；`next()` 会把位置向后推进一格。多次调用 `peekNext()` 会得到同一元素，直到其他操作移动游标。

### 9.4 搜索失败后继续按原位置理解

```cpp
if (!it.findNext(target)) {
    // it 已经在 back，不在搜索前的原位置
}
```

反向搜索失败时相反：游标已经在 `front`。

### 9.5 用迭代器遍历时直接改原列表

`QListIterator` 自己持有列表副本，所以源列表修改不会更新它；如果目标是同步修改，应使用 `QMutableListIterator` 或索引 API。不要在可变迭代器活跃时直接调用 `append()`、`remove()` 等列表成员函数。

### 9.6 把它当作内存地址迭代器

Java 风格迭代器不提供 `operator*`、指针算术或随机跳转。需要这些能力时选择 `QList::iterator`/`const_iterator`。

### 9.7 忽略 `T` 的相等比较要求

`findNext()` 和 `findPrevious()` 要执行 `operator==()`。如果自定义类型没有合适的相等比较，代码可能无法编译，或者比较语义不符合业务预期。

## 10. 逐项 API 说明

### 10.1 `QListIterator(const QList<T> &list)`

```cpp
QListIterator(const QList<T> &list);
```

构造一个遍历 `list` 的只读迭代器。构造完成后位置在 `front`，即第一个元素之前。

迭代器内部保存列表副本。由于 `QList` 隐式共享，构造通常不会立即复制全部元素；源列表之后修改时，迭代器继续使用原来的共享数据。

### 10.2 `findNext(const T &value)`

```cpp
bool findNext(const T &value);
```

从当前游标向 `back` 搜索第一个相等值。成功返回 `true`，位置移动到匹配项之后；失败返回 `false`，位置移动到 `back`。

### 10.3 `findPrevious(const T &value)`

```cpp
bool findPrevious(const T &value);
```

从当前游标向 `front` 搜索第一个相等值。成功返回 `true`，位置移动到匹配项之前；失败返回 `false`，位置移动到 `front`。

### 10.4 `hasNext() const`

```cpp
bool hasNext() const;
```

判断游标和 `back` 之间是否还有元素。它是安全调用 `next()` 和 `peekNext()` 的前置检查。

### 10.5 `hasPrevious() const`

```cpp
bool hasPrevious() const;
```

判断 `front` 和游标之间是否还有元素。它是安全调用 `previous()` 和 `peekPrevious()` 的前置检查。

### 10.6 `next()`

```cpp
const T &next();
```

返回游标前方的元素，并将游标向 `back` 移动一个元素位置。游标在 `back` 时调用会产生未定义结果。

### 10.7 `peekNext() const`

```cpp
const T &peekNext() const;
```

返回游标前方的元素，但不移动游标。游标在 `back` 时调用会产生未定义结果。

### 10.8 `peekPrevious() const`

```cpp
const T &peekPrevious() const;
```

返回游标后方的元素，但不移动游标。游标在 `front` 时调用会产生未定义结果。

### 10.9 `previous()`

```cpp
const T &previous();
```

返回游标后方的元素，并将游标向 `front` 移动一个元素位置。游标在 `front` 时调用会产生未定义结果。

### 10.10 `toBack()`

```cpp
void toBack();
```

把游标移动到列表末尾之后。调用后 `hasNext()` 为 `false`；如果列表非空，`hasPrevious()` 为 `true`。

### 10.11 `toFront()`

```cpp
void toFront();
```

把游标移动到列表第一个元素之前。调用后 `hasPrevious()` 为 `false`；如果列表非空，`hasNext()` 为 `true`。

### 10.12 `operator=(const QList<T> &list)`

```cpp
QListIterator<T> &operator=(const QList<T> &list);
```

让迭代器改为遍历 `list`，并重置到 `front`。返回当前迭代器引用，便于链式赋值。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QListIterator(const QList<T> &list)` | 构造只读 Java 风格迭代器。 | 位置初始在 `front`；内部保存列表值副本。 |
| `bool findNext(const T &value)` | 从当前位置向后找值。 | 成功后在匹配项之后；失败后在 `back`。 |
| `bool findPrevious(const T &value)` | 从当前位置向前找值。 | 成功后在匹配项之前；失败后在 `front`。 |
| `bool hasNext() const` | 判断是否可以安全调用 `next()`/`peekNext()`。 | 游标在 `back` 时为 `false`。 |
| `bool hasPrevious() const` | 判断是否可以安全调用 `previous()`/`peekPrevious()`。 | 游标在 `front` 时为 `false`。 |
| `const T &next()` | 返回下一个元素并向后移动。 | 没有下一个元素时调用是未定义行为。 |
| `const T &peekNext() const` | 查看下一个元素但不移动。 | 没有下一个元素时调用是未定义行为。 |
| `const T &peekPrevious() const` | 查看上一个元素但不移动。 | 没有上一个元素时调用是未定义行为。 |
| `const T &previous()` | 返回上一个元素并向前移动。 | 没有上一个元素时调用是未定义行为。 |
| `void toBack()` | 把游标放到末尾之后。 | 适合开始反向遍历。 |
| `void toFront()` | 把游标放到开头之前。 | 适合重新开始正向遍历。 |
| `QListIterator<T> &operator=(const QList<T> &list)` | 切换遍历列表并重置位置。 | 新列表由 `front` 开始。 |

## 12. 完整示例：查找并从两侧读取

```cpp
#include <QList>
#include <QListIterator>
#include <QString>

void inspect(const QList<QString> &names)
{
    QListIterator<QString> it(names);

    if (it.hasNext()) {
        const QString &first = it.peekNext();
        qDebug() << "first:" << first;
    }

    while (it.hasNext()) {
        const QString &name = it.next();
        if (name.startsWith(u'A'))
            qDebug() << "A-name:" << name;
    }

    it.toBack();
    if (it.hasPrevious())
        qDebug() << "last:" << it.peekPrevious();
}
```

示例中的 `peekNext()` 和 `peekPrevious()` 只读取不移动；真正推进游标的操作是 `next()` 和 `previous()`。

## 13. 选型结论

1. `QListIterator` 是 Java 风格的只读双向迭代器，游标位于元素之间。
2. 构造后位于 `front`，反向遍历前先调用 `toBack()`。
3. `next()`、`previous()`、`peekNext()`、`peekPrevious()` 都必须先检查对应的 `has...()`。
4. `findNext()` 成功后停在匹配项之后，失败后停在 `back`；`findPrevious()` 的方向相反。
5. 迭代器保存 `QList` 值副本，源列表修改后会继续遍历原数据。
6. 只读普通遍历优先使用范围 `for` 或 `QList::const_iterator`；需要修改时使用 `QMutableListIterator`。
7. 不要在可变迭代器活跃期间直接修改列表；所有插入、删除和替换都应通过可变迭代器完成。

