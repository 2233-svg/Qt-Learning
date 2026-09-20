# QRawFont

> Qt 6.11.1 · Qt GUI · 来自 `QRawFont`

## 1. 先建立直觉

`QFont` 表达“想要什么字体”；`QRawFont` 表达“已经选定的一张物理字体，以某个像素大小解释 glyph”。它让程序直接访问 cmap 映射、glyph ID、轮廓、字形位图、sfnt 表和设计度量。

这不是普通文字显示的首选。`QRawFont` 不做完整 OpenType 塑形，不理解文本方向、连字上下文或脚本规则；要把一段 Unicode 正确排成字形，先用 `QTextLayout`。它适合字体检查器、轮廓文字、字形缓存和自定义渲染器。

## 2. 类说明

- 头文件：`#include <QRawFont>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：值类型；空构造结果无效，所有低层查询前应检查 `isValid()`。
- 可由 TrueType/OpenType 文件、内存数据，或 `fromFont()` 的实际物理匹配构造。
- `pixelSize` 影响度量、轮廓缩放和栅格化结果；它不是 `QFont` 的 point size。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QRawFont(file/data, pixelSize, hinting)` | 从字体文件或内存 OpenType/TrueType 构造 |
| `loadFromFile()` / `loadFromData()` | 重新载入当前对象 |
| `fromFont(font, writingSystem)` | 从一个字体请求取得优先匹配的物理字体 |
| `isValid()` | 判断加载或匹配是否成功 |
| `familyName()` / `styleName()` / `style()` / `weight()` | 查询物理字体信息 |
| `pixelSize()` / `setPixelSize()` | 查询或更改 glyph 解释、栅格化的像素大小 |
| `glyphIndexesForString()` | 用 cmap 将字符映射到 glyph ID，不做完整塑形 |
| `glyphIndexesForChars()` | 指针数组版本，避免列表分配并可处理容量不足 |
| `glyphCount()` / `glyphName()` | Qt 6.11 起查询字体内 glyph 总数与名称 |
| `supportsCharacter()` | 检查特定 BMP 或 UCS-4 字符是否存在 glyph |
| `pathForGlyph()` | 获得未 hint 的 `QPainterPath` 轮廓 |
| `alphaMapForGlyph()` | 把单个 glyph 栅格化为 alpha/子像素图像 |
| `boundingRect()` | 获取单 glyph 的像素级逻辑包围框 |
| `advancesForGlyphIndexes()` | 计算 glyph 前进量，可选 kerning、设计度量 |
| `ascent()` / `descent()` / `leading()` | 获取浮点行度量 |
| `capHeight()` / `xHeight()` / `averageCharWidth()` / `maxCharWidth()` | 获取辅助排版度量 |
| `lineThickness()` / `underlinePosition()` | 获取适合该字体的装饰线尺寸 |
| `unitsPerEm()` | 得到字体内部设计单位缩放基准 |
| `fontTable(tag)` | 读取原始 sfnt 表；Qt 6.7 起可用类型安全 `QFont::Tag` |
| `supportedWritingSystems()` | 读取字体元数据声明的书写系统 |
| `AntialiasingType` | 选择整像素 alpha 或 RGB 子像素 glyph 图 |
| `LayoutFlags` | 选择单独 advance、传统 kern、设计度量 |
| `swap()` / 比较 / `qHash()` | 管理值对象与缓存键 |

## 4. 关键用法

### 从普通字体请求得到物理字体

```cpp
QFont requested({"Inter", "Noto Sans CJK SC"});
requested.setPixelSize(18);

QRawFont raw = QRawFont::fromFont(
    requested, QFontDatabase::SimplifiedChinese);
if (!raw.isValid())
    return;

qDebug() << raw.familyName() << raw.styleName()
         << raw.unitsPerEm() << raw.glyphCount();
```

`fromFont()` 会执行字体匹配，成本可能较高，不能放在高频绘制路径。其 `writingSystem` 参数影响优先取哪张物理字体；混排文本可能仍会需要多个 `QRawFont`，因此完整文本应让 `QTextLayout` 产生 `QGlyphRun`。

### 把 glyph 轮廓变成路径

```cpp
const QList<quint32> ids = raw.glyphIndexesForString("A");
if (!ids.isEmpty()) {
    QPainterPath outline = raw.pathForGlyph(ids.first());
    painter.save();
    painter.translate(anchor);
    painter.fillPath(outline, Qt::black);
    painter.restore();
}
```

`pathForGlyph()` 的轮廓**不带 hinting**。这正适合放大、布尔运算、动画和导出矢量，但在小字号屏幕文字上可能不如平台文字渲染清晰。普通文本仍使用 `drawText()` 或 `drawGlyphRun()`。

### 制作单 glyph 位图缓存

```cpp
const quint32 glyph = raw.glyphIndexesForString("A").value(0);
QImage image = raw.alphaMapForGlyph(
    glyph, QRawFont::PixelAntialiasing);

if (!image.isNull())
    cache.insert({ raw, glyph }, image);
```

`PixelAntialiasing` 生成覆盖率 alpha 图（通常 `Indexed8`）；`SubPixelAntialiasing` 可能生成 RGB32，每个通道表达子像素覆盖。彩色字体 glyph 的结果可能不同，且会忽略所选抗锯齿类型。

### 计算 glyph advance 的适用边界

```cpp
const QList<quint32> glyphs = raw.glyphIndexesForString("AV");
const QList<QPointF> advances = raw.advancesForGlyphIndexes(
    glyphs, QRawFont::KernedAdvances | QRawFont::UseDesignMetrics);
```

`KernedAdvances` 仅能利用传统 TrueType `kern` 表，不能替代现代 OpenType GPOS、连字、阿拉伯文形态和字符重排。只要输入是自然语言文本，就应改用 `QTextLayout`；这里适合你已经有正确 glyph 序列的专用渲染路径。

## 5. 使用场景

- 字体浏览器、字体诊断器、字体文件元数据查看器。
- 将文字轮廓转换为 `QPainterPath`，制作徽标、路径动画或矢量导出。
- 自定义 glyph atlas、纹理缓存或游戏/图形引擎文本后端。
- 检查某个字体能否覆盖特定 Unicode 码点。
- 读取 `cmap`、`name`、`GSUB` 等 sfnt 表，做字体分析工具。

## 6. 常见坑与经验

- **字符映射不是塑形。** `glyphIndexesForString("ffi")` 不会保证得到真实绘制时的连字；复杂文本必须 `QTextLayout`。
- **glyph ID 不能跨字体复用。** 同一个数值在不同 `QRawFont` 里表示完全不同的 glyph。
- **先检查有效性。** 文件加载失败、格式不受支持或物理匹配失败时，后续结果可能为空。
- **`fontTable()` 返回大端 sfnt 原始字节。** 解析它需要理解 OpenType 表格式与字节序，不能当 UTF-8 文本。
- **`supportedWritingSystems()` 只看字体表声明。** 最终字符覆盖应使用 `supportsCharacter()`，且 emoji 序列还涉及多个码点与选择符。
- **`setPixelSize()` 会改变缓存语义。** 任何以轮廓坐标、位图或 advance 为键的缓存都必须包含字号与 hinting。
- **指针版 API 的数组容量由调用者保证。** `glyphIndexesForChars()` 在空间不足时返回 `false` 并通过 `numGlyphs` 告知所需数量。

## 7. 知识点覆盖

物理字体、OpenType/sfnt、cmap、glyph ID、字形轮廓、字形栅格化、hinting、设计单位、传统 kerning 与复杂塑形、字体表解析、glyph 缓存。
