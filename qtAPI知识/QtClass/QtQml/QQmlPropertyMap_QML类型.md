# QQmlPropertyMap：给 QML 提供可绑定的动态键值属性

> Qt 6.11.1 | `#include <QQmlPropertyMap>` | CMake: `Qt6::Qml`

`QQmlPropertyMap` 把一组运行时确定的键值对做成 QML 可读写、可参与绑定的对象属性。它解决的是领域数据字段不稳定或可配置时，不想为每个字段都写一个 `Q_PROPERTY` 的场景，例如用户资料、设备遥测、可扩展表单和设置面板。

这不是普通 `QVariantHash` 的直接替身：它是 `QObject`，能作为 context property 暴露给 QML，且每个键以属性形式参与 QML 表达式。

## 先建好字段，再暴露给界面

Qt 6.11.1 中直接构造 `QQmlPropertyMap(QObject *)` 已被弃用。未派生的普通用法应使用 `create()`：

```cpp
auto *owner = QQmlPropertyMap::create(this);
owner->insert("name", "Ada");
owner->insert("phone", "555-0100");
owner->freeze();

engine.rootContext()->setContextProperty("owner", owner);
```

```qml
Text { text: owner.name }
```

`create()` 返回可绑定的 map。让 map 有一个可靠的 QObject parent，或由更高层对象明确管理。`QQmlContext::setContextProperty()` 不取得所有权。

## 写入方向决定哪些钩子和信号会发生

C++ 侧用 `insert(key, value)` 更新值；不存在的键会被创建。批量更新优先使用 `insert(const QVariantHash &)`，比循环插入更高效。

QML 侧为可写值赋值时，`updateValue(key, input)` 是拦截点；派生类可在这里做范围限制、转换或拒绝策略，并返回最终要存储的 QVariant。

```cpp
class SettingsMap : public QQmlPropertyMap
{
    Q_OBJECT

public:
    SettingsMap(QObject *parent) : QQmlPropertyMap(this, parent) {}

protected:
    QVariant updateValue(const QString &key, const QVariant &input) override
    {
        if (key == "opacity")
            return std::clamp(input.toDouble(), 0.0, 1.0);
        return input;
    }
};
```

`updateValue()` 只为来自 QML 的更新调用，C++ 调用 `insert()` 不会经过它。同样，`valueChanged(key, value)` 只在 QML 更新某个值时发射；**C++ 的 `insert()` 和 `clear()` 不会发射此信号**。若 C++ 侧更新也要驱动业务逻辑，直接在更新路径发出自己的领域信号。

## clear 不是删除键，freeze 不是冻结值

`clear(key)` 让对应值变成无效 `QVariant`，但键仍然存在：`keys()` 仍会列出它，`size()` 仍会计数。这常被误解为从 map 中移除字段。

`freeze()` 自 Qt 6.1 起阻止再添加新键，同时为已有键启用内部缓存以加快 QML 访问；已有键仍然可以 `insert()` 修改或 `clear()`。当 schema 已确定、但数据持续刷新时，在初始化后 freeze 很合适。

非 const `operator[]` 会在键缺失时插入一个无效 QVariant，因此查询未知键时优先用 `contains()` 和 `value()`，不要无意间改变 schema。

## 适用边界

- 字段稳定且有严格类型、NOTIFY 和文档需求时，明确的 `Q_PROPERTY` 更适合长期 API。
- map 键来自外部输入时，要做白名单和名称校验；不要把它当作给 QML 任意扩展业务对象的通道。
- 传入 `QVariant` 时仍要考虑 QML 能否处理其元类型。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlPropertyMap::create(parent)` | 创建可绑定的 map | Qt 6.11 推荐入口；调用方安排 parent/所有权 |
| `insert(key, value)` | 设置或创建一个键 | C++ 更新不调用 `updateValue()`，也不发 `valueChanged()` |
| `insert(QVariantHash)` | 批量设置或创建键 | Qt 6.1 起提供；大批量更新优先用它 |
| `value(key)` | 读取键的值 | 缺失或已 clear 时返回无效 QVariant |
| `clear(key)` | 清空键的值 | 键不会被删除，仍会出现在 `keys()` 和计数中 |
| `contains()` / `keys()` / `size()` | 查询 schema 和键集合 | `keys()` 包含已 clear 的键 |
| `freeze()` | 禁止新增键并启用已有键缓存 | 仍可修改或清空已有键 |
| `valueChanged(key, value)` | QML 写入导致值改变时的通知 | `insert()` 与 `clear()` 不发射它 |
| `updateValue(key, input)` | 截获 QML 写入并返回要存储的值 | 仅 QML 侧更新会调用；派生时返回合法 QVariant |
| `operator[](key)` | 读写值的容器式入口 | 非 const 重载会隐式创建缺失键 |

## 相关类型

- `QQmlContext`：将 map 作为 context property 暴露给 QML。
- `QVariant` / `QVariantHash`：承载单个值和批量更新数据。
- `Q_PROPERTY`：字段固定时更明确、更类型安全的替代方案。
