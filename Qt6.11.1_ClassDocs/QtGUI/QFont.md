# QFont

> Qt 6.11.1 · Qt GUI · 来自 `QFont`

## 1. 先建立直觉

`QFont` 不是某一份已打开的字体文件，而是一份**字体请求**：我偏好哪些字族、希望多大、多粗、是否斜体、以什么策略匹配。真正渲染时 Qt 再根据系统字体库、设备 DPI、文字脚本和可用后端选择实际字体，必要时回退到其他字族。

因此，`QFont` 适合设置 UI 外观和传递排版意图；若要知道实际结果，用 `QFontInfo`；若要知道文字尺寸，用 `QFontMetrics`；若要编辑复杂文本或获取 glyph，使用 `QTextLayout`。

## 2. 类说明

- 头文件：`#include <QFont>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：隐式共享的值类型，可复制、保存于 `QVariant`、`QSettings` 和容器中。
- 字体请求通常由控件、`QPainter` 或 `QGuiApplication` 的默认字体继承，并可用 `resolve()` 合并。
- 实际匹配取决于平台。`exactMatch()` 是诊断工具，不应作为普通 UI 的硬失败条件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFont()` / `QFont(family, size, weight, italic)` | 创建默认字体请求或指定首选字族的请求 |
| `setFamily()` / `setFamilies()` / `family()` / `families()` | 设置或读取单个字族、回退候选列表 |
| `defaultFamily()` / `exactMatch()` | 查询默认候选与请求是否被精确满足 |
| `setPointSize()` / `setPointSizeF()` | 用设备无关的 point 指定字号 |
| `setPixelSize()` | 用设备相关像素指定字号 |
| `pointSize()` / `pointSizeF()` / `pixelSize()` | 读取所采用的字号表示；另一个表示通常为 `-1` |
| `setWeight()` / `setBold()` / `weight()` / `bold()` | 设置或读取离散字重（100 至 900） |
| `setItalic()` / `setStyle()` / `setStyleName()` | 请求斜体、oblique 或字体专有样式 |
| `setStretch()` / `stretch()` | 请求压缩或扩展字宽 |
| `setCapitalization()` | 渲染时改为全大写、小写、小型大写或词首大写 |
| `setUnderline()` / `setOverline()` / `setStrikeOut()` | 设置文字装饰 |
| `setLetterSpacing()` / `setWordSpacing()` | 调整字距、词距 |
| `setKerning()` | 控制 kerning；会影响字符串宽度 |
| `setFixedPitch()` | 向匹配器表达等宽偏好，不保证实际列宽 |
| `setStyleHint()` / `setStyleStrategy()` | 指导字体匹配、抗锯齿、回退和轮廓/位图偏好 |
| `setHintingPreference()` | 请求字体 hinting 策略，平台可忽略 |
| `setFeature()` / `unsetFeature()` / `featureTags()` | Qt 6.7 起显式控制 OpenType 特性 |
| `setVariableAxis()` / `unsetVariableAxis()` / `variableAxisTags()` | Qt 6.7 起设置可变字体轴 |
| `resolve(other)` | 把当前已显式设置的属性与另一个字体合并 |
| `toString()` / `fromString()` | 在设置中序列化、恢复字体描述 |
| `key()` / `operator<` / `qHash()` | 用作缓存或关联容器的键 |
| `operator QVariant()` / 数据流运算符 | 与 QVariant、QDataStream 互操作 |
| `insertSubstitution()` 等静态函数 | 配置进程级字族替换规则 |
| `swap()` / `isCopyOf()` / 比较与赋值运算符 | 管理隐式共享值对象 |

## 4. 关键用法

### 把字族回退作为显式设计

```cpp
QFont uiFont;
uiFont.setFamilies({
    "Inter",
    "Noto Sans CJK SC",
    "Segoe UI",
    "sans-serif"
});
uiFont.setPointSizeF(10.5);
uiFont.setWeight(QFont::Medium);
titleLabel->setFont(uiFont);
```

`setFamilies()` 的首项是主偏好，后面是明确回退候选；最终仍可能发生系统级回退。中西文混排、emoji 和符号常来自不同字体，这是正常的。需要记录真实匹配时查询 `QFontInfo`。

### point 与 pixel 只能选一种

```cpp
QFont textFont("Noto Sans CJK SC");
textFont.setPointSizeF(11.0);  // 适合常规 UI、打印与 DPI 适配

QFont bitmapFont("Terminal");
bitmapFont.setPixelSize(16);   // 适合必须对齐像素的位图字
```

调用 `setPixelSize()` 会取消 point size；调用 `setPointSize*()` 会取消 pixel size。读取未使用的一种会得到 `-1`。常规桌面 UI 优先 point size；图像缓存、像素艺术或固定分辨率渲染才使用 pixel size。

### 正确处理粗体、斜体和字体专有样式

```cpp
QFont font("Source Serif 4");
font.setWeight(QFont::DemiBold);
font.setItalic(true);

// 只有确知字体提供非标准样式名时才这样写：
// font.setStyleName("Caption");
```

`styleName()` 用于字体内部不规则的命名实例，设置后匹配器可能忽略 `weight()` 和 `style()`。不要同时用两套 UI 控件无提示地竞争；普通设置应优先 `setWeight()`、`setItalic()`、`setStyle()`。

