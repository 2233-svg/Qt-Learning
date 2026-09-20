# QAccessibleValueInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleValueInterface`

## 1. 先建立直觉

`QAccessibleValueInterface` 描述一个对象的数值范围、当前值和最小步进。它让辅助技术不只知道“这是滑块”，还知道它现在是 40、范围是 0 到 100、合理的增减步长是 1。

它适用于滑块、滚动条、进度条、旋钮、缩放控件、评分控件等“有值”的控件。复选框的勾选状态、按钮的按下状态、文本编辑器的内容变化通常不属于这个接口。

## 2. 类说明

- 头文件：`#include <QAccessibleValueInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：可访问子接口；通过 `QAccessibleInterface::valueInterface()` 获取。
- 协作事件：值改变后通常发送 `QAccessibleValueChangeEvent`。

所有返回值使用 `QVariant`，但同一个控件的类型应保持稳定。例如音量滑块始终返回 `int`，缩放比例始终返回 `double`，不要在数值和带单位字符串之间来回切换。

## 3. API 速查

| API | 用途 |
|---|---|
| `currentValue()` | 返回当前值。 |
| `setCurrentValue(value)` | 请求把控件设为指定值。 |
| `minimumValue()` | 返回可接受的最小值。 |
| `maximumValue()` | 返回可接受的最大值。 |
| `minimumStepSize()` | 返回合理的最小变化步长。 |

## 4. 关键用法

```cpp
QVariant AccessibleVolume::currentValue() const
{
    return volume()->value();
}

void AccessibleVolume::setCurrentValue(const QVariant &value)
{
    bool ok = false;
    const int v = value.toInt(&ok);
    if (!ok)
        return;

    volume()->setValue(qBound(0, v, 100));
}
```

`setCurrentValue()` 应走真实控件的设置路径，让范围限制、重绘、信号和无障碍事件都保持一致。超出范围或类型无法转换时，应安全拒绝，而不是崩溃或产生未定义状态。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 滑块/旋钮 | 返回当前、最小、最大和步进；同时提供增减动作。 |
| 进度条 | 当前值可读，`setCurrentValue()` 可为空操作；仍提供范围和步进。 |
| 滚动条 | 当前滚动位置、范围和页步进要符合真实滚动模型。 |
| 星级评分 | 可用整数或浮点表达评分，步进反映半星/整星。 |
| 复选框/开关 | 用 State 和 ActionInterface，不用 ValueInterface。 |

## 6. 常见坑与经验

- `minimumStepSize()` 不代表当前值，也不代表页面步长。它是辅助技术调整值时可采用的合理最小增量。
- 只读控件也可以提供值接口；区别是 `setCurrentValue()` 不改变值。
- 值变化后，`currentValue()` 必须立即返回新值，并发送 `QAccessibleValueChangeEvent`。
- `QVariant` 的单位要通过控件文本、Name/Description 或平台约定补足；不要把显示字符串当机器可调数值。
- 浮点值比较要考虑容差，避免因微小舍入误差反复发送值变化事件。

## 7. 知识点覆盖

- 数值控件的当前值、范围和步进
- `QVariant` 类型稳定性与单位表达
- 可读值与可写值的区别
- 值接口、动作接口和值变化事件协作
- 范围校验、只读控件和高频通知控制
