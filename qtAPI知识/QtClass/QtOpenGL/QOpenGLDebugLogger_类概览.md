# QOpenGLDebugLogger 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLDebugLogger>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QObject`

## 它解决什么问题

一次 OpenGL 错误常常只表现为“画面没了”。`glGetError()` 能看到有限错误码，却看不到许多关键诊断，例如 shader compiler 提示、弃用 API、性能警告、可移植性问题和 debug group 事件。

`QOpenGLDebugLogger` 将 OpenGL 的 debug output 接入 Qt 对象模型，提供：

- 读取 OpenGL 内部 debug log；
- 用 `messageLogged()` 实时接收新消息；
- 异步与同步两种日志模式；
- 按 source、type、severity 或 ID 过滤；
- 建立和退出 debug group；
- 插入应用或第三方自定义消息。

它依赖当前 OpenGL context 的 `GL_KHR_debug` 扩展。它不是独立的文本日志器，初始化和使用都与具体 OpenGL context 绑定。

## 实际使用场景

### 开发阶段定位具体 OpenGL 调用

使用同步日志，在收到高严重度消息时设置断点。同步模式保证某条 OpenGL 调用引发的消息会在调用返回前产生，便于从调用栈追踪根因。

### 发布前监控性能与兼容性

异步日志开销较低，可用于收集性能、可移植性和弃用提示。通常再配合 `disableMessages()` 屏蔽噪声。

### 给渲染 pass 标注分组

`pushGroup("shadow pass")` 与 `popGroup()` 能让 debug output 显示层次。启用/禁用消息的过滤状态也以当前 group 为作用域。

### 读取实时日志启动之前的消息

初始化后调用 `loggedMessages()` 可以读取内部 log 中已经积累的信息。这个接口是“读取并清空”，用于补读早期消息，不是长期消息队列。

## 创建 debug context

OpenGL 实现为了性能可以在非 debug context 中不产生 debug output。创建 context 时应请求 debug context：

```cpp
#include <QOpenGLContext>
#include <QSurfaceFormat>

QSurfaceFormat format;
format.setMajorVersion(3);
format.setMinorVersion(3);
format.setProfile(QSurfaceFormat::CoreProfile);
format.setOption(QSurfaceFormat::DebugContext);

QOpenGLContext context;
context.setFormat(format);
if (!context.create()) {
    // context 创建失败。
}
```

创建完成后检查实际能力：

```cpp
if (!context.hasExtension(QByteArrayLiteral("GL_KHR_debug"))) {
    // QOpenGLDebugLogger 无法在此 context 上初始化。
}
```

请求 `DebugContext` 并不取代扩展检查，最终仍以 `initialize()` 返回值为准。

## 初始化与最小示例

以下代码必须运行在 `context` 已经 current 的位置，例如 `QOpenGLWidget::initializeGL()`：

```cpp
#include <QOpenGLDebugLogger>
#include <QOpenGLDebugMessage>

auto *logger = new QOpenGLDebugLogger(this);

if (!logger->initialize()) {
    // 没有 current context，或当前实现未提供 GL_KHR_debug。
    return;
}

connect(logger, &QOpenGLDebugLogger::messageLogged,
        this, [](const QOpenGLDebugMessage &message) {
            qDebug() << message;
        });

logger->startLogging(QOpenGLDebugLogger::AsynchronousLogging);
```

构造 logger 不会自动完成初始化。必须先有 current context，再检查 `initialize()`。

## 实时日志模式

### `AsynchronousLogging`

默认模式，性能开销较小。消息可能在引发它的 OpenGL 调用之后很久才到达，顺序也可能不同；实现甚至可能从不同于 context 绑定线程的线程发射消息。

因此：

- 不要用到达顺序精确还原 OpenGL 调用顺序；
- 默认 queued connection 可以帮助跨线程投递；
- 强制 `Qt::DirectConnection` 时，槽函数必须自己处理并发与线程安全。

### `SynchronousLogging`

同步模式性能开销明显更高，但 OpenGL 保证某命令产生的消息会在该命令返回前按顺序发出，并从 context 绑定线程发出。适合调试器断点和定位精确调用源。

运行期间不能直接切换模式；要改变模式，需要先 `stopLogging()`，再以新模式调用 `startLogging()`。

## 内部 debug log 与实时信号的关系

OpenGL 内部 log 容量有限，满后旧消息会被丢弃。`loggedMessages()` 会返回当前全部消息，并清空这些已返回的消息。

当实时日志开启后，新消息不会再写入内部 debug log，而是通过 `messageLogged()` 发出。实时日志启动前积累的内部消息不会自动补发为信号。

