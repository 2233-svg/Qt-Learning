# QStyle

> Qt 6.11.1 · Qt Widgets · 来自 `QStyle`

## 1. 先建立直觉

`QStyle` 是 Qt Widgets 的外观策略中心。按钮怎么画、滚动条箭头有多大、复选框指示器放哪、控件之间该留多少像素，很多规则都由 style 决定。

它不是样式表，也不是调色板。`QPalette` 提供颜色角色，style 决定控件结构、绘制、尺寸、命中区域和平台习惯；样式表则是另一层覆盖机制。

## 2. 类说明

`QStyle` 继承自 `QObject`，但通常通过 `QApplication::style()` 使用。自定义外观可以继承 `QProxyStyle` 包装现有 style，也可以继承 `QCommonStyle` / `QStyle` 做完整实现。

绝大多数自定义 widget 不应该硬编码控件细节，而应构造 `QStyleOption`，调用 `style()->drawControl()`、`drawPrimitive()`、`subControlRect()`、`pixelMetric()` 等，让当前平台 style 参与绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `drawPrimitive()` | 绘制基础元素，如面板、焦点框、指示器。 |
| `drawControl()` | 绘制完整控件部件，如按钮、菜单项、标签页。 |
| `drawComplexControl()` | 绘制由多个子控件组成的控件，如滚动条、滑块、组合框。 |
| `subElementRect()` | 查询普通控件内部元素区域。 |
| `subControlRect()` | 查询复杂控件某个子控件区域。 |
| `hitTestComplexControl()` | 判断坐标命中复杂控件的哪个子控件。 |
| `pixelMetric()` | 查询平台相关像素尺寸。 |
| `styleHint()` | 查询行为/视觉提示。 |
| `sizeFromContents()` | 根据内容尺寸推导控件整体尺寸。 |
| `standardPixmap()` / `standardIcon()` | 获取标准图标/位图。 |
| `standardPalette()` | 获取 style 默认调色板。 |
| `polish()` / `unpolish()` | style 应用/撤销到 app 或 widget 时做初始化/清理。 |
| `proxy()` | 返回当前 style 代理，便于 style 链正确转发。 |

## 4. 关键用法

自定义按钮式绘制：

```cpp
QStyleOptionButton opt;
opt.initFrom(this);
opt.text = text();
opt.state |= isDown() ? QStyle::State_Sunken : QStyle::State_Raised;

QPainter p(this);
style()->drawControl(QStyle::CE_PushButton, &opt, &p, this);
```

查询平台尺寸：

```cpp
const int margin = style()->pixelMetric(QStyle::PM_DefaultFrameWidth, nullptr, this);
```

## 5. 使用场景

适合自定义控件绘制、平台一致性适配、控件尺寸计算、命中测试、代理 style 修改局部行为、插件式主题。

如果只是改颜色和少量边距，样式表可能更直接；如果要尊重平台控件结构，`QStyle` 是更底层也更准确的工具。

## 6. 常见坑与经验

不要在 paintEvent 里凭感觉画系统控件。用 `QStyleOption` 加 style 绘制，才能跟随平台、主题、高 DPI 和禁用/悬停/焦点状态。

自定义 style 工作量很大。多数产品只需要 `QProxyStyle` 改几个 metric 或 hint。

样式表会改变 style 行为。调试外观时要确认问题来自 style、palette、stylesheet 还是控件自身绘制。
