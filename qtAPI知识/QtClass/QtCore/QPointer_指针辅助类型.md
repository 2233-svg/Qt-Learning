# Qt QPointer：自动归零的 QObject 观察指针

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：非拥有、可观察 QObject 生命周期的弱指针  
> 关联类型：`QObject`、`QWeakPointer`

## 1. 它解决什么问题

`QPointer<T>` 保存一个 `QObject` 派生对象的弱引用。当目标对象被销毁时，`QPointer` 会自动变为空指针，避免继续使用已经悬空的 QObject 地址：

```cpp
QPointer<QWidget> dialog = new QWidget;
dialog->deleteLater();

// 事件循环处理删除后：
if (dialog)
    dialog->show();       // 只有目标仍存在时才访问
```

它适合“对象可能在别处被销毁，但我还想保留一个可检查的引用”的场景，例如：

- 非模态对话框或临时窗口；
- 异步请求完成时，目标控件可能已关闭；
- 延迟回调、事件过滤器或任务对象保存可选 QObject；
- 观察由 parent 所有、但不由当前函数管理的对象。

`QPointer` 只解决“目标 QObject 是否还存在”的问题，不解决线程同步、业务状态一致性或回调是否应该继续执行。

## 2. 它不拥有对象

`QPointer` 不会在析构时 `delete` 目标对象，也不会改变目标对象的 parent：

```cpp
auto *object = new QObject;
QPointer<QObject> guard = object;

guard.clear(); // 只清除 guard，不销毁 object
delete object; // 由真正的 owner 负责
```

对象通常由以下机制之一拥有：

- QObject parent-child 对象树；
- 明确的 `delete` / `deleteLater()`；
- 其他专门的所有权管理方案。

不要把 `QPointer` 当作 `std::unique_ptr` 或 `QSharedPointer`。如果当前代码需要负责销毁对象，使用明确的拥有型指针；如果只需要随对象销毁自动失效，使用 `QPointer`。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QPointer>
#include <QTimer>
#include <QWidget>

void showLater(QWidget *widget)
{
    QPointer<QWidget> watched = widget;
    QTimer::singleShot(500ms, widget, [watched] {
        if (watched)
            watched->show();
    });
}
```

如果延迟回调以目标对象作为 context，context 销毁本身就会自动断开回调；`QPointer` 仍适合跨越多个调用层、保存可选对象状态，或保护不以该对象作为连接 context 的代码。

## 4. 目标类型要求与转换

`QPointer<T>` 的 `T` 必须是 `QObject` 派生类型，不能再写一层裸指针：

```cpp
QPointer<QWidget> good;
// QPointer<QWidget *> bad; // T 不能是指针类型
```

Qt 6.6 起支持从可转换的 `QPointer<X>` 构造或赋值到 `QPointer<T>`，方向与裸指针隐式转换一致：

```cpp
QPointer<QPushButton> button = new QPushButton;
QPointer<QWidget> widget = button; // 派生类 -> 基类
```

反向转换需要显式使用 `qobject_cast` 或通过目标类型指针重新构造，不能依靠不安全的静态向下转换。

`QPointer<const T>` 可以观察 const QObject，但不能把它当作修改对象的入口。模板参数的 const 性会体现在 `data()`、`operator->()` 和隐式转换的返回类型中。

## 5. 生命周期语义

### 5.1 目标销毁后自动归零

当 QObject 开始销毁时，Qt 的对象销毁机制会使指向它的 `QPointer` 变为空：

```cpp
QPointer<QObject> watched = object;
delete object;
Q_ASSERT(watched.isNull());
```

因此每次跨越事件循环、异步任务或未知调用后，都应重新检查指针，而不是只在最初赋值时检查一次。

### 5.2 检查不是永久保证

```cpp
if (watched)
    watched->doSomething();