建议启动顺序：

1. 在 current context 中 `initialize()`；
2. 连接 `messageLogged()`；
3. `startLogging()`；
4. 调用一次 `loggedMessages()`，检查实时模式启用前的遗留消息。

若目标是不丢诊断，尽早开启实时日志，而不要只周期性轮询 `loggedMessages()`。

## 消息过滤和 debug group

`enableMessages()` / `disableMessages()` 有两类匹配方式：

- `sources + types + severities`，匹配任意 ID；
- `ids + sources + types`，匹配任意 severity。

消息的启用状态属于 `(id, source, type, severity)` 这个完整组合，不存在“source 的设置覆盖某个 type”这样的层级规则。因此多次 enable/disable 的调用顺序会影响最后结果。

过滤作用于当前 debug group：

- `pushGroup()` 新建 group，并继承当前顶层 group 的过滤设置；
- 在新 group 中改变过滤，只影响该 group；
- `popGroup()` 恢复外层 group 的过滤状态。

`pushGroup()` 的 source 只能是 `ApplicationSource` 或 `ThirdPartySource`。成功 push/pop 时，OpenGL 会分别产生 `GroupPushType`、`GroupPopType` 的通知消息。

## 自定义消息与长度限制

```cpp
const auto marker =
    QOpenGLDebugMessage::createApplicationMessage(
        QStringLiteral("Begin lighting pass"),
        100,
        QOpenGLDebugMessage::NotificationSeverity,
        QOpenGLDebugMessage::MarkerType);

logger->logMessage(marker);
```

`logMessage()` 的必要条件：

- logger 已成功 `initialize()`；
- message 的 source 是 `ApplicationSource` 或 `ThirdPartySource`；
- type 和 severity 有效。

`maximumMessageLength()` 返回可插入文本的最大长度，单位是 UTF-8 **字节**，不是 `QString` 的 UTF-16 code unit 数量。Qt 会自动截断超长消息；同一上限也适用于 debug group 名称。

## QObject、线程和 context 生命周期

`QOpenGLDebugLogger` 是 `QObject`，可以设置 parent 并使用信号槽；但 QObject 的线程归属不改变 OpenGL context 的使用规则。

`initialize()` 绑定的是调用时 current 的 context。要把已初始化 logger 用于另一个 context，必须先停止 logging，然后在新 context current 时重新 `initialize()`。在同一个 context 中重复初始化是安全的。

异步模式下 `messageLogged()` 可以由其他线程、甚至多个线程同时发射。接收槽若访问 UI、非线程安全容器或共享输出，必须使用合适的 queued 投递、互斥或专属消费线程。

## 逐项 API 说明

### 成员类型

#### `enum QOpenGLDebugLogger::LoggingMode`

- `AsynchronousLogging`：低开销，但消息时机、顺序和发射线程不保证。
- `SynchronousLogging`：高开销，但消息在相关 OpenGL 调用返回前、按顺序从 context 线程发出。

### 属性

#### `loggingMode : LoggingMode`

只读属性，对应 `loggingMode()`。只有日志已经启动时，该值才具备可依赖的实际意义。

### 构造和初始化

#### `explicit QOpenGLDebugLogger::QOpenGLDebugLogger(QObject *parent = nullptr)`

构造 logger QObject，可设置 parent 管理其生命周期。构造后还不能记录日志，必须调用 `initialize()`。

#### `virtual noexcept QOpenGLDebugLogger::~QOpenGLDebugLogger()`

销毁 logger。带 parent 的对象会由 QObject 树销毁，不要与其他所有权机制重复释放。

#### `bool QOpenGLDebugLogger::initialize()`

在 current OpenGL context 中初始化。该 context 必须支持 `GL_KHR_debug`；成功返回 `true`，失败返回 `false`。

可在同一 context 重复调用。若用它切换到另一个 context，调用时 logger 不能正在 logging。

### 状态和读取

#### `bool isLogging() const`

返回实时日志是否正在运行。

#### `LoggingMode loggingMode() const`

返回当前模式。尚未启动日志时不应基于该值做业务判断。

#### `qint64 maximumMessageLength() const`

返回可写入消息文本和 debug group 名称的最大 UTF-8 字节数。超长文本会截断。

#### `QList<QOpenGLDebugMessage> loggedMessages() const`

读取内部 debug log 的全部可用消息，并清空已读取内容。内部 log 有容量上限，不能作为不丢消息的永久队列。

### 分组和过滤

#### `void pushGroup(const QString &name, GLuint id = 0, Source source = ApplicationSource)`

