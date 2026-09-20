# QTextLength 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextLength>`  
> 所属模块：`Qt6::Gui`  
> 类型：轻量值类型

## 1. 它解决什么问题

`QTextLength` 把“长度”表示成三种不同语义：固定值、相对可用空间的百分比，或由布局自行分配的可变长度。它主要出现在 `QTextFrameFormat` 的宽高、`QTextImageFormat` 的最大宽度，以及 `QTextTableFormat` 的列宽约束中。

它解决的是富文本文档中“不能只用一个 `qreal` 表示长度”的问题。例如表格列宽既可能固定为 80，也可能是可用宽度的 25%，还可能要求布局自动分配。

## 2. 三种类型和计算方式

| 类型 | `rawValue()` 含义 | `value(maximumLength)` 结果 |
| --- | --- | --- |
| `VariableLength` | 通常为 `0` | 返回 `maximumLength`。 |
| `FixedLength` | 固定逻辑长度 | 忽略 maximum，返回原始值。 |
| `PercentageLength` | 百分比数值，例如 `25` | 返回 `rawValue * maximumLength / 100`。 |

默认构造的 `QTextLength` 是 `VariableLength`，原始值为 `0`。它表示“由布局决定”，不是固定为零宽或零高。

```cpp
QTextLength fixed(QTextLength::FixedLength, 80);
QTextLength quarter(QTextLength::PercentageLength, 25);

Q_ASSERT(fixed.value(400) == 80);
Q_ASSERT(quarter.value(400) == 100);
```

`maximumLength` 的单位由使用它的布局属性决定，通常是逻辑排版单位；它不是自动转换后的物理像素。百分比的最终值还可能被最小尺寸、内容或外层布局约束进一步限制。

## 3. 生命周期和线程

`QTextLength` 是无所有权的可复制值类型。它可以在任何线程中独立创建、比较和计算。把它写入 `QTextDocument`、`QTextFrameFormat` 或表格格式时，则要遵守目标文档的线程规则。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextLength()` | 创建可变长度。 | `type()` 为 `VariableLength`，`rawValue()` 为 `0`；不代表零长度。 |
| `QTextLength(Type type, qreal value)` | 用类型和原始值创建长度。 | 对百分比传 `25` 表示 25%，不是 `0.25`。 |
| `Type::VariableLength` | 把可用最大长度交由布局使用。 | `value(maximum)` 返回 maximum。 |
| `Type::FixedLength` | 表示固定逻辑长度。 | `value(maximum)` 忽略 maximum。 |
| `Type::PercentageLength` | 表示相对最大长度的百分比。 | `value(maximum)` 做百分比计算；最终布局仍可受其他约束影响。 |
| `type()` | 返回长度语义类型。 | 先看类型再解释 `rawValue()`。 |
| `rawValue()` | 返回未计算的固定数值或百分比。 | 对可变长度通常是 `0`，但不等同于 `value()` 为 0。 |
| `value(qreal maximumLength)` | 按类型计算实际请求值。 | maximum 的单位和合法范围由调用布局决定。 |
| `operator==` / `operator!=` | 比较类型和数值。 | 浮点值使用 Qt 的模糊比较语义。 |
| `operator QVariant()` | 包装为 `QVariant`。 | 用于通用属性或元数据传递，不计算长度。 |

## 5. 记忆重点

`QTextLength` 的核心不是数值，而是数值的解释方式。固定、百分比和可变长度的 `rawValue()` 都可能看起来简单，但必须通过 `type()` 和当前可用长度解释。
