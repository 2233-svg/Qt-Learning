# Qt QWeakPointer：不延长生命周期的共享对象观察者

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWeakPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：配合 `QSharedPointer` 使用的非拥有弱引用

## 1. 它解决什么问题

`QWeakPointer<T>` 保存共享控制块的弱引用，但不增加强引用数量。它适合表达：

- “对象还活着时我可以使用它”；
- 缓存或索引只观察对象，不应阻止对象回收；
- 异步任务记录可选目标，执行时再决定是否继续；
- 避免两个对象通过强引用互相保持，导致生命周期环。

它不能直接解引用。必须调用 `toStrongRef()` 或 `lock()`，取得一个临时的 `QSharedPointer<T>`，再检查返回值：

```cpp
QSharedPointer<Item> item = weakItem.toStrongRef();
if (!item)
    return;

item->process();
```

这个强引用必须保存到局部变量中。只写 `if (!weakItem.isNull())` 再访问弱引用是不成立的，因为检查完成后对象仍可能被最后一个强引用释放。

## 2. 它和 QSharedPointer 的关系

`QWeakPointer` 只能从 `QSharedPointer` 或另一个 `QWeakPointer` 建立，不能从一个独立裸指针凭空构造有效弱引用：

```cpp
auto strong = QSharedPointer<Item>::create();
QWeakPointer<Item> weak = strong;

strong.clear(); // 如果没有其他强引用，Item 可立即销毁
auto again = weak.toStrongRef(); // 可能为空
```

弱引用本身只延长控制块的生命周期，不延长 `Item` 的生命周期。对象销毁后，控制块仍可能因为弱引用存在而保留，用于让后续提升安全地失败。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QSharedPointer>
#include <QWeakPointer>

QWeakPointer<Job> queuedTarget;

void submit(const QSharedPointer<Job> &job)
{
    queuedTarget = job;
}

void runLater()
{
    QSharedPointer<Job> job = queuedTarget.toStrongRef();
    if (!job)
        return;

    job->run();
}
```

## 4. 实际使用场景

### 4.1 缓存不阻止对象回收

```cpp
QHash<Key, QWeakPointer<Resource>> cache;

void useResource(const Key &key)
{
    QSharedPointer<Resource> resource = cache.value(key).toStrongRef();
    if (!resource) {
        resource = loadResource(key);
        cache.insert(key, resource);
    }

    resource->use();
}
```

缓存只保存观察关系。真正使用前通过提升得到强引用，保证 `resource->use()` 执行期间对象仍然存在。

### 4.2 避免双向强引用

```cpp
class Parent;

class Child
{
    QWeakPointer<Parent> parent;
};
```

如果 `Parent` 强引用 `Child`，`Child` 再强引用 `Parent`，二者都可能无法归零。反向关系通常应使用 `QWeakPointer`，除非业务上确实要求互相拥有。

### 4.3 异步回调的可选目标

```cpp
QWeakPointer<Controller> target;

enqueue([target] {
    QSharedPointer<Controller> controller = target.lock();
    if (!controller)
        return;

    controller->applyResult();
});
```

队列中的回调不会因为保存 `target` 而把控制器强行留到任务执行之后。回调运行时若控制器已经释放，任务自然结束。

## 5. `isNull()` 的瞬时语义

`isNull()`、`operator bool()` 和 `operator!()` 只能提供一次观察结果：

```cpp
if (!weak.isNull()) {
    // 这里不能直接访问 weak 指向的对象
}
```

在检查和后续提升之间，另一个线程可能释放最后一个强引用。因此可靠模式是直接提升，并检查返回的强引用：

```cpp
if (QSharedPointer<Item> item = weak.toStrongRef())
    item->process();
