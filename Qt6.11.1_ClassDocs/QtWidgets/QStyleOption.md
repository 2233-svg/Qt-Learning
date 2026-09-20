# QStyleOption

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOption`

## 1. 先建立直觉

`QStyleOption` 是传给 `QStyle` 的绘制参数包。控件把“我现在的矩形、状态、方向、调色板、字体信息”等放进 option，style 再根据这些信息画出正确外观。

它让绘制函数不必依赖具体控件类，也让同一套 style 能绘制按钮、菜单、滑块、标题栏等不同元素。

## 2. 类说明

`QStyleOption` 是基类，派生类针对具体控件补充字段，例如 `QStyleOptionButton`、`QStyleOptionSlider`、`QStyleOptionViewItem`。

自定义 widget 绘制时，常先创建合适的 option，调用 `initFrom(widget)` 初始化通用状态，再填入控件特有字段。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `initFrom(const QWidget *)` | 从 widget 初始化通用状态、方向、矩形、调色板等。 |
| `rect` | 当前绘制区域。 |
| `state` | 控件状态集合，如 enabled、hover、pressed、focus。 |
| `direction` | 布局方向，影响 RTL 绘制。 |
| `palette` | 当前调色板。 |
| `fontMetrics` | 当前字体指标。 |
| `styleObject` | 和 style 相关的对象指针。 |
| `type` / `version` | option 类型和版本，用于安全转换。 |
| `qstyleoption_cast<T>()` | 安全地把基类 option 转成派生 option。 |

## 4. 关键用法

```cpp
QStyleOption opt;
opt.initFrom(this);

QPainter painter(this);
style()->drawPrimitive(QStyle::PE_Widget, &opt, &painter, this);
```

派生 option：

```cpp
QStyleOptionButton opt;
opt.initFrom(this);
opt.text = text;
style()->drawControl(QStyle::CE_PushButton, &opt, &painter, this);
```

## 5. 使用场景

适合自定义 widget 绘制、实现 style、delegate 绘制、复用平台控件外观。

如果完全自绘，不调用 `QStyle`，也可以不用 option；但那会失去平台一致性。

## 6. 常见坑与经验

不要忘记 `initFrom()`。否则 disabled、focus、RTL、palette 等状态很容易不完整。

option 是临时值对象，不要长期保存。每次绘制时按当前 widget 状态重新构造更可靠。

派生 option 要和绘制元素匹配。用 button option 去画 slider，style 无法得到正确字段。
