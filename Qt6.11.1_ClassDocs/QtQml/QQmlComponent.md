# QQmlComponent
> Qt 6.11.1 · Qt QML · 来自 `QQmlComponent`

## 作用定位

`QQmlComponent` 是 QML 组件工厂：它先加载/编译某个 QML 类型，再按需创建对象实例。相比 `QQmlApplicationEngine`，它更适合“运行期创建很多对象”“自定义上下文”“异步加载和孵化”“分阶段创建”的场景。

## 类说明

- 头文件：`#include <QQmlComponent>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 关键状态：`Null`、`Loading`、`Ready`、`Error`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 从 engine、文件名、URL、模块 URI/typeName 创建组件，可指定同步/异步编译。 |
| `loadUrl()` / `loadFromModule()` / `setData()` | 后续加载 URL、模块类型或内存 QML 数据。 |
| `CompilationMode` | `PreferSynchronous` 尽量同步，`Asynchronous` 后台加载/编译。 |
| `status()` / `isReady()` / `isLoading()` / `isError()` / `isNull()` | 判断组件加载状态。 |
| `progress()` / `progressChanged()` | 观察异步加载进度。 |
| `errors()` | 读取编译或加载错误。 |
| `create(context)` | 直接创建对象，最常见入口。 |
| `createWithInitialProperties()` | 创建前注入初始属性。 |
| `beginCreate()` / `completeCreate()` | 分阶段创建：先实例化和设常量，再完成绑定和 componentComplete。 |
| `create(incubator, context, forContext)` | 使用 `QQmlIncubator` 异步创建对象。 |
| `setInitialProperties(object, properties)` | 给 beginCreate 后的对象设置初始属性。 |
| `creationContext()` | 组件定义时的上下文。 |
| `engine()` / `url()` | 查询所属引擎和来源 URL。 |
| `statusChanged()` | 状态变化通知。 |

## 创建方式选择

| 场景 | 建议 |
| --- | --- |
| 小组件、同步创建可接受 | `create()`。 |
| 需要在 QML 完成前设置属性 | `beginCreate()` + `setInitialProperties()` + `completeCreate()`。 |
| 组件较重，不想卡界面 | `CompilationMode::Asynchronous` + `QQmlIncubator`。 |
| 从模块加载注册类型 | Qt 6.5 起用 `loadFromModule()` 或 URI/typeName 构造。 |

## 常见坑与经验

- 调用 `create()` 前必须确认 `isReady()`；如果状态是 `Loading`，等 `statusChanged(Ready)`。
- `create()` 返回的根对象所有权要明确，通常设置 parent 或交给 QML 视觉树管理。
- `beginCreate()` 后如果不调用 `completeCreate()`，对象处于半初始化状态，绑定和 `componentComplete()` 不完整。
- `errors()` 不只在语法错误时有用，import 路径、类型缺失、属性赋值失败都可能出现在这里。
- 异步编译不等于异步实例化，重对象创建还要结合 incubator。

## 知识点覆盖

- QML 组件加载/编译/实例化
- 同步与异步编译
- 分阶段创建生命周期
- 初始属性注入
- 孵化器创建
- 错误与进度处理