```

这不是“先判断再使用弱指针”，而是一次原子的强引用提升操作。提升成功后，局部 `item` 保证对象继续存活到该变量离开作用域。

## 6. 线程与对象访问边界

不同 `QWeakPointer` 包装对象可以在多个线程中使用，控制块中的引用计数操作是线程安全的。一个具体的 `QWeakPointer` 变量同时被读写，仍然需要外部同步。

弱引用的线程安全不代表 `T` 的成员访问安全：

- 提升成功只保证对象没有被共享指针销毁；
- 不保证 `T` 的成员数据可以被多个线程同时读写；
- 若 `T` 是 QObject，还必须遵守 QObject 的线程归属和事件循环规则；
- `QWeakPointer` 不能替代 mutex、queued connection 或任务取消协议。

## 7. 弱引用转换与比较

`qWeakPointerCast<X>()` 对兼容类型执行静态转换，并返回仍然是弱引用的 `QWeakPointer<X>`。它不会提升对象，也不会把弱引用变成强引用：

```cpp
QWeakPointer<Base> base = derived;
QWeakPointer<Derived> derivedAgain = qWeakPointerCast<Derived>(base);
```

普通 `operator==` / `operator!=` 支持弱引用与兼容的 `QSharedPointer`、以及弱引用与 `nullptr` 比较。Qt 6.11.1 没有提供两个 `QWeakPointer` 之间的普通 `==` / `!=` 重载；若要比较它们是否属于同一共享所有权，使用 `owner_equal()`。

Qt 6.7 起，`owner_equal()`、`owner_before()` 和 `owner_hash()` 面向共享控制块所有权。尤其是在多重继承或不同视图指针可能有不同地址时，控制块比较和裸指针比较不是同一个问题。

## 8. 常见错误

### 8.1 只检查 `isNull()`，不提升

弱引用没有稳定的解引用入口。必须保存 `toStrongRef()` / `lock()` 的返回值。

### 8.2 丢弃提升结果

```cpp
weak.toStrongRef()->run(); // 不推荐
```

虽然表达式可能在一次求值内工作，但没有清晰保存生命周期，也容易在复杂表达式中误用。使用局部强引用更可靠：

```cpp
auto strong = weak.toStrongRef();
if (strong)
    strong->run();