### 设置 OpenType 特性与可变字体轴

```cpp
QFont font("Roboto Flex");
font.setVariableAxis("wght", 550.0f);
font.setVariableAxis("wdth", 92.0f);

font.setFeature("tnum", 1); // tabular figures，前提是字体支持
font.setFeature("liga", 0); // 明确关闭标准连字
```

`QFont::Tag` 必须是四字符标识；字面量 `"wght"`、`"tnum"` 会在编译期受约束。`setFeature()` 传入的通常是开关值，但少数特性用非零值表达索引。应先理解字体特性，不能把 tag 当任意 CSS 属性。

显式设置 `letterSpacing()` 时，Qt 默认会禁用装饰性连字；`kerning()` 也会改变宽度。对布局敏感的文本，设置这些属性后重新测量，不要复用旧的缓存尺寸。

### 从应用默认字体派生局部样式

```cpp
QFont emphasis;
emphasis.setWeight(QFont::Bold);
emphasis.setUnderline(true);

QFont inherited = emphasis.resolve(QGuiApplication::font());
```

`resolve()` 的方向容易写反：返回值以调用者已显式设置的属性为优先，其他未设置属性从参数 `other` 补齐。它适合主题和局部覆盖，而不是把两个完整字体任意“混合”。

### 持久化用户选择

```cpp
settings.setValue("editor/font", editorFont.toString());

QFont restored;
if (restored.fromString(settings.value("editor/font").toString()))
    editor->setFont(restored);
```

序列化的是字体请求，不是可移植的字体资源。换电脑或操作系统后仍可能匹配到不同字体；对产品配置应保存回退策略，并接受回退。

## 5. 重要枚举与策略

| 枚举 | 实际决策 |
| --- | --- |
| `Weight` | `Thin=100` 至 `Black=900` 的 CSS 风格字重刻度；普通用 `Normal=400`、`Bold=700` |
| `Style` | `StyleNormal`、设计好的 `StyleItalic`、通常由正体倾斜得到的 `StyleOblique` |
| `Stretch` | `AnyStretch` 表示不限制；`Unstretched=100`，其余是压缩/扩展请求 |
| `Capitalization` | 改变绘制文本的大小写外观，不改变原 `QString` 内容 |
| `SpacingType` | `PercentageSpacing` 以字宽百分比调整，100 表示不变；`AbsoluteSpacing` 以像素调整 |
| `StyleHint` | 表达通用家族偏好，如 `SansSerif`、`Serif`、`Monospace`、`Cursive`、`System` |
| `StyleStrategy` | 影响匹配和渲染，如 `PreferOutline`、`NoAntialias`、`NoFontMerging`、`PreferQuality` |
| `HintingPreference` | 在清晰度与跨 DPI 度量一致性间取舍：默认、无 hinting、仅垂直、完整 hinting |

`StyleStrategy::ContextFontMerging`（Qt 6.8）会尝试让一段缺字文本采用更一致的回退字体，可能更耗时；`NoFontMerging` 则禁止常规缺字回退。除非产品明确需要可预测的缺字行为，不要轻易禁止合并。

`PreferTypoLineMetrics`（Qt 6.8）可让一些 OpenType 字体采用更紧凑、通常更符合排版语义的 typo 行度量；它会改变行高，启用后应重测布局并做跨平台验证。

## 6. 使用场景

- 应用、窗口、控件、画布和打印输出的字体主题。
- 编辑器或数据表格中的等宽/等数字宽度需求。
- 多语言 UI 的主字族与 CJK、emoji、符号回退设计。
- 高级排版中的可变字重、宽度、OpenType 数字样式和连字控制。
- 用户可配置字体、字体缓存键、设置持久化和样式继承。

## 7. 常见坑与经验

- **请求不是保证。** `setFamily("X")` 不代表 X 真会被使用；用 `QFontInfo` 查实际结果。
- **`setFixedPitch(true)` 不保证每个字符等宽。** 它只是匹配偏好；而 Unicode 回退字符还可能来自另一种字体。列布局用实际测量验证。
- **别在布局后再改 kerning、字距或可变轴。** 它们会改变文本宽度、连字和断行。
- **字体回退不等于“所有字形完整”。** emoji、罕见汉字和数学符号可能触发不同回退；`QFontMetrics::inFontUcs4()` 只能检查单个码点。
- **避免强制 `NoFontMerging`。** 这通常把可读字符变成缺字方框，且不一定阻止书写系统级字体替换。
- **hinting 是偏好不是命令。** 不同后端（Windows、FreeType、macOS）会有不同支持和结果。
- **进程级 substitutions 要慎用。** `insertSubstitution()` 影响整个应用进程，适合启动阶段的兼容层，不适合某个临时控件。
- **比较的是请求属性。** `operator==` 并不表示屏幕上最终使用的是同一字体文件；匹配结果另查。

## 8. 知识点覆盖

字体匹配与回退、隐式共享、point/pixel 字号、字重与样式、字距与 kerning、OpenType 特性、可变字体、字体 hinting、行度量策略、跨平台差异、主题继承、序列化与缓存。