```

这只表示检查瞬间目标非空。若多个线程或重入代码可能销毁对象，检查和使用之间仍需遵守 QObject 线程规则，并设计合适的同步或串行化协议。

Qt 的 QObject 通常不允许跨线程直接操作；`QPointer` 变为空也不表示对跨线程访问自动加锁。

### 5.3 `deleteLater()` 的时间边界

调用 `deleteLater()` 后，目标通常仍存在到事件循环处理 deferred delete 事件为止。此期间 `QPointer` 可能仍非空，但业务上对象已经进入销毁流程：

- 不要仅依赖 `QPointer` 判断“对象是否还应该接受新工作”；
- 必要时另外维护关闭/取消状态；
- 在跨线程和异步流程中优先使用 context 连接或显式取消协议。

## 6. 查询和解引用

```cpp
QPointer<QObject> watched = object;

if (!watched.isNull()) {
    QObject *raw = watched.data();
    raw->setObjectName("active");
}
```

常见写法：

- `if (watched)`：快速判断非空；
- `watched.isNull()`：判断为空；
- `watched.data()` 或 `watched.get()`：取裸指针；
- `watched->member()`：直接访问成员，但前提是当前状态非空；
- `*watched`：解引用为对象引用，前提同上。

`operator->()`、`operator*()` 不会在空指针时抛出异常；空时解引用是未定义行为。不要为了省一行 `if` 而直接访问可能已销毁的对象。

## 7. 赋值、清空和交换

### 7.1 赋裸指针

```cpp
QPointer<QObject> watched;
watched = object;
watched = nullptr;
```

赋值只改变观察目标，不转移对象所有权。若新指针不是 QObject 或不符合 `T` 的转换关系，代码无法通过编译。

### 7.2 `clear()`

`clear()` 只清空当前弱指针。它不会发出信号、不会销毁 QObject，也不会影响其他 `QPointer`。

### 7.3 `swap()`

```cpp
watched.swap(other);
swap(watched, other);
```

交换的是两个观察关系，目标 QObject 不发生任何变化。

## 8. 典型使用场景

### 8.1 保护延迟 UI 操作

```cpp
class Controller : public QObject
{
public:
    void openEditor()
    {
        if (!m_editor)
            m_editor = new Editor;

        QPointer<Editor> editor = m_editor;
        QTimer::singleShot(100ms, this, [editor] {
            if (editor)
                editor->raise();
        });
    }

private:
    QPointer<Editor> m_editor;
};
```

这里成员 `m_editor` 只观察 editor；真正的 owner 可以是对象树或其他明确的管理者。

### 8.2 异步结果返回时检查接收对象

```cpp
QPointer<QWidget> target = widget;
connect(reply, &QNetworkReply::finished, this, [target, reply] {
    if (!target)
        return;

    target->setProperty("loaded", true);
    reply->deleteLater();
});
```

如果连接 context 不是 target，`QPointer` 可以避免 target 关闭后继续解引用。仍需处理 reply 生命周期、线程归属和回调取消语义。

### 8.3 观察由 parent 管理的临时对象

```cpp
QPointer<QObject> child = parent->findChild<QObject *>();
if (child)
    child->setObjectName("found");
