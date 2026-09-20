# QTextLayout 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextLayout>`  
> 所属模块：`Qt6::Gui`  
> 类型：不可复制的单段文本布局器

## 1. 它解决什么问题

`QTextLayout` 把一段字符串、字体、文本选项和格式范围整形成可绘制的若干 `QTextLine`。它提供手工换行、坐标到光标位置映射、字形运行提取以及绘制能力，适合需要比 `QPainter::drawText()` 更精确控制的单段文本。

它不管理富文本文档树；需要块、表格、撤销和资源时使用 `QTextDocument`。也不等于 QWidget 布局系统；`setPosition()` 只设置这段文字在绘制坐标系中的原点，不会给控件自动排列子控件。

实际场景：

- 自绘控件中的标签、代码行、日志行与命中测试；
- 需要按照固定行宽逐行排版、再自行控制每行 y 坐标；
- 输入法预编辑文本、双向文本光标移动和字形调试；
- 自定义文本视图按范围绘制选择色或查找高亮。

## 2. 手工布局状态机

手工换行必须遵循 `beginLayout()`、反复 `createLine()`、`endLayout()` 的顺序：

```cpp
QTextLayout layout(text, font);
layout.beginLayout();

qreal y = 0;
for (;;) {
    QTextLine line = layout.createLine();
    if (!line.isValid())
        break;

    line.setLineWidth(availableWidth);
    line.setPosition(QPointF(0, y));
    y += line.height();
}

layout.endLayout();
```

`createLine()` 返回无效 `QTextLine` 表示所有文本已经布局完毕，不是异常对象。漏掉 `endLayout()` 会让布局停留在构建状态；`clearLayout()` 会丢弃已有行，因此此前得到的 `QTextLine` 句柄不应再使用。

修改 `text`、`font`、`rawFont`、`textOption`、预编辑区域或 formats 后，应视为旧布局已过期并重新执行布局。缓存开启时 Qt 可以保留内部排版数据，但它不会替你推断外部尺寸和内容变化。

## 3. 坐标、格式与绘制

`setPosition()` 是 layout 的整体偏移，行的 `setPosition()` 是行相对 layout 的位置；`draw()` 的 `pos` 是绘制时再叠加的 painter 坐标。为了避免双重偏移，项目中应明确选择“布局持有位置”或“绘制调用传位置”的一种约定。

`FormatRange` 用于给 layout 文本的局部范围叠加临时 `QTextCharFormat`，常用于选择、高亮和自绘搜索结果。它不修改 `QTextDocument`，也不会写回源字符串。范围以文本位置计数，不是 UTF-8 字节偏移。

`draw()` 需要有效且已开始绘制的 `QPainter`。`selections` 也是临时绘制覆盖；`clip` 为空矩形时不额外限制绘制区域。`drawCursor()` 只绘制光标，不处理输入状态、闪烁计时或焦点管理。

## 4. 光标与字形

`isValidCursorPosition()` 判断位置是否为布局认可的光标边界。`nextCursorPosition()` / `previousCursorPosition()` 可以按字符或单词移动；`leftCursorPosition()` / `rightCursorPosition()` 按视觉方向移动，在双向文字中不必等价于字符串下标加减一。

`glyphRuns()` 返回已整形的 `QGlyphRun`，适合底层绘制、选区或字体调试。默认重载请求常用字形索引和位置；Qt 6.5 起可传 `GlyphRunRetrievalFlags` 请求字符串及字符串索引。数据量较大时不要在普通 `paintEvent` 中无条件反复提取。

## 5. 线程与生命周期

`QTextLayout` 不可复制，也没有 QObject 父子关系；它拥有可变的排版状态。不要让多个线程并发读写同一个 layout，即使部分方法标为 `const`。若在后台做独立文本测量，使用完全独立的 layout 和与目标环境一致的字体/设备配置。

