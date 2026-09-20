# QPalette

> Qt 6.11.1 · Qt GUI · 来自 `QPalette`

## 1. 先建立直觉

`QPalette` 不是一组随便命名的颜色，而是 Qt Widgets 风格系统用来回答“这个控件在当前状态下应该用什么前景、背景、高亮、按钮、输入框颜色”的语义表。它同时按 **颜色角色** 和 **颜色组** 组织：角色说明颜色用在哪里，颜色组说明控件处于 active、inactive 还是 disabled。

写跨平台 widget 样式时，优先使用 palette 的角色色，而不是硬编码黑白灰。这样控件才更容易适配暗色模式、系统主题、高对比度设置和用户个性化 accent color。

## 2. 类说明

- 头文件：`#include <QPalette>`
- CMake：`Qt6::Gui`
- 类型性质：隐式共享值类型，可复制、可移动、可序列化
- 使用者：`QWidget`、`QStyle`、部分 Qt 绘制代码和控件样式
- 两个维度：`ColorRole` 表示用途，`ColorGroup` 表示状态组

`QPalette` 本身不保证某个样式一定严格使用每个角色。原生平台样式可能直接从系统主题取色；样式表也可能覆盖 palette。因此它是 Widgets 生态的颜色语义基础，但不是所有视觉结果的唯一来源。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `ColorRole` | 颜色用途，如 `Window`、`WindowText`、`Base`、`Text`、`Button`、`Highlight`。 |
| `ColorGroup` | 状态组：`Active`、`Inactive`、`Disabled`，`Normal` 是 `Active` 的别名。 |
| `QPalette()` | 创建未显式设置角色的调色板，作为 widget palette 时会与默认调色板解析。 |
| `QPalette(QColor/GlobalColor)` | 用按钮/窗口基色推导一套基础调色板。 |
| `brush(role)` / `color(role)` | 读取当前颜色组下某个角色的刷子或纯色。 |
| `brush(group, role)` / `color(group, role)` | 精确读取指定状态组和角色。 |
| `setBrush(role, brush)` / `setColor(role, color)` | 设置所有或当前相关组中的角色颜色。 |
| `setBrush(group, role, brush)` / `setColor(group, role, color)` | 只设置某个状态组的角色。 |
| `setColorGroup()` | 一次设置某个颜色组的核心角色。 |
| `currentColorGroup()` / `setCurrentColorGroup()` | 控制无 group 读取时使用哪一组。 |
| `isBrushSet(group, role)` | 判断某个组/角色是否被显式设置。 |
| `resolve(other)` | 将当前 palette 中显式设置的角色覆盖到 `other` 上，常用于继承式合成。 |
| `isEqual(cg1, cg2)` | 判断两个颜色组是否等价。 |
| `cacheKey()` | 获取缓存标识，适合内部缓存判断 palette 是否变化。 |
| `accent()` | Qt 6.6 起的强调色角色；未设置时通常退回到 `Highlight`。 |
| `operator QVariant()` | 便于放入 Qt 属性系统。 |

## 4. 角色速查

| 角色 | 典型用途 |
| --- | --- |
| `Window` / `WindowText` | 普通窗口背景与其上的文字。 |
| `Base` / `Text` | 输入框、列表、表格等内容区域背景与文字。 |
| `AlternateBase` | 交替行背景，例如表格斑马纹。 |
| `Button` / `ButtonText` | 按钮背景与按钮文字。 |
| `Light`、`Midlight`、`Mid`、`Dark`、`Shadow` | 传统 3D 边框、阴影和分隔效果。 |
| `Highlight` / `HighlightedText` | 选中项背景与选中文本。 |
| `Accent` | Qt 6.6 起的强调色，常对应系统个性化色。 |
| `ToolTipBase` / `ToolTipText` | 工具提示背景与文字。 |
| `PlaceholderText` | 输入框占位文本。 |
| `Link` / `LinkVisited` | 链接颜色；富文本中常用 CSS 覆盖更直接。 |
| `BrightText` | 在深色或警示背景上的高对比文字。 |
| `NoRole` | 表示无角色，通常用于占位或无效状态。 |

## 5. 关键用法

### 用语义色绘制自定义控件

```cpp
void Panel::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    const QPalette pal = palette();

    p.fillRect(rect(), pal.window());
    p.setPen(pal.color(QPalette::WindowText));
    p.drawText(rect(), Qt::AlignCenter, title);
}
```

这比写死白底黑字更稳：暗色主题下 `Window` 和 `WindowText` 会随系统或应用主题变化。

### 单独调整 disabled 颜色

```cpp
QPalette pal = widget->palette();
pal.setColor(QPalette::Disabled, QPalette::Text, QColor(130, 130, 130));
widget->setPalette(pal);
```

颜色组的意义在这里体现出来：同一个 `Text` 角色，正常和禁用状态可以不同。

### 使用 resolve 做局部覆盖

```cpp
QPalette override;
override.setColor(QPalette::Highlight, QColor("#2f80ed"));

const QPalette merged = override.resolve(qApp->palette());
```

`resolve()` 只把显式设置过的角色覆盖过去，适合“继承全局调色板，只改一两个角色”的场景。

## 6. 使用场景

- 自定义 QWidget 绘制时读取主题色。
- 应用级主题：`QApplication::setPalette()` 设置全局色彩基础。
- 控件局部强调：只调整某个 panel、输入框或按钮的角色色。
- 高对比度和暗色模式适配：使用角色语义避免硬编码颜色。
- 自定义 `QStyle`：根据角色和颜色组绘制控件状态。

## 7. 常见坑与经验

- **角色不是具体控件名。** `Base` 不只给输入框用，也可能用于列表、组合框下拉和视图背景。
- **当前颜色组会影响无 group 查询。** `color(QPalette::Text)` 取的是当前组，不一定是 active 组。
- **样式表可能覆盖 palette。** 如果控件设置了 CSS，实际颜色可能不再来自 palette。
- **原生样式未必使用所有角色。** 特别是 macOS、Windows 原生控件，平台主题可能有更高优先级。
- **不要只改一种状态。** 如果只改 active 的文字色，disabled 或 inactive 下可能对比度很差。
- **`Link` 不一定控制富文本链接。** 富文本链接样式常用 `QTextDocument::setDefaultStyleSheet()` 或 HTML/CSS 控制。
- **颜色对比要成对考虑。** 改 `Highlight` 时同时检查 `HighlightedText`；改 `Base` 时检查 `Text`。

## 8. 知识点覆盖

- 颜色角色与颜色组的二维模型
- Widgets 主题、系统主题、样式表和 palette 的关系
- 隐式共享值类型、缓存 key 与局部覆盖合成
- 暗色模式、高对比度和 disabled 状态适配
- 选中、高亮、链接、占位文本、工具提示等语义色
- 自定义绘制中避免硬编码颜色的实践