```

`findChild()` 返回的裸指针不转移所有权；需要跨越后续调用保存时，`QPointer` 比长期保存裸指针更稳妥。

## 9. 与其他指针类型的选择

| 类型 | 是否拥有 | 目标销毁后 | 适合场景 |
| --- | --- | --- | --- |
| 裸 `T *` | 不明确 | 仍是悬空地址 | 明确受短作用域或外部协议保护的临时访问 |
| `QPointer<T>` | 否 | 自动变空 | 观察 QObject 生命周期 |
| `std::unique_ptr<T>` | 是 | owner 销毁对象 | 独占所有权；QObject parent 关系需谨慎 |
| `QSharedPointer<T>` | 共享 | 引用归零时销毁 | 非 QObject 或明确共享所有权 |
| `QWeakPointer<T>` | 否 | 可升级/检查 | 配合 `QSharedPointer` 的共享对象 |

QObject 对象树和 `QSharedPointer` 同时管理同一对象通常会造成重复释放。`QPointer` 适合作为观察层，不参与销毁决策。

## 10. 线程与异步边界

`QPointer` 的自动归零依赖 QObject 的生命周期机制，但它不是跨线程安全的对象访问协议：

- 不能因为 pointer 会自动归零，就从任意线程调用目标 QObject；
- 不能把“非空”当作跨线程调用授权；
- queued 调用执行时仍应重新判断对象状态；
- 线程退出、对象移动和 `deleteLater()` 要按 QObject 事件循环规则安排。

在同一线程中，重入也可能导致目标销毁。将多个操作拆开或发出信号后，下一段代码应重新检查 `QPointer`。

## 11. 常见错误

### 11.1 误以为 QPointer 会删除对象

它只会观察和归零，不负责释放。需要 owner 时选择拥有型指针或对象树。

### 11.2 只在创建时检查一次

目标可能在后续事件、信号或异步回调中被销毁。跨越边界后重新检查。

### 11.3 空指针直接 `operator->()` 或 `operator*()`

空时解引用是未定义行为。使用 `if (pointer)` 或 `data()` 检查。

### 11.4 把 QPointer 当作线程同步

自动归零不等于原子业务操作，不保护成员数据，也不能替代 queued connection、锁或取消协议。

### 11.5 用 QPointer 表示“业务对象仍有效”

QObject 可能仍存在但已关闭、正在销毁或不再接受任务。生命周期有效和业务可用是两个状态。

### 11.6 与 QObject parent 和 shared pointer 重复拥有

同一个对象只能有清晰的销毁责任。`QPointer` 不增加 owner，但 `QSharedPointer` 和 parent 同时拥有则可能重复释放。

## 12. 逐项 API 语义

### `QPointer()`

默认构造空的观察指针，`isNull()` 为 `true`。它不关联 QObject，也不注册任何销毁回调以外的资源。

### `QPointer(std::nullptr_t)`

构造空观察指针，语义与默认构造相同。

### `QPointer(T *p)`

从 QObject 裸指针建立观察关系。它不取得所有权；若 `p` 已经为空，结果为空。

### `QPointer(const QPointer<X> &other)`

Qt 6.6 起，从可转换的其他 `QPointer<X>` 复制观察关系。目标对象不变，仍由原 owner 管理。

### `QPointer(QPointer<X> &&other)`

Qt 6.6 起，从可转换的其他 `QPointer<X>` 移动观察关系。源 QPointer 被清空，目标 QPointer 接管观察关系；QObject 本身不受影响。

### `~QPointer()`

销毁弱指针对象，不销毁目标 QObject。目标仍可被其他 owner 或 observer 使用。

### `operator=(const QPointer<X> &other)`

Qt 6.6 起，复制可转换的观察关系到当前对象。当前观察目标被替换，QObject 所有权不变。

### `operator=(QPointer<X> &&other)`

Qt 6.6 起，移动可转换的观察关系。源对象被清空，当前对象观察新目标。

### `operator=(T *p)`

把当前观察目标替换为 `p`。赋值不删除旧目标，也不获取新目标的所有权。

### `data() const`

返回当前目标的 `T *`；目标已销毁或当前为空时返回 `nullptr`。

### `get() const`

Qt 6.0 起，返回与 `data()` 相同的裸指针，命名更接近标准智能指针。仍然不转移所有权。

### `operator T *() const`

隐式转换为 `T *`，便于传给接受裸指针的函数。隐式转换也可能让代码不明显地丢失生命周期检查，新代码在复杂表达式中可显式使用 `data()`。

### `operator->() const`

返回当前目标指针以访问成员。空指针上调用是未定义行为，不能代替空检查。

### `operator*() const`

返回当前目标对象引用。空指针上解引用是未定义行为。

### `isNull() const`

判断当前是否没有有效目标。目标销毁后 Qt 会自动使它变为 `true`。

### `operator bool() const`

在条件语句中判断是否有非空目标，等价于 `!isNull()` 的布尔语义：

```cpp
if (watched)
    watched->update();
