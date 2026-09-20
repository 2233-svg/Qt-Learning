# QQmlContext::PropertyPair：批量设置上下文属性的一对名称和值

> Qt 6.11.1 · 定义于 `#include <QQmlContext>` · 模块：`Qt6::Qml`

`QQmlContext::PropertyPair` 是一个简单结构体：

```cpp
struct PropertyPair {
    QString name;
    QVariant value;
};
```

它解决的不是数据建模，而是批量调用 `QQmlContext::setContextProperties()` 时，把“上下文属性名”和“要暴露的值”作为一个明确条目传递。

## 为什么要用它

逐个 `setContextProperty()` 会让 QML context 反复更新可见名称并触发绑定刷新。多个值必须注入时，先组织成 `PropertyPair` 列表再一次提交，可避免不必要的重复刷新：

```cpp
QQmlContext context(engine.rootContext());
context.setContextProperties({
    {u"accountName"_s, u"Ada"_s},
    {u"maxRetries"_s, 3},
    {u"featureEnabled"_s, true},
});
```

这仍然只适合动态实例化等局部桥接场景。对常驻应用状态，优先使用 QML singleton、注册 QObject 类型或组件的显式属性，以保留工具可见性和可维护性。

## 字段语义与边界

- `name` 是 QML 上下文中要解析的标识符；命名冲突会遮蔽父 context 或 context object 中的同名名称。
- `value` 是 `QVariant`，可承载普通值或已注册的 Qt 元类型；`QObject *` 的生命周期并不会因为装入 Variant 就自动得到妥善管理。
- 批量设置应在此 context 创建任何 QML 对象之前完成。之后更新仍可能触发已有对象所有绑定的大范围重新求值。
- `PropertyPair` 本身不具备 NOTIFY、所有权或深拷贝语义；动态变化是否能被 QML 观察，取决于 `value` 所代表 QObject 的属性通知设计。

## API 速查表

| 项目 | 用途 | 语义与边界 |
| --- | --- | --- |
| `PropertyPair::name` | 指定上下文属性名 | 决定 QML 中可见的名字，可能遮蔽父 context 同名属性。 |
| `PropertyPair::value` | 指定要暴露的 QVariant | 只承载值；不自动解决 QObject 生命周期与通知。 |
| `QQmlContext::setContextProperties(list)` | 一次提交多个 Pair | 比逐项设置减少重复绑定刷新，应在对象创建前调用。 |
| `QQmlContext::setContextProperty()` | 设置单个名称和值 | 少量一次性设置可以使用；不要在运行期频繁注入。 |

它的职责非常窄：把一批上下文输入一次性描述清楚。真正需要长期维护的状态，仍应放在 QML 可见且可分析的对象接口中。
