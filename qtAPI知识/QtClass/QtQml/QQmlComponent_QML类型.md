# QQmlComponent：加载一个 QML 定义，再按需创建实例

> Qt 6.11.1 · `#include <QQmlComponent>` · 模块：`Qt6::Qml` · 基类：`QObject`

`QQmlComponent` 表示的是一份**组件定义**，而不是由它创建出来的对象。它解决动态页面、委托、插件界面和按需加载场景中“先编译/加载 QML，稍后创建零个或多个实例”的需求。

`QQmlApplicationEngine` 适合一次性启动根界面；需要复用定义、控制异步加载、指定上下文或分阶段注入初始属性时，使用 `QQmlComponent`。

## 正确的加载、检查与创建流程

```cpp
#include <QQmlComponent>
#include <QQmlEngine>
#include <QDebug>

QQmlEngine engine;
QQmlComponent component(&engine, QUrl(u"qrc:/ui/Badge.qml"_s));

if (!component.isReady()) {
    qWarning() << component.errors();
    return;
}

QObject *badge = component.createWithInitialProperties(
    {{u"text"_s, u"New"_s}});
if (!badge)
    qWarning() << component.errors();
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

`create()`、`createWithInitialProperties()` 成功时返回的对象**归调用者所有**。若根对象是 `QQuickItem`，还必须显式设置视觉父项 `setParentItem()`；仅设置 QObject parent 不会让它出现在场景中。

## 状态机决定何时可以 create

| 状态 | 含义 | 下一步 |
| --- | --- | --- |
| `Null` | 尚未设置源 | 调用 `loadUrl()`、`loadFromModule()` 或 `setData()`。 |
| `Loading` | 正在异步加载/编译 | 监听 `statusChanged()` 和 `progressChanged()`。 |
| `Ready` | 定义可创建 | 调用 `create...()` 或 incubator 版本。 |
| `Error` | 加载或创建失败 | 用 `errors()` / `errorString()` 诊断。 |

`Asynchronous` 只请求异步编译；后续创建仍要等 `Ready`。通过模块加载的 C++ 类型始终同步。`progress` 是 0 到 1 的加载进度，不是对象实例化进度。

## 创建方式的差异

- `create(context)`：一次性创建；未传上下文时使用 engine 的 root context。
- `createWithInitialProperties(map, context)`：在顶层初始化属性；未设置 required 属性会失败并返回 `nullptr`。
- `create(incubator, context, forContext)`：交给 `QQmlIncubator`，适合避免一次性创建大量对象卡住 UI。
- `beginCreate(context)` + `setInitialProperties()` + `completeCreate()`：高级两阶段创建。两步必须配对；不要依赖某个绑定一定在 `beginCreate()` 前或后执行，编译器优化会改变时机。

`setInitialProperties(object, map)` 只适用于 `beginCreate()` 与 `completeCreate()` 之间，不能直接设置嵌套初始属性。对值类型嵌套字段，先在 C++ 中构造完整值类型再整体传入。

## 载入来源和上下文

`loadUrl()` 的相对 URL 基于 `QQmlEngine::baseUrl()` 解析；从本地文件加载必须用 `QUrl::fromLocalFile()`，不要把 Windows 路径直接当通用 URL。`setData(data, baseUrl)` 的 `baseUrl` 同时用于相对引用和诊断；不要传入已有组件的 URL，因为新内存组件会遮蔽同 URL 的既有组件。

`creationContext()` 只对直接从 QML 创建的 component 有效。`isBound()`（Qt 6.5 起）反映该组件源文件是否声明 `pragma ComponentBehavior: Bound`，它不是“对象已绑定完所有属性”的状态。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlComponent(engine, source, mode)` | 创建并加载定义 | `source` 可为 URL、文件或模块类型；异步时等待 Ready。 |
| `CompilationMode::PreferSynchronous` | 默认加载策略 | 本地定义通常立即就绪。 |
| `CompilationMode::Asynchronous` | 异步加载/编译 | 不能在 `Loading` 时创建实例。 |
| `status` / `isNull()` / `isLoading()` / `isReady()` / `isError()` | 查询状态机 | 创建失败也应查看状态和 `errors()`。 |
| `progress` / `progressChanged()` | 观察加载进度 | 范围 0.0 到 1.0。 |
| `statusChanged(status)` | 观察状态变化 | 异步组件就绪后再创建。 |
| `errors()` / `errorString()` | 读取错误 | 覆盖最近一次编译或创建错误。 |
| `loadUrl(url, mode)` | 从 URL 加载定义 | 本地路径使用 `QUrl::fromLocalFile()`。 |
| `loadFromModule(uri, typeName, mode)` | 从模块加载类型 | Qt 6.5 起；C++ 实现类型总是同步。 |
| `setData(data, baseUrl)` | 从内存 QML 加载 | base URL 不能与已有组件 URL 冲突。 |
| `create(context)` | 同步创建对象 | 返回对象归调用者；视觉项仍需视觉父项。 |
| `createWithInitialProperties(map, context)` | 创建时写顶层初始属性 | required 属性未满足则失败。 |
| `create(incubator, context, forContext)` | 可孵化创建 | 通过 incubator 取状态和对象。 |
| `beginCreate()` / `completeCreate()` | 两阶段创建 | 必须成对调用；绑定时机不可假定。 |
| `setInitialProperties(object, map)` | 两阶段创建期间设置初值 | 只在 begin/complete 之间使用，不能直接写嵌套字段。 |
| `engine()` / `creationContext()` | 查询所属运行环境 | `creationContext()` 仅对 QML 直接创建的 component 有效。 |
| `isBound()` | 查询 Bound 组件行为 | Qt 6.5 起；不表示运行时绑定是否已求值。 |
| `url()` | 读取组件源 URL | 可用于定位错误和相对引用来源。 |

`QQmlComponent` 的关键是把“定义加载成功”和“实例创建成功”当作两件独立的事处理，两处都要检查错误和生命周期。
