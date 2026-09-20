# Qt QUnhandledException：把并发线程中的未知异常带回接收线程

`QUnhandledException` 是 Qt Concurrent 用来包装“没有继承 `QException` 的工作线程异常”的类型。它本身不保存异常文本，也不把原异常转换成某个固定错误码；它保存一个 `std::exception_ptr`，让接收线程可以重新抛出原来的动态异常类型。

最典型的路径是：

```text
QtConcurrent 工作线程抛出 MyException
    -> QFuture 保存 std::exception_ptr
    -> 接收线程调用 waitForFinished()/result()
    -> 抛出 QUnhandledException
    -> exception() 取出指针
    -> std::rethrow_exception() 恢复 MyException
```

```cpp
#include <QUnhandledException>
#include <QtConcurrentRun>

struct NetworkFailure {};

auto future = QtConcurrent::run([] {
    throw NetworkFailure {};
    return 42;
});

try {
    const int value = future.result();
    Q_UNUSED(value);
} catch (const QUnhandledException &wrapper) {
    if (const std::exception_ptr exception = wrapper.exception()) {
        try {
            std::rethrow_exception(exception);
        } catch (const NetworkFailure &) {
            // 处理原始异常类型
        }
    }
}
```

## 它解决什么问题

跨线程传递 C++ 异常不能简单地把异常对象复制到另一个线程。异常可能是任意类型，可能没有公共基类，也可能包含只能由异常运行时管理的对象状态。`std::exception_ptr` 提供了保存和重新抛出当前异常的标准机制。

Qt Concurrent 对可以实现 `raise()` 和 `clone()` 的 `QException` 子类能够直接重建并抛出原始 Qt 异常。对于普通 C++ 异常，Qt 不知道如何复制它，就把当前异常捕获为 `std::exception_ptr`，在 future 的接收侧抛出 `QUnhandledException`。

因此，`QUnhandledException` 的职责很窄：

- 标记这是一次由 Qt Concurrent 传回的未处理异常；
- 持有原始异常的 `std::exception_ptr`；
- 让接收线程重新抛出原始异常并按动态类型处理。

它不是：

- 一个带 `message()` 的错误对象；
- 原始异常的基类替代品；
- 让任意线程可以安全地直接访问另一个线程对象的机制；
- 捕获所有 Qt 信号槽异常的全局兜底类型。

## 构建与包含

类型属于 Qt Core，但典型调用来自 Qt Concurrent：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::Concurrent)
```

```cpp
#include <QUnhandledException>
#include <QtConcurrentRun>
```

qmake 工程使用：

```text
QT += core concurrent
```

Qt 的异常支持必须启用。若 Qt 是以禁用 C++ 异常的配置构建，`QUnhandledException` 的定义不会按普通异常路径提供；应用也不能用 `try`/`catch` 处理被关闭的异常机制。

## 异常从哪里抛出

`QtConcurrent::run()`、`mapped()`、`mappedReduced()`、`blockingMap()` 等并发 API 会在工作函数中捕获异常并保存。对于 `QFuture`，转移过来的异常会在以下操作中重新抛出：

- `QFuture::waitForFinished()`；
- `QFuture::result()`；
- `QFuture::resultAt()`；
- `QFuture::results()`。

“工作线程抛出”与“接收线程观察到”是两个时刻。真正执行 `catch` 的线程通常是调用这些 future API 的线程，而不是发生原始 `throw` 的线程。

```cpp
auto future = QtConcurrent::run([] {
    throw std::runtime_error("worker failed");
});

future.waitForFinished();
// waitForFinished() 可能在这里把异常重新抛出
```

如果程序只检查 `isFinished()` 而从不读取结果或等待完成，就不能把“没有执行到 catch”理解为工作函数没有异常。异常可能仍然保存在 future 的状态中。

## `QException` 与 `QUnhandledException` 的区别

如果你能控制异常类型，Qt Concurrent 更适合使用 `QException` 子类：

```cpp
class ParseException final : public QException
{
public:
    void raise() const override
    {
        throw *this;
    }

