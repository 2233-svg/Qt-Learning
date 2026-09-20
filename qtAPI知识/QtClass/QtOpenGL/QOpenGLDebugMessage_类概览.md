# QOpenGLDebugMessage 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLDebugMessage>`  
> 所属模块：`Qt6::OpenGL`  
> 类型：隐式共享、可重入的 OpenGL 调试消息值类型

## 它解决什么问题

OpenGL debug output 不只是一个字符串。每条消息还包含由谁产生、属于什么类别、严重程度如何、以及驱动或应用提供的数值 ID。`QOpenGLDebugMessage` 把这些字段包装为一个可复制、可放入容器、可通过信号传递的 Qt 值对象：

- `message()`：文本；
- `id()`：通常 vendor-specific 的数值 ID；
- `source()`：来源；
- `type()`：类别；
- `severity()`：严重级别。

它不负责从 OpenGL server 取消息或启动 debug output；这部分由 `QOpenGLDebugLogger` 完成。它的工作是表达一条消息，以及为应用或第三方库构造可插入日志的消息。

## 实际使用场景

### 接收实时 OpenGL 调试输出

`QOpenGLDebugLogger::messageLogged` 的参数就是 `QOpenGLDebugMessage`。接收者可以根据 `type()` 和 `severity()` 分类记录，或直接将它输出到 `QDebug`。

### 给渲染阶段写入标记

应用可以使用 `createApplicationMessage()` 创建 `"Begin shadow pass"` 这样的 marker，再调用 logger 的 `logMessage()`。这样驱动日志、GPU 调试器和应用自身日志中都能保留阶段边界。

### 标识第三方渲染库

插件、引擎模块和外部工具产生的诊断信息可使用 `createThirdPartyMessage()`，使过滤规则能区分其来源。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL)
target_link_libraries(mytarget PRIVATE Qt6::OpenGL)
```

```cpp
#include <QDebug>
#include <QOpenGLDebugMessage>

const QOpenGLDebugMessage marker =
    QOpenGLDebugMessage::createApplicationMessage(
        QStringLiteral("Begin geometry pass"),
        101,
        QOpenGLDebugMessage::NotificationSeverity,
        QOpenGLDebugMessage::MarkerType);

qDebug() << marker;
```

要真正写入 OpenGL debug log，还需已初始化的 `QOpenGLDebugLogger`：

```cpp
logger->logMessage(
    QOpenGLDebugMessage::createApplicationMessage(
        QStringLiteral("Upload material textures")));