```

它只表示当前观察指针非空，不表示线程和业务状态都允许调用。

### `clear()`

清除当前观察关系，使指针为空。不会销毁目标，也不影响其他 `QPointer`。

### `swap(QPointer &other)`

交换两个 `QPointer` 的观察关系，不改变 QObject 本身的生命周期或 parent。

### `swap(QPointer<T> &, QPointer<T> &)`

非成员交换函数，调用成员 `swap()`，适合泛型代码和标准 `swap` 习惯。

### 比较运算符

Qt 为 `QPointer` 提供与 `nullptr`、裸指针和可转换 `QPointer` 的相等/不等比较。比较的是当前裸指针地址，不会比较 QObject 内容，也不会延长对象生命周期：

```cpp
if (watched == object) {
    // 当前仍观察同一个地址
}
```

比较结果不能替代后续对目标对象状态和线程归属的检查。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPointer()` | 创建空观察指针。 | 不拥有对象，`isNull()` 为 `true`。 |
| 构造 | `QPointer(std::nullptr_t)` | 创建空观察指针。 | 与默认构造相同。 |
| 构造 | `QPointer(T *)` | 观察一个 QObject 派生对象。 | 不转移所有权；目标销毁后自动归零。 |
| 转换 | `QPointer(const QPointer<X> &)` | 从可转换的 QPointer 复制观察关系。 | Qt 6.6 起；通常是派生类到基类。 |
| 转换 | `QPointer(QPointer<X> &&)` | 移动观察关系。 | Qt 6.6 起；源 QPointer 被清空，QObject 不受影响。 |
| 生命周期 | `~QPointer()` | 销毁观察指针对象。 | 不删除目标 QObject。 |
| 赋值 | `operator=(const QPointer<X> &)` | 复制其他观察关系。 | Qt 6.6 起；覆盖当前目标。 |
| 赋值 | `operator=(QPointer<X> &&)` | 移动其他观察关系。 | Qt 6.6 起；源对象之后为空。 |
| 赋值 | `operator=(T *)` | 替换观察目标。 | 不释放旧目标或拥有新目标。 |
| 查询 | `data()` | 返回当前 `T *`。 | 目标销毁后返回 `nullptr`。 |
| 查询 | `get()` | 返回当前 `T *`。 | Qt 6.0 起；与 `data()` 同义。 |
| 查询 | `isNull()` | 判断是否为空。 | 只反映当前生命周期观察状态。 |
| 查询 | `operator bool()` | 在条件中判断非空。 | 非空不等于业务可用或线程安全。 |
| 访问 | `operator->()` | 访问目标成员。 | 空时解引用是未定义行为。 |
| 访问 | `operator*()` | 获取目标引用。 | 空时解引用是未定义行为。 |
| 转换 | `operator T *()` | 隐式转为裸指针。 | 方便但可能隐藏生命周期检查，复杂代码可显式 `data()`。 |
| 清空 | `clear()` | 清除观察关系。 | 不销毁目标，也不影响其他观察者。 |
| 交换 | `swap()` / `swap(lhs, rhs)` | 交换观察关系。 | 目标 QObject 的 owner、parent 和线程不变。 |
| 比较 | `==` / `!=` | 比较当前指针地址。 | 与 nullptr、裸指针和可转换 QPointer 比较；不比较对象内容。 |

## 14. 一句话总结

`QPointer` 是 QObject 的非拥有弱指针：目标销毁后自动归零，适合保护跨事件和异步边界的对象访问；它不删除对象、不提供线程同步，也不能把“对象仍存在”当作“业务仍可用”。
