# Qt QDBusPendingReply 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusPendingReply>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QDBusPendingCall` → `QDBusPendingReplyBase` → `QDBusPendingReply<Types...>`

## 1. 它解决什么问题

异步 D-Bus 调用的原始回复是一组 `QVariant` 参数。若业务代码手动按下标取 `QVariant`、再逐个转换，远端接口一旦修改返回参数的个数或类型，错误往往会晚很久才暴露。

`QDBusPendingReply<Types...>` 给异步回复声明一份“类型契约”：模板参数就是预期的输出参数类型。它在调用完成后读取并校验回复；若参数个数或类型不匹配，会把这次结果转化为错误回复。

```cpp
QDBusPendingReply<QString, int> reply = iface.asyncCall("GetInfo");
```

上面代码表达的不是“返回两个 QVariant”，而是“协议规定 `GetInfo` 成功时必须返回一个 `QString` 和一个 `int`”。这种约束正是它解决的问题。

它与前两种结果类型的分工：

```text
QDBusPendingCall            只代表一次未完成调用
QDBusPendingReply<T...>     持有调用，并按 T... 校验、读取多个异步输出
QDBusReply<T>               读取同步或已完成调用的第一个输出
```

## 2. 构建与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

在需要阻塞等待的非 GUI 场景：

```cpp
#include <QDBusPendingReply>

QDBusPendingReply<QString, int> reply = iface.asyncCall("GetInfo");
reply.waitForFinished();

if (reply.isError()) {
    handleError(reply.error());
    return;
}

const QString name = reply.argumentAt<0>();
const int version = reply.argumentAt<1>();
```

`waitForFinished()` 返回后不代表远端调用成功，只表示回复已可检查。始终先判断 `isError()`，再读取 `value()` 或 `argumentAt<Index>()`。

## 3. 模板参数如何表达 D-Bus 协议

### 3.1 一个返回值

```cpp
QDBusPendingReply<QString> nameReply = iface.asyncCall("GetName");
```

完成且无错误后，`nameReply.value()` 或 `nameReply.argumentAt<0>()` 得到 `QString`。

### 3.2 多个返回值

```cpp
QDBusPendingReply<QString, QByteArray, int> reply =
    iface.asyncCall("GetMetadata");
```

用编译期下标读取：

```cpp
const QString title = reply.argumentAt<0>();
const QByteArray payload = reply.argumentAt<1>();
const int revision = reply.argumentAt<2>();
```

`argumentAt<Index>()` 的 `Index` 在编译期确定，返回类型也随之确定。它比 `argumentAt(int)` 更适合业务代码。

### 3.3 没有输出参数

远端方法返回 `void` 时使用 `QDBusPendingReply<>` 或项目约定的 `QDBusPendingReply<void>`。此时只检查完成和错误，不读取 `value()`：

```cpp
QDBusPendingReply<> reply = iface.asyncCall("Refresh");
reply.waitForFinished();

if (reply.isError())
    handleError(reply.error());
```

`Count` 和 `count()` 都为 0。

## 4. 两种完成方式

### 4.1 等待完成

`waitForFinished()` 挂起当前线程，直到回复已接收和处理。它适合 CLI、测试、启动阶段或专用工作线程。

不要在 GUI 主线程调用，因为主线程被阻塞后窗口无法响应。

### 4.2 用 watcher 继续异步处理

界面代码应让事件循环继续运行，并借助 `QDBusPendingCallWatcher`：

```cpp
QDBusPendingReply<QString, int> reply = iface.asyncCall("GetInfo");
auto *watcher = new QDBusPendingCallWatcher(reply, this);

connect(watcher, &QDBusPendingCallWatcher::finished, this,
        [watcher] {
            QDBusPendingReply<QString, int> result = *watcher;
            if (!result.isError())
                showInfo(result.argumentAt<0>(), result.argumentAt<1>());
            else
                showError(result.error());

            watcher->deleteLater();
        });
```

对象保留的是同一次 pending call 的共享引用。创建 watcher 后，局部 `reply` 可以离开作用域。

## 5. 完成、有效和错误的区别

这三个状态很容易混淆：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 完成状态 | `isFinished()` | 判断回复是否已经到达并完成处理。 | 未完成时不能读取结果；状态依赖事件循环或 `waitForFinished()` 推进。 |
| 错误状态 | `isError()` | 判断回复是否为错误，未完成时也返回 `true`。 | 不能单独把 `true` 理解为远端错误，先用 `isFinished()` 区分未完成。 |
| 成功状态 | `isValid()` | 判断回复是否为正常的方法回复。 | 未完成、远端错误、参数个数或类型不匹配时均为 `false`。 |