压入一个 debug group。source 必须是 `ApplicationSource` 或 `ThirdPartySource`；成功后自动记录 `GroupPushType` 消息，新组继承原组过滤设置。

#### `void popGroup()`

弹出最上层 debug group。成功后自动记录 `GroupPopType` 消息，并恢复外层 group 的过滤设置。

#### `void enableMessages(Sources sources = AnySource, Types types = AnyType, Severities severities = AnySeverity)`

启用匹配 source/type/severity 的全部 ID 消息，作用于当前 group。

#### `void enableMessages(const QList<GLuint> &ids, Sources sources = AnySource, Types types = AnyType)`

启用指定 ID、source 和 type 的消息，匹配任意 severity，作用于当前 group。

#### `void disableMessages(Sources sources = AnySource, Types types = AnyType, Severities severities = AnySeverity)`

禁用匹配 source/type/severity 的全部 ID 消息，作用于当前 group。

#### `void disableMessages(const QList<GLuint> &ids, Sources sources = AnySource, Types types = AnyType)`

禁用指定 ID、source 和 type 的消息，匹配任意 severity，作用于当前 group。

### 实时日志槽与信号

#### `void logMessage(const QOpenGLDebugMessage &debugMessage)`

向 OpenGL debug log 插入应用或第三方消息。logger 必须已经初始化，且 source/type/severity 必须有效。

#### `void startLogging(LoggingMode loggingMode = AsynchronousLogging)`

开始实时日志，新消息通过 `messageLogged()` 发出。Qt 会保存启动时的 `GL_DEBUG_OUTPUT`、`GL_DEBUG_OUTPUT_SYNCHRONOUS` 和已安装回调，并在停止时恢复它们。

要改模式需先停止后重新开始。

#### `void stopLogging()`

停止实时日志，恢复启动时保存的 OpenGL debug output 状态与既有回调。

#### `void messageLogged(const QOpenGLDebugMessage &debugMessage)`

实时收到 OpenGL server 消息时发出。异步模式可能跨线程或并发发出；同步模式下从 context 绑定线程顺序发出。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `LoggingMode` | 选择异步或同步 debug output。 | 异步不保证顺序/线程；同步开销高。 |
| 属性 | `loggingMode` | 读取当前日志模式。 | 仅在已启动 logging 时有实际意义。 |
| 构造 | `QOpenGLDebugLogger(QObject *)` | 创建 QObject logger。 | 构造后必须先 `initialize()`。 |
| 生命周期 | `~QOpenGLDebugLogger()` | 销毁 logger。 | 遵守 QObject parent 所有权，避免重复释放。 |
| 初始化 | `initialize()` | 在 current context 绑定 debug API。 | 需要 `GL_KHR_debug`；改 context 前必须停止 logging。 |
| 状态 | `isLogging()` | 查询实时日志是否运行。 | 不表示内部 log 是否为空。 |
| 状态 | `loggingMode()` | 查询当前模式。 | 日志未启动时不应依赖。 |
| 查询 | `maximumMessageLength()` | 查询消息/组名 UTF-8 字节上限。 | 超长内容会截断，不能以 `QString::length()` 代替。 |
| 查询 | `loggedMessages()` | 读取并清空内部 debug log。 | 容量有限；实时日志开启后新消息不再写入内部 log。 |
| 分组 | `pushGroup()` | 压入 debug group。 | source 仅限应用/第三方；继承过滤规则。 |
| 分组 | `popGroup()` | 弹出 debug group。 | 恢复外层 group 的过滤规则。 |
| 过滤 | `enableMessages()` 两个重载 | 按属性或 ID 启用消息。 | 匹配完整 tuple，调用顺序影响最终状态。 |
| 过滤 | `disableMessages()` 两个重载 | 按属性或 ID 禁用消息。 | 过滤作用于当前 group。 |
| 写入 | `logMessage()` | 插入一条自定义日志。 | 需要初始化、合法 source/type/severity。 |
| 实时 | `startLogging()` | 开始实时消息信号。 | 改模式前先 stop；会临时接管部分 GL debug 状态。 |
| 实时 | `stopLogging()` | 停止实时消息。 | 恢复先前 GL debug 状态和回调。 |
| 信号 | `messageLogged()` | 接收 OpenGL server 消息。 | 异步模式下槽必须考虑跨线程并发。 |

### 一句话总结

`QOpenGLDebugLogger` 是绑定到一个 current OpenGL context 的诊断管道：先初始化并确认 `GL_KHR_debug`，再根据性能和定位需求选择异步或同步实时日志，必要时结合内部 log、过滤和 debug group 使用。
