# QAccessibleValueChangeEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleValueChangeEvent`

## 1. 先建立直觉

`QAccessibleValueChangeEvent` 通知辅助技术：一个有“当前值”的对象发生了值变化。它适合滑块、滚动条、进度条、旋钮、评分控件、音量控制和自定义数值仪表。

值变化事件应与 `QAccessibleValueInterface` 配套：事件告诉外界“值变了”，值接口让外界继续查询当前值、最小值、最大值和步进信息。

## 2. 类说明

- 头文件：`#include <QAccessibleValueChangeEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleEvent`
- 值类型：通过 `QVariant` 携带，可是整数、浮点、字符串或控件定义的其他合适类型。

事件值应是变化后的新值，而不是增量。例如滑块从 30 调到 40，事件值应为 40，不是 +10。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleValueChangeEvent(object, value)` | 为 QObject 构造值变化事件。 |
| `QAccessibleValueChangeEvent(iface, value)` | 为可访问接口构造值变化事件。 |
| `value()` | 返回事件携带的新值。 |
| `setValue(value)` | 修改事件携带的新值。 |
| `QAccessible::updateAccessibility()` | 将变化通知辅助技术。 |

## 4. 关键用法

```cpp
void VolumeKnob::setVolume(int value)
{
    value = qBound(0, value, 100);
    if (m_volume == value)
        return;

    m_volume = value;
    update();

    QAccessibleValueChangeEvent event(this, m_volume);
    QAccessible::updateAccessibility(&event);
}
```

事件应在内部值已经改变后发送。这样辅助技术接到事件后通过 `valueInterface()->currentValue()` 查询时，能读到同一个新值。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 滑块、旋钮、滚动条 | 发送新数值，并实现 ValueInterface。 |
| 进度条 | 进度变化可发送事件，但高频进度应节流。 |
| 星级评分、缩放比例 | 用清晰的 QVariant 类型表达当前值。 |
| 复选框状态变化 | 通常是 StateChange，不是 ValueChange。 |
| 文本内容变化 | 使用文本事件或 Name/Value 文本属性变化，不混用数值事件。 |

## 6. 常见坑与经验

- `QVariant` 类型要稳定。同一个控件不要有时发 `int`、有时发 `"40%"` 字符串，否则平台端难以解释。
- 不要为动画每一帧发送值变化；只在用户可感知或语义状态改变时通知。
- 最小值、最大值和步进不是这个事件的职责，应通过 `QAccessibleValueInterface` 暴露。
- 若值变化同时改变 `disabled`、`busy` 或 `readOnly` 等状态，需要额外发送状态变化事件。
- 密码强度、音量、亮度等值应选择用户能理解的单位，并在文本说明中补足上下文。

## 7. 知识点覆盖

- 值变化事件和数值接口的配合
- 新值、增量、范围和步进的职责分离
- `QVariant` 类型稳定性
- 高频值变化的通知节流
- 数值语义与状态/文本语义的边界