```

### 8.3 误以为 weak 会“锁住”对象

只有提升成功产生的 `QSharedPointer` 才会延长对象生命周期。原来的 `QWeakPointer` 始终不拥有对象。

### 8.4 从裸指针重新创建共享指针

弱引用提升失败时，不要用旧的裸指针或缓存地址重新构造 `QSharedPointer`。那会创建新的控制块，并可能产生悬空访问或重复删除。

### 8.5 把弱引用当作 QObject 的 QPointer

`QWeakPointer` 依赖 `QSharedPointer` 控制块，不能观察由 QObject parent 单独管理的对象。观察 QObject 对象树生命周期通常使用 `QPointer`。

## 9. 逐项 API 语义

### 构造、析构与赋值

#### `QWeakPointer()`

构造空弱引用，不关联控制块。

#### `QWeakPointer(const QSharedPointer<T> &other)`

从强引用创建弱引用。弱引用共享控制块，但不增加强引用数量。

#### `QWeakPointer(const QSharedPointer<X> &other)`

Qt 允许在兼容类型之间建立弱引用转换，要求 `X *` 可以隐式转换到 `T *`。

#### `QWeakPointer(const QWeakPointer<T> &other)`

复制弱引用，增加弱引用计数，不改变强引用数量。

#### `QWeakPointer(const QWeakPointer<X> &other)`

复制兼容类型的弱引用。对象不会因为复制弱引用而复活。

#### `QWeakPointer(QWeakPointer<T> &&other)`

移动弱引用，不增加计数；源弱引用变为空。

#### `QWeakPointer(QWeakPointer<X> &&other)`

移动兼容类型的弱引用，要求目标类型可由源类型转换得到。

#### `~QWeakPointer()`

释放弱引用。它不会删除被观察的对象；只有控制块中强引用和弱引用都消失时，控制块本身才可回收。

#### `operator=(const QSharedPointer<T> &other)`

让当前弱引用观察 `other` 的控制块。当前弱引用被替换，但旧对象不会因为这次赋值而删除。

#### `operator=(const QSharedPointer<X> &other)`

兼容类型的强引用到弱引用赋值。

#### `operator=(const QWeakPointer<T> &other)`

复制观察关系。旧弱引用关系被释放，目标对象生命周期不受影响。

#### `operator=(const QWeakPointer<X> &other)`

复制兼容类型的观察关系。

#### `operator=(QWeakPointer<T> &&other)`

移动观察关系，源变为空。

### 查询、提升和修改关系

#### `isNull() const`

若弱引用为空、强引用数量已经归零或保存的视图为空，返回 `true`。结果是瞬时观察值，下一次调用可能改变。

#### `operator bool() const`

当前观察结果非空时为 `true`。不能把它当作后续成员访问的生命周期保证。

#### `operator!() const`

当前观察结果为空时为 `true`，同样是瞬时检查。

#### `toStrongRef() const`

尝试原子地提升为 `QSharedPointer<T>`。成功时返回强引用并保证对象在该强引用存活期间不会因引用归零而销毁；失败时返回空共享指针。

#### `lock() const`

与 `toStrongRef()` 完全相同，为兼容 `std::weak_ptr` 提供的命名。

#### `clear()`

清除当前弱引用关系，不影响对象和其他强引用。

#### `swap(QWeakPointer<T> &other)`

交换两个弱引用的观察关系，不改变对象生命周期。

### 所有权比较

#### `owner_before(const QSharedPointer<X> &other)`

Qt 6.7 起按控制块建立实现定义的排序。它不表示裸指针地址大小规律。

#### `owner_before(const QWeakPointer<X> &other)`

Qt 6.7 起，按控制块比较两个弱引用的排序关系。

#### `owner_equal(const QSharedPointer<X> &other)`

Qt 6.7 起判断当前弱引用和强引用是否共享同一个控制块。

#### `owner_equal(const QWeakPointer<X> &other)`

Qt 6.7 起判断两个弱引用是否共享同一个控制块。

#### `owner_hash() const`

Qt 6.7 起返回基于控制块的哈希。所有权相等的智能指针哈希相同。

### 相关非成员 API

#### `qWeakPointerCast<X>(const QWeakPointer<T> &src)`

对弱引用保存的指针视图执行兼容的静态转换，返回 `QWeakPointer<X>`。它不提升强引用；类型关系或 cv 限定不满足时无法通过编译。

#### 比较运算符 `==` / `!=`

支持强引用与弱引用、以及弱引用与 `nullptr` 的比较。比较的是当前保存的指针值和空状态，不会把弱引用提升为强引用。两个弱引用之间要比较控制块关系时使用 `owner_equal()`。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QWeakPointer()` | 创建空弱引用。 | 不观察任何对象。 |
| 建立观察 | `QWeakPointer(shared)` | 从强引用建立弱引用。 | 不增加强引用数量。 |
| 复制 | `QWeakPointer(other)` | 复制观察关系。 | 不延长对象生命周期。 |
| 移动 | `QWeakPointer(std::move(other))` | 移动观察关系。 | 源弱引用变空。 |
| 查询 | `isNull()` | 判断当前是否观察到有效强对象。 | 结果瞬时，不能替代提升。 |
| 查询 | `operator bool()` / `operator!()` | 在条件中观察空状态。 | 不能直接解引用弱引用。 |
| 提升 | `toStrongRef()` | 尝试取得强引用。 | 必须保存返回值并检查是否为空。 |
| 提升 | `lock()` | `toStrongRef()` 的兼容命名。 | 语义相同。 |
| 清除 | `clear()` | 放弃弱观察关系。 | 不删除对象。 |
| 交换 | `swap()` | 交换两个弱引用。 | 不改变对象生命周期。 |
| 转换 | `qWeakPointerCast<X>()` | 转换弱引用的类型视图。 | 不提升，不做动态类型检查。 |
| 所有权比较 | `owner_equal()` | 比较控制块是否相同。 | 与普通指针值比较不同；Qt 6.7 起。 |
| 所有权排序 | `owner_before()` | 建立控制块排序。 | 不表示对象地址大小规律；Qt 6.7 起。 |
| 所有权哈希 | `owner_hash()` | 计算控制块哈希。 | 与裸指针哈希不是一回事；Qt 6.7 起。 |
| 比较 | `==` / `!=` | 比较当前指针值或空状态。 | 不会自动提升。 |

---

### 一句话总结

`QWeakPointer` 是共享对象的非拥有观察者：它不延长生命周期，也不能直接解引用；可靠使用方式始终是 `toStrongRef()` 或 `lock()`，保存并检查返回的 `QSharedPointer`。
