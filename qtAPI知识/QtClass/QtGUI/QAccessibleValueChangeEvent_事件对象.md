# QAccessibleValueChangeEvent：通知可访问对象的新数值

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleValueChangeEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QAccessibleEvent`

## 它解决什么问题

滑块、微调框、旋钮、滚动条和进度类控件的核心信息是当前数值。值变动后，辅助技术需要获知新值，才能朗读“音量 70%”或刷新其自动化状态。`QAccessibleValueChangeEvent` 用一个 `QVariant` 携带这个新值。

构造后事件类型固定为 `QAccessible::ValueChanged`。它只描述状态，不会调用控件的 setter，也不检查值是否在最小值与最大值之间。

## 典型用法

标准 Qt 数值控件已经会发送需要的通知。这个类主要服务于自定义控件，或自定义可访问性实现。

```cpp
#include <QAccessible>
#include <QAccessibleValueChangeEvent>

void VolumeDial::setVolume(int value)
{
    const int bounded = qBound(minimum(), value, maximum());
    if (m_value == bounded)
        return;

    m_value = bounded; // 先更新真实控件状态

    QAccessibleValueChangeEvent event(this, m_value);
    QAccessible::updateAccessibility(&event);
}
```

当对象实现 `QAccessibleValueInterface` 时，事件中的值应与 `currentValue()` 返回的值一致，类型也应尽量一致，例如都使用 `int` 或都使用 `double`。事件值与查询接口不一致会使辅助技术缓存出现冲突。

## 目标、生命周期和 `QVariant`

构造函数可面向 `QObject *` 或 `QAccessibleInterface *`。事件不拥有目标对象或接口，通常在栈上创建，并立即传给 `QAccessible::updateAccessibility()`。

`QVariant` 是按值保存的，调用者之后改变原始变量不会改写事件。它可容纳多种类型，但可访问数值接口通常使用 `int` 或 `double`。不要用显示文本，例如 `"70%"`，代替数值本身；名称、值格式化和单位应由对象的可访问性信息及平台后端处理。

## API 语义与边界

### 构造函数

`QAccessibleValueChangeEvent(QAccessibleInterface *iface, const QVariant &val)` 和对象版本创建一个携带新值的通知。

- `type()` 为 `QAccessible::ValueChanged`。
- `value()` 初始返回传入值的副本。
- 构造不会改变控件，也不会验证值范围或 `QVariant` 类型。

### `value() const`

返回事件中记录的新值，而不是实时调用对象的 `QAccessibleValueInterface::currentValue()`。所以应在控件已更新后才创建事件。

### `setValue(const QVariant &value)`

分发前改写事件载荷。它不调用控件 setter，不触发范围修正，也不自动重新分发事件。需要修改真实状态时应先调用控件自己的状态更新逻辑。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QAccessibleValueChangeEvent(QAccessibleInterface *iface, const QVariant &val)` | 为可访问性接口创建新值通知。 | `iface` 不转移所有权，分发期间必须有效。 |
| `QAccessibleValueChangeEvent(QObject *object, const QVariant &value)` | 为对象创建新值通知。 | 先更新对象，再使 `value` 与实际新值一致。 |
| `QVariant value() const` | 取得事件携带的新值。 | 是快照，不会重新查询控件。 |
| `void setValue(const QVariant &value)` | 改写事件的新值载荷。 | 不会修改真实控件，也不校验值范围。 |
| 继承的 `type()` | 查询事件种类。 | 本类构造后为 `QAccessible::ValueChanged`。 |
| 配套调用 `QAccessible::updateAccessibility(QAccessibleEvent *)` | 把通知交给可访问性框架。 | 局部事件应在同步分发完成前保持存活。 |
