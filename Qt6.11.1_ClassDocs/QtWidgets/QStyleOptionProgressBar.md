# QStyleOptionProgressBar

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionProgressBar`

## 1. 先建立直觉

`QStyleOptionProgressBar` 是进度条绘制参数包。它告诉 style 当前范围、进度值、显示文本、文字对齐、方向和是否倒置。

进度条看似简单，但平台 style 对忙碌状态、文本位置、RTL 和垂直方向的处理都可能不同。

## 2. 类说明

`QStyleOptionProgressBar` 继承自 `QStyleOption`。它主要用于 `QStyle::CE_ProgressBar` 相关绘制。

当 minimum 和 maximum 都为 0 时，进度条通常表示忙碌/未知进度状态，而不是具体百分比。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `minimum` / `maximum` | 进度范围。 |
| `progress` | 当前进度值。 |
| `text` | 显示文本。 |
| `textVisible` | 是否显示文本。 |
| `textAlignment` | 文本对齐方式。 |
| `orientation` | 水平或垂直进度条。 |
| `invertedAppearance` | 是否反向显示增长方向。 |
| `bottomToTop` | 垂直文本方向相关字段。 |
| `QStyle::CE_ProgressBar` | 绘制完整进度条。 |
| `QStyle::CE_ProgressBarGroove` | 绘制槽。 |
| `QStyle::CE_ProgressBarContents` | 绘制进度内容。 |
| `QStyle::CE_ProgressBarLabel` | 绘制文字标签。 |

## 4. 关键用法

```cpp
QStyleOptionProgressBar opt;
opt.initFrom(this);
opt.minimum = minimum();
opt.maximum = maximum();
opt.progress = value();
opt.text = text();
opt.textVisible = isTextVisible();
opt.textAlignment = Qt::AlignCenter;

QStylePainter p(this);
p.drawControl(QStyle::CE_ProgressBar, opt);
```

未知进度：

```cpp
opt.minimum = 0;
opt.maximum = 0;
```

## 5. 使用场景

适合自定义进度条、delegate 中绘制进度、任务列表状态、下载/构建/处理进度可视化。

普通业务使用 `QProgressBar` 即可，不需要手写 option。

## 6. 常见坑与经验

未知进度不要伪造百分比。用 0/0 范围更符合平台 style 对 busy indicator 的处理。

文本可见性和实际文本要同时设置。只填 `text` 不代表 style 一定会画。

垂直进度条、RTL、反向外观会改变增长方向，绘制时不要硬编码从左到右。