推荐逻辑：

```cpp
if (!reply.isFinished())
    return; // 或等待，或交给 watcher

if (reply.isError()) {
    handleError(reply.error());
    return;
}

use(reply.value());
```

## 6. 读取结果时的边界

### 6.1 `value()` 会隐式等待

`value()` 和隐式转换运算符在回复尚未到达时会阻塞当前线程。它们看起来很像普通 getter，实际却可能等待 I/O：

```cpp
const QString name = reply.value(); // 未完成时会阻塞
```

因此 GUI 回调外不要随手调用它。要么在 `finished()` 中读取，要么明确先 `waitForFinished()`。

### 6.2 默认值不能证明成功

若回复是错误，`value()` 返回第一个模板类型的默认构造值。例如 `QString()`、`0`、空 `QByteArray` 都可能既是合法业务值，也是错误时的返回值。必须通过 `isError()` 判断。

### 6.3 `argumentAt(int)` 只用于动态协议

`argumentAt(int)` 返回 `QVariant`，适合调试工具或必须动态遍历的通用代码。调用前必须确保回复完成、有效，且下标在 `0` 到 `count() - 1` 内；越界访问不应作为常规错误处理手段。

## 7. 生命周期与赋值

本类最终持有 `QDBusPendingCall` 的共享引用。复制 `QDBusPendingReply` 仍是同一笔调用，不会发起新请求。

对一个仍在等待回复的对象重新赋值时，它会放弃旧调用的引用；若那是最后一个引用，旧调用会被取消：

```cpp
QDBusPendingReply<QString> reply = iface.asyncCall("SlowOperation");
reply = iface.asyncCall("OtherOperation"); // 旧调用可能被取消
```

需要并行等待两笔请求时，使用两个变量或容器元素，不要覆盖同一对象。

## 8. 逐项 API 说明

### 模板常量与构造

#### `Count`

编译期常量，等于非 `void` 模板参数的个数。例如 `QDBusPendingReply<QString, int>::Count` 为 2。它描述的是**期望的**输出个数，不是网络消息中实际收到的任意参数数。

#### `QDBusPendingReply()`

创建空对象，尚未绑定 `QDBusPendingCall` 或 `QDBusMessage`。此时所有状态和取值 API 都只返回失败值，不能用于真实结果处理。

#### `QDBusPendingReply(const QDBusMessage &message)`

从一条已有消息创建对象，结果立即处于完成状态。常用于把已收到的 `QDBusMessage` 接入统一的类型校验流程。

#### `QDBusPendingReply(const QDBusPendingCall &call)`

绑定一笔异步调用，并与 `call` 共享引用。它不会复制请求，也不会等待；调用完成前通过 watcher 或 `waitForFinished()` 推进。

#### 复制构造与复制赋值

复制对象会共享同一个 pending call 和同一份结果。它适合把类型化回复传入另一个处理层，但不会创建独立、可取消的第二次请求。

#### 移动构造与移动赋值，Qt 6.10 起

移动转移对象状态，避免额外共享引用。移动赋值会放弃当前调用；若当前引用是未完成调用的最后一份引用，该调用会被取消。

### 结果与状态

#### `int count() const`

返回期望的输出参数数量，等于 `Count`。收到的回复参数数量或类型不符合该约定时，结果会被视作错误回复。

#### `template<int Index> argumentAt() const`

按编译期下标读取第 `Index` 个输出，并返回相应模板类型。只在回复完成且 `isError()` 为 `false` 后调用。

#### `QVariant argumentAt(int index) const`

按运行时下标读取原始参数。用于动态协议或通用调试代码；先检查 `isFinished()`、`isValid()` 和下标范围。

#### `QDBusError error() const`

返回已完成错误回复的错误信息。调用尚未完成或是正常回复时，返回无效 `QDBusError`。

#### `bool isError() const`

回复为错误时返回 `true`，但**未完成时也返回 `true`**。若需要区分“尚未完成”与“真正出错”，先检查 `isFinished()`。

#### `bool isFinished() const`

回复已接收和处理时返回 `true`。异步状态通常由事件循环中的 D-Bus 事件推进，或由 `waitForFinished()` 推进。

#### `bool isValid() const`

正常方法回复才返回 `true`。错误回复、未完成回复及返回签名不匹配都返回 `false`。

#### `QDBusMessage reply() const`

