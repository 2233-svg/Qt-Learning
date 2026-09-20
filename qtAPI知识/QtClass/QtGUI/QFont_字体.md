# QFont

`QFont` 是 Qt 的“字体请求”值类型，而不是某个确定的字体文件或已经完成的字形布局。它让代码描述希望使用的家族、字号、粗细、斜体、间距、特性和可变字体轴；Qt 再结合当前平台、输出设备与可用字体选择实际字体。

- 头文件：`#include <QFont>`
- 模块：`Qt6::Gui`
- 适用：Qt 6；OpenType 特性和可变字体 API 自 Qt 6.7 起提供
- 前提：使用字体前必须已有 `QGuiApplication`
- 类型特性：隐式共享的可复制值类型；修改副本会按需分离，不管理 `QObject` 生命周期

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(app PRIVATE Qt6::Gui)
```

## 它解决的问题

界面代码不能假设“指定了某个字体名称，就一定会用这个字体”。不同系统安装的字体、字体别名、语言脚本覆盖、DPI 和输出设备都不同。`QFont` 将这些需求作为查询条件交给字体匹配器：先按 `families()` 的优先顺序查找，再挑选支持目标书写系统和字形的最接近候选；找不到单个字形时，默认还会进行逐字形回退。

因此应区分三件事：

| 需要的问题 | 应使用的类型 |
| --- | --- |
| 表达“我希望怎样画文字” | `QFont` |
| 确认“最终匹配到了什么” | `QFontInfo` |
| 测量字符串的推进宽度、墨迹边界、行高 | 优先 `QFontMetricsF` |
| 绑定一个明确的物理字体文件、读取字形 | `QRawFont` |

## 实际场景

**应用和控件的默认字体。** 使用 `QGuiApplication::setFont()` 设置应用默认值，或把局部 `QFont` 传给 `QWidget::setFont()`、`QPainter::setFont()`、`QTextCharFormat::setFont()`。局部对象只影响相应目标，并不会改写全局默认字体。

**跨平台 UI。** 首选点大小和多个候选家族，不把像素字号或单一 Windows/macOS 字体名写死。

```cpp
QFont codeFont;
codeFont.setFamilies({u"JetBrains Mono"_s, u"Consolas"_s, u"Monospace"_s});
codeFont.setPointSizeF(10.5);
codeFont.setStyleHint(QFont::Monospace);
editor->setFont(codeFont);
```

**排查字体不一致。** 用户机器上缺少请求家族、某个样式不可用或不可缩放时，`QFont` 的 getter 仍返回“请求值”。构造并检查 `QFontInfo` 才能得知实际家族、大小和样式。

**排版与高级 OpenType 控制。** `setFeature()` 可按四字节标签启用分数字形、连字或样式替代；`setVariableAxis()` 可对可变字体直接指定 `wght`、`wdth`、`opsz` 等轴的连续值。

## 从请求到渲染

未显式设置的属性通常不参与字体匹配，Qt 会偏好默认值。设置了家族却没有设置字号、粗细或固定宽度要求，不等于这些属性被锁定。一般流程如下：

1. 用 `setFamilies()` 给出优先级，或用 `setFamily()` 给出单个首选。
2. 设置必要的大小、权重、倾斜和策略。
3. 将字体交给控件、绘制器或文本格式。
4. 需要确认实际结果时，在设置完成后创建 `QFontInfo`；需要布局时，为相同输出设备创建 `QFontMetricsF`。

`QFontInfo` 和 `QFontMetrics(F)` 都是快照。之后即使修改了原始 `QFont` 或 `QPainter` 的字体，旧快照也不会刷新。

## 大小、设备与回退边界

- `setPointSize()` / `setPointSizeF()` 是设备无关的常用选择，值必须大于零；浮点精度不保证能在所有平台完整实现。
- `setPixelSize()` 使请求依赖设备像素密度，最大值为无符号 16 位整数范围。它适合像素对齐资源，不适合希望在屏幕和打印机上保持物理尺寸的正文。
- 点大小与像素大小二选一设置；查询另一种大小时常会得到 `-1`。
- `exactMatch()` 为真只表示窗口系统能提供完全匹配的字体设置，不代表每个字符都存在；缺字仍可能触发回退。
- `NoFontMerging` 会关闭缺字回退，缺失字形会显示缺字符方框。它通常只适用于需要严格验证字体覆盖的工具。

## 常用属性语义

| 组 | 要点 |
| --- | --- |
| 家族 | `families()` 是请求列表，第一项也是 `family()`；家族名不区分大小写，可附带 `Family [Foundry]`。 |
| 粗细与样式 | `setBold(true)` 实际等价于 `setWeight(Bold)`；想要 Medium、DemiBold 等应直接用 `setWeight()`。`setItalic()` 将样式设为 `StyleItalic`。 |
| 样式名 | `setStyleName()` 后，权重和 `Style` 对匹配通常会被忽略；平台可能事后模拟效果。不要混用“按样式名匹配”和“按权重/斜体匹配”。 |
| 策略 | `StyleHint` 是“找不到家族时优先找哪一类”的提示；`StyleStrategy` 是匹配/渲染偏好，平台不保证完全支持。X11 不支持样式提示。 |
| 间距 | `PercentageSpacing` 按字宽百分比调整，`AbsoluteSpacing` 按像素调整。字距会影响可选连字；词间距只调词之间的空白。 |
| 变形 | `setStretch(1..4000)` 改变字宽，`100` 为正常宽度，`AnyStretch` 表示不施加变形；位图字体忽略此设置。 |
| 装饰线 | 下划线、上划线、删除线是绘制请求，不保证物理字体本身定义了同样的装饰。 |

## OpenType 特性与可变字体

两者都用 `QFont::Tag` 表示四个 Latin-1 字节的标签，例如 `"kern"`、`"frac"`、`"wght"`。

```cpp
QFont font(u"Inter Variable"_s);
font.setFeature("tnum", 1);        // 请求等宽数字
font.setVariableAxis("wght", 625); // 仅在该字体定义了该轴时有意义
```

`setFeature(tag, value)` 直接影响 shaping：多数特性以 `0` / 非零代表关闭/启用，但例如 `"salt"` 可以把值解释为替代字形索引。显式设置 `"kern"` 会覆盖 `setKerning()` 的默认控制；设置字距时，某些书写系统的可选连字默认会关闭。使用 `unsetFeature()` 恢复 Qt 的默认逻辑，而不是把值设为零；后者是明确禁用。

变量轴值应先通过匹配字体的 `QFontInfo::variableAxes()` 查询轴和 `[minimumValue(), maximumValue()]` 范围。对不存在的轴、超出范围的值或不支持可变字体的后端不能作出可移植的视觉承诺；Windows 可选 GDI 后端不支持变量轴。

## 字体替换表

`insertSubstitution()` 和 `insertSubstitutions()` 配置进程级替换关系，供家族匹配前使用；`substitute()` 返回首个替代名，若未配置则原样返回，`substitutes()` 则在未配置时返回空列表。更改替换表不会自动改变既有的 `QFont` 对象，应销毁并重新创建依赖它们的字体对象。

不要用替换表代替“多个候选家族”：前者是全局规则，后者是单个字体请求的显式优先级。

## API 速查表

### 构造、复制与转换

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `QFont()` | 创建默认字体请求。 | 实际默认字体由应用和平台决定。 |
| `QFont(family, pointSize, weight, italic)` | 以单个家族及常用样式创建请求。 | `pointSize` / `weight` 为 `-1` 时未显式设置。 |
| `QFont(families, pointSize, weight, italic)` | 以有序候选家族列表创建请求。 | 列表第一项为主家族；这是跨平台回退的常用入口。 |
| `QFont(font, paintDevice)` | 以指定绘制设备的字体为基础创建副本。 | 用于设备相关匹配；设备对象必须在构造时有效。 |
| `QFont(const QFont &)`、`operator=`、移动赋值、`swap()` | 复制、赋值或常数时间交换字体请求。 | 值类型，修改副本不会改原对象。 |
| `operator QVariant()` | 转为可保存于 `QVariant` 的字体值。 | 适合属性/模型数据，不表示可跨平台复现同一物理字体。 |
| `isCopyOf(other)` | 判断是否仍共享同一内部数据副本。 | 不是字体视觉相等判断。 |
| `operator==` / `!=` / `<`、`qHash()` | 比较、排序或作为哈希键。 | 比较的是请求状态，不是最终渲染出来的字形。 |
| `toString()` / `fromString(text)` | 以 Qt 字体描述文本序列化或恢复请求。 | `fromString()` 返回是否成功；格式用于 Qt 兼容用途，不应当作长期公开文件格式。 |
| `QDataStream <<` / `>>` | 流式读写 `QFont`。 | 设置合适的 `QDataStream` 版本以控制持久化兼容性。 |

### 家族、大小与基础外观

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `family()` / `setFamily(name)` | 读取或设置第一个请求家族。 | 返回的是请求名；实际家族看 `QFontInfo::family()`。 |
| `families()` / `setFamilies(list)` | 读取或设置完整候选列表。 | 未设置时 getter 返回空列表；可写 `Family [Foundry]`。 |
| `defaultFamily()` | 返回匹配器为此请求选择的默认家族。 | 仍不是“已实际绘制的每个回退字形”列表。 |
| `pointSize()` / `setPointSize(int)` | 读取/设置整数点大小。 | 设置值必须大于零；像素大小模式下常为 `-1`。 |
| `pointSizeF()` / `setPointSizeF(qreal)` | 读取/设置浮点点大小。 | 平台可能量化精度。 |
| `pixelSize()` / `setPixelSize(int)` | 读取/设置像素大小。 | 设备相关；最大 65535；点大小模式下常为 `-1`。 |
| `weight()` / `setWeight(Weight)` | 读取/设置 100 至 900 标尺上的字重。 | 推荐精确使用此 API。 |
| `bold()` / `setBold(bool)` | 便捷判断/设置粗体。 | `true` 设为 `Bold`，`false` 设为 `Normal`，会覆盖原来的细粒度字重。 |
| `style()` / `setStyle(Style)` | 读取/设置正常、斜体、倾斜。 | 字体可能没有相应 face，平台可能模拟。 |
| `italic()` / `setItalic(bool)` | 便捷判断/设置斜体。 | `true` 会设为 `StyleItalic`；不是 `StyleOblique`。 |
| `styleName()` / `setStyleName(name)` | 读取/指定字体内部样式名。 | 设置后 `weight` 和 `style` 通常不参与匹配；慎与它们混用。 |
| `fixedPitch()` / `setFixedPitch(bool)` | 请求等宽或非等宽字体。 | 是匹配属性，不是对结果的绝对保证。 |
| `underline()` / `setUnderline(bool)` | 读取/请求下划线。 | 与 `QFontInfo` 的实际样式信息不是同一概念。 |
| `overline()` / `setOverline(bool)` | 读取/请求上划线。 | 常用于文本格式，不是字体选择核心条件。 |
| `strikeOut()` / `setStrikeOut(bool)` | 读取/请求删除线。 | 同上。 |

### 匹配提示、间距与修饰

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `styleHint()` / `setStyleHint(hint, strategy)` | 获取/设置通用字体类别提示及策略。 | `AnyStyle` / `PreferDefault` 为默认；提示不强制命中。 |
| `styleStrategy()` / `setStyleStrategy(strategy)` | 获取/设置匹配与抗锯齿、回退策略。 | 多数标志只是偏好，平台支持不同。 |
| `hintingPreference()` / `setHintingPreference(pref)` | 获取/设置字形 hinting 偏好。 | 全 hinting 会使度量随设备像素密度改变；不支持的平台会降级。 |
| `stretch()` / `setStretch(factor)` | 读取/设置横向拉伸因子。 | 范围 1..4000；`AnyStretch` 表示不施加变换；位图字体忽略。 |
| `kerning()` / `setKerning(bool)` | 读取/控制 kerning。 | 可被显式 `"kern"` OpenType 特性覆盖。 |
| `letterSpacing()` / `letterSpacingType()` / `setLetterSpacing(type, value)` | 获取/设置字符间距。 | 百分比相对字宽，绝对值为像素；可能影响连字。 |
| `wordSpacing()` / `setWordSpacing(value)` | 获取/设置词间额外间距。 | 单位为像素；负值会收紧词间空白。 |
| `capitalization()` / `setCapitalization(mode)` | 获取/设置大小写变换。 | `AllUppercase` 等会影响文本 shaping/绘制，不会修改原字符串。 |

### OpenType 特性和变量轴（Qt 6.7 起）

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `setFeature(tag, value)` | 为 shaping 指定 OpenType 特性值。 | `0` 常表示禁用但并非总是；标签与值语义由字体定义。 |
| `unsetFeature(tag)` | 移除某项显式特性。 | 恢复 Qt 的默认特性规则。 |
| `isFeatureSet(tag)` / `featureValue(tag)` | 查询是否显式设置及其值。 | 未设置时 `featureValue()` 返回 `0`，因此必须先看 `isFeatureSet()`。 |
| `featureTags()` / `clearFeatures()` | 枚举或清除所有显式特性。 | 只列出此 `QFont` 上设置的项，不代表字体支持列表。 |
| `setVariableAxis(tag, value)` | 请求某可变字体轴的值。 | 应限制在 `QFontInfo::variableAxes()` 报告的范围内。 |
| `unsetVariableAxis(tag)` | 移除某个轴的显式请求。 | 回到该轴默认值或匹配器行为。 |
| `isVariableAxisSet(tag)` / `variableAxisValue(tag)` | 查询是否显式设置及其值。 | 先调用 `isVariableAxisSet()`；未设置时数值本身不能说明状态。 |
| `variableAxisTags()` / `clearVariableAxes()` | 枚举或清除显式轴设置。 | 仅为请求中的轴，不等于字体实际提供的轴。 |

### 匹配、合并与替换

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `exactMatch()` | 判断窗口系统是否存在完全匹配的字体。 | 不保证文字覆盖，也不等于像素输出完全一致。 |
| `resolve(other)` | 用 `other` 补齐本对象未显式设置的属性。 | 常用于控件继承字体；已设置属性保持本对象的值。 |
| `key()` | 返回内部缓存/比较用的键。 | 不能当作用户可见字体名称或稳定持久化格式。 |
| `substitute(family)` | 返回首个全局替换名。 | 没有替换时返回原家族名。 |
| `substitutes(family)` | 返回全局替换列表。 | 没有替换时为空列表。 |
| `substitutions()` | 返回已配置替换规则的源家族列表。 | 进程级状态。 |
| `insertSubstitution(from, to)` | 添加一个全局替换项。 | 已创建的 `QFont` 不会自动更新。 |
| `insertSubstitutions(from, list)` | 设置多个替换候选。 | 候选顺序有意义。 |
| `removeSubstitutions(family)` | 移除一个源家族的所有替换项。 | 同样需要重新创建相关字体对象。 |

### 枚举速览

| 枚举 | 核心取值与选择建议 |
| --- | --- |
| `Weight` | `Thin=100` 到 `Black=900`，`Normal=400`，`Bold=700`。 |
| `Style` | `StyleNormal`、`StyleItalic`、`StyleOblique`。 |
| `Stretch` | `AnyStretch=0`，`UltraCondensed=50`，`Unstretched=100`，`UltraExpanded=200`。 |
| `Capitalization` | `MixedCase`、全大写、全小写、小型大写、词首大写。 |
| `SpacingType` | `PercentageSpacing` 或 `AbsoluteSpacing`。 |
| `HintingPreference` | 默认、无、仅垂直、完整 hinting；后两者会影响跨设备布局稳定性。 |
| `StyleHint` | `SansSerif`、`Serif`、`Monospace`、`Cursive`、`Fantasy` 等类别提示。 |
| `StyleStrategy` | `PreferOutline`、`PreferBitmap`、`NoAntialias`、`NoFontMerging`、`ContextFontMerging`、`PreferTypoLineMetrics` 等可组合标志。 |

## 易错点

1. 以 `QFont::family()` 判断字体是否安装。它只是请求值；检查实际匹配用 `QFontInfo`，做启动期快速检查可用 `QFontDatabase::families()`。
2. 用 `boundingRect().width()` 做连续文本布局。墨迹边界不等于下一段文字的起点，应使用 `QFontMetricsF::horizontalAdvance()`。
3. 在高 DPI UI 中固定 `pixelSize`。这会令字体随输出设备改变物理大小，优先点大小或由布局决定。
4. 以为设置可变轴就一定生效。只有匹配到支持该轴的可变字体和后端才有预期视觉效果。
5. 对普通 UI 文本使用 `NoFontMerging`。它会破坏混合语言和 emoji 的回退。