    ParseException *clone() const override
    {
        return new ParseException(*this);
    }
};
```

工作线程抛出 `ParseException` 后，接收侧可以直接捕获 `ParseException`。`QException` 的 `raise()` 和 `clone()` 是跨线程重建原异常所需的协议，异常必须按值抛出、按引用捕获。

```cpp
try {
    QtConcurrent::blockingMap(items, parseItem);
} catch (const ParseException &) {
    // 直接处理 Qt 自定义异常
}
```

如果异常没有继承 `QException`，例如 `std::runtime_error`、业务结构体或第三方库异常，Qt Concurrent 会使用 `QUnhandledException` 作为接收侧的外层包装：

```cpp
try {
    future.result();
} catch (const QUnhandledException &wrapper) {
    // wrapper.exception() 仍然指向原始异常
}
```

不要为了避免包装而强行把所有第三方异常改造成 `QException`。是否转换应由异常跨线程协议、库边界和团队错误处理策略决定。

## `exception()` 的正确打开方式

`exception()` 返回保存的 `std::exception_ptr`。它可能为空，尤其是默认构造的 `QUnhandledException` 或手工传入空指针时。只有非空指针才能传给 `std::rethrow_exception()`：

```cpp
catch (const QUnhandledException &wrapper) {
    const std::exception_ptr exception = wrapper.exception();
    if (!exception)
        return;

    try {
        std::rethrow_exception(exception);
    } catch (const std::bad_alloc &) {
        handleMemoryFailure();
    } catch (const std::exception &error) {
        handleStdException(error);
    } catch (...) {
        handleUnknownException();
    }
}
```

重新抛出后，动态类型仍然是原始异常类型。若原异常是一个不继承 `std::exception` 的业务类型，就不能只写 `catch (const std::exception &)`, 还需要按该业务类型或 `catch (...)` 处理。

`std::exception_ptr` 是异常运行时持有的共享句柄，不是原始异常对象的裸指针。不要尝试解引用它、转换成 `void *` 或跨 ABI 手工解析内部结构。

## 手工构造的用途

构造函数接收一个可选的 `std::exception_ptr`：

```cpp
QUnhandledException empty;
Q_ASSERT(!empty.exception());

try {
    throw std::logic_error("invalid state");
} catch (...) {
    QUnhandledException wrapper(std::current_exception());
    Q_ASSERT(wrapper.exception());
}
```

手工构造主要适合测试包装逻辑、桥接自定义 future 或把已有异常状态交给需要 `QException` 接口的 Qt 代码。`std::current_exception()` 应该在 `catch` 块中调用；在没有活动异常时通常得到空指针。

若只是为了让 `QFuture` 带失败状态，也可以考虑 `QtFuture::makeExceptionalFuture()`，这样不必手动创建 `QUnhandledException`：

```cpp
try {
    throw std::runtime_error("request failed");
} catch (...) {
    auto failed = QtFuture::makeExceptionalFuture<int>(
        std::current_exception());
    // failed.result() 会重新抛出保存的异常
}
```

## 拷贝、移动和共享状态

`QUnhandledException` 是可拷贝、可移动的异常值对象。拷贝不会复制一个新的底层异常实例，而是复制异常指针所代表的共享引用；多个副本可以重新抛出同一个原始异常对象状态。

```cpp
QUnhandledException first(std::current_exception());
QUnhandledException second = first;

