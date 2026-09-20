# Qt QGenericReturnArgument 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGenericReturnArgument>`  
> 所属模块：`Qt6::Core`  
> 继承：`QGenericArgument -> QGenericReturnArgument`  
> 类型性质：元对象调用的内部返回值包装  
> 相关 API：`Q_RETURN_ARG`、`QMetaObject::invokeMethod`、`QGenericArgument`

## 1. 它解决什么问题

`QGenericReturnArgument` 是 Qt 元对象系统为“动态调用一个方法并把返回值写入调用方对象”准备的低层包装。它继承自 `QGenericArgument`，但传入的是可写的返回值地址。

普通代码不应该直接使用它。Qt 文档明确建议使用 `Q_RETURN_ARG(Type, value)` 宏，或在较新的 `QMetaObject::invokeMethod` API 中使用类型安全的 `qReturnArg(value)` / 返回值指针形式。

## 2. 实际使用场景

### 2.1 推荐的旧式动态调用

```cpp
QString result;

const bool ok = QMetaObject::invokeMethod(
    receiver,
    "compute",
    Qt::DirectConnection,
    Q_RETURN_ARG(QString, result),
    Q_ARG(QString, QStringLiteral("sqrt")),
    Q_ARG(int, 42),
    Q_ARG(double, 9.7));
```

调用成功后，`result` 由目标方法写入。`Q_RETURN_ARG` 内部会生成一个 `QGenericReturnArgument`，同时带上返回类型名和可写地址。

### 2.2 新代码优先使用类型安全重载

Qt 6.5 起，`QMetaObject::invokeMethod` 提供更多 functor、成员函数指针和返回值重载。能在编译期表达目标方法时，优先使用这些 API；只有方法名在运行时才知道、需要兼容 Qt 6.4 及以前的旧式动态调用，或需要处理特殊 typedef 时，才保留 `Q_RETURN_ARG`。

## 3. 返回值地址和连接类型

### 3.1 必须提供可写对象

构造函数的 `data` 参数必须指向一个由调用方拥有、可写且类型正确的对象：

```cpp
QString result;
QGenericReturnArgument ret("QString", &result);
```

包装对象不分配、不复制、不销毁 `result`。`result` 必须活到同步调用写入完成。

### 3.2 异步调用不能像同步调用那样立即返回结果

`Qt::DirectConnection` 在当前线程立即执行，返回值可以写回本地变量。`Qt::BlockingQueuedConnection` 会等待目标线程执行完成，也可以表达同步返回，但同线程使用会死锁。

`Qt::QueuedConnection` 只是把调用排入目标线程事件循环；调用函数返回时目标方法可能尚未执行，不能把局部变量地址当作一个可长期保存的异步结果槽。对异步任务，使用信号、future 或共享结果对象更合适。

### 3.3 目标签名必须精确匹配

动态调用按元对象中的方法签名匹配。返回类型、参数数量、顺序和类型名不匹配时，调用会失败。`QGenericReturnArgument` 不会替你做转换，也不会检查返回对象的真实类型。

## 4. 继承关系和 const 边界

`QGenericReturnArgument` 继承 `QGenericArgument`，因此可通过基类的 `name()` 和 `data()` 查看包装内容。但它的语义不同：

- 普通 `QGenericArgument` 描述输入参数，数据通常来自 const 地址；
- `QGenericReturnArgument` 描述输出位置，数据必须是可写地址；
- `data()` 返回 `void *`，这是元对象 ABI 的历史接口，不是通用类型安全引用。

不要把 `QGenericReturnArgument` 当作普通输入参数传给不接受返回包装的 API，也不要用它包装临时对象的地址。

## 5. 逐项 API 说明

#### `QGenericReturnArgument::QGenericReturnArgument(const char *name = nullptr, void *data = nullptr)`

构造一个返回值包装：

- `name` 是元对象识别的返回类型名；
- `data` 是目标方法写入返回值的地址；
- 包装对象不拥有 `data` 指向的对象；
- `name` 和对象都必须在调用所需的时间内有效。

通常通过 `Q_RETURN_ARG(Type, value)` 间接构造，不直接写这个构造函数。

由于它继承 `QGenericArgument`，还可以使用继承来的：

- `name()`：读取保存的类型名；
- `data()`：读取保存的地址，但必须遵守可写对象和真实类型约束。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QGenericReturnArgument(name, data)` | 保存返回类型名和可写地址 | 不拥有目标对象，不校验签名 |
| `Q_RETURN_ARG(Type, value)` | 推荐的返回值包装宏 | `value` 必须是非 const 左值 |
| `name()` | 继承自 `QGenericArgument` | 返回原始类型名指针 |
| `data()` | 继承自 `QGenericArgument` | 返回 `void *`，实际类型需自行保证 |
| `QMetaObject::invokeMethod(..., Q_RETURN_ARG(...))` | 动态调用并写回结果 | 适合同步或阻塞调用 |

## 7. 和相邻 API 如何选择

- 输入参数：`Q_ARG(Type, value)` / `QGenericArgument`。
- 输出参数：`Q_RETURN_ARG(Type, value)` / `QGenericReturnArgument`。
- Qt 6.5 以后、目标方法可在编译期表达：优先成员函数指针或 functor `invokeMethod`。
- 动态方法名且需要兼容旧接口：使用 `QMetaObject::invokeMethod` 加 `Q_ARG` / `Q_RETURN_ARG`。
- 真正异步的返回结果：使用信号、`QFuture` 或显式共享状态，不依赖局部返回变量地址。

## 8. 排查顺序

1. `invokeMethod` 返回 false，先核对方法名、返回类型名、参数类型和顺序。
2. 返回变量没有变化，确认连接类型不是普通 `QueuedConnection`，并确认目标方法确实有返回值。
3. 崩溃或乱码，检查 `data` 是否指向已销毁、const 或类型不匹配的对象。
4. 同线程调用 `BlockingQueuedConnection` 造成卡死，改用 `DirectConnection` 或重新设计异步回调。
5. 新代码无法安全维护时，去掉手写 `QGenericReturnArgument`，改用类型安全 `invokeMethod`。
