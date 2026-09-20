# QQmlContext
> Qt 6.11.1 · Qt QML · 来自 `QQmlContext`

## 作用定位

`QQmlContext` 是 QML 名字查找和作用域链的一环。它保存 context object、context property、base URL，并连接父子上下文。QML 表达式解析标识符时，会沿上下文链查找这些名字。

它很强大，也很容易被滥用。上下文属性适合应用启动时注入少量全局对象，不适合大量动态业务状态。

## 类说明

- 头文件：`#include <QQmlContext>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 构造：可从父上下文或 `QQmlEngine` 创建

## API 速查

| API | 说明 |
| --- | --- |
| `setContextProperty(name, QObject*/QVariant)` | 向 QML 作用域注入命名值。 |
| `setContextProperties()` | 批量注入 `PropertyPair`。 |
| `contextProperty()` | 读取上下文属性。 |
| `setContextObject()` / `contextObject()` | 设置一个 QObject，其属性可被作为上下文属性访问。 |
| `parentContext()` / `childContexts()` | 查询上下文层级；`childContexts()` 为 Qt 6.11 新增。 |
| `engine()` | 返回所属 QML 引擎。 |
| `isValid()` | 上下文是否仍有效。 |
| `setBaseUrl()` / `baseUrl()` / `resolvedUrl()` | 控制相对 URL 解析。 |
| `nameForObject()` | 查找上下文里某对象对应的 id/name。 |
| `objectForName()` | Qt 6.2 起按 id/name 找对象。 |
| `findObjectRecursively()` / `findObjectsRecursively()` | Qt 6.11 起递归查找 id 对象。 |

## 使用场景

- 在加载 QML 前注入 `backend`、`settings`、`appModel` 等 C++ 对象。
- 为动态创建组件提供局部上下文。
- 根据组件来源调整相对 URL 基准。
- 调试 QML 对象 id 与上下文关系。

## 常见坑与经验

- 加载对象后再修改上下文属性会触发绑定重新求值，可能代价很高，也可能改变已经稳定的状态。
- context property 没有像 QML 注册类型那样的显式 import 依赖，项目大了会降低可读性。
- context object 的属性变化仍依赖 NOTIFY 信号；没有 NOTIFY 的属性不会自动驱动绑定刷新。
- 上下文失效后，基于它创建的表达式或对象名字查询也可能失效。
- 优先考虑注册类型、单例或 model；context property 适合入口注入，不适合作为通用数据总线。

## 知识点覆盖

- QML 作用域链和名字解析
- context property 与 context object
- base URL 与资源解析
- QML id/name 查找
- 上下文生命周期对绑定的影响
