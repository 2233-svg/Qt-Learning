# Qt QAccessibleAttributesInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleAttributesInterface>`  
> 所属模块：`Qt6::Gui`  
> 自 Qt 6.8 引入  
> 定位：为整个可访问对象报告结构化 key-value 属性的纯虚接口

## 1. 它解决什么问题

`QAccessibleAttributesInterface` 为辅助技术提供对象级属性。它通过 `QAccessible::Attribute` 枚举作为键、`QVariant` 作为值，让某个对象能报告超出角色、文本、状态和几何之外的语义信息。

它与 `QAccessibleTextInterface::attributes()` 的职责不同：

- `QAccessibleAttributesInterface` 的属性适用于整个对象，对象可以是任意 role；
- `QAccessibleTextInterface::attributes()` 面向实现文本接口的对象，描述某个文本 offset 附近的文本属性；
- 两个接口可以同时实现，分别报告对象级信息和文本级信息。

它不是自由格式元数据字典。可用键和每个键应放入 `QVariant` 的具体类型由 `QAccessible::Attribute` 的文档定义；实现者不能随意用同一键返回不同类型。

## 2. 实际使用场景

当自定义控件有标准 role/state 无法完整表达的对象级无障碍信息时，可以实现本接口：

```cpp
QList<QAccessible::Attribute> MyAccessible::attributeKeys() const
{
    return { QAccessible::Level };
}

QVariant MyAccessible::attributeValue(QAccessible::Attribute key) const
{
    if (key == QAccessible::Level)
        return headingLevel();
    return {};
}
```

示例只说明调用模式。实际应只报告 Qt 枚举中有定义、且确实适用于该对象 role 的属性，并返回该键规定的 QVariant 类型。

## 3. 实现契约

### 3.1 `attributeKeys()` 与 `attributeValue()` 必须一致

`attributeKeys()` 列出的每个键，`attributeValue()` 都应能返回有效值。未列出的键应返回无效 `QVariant`。不要让 keys 报告一种能力而 value 又返回空值，除非对象状态在两次调用之间已经真正变化。

### 3.2 用无效 `QVariant` 表示“不支持”

对于不支持、未知或当前不适用的键，返回默认构造的无效 `QVariant`：

```cpp
return {};
```

不要用 `0`、空字符串或 `false` 代替“不支持”，因为这些可能是某些属性的有效值。调用方应使用 `QVariant::isValid()` 区分不存在与存在但取值为零/假。

### 3.3 类型必须遵守键定义

`QVariant` 只是承载容器，不会自动修正类型错误。返回值应严格符合对应 `QAccessible::Attribute` 所要求的类型；辅助技术往往无法从错误类型中恢复。

属性值应是读取快照，不应把临时指针、QObject 指针或依赖短生命周期数据塞入 QVariant。对象销毁或状态改变后，接口实现仍要避免访问已经失效的底层对象。

## 4. 所有权、缓存与通知

接口没有 QObject 基类，也不规定对象所有权。通常它由同一对象通过 `QAccessibleInterface::interface_cast(QAccessible::AttributesInterface)` 暴露。辅助技术得到的接口指针只是借用，不应删除。

属性查询可能频繁发生，因此实现应避免昂贵的 IO、网络请求或同步模型加载。若属性来自缓存，状态变化后要让缓存失效，并通过合适的无障碍事件报告变化；本接口本身没有专门的属性变更信号。

## 5. 逐项 API 说明

### `virtual ~QAccessibleAttributesInterface()`

虚析构函数，允许通过接口指针销毁派生对象。实际对象通常由 accessible interface 或其 owner 管理，调用方不能因为拿到接口指针就认定拥有它。

### `virtual QList<QAccessible::Attribute> attributeKeys() const = 0`

返回此对象当前支持的所有对象级属性键。列表可为空。

键应避免重复，并只包含 `attributeValue()` 可以返回有效且类型正确数据的条目。不要把文本 offset 特有属性放到这里；那类信息应通过 `QAccessibleTextInterface` 提供。

### `virtual QVariant attributeValue(QAccessible::Attribute key) const = 0`

返回指定键的属性值。若对象支持该键，返回类型必须符合该键在 `QAccessible::Attribute` 中的规定；不支持时返回无效 `QVariant`。

该函数是查询，不应修改对象、不应触发用户动作，也不应为了回答查询而执行阻塞操作。调用方不能把有效 QVariant 的具体内容当成跨 Qt 版本自由扩展的数据结构，应该按键的已定义类型解析。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `~QAccessibleAttributesInterface()` | 虚析构接口。 | 接口指针通常为借用，不代表调用方拥有对象。 |
| 发现 | `attributeKeys()` | 返回当前支持的对象级属性键。 | 可为空；每个键都应有有效、类型正确的 value。 |
| 查询 | `attributeValue(QAccessible::Attribute)` | 返回键对应的 QVariant 值。 | 不支持时返回无效 QVariant，不要用 `0`/`false` 代替。 |

### 一句话总结

`QAccessibleAttributesInterface` 是对象级无障碍属性的严格 key-value 契约：keys 说明支持什么，values 用规定类型的 `QVariant` 返回数据，不能回答的键必须明确返回无效 QVariant；它与文本 offset 属性接口互补而不重叠。
