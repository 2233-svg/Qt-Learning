# QStyleHintReturnMask

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleHintReturnMask`

## 1. 先建立直觉

`QStyleHintReturnMask` 是 `QStyleHintReturn` 的派生类，用来让 `QStyle::styleHint()` 返回一个 `QRegion`。这个 region 通常表示某种形状、遮罩或命中区域。

它服务 style 系统，不是图像处理里的 mask 工具。

## 2. 类说明

`QStyleHintReturnMask` 保存一个公开成员 `region`。调用方创建它并传给 `styleHint()`，style 如果支持对应 hint，就把区域写进去。

这种结构让 style hint 在 `int` 返回值之外携带更复杂的几何信息。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStyleHintReturnMask()` | 创建 mask 返回对象。 |
| `region` | 保存 style 返回的 `QRegion`。 |
| `QStyleHintReturn::type` | 标识这是 mask 类型返回。 |
| `QStyle::styleHint()` | 填充该对象的入口。 |

## 4. 关键用法

```cpp
QStyleHintReturnMask mask;
style()->styleHint(hint, option, widget, &mask);

if (!mask.region.isEmpty())
    applyMask(mask.region);
```

## 5. 使用场景

适合 style 实现和少量高级控件，需要从当前 style 获取非矩形区域或遮罩规则。

普通 widget 绘制和布局通常不需要直接使用它。

## 6. 常见坑与经验

`region` 是否有效取决于具体 hint 和 style 实现。不要假设所有 style 都会填充。

mask 坐标要结合 option/widget 语境理解。拿到 region 后不要脱离原控件几何乱用。

如果只是裁剪绘制区域，通常直接用 `QPainter::setClipRegion()`，不需要 style hint return。
