# Qt QGlobalStatic 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGlobalStatic>`  
> 所属模块：`Qt6::Core`  
> 类型性质：实现惰性初始化全局静态对象的前端结构  
> 常用入口：`Q_GLOBAL_STATIC`

## 1. 它解决什么问题

普通的非平凡全局静态对象有三个经典问题：

- 程序或库加载时就构造，即使整个进程从未使用它；
- 不同翻译单元之间的初始化和析构顺序难以推断；
- 一个全局对象的析构函数可能访问另一个已经析构的全局对象。

`QGlobalStatic` 和 `Q_GLOBAL_STATIC` 用“第一次使用时初始化”的方式解决这些问题：

- 对象不会因为仅仅加载库就立即构造；
- 初始化在所有平台上以线程安全方式完成；
- 可以通过 `exists()` 查询是否已经初始化，而不触发创建；
- 可以通过 `isDestroyed()` 防止退出期或卸载期继续解引用；
- 通过类似指针的语法访问对象。

通常不直接写 `QGlobalStatic<Holder>`，而是在源文件的全局作用域使用宏：

```cpp
Q_GLOBAL_STATIC(MyType, myGlobal)
```

## 2. 实际使用场景

### 2.1 惰性创建缓存或注册表

```cpp
class Cache
{
public:
    QString lookup(const QString &key) const;
};

Q_GLOBAL_STATIC(Cache, cache)

QString lookup(const QString &key)
{
    return cache->lookup(key);
}
```

只有第一次真正通过 `cache` 访问对象时，`Cache` 才构造。

### 2.2 带构造参数的全局状态

Qt 6.3 起，`Q_GLOBAL_STATIC` 接受可变参数：

```cpp
class Registry
{
public:
    explicit Registry(int bucketCount);
};

Q_GLOBAL_STATIC(Registry, registry, 64)
```

参数不需要再额外包一层括号。旧代码中的 `Q_GLOBAL_STATIC_WITH_ARGS(Registry, registry, (64))` 是兼容形式，新代码优先使用可变参数版本。

### 2.3 退出期检查

可能在应用或插件退出阶段运行的代码，可以先检查：

```cpp
if (cache.isDestroyed())
    return;

if (auto *value = cache)
    use(value);
```

不要用 `cache->method()` 绕过检查，因为 `operator->()` 在对象已经销毁后不能提供有效对象。

## 3. 宏和结构的关系

`Q_GLOBAL_STATIC(Type, variableName, ...)` 会生成：

1. 一个描述类型和构造参数的内部 holder；
2. 一个 `QGlobalStatic<Holder>` 变量；
3. 一个在第一次访问时创建 `Type` 的存储对象。

`QGlobalStatic::Type` 是宏中 `Type` 参数的别名。宏生成的变量表现得像一个 `Type *`，同时提供 `exists()` 和 `isDestroyed()`。

## 4. 放置位置是硬边界

### 4.1 必须放在源文件的全局作用域

宏不能放进函数体或类体：

```cpp
// cache.cpp
Q_GLOBAL_STATIC(Cache, cache)
```

不要把它写进公共头文件。宏创建的对象具有静态链接属性，每个包含该头文件的翻译单元都可能得到一个独立实例。这样不会一定触发链接错误，却会造成每个 `.cpp` 看见不同的全局缓存。

### 4.2 类型构造和析构必须可访问

只有 `Type` 和变量名时，`Type` 必须有公开默认构造函数和公开析构函数。带参数时，必须有能接受这些参数的公开构造函数。

如果原类型的构造或析构受保护，可以通过派生一个公开构造/析构的包装类型解决；私有成员则还需要适当的友元关系。更简单的替代方案通常是提供一个专门的公开 holder 类型。

## 5. 初始化、线程安全和死锁

### 5.1 第一次访问才构造

指针转换、`operator()`、`operator->()` 和 `operator*()` 都可能触发初始化。多个线程同时第一次访问时，只有一个线程执行构造，其他线程等待初始化完成。

