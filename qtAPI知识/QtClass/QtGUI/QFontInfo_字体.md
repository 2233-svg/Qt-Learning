# QFontInfo

`QFontInfo` 是一次字体匹配结果的只读快照。它回答“Qt 最终找到了什么字体”，而 `QFont` 回答“代码请求了什么字体”。

- 头文件：`#include <QFontInfo>`
- 模块：`Qt6::Gui`
- 类型特性：隐式共享、可复制值类型
- 关键边界：构造后不会因原始 `QFont`、控件或 `QPainter` 字体改变而更新

## 它解决的问题

字体请求常常无法被精确满足：指定家族没安装、某种 weight 没有独立字形、位图字体只提供固定点大小，或平台替换了别名。`QFont` 的 getter 仍返回请求值，`QFontInfo` 才暴露匹配后的家族、样式、大小和属性。

```cpp
QFont requested(u"Courier"_s, 25);
QFontInfo actual(requested);

qDebug() << requested.family() << requested.pointSize();
qDebug() << actual.family() << actual.pointSize();
```

例如机器只有不可缩放的 24pt Courier 时，请求对象仍为 25pt，而 `QFontInfo::pointSize()` 可报告实际匹配的 24pt。

## 实际场景

**诊断跨平台字体问题。** 将 `family()`、`styleName()`、`pointSizeF()`、`exactMatch()` 记入日志，快速判断问题来自家族缺失还是尺寸/样式回退。

**根据实际能力调整 UI。** `fixedPitch()`、`italic()`、`weight()` 可帮助代码编辑器或字体预览标出真正匹配的字体特征。

**读取可变字体能力。** Qt 6.9 起，`variableAxes()` 返回实际匹配字体定义的 `QFontVariableAxis` 列表；据此限制 `QFont::setVariableAxis()` 的标签和值。

## 使用规则

在所有 `QFont` 属性设完后再构造 `QFontInfo`。需要观察控件当前字体时，以 `widget->font()` 创建；需要反映 `QPainter` 的绘制设备和字体时，优先从 `painter.font()` 以及相同设备构造度量/绘制流程。

`exactMatch()` 为真表示窗口系统中存在精确匹配设置的字体，不代表它覆盖待显示文本的每一个 Unicode 字符。缺字仍可能走字体回退；要验证某字符的直接覆盖，应使用对应 `QFontMetrics(F)::inFont()` 并理解它同样不是整段复杂文本 shaping 的完整模拟。

## API 速查表

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QFontInfo(const QFont &font)` | 根据一个字体请求进行匹配并创建结果快照。 | 在所有请求属性设置后再构造。 |
| `QFontInfo(const QFontInfo &)`、`operator=`、`swap()` | 复制、赋值或交换快照。 | 都不会重新触发字体匹配。 |
| `family()` | 返回实际匹配的字体家族。 | 与 `QFont::family()` 的请求名可能不同。 |
| `styleName()` | 返回实际匹配样式名。 | 可用于 UI 说明和诊断；跨平台命名不同。 |
| `pixelSize()` | 返回匹配字体的像素大小。 | 与设备 DPI 相关。 |
| `pointSize()` | 返回匹配字体的整数点大小。 | 不可缩放字体可能不同于请求大小。 |
| `pointSizeF()` | 返回匹配字体的浮点点大小。 | 用于避免整数截断造成的诊断误差。 |
| `italic()` | 返回实际匹配字体是否为斜体。 | 请求斜体可能被回退或模拟。 |
| `style()` | 返回实际使用的 `QFont::Style`。 | 与 `styleName()` 一起看更可靠。 |
| `weight()` | 返回实际匹配的字重。 | 采用 `QFont::Weight` 标尺。 |
| `bold()` | 判断实际字重是否大于 `QFont::Normal`。 | 这是快捷判断，不区分 DemiBold / Bold / Black。 |
| `underline()` / `overline()` / `strikeOut()` | 返回匹配字体的装饰设置。 | 装饰更接近文本绘制属性，不要据此推断物理字体文件能力。 |
| `fixedPitch()` | 返回实际字体是否等宽。 | 代码编辑器应以此而非家族名决定等宽标识。 |
| `styleHint()` | 返回实际匹配的样式提示。 | 提示是匹配信息，不是文字类别的强保证。 |
| `variableAxes()` | 返回实际字体提供的变量轴。 | Qt 6.9；用它的标签和值域限制轴选择 UI。 |
| `exactMatch()` | 判断是否存在精确匹配请求的窗口系统字体。 | 不等于完整 Unicode 覆盖或跨平台像素一致。 |

## 易错点

1. 修改 `QFont` 后复用旧 `QFontInfo`。它是快照，需要重新构造。
2. 用 `exactMatch()` 断言“不会缺字”。它只说明匹配属性，不说明每个字形覆盖。
3. 用请求字体的 `pointSize()` 为像素级布局做最终依据。布局应以对应输出设备的 `QFontMetricsF` 为准。
4. 在 Qt 6.8 或更早版本调用 `variableAxes()`。该 API 自 Qt 6.9 起可用。
