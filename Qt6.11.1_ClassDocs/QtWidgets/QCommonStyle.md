# QCommonStyle

> Qt 6.11.1 · Qt Widgets · 来自 `QCommonStyle`

## 1. 先建立直觉

`QCommonStyle` 是 Qt 提供的通用 style 基类。它已经实现了许多控件绘制和尺寸逻辑，让你不用从纯 `QStyle` 的空白状态开始。

如果你要做一个完整自定义 style，`QCommonStyle` 是比直接继承 `QStyle` 更现实的起点；如果只是微调现有平台 style，通常用 `QProxyStyle` 更轻。

## 2. 类说明

`QCommonStyle` 继承自 `QStyle`，重写了大量绘制、尺寸、标准图标、布局间距等函数。它体现的是跨平台通用控件逻辑，而不是某个操作系统原生外观。

使用它时，你可以只覆盖自己关心的控件元素，其余交给基类处理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `drawPrimitive()` | 绘制基础 primitive 的通用实现。 |
| `drawControl()` | 绘制按钮、菜单项、标签等普通控件元素。 |
| `drawComplexControl()` | 绘制滑块、滚动条、组合框等复杂控件。 |
| `subElementRect()` | 返回通用子元素矩形。 |
| `subControlRect()` | 返回复杂控件子区域。 |
| `hitTestComplexControl()` | 命中复杂控件子控件。 |
| `pixelMetric()` | 返回通用像素尺寸。 |
| `styleHint()` | 返回通用行为提示。 |
| `sizeFromContents()` | 从内容尺寸计算控件尺寸。 |
| `standardIcon()` / `standardPixmap()` | 获取标准图标/位图。 |
| `layoutSpacing()` | 计算控件之间推荐间距。 |
| `polish()` / `unpolish()` | 应用/撤销 style 初始化。 |

## 4. 关键用法

```cpp
class CompactStyle : public QCommonStyle {
public:
    int pixelMetric(PixelMetric metric, const QStyleOption *opt,
                    const QWidget *widget) const override
    {
        if (metric == PM_DefaultFrameWidth)
            return 1;
        return QCommonStyle::pixelMetric(metric, opt, widget);
    }
};
```

只覆盖局部行为时，一定保留基类回退：

```cpp
return QCommonStyle::drawControl(element, option, painter, widget);
```

## 5. 使用场景

适合做跨平台统一风格、嵌入式设备主题、自定义控件库 style、需要完整控制绘制但又不想从零实现所有元素的场景。

桌面应用若只想跟随系统外观，不必直接碰它；使用默认 style 即可。

## 6. 常见坑与经验

完整 style 是系统工程。一个控件看起来对了，不代表 hover、disabled、RTL、高 DPI、键盘焦点、辅助功能都对了。

不要只实现绘制，不实现尺寸和 hit test。复杂控件的绘制区域、点击区域和布局尺寸必须匹配。

如果目标是“在当前系统 style 上微调”，优先继承 `QProxyStyle`，避免丢失平台细节。
