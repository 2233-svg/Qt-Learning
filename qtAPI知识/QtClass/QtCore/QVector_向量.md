# Qt QVector：Qt 6 中只是 QList 的别名

在 Qt 6.11.1，`QVector<T>` 不是独立容器类，而是 `QList<T>` 的类型别名。它保留是为了兼容旧代码和旧术语：

```cpp
template <typename T>
using QVector = QList<T>;
```

因此 `QVector<int>` 与 `QList<int>` 是同一个类型，不存在“从 `QList` 继承到 `QVector`”的对象模型，也没有只属于 `QVector` 的成员函数、虚函数或运行时类型差异。要理解其存储、隐式共享、迭代器失效、元素要求和全部容器 API，应直接查阅 `QList`。

```cpp
#include <QVector>

QVector<int> points { 4, 8, 15 };
points.append(16);

static_assert(std::is_same_v<QVector<int>, QList<int>>);
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVector>`  
> CMake：`Qt6::Core`  
> 本质：`QVector<T>` 是 `QList<T>` 的别名，不是派生类。

## 它解决什么问题

Qt 5 曾区分 `QList` 与 `QVector`，很多代码用 `QVector` 表达“连续数组”意图。Qt 6 统一了两者：保留 `QVector` 名字，使现有源码大多无需修改，同时让所有实现和行为直接复用 `QList`。

真实场景通常是维护已有 API：

```cpp
QVector<QPointF> readPolyline();
```

这份函数声明仍然清楚表达“返回一组点”。但新代码若没有兼容旧接口的原因，选 `QList` 可以减少团队对“它们是否有不同性能和 API”的无效猜测。两种拼写可以互相赋值、作为模板实参匹配，并共享完全相同的容器行为。

## 不要把别名当作继承

文档页面把 `QList` 列在 “Inherits” 位置只是文档呈现方式；C++ 中这不是继承：

- 不存在 `QVector` 独有的 vtable、基类指针转换或多态；
- `QVector<int>` 和 `QList<int>` 的 `std::is_same_v` 为真；
- 不能为 `QVector` 单独写偏特化、重载或元类型注册；那会与 `QList` 的同一类型定义冲突；
- `QList` 的任何成员 API 都是 `QVector` 可用 API，反过来也一样。

因此，重载下面两个函数不是两个重载：

```cpp
void use(QList<int>);
// void use(QVector<int>); // 重定义：参数类型相同
```

同理，若公开库 API 从 `QVector<T>` 改写为 `QList<T>`，对 C++ 类型系统通常没有 ABI 类型差异，但仍可能影响源码可读性、文档、生成绑定和用户预期。公共接口迁移仍应按项目的兼容性政策处理。

## 选择和性能：看 QList，而不是旧经验

不要把 Qt 5 时期关于 `QList` / `QVector` 内存布局和性能的经验直接套到 Qt 6。Qt 6 中 `QVector` 就是 `QList`，比较性能时应针对当前 Qt 版本、`T` 的大小和可移动性、访问模式以及是否发生隐式共享分离来测量。

`QList` 是值类型并采用隐式共享。复制容器通常成本较低，但非 const 访问或修改可能触发分离，令指针、引用和迭代器发生变化。以下原则同样适用于 `QVector`：

- 长期保存 `data()`、元素引用或迭代器前，先保证容器不会被修改、分离或销毁；
- 范围遍历时修改同一容器可能使迭代器失效；
- 跨线程共享同一个可变实例仍需同步；值类型和隐式共享不消除数据竞争；
- 需要与 C API 交换连续数据时，传递指针的同时传递长度，且不要假定 NUL 终止。

## Java 风格迭代器别名

当没有定义 `QT_NO_JAVA_STYLE_ITERATORS` 时，`<QVector>` 还提供两个旧式别名：

```cpp
template <typename T>
using QVectorIterator = QListIterator<T>;

template <typename T>
using QMutableVectorIterator = QMutableListIterator<T>;
```

它们同样不是独立实现。新代码更推荐 C++ 范围 for、STL 风格迭代器或 Qt 容器算法；若现有代码使用 Java 风格迭代器，修改容器时仍必须遵守其与容器修改交互的规则。

## API 速查表

`QVector` 自身没有独立成员 API。下表列出它实际引入的类型接口；所有构造、访问、追加、插入、删除、迭代、比较、哈希和数据流 API 均为 `QList` API。

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QVector<T>` | `QList<T>` 的模板别名 | Qt 6 中两者是同一类型，不是继承关系。 |
| `QVector<T>` 的全部容器成员 | 构造、`append`、`insert`、`remove`、`data`、迭代等 | 直接遵守 `QList<T>` 文档中的语义、元素要求和迭代器失效规则。 |
| `QVectorIterator<T>` | `QListIterator<T>` 的别名 | 仅在未定义 `QT_NO_JAVA_STYLE_ITERATORS` 时提供；适合兼容旧代码。 |
| `QMutableVectorIterator<T>` | `QMutableListIterator<T>` 的别名 | 同样受宏控制；修改时遵守 `QMutableListIterator` 语义。 |
| `#include <QVector>` | 引入别名和依赖声明 | 可以继续用于兼容性；也可直接包含 `<QList>` 使用实际容器。 |

## 常见错误

- 把 Qt 6 的 `QVector` 当作拥有不同实现的另一种容器来做“二选一”性能判断。
- 依据文档页面的 “Inherits” 文字，误以为存在 C++ 继承和运行时多态。
- 同时为 `QVector<T>` 与 `QList<T>` 写重载、特化或不同元类型声明。
- 忽略 `QList` 的隐式共享与修改后迭代器/引用失效规则。
- 在新代码里使用 Java 风格迭代器，却不知道它只是 `QListIterator` 的兼容名称。

---

### 一句话总结

Qt 6 的 `QVector<T>` 就是 `QList<T>`；保留这个名字主要为了源码兼容，真正的行为和完整 API 必须以 `QList` 文档为准。
