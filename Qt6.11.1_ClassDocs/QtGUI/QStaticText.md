# QStaticText

> Qt 6.11.1 · Qt GUI · 来自 `QStaticText`

## 1. 先建立直觉

`QStaticText` 是为“内容长期不变、却要反复画”的文本准备的缓存对象。它预先保存文本布局和可复用的绘制数据，让大量标签、坐标刻度、节点标题或叠加层不必在每一帧重新解析、换行和塑形。

它不是通用富文本控件，也不是所有 `drawText()` 的替代品。文本、字体、宽度、格式或变换频繁变化时，维护缓存的代价通常抵消收益；这种场景直接 `QPainter::drawText()` 或使用 `QTextLayout` 更合适。

## 2. 类说明

- 头文件：`#include <QStaticText>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：隐式共享值类型，可作为成员缓存。
- 使用 `QPainter::drawStaticText(position, text)` 输出；首次绘制或状态变化时会创建/更新内部布局。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStaticText()` / `QStaticText(text)` | 创建空对象或以字符串创建缓存文本 |
| `setText()` / `text()` | 修改或读取文本；修改会使布局缓存失效 |
| `setTextFormat()` / `textFormat()` | 指定纯文本、富文本或自动识别格式 |
| `setTextOption()` / `textOption()` | 设置换行、对齐、方向等布局选项 |
| `setTextWidth()` / `textWidth()` | 设置首选换行宽度；负值表示不限制 |
| `size()` | 获取当前文本布局占用的浮点尺寸 |
| `prepare(matrix, font)` | 预热指定变换和字体下的缓存，避免第一次绘制抖动 |
| `setPerformanceHint()` / `performanceHint()` | 在内存与缓存激进程度之间取舍 |
| `PerformanceHint::ModerateCaching` | 默认的适度缓存，适合大多数重复绘制 |
| `PerformanceHint::AggressiveCaching` | 更积极缓存，尤其可能利于 OpenGL/QOpenGLWidget，代价是内存 |
| `swap()` / 比较与赋值运算符 | 管理缓存值对象 |

## 4. 关键用法

### 缓存画布上的稳定标签

```cpp
class NodeLabel {
public:
    QStaticText title;

    explicit NodeLabel(const QString &name) : title(name) {
        QTextOption option(Qt::AlignCenter);
        option.setWrapMode(QTextOption::NoWrap);
        title.setTextOption(option);
    }
};

void Canvas::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setFont(labelFont);
    for (const NodeLabel &node : nodes)
        p.drawStaticText(nodePosition(node), node.title);
}
```

缓存对象应与业务对象一起保存，而不是在每一次 `paintEvent()` 临时创建。若标题变化，调用 `setText()`；下一次绘制时 Qt 自动重建必要布局。

### 在已知样式下预热

```cpp
QStaticText caption("Frames per second");
caption.setPerformanceHint(QStaticText::AggressiveCaching);
caption.prepare(QTransform(), hudFont);
```

`prepare()` 将首次布局成本前移到加载/初始化阶段。传入的 `font` 和 `matrix` 必须接近实际绘制时的 painter 状态；字体或变换不一致仍会导致重算。对非 OpenGL2 绘制引擎，矩阵变化也可能使缓存无效。

### 让静态文本按指定宽度换行

```cpp
QStaticText note(description);
note.setTextFormat(Qt::PlainText);
note.setTextWidth(220.0);

const QSizeF extent = note.size();
painter.drawStaticText(QPointF(12, 12), note);
```

`setTextWidth()` 是**首选**换行宽度。无法拆开的长 token 仍可超出；用 `size()` 获取实际结果，再决定背景区域和控件高度。

## 5. 使用场景

- 图表刻度、网格标签、地图标注、仪表盘固定文案。
- 大量节点或项目拥有很少变化的名称，且频繁重绘。
- 高帧率画布中的状态文字、HUD、调试信息。
- OpenGL 相关绘制中的可复用文本，经过实际性能测试后使用激进缓存。

## 6. 常见坑与经验

- **变化快的文本不要缓存。** 时钟、进度、搜索高亮、打字预览每帧或每次输入变化，`QStaticText` 通常没有优势。
- **缓存键包含绘制状态。** 文本、文本宽度、格式、选项、字体和某些变换变化都会重排；不要误以为只要字符串相同就能复用。
- **`Qt::AutoText` 可能把意外的尖括号当富文本。** 来自文件名、日志或用户输入的文字通常显式设为 `Qt::PlainText`。
- **`size()` 是布局尺寸，不是 widget 的自动尺寸。** 它不会替你更新 `sizeHint()` 或调用 `updateGeometry()`。
- **Aggressive 不是默认答案。** 它会占用更多内存；先剖析，再只给重复热点开启。
- **只在 GUI 线程绘制。** 值对象可准备数据，但与 GUI 绘制相关的使用仍应遵守 painter/设备线程规则。

## 7. 知识点覆盖

文本布局缓存、重绘热点、缓存失效、预热、富文本识别、换行宽度、浮点文本尺寸、OpenGL 绘制优化、内存与性能取舍。