如果构造函数抛异常，初始化视为未完成，后续访问会再次尝试构造。不要在构造函数中隐藏不可恢复的跨线程副作用。

### 5.2 构造函数必须避免自依赖

如果全局对象的构造过程中直接或间接再次访问自己，会产生死锁。两个不同 `Q_GLOBAL_STATIC` 对象在不同线程上交叉访问对方的构造过程，也可能死锁。

因此全局静态构造函数应尽量简单：

- 不访问其他惰性全局对象；
- 不启动需要回调回当前全局对象的线程任务；
- 不依赖复杂的 QObject、插件或日志初始化链；
- 把昂贵或有依赖的工作推迟到显式成员函数。

### 5.3 初始化安全不等于对象内部线程安全

宏保证的是“只初始化一次”这一层安全，不会自动让 `Type` 的成员读写线程安全。`Type` 仍需自己使用互斥量、原子或不可变数据设计。

## 6. 销毁和退出期边界

如果对象从未真正使用过，只调用 `exists()` 或 `isDestroyed()`，其内容不会被创建，也不会产生对应的退出期析构工作。

一旦创建，`Type` 通常在进程退出时析构；包含它的插件或动态库卸载时也可能析构。析构阶段不提供线程安全保证，也不提供异常安全保证。

析构正在进行时，重复访问可能是允许的，但析构完成后：

- `exists()` 不再为真；
- `isDestroyed()` 为真；
- 指针转换和 `operator()` 返回空指针；
- `operator->()` 和 `operator*()` 不应再调用。

退出期代码应主动检查 `isDestroyed()`，避免使用已经销毁的服务、日志器或缓存。

## 7. `exists()` 的特殊语义

`exists()` 是一个不触发创建的查询：

- 初始化尚未开始或正在进行时返回 `false`；
- 构造完成且尚未开始销毁时返回 `true`；
- 销毁完成后返回 `false`；
- 不会为了回答查询而构造对象；
- 可以从任意线程调用，不会因为对象尚未创建而等待构造。

文档还特别说明，它不提供一般的内存排序保证；真正获取对象指针或引用的访问器会提供所需的访问顺序。不要使用 `exists()` 作为复杂共享状态同步原语。

## 8. 逐项 API 说明

### 成员类型

#### `[alias] QGlobalStatic::Type`

等价于传给 `Q_GLOBAL_STATIC` 或 `Q_GLOBAL_STATIC_WITH_ARGS` 的 `Type` 参数。它用于描述转换运算符、解引用和箭头运算符的返回类型。

### 状态查询

#### `[noexcept] bool QGlobalStatic::exists() const`

查询对象是否已经完成初始化并且尚未完成销毁。它不会触发创建，适合在可能不需要对象时快速返回默认值。

初始化仍在进行时返回 `false`。在构造完成后，第一次观察到 `true` 后，直到销毁开始前不会再回到 `false`；退出期和库卸载期是例外边界。

#### `[noexcept] bool QGlobalStatic::isDestroyed() const`

查询对象析构是否已经完成。它不会触发创建，可以在退出期防止解引用已经失效的全局对象。

析构正在进行时返回 `false`，只有析构完成后才返回 `true`。如果对象从未被创建，它也不会因为“从未创建”而被视为已销毁。

### 指针和引用访问

#### `QGlobalStatic<Holder>::Type *QGlobalStatic::operator QGlobalStatic<Holder>::Type *()`

把 wrapper 转换为对象指针：

- 尚未创建时，线程安全地创建对象；
- 对象存活时返回其地址；
- 对象已经销毁时返回 `nullptr`。

可以把结果保存到局部指针，避免一个热点路径重复访问 wrapper。但局部指针不能跨越对象销毁边界保存使用。

#### `QGlobalStatic<Holder>::Type *QGlobalStatic::operator()()`

显式的指针访问形式。头文件实现和指针转换一样：未创建时初始化，销毁后返回 `nullptr`。

它适合不希望依赖隐式指针转换的代码：

