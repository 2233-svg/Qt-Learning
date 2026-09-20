# QAccessibleAttributesInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleAttributesInterface`

## 1. 先建立直觉

`QAccessibleAttributesInterface` 为可访问对象提供标准 Role、State、Name 之外的附加元数据。它解决的是“这是一个标题，而且是第三级”“这段文字采用不同语言”“这个控件是水平的”这类结构性信息。

此接口用于补充语义，而不是塞进所有业务字段的杂物箱。能用明确的 Role、State、Value、Relation 或文本接口表达的内容，应优先用那些机制。

## 2. 类说明

- 头文件：`#include <QAccessibleAttributesInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：抽象可访问子接口；需要从主 `QAccessibleInterface` 的 `interface_cast()` 暴露。
- 协作枚举：`QAccessible::Attribute`，在 Qt 6.8 引入，部分键有更高版本要求。

平台后端会在可支持时将这些属性桥接到 ARIA、UI Automation、AT-SPI 或 NSAccessibility 等原生概念。不能假定每个属性在每个平台的辅助技术中都有同样表现。

## 3. API 速查

| API | 用途 |
|---|---|
| `attributeKeys()` | 列出当前对象实际支持的属性键。 |
| `attributeValue(key)` | 返回指定属性的 `QVariant` 值；不支持时返回无效 `QVariant`。 |
| `Attribute::Level` | `int`，表示标题、分组等结构层级。 |
| `Attribute::Locale` | `QLocale`，表示此对象内容的语言/区域；Qt 6.10 起。 |
| `Attribute::Orientation` | `Qt::Orientation`，表示横向或纵向；Qt 6.11 起。 |
| `Attribute::Custom` | `QHash<QString, QString>`，用于平台可桥接的自定义键值对。 |

## 4. 关键用法

```cpp
QList<QAccessible::Attribute> AccessibleHeading::attributeKeys() const
{
    return { QAccessible::Attribute::Level,
             QAccessible::Attribute::Locale };
}

QVariant AccessibleHeading::attributeValue(QAccessible::Attribute key) const
{
    switch (key) {
    case QAccessible::Attribute::Level:
        return 2;
    case QAccessible::Attribute::Locale:
        return QLocale(QLocale::English, QLocale::UnitedStates);
    default:
        return {};
    }
}
```

`attributeKeys()` 与 `attributeValue()` 必须一致：不要把一个键列出来却返回无效值，也不要为未列出的键返回数据。`QVariant` 中的实际类型必须遵从对应枚举的规定，不能用字符串替代 `int`、`QLocale` 或 `Qt::Orientation`。

## 5. 使用场景

| 需求 | 属性 | 说明 |
|---|---|---|
| 文档大纲、富文本标题 | `Level` | 配合 `Role::Heading` 传递层级，不靠字体大小猜测。 |
| 多语言文档的局部段落 | `Locale` | 让读屏以更合适的语言或发音规则处理该片段。 |
| 自定义滑轨、标签条、分割栏 | `Orientation` | 用于表达水平或垂直交互方向。 |
| 尚无 Qt 标准键的跨平台扩展 | `Custom` | 仅作为临时或平台特定补充，键值应稳定、文档化。 |

## 6. 常见坑与经验

- `Custom` 不是逃避语义建模的捷径。跨平台一致性最弱，优先使用强类型标准属性。
- 属性的值可能动态变化；变化后应发送恰当的 `QAccessible::AttributeChanged` 事件，使辅助技术刷新缓存。
- 不要把界面可视布局顺序误当层级。`Level` 描述语义结构，而不是像素 y 坐标。
- `Locale` 适合内容语言，不是应用主题语言或日期格式偏好。
- 接口不能孤立存在：主接口应报告 `AttributesInterface` 类型，并保持对象销毁时接口生命周期正确。

## 7. 知识点覆盖

- 可访问结构化元数据与基础语义的分工
- `QVariant` 的严格类型契约
- 标题层级、多语言内容与方向
- 平台无障碍属性桥接的可移植性边界
- 属性变更事件与缓存刷新
