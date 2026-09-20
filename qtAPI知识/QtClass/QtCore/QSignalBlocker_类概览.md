# Qt QSignalBlocker：临时阻止 QObject 发出信号

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSignalBlocker>`  
> 所属模块：`Qt6::Core`  
> 类型性质：QObject 信号状态的 RAII 管理器  
> 相关类型：`QObject`、`QSignalBlocker`

## 1. 它解决什么问题

某些内部更新需要修改 QObject 的属性或模型状态，但不希望在更新过程中通知外部观察者。例如：

- 从多个控件同步一个表单值；
- 程序批量初始化界面，避免每次 `setValue()` 都触发槽；
- 更新模型内部字段时暂时阻止级联刷新；
- 在一次逻辑操作中合并多个变化，最后只发出一次显式通知。

手工保存和恢复 `signalsBlocked()` 状态容易在早退出路径上遗漏恢复。`QSignalBlocker` 把这段状态切换绑定到作用域：

```cpp
void setUiState(QSpinBox *spinBox, int value)
{
    QSignalBlocker blocker(spinBox);
    spinBox->setValue(value);
} // 恢复进入前的信号阻止状态
```

构造时调用 `QObject::blockSignals(true)`，析构时恢复构造前的状态。

## 2. 它不是什么

`QSignalBlocker` 不是：

- 信号连接的删除器；
- 槽函数的禁用器；
- 事件过滤器；
- 阻止 QObject 接收其他对象信号的开关；
- 线程同步工具；
- 取消已经排队投递信号的机制。

它只影响目标 QObject 自己发出的信号。`destroyed()` 信号是 Qt 的特殊例外，即使信号被阻止，QObject 销毁时也会发出该信号。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

`QSignalBlocker` 在 Qt 6.11.1 的公共声明位于 `QObject` 相关头文件中，使用文档指定的包含方式：

```cpp
#include <QSignalBlocker>
```

## 4. 最小可用代码

```cpp
#include <QSignalBlocker>
#include <QSpinBox>

void setValueSilently(QSpinBox *spinBox, int value)
{
    if (!spinBox)
        return;

    QSignalBlocker blocker(spinBox);
    spinBox->setValue(value);
}
```

如果目标对象进入函数前已经处于 blocked 状态，guard 析构时会恢复为 blocked，而不是强行打开信号。

## 5. 构造和析构的状态语义

### 5.1 构造保存旧状态并阻止信号

指针构造函数的核心行为等价于：

```cpp
m_blocked = object->blockSignals(true);
```

`QObject::blockSignals(bool)` 返回调用前的状态。因此 `m_blocked` 记录的是“进入作用域前是否已经阻止信号”，不是本次调用后状态。

如果对象原先未阻止信号，构造后变为阻止；如果对象原先已阻止信号，构造后仍然阻止。

### 5.2 析构恢复旧状态

```cpp
{
    QSignalBlocker blocker(object);
    object->setProperty("value", 42);
} // 等价于 object->blockSignals(进入前状态)
```

它不会简单地调用 `blockSignals(false)`。这一区别很重要，因为 guard 可能嵌套：

```cpp
{
    QSignalBlocker outer(object);
    {
        QSignalBlocker inner(object);
    } // 恢复为 outer 仍然阻止的状态
} // 恢复最初状态
```

### 5.3 目标 QObject 必须先于 blocker 销毁

`QSignalBlocker` 只保存裸指针，不监听 QObject 的销毁通知。若 blocker 比目标 QObject 活得更久，析构时会访问悬空指针，产生未定义行为：

```cpp
// 错误的生命周期关系
QSignalBlocker blocker(object);
delete object;
```

通常把 blocker 放在目标对象仍由外层拥有的局部作用域中即可。

## 6. `unblock()`、`reblock()` 和 `dismiss()`

### 6.1 `unblock()`：暂时恢复进入前状态

```cpp
QSignalBlocker blocker(object);
updateSilently();

