# Qt QMetaObject::Connection 信号槽连接句柄笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaObject>`  
> 所属模块：`Qt6::Core`  
> 类型性质：表示一次具体信号槽或信号回调连接的轻量句柄  
> 相关类型：`QObject`、`QMetaObject`、`Qt::ConnectionType`

## 1. 它解决什么问题

调用 `QObject::connect()` 或相关连接 API 后，Qt 会创建一条运行时连接。`QMetaObject::Connection` 是这条连接的可保存句柄，主要用于：

- 判断连接请求是否成功；
- 精确断开这一条连接；
- 把连接作为类成员保存，稍后按生命周期或状态撤销；
- 在容器中保存多条连接；
- 在管理多个连接时移动、交换句柄。

它只是连接记录的句柄，不是槽对象、不拥有 sender/receiver，也不是“离开作用域自动断开”的 RAII 锁。

## 2. 实际使用场景

### 2.1 保存连接并精确断开

```cpp
QMetaObject::Connection connection =
    QObject::connect(sender, &Sender::valueChanged,
                     receiver, &Receiver::setValue);

if (!connection) {
    qWarning() << "connect failed";
    return;
}

// 某个业务状态结束时：
const bool disconnected = QObject::disconnect(connection);
```

`QObject::disconnect(connection)` 只针对这个连接句柄。它不会影响同一 signal 的其他连接。

### 2.2 连接临时回调并绑定 context 生命周期

```cpp
QMetaObject::Connection connection =
    QObject::connect(sender, &Sender::valueChanged,
                     context,
                     [context](int value) {
                         context->updateValue(value);
                     });
```

当 `context` 被销毁时，这条连接会自动断开。句柄本身仍然只是一个观察和控制入口，不会替代 context 的对象树生命周期。

### 2.3 延迟建立或替换连接

```cpp
class Controller : public QObject
{
    Q_OBJECT
public:
    void setEnabledSource(QObject *source)
    {
        QObject::disconnect(m_connection);
        m_connection = QObject::connect(
            source, &QObject::objectNameChanged,
            this, &Controller::sourceChanged);
    }

private:
    QMetaObject::Connection m_connection;
};
```

重复赋值前先断开旧连接，否则旧连接不会因为句柄被覆盖而自动消失。

## 3. 连接句柄的状态模型

### 3.1 默认构造表示无连接

```cpp
QMetaObject::Connection connection;
Q_ASSERT(!connection);
```

默认句柄可以安全地传给 `QObject::disconnect()`，但不会断开任何连接。它适合用于类成员的初始状态。

### 3.2 连接成功不等于连接永久有效

`operator bool()` 通常同时考虑句柄内部指针和连接当前是否仍存在。因此下面这些事件之后，旧句柄可能转为 false：

- sender 或 receiver 被销毁；
- 连接被显式断开；
- context 被销毁；
- 其他断开操作移除了这条连接。

不要把一次成功的 bool 判断当作永久有效性保证。

### 3.3 句柄析构不会断开连接

```cpp
{
    const auto connection = QObject::connect(...);
} // connection 析构，不代表连接自动断开
```

如果确实需要作用域结束自动断开，应使用 `QMetaObject::Connection` 外包一层明确的 RAII 管理类，或让 context 的生命周期负责连接销毁。不能依赖句柄析构的副作用。

## 4. 拷贝、移动与所有权

### 4.1 拷贝是同一连接的另一个句柄

```cpp
const QMetaObject::Connection a =
    QObject::connect(...);
const QMetaObject::Connection b = a;
```

`a` 和 `b` 指向同一条连接。销毁其中一个句柄不会断开连接；对任一有效句柄调用 `QObject::disconnect()` 都可能让另一份句柄随之变为无效。

### 4.2 移动转移句柄状态

```cpp
QMetaObject::Connection source =
    QObject::connect(...);
QMetaObject::Connection target = std::move(source);
```

移动后 `target` 接管句柄，`source` 处于空的可析构状态。不要继续用 moved-from 句柄断开或判断业务连接。

### 4.3 `swap()` 只交换句柄

```cpp
connectionA.swap(connectionB);
```

它不创建新连接，也不改变信号槽关系，只交换两个对象当前持有的连接记录。

## 5. 线程和并发边界

连接的建立和断开通常可以在不同线程进行，但这不等于业务回调自动线程安全：

- `AutoConnection` 的执行线程由 sender/receiver 的线程归属决定；
- `DirectConnection` 可能在发射线程直接调用 receiver；
- `QueuedConnection` 依赖 receiver/context 线程事件循环；
- 断开正在执行的回调时，已经进入调用栈的槽函数不会被“撤回”；
- 句柄的 bool 状态与另一个线程刚刚发生的断开之间存在竞态。

不要用：

```cpp
if (connection)
    QObject::disconnect(connection);
```

来假设中间不会被其他线程断开。这个判断最多是诊断信息，不能作为跨线程同步协议。

## 6. 与 `QObject::disconnect()` 的配合

### 6.1 精确断开

```cpp
const bool result = QObject::disconnect(connection);
```

成功表示这次调用找到了并断开了对应连接；如果连接已经由对象销毁或其他代码断开，返回 false 是正常可能结果。

### 6.2 对象销毁会自动清理

Qt 会在 sender、receiver 或 context 销毁时清理相关连接。句柄本身不会让这些对象延长生命周期，也不应在对象已经销毁后继续依赖其连接状态做业务决策。

### 6.3 不能反向查询连接两端

