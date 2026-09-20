# QGlyphRun

> Qt 6.11.1 · Qt GUI · 来自 `QGlyphRun`

## 1. 先建立直觉

Unicode 字符串不是绘制器最终看到的东西。文本塑形以后，一个或多个字符会变成字体内部的**字形索引**，再配上每个字形的准确位置、方向、装饰与原始字体；这一小段可直接绘制的数据就是 `QGlyphRun`。

它处在文本系统的底层边缘。通常由 `QTextLayout::glyphRuns()` 产出，再交给 `QPainter::drawGlyphRun()` 绘制。只有在自定义文本渲染、选择区域、轮廓提取、GPU 文本或诊断连字时，才需要主动操作它。

## 2. 类说明

- 头文件：`#include <QGlyphRun>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：值类型；保存 `QRawFont`、字形索引、对应位置、可选源字符串和索引。
- 相关类：`QTextLayout` 负责塑形与布局；`QRawFont` 提供字形轮廓和字形索引；`QPainter::drawGlyphRun()` 负责输出。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGlyphRun()` / `isEmpty()` / `clear()` | 创建、判断和清空字形运行 |
| `rawFont()` / `setRawFont()` | 读取或指定解释字形索引的原始字体 |
| `glyphIndexes()` / `setGlyphIndexes()` | 读取或设置字体内部 glyph ID 列表 |
| `positions()` / `setPositions()` | 读取或设置各 glyph 的基线位置 |
| `setRawData(indexes, positions, size)` | 零拷贝地引用外部 glyph ID 与位置数组 |
| `boundingRect()` / `setBoundingRect()` | 获取或覆盖这一段应占的绘制范围 |
| `flags()` / `setFlags()` / `setFlag()` | 批量或单独设置绘制语义标志 |
| `isRightToLeft()` / `setRightToLeft()` | 查询或设置从右到左的视觉运行 |
| `underline()` / `overline()` / `strikeOut()` | 查询或设置文字装饰标志 |
| `sourceString()` / `setSourceString()` | Qt 6.5 起保存产生该 run 的原始字符串 |
| `stringIndexes()` / `setStringIndexes()` | Qt 6.5 起保存 glyph 对应的源字符串位置 |
| `GlyphRunFlag::SplitLigature` | 标记当前运行仅代表连字的一部分，绘制时必须裁剪 |
| `swap()` / 比较与赋值运算符 | 管理和比较值对象 |

## 4. 关键用法

### 从 QTextLayout 取得已塑形结果

```cpp
QTextLayout layout(text, font);
layout.beginLayout();
QTextLine line = layout.createLine();
line.setLineWidth(width);
layout.endLayout();

for (const QGlyphRun &run : line.glyphRuns()) {
    painter.drawGlyphRun(QPointF(0, line.ascent()), run);
}
```

应该让 `QTextLayout` 处理连字、阿拉伯文形态、组合音标与双向顺序。手动把每个 `QChar` 映射为 glyph ID 会直接跳过这些关键步骤。

### 在自定义绘制中处理连字切片

```cpp
for (const QGlyphRun &run : selectedRuns) {
    painter.save();
    if (run.flags().testFlag(QGlyphRun::SplitLigature))
        painter.setClipRect(run.boundingRect());
    painter.drawGlyphRun(origin, run);
    painter.restore();
}
```

选区恰好落在 `fi`、阿拉伯文连写等连字的一部分时，run 可能拥有完整连字 glyph，却只代表其中几个源字符。`SplitLigature` 表示必须裁剪到 `boundingRect()`，否则会把选区外的连字部分一起画出来。

### 使用零拷贝原始数组时保住生命周期

```cpp
QVector<quint32> ids = { glyphA, glyphB };
QVector<QPointF> positions = { {0, 0}, {12.4, 0} };

QGlyphRun run;
run.setRawFont(rawFont);
run.setRawData(ids.constData(), positions.constData(), ids.size());
painter.drawGlyphRun(origin, run); // ids 和 positions 此时必须仍然存在
```

`setRawData()` 不接管数组，也不复制数组。`ids` 与 `positions` 必须在 `QGlyphRun` 的所有使用期间保持存活且地址不变；`QVector` 扩容、离开作用域或后台线程修改都会让 run 悬空。需要长期持有时，使用 `setGlyphIndexes()` 与 `setPositions()` 复制数据。

## 5. 使用场景

- 富文本或代码编辑器的选区、搜索高亮和自定义装饰层。
- 将 `QTextLayout` 的排版结果交给特殊绘制后端。
- 从 `QRawFont` 提取 glyph ID，再绘制字形或轮廓。
- 排查字体回退、连字、RTL 视觉顺序和字符到 glyph 的映射。

## 6. 常见坑与经验

- **glyph ID 只在对应 `QRawFont` 中有意义。** 把某字体的 indexes 配给另一字体，会得到错误字形或空白。
- **列表长度必须匹配。** 每个 glyph ID 应有对应位置；不匹配的数据没有可靠的绘制语义。
- **位置不是字符索引。** 它们是塑形后的视觉坐标，不能当作 `QString` 的下标。
- **`RightToLeft` 不等于反转数组。** 方向属于布局语义；自行 reverse 往往会破坏双向文本顺序。
- **`sourceString()` 与 `stringIndexes()` 是辅助元数据。** 它们在 Qt 6.5 才有，且不是所有手工构造的 run 都具备。
- **低层 API 不代替文本布局。** 如果你的目标只是画一段文本，用 `QPainter::drawText()`；如果是编辑和命中测试，用 `QTextLayout`。

## 7. 知识点覆盖

Unicode 到字形塑形、glyph ID、`QRawFont`、基线坐标、双向文字、连字裁剪、零拷贝生命周期、富文本选区、自定义文本渲染。