Q_ASSERT(first.exception());
Q_ASSERT(second.exception());
```

移动构造和移动赋值用于转移或交换内部共享状态，并且标记为 `noexcept`。对移动后的对象不要依赖除“可析构、可重新赋值”之外的具体状态。

`swap()` 同样是 `noexcept` 且开销很低，适合实现异常对象的高效交换。它不改变原始异常的动态类型，也不会把异常重新抛出。

## `raise()`、`clone()` 与 final 限制

`QUnhandledException` 继承 `QException`，并在头文件中重写 `raise()` 和 `clone()`。这些函数用于 Qt 的异常存储和再抛出机制，普通业务代码通常只需要 `exception()`。

这个类声明为 `final`，官方明确不支持从它继续继承。若需要自己的可跨线程 Qt 异常，应直接继承 `QException`，实现：

```cpp
void raise() const override;
QException *clone() const override;
```

不要继承 `QUnhandledException` 来添加错误码、消息或业务字段。可以把原始异常重新抛出后，在自己的异常类型中提供这些信息。

## Future 链和异常处理

Qt 6 的 `QFuture::then()`、`onFailed()` 等链式 API 使用异常表示失败。一个 continuation 抛出的异常会进入后续 future；可以在链末端用 `onFailed()` 处理，也可以在读取结果时用 `try`/`catch` 处理。

```cpp
auto future = QtConcurrent::run([] {
    throw std::runtime_error("download failed");
    return QByteArray {};
}).onFailed([](const QUnhandledException &wrapper) {
    if (wrapper.exception())
        logException(wrapper.exception());
});
```

实际项目中应确认 `onFailed()` 的处理器签名与 Qt Future 的异常匹配规则，并确保异常最终被消费。若需要把错误作为正常业务数据传递，使用 `std::variant`、结果结构体或其他显式错误类型，避免让所有调用者都依赖异常控制流。

把 continuation 绑定到 `QObject *context` 时，context 的线程决定 continuation 的执行上下文；这和 `QUnhandledException` 保存哪一个异常是两个独立问题。异常处理代码仍然要在合适的线程中更新 UI 或其他线程受限对象。

## 生命周期、线程和 ABI 边界

异常对象通常只在 `catch` 块中短暂存在，但 `std::exception_ptr` 可以延长原始异常状态的生命周期。将 `QUnhandledException` 或 `exception_ptr` 放入 future、队列或日志任务时，要意识到原始异常对象会一直保留到最后一个指针释放。

异常指针可以跨线程传递，但这不等于原始异常所引用的业务对象都能跨线程使用。重新抛出后访问异常中的字符串、文件句柄或自定义指针，仍须遵守这些资源自己的线程和生命周期规则。

`std::exception_ptr` 依赖编译器和 C++ 运行时 ABI。Qt、应用和涉及异常边界的动态库应使用兼容的编译器、运行库和异常开关。不要把 `std::exception_ptr` 当成跨进程或跨语言的可序列化数据。

## 常见错误与排查顺序

- 只捕获 `std::exception`，却忘了原异常可能不是标准异常；应保留 `catch (...)` 或按业务类型捕获。
- 认为 `QUnhandledException::what()` 会包含原异常消息。恢复原异常后再调用它的接口。
- 不检查 `exception()` 是否为空就调用 `std::rethrow_exception()`。
- 在工作线程里直接把异常抛出到线程入口之外。让 QtConcurrent 或 QFuture 接管异常，避免跨线程未处理异常触发终止。
- 把 `QUnhandledException` 当成所有 Qt 异步错误的统一错误码。取消、超时和业务失败可能是不同状态。
- 从 `QFuture` 只调用 `isFinished()`，却期待异常自动进入 `catch`。异常通常在等待或读取结果的 API 中重新抛出。
- 用 `QUnhandledException` 继承出业务异常。该类是 `final`，应继承 `QException`。
- 在 `QException` 子类中忘记实现正确的 `raise()` / `clone()`，导致 Qt 无法按原类型跨线程传递。
- 直接跨动态库或进程传递 `std::exception_ptr`。
- 在异常处理 continuation 中不检查 context 生命周期就操作已经销毁的 QObject。

## 逐项 API 说明

### 构造、复制与赋值

#### `QUnhandledException::QUnhandledException(std::exception_ptr exception = nullptr)`

创建一个包装对象，并保存传入的异常指针。参数为空时对象不指向实际异常。该构造函数从 Qt 6.0 开始提供，并标记为 `noexcept`。

#### `QUnhandledException::QUnhandledException(const QUnhandledException &other)`

复制另一个包装对象。复制的是内部共享异常状态的句柄，不会把原始异常重新抛出，也不要求原异常类型可复制。

#### `QUnhandledException::QUnhandledException(QUnhandledException &&other)`

移动构造包装对象。操作不抛异常；移动后的 `other` 只保证处于可析构、可赋值状态。

#### `QUnhandledException::~QUnhandledException()`

销毁包装对象并释放它持有的共享异常引用。它不会主动抛出原异常。

#### `QUnhandledException &QUnhandledException::operator=(const QUnhandledException &other)`

复制赋值另一个包装对象并返回自身引用。旧的异常指针引用会被替换。

#### `QUnhandledException &QUnhandledException::operator=(QUnhandledException &&other)`

移动赋值包装对象。该运算符由 Qt 的移动赋值辅助宏提供，标记为 `noexcept`，适合在容器和异常传播路径中使用。

### 异常访问与交换

#### `std::exception_ptr QUnhandledException::exception() const`

返回保存的原始异常指针。返回空指针表示没有保存异常；非空时可传给 `std::rethrow_exception()`。该函数从 Qt 6.0 开始提供。

#### `void QUnhandledException::swap(QUnhandledException &other)`

交换两个包装对象的内部状态。操作 `noexcept`、快速且不会重新抛异常；交换后两者分别指向对方原先持有的异常状态。

### QException 重写点

#### `void QUnhandledException::raise() const`

按 `QException` 协议重新抛出当前包装对象。主要供 Qt 的异常存储机制调用，业务代码通常使用 `exception()` 加 `std::rethrow_exception()` 以恢复原始动态类型。

#### `QUnhandledException *QUnhandledException::clone() const`

创建当前包装对象的副本，供 `QException` 的跨线程传递协议使用。类为 `final`，不能通过继承它来改变 clone 行为。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUnhandledException(std::exception_ptr exception = nullptr)` | 创建异常包装器 | 保存异常指针；空参数表示没有原始异常 |
| `QUnhandledException(const QUnhandledException &other)` | 复制包装器 | 复制共享异常句柄，不复制动态异常对象 |
| `QUnhandledException(QUnhandledException &&other)` | 移动构造 | `noexcept`；移动后的源对象状态不应被依赖 |
| `~QUnhandledException()` | 销毁包装器 | 释放共享异常引用，不主动抛出 |
| `operator=(const QUnhandledException &other)` | 复制赋值 | 替换当前保存的异常状态 |
| `operator=(QUnhandledException &&other)` | 移动赋值 | Qt 宏生成的 `noexcept` 运算符 |
| `exception() const` | 取出原始异常指针 | 可能为空；非空后用 `std::rethrow_exception()` 恢复动态类型 |
| `swap(QUnhandledException &other)` | 交换两个包装器 | `noexcept`、快速，不执行异常处理 |
| `raise() const` | 按 `QException` 协议重新抛出 | 主要供 Qt 内部调用 |
| `clone() const` | 复制当前 Qt 异常 | 主要供 Qt 跨线程异常传递；本类为 `final` |
| `QFuture::waitForFinished()` | 等待并可能重新抛出 future 异常 | 接收线程执行 `catch`；不只是状态查询 |
| `QFuture::result()` / `resultAt()` / `results()` | 读取 future 结果 | 结果或异常会在调用线程可见；应放在 `try` 块内 |
| `std::current_exception()` | 捕获当前异常句柄 | 应在 `catch` 中调用；没有活动异常时通常为空 |
| `std::rethrow_exception(exception)` | 重新抛出原异常 | 先确认指针非空，并按原动态类型捕获 |
| `QtFuture::makeExceptionalFuture()` | 创建已失败的 future | 可直接保存 `QException` 或 `std::exception_ptr`，适合测试和错误桥接 |

---

### 一句话总结

`QUnhandledException` 是 Qt Concurrent 的异常外壳：它不替换原异常，而是保存 `std::exception_ptr`，让接收线程通过 `exception()` 和 `std::rethrow_exception()` 恢复原始类型。