公开 `QMetaObject::Connection` API 不提供 sender、receiver、signal 和 slot 的查询接口。需要审计连接图时，应在建立连接处保存额外的业务元数据，而不是尝试从句柄反射出两端。

## 7. 逐项 API 说明

### 7.1 `Connection()`

```cpp
Connection();
```

构造空连接句柄。它不创建连接，也不绑定任何对象。

### 7.2 `Connection(const Connection &other)`

```cpp
Connection(const QMetaObject::Connection &other);
```

复制另一个句柄，使两个句柄引用同一连接记录。复制不会新建第二条信号槽连接。

### 7.3 `Connection(Connection &&other)`

```cpp
Connection(Connection &&other) noexcept;
```

移动连接句柄。目标接管源句柄的内部连接记录，源句柄变为空。移动不会改变连接本身。

### 7.4 `~Connection()`

```cpp
~Connection();
```

销毁句柄对象。它释放句柄自身的引用管理状态，但不会自动调用 `QObject::disconnect()`。若要求明确断开，必须显式断开。

### 7.5 `operator=(const Connection &other)`

```cpp
QMetaObject::Connection &operator=(
    const QMetaObject::Connection &other);
```

让当前句柄改为引用 `other` 的连接。覆盖旧句柄不会自动断开旧连接；如需移除旧连接，先显式调用 `QObject::disconnect()`。

### 7.6 `operator=(Connection &&other)`

```cpp
QMetaObject::Connection &operator=(
    QMetaObject::Connection &&other) noexcept;
```

移动赋值并接管 `other` 的句柄。当前对象原先持有的句柄引用会被替换，但对应的连接关系不会仅因为句柄覆盖而自动断开。

### 7.7 `operator bool() const`

```cpp
operator bool() const;
```

在条件表达式中判断句柄是否指向当前仍存在的连接：

```cpp
if (connection) {
    // 连接句柄当前看起来有效
}
```

它不是对业务回调“已经执行”或“以后一定会执行”的保证，也不应被当作跨线程同步原语。

### 7.8 `swap(Connection &other)`

```cpp
void swap(QMetaObject::Connection &other) noexcept;
```

交换两个句柄的内部连接记录。等价的非成员 `swap(lhs, rhs)` 也可用。

## 8. 常见错误

### 8.1 误以为句柄析构会自动断开

**症状：** 局部变量离开作用域后，回调仍然继续触发。

**原因：** `Connection` 不是自动断开型 RAII 对象。

**修复：** 显式 `QObject::disconnect(connection)`，或使用 context 生命周期和专门的 scope guard。

### 8.2 覆盖句柄却忘记断开旧连接

**症状：** 回调触发次数越来越多。

**原因：** 赋值只替换了句柄，不会移除旧连接。

**修复：** 赋新值前断开旧句柄，或在设计上只建立一次连接。

### 8.3 把 bool 当作永久状态

**症状：** 检查为 true 后，另一个线程断开连接导致后续操作失败。

**原因：** 连接状态可被对象销毁或其他线程变化。

**修复：** 将连接管理放入明确的线程/生命周期协议中，不依赖一次性 bool 检查。

### 8.4 试图从句柄查询连接两端

**症状：** 希望通过 `QMetaObject::Connection` 取得 sender、receiver 或信号名。

**原因：** 公开 API 没有提供这些查询操作。

**修复：** 建立连接时同时保存业务侧描述，或使用统一连接管理器。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Connection()` | 构造空连接句柄 | 不创建连接 |
| `Connection(const Connection &)` | 复制连接句柄 | 引用同一条连接，不创建新连接 |
| `Connection(Connection &&)` | 移动连接句柄 | moved-from 句柄为空 |
| `~Connection()` | 销毁句柄对象 | 不自动断开连接 |
| `operator=(const Connection &)` | 复制赋值句柄 | 覆盖句柄不等于断开旧连接 |
| `operator=(Connection &&)` | 移动赋值句柄 | 接管新句柄；旧连接关系仍需显式管理 |
| `operator bool()` | 判断连接当前是否有效 | 不是永久保证，也不是线程同步 |
| `swap()` | 交换两个句柄 | 不创建、断开或修改连接关系 |
| `QObject::disconnect(connection)` | 精确断开句柄对应连接 | 已断开的连接可能返回 false |

## 10. 推荐的作用域管理模板

```cpp
class ConnectionGuard
{
public:
    ConnectionGuard() = default;
    explicit ConnectionGuard(QMetaObject::Connection connection)
        : m_connection(std::move(connection))
    {
    }

    ConnectionGuard(const ConnectionGuard &) = delete;
    ConnectionGuard &operator=(const ConnectionGuard &) = delete;

    ConnectionGuard(ConnectionGuard &&other) noexcept
        : m_connection(std::move(other.m_connection))
    {
    }

    ~ConnectionGuard()
    {
        QObject::disconnect(m_connection);
    }

private:
    QMetaObject::Connection m_connection;
};
```

这个小类才具有作用域结束断开语义。实际项目中还应按需要补充 `reset()`、`release()` 和移动赋值，并明确它只能在允许断开连接的线程/生命周期中使用。

## 11. 一句话总结

`QMetaObject::Connection` 是一次信号槽连接的可保存句柄：可复制、移动和交换，可通过 `QObject::disconnect()` 精确断开，但句柄析构和赋值都不会自动断开连接；它不拥有连接两端对象，也不提供跨线程同步或反向查询连接图的能力。
