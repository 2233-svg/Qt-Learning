# QGenericPluginFactory

> Qt 6.11.1 · Qt GUI · 来自 `QGenericPluginFactory`

## 1. 先建立直觉

`QGenericPluginFactory` 是 Qt 用来发现和创建通用 GUI 插件对象的静态工厂。插件作者实现 `QGenericPlugin::create()`，使用者或 Qt 内部通过工厂按 key 请求对象。

这个工厂不是通用的应用插件管理器。它服务于 Qt GUI 的通用插件机制，常见于平台输入、设备或底层后端扩展；普通业务插件通常会有自己的接口和加载策略。

## 2. 类说明

- 头文件：`#include <QGenericPluginFactory>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：纯静态工厂类，不需要实例化。
- 协作类：`QGenericPlugin` 提供实际插件实现。

可用 key 来自已加载或可发现的插件元数据。创建失败时返回 `nullptr`。

## 3. API 速查

| API | 用途 |
|---|---|
| `keys()` | 返回当前可用的通用插件 key 列表。 |
| `create(key, specification)` | 按 key 和附加说明创建 QObject 插件对象。 |

`key` 不区分大小写。`specification` 原样传给插件实现解释，工厂本身不理解它的业务含义。

## 4. 关键用法

```cpp
const QStringList available = QGenericPluginFactory::keys();

QObject *driver =
    QGenericPluginFactory::create(u"mydriver"_s, u"device=/dev/input0"_s);

if (!driver) {
    // 插件不存在、key 不匹配或 specification 无效。
}
```

调用方必须处理空返回。插件缺失、部署路径不正确、元数据不匹配、key 拼写错误或 specification 解析失败都可能导致创建失败。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 查看 Qt 当前能发现哪些通用插件 | 调用 `keys()`。 |
| 按名称创建底层驱动对象 | 调用 `create()` 并检查返回值。 |
| 应用业务层插件架构 | 不建议使用此工厂，设计专用接口更清楚。 |
| 调试插件部署 | 用 `keys()` 验证插件是否被发现，再尝试 `create()`。 |

## 6. 常见坑与经验

- `keys()` 为空不一定表示代码错，可能是部署目录没有对应插件或平台根本不需要该类插件。
- 工厂返回的是 `QObject *`，具体类型要由 key/specification 协议决定；转换前应确认类型。
- 不要假定 `specification` 有统一格式。每个插件可以定义自己的参数语法。
- 创建出的对象生命周期取决于调用方和插件约定，不能把工厂当作长期所有者。
- 插件发现受 Qt 插件路径、应用目录、环境变量和平台部署方式影响。

## 7. 知识点覆盖

- 通用 GUI 插件的发现与创建
- `QGenericPlugin` 与工厂的分工
- key、specification 和空返回处理
- QObject 类型转换与生命周期
- 插件部署路径和可用 key 调试
