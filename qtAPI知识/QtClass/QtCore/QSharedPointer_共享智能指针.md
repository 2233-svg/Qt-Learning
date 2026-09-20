# Qt QSharedPointer：共享对象生命周期

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSharedPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：共享所有权、引用计数智能指针

## 1. 它解决什么问题

`QSharedPointer<T>` 用一个位于对象外部的控制块记录强引用数量和删除策略。多个 `QSharedPointer` 可以指向同一个对象；最后一个强引用销毁或清空时，控制块调用删除器释放对象。

它适合：

- 异步任务和调用方共同持有一份状态；
- 缓存、队列和当前操作共同使用同一个对象；
- 工厂返回对象，但调用方不希望手工 `delete`；
- 需要弱引用观察对象，却不希望观察者延长生命周期。

它不表示对象内容被复制，也不提供写时复制。所有强引用看到的是同一个 `T` 对象。若需要隐式共享数据，应考虑 `QSharedDataPointer`，而不是把 `QSharedPointer` 当作容器值类型。

## 2. 所有权模型

```cpp
auto first = QSharedPointer<Record>::create();
auto second = first;       // 共享同一个控制块和 Record

first.clear();             // Record 仍由 second 保持
second.clear();            // 最后一个强引用清空，Record 被销毁
```

从裸指针构造会转移删除责任：

```cpp
Record *raw = new Record;
QSharedPointer<Record> owner(raw); // owner 接管 raw
// 不要再 delete raw，也不要用 raw 创建另一个 QSharedPointer
```

下面的写法会创建两个互不认识的控制块，最后很可能对同一对象执行两次删除：

```cpp
Record *raw = new Record;
QSharedPointer<Record> a(raw);
QSharedPointer<Record> b(raw); // 错误：重复接管同一个裸指针
```

如果对象已经由 `QSharedPointer` 管理，需要从对象内部取得共享指针，应使用 `QEnableSharedFromThis::sharedFromThis()`，不能重新写 `QSharedPointer<T>(this)`。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QSharedPointer>

struct JobState
{
    int completed = 0;
};

QSharedPointer<JobState> makeState()
{
    return QSharedPointer<JobState>::create();
}

void updateState(QSharedPointer<JobState> state)
{
    if (!state)
        return;

    ++state->completed;
}
```

`create()` 会构造一个新的 `T`，并把对象与 `QSharedPointer` 的内部数据尽量放在一次分配中。构造参数会完美转发给 `T`。

## 4. 实际使用场景

### 4.1 跨异步边界保持状态有效

```cpp
QSharedPointer<ExportState> state = QSharedPointer<ExportState>::create();

enqueue([state] {
    state->result = buildResult();
});
```

lambda 捕获的是一个新的强引用。只要队列中的任务还保存它，`ExportState` 就不会提前销毁。

### 4.2 多个组件共享同一对象

```cpp
QSharedPointer<Session> session = QSharedPointer<Session>::create();
cache.insert(id, session);
controller->setSession(session);
```

这里的前提是这些组件确实需要共同延长生命周期。若某个组件只是“有机会使用”，应保存 `QWeakPointer`，在使用时提升为强引用。

### 4.3 QObject 的延迟销毁

如果最后一个强引用可能在不适合直接删除 QObject 的线程中释放，可以使用自定义删除器：

```cpp
#include <QSharedPointer>
#include <QObject>

auto object = QSharedPointer<QObject>(
    new QObject,
    &QObject::deleteLater
);
```

删除器只在强引用数量降为零时调用。`deleteLater()` 仍依赖对象所属线程的事件循环；没有机会处理 deferred delete 时，不能把它当作立即销毁。

QObject parent 也会负责删除子对象。不要同时让 parent-child 对象树和 `QSharedPointer` 独立拥有同一个对象，否则两个所有权体系可能重复删除。

## 5. 线程与重入边界

`QSharedPointer` 和 `QWeakPointer` 的引用计数是原子的，**不同的指针包装对象**可以在多个线程中同时操作，即使它们指向同一个 `T`：

```cpp
QSharedPointer<JobState> shared = QSharedPointer<JobState>::create();
// 把 shared 的副本分别交给不同线程是安全的
```

但同一个 `QSharedPointer` 变量同时被一个线程写入、另一个线程读取，仍然需要同步：

```cpp
// shared 同时 reset 和读取，不能仅靠 QSharedPointer 保证安全
shared.reset();
use(shared.data());
```

引用计数安全也不等于 `T` 的成员访问安全。`T` 是否可并发访问，仍由 `T` 自己的线程约束、互斥和原子协议决定。

## 6. 空状态、裸指针和失效边界

- 默认构造、`nullptr` 构造和 `clear()` 后都是空指针；
- `data()` / `get()` 只借出裸指针，不转移所有权；
- 不能删除 `data()` 返回的指针，也不能把它交给另一个拥有型智能指针；
- `operator->()`、`operator*()` 在空指针上使用是未定义行为；
- `isNull()` 和 `operator bool()` 只判断当前包装对象是否为空，不检查 `T` 的业务状态。

若需要在一段代码内保证对象不被最后释放者销毁，应先复制或提升出一个强引用，并保存该强引用：

```cpp
QSharedPointer<JobState> keepAlive = maybeWeak.toStrongRef();
if (!keepAlive)
    return;

