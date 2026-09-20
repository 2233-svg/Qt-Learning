# QStylePainter

> Qt 6.11.1 · Qt Widgets · 来自 `QStylePainter`

## 1. 先建立直觉

`QStylePainter` 是 `QPainter` 的便利子类，专门用于在 widget 的 `paintEvent()` 中调用当前 `QStyle` 绘制控件元素。

它不提供新的绘制规则，只是把 painter、widget、style 的组合使用变得更顺手。

## 2. 类说明

`QStylePainter` 继承自 `QPainter`。构造时绑定 widget 后，可以直接调用 `drawPrimitive()`、`drawControl()`、`drawComplexControl()`，内部会使用 widget 的 style。

它适合自定义控件想“像系统控件一样画”的场景，尤其是控件主体交给 style，额外内容自己补画。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStylePainter()` | 创建未开始绘制的 style painter。 |
| `QStylePainter(QWidget *)` | 为指定 widget 开始绘制。 |
| `QStylePainter(QPaintDevice *, QWidget *)` | 在指定 paint device 上按 widget style 绘制。 |
| `begin(QWidget *)` | 开始为 widget 绘制。 |
| `begin(QPaintDevice *, QWidget *)` | 开始在设备上按 widget style 绘制。 |
| `drawPrimitive()` | 调用 style 绘制 primitive。 |
| `drawControl()` | 调用 style 绘制 control。 |
| `drawComplexControl()` | 调用 style 绘制 complex control。 |
| `drawItemText()` | 按 style 规则绘制文本。 |
| `drawItemPixmap()` | 按 style 规则绘制 pixmap。 |
| `style()` | 返回正在使用的 style。 |

## 4. 关键用法

```cpp
void MyButton::paintEvent(QPaintEvent *)
{
    QStyleOptionButton opt;
    opt.initFrom(this);
    opt.text = text();

    QStylePainter painter(this);
    painter.drawControl(QStyle::CE_PushButton, opt);
}
```

额外绘制内容：

```cpp
painter.drawControl(QStyle::CE_PushButtonBevel, opt);
painter.drawText(rect(), Qt::AlignCenter, label);
```

## 5. 使用场景

适合自定义 widget、复合控件、需要保留平台外观的轻度重绘、教学/示例中简化 style 调用。

如果完全自绘且不想依赖 style，普通 `QPainter` 就够；如果要完整控件外观一致，`QStylePainter` 很方便。

## 6. 常见坑与经验

仍然要正确初始化 `QStyleOption`。painter 再方便，也无法猜出控件状态。

不要在 paintEvent 外长期持有 painter。它和普通 `QPainter` 一样遵守绘制生命周期。

自绘控件要同时考虑 sizeHint、focus、hover、disabled。画出来只是第一步。