绘制时还必须遵守 `QPainter` 与其目标设备的线程规则。由 `QTextBlock::layout()` 得到的 layout 属于该文档，文档修改、块删除或 `clearLayout()` 后不得继续保存其行句柄。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextLayout()` | 创建空布局。 | 后续应设置文本和字体再布局。 |
| `QTextLayout(const QString &text)` | 用文本创建布局。 | 使用默认字体状态；最终度量依赖后续字体设置。 |
| `QTextLayout(const QString &, const QFont &, const QPaintDevice * = nullptr)` | 用文本、字体和可选设备创建布局。 | 设备影响字体度量；绘制到不同设备时要留意 DPI 差异。 |
| `QTextLayout(const QTextBlock &block)` | 为块的文本布局创建访问对象。 | 依附来源文档；块或文档变化后不要缓存结果。 |
| `~QTextLayout()` | 销毁布局及内部排版缓存。 | 关联 `QTextLine` 和内联对象句柄随之失效。 |
| `setText()` / `text()` | 设置或读取布局文本。 | 改文本后重新布局。 |
| `setFont()` / `font()` | 设置或读取默认字体。 | 改字体后重新布局。 |
| `setRawFont()` | 直接设置 raw font。 | 仅在启用 raw font 的构建中可用；改后重新布局。 |
| `setTextOption()` / `textOption()` | 设置或读取换行、方向、制表位等选项。 | 改选项后旧行几何不再可信。 |
| `setPreeditArea()` / `preeditAreaPosition()` / `preeditAreaText()` | 设置或读取输入法预编辑区域。 | 位置使用 layout 文本坐标；UI 仍需自行管理输入法会话。 |
| `setFormats()` / `formats()` / `clearFormats()` | 管理临时格式覆盖列表。 | 不修改文档或源文本；范围按 layout 文本位置计。 |
| `setCacheEnabled()` / `cacheEnabled()` | 开关内部布局缓存。 | 优化提示，不替代内容变化后的重新布局。 |
| `setCursorMoveStyle()` / `cursorMoveStyle()` | 设置逻辑或视觉光标移动风格。 | 双向文本中会明显影响左右移动。 |
| `beginLayout()` | 开始创建行。 | 必须与 `endLayout()` 成对。 |
| `createLine()` | 创建下一行。 | 失败/结束时返回无效 `QTextLine`；创建后立即设置宽度。 |
| `endLayout()` | 完成行创建。 | 漏掉会留下不完整布局状态。 |
| `clearLayout()` | 清除已有行。 | 旧 `QTextLine`、内联对象句柄不再可用。 |
| `lineCount()` / `lineAt(int)` | 查询行数或取第 N 行。 | 索引越界不能当作有效行；先检查范围。 |
| `lineForTextPosition(int)` | 查找包含指定文本位置的行。 | 位置是 layout 文本坐标。 |
| `isValidCursorPosition(int)` | 判断是否为有效光标边界。 | 不要假设每个 UTF-16 位置都可作为视觉光标点。 |
| `nextCursorPosition()` / `previousCursorPosition()` | 按字符或单词移动逻辑位置。 | `SkipWords` 依赖分词边界。 |
| `leftCursorPosition()` / `rightCursorPosition()` | 按视觉左右方向移动。 | RTL/BiDi 中不等于字符串索引加减一。 |
| `setPosition()` / `position()` | 管理整体布局位置。 | 与 `draw()` 的位置参数会叠加。 |
| `boundingRect()` | 返回已布局内容的边界。 | 布局不完整或刚变更时不是最终几何。 |
| `minimumWidth()` / `maximumWidth()` | 返回布局计算出的最小/最大自然宽度。 | 用于尺寸协商，不等同于当前每行设置宽度。 |
| `draw()` | 绘制布局及可选选择格式。 | painter 必须有效；不会自动完成未做的 layout。 |
| `drawCursor()` | 在指定位置绘制光标。 | 只绘制，不维护焦点、闪烁或输入法。 |
| `glyphRuns(int, int)` | 提取范围的字形运行。 | 默认范围为全部；代价高于普通绘制。 |
| `glyphRuns(int, int, GlyphRunRetrievalFlags)` | 按检索标志提取字形运行。 | Qt 6.5 起；按需求请求数据，避免 `RetrieveAll` 滥用。 |
| `GlyphRunRetrievalFlags` | 请求字形索引、位置、字符串索引、字符串或全部数据。 | 仅在启用 raw font 支持时可用。 |

## 7. 记忆重点

`QTextLayout` 是单段文本的手工排版器。最重要的契约是“改输入后重新布局”和 `beginLayout()` -> `createLine()` -> `endLayout()`；`QTextLine`、内联对象和字形数据都是当前布局状态的短期视图。
