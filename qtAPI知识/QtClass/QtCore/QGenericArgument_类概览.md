# Qt QGenericArgument 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGenericArgument>`  
> 所属模块：`Qt6::Core`  
> 类型性质：元对象调用的内部参数包装  
> 相关 API：`Q_ARG`、`QMetaObject::invokeMethod`、`QGenericReturnArgument`

## 1. 它解决什么问题

`QGenericArgument` 是 Qt 元对象系统用来保存“参数类型名 + 参数地址”的低层包装。它让旧式字符串调用可以把运行时才知道的参数传给：

```cpp
QMetaObject::invokeMethod(object, "method", ...);
```

它不负责类型检查、内存管理、复制或序列化。它只是把调用方已经准备好的数据地址和类型名称交给元对象系统。

这也是一个重要结论：普通业务代码几乎不应该直接构造 `QGenericArgument`。Qt 文档明确建议使用 `Q_ARG(Type, value)` 宏，让编译器和 Qt 的包装类型正确填充元类型信息。

## 2. 实际使用场景

### 2.1 推荐：用 `Q_ARG`

```cpp
QString text = QStringLiteral("hello");
const bool ok = QMetaObject::invokeMethod(
    receiver,
    "setText",
    Qt::DirectConnection,
    Q_ARG(QString, text));
```

在 Qt 6.5 及以后，优先使用类型安全的 functor/member-pointer `invokeMethod` 重载；只有调用目标是运行时字符串、旧接口或动态元对象场景时，才需要旧式 `Q_ARG`。

### 2.2 直接构造只适合桥接层

```cpp
QGenericArgument argument("QString", &text);
```

这段代码可以表达一个底层包装，但调用方必须自己保证：

- `name` 与实际数据类型完全匹配；
- `data` 在元对象调用完成前一直有效；
- 数据的 const、对齐和对象生命周期都正确；
- 使用的连接类型允许这种参数传递。

任一条件不满足，都可能产生调用失败、错误转换或未定义行为。

## 3. 参数模型和生命周期

### 3.1 `name` 是类型名，不是参数变量名

在 `Q_ARG(QString, text)` 中，宏会使用 `QString` 作为类型信息。它不是把变量名 `text` 传给目标槽，而是为元对象系统描述参数类型。

直接构造时的 `name` 应与元对象签名能够识别的类型名一致。不要把 `"text"`、`"arg1"` 之类变量名当成类型名。

### 3.2 `data` 是外部存储地址

`QGenericArgument` 不拥有 `data` 指向的对象，不会替调用方分配、复制或销毁它。构造临时对象时尤其要注意：

```cpp
// 只适用于调用期间对象仍然有效的同步调用。
QMetaObject::invokeMethod(object, "setText",
                          Qt::DirectConnection,
                          Q_ARG(QString, QStringLiteral("hello")));
```

如果使用 queued invocation，Qt 需要把参数保存到事件中，参数必须满足对应的可复制和元类型要求。不要把指向即将销毁的局部数据的裸指针交给异步调用。

### 3.3 不要用 `data()` 绕过类型系统

`data()` 的返回类型是 `void *`，这是历史 ABI 和元对象调用接口的需要，并不意味着调用方可以安全地修改任何参数。实际指针可能原本指向 const 对象，只有在确认真实类型和可写性后才能转换。

## 4. `QMetaObject::invokeMethod` 的版本选择

Qt 6.5 起，`QMetaObject::invokeMethod` 增加了更多基于成员函数指针和 functor 的重载；Qt 6.7 又扩展了 functor 返回值形式。新代码优先：

```cpp
QMetaObject::invokeMethod(receiver, [receiver] {
    receiver->refresh();
}, Qt::QueuedConnection);
```

这些重载通常比字符串 + `QGenericArgument` 更能在编译期发现签名错误。旧式参数包装仍适用于动态方法名、旧代码和需要 `Q_ARG` / `Q_RETURN_ARG` 的元对象桥接。

## 5. 逐项 API 说明

#### `QGenericArgument::QGenericArgument(const char *name = nullptr, const void *data = nullptr)`

用类型名指针和数据地址构造包装对象：

- `name` 可为空，表示没有提供类型名；
- `data` 可为空，表示没有提供参数存储；
- 两个指针都只是借用，不发生深拷贝；
- 由调用者负责保证指向对象和字符串在使用期间有效。

一般使用 `Q_ARG(Type, value)`，不要手写此构造函数。

#### `void *QGenericArgument::data() const`

返回构造时保存的数据地址。返回类型是 `void *`，但不应据此推断数据可写。它主要供 Qt 元对象内部读取。

如果手动转换返回值，必须确认实际类型、对象生命周期、对齐和 const 约束；错误转换不会由 `QGenericArgument` 保护。

#### `const char *QGenericArgument::name() const`

返回构造时保存的类型名指针。它返回的是原始字符串指针，不是 `QMetaType` 对象，也不会替调用方检查名字是否注册或是否和 `data()` 匹配。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QGenericArgument(name, data)` | 保存类型名和数据地址 | 不拥有数据，不校验类型 |
| `data()` | 取出数据地址 | 返回 `void *` 不代表可写 |
| `name()` | 取出类型名 | 返回原始字符串指针，不做匹配检查 |
| `Q_ARG(Type, value)` | 推荐的参数包装入口 | 优先于手写构造 |
| `QMetaObject::invokeMethod(..., Q_ARG(...))` | 动态元对象调用 | queued 调用要满足可复制/元类型要求 |

## 7. 与相邻类型的关系

- `QGenericArgument`：输入参数的低层包装。
- `QGenericReturnArgument`：返回值的低层包装，内部保存可写地址。
- `Q_ARG(Type, value)`：创建输入参数包装的推荐宏。
- `Q_RETURN_ARG(Type, value)`：创建返回参数包装的推荐宏。
- `QMetaMethodArgument`：新式元方法调用接口使用的更强类型参数描述。

## 8. 排查顺序

1. 动态调用失败，先检查字符串方法名和参数类型名是否与 `Q_OBJECT` 元对象签名一致。
2. 发现异步调用后数据异常，检查 `data` 指向的对象是否在事件执行前已经销毁。
3. 出现类型转换或崩溃，停止手写 `QGenericArgument`，改用 `Q_ARG` 或新式 functor `invokeMethod`。
4. 需要返回值时，不要把可写结果地址包装成普通 `QGenericArgument`，应使用 `Q_RETURN_ARG`。
5. 参数类型未注册或不可复制时，检查连接类型和 `QMetaType` 注册要求。