blocker.unblock();
emitIntermediateNotification();
```

`unblock()` 调用 `blockSignals(m_blocked)`，把对象恢复到构造前的状态，并把内部标记设为 inhibited。此后 blocker 析构不会再次修改对象信号状态。

它不是永久释放 guard，也不是把状态固定为“允许信号”。如果对象进入前本来就是 blocked，`unblock()` 仍会恢复为 blocked。

### 6.2 `reblock()`：重新阻止信号

```cpp
blocker.unblock();
doSomethingThatMayEmit();
blocker.reblock();
```

`reblock()` 调用 `blockSignals(true)`，并恢复析构时自动恢复旧状态的行为。调用后离开作用域，QObject 会回到最初的 `m_blocked` 状态。

反复调用 `reblock()` 不会叠加计数；它只是确保当前处于阻止状态，并让析构恢复逻辑重新生效。

### 6.3 `dismiss()`：放弃后续恢复

```cpp
QSignalBlocker blocker(object);
object->setProperty("value", 42);
blocker.dismiss();
```

`dismiss()` 让 blocker 放弃目标 QObject 指针。之后析构不会恢复信号状态。此时对象会保持 `dismiss()` 调用时的状态，因此它不是“自动打开信号”的操作。

适合在调用方已经明确接管最终状态时使用，但应该谨慎，因为它打破了“作用域结束恢复旧状态”的默认保证。

## 7. 移动语义和不可复制

### 7.1 不可复制

复制 blocker 会产生两个对象都可能在析构时恢复同一个 QObject 的状态，因此复制构造和复制赋值被禁用。

### 7.2 移动构造转移恢复责任

```cpp
QSignalBlocker first(object);
QSignalBlocker second(std::move(first));
```

移动构造把目标指针、旧 blocked 状态和 inhibited 状态交给 `second`，并把 `first` 置为空。之后由 `second` 负责恢复，`first` 的析构不会再访问对象。

### 7.3 移动赋值的同对象边界

Qt 的移动赋值需要处理两个 blocker 可能指向同一个 QObject 的情况。它会根据双方的 inhibited 状态决定是否先恢复目标对象，再接管源状态。

虽然这个运算符可用，但实际代码中最好让一个 blocker 对应一个清晰作用域，避免在多个对象之间频繁转移信号状态责任。

## 8. 信号阻止的实际边界

### 8.1 阻止的是发出，不是连接

`QSignalBlocker` 不断开连接，也不改变接收者。离开作用域后原连接仍然存在。

### 8.2 不取消已经排队的通知

如果信号在阻止前已经通过队列连接投递，阻止信号通常不会撤销已经进入事件队列的调用。它主要影响目标 QObject 在阻止期间发出的信号。

因此不要把它当作“清空通知队列”的工具。

### 8.3 不阻止 `destroyed()`

QObject 的 `destroyed()` 信号即使在 `blockSignals(true)` 状态下也会发出。需要观察对象销毁时，不能依赖 `QSignalBlocker` 抑制它。

### 8.4 不保护数据一致性

阻止信号只是改变通知，不会阻止其他线程修改对象，也不会自动把多步状态更新变成原子操作。跨线程对象访问仍须遵守 QObject 线程规则和同步协议。

## 9. 与界面和模型更新协作

### 9.1 批量设置控件

```cpp
void Form::loadValues(const Values &values)
{
    QSignalBlocker a(firstSpinBox);
    QSignalBlocker b(secondSpinBox);

    firstSpinBox->setValue(values.first);
    secondSpinBox->setValue(values.second);

    refreshSummary();
}
```

控件不会因每个中间赋值都触发业务槽。作用域结束后，各控件恢复进入前的阻止状态；如果业务需要统一通知，应在状态完整后显式调用一次刷新逻辑。

### 9.2 嵌套更新

嵌套 blocker 会自然保存并恢复每一层的旧状态。不要在内层直接无条件 `blockSignals(false)`，否则会破坏外层 blocker 的保护。

### 9.3 目标对象可能为空

指针构造函数允许 `nullptr`，会产生不活动 blocker。它适合把可选对象纳入统一代码路径，但不能替代空指针检查，因为后续对空对象调用 `setValue()` 等操作仍然会失败。

## 10. 逐项 API 语义

### 10.1 `QSignalBlocker(QObject *object)`

```cpp
explicit QSignalBlocker(QObject *object) noexcept;
```

对象非空时保存旧状态并调用 `object->blockSignals(true)`；对象为空时不执行任何 QObject 操作。blocker 不拥有对象。

### 10.2 `QSignalBlocker(QObject &object)`

```cpp
explicit QSignalBlocker(QObject &object) noexcept;
```

引用版本始终有有效对象，保存其旧状态并立即阻止信号。引用对象必须在 blocker 析构前保持有效。

### 10.3 `QSignalBlocker(QSignalBlocker &&other)`

```cpp
QSignalBlocker(QSignalBlocker &&other) noexcept;
```

转移目标指针、进入前的 blocked 状态和当前 inhibited 状态。源对象被置为不再负责恢复。

### 10.4 `operator=(QSignalBlocker &&other)`

```cpp
QSignalBlocker &operator=(QSignalBlocker &&other) noexcept;
```

移动赋值并处理目标对象原有的恢复责任，随后接管源 blocker 的状态。复制赋值不可用。

### 10.5 `~QSignalBlocker()`

```cpp
~QSignalBlocker();
```

当目标非空且当前未被 `unblock()` / `dismiss()` 抑制恢复时，调用 `blockSignals(m_blocked)` 恢复进入前状态。

### 10.6 `unblock()`

```cpp
void unblock() noexcept;
```

恢复构造前的信号阻止状态，并让析构不再重复恢复。它不一定等价于 `blockSignals(false)`。

### 10.7 `reblock()`

```cpp
void reblock() noexcept;
```

重新调用 `blockSignals(true)`，并让析构恢复逻辑重新生效。

### 10.8 `dismiss()`

```cpp
void dismiss() noexcept;
```

从 blocker 中移除目标 QObject 指针，析构不再恢复信号状态。Qt 6.7 起提供。

## 11. 实际使用模式

### 11.1 静默填充表单

```cpp
void Editor::setDocument(const Document &document)
{
    QSignalBlocker blocker(this);
    titleEdit->setText(document.title);
    bodyEdit->setPlainText(document.body);
    updateButtons();
}
```

这里阻止的是 `Editor` 自己发出的信号；如果控件也会发出信号，需要分别阻止控件对象。

### 11.2 暂时恢复通知

```cpp
QSignalBlocker blocker(model);
model->setData(index, value);

