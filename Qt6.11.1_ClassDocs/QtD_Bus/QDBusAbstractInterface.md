# QDBusAbstractInterface
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusAbstractInterface`

## 作用定位

`QDBusAbstractInterface` 是 Qt D-Bus “远端对象代理”的基类。它保存 service、object path、interface、connection 和 timeout，并提供同步调用、异步调用、回调式调用等通用能力。平时很少直接实例化它，而是使用 `QDBusInterface` 或由 `qdbusxml2cpp` 生成的强类型代理类。

它解决的问题是：调用者不想手工组装 `QDBusMessage`，只想像“调用某个接口上的某个方法”一样发起 D-Bus 请求，同时还能获取错误、超时和异步结果。

## 类说明

- 头文件：`#include <QDBusAbstractInterface>`
- CMake：链接 `Qt6::DBus`
- 继承：`QObject`
- 直接派生：`QDBusConnectionInterface`、`QDBusInterface`
- 对象规则：不可复制；受 QObject parent 和线程归属约束

## API 速查

| API | 说明 |
| --- | --- |
| `call(method, args...)` | 默认同步调用远端方法，返回 `QDBusMessage`；错误会反映到 `lastError()`。 |
| `call(mode, method, args...)` | 指定调用模式，如不等待回复、阻塞、等待时处理事件等。 |
| `callWithArgumentList(mode, method, args)` | 参数已在 `QList<QVariant>` 中时使用，适合动态参数列表。 |
| `asyncCall(method, args...)` | 发起异步调用，返回 `QDBusPendingCall`。 |
| `asyncCallWithArgumentList(method, args)` | 动态参数列表版本的异步调用。 |
| `callWithCallback(method, args, receiver, returnMethod, errorMethod)` | 成功和失败分派到不同槽。 |
| `callWithCallback(method, args, receiver, slot)` | 旧式单槽回调，已不推荐。 |
| `connection()` | 代理使用的 D-Bus 连接。 |
| `service()` | 目标服务名。 |
| `path()` | 目标对象路径。 |
| `interface()` | 目标接口名。 |
| `isValid()` | 代理对象是否有效；不能保证远端永远在线。 |
| `lastError()` | 最近一次调用或初始化产生的 D-Bus 错误。 |
| `setTimeout()` / `timeout()` | 设置或读取未来调用的超时时间，单位毫秒，`-1` 表示默认。 |
| `setInteractiveAuthorizationAllowed()` | 允许异步调用设置交互式授权 flag。 |
| `isInteractiveAuthorizationAllowed()` | 读取上述授权设置。 |

## 调用方式选择

| 场景 | 建议 |
| --- | --- |
| 简单命令行工具、初始化阶段 | `call()` 可以接受，但要检查错误。 |
| GUI 主线程、可能慢的远端服务 | 优先 `asyncCall()` + `QDBusPendingCallWatcher`。 |
| 参数数量运行期才确定 | `callWithArgumentList()` 或 `asyncCallWithArgumentList()`。 |
| 想把结果直接送进对象槽 | `callWithCallback()`。 |
| 不需要回复 | 使用 `QDBus::NoWaitForReply`，或服务端方法标 `Q_NOREPLY`。 |

## 使用场景

- `QDBusInterface` 内部复用的基础调用层。
- `qdbusxml2cpp` 生成的代理类基类。
- 需要统一设置超时、授权 flag、错误读取的 D-Bus 客户端封装。
- 动态选择同步/异步调用模式的框架代码。

## 常见坑与经验

- `isValid()` 只说明代理创建阶段没有明显错误；D-Bus 是分布式 IPC，远端随时可能退出，真正的调用仍要检查返回消息或 `lastError()`。
- `call()` 等待远端返回，远端如果做 I/O、授权或激活，调用线程就会一起等。GUI 中更推荐 watcher。
- `UseEventLoop` / GUI 阻塞模式会让事件循环继续派发事件，代码要能承受重入。
- 模板版本的 `call()` 要求参数能转换成 `QVariant` 并且已向 Qt 元类型系统注册；自定义结构需要 `Q_DECLARE_METATYPE` 和 D-Bus stream operator。
- `callWithCallback()` 返回 `true` 只代表请求成功排队，不代表远端执行成功。
- `setTimeout()` 是之后调用的设置，不会改变已经发出的 pending call。

## 知识点覆盖

- D-Bus 远端对象代理模型
- 同步、异步、回调式调用差异
- `QDBus::CallMode` 对阻塞和事件循环的影响
- `QVariant` 参数封送
- `QDBusPendingCall` 与 watcher 协作
- D-Bus 错误读取与超时设置
