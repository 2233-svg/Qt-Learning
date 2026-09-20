# Qt QPlainTextDocumentLayout 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPlainTextDocumentLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractTextDocumentLayout -> QPlainTextDocumentLayout`  
> 定位：纯文本文档排版器

## 1. QPlainTextDocumentLayout 解决什么问题

`QPlainTextDocumentLayout` 不是通用“布局管理器”，而是 `QTextDocument` 的纯文本排版实现。它负责把文档里的文本 block 计算成可绘制的几何信息，并把这些信息交给 `QPlainTextEdit` 这类控件使用。

它最适合做这些事：

- 大段纯文本显示；
- 日志窗口；
- 代码编辑器的底层排版；
- 只关心 block、光标和滚动，不需要复杂富文本结构的场景。

它不适合拿来排版表格、复杂富文本、嵌入对象很多的文档；那类需求更应该看 `QTextDocumentLayout` 体系中的其他实现。

```text
QTextDocument
  └─ QAbstractTextDocumentLayout
       └─ QPlainTextDocumentLayout
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 给 QTextDocument 安装纯文本布局

```cpp
#include <QApplication>
#include <QPlainTextEdit>
#include <QPlainTextDocumentLayout>
#include <QTextDocument>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    auto *document = new QTextDocument;
    document->setPlainText("line 1\nline 2\nline 3");
    document->setDocumentLayout(new QPlainTextDocumentLayout(document));

    QPlainTextEdit edit;
    edit.setDocument(document);
    edit.show();

    return app.exec();
}
```

`QPlainTextEdit` 默认就会使用适合纯文本的排版方式，但如果你直接操作 `QTextDocument`，就要明确给它安装合适的 layout。

## 3. 核心使用模型

### 3.1 它按 block 工作

纯文本文档的核心单位是 `QTextBlock`。每一段文本 block 都有自己的高度、位置和可见区域。布局器负责更新这些 block 的几何，而不是像富文本那样走复杂的分页和对象布局。

### 3.2 它的职责是“文档几何”，不是“编辑器逻辑”

`QPlainTextDocumentLayout` 不负责输入框、滚动条、光标键盘导航这些控件交互；那些是 `QPlainTextEdit` 的事。它只告诉上层：

- 文档多大；
- 某个 block 在哪里；
- 文档变了以后哪里需要更新。

### 3.3 更新是增量的

文档内容变化时，布局器会收到 `documentChanged()`，然后只更新受影响的 block。这样大文本编辑器才能比富文本布局更轻。

### 3.4 `cursorWidth` 影响光标绘制

`cursorWidth` 是这类布局器里比较少见但很实用的属性。它控制文本光标宽度，通常会被编辑器用来统一显示效果。

## 4. 适合用在哪里

- 纯文本编辑器；
- 日志查看器；
- 代码浏览器；
- 只要求 block 排版，不要求富文本混排的文档视图。

如果文档里有图片、表格、浮动对象、复杂富格式，`QPlainTextDocumentLayout` 就不是首选。

## 5. 常见误区

### 5.1 把它当成 QWidget 布局

它不是 `QLayout`，也不摆控件位置。它排的是文档 block。

### 5.2 以为它支持完整富文本排版

不支持。它的目标是纯文本效率，而不是富文本能力。

### 5.3 忽略 document 所有权

布局器要绑定到 `QTextDocument` 上，不是随便 new 一个就能直接当独立对象用。

### 5.4 以为 `requestUpdate()` 会立刻重绘

它只是发起更新请求，真正的重绘仍要看上层控件和事件循环。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `cursorWidth : int` | 控制纯文本编辑器里光标的绘制宽度。 | 影响视觉呈现，不改文档内容。 |
| 构造 | `QPlainTextDocumentLayout(QTextDocument *document)` | 给指定文档安装纯文本布局。 | 文档是核心宿主对象。 |
| 析构 | `~QPlainTextDocumentLayout()` | 销毁布局器对象。 | 绑定的文档关系要按所有权规则处理。 |
| 属性访问器 | `cursorWidth() const` | 读取当前光标宽度。 | 和 `setCursorWidth()` 配对使用。 |
| 属性访问器 | `setCursorWidth(int width)` | 设置当前光标宽度。 | 一般传入像素值。 |
| 几何 | `blockBoundingRect(const QTextBlock &block) const` | 返回某个 block 的边界矩形。 | 这是 block 排版的核心查询之一。 |
| 更新 | `documentChanged(int from, int charsRemoved, int charsAdded)` | 响应文档内容变化并更新布局。 | 由框架调用，通常不手动触发。 |
| 查询 | `documentSize() const` | 返回整个文档的推荐尺寸。 | 会随文本量和 block 布局变化。 |
| 绘制 | `draw(QPainter *, const PaintContext &)` | 把文档按纯文本方式绘制出来。 | 上层视图通过它完成显示。 |
| 几何 | `ensureBlockLayout(const QTextBlock &block) const` | 确保某个 block 的布局已计算。 | 需要时用于延迟布局补全。 |
| 几何 | `frameBoundingRect(QTextFrame *) const` | 返回 frame 的边界矩形。 | 纯文本场景下通常不复杂。 |
| 命中 | `hitTest(const QPointF &, Qt::HitTestAccuracy) const` | 根据点位置找字符位置。 | 光标定位和鼠标点击依赖它。 |
| 查询 | `pageCount() const` | 返回文档页数。 | 纯文本里一般更关注滚动而不是分页。 |
| 更新 | `requestUpdate()` | 请求文档布局更新。 | 只是请求，不等于立刻绘制。 |
| 父类查询 | `document() const` | 返回当前绑定的 `QTextDocument`。 | 用于确认布局器挂在哪个文档上。 |
| 父类查询 | `paintDevice() const` | 返回当前绘制设备。 | 影响排版和测量结果。 |
| 父类查询 | `anchorAt(const QPointF &pos) const` | 查询某个点对应的锚点链接。 | 富文本能力有限，但接口仍在父类里。 |
| 父类查询 | `imageAt(const QPointF &pos) const` | 查询某个点处的图片资源。 | 纯文本布局通常很少用到。 |
| 父类查询 | `formatAt(const QPointF &pos) const` | 查询某个点处的文本格式。 | 用于定位和格式检查。 |
| 父类查询 | `blockWithMarkerAt(const QPointF &pos) const` | 返回带标记的 block。 | 供编辑和布局辅助使用。 |
| 父类更新 | `setPaintDevice(QPaintDevice *device)` | 指定布局使用的绘制设备。 | 改设备会影响测量和绘制。 |
| 父类注册 | `registerHandler(int objectType, QObject *component)` | 注册自定义文本对象处理器。 | 复杂富文本布局会用到。 |
| 父类注册 | `unregisterHandler(int objectType, QObject *component = nullptr)` | 注销自定义文本对象处理器。 | 与注册接口配对。 |
| 父类查询 | `handlerForObject(int objectType) const` | 查询某类对象的处理器。 | 自定义文本对象时使用。 |

## 7. 一句话总结

`QPlainTextDocumentLayout` 是 `QTextDocument` 的纯文本排版实现，适合大文本和编辑器场景，核心价值是按 block 计算几何并保持更新轻量。