blocker.unblock();
emit modelUpdated();
```

若目标对象进入前未阻止信号，`unblock()` 会恢复允许发信号的状态；析构不会再改变它。若需要继续静默更新，应在后续调用 `reblock()`。

### 11.3 取消自动恢复

```cpp
QSignalBlocker blocker(object);
configureFinalSignalState(object);
blocker.dismiss();
```

调用方明确负责最终状态时可以使用，但应把这段责任转移写得足够明显。

## 12. 常见错误

### 12.1 误以为 `unblock()` 总是打开信号

它恢复的是构造前状态。如果对象原先已经 blocked，`unblock()` 之后仍然 blocked。

### 12.2 误以为 blocker 会断开连接

连接不会被删除。blocker 只临时改变 QObject 的信号阻止状态。

### 12.3 目标对象先被销毁

blocker 不会自动跟踪 QObject 生命周期。确保目标对象比 blocker 活得更久，或在销毁目标前调用 `dismiss()`。

### 12.4 用信号阻止代替线程同步

阻止通知不等于保护共享数据，也不等于取消异步工作。数据竞争应由锁、消息传递或对象线程亲和性规则解决。

### 12.5 忽略 `destroyed()` 特例

即使信号被阻止，`destroyed()` 仍会发出。不能用 blocker 把对象销毁通知当作可选项关闭。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QSignalBlocker(QObject *)` | 保存旧状态并阻止目标对象信号 | `nullptr` 产生不活动 blocker；不拥有 QObject |
| `QSignalBlocker(QObject &)` | 引用版本的构造和阻止 | 引用对象必须覆盖 blocker 生命周期 |
| `QSignalBlocker(QSignalBlocker &&)` | 转移信号恢复责任 | 源对象不再恢复；不可复制 |
| `operator=(QSignalBlocker &&)` | 移动赋值并处理目标旧责任 | 同一 QObject 的嵌套状态要谨慎 |
| `~QSignalBlocker()` | 恢复构造前的 blocked 状态 | `unblock()` 或 `dismiss()` 后不再重复恢复 |
| `unblock()` | 恢复进入前状态并抑制析构恢复 | 不一定等于允许信号 |
| `reblock()` | 重新阻止信号并恢复析构恢复逻辑 | 不累计嵌套计数 |
| `dismiss()` | 放弃目标和自动恢复 | Qt 6.7 起；对象会保持当前状态 |

## 14. 一句话总结

`QSignalBlocker` 是 QObject 信号状态的 RAII 管理器：构造时保存旧状态并阻止信号，析构时恢复；`unblock()` 暂时恢复旧状态，`reblock()` 重新阻止，`dismiss()` 放弃自动恢复。它不删除连接、不取消已排队通知，也不提供线程同步。