```

## 成员数据的语义

### `Source` 与 `Sources`

| 取值 | 含义 |
| --- | --- |
| `InvalidSource` | 无效来源；默认构造消息使用它。 |
| `APISource` | OpenGL API 调用产生。 |
| `WindowSystemSource` | 窗口系统产生。 |
| `ShaderCompilerSource` | shader compiler 产生。 |
| `ThirdPartySource` | 第三方框架、工具或库产生。 |
| `ApplicationSource` | 应用自身产生。 |
| `OtherSource` | 枚举未覆盖的来源。 |
| `AnySource` | 匹配全部来源的筛选掩码。 |

`Sources` 是 `QFlags<Source>`，可用按位或组合多个具体来源。

### `Type` 与 `Types`

| 取值 | 含义 |
| --- | --- |
| `InvalidType` | 无效类别；默认构造消息使用它。 |
| `ErrorType` | OpenGL 错误。 |
| `DeprecatedBehaviorType` | 使用已弃用行为。 |
| `UndefinedBehaviorType` | 存在未定义行为。 |
| `PortabilityType` | 依赖 vendor 特有行为，可能影响可移植性。 |
| `PerformanceType` | 性能问题。 |
| `OtherType` | 未列入枚举的其他类型。 |
| `MarkerType` | 调试标记。 |
| `GroupPushType` | debug group 入栈事件。 |
| `GroupPopType` | debug group 出栈事件。 |
| `AnyType` | 匹配全部类型的筛选掩码。 |

`Types` 是 `QFlags<Type>`。

### `Severity` 与 `Severities`

| 取值 | 含义 |
| --- | --- |
| `InvalidSeverity` | 无效级别；默认构造消息使用它。 |
| `HighSeverity` | 高严重度。 |
| `MediumSeverity` | 中严重度。 |
| `LowSeverity` | 低严重度。 |
| `NotificationSeverity` | 通知性信息。 |
| `AnySeverity` | 匹配全部级别的筛选掩码。 |

`Severities` 是 `QFlags<Severity>`。

`AnySource`、`AnyType`、`AnySeverity` 适合传给 logger 的过滤 API，不应把它们当作一条具体自定义消息的 source、type 或 severity。

## 默认构造不是“空但有效”的日志消息

默认构造的对象具有：

- 空文本；
- `id == 0`；
- `InvalidSource`；
- `InvalidType`；
- `InvalidSeverity`。

它适合容器占位、延后赋值或 API 返回默认值，不适合直接写入 debug log。需要自定义有效消息时，请使用 `createApplicationMessage()` 或 `createThirdPartyMessage()`，并传入有效 type 和 severity。

## 值语义、比较与线程

`QOpenGLDebugMessage` 是隐式共享值类型，文档标注其所有成员函数可重入。可以安全地把一条已获得的消息作为值传给 `QList`、信号槽、日志队列或后台处理代码。

可重入不等于任意共享对象无需同步：若多个线程同时修改同一个外部容器或写同一个输出设备，仍然需要按容器和 I/O 对象的线程规则组织。

比较时，`operator==` 要求五个字段全部相同：文本、ID、source、type、severity。仅凭 ID 判定同一问题不可靠，因为驱动 ID 通常是 vendor-specific。

## 逐项 API 说明

### 成员类型

#### `enum QOpenGLDebugMessage::Source` / `Sources`

描述消息来源。`Sources` 可以组合多个 source，用于 logger 筛选。

#### `enum QOpenGLDebugMessage::Type` / `Types`

描述消息类别。`Types` 可以组合错误、性能、弃用等多个类别。

#### `enum QOpenGLDebugMessage::Severity` / `Severities`

描述严重程度。`Severities` 可组合多个级别。

### 构造、工厂与查询

#### `QOpenGLDebugMessage::QOpenGLDebugMessage()`

构造无效默认消息。source/type/severity 均为 `Invalid*`，不应用作待插入日志的自定义消息。

#### `QOpenGLDebugMessage::QOpenGLDebugMessage(const QOpenGLDebugMessage &debugMessage)`

复制消息值。类是隐式共享的，复制通常很轻量。

#### `QOpenGLDebugMessage::~QOpenGLDebugMessage() noexcept`

销毁消息值对象；不影响 logger、OpenGL context 或 OpenGL server 内部日志。

#### `static QOpenGLDebugMessage createApplicationMessage(const QString &text, GLuint id = 0, Severity severity = NotificationSeverity, Type type = OtherType)`

创建 source 为 `ApplicationSource` 的消息。默认是通知级别和 `OtherType`，适合应用插入阶段标记或诊断文本。

#### `static QOpenGLDebugMessage createThirdPartyMessage(const QString &text, GLuint id = 0, Severity severity = NotificationSeverity, Type type = OtherType)`

创建 source 为 `ThirdPartySource` 的消息。适合表示第三方库、框架或工具产生的信息。

#### `Source source() const`

返回消息来源。

#### `Type type() const`

返回消息类别。

#### `Severity severity() const`

返回严重级别。

#### `GLuint id() const`

返回数值 ID。它一般是驱动厂商定义的值，不能假定跨平台稳定。

#### `QString message() const`

返回消息文本。

### 值操作

#### `void swap(QOpenGLDebugMessage &other) noexcept`

快速交换两个消息对象，不涉及 OpenGL context。

#### `QOpenGLDebugMessage &operator=(const QOpenGLDebugMessage &debugMessage)`

复制赋值消息内容。

#### `QOpenGLDebugMessage &operator=(QOpenGLDebugMessage &&debugMessage) noexcept`

移动赋值消息内容。

#### `bool operator==(const QOpenGLDebugMessage &debugMessage) const`

当文本、ID、source、type、severity 五个字段都相同才返回 `true`。

#### `bool operator!=(const QOpenGLDebugMessage &debugMessage) const`

等价于 `!operator==()`。

### 相关非成员函数

#### `QDebug operator<<(QDebug, Severity)`

把严重级别写入调试流。

#### `QDebug operator<<(QDebug, Source)`

把消息来源写入调试流。

#### `QDebug operator<<(QDebug, Type)`

把消息类别写入调试流。

#### `QDebug operator<<(QDebug, const QOpenGLDebugMessage &)`

把整条调试消息写入调试流，适合 `qDebug() << message`。

## 使用边界

- 两个工厂函数只创建 Qt 值对象，不会自动写入 OpenGL debug log。
- 调用 `QOpenGLDebugLogger::logMessage()` 时，消息 source 必须为 `ApplicationSource` 或 `ThirdPartySource`，type 和 severity 必须有效。
- 自定义消息文本最终以 UTF-8 传给 OpenGL，实际允许长度受 logger 的 `maximumMessageLength()` 字节上限约束。
- `Any*` 是筛选掩码，不是单条消息应使用的普通属性值。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Source` / `Sources` | 表示消息来源并支持 flags 组合。 | 默认消息为 `InvalidSource`；`AnySource` 用于筛选。 |
| 类型 | `Type` / `Types` | 表示错误、性能、标记等类别。 | `InvalidType` 不是有效日志类别；`AnyType` 用于筛选。 |
| 类型 | `Severity` / `Severities` | 表示严重程度。 | `InvalidSeverity` 不是有效日志级别；`AnySeverity` 用于筛选。 |
| 构造 | `QOpenGLDebugMessage()` | 创建默认无效消息。 | 不能直接作为待插入日志的消息。 |
| 构造 | `QOpenGLDebugMessage(const QOpenGLDebugMessage &)` | 复制消息值。 | 类隐式共享，适合容器和信号传递。 |
| 工厂 | `createApplicationMessage()` | 创建应用来源消息。 | 不会自动写入 logger。 |
| 工厂 | `createThirdPartyMessage()` | 创建第三方来源消息。 | 不会自动写入 logger。 |
| 查询 | `source()` / `type()` / `severity()` | 读取消息分类字段。 | 可用于日志路由和筛选。 |
| 查询 | `id()` | 读取消息数值 ID。 | 通常是 vendor-specific。 |
| 查询 | `message()` | 读取文本内容。 | 写入 OpenGL 时受 UTF-8 字节长度限制。 |
| 值语义 | `swap()` / `operator=()` | 交换、复制或移动消息。 | 只改变值对象，不操作 OpenGL log。 |
| 比较 | `operator==()` / `operator!=()` | 判断两条消息是否完全相同。 | 比较全部五个字段，不能只看 ID。 |
| 输出 | `operator<<(QDebug, ...)` | 输出枚举或消息。 | 用于诊断，不会写入 OpenGL log。 |

### 一句话总结

`QOpenGLDebugMessage` 是一条结构化 OpenGL 诊断信息的值对象：用工厂创建有效消息，用 source/type/severity 分类，再由 `QOpenGLDebugLogger` 负责真正写入或接收。