取得底层回复消息。未完成时得到 `QDBusMessage::InvalidMessage`；完成后则是正常回复或错误消息。

#### `value()` 与 `operator Type()`

返回第一个输出参数，等价于 `argumentAt<0>()`，且未完成时会阻塞。错误时返回默认构造值，不能据此判断成功。

#### `waitForFinished()`

阻塞当前线程直到回复处理完成。返回后仍要检查 `isError()`。

### 重新绑定数据源

#### `operator=(const QDBusMessage &message)`

丢弃当前 pending call 引用，改为使用 `message`，结果立即完成。若被丢弃引用是未完成调用的最后一个引用，该调用会被取消。

#### `operator=(const QDBusPendingCall &call)`

改为跟踪 `call`。原先未完成调用若失去最后一份引用会被取消。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 编译期常量 | `Count` | 给出预期的非 `void` 输出参数数量。 | 是协议契约，不是实际消息可随意变化的参数数。 |
| 构造 | `QDBusPendingReply()` | 创建未绑定调用的空回复对象。 | 所有查询仅返回失败值，先绑定 call 或 message。 |
| 构造 | `QDBusPendingReply(const QDBusMessage &message)` | 从已有消息创建已完成回复。 | 仍会按模板参数校验消息返回类型。 |
| 构造 | `QDBusPendingReply(const QDBusPendingCall &call)` | 绑定并共享一笔异步调用。 | 不会发送第二次请求，也不会自动等待。 |
| 复制 | `QDBusPendingReply(const QDBusPendingReply &other)` | 复制同一笔调用的类型化句柄。 | 副本共享结果与取消语义。 |
| 移动 | `QDBusPendingReply(QDBusPendingReply &&other)` | 移入另一个回复对象的状态。 | Qt 6.10 起可用；移动后只销毁或重新赋值源对象。 |
| 参数个数 | `int count() const` | 返回期望的输出参数数。 | 与 `Count` 相同；签名不匹配会导致错误回复。 |
| 类型化读取 | `template<int Index> argumentAt() const` | 以模板类型读取第 `Index` 个输出。 | 先确保已完成且无错误；`Index` 必须在模板参数范围内。 |
| 动态读取 | `QVariant argumentAt(int index) const` | 以 `QVariant` 读取运行时下标参数。 | 只在完成、有效且下标合法时使用。 |
| 错误读取 | `QDBusError error() const` | 获取错误回复的详情。 | 未完成或成功时返回无效错误对象。 |
| 错误查询 | `bool isError() const` | 判断回复是否错误或尚未完成。 | 未完成也为 `true`，要结合 `isFinished()`。 |
| 完成查询 | `bool isFinished() const` | 判断回复是否已经处理完毕。 | 依赖事件循环或 `waitForFinished()`。 |
| 成功查询 | `bool isValid() const` | 判断是否为正常且签名匹配的回复。 | `false` 可能是未完成、远端错误或类型不匹配。 |
| 原始消息 | `QDBusMessage reply() const` | 读取底层 D-Bus 回复消息。 | 未完成时是 InvalidMessage。 |
| 首值读取 | `value() const` | 返回第一个类型化输出。 | 未完成会阻塞；错误时默认值不能表示成功。 |
| 隐式读取 | `operator Type() const` | 隐式取得第一个输出。 | 同 `value()` 一样可能阻塞，业务代码更推荐显式 `value()`。 |
| 阻塞等待 | `void waitForFinished()` | 等待回复完成。 | 不要在 GUI 主线程调用；返回后仍应判断错误。 |
| 复制赋值 | `operator=(const QDBusPendingReply &other)` | 改为共享 `other` 的调用。 | 覆盖旧对象可能取消旧的未完成调用。 |
| 移动赋值 | `operator=(QDBusPendingReply &&other)` | 移入 `other` 的调用状态。 | Qt 6.10 起可用；覆盖旧对象同样可能取消其旧调用。 |
| 消息赋值 | `operator=(const QDBusMessage &message)` | 改为持有一条已完成消息。 | 会丢弃当前调用引用，结果立即完成。 |
| 调用赋值 | `operator=(const QDBusPendingCall &call)` | 改为跟踪另一笔异步调用。 | 旧调用若失去最后引用会被取消。 |

---

### 一句话总结

`QDBusPendingReply<Types...>` 把异步 D-Bus 返回值变成可校验的类型协议；完成后先判错再读取，在 GUI 中用 watcher 而不是让 `value()` 悄悄阻塞主线程。
