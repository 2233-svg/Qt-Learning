# Qt QException 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QException>`  
> 所属模块：`Qt6::Core`  
> 继承：`std::exception`  
> 直接派生类：`QUnhandledException`  
> 关键协作模块：`Qt6::Concurrent`、`QFuture`

## 1. 它解决什么问题

`QException` 是 Qt 为 Qt Concurrent 提供的“可跨线程转移异常”的基类。

普通 C++ 异常对象通常在抛出线程的栈展开过程中使用。Qt Concurrent 需要把工作线程中的异常保存下来，等调用方在另一个线程调用 `QFuture::result()`、`waitForFinished()` 等接口时再重新抛出。为了在这个过程中保留具体异常类型，Qt 要求异常派生类提供两个操作：

- `clone()`：复制当前异常，并保留具体派生类型；
- `raise()`：在接收线程中再次以具体类型抛出异常。

因此，`QException` 不是一个带错误字符串的通用错误对象，也不是 `QFuture` 的结果类型。它是一份跨线程异常传递协议。自定义异常要按值抛出、按引用捕获，并实现这两个虚函数。

## 2. 最小可用模式

```cpp
#include <QException>
#include <QString>
#include <utility>

class ParseException : public QException
{
public:
    explicit ParseException(QString message)
        : m_message(std::move(message))
    {
    }

    void raise() const override
    {
        throw *this;
    }

    ParseException *clone() const override
    {
        return new ParseException(*this);
    }

    const QString &message() const
    {
        return m_message;
    }

private:
    QString m_message;
};
```

两个重写缺一不可：

- 只有 `clone()` 没有 `raise()`，接收线程无法按正确类型重新抛出；
- 只有 `raise()` 没有 `clone()`，异常保存或跨线程复制时无法保留派生类型；
- 返回 `new QException(*this)` 会发生切片，具体的 `ParseException` 信息会丢失。

## 3. Qt Concurrent 中的使用方式

### 3.1 按值抛出，按引用捕获

```cpp
#include <QList>
#include <QtConcurrent>
#include <utility>

void checkValues(QList<int> values)
{
    try {
        QtConcurrent::blockingMap(values, [](int &value) {
            if (value < 0)
                throw ParseException(QStringLiteral("negative value"));
            ++value;
        });
    } catch (ParseException &exception) {
        qWarning() << exception.message();
    }
}
```

派生异常应按值抛出：

```cpp
throw ParseException(QStringLiteral("bad input"));
```

捕获时使用引用：

```cpp
catch (ParseException &exception) {
    // 保留具体异常类型，避免再次复制和切片。
}
```

不要按值捕获基类：

```cpp
catch (QException exception) {
    // 这里可能已经发生切片，具体类型信息不可用。
}
```

### 3.2 `QFuture` 何时重新抛出

使用异步任务时，异常通常在读取结果或等待完成时重新抛出：

```cpp
#include <QFuture>
#include <QtConcurrent>
#include <utility>

QFuture<int> future = QtConcurrent::run([] {
    throw ParseException(QStringLiteral("worker failed"));
    return 0;
});

try {
    const int value = future.result();
    Q_UNUSED(value);
} catch (ParseException &exception) {
    qWarning() << exception.message();
}
```

Qt 6.11.1 文档列出的会触发转移异常重新抛出的 `QFuture` 操作包括：

- `waitForFinished()`；
- `result()`；
- `resultAt()`；
- `results()`。

所以 `waitForFinished()` 不是“只等待、不抛错”的绝对保证。需要统一处理工作线程错误时，应把这些调用放在 `try` 块中。

### 3.3 非 `QException` 异常

如果 Qt Concurrent 工作函数抛出的不是 `QException` 子类，接收线程会得到 `QUnhandledException`。这意味着具体的业务异常类型不能按自定义类型直接捕获。

如果项目有明确的异常类型体系，应让跨 Qt Concurrent 边界的异常都继承 `QException`，而不是混用任意 `std::exception` 派生类。

## 4. 实际使用场景

### 4.1 并行解析、校验和批处理

多个工作线程处理文件、记录或图像时，某一项可能发现格式错误。把异常保存进 `QFuture`，由启动任务的线程在读取结果时统一处理，可以避免在工作线程中直接操作界面或业务控制器。

异常对象应携带足够的值语义信息，例如错误码、记录索引和简短消息：

```cpp
#include <utility>

class RecordException : public QException
{
public:
    RecordException(int index, QString message)
        : m_index(index), m_message(std::move(message))
    {
    }

    void raise() const override { throw *this; }
    RecordException *clone() const override
    {
        return new RecordException(*this);
    }

    int index() const { return m_index; }
    const QString &message() const { return m_message; }

private:
    int m_index = -1;
    QString m_message;
};
```

### 4.2 QFuture 链中的失败处理

`QFuture` 的 continuation 可以使用异常传播失败状态。读取结果时由调用方捕获 `QException` 的具体派生类，或者使用 `QFuture::onFailed()` 集中注册失败处理器。

`QException` 只解决异常如何复制和重新抛出，不替代 `QFuture` 的取消、进度和 continuation 机制。

### 4.3 跨线程边界统一转换错误

底层工作代码可以抛出领域异常，接收线程负责把它转换成界面提示、日志记录或上层错误码。这样错误处理位置与实际执行线程解耦，但异常类本身必须保持可复制、可重新抛出。

## 5. 关键 API 语义

### 5.1 `clone()` 是为了防止切片

Qt 保存异常时通过 `clone()` 得到一个新的 `QException *`。派生类应该返回自己的具体类型：

```cpp
ParseException *clone() const override
{
    return new ParseException(*this);
}
```

返回类型可以使用协变返回类型 `ParseException *`，因为它可以转换为基类要求的 `QException *`。