use(*keepAlive);
```

## 7. 转换 API 的选择

| API | 底层转换 | 失败时 | 适合情况 |
| --- | --- | --- | --- |
| `staticCast<X>()` | `static_cast` | 不做运行时类型检查 | 已经证明类型关系，通常用于向上转换 |
| `dynamicCast<X>()` | `dynamic_cast` | 返回空 `QSharedPointer<X>` | 多态层次中的运行时检查 |
| `objectCast<X>()` | `qobject_cast` | 返回空 `QSharedPointer<X>` | `QObject` 元对象类型转换 |
| `constCast<X>()` | `const_cast` | 通常不因类型关系失败 | 确认对象原本可写时去除 const |

这些转换返回的指针仍共享原控制块，不会复制对象，也不会产生第二次删除责任。右值重载自 Qt 6.9 起提供；成功后会把源右值指针重置为空。

```cpp
QSharedPointer<Base> base = QSharedPointer<Derived>::create();
QSharedPointer<Derived> derived = base.dynamicCast<Derived>();
if (derived)
    derived->run();
```

`staticCast` 只适合类型关系已经被程序逻辑证明的路径，不能代替对不确定动态类型的检查。

## 8. 指针值比较与控制块比较

普通 `operator==` / `operator!=` 比较当前保存的指针值。Qt 6.7 起的 `owner_equal()`、`owner_before()` 和 `owner_hash()` 比较的是共享所有权关系，也就是控制块，而不是当前裸指针值。

```cpp
QSharedPointer<Base> base = QSharedPointer<Derived>::create();
auto derived = base.dynamicCast<Derived>();