```cpp
if (auto *p = cache())
    p->clear();
```

#### `QGlobalStatic<Holder>::Type *QGlobalStatic::operator->()`

以指针成员访问语法取得对象。未创建时会初始化。

该运算符不在销毁后返回空指针，而是对已销毁状态执行断言并可能产生悬空指针；析构完成后禁止调用。需要处理退出期时，先使用 `isDestroyed()` 或显式指针转换。

#### `QGlobalStatic<Holder>::Type &QGlobalStatic::operator*()`

以引用形式访问对象。未创建时会初始化。

它同样不替你检查对象是否已经销毁；析构完成后得到的引用无效，调用前必须确保对象仍然存活。

### 宏

#### `Q_GLOBAL_STATIC(Type, variableName, ...)`

在全局作用域创建一个惰性、线程安全初始化的 `QGlobalStatic` 变量：

- `Type` 是实际对象类型；
- `variableName` 是 wrapper 变量名；
- 后续参数从 Qt 6.3 起作为构造参数传给 `Type`；
- 宏必须放在源文件，不能放头文件、函数体或类体；
- `Type` 的相关构造函数和析构函数必须满足访问性要求。

它适合非 POD、构造有成本或存在静态初始化顺序风险的全局对象。对平凡类型或 constexpr 构造类型，普通 `static` 往往更简单且开销更低。

#### `[obsolete] Q_GLOBAL_STATIC_WITH_ARGS(Type, variableName, (args))`

旧的带参数宏形式。新代码使用 `Q_GLOBAL_STATIC(Type, variableName, args...)`，不再需要额外的参数括号。保留旧形式主要是为了兼容已有 Qt 代码。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QGlobalStatic::Type` | 宏中实际类型的别名 | 不是新的对象类型 |
| `exists()` | 查询是否已初始化且仍存活 | 不触发创建；不提供通用内存同步 |
| `isDestroyed()` | 查询析构是否完成 | 未创建不等于已销毁 |
| `operator Type *()` | 取得指针 | 未创建会初始化；销毁后返回 null |
| `operator()()` | 显式取得指针 | 与指针转换相同，适合显式代码 |
| `operator->()` | 箭头访问 | 销毁后断言/悬空，不应使用 |
| `operator*()` | 引用访问 | 销毁后引用无效 |
| `Q_GLOBAL_STATIC(Type, name, ...)` | 定义惰性全局对象 | 只能放源文件全局作用域 |
| `Q_GLOBAL_STATIC_WITH_ARGS(...)` | 旧带参数宏 | 新代码用可变参数 `Q_GLOBAL_STATIC` |

## 10. 推荐与不推荐做法

### 推荐

- 在 `.cpp` 文件的全局作用域声明；
- 保持全局对象构造函数简单；
- 访问前明确是否允许第一次使用触发构造；
- 退出期代码检查 `isDestroyed()`；
- 把对象内部的并发安全单独设计。

### 不推荐

- 把宏放进头文件；
- 在 `Type` 构造函数里访问另一个有复杂依赖的 `Q_GLOBAL_STATIC`；
- 把 `operator->()` 当作退出期安全访问；
- 用 `exists()` 代替原子或互斥同步；
- 对 POD 或平凡 constexpr 类型滥用宏；
- 在全局静态构造期间执行可能回到自身的同步调用。

## 11. 排查顺序

1. 每个 `.cpp` 看到一份不同缓存：检查宏是否误放在头文件。
2. 程序启动时出现意外构造：检查是否在静态初始化阶段通过指针运算符访问了对象。
3. 多线程首次访问卡住：检查构造函数是否自依赖或和另一个全局对象交叉依赖。
4. 退出阶段崩溃：检查是否在 `isDestroyed()` 为真后仍使用 `operator->()` 或 `operator*()`。
5. 线程安全误判：区分“只初始化一次”与 `Type` 内部状态的读写安全。
6. 构造参数编译失败：确认 Qt 版本、参数顺序以及 `Type` 的公开构造函数。