`clone()` 返回的对象由 Qt 的异常传递机制管理。调用方不要把返回指针当作自己的长期裸指针，也不要在接收端手动释放 Qt 内部持有的克隆对象。

### 5.2 `raise()` 是为了在接收线程恢复动态类型

典型实现是：

```cpp
void ParseException::raise() const
{
    throw *this;
}
```

这里的 `*this` 在派生类成员函数中按 `ParseException` 的静态类型复制并抛出，因此接收端可以捕获 `ParseException &`。实现时不要写成 `throw QException(*this)`，否则会主动切片。

### 5.3 复制构造和赋值有切片风险

`QException` 提供复制构造和复制赋值，但文档明确提醒：直接把派生对象复制到 `QException` 对象可能发生 slicing。

应优先使用：

```cpp
auto copy = original.clone();
```

或者在具体派生类中使用自己的复制构造函数。不要把 `QException` 当作一个可以安全按值传递的多态值容器。

### 5.4 基类不提供业务错误负载

`QException` 本身没有错误码、消息或上下文成员。自定义派生类负责定义这些字段，并保证它们支持复制。

如果需要文本接口，可以在派生类中提供 `message()`，或按项目约定重写 `std::exception::what()`。不要假设 `QException` 会自动把 `QString`、错误码或源线程信息保存下来。

## 6. 配置和边界

### 6.1 异常开关和 future 配置

Qt 6.11.1 的 `QException` 头文件要求启用 `future` 配置；在 `QT_NO_EXCEPTIONS` 配置下，普通构建不会提供完整的 `QException` 类实现。

因此，如果项目显式关闭了 C++ 异常，或者构建 Qt 时关闭了 future 相关配置，不能只看源代码是否包含 `<QException>`，还要确认项目和 Qt 构建配置是否支持这条 API 路径。

### 6.2 异常对象必须可复制

Qt 需要调用 `clone()`，所以派生异常中的字段要能正确复制。不要在异常对象中保存只在抛出线程有效的裸指针、引用或已经销毁的临时缓冲区。

### 6.3 异常不等于取消

异常表示计算失败；`QFuture::cancel()` 表示请求取消。取消和异常可以在同一条 future 链中同时出现，但两者不是同一种状态。不要用抛出 `QException` 来代替正常的协作式取消。

### 6.4 捕获位置要覆盖真正读取结果的调用

异常可能直到 `result()` 或 `waitForFinished()` 才重新抛出。只把启动 `QtConcurrent::run()` 的语句放进 `try` 块，并不能保证捕获后续结果读取阶段的异常。

## 7. 与相似类型的区别

| 类型或方案 | 主要用途 | 关键区别 |
| --- | --- | --- |
| `QException` | Qt Concurrent 跨线程异常传递 | 要实现 `clone()` 和 `raise()` |
| `QUnhandledException` | 包装未被识别或非 `QException` 的异常 | 接收端拿到的是包装类型，不是原业务派生类 |
| `std::exception` | 标准 C++ 异常基类 | 单独继承它不满足 Qt Concurrent 的克隆/重抛协议 |
| `QFuture::onFailed()` | 对 future 链注册失败处理 | 处理机制，不是异常基类 |
| `QFuture` 结果中的错误类型 | 用 `std::variant` 等表达失败 | 不依赖 C++ 异常，适合项目禁用异常时使用 |

## 8. API 逐项说明

### `QException()`

构造一个没有业务负载的基类异常对象。实际项目通常直接实例化派生异常，而不是抛出空的 `QException`。

### `QException(const QException &other)`

复制基类部分。直接以基类对象复制派生异常有切片风险，跨线程传递应依赖派生类的 `clone()`。

### `~QException()`

虚析构函数，允许通过 `QException *` 正确销毁派生异常。析构函数为 `noexcept`。

### `QException *clone() const`

派生类必须重写为返回具体派生类型的新对象。典型实现是 `return new MyException(*this);`。

### `void raise() const`

派生类必须重写为按具体派生类型抛出当前对象，典型实现是 `throw *this;`。

### `QException &operator=(const QException &other)`

复制赋值基类部分。对多态异常直接使用时同样存在切片风险；异常负载的赋值语义应由派生类自行设计。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QException()` | 创建一个空的基类异常对象 | 通常由派生异常继承，不负责保存业务错误信息 |
| 构造 | `QException(const QException &other)` | 复制基类异常部分 | 复制派生对象到基类对象可能切片；多态传递优先使用 `clone()` |
| 析构 | `virtual ~QException()` | 通过基类接口销毁异常对象 | 虚析构且 `noexcept`，适合多态删除 |
| 扩展点 | `virtual QException *clone() const` | 创建保留具体异常类型的堆复制 | 派生类必须重写；典型返回 `new Derived(*this)` |
| 扩展点 | `virtual void raise() const` | 在接收线程按具体派生类型重新抛出 | 派生类必须重写；典型实现为 `throw *this` |
| 赋值 | `QException &operator=(const QException &other)` | 复制基类异常部分 | 直接对多态异常赋值有切片风险 |
| 相关调用 | `QFuture::waitForFinished()` | 等待 future 完成，并可能重新抛出转移异常 | 放在 `try` 块中；等待不代表不会报告异常 |
| 相关调用 | `QFuture::result()` / `resultAt()` / `results()` | 读取 future 结果，并可能重新抛出转移异常 | 读取阶段才可能抛出，捕获范围要覆盖这些调用 |

## 10. 一句话总结

`QException` 是 Qt Concurrent 的跨线程异常传递协议：派生类按值抛出、实现 `clone()` 保留具体类型、实现 `raise()` 在接收线程重新抛出，并在 `QFuture` 的等待或结果读取处按引用捕获。
