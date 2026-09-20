# QQmlContext：决定 QML 名称、绑定和相对 URL 的作用域

> Qt 6.11.1 · `#include <QQmlContext>` · 模块：`Qt6::Qml` · 基类：`QObject`

`QQmlContext` 定义 QML 对象创建时可见的名称、`id`、上下文对象和相对 URL 基准。它主要解决局部实例化时“这份 QML 绑定看到哪些对象与值”的问题。

它很强，但也是隐藏依赖的来源。现代 QML 代码中，向 QML 暴露长期应用状态应优先使用注册类型、对象属性或 singleton；context property 对 QML 工具、静态分析和后续维护者都不可见。

## 创建前完成上下文配置

```cpp
#include <QQmlComponent>
#include <QQmlContext>
#include <QQmlEngine>

QQmlEngine engine;
QQmlContext context(engine.rootContext());
context.setContextProperties({
    {u"accountName"_s, u"Ada"_s},
    {u"retryCount"_s, 3},
});

QQmlComponent component(&engine, QUrl(u"qrc:/ui/Panel.qml"_s));
QObject *panel = component.create(&context);
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

在该 context 中创建对象后再设置 context object 或新增 context property，会强制重新求值大量绑定，代价很高。应先完成 setup，再交给 `QQmlComponent::create()`。

## 上下文层级与生命周期

根 context 属于 `QQmlEngine`；每个组件实例又会产生自己的 context，某些 QML 元素还会再建立子 context。子 context 继承父 context 的属性，同名属性在子 context 中覆盖父值。

创建者必须销毁自己创建的 `QQmlContext`，最简单的方式是给它设置 QObject parent。销毁 context 不一定销毁已创建的 QML 对象，但这些对象的绑定属于 context：context 消失后，仍存活对象的绑定将停止求值。

`isValid()` 需要 engine 仍在，并且 context object（若有）尚未删除。不要把 context 生命周期设得短于依赖它的动态 QML 对象。

## Context property、context object 与 id 查找

`setContextProperty(name, value)` 可加入 QObject 或 QVariant 值；QQmlContext **不拥有**传入的 QObject。显式 context property 的优先级高于 context object 的同名属性。

`setContextObject()` 会将该 QObject 的属性整体暴露为上下文名称，并通过 NOTIFY 信号追踪变化；在大量相关属性场景中，它比逐项维护 context property 更高效。但对新设计仍应优先 singleton 或正常 QML 属性，因为两者都形成工具不可见的隐式输入。

`contextProperty()` 会向父 context 搜索，也会考虑 context object。`objectForName()` 和 `nameForObject()` 只在当前 context 查找，适合 QML `id` 或已注册 QObject 名称的精确映射。Qt 6.11 的 `findObjectRecursively()` / `findObjectsRecursively()` 会在本 context 及子 context 中按广度优先查找同名 `id`；委托和视图中同一 id 可出现多次。

## URL 解析边界

`baseUrl()` 默认来自包含组件；`setBaseUrl()` 覆盖它。`resolvedUrl()` 用该基准解析相对 URL。动态 `setData()` 或手工 component 装载时，明确 base URL 可避免资源路径和错误位置都指向错误目录。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlContext(engine/parentContext, parent)` | 创建子上下文 | 创建者负责销毁，推荐设置 QObject parent。 |
| `isValid()` | 判断 context 是否仍可用 | engine 或 context object 被销毁后失效。 |
| `engine()` | 取得所属 engine | engine 已销毁时返回空。 |
| `parentContext()` / `childContexts()` | 查询层级 | `childContexts()` 为 Qt 6.11 起的直接子 context 列表。 |
| `setContextProperty(name, QObject*)` | 暴露 QObject 名称 | context 不取得 QObject 所有权。 |
| `setContextProperty(name, QVariant)` | 暴露值名称 | 创建对象后新增会触发昂贵的绑定刷新。 |
| `setContextProperties(pairs)` | 批量加入属性 | 比逐项调用减少重复刷新。 |
| `setContextObject(object)` | 批量暴露 QObject 属性 | 同样是隐式依赖；新代码优先 singleton/对象属性。 |
| `contextObject()` | 读取 context object | 可为空。 |
| `contextProperty(name)` | 查上下文值 | 会沿父 context 查找，并考虑 context object。 |
| `objectForName(name)` | 查当前 context 中 QObject | Qt 6.2 起；不沿父 context 搜索。 |
| `nameForObject(object)` | 查对象在当前 context 的名称 | 多名称时返回第一个；不沿父 context 搜索。 |
| `findObjectRecursively(id)` | 递归查一个 QML id | Qt 6.11 起；多匹配只返回广度优先的首个。 |
| `findObjectsRecursively(id)` | 递归查全部同名 id | Qt 6.11 起；视图/委托可有多个匹配。 |
| `baseUrl()` / `setBaseUrl()` | 查询/设置相对 URL 基准 | 覆盖包含组件默认 URL。 |
| `resolvedUrl(url)` | 按 context 解析相对 URL | 用于动态资源和组件路径。 |
| `importedScript(name)` | 取此 context 的导入脚本值 | 仅适合已在对应上下文导入的脚本。 |

`QQmlContext` 的价值在于局部作用域控制；它的风险也在于局部作用域控制。上下文配置应在创建前一次完成，并尽量不成为长期应用架构的依赖注入通道。