Q_ASSERT(base == base.data());
Q_ASSERT(base.owner_equal(derived)); // 共享同一个控制块
```

这组 API 适合构建“按所有权分组”的容器或排序关系。`qHash(QSharedPointer)` 则是普通指针值的哈希辅助，不等同于 `owner_hash()`。

## 9. 常见错误

### 9.1 从同一个裸指针建立多个控制块

裸指针一旦交给一个 `QSharedPointer`，就不能再次交给另一个 owner。

### 9.2 把 QObject parent 和 QSharedPointer 同时当 owner

对象树删除和共享指针删除互不知情。需要共享 QObject 时，设计清楚谁拥有对象，或用不拥有的 `QPointer` 观察对象。

### 9.3 误以为 QSharedPointer 保护对象内容

它只保护销毁时机，不保护 `T` 的字段读写。多个线程修改同一对象仍需锁或其他同步方案。

### 9.4 保存 `data()` 返回值跨越异步边界

裸指针不延长生命周期。跨越回调、队列或线程边界时保存 `QSharedPointer` 副本。

### 9.5 对空指针直接解引用

先检查，或在逻辑上保证强引用非空后再使用 `operator->()` / `operator*()`。

### 9.6 用 QSharedPointer 表示复制语义

多个指针共享一个对象，不会自动复制内容。需要独立副本时显式复制 `T`。

## 10. 逐项 API 语义

### 构造、析构与赋值

#### `QSharedPointer()`

构造空的共享指针，不关联可访问对象。

#### `QSharedPointer(std::nullptr_t)`

构造空指针，语义与默认构造相同。

#### `QSharedPointer(X *ptr)`

接管 `ptr` 的删除责任。最后一个强引用释放时按 `X` 的类型销毁对象。`X *` 必须能够隐式转换为 `T *`，且 `ptr` 不能再被其他 owner 接管。

#### `QSharedPointer(X *ptr, Deleter d)`

接管 `ptr`，在强引用归零时调用自定义 `d`，而不是直接使用 `operator delete`。删除器接收 `X *`，所以可以使用 `&QObject::deleteLater` 或项目自己的资源回收函数。

#### `QSharedPointer(std::nullptr_t, Deleter d)`

构造空共享指针并保存删除策略，主要用于统一模板代码。空指针本身没有可释放对象。

#### `QSharedPointer(const QSharedPointer<T> &other)`

复制强引用，共享同一个对象和控制块，引用计数增加。

#### `QSharedPointer(const QSharedPointer<X> &other)`

在 `X *` 可转换为 `T *` 时复制兼容类型的共享引用。对象和控制块不变。

#### `QSharedPointer(QSharedPointer<T> &&other)`

移动共享引用，不增加引用计数；源对象被置为空。

#### `QSharedPointer(QSharedPointer<X> &&other)`

移动兼容类型的共享引用。要求 `X *` 能隐式转换为 `T *`。

#### `QSharedPointer(const QWeakPointer<T> &other)`

尝试把弱引用提升为强引用。对象已经销毁时结果为空，不能假设一定成功。

#### `~QSharedPointer()`

释放一个强引用。若这是最后一个强引用，调用控制块保存的删除器。

#### `operator=(const QSharedPointer<T> &other)`

共享 `other` 的控制块，再释放当前引用。若当前引用是最后一个，会在赋值过程中销毁旧对象。

#### `operator=(const QSharedPointer<X> &other)`

对兼容类型执行复制赋值，当前对象切换到 `other` 的共享所有权。

#### `operator=(QSharedPointer<T> &&other)`

移动赋值，接收 `other` 的共享引用并使 `other` 为空。

#### `operator=(QSharedPointer<X> &&other)`

兼容类型的移动赋值。要求 `X *` 可以隐式转换到 `T *`。

#### `operator=(const QWeakPointer<T> &other)`

尝试提升弱引用并替换当前强引用。提升失败时结果为空，应检查当前指针后再使用。

### 生命周期和访问

#### `clear()`

放弃当前强引用。若没有其他强引用，进入删除器流程。

#### `reset()`

`clear()` 的标准库兼容名称。

#### `reset(T *t)`

用默认删除策略接管 `t`，语义等价于先构造临时 `QSharedPointer<T>(t)` 再交换。新对象必须尚未被其他 owner 接管。

#### `reset(T *t, Deleter deleter)`

用指定删除器接管 `t`，再替换当前控制块。

#### `data() const`

返回当前保存的 `T *`，不转移所有权。返回值不能被 `delete`，也不应交给另一个拥有型智能指针。

#### `get() const`

与 `data()` 相同，为兼容 `std::shared_ptr` 提供的命名。

#### `isNull() const`

当前没有有效指针时返回 `true`。

#### `operator bool() const`

当前指针非空时为 `true`，适合用于 `if`。

#### `operator!() const`

当前指针为空时为 `true`。

#### `operator*() const`

返回对象引用。空指针上解引用是未定义行为。

#### `operator->() const`

返回对象指针以访问成员。空指针上访问是未定义行为。

#### `swap(QSharedPointer<T> &other)`

交换两个共享指针的保存关系，操作快速且不改变对象本身。

#### `toWeakRef() const`

创建指向同一控制块的 `QWeakPointer<T>`，不增加强引用数量。

### 转换和所有权比较

#### `staticCast<X>() const &` / `staticCast<X>() &&`

使用 `static_cast` 转换保存的指针，同时共享原控制块。右值重载自 Qt 6.9 起提供；不做运行时检查。

#### `dynamicCast<X>() const &` / `dynamicCast<X>() &&`

使用 `dynamic_cast` 进行运行时多态转换。转换失败返回空共享指针；右值重载自 Qt 6.9 起提供。

#### `objectCast<X>() const &` / `objectCast<X>() &&`

对 `QObject` 使用 `qobject_cast`。转换失败返回空共享指针；右值重载自 Qt 6.9 起提供。

#### `constCast<X>() const &` / `constCast<X>() &&`

使用 `const_cast` 调整 const/volatile 限定，同时共享控制块。只有在底层对象原本确实允许修改时才可以去除 const。

#### `owner_before(const QSharedPointer<X> &other)`

Qt 6.7 起提供实现定义的控制块排序。两个空指针或共享同一所有权的指针在这种排序中视为等价。

#### `owner_before(const QWeakPointer<X> &other)`

Qt 6.7 起，和弱引用比较控制块排序。

#### `owner_equal(const QSharedPointer<X> &other)`

Qt 6.7 起，判断两个智能指针是否共享所有权，而不是只判断裸指针地址。

#### `owner_equal(const QWeakPointer<X> &other)`

Qt 6.7 起，判断当前强引用和弱引用是否指向同一控制块。

#### `owner_hash() const`

Qt 6.7 起返回基于控制块所有权的哈希值。`owner_equal()` 为真时，哈希值相同。

### 静态和相关非成员 API

#### `QSharedPointer<T>::create(Args &&... args)`

分配并构造一个 `T`，返回管理它的共享指针。参数完美转发给 `T` 的构造函数。

#### `qSharedPointerCast<X>(...)`

相关静态转换函数，可接受强引用左值、强引用右值或弱引用。弱引用版本会先提升，失败时返回空；右值版本自 Qt 6.9 起提供并在成功后清空源。

#### `qSharedPointerDynamicCast<X>(...)`

相关动态转换函数。失败或弱引用提升失败时返回空。

#### `qSharedPointerConstCast<X>(...)`

相关 const 转换函数。弱引用版本先提升；右值版本自 Qt 6.9 起提供。

#### `qSharedPointerObjectCast<X>(...)`

相关 `qobject_cast` 转换函数。只适用于 QObject 元对象体系；弱引用版本先提升。

#### `qHash(const QSharedPointer<T> &key, size_t seed)`

根据共享指针的普通指针值计算哈希，可用于 `QHash` 等哈希容器。它不是 `owner_hash()`。

#### 比较运算符 `==` / `!=`

可比较两个兼容类型的 `QSharedPointer`、共享指针与兼容裸指针、以及与 `nullptr` 的关系。比较的是保存的指针值，不是控制块。

#### `operator<<(QDebug, const QSharedPointer<T> &ptr)`

把共享指针跟踪的指针值写入调试输出，不输出对象内容。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSharedPointer()` / `QSharedPointer(nullptr)` | 创建空共享指针。 | 没有对象，也没有成员访问入口。 |
| 接管 | `QSharedPointer(X *)` | 接管裸指针并默认删除。 | 一个裸指针只能交给一个控制块。 |
| 接管 | `QSharedPointer(X *, Deleter)` | 接管裸指针并使用自定义删除器。 | 删除器在最后一个强引用释放时调用。 |
| 复制 | `QSharedPointer(other)` | 共享同一控制块。 | 不复制 `T` 对象。 |
| 移动 | `QSharedPointer(std::move(other))` | 转移包装对象中的共享引用。 | 源对象变空。 |
| 弱化 | `toWeakRef()` | 创建不拥有对象的弱引用。 | 弱引用不延长生命周期。 |
| 工厂 | `create(args...)` | 创建并构造 `T`。 | 参数转发给 `T` 构造函数。 |
| 访问 | `data()` / `get()` | 借出裸指针。 | 不转移所有权，不要 `delete`。 |
| 查询 | `isNull()` / `operator bool()` | 判断当前是否为空。 | 非空只代表当前强引用有对象。 |
| 清空 | `clear()` / `reset()` | 释放当前强引用。 | 最后一个强引用会触发删除器。 |
| 替换 | `reset(T *)` | 用默认策略接管新对象。 | 新对象必须尚未被其他 owner 接管。 |
| 替换 | `reset(T *, Deleter)` | 用自定义删除器接管新对象。 | 适合 `deleteLater` 等销毁策略。 |
| 解引用 | `operator*` / `operator->` | 访问 `T`。 | 空指针上使用是未定义行为。 |
| 转换 | `staticCast<X>()` | 静态类型转换并共享控制块。 | 不做运行时检查。 |
| 转换 | `dynamicCast<X>()` | 运行时多态转换。 | 失败返回空；保持 cv 限定。 |
| 转换 | `objectCast<X>()` | 使用 `qobject_cast`。 | 只适用于 QObject 元对象类型。 |
| 转换 | `constCast<X>()` | 调整 const/volatile 限定。 | 去 const 前确认底层对象可写。 |
| 所有权比较 | `owner_equal()` | 比较控制块是否相同。 | 与普通 `operator==` 不同；Qt 6.7 起。 |
| 所有权排序 | `owner_before()` | 建立控制块排序。 | 不表示对象地址大小规律；Qt 6.7 起。 |
| 所有权哈希 | `owner_hash()` | 计算控制块哈希。 | 与 `qHash()` 不是一回事；Qt 6.7 起。 |
| 交换 | `swap()` | 交换两个共享指针的关系。 | 不改变对象和控制块。 |
| 比较 | `==` / `!=` | 比较指针值或空状态。 | 不比较共享所有权关系。 |
| 哈希 | `qHash()` | 对普通指针值计算哈希。 | 不等同于 owner-based 哈希。 |

---

### 一句话总结

`QSharedPointer` 通过共享控制块管理对象生命周期：复制它会共享所有权，最后一个强引用才触发删除；最重要的边界是不要重复接管同一个裸指针，也不要把引用计数安全误认为对象内容的线程安全。

