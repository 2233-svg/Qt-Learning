# Qt QAbstractTextDocumentLayout 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractTextDocumentLayout>`  
> 所属模块：`Qt6::Gui`  
> 基类：`QObject`  
> 定位：把 `QTextDocument` 的内容结构转换为几何、绘制结果和命中测试的抽象布局基类

## 1. 它解决什么问题

`QTextDocument` 保存的是富文本结构：段落、字符格式、表格、列表、图片、嵌入对象和文本框架。它本身不规定这些内容在某个页面、窗口或打印设备上具体排成什么几何形状。`QAbstractTextDocumentLayout` 就是这层“结构到视觉结果”的接口。

布局需要回答四类问题：

1. 这份文档有多少页，整体尺寸是多少？
2. 每个 frame 或 block 在文档坐标中占据哪块矩形？
3. 给定一个点，应该命中哪个字符位置、链接、图片或文本格式？
4. 如何用 `QPainter` 把文档画到屏幕、打印机或图像设备？

Qt 的富文本控件通常使用 Qt 自带的具体布局实现。只有在实现自定义编辑器、分页排版器、特殊打印布局、文档预览器或嵌入对象布局时，才需要直接继承这个抽象类。

它不是一个可以直接使用的“自动布局工具”：

- 类含有多个纯虚函数，不能直接实例化；
- 派生类必须维护自己的排版缓存；
- `QTextDocument` 的结构变化会通过 `documentChanged()` 进入派生布局；
- 需要在几何变化、页数变化和局部重绘时发出对应信号。

## 2. 坐标系先分清

自定义布局最容易出错的地方是把不同坐标混在一起：

- **文档坐标**：`documentSize()`、`blockBoundingRect()`、`frameBoundingRect()`、`anchorAt()` 等 API 使用的逻辑坐标；
- **视口坐标**：滚动区域或控件把文档坐标平移、缩放后得到的坐标；
- **绘制设备坐标**：`QPainter` 当前设备和 transform 下的坐标；
- **命中测试输入**：`hitTest()` 接收的点必须按派生布局约定解释，通常是文档坐标。

`PaintContext::clip` 是文档坐标中的绘制优化提示；真正的裁剪仍应由调用者在 `QPainter` 上设置，布局不能假设 `clip` 自动改变 painter 的裁剪区域。

## 3. 最小派生类骨架

```cpp
class SingleColumnLayout final : public QAbstractTextDocumentLayout
{
public:
    explicit SingleColumnLayout(QTextDocument *doc)
        : QAbstractTextDocumentLayout(doc)
    {
    }

    void draw(QPainter *painter,
              const PaintContext &context) override;
    int hitTest(const QPointF &point,
                Qt::HitTestAccuracy accuracy) const override;
    int pageCount() const override;
    QSizeF documentSize() const override;
    QRectF frameBoundingRect(QTextFrame *frame) const override;
    QRectF blockBoundingRect(const QTextBlock &block) const override;

protected:
    void documentChanged(int from,
                         int charsRemoved,
                         int charsAdded) override;
};
```

构造函数中的 `QTextDocument *` 由外部拥有。布局保存的是关联文档关系，不应在析构时删除文档。通常由文档通过 `setDocumentLayout()` 管理布局对象；如果手动替换布局，应明确旧布局和文档的生命周期关系。

## 4. 文档变化与缓存

`documentChanged()` 是派生类更新排版缓存的核心入口。参数含义是：

- `from`：变化开始的文档字符位置；
- `charsRemoved`：被删除的字符数；
- `charsAdded`：新增的字符数。

它描述的是文档内容变化，不是像素矩形。派生类通常需要重新计算受影响的 block、后续内容的垂直位置、页分页点、嵌入对象尺寸以及总文档尺寸。

变化处理完成后，按影响范围发信号：

- 只需局部重绘时发 `update(rect)`；
- 某个 block 的布局或绘制发生变化时发 `updateBlock(block)`；
- 总尺寸改变时发 `documentSizeChanged(newSize)`；
- 页数改变时发 `pageCountChanged(newPages)`。

信号不是“自动替你完成布局”的通知。若派生类缓存未更新就发信号，控件会在下一次绘制或命中测试时读到过期几何。

## 5. 嵌套数据结构

`QAbstractTextDocumentLayout::Selection` 和 `PaintContext` 是绘制请求中的值类型数据，分别见独立笔记：

- [QAbstractTextDocumentLayout_PaintContext_布局管理器.md](D:\笔记\qtAPI知识\QtClass\QtGUI\QAbstractTextDocumentLayout_PaintContext_布局管理器.md)
- [QAbstractTextDocumentLayout_Selection_布局管理器.md](D:\笔记\qtAPI知识\QtClass\QtGUI\QAbstractTextDocumentLayout_Selection_布局管理器.md)

## 6. 逐项 API 说明

### `explicit QAbstractTextDocumentLayout(QTextDocument *doc)`

把布局关联到 `doc`。布局不拥有该文档；文档必须在布局使用期间保持有效。

传入 `nullptr` 不适合作为正常布局对象使用，因为多数查询和变化通知都依赖关联文档。派生类构造时可以初始化自己的缓存，但不要在基类构造完成前调用依赖完整文档状态的复杂逻辑。

### `~QAbstractTextDocumentLayout()`

销毁布局对象及其内部状态。它不会删除构造时传入的 `QTextDocument`。作为 `QObject`，它有线程亲和性和父对象关系；绘制、文档变化和布局缓存访问应遵守对象所在线程的约束。

### `virtual void draw(QPainter *painter, const PaintContext &context) = 0`

把文档绘制到 `painter`。`context` 描述调色板、光标、选区和建议裁剪区域。

实现要求：

- 不应保存 `painter` 指针供异步使用；
- 不应在绘制过程中修改 `QTextDocument`；
- 应尊重 painter 当前的 transform、opacity、clip 和 composition 状态；
- `context.clip` 为空时不能假定“没有任何内容需要画”，它只是可选的优化提示；
- `painter` 必须由调用者保证有效并处于可绘制状态。

如果布局支持图片或自定义文本对象，通常要在合适位置调用 `drawInlineObject()` 或对象处理器的 `drawObject()`。

### `virtual int hitTest(const QPointF &point, Qt::HitTestAccuracy accuracy) const = 0`

把一个文档坐标点转换为字符位置。返回值是 `QTextCursor` 可使用的文档位置；找不到合适位置时返回 `-1`。

`accuracy` 用于区分严格命中和粗略命中。严格命中通常要求点位于文本实际区域，粗略命中可以把点吸附到最近的字符位置。具体吸附策略由派生布局决定，但必须保持结果与自己的绘制几何一致。

不要把返回的字符位置当作像素，也不要在布局缓存未更新时使用旧位置。

### `QString anchorAt(const QPointF &pos) const`

返回点处链接锚点的目标字符串。没有链接或点不在可识别文本区域时返回空字符串。

该函数是基于布局命中测试和字符格式的便利查询，不会导航、不触发网络请求，也不改变文档。返回值是拥有数据的 `QString`，可以直接交给外部逻辑。

### `QString imageAt(const QPointF &pos) const`

返回点处图片资源的标识，通常对应 `QTextImageFormat` 中的 `name`。没有图片时返回空字符串。

返回的是标识，不是 `QImage` 或 `QPixmap`。图片实际如何加载、是否缓存、是否允许网络资源，由文档资源提供逻辑和使用者决定。

### `QTextFormat formatAt(const QPointF &pos) const`

返回点处的文本格式。没有命中有效格式时返回无效或空的 `QTextFormat`。

结果是值类型快照，不是对文档格式对象的可变引用。它适合上下文菜单、格式检查和工具提示；修改返回值不会修改文档。

### `QTextBlock blockWithMarkerAt(const QPointF &pos) const`

返回点处带有列表标记或其他 block marker 的文本块。没有命中时返回无效 `QTextBlock`。

该 API 适合实现点击列表项目符号、编号区域或 block 级交互。它不是通用的“返回最近 block”函数，空白区域和没有 marker 的 block 可能返回无效结果。

### `virtual int pageCount() const = 0`

返回当前布局的页数。对于连续滚动布局通常可以返回 `1`，但如果文档为空、布局定义了特殊分页或正在更新，派生类应定义一致的约定。

返回值必须和 `documentSize()`、绘制及分页命中策略保持一致。文档变化导致页数改变时应发 `pageCountChanged()`。

### `virtual QSizeF documentSize() const = 0`

返回文档在布局坐标中的总尺寸。它是逻辑尺寸，不是设备像素尺寸；设备 DPI 和 painter transform 不应被重复乘入，除非布局明确把它们纳入自己的排版策略。

返回尺寸不能随意为负。布局缓存更新后，如果尺寸发生变化，应发 `documentSizeChanged()`。

### `virtual QRectF frameBoundingRect(QTextFrame *frame) const = 0`

返回 frame 在文档坐标中的包围矩形。`QTextFrame` 由文档拥有，布局不应删除它。

必须处理根 frame 和嵌套 frame 的边界。对于未知或已脱离当前文档的 frame，应返回一致的无效/空矩形策略，而不是访问已失效缓存。

### `virtual QRectF blockBoundingRect(const QTextBlock &block) const = 0`

返回 block 的文档坐标包围矩形。矩形应覆盖派生布局认为属于该 block 的排版区域，通常包括行高和 block 间距，但具体是否包含列表标记、额外边距必须与 `draw()` 和 `hitTest()` 一致。

传入的 `QTextBlock` 只借用。若 block 不属于关联文档，返回值应有明确行为，不能把它当成当前文档中的合法 block。

### `void setPaintDevice(QPaintDevice *device)`

设置排版所依据的绘制设备。布局不拥有 `device`；设备必须在布局需要查询其 DPI、字体度量或进行相关计算时保持有效。

改变 paint device 可能改变字体度量、分页和文档尺寸。设置后派生实现通常需要重新排版，并在尺寸变化时发出信号。不要在设备已经销毁后继续让布局缓存依赖其属性。

### `QPaintDevice *paintDevice() const`

返回当前绘制设备指针，没有设置时返回 `nullptr`。返回指针不转移所有权，也不保证设备仍然适合绘制；调用者必须负责生命周期。

### `QTextDocument *document() const`

返回关联的文档指针。文档由外部拥有，不能通过该返回值推断布局拥有权。

### `void registerHandler(int objectType, QObject *component)`

为指定的文本对象类型注册对象处理器。`component` 通常同时实现 `QTextObjectInterface`，用于提供内嵌对象的尺寸和绘制。

注册不会把 `QObject` 的所有权转移给布局。处理器必须在布局使用期间有效；对象销毁前应先 `unregisterHandler()`。同一 `objectType` 的注册策略和重复注册行为应由应用保持明确，不要依赖不稳定的替换顺序。

### `void unregisterHandler(int objectType, QObject *component = nullptr)`

取消指定对象类型的处理器注册。传入 `component` 时可以限制只移除该组件；传入 `nullptr` 时按该类型移除当前处理器。

取消注册后，文档中的对应嵌入对象可能无法计算尺寸或绘制。若页面内容仍包含该对象，应同时触发受影响区域的重新布局或重绘。

### `QTextObjectInterface *handlerForObject(int objectType) const`

返回指定对象类型对应的处理器接口；没有注册处理器时返回 `nullptr`。返回接口指针不转移所有权，不能在外部删除。

调用者应确保返回对象仍然是有效的 `QObject`/接口实现，并且其线程亲和性与文档布局使用方式兼容。

## 7. 信号

### `void update(const QRectF &rect = QRectF(0., 0., 1000000000., 1000000000.))`

请求使用者重绘文档中的区域。默认矩形非常大，表示近似“需要更新全部可见内容”的通用请求，并不意味着布局真的拥有一个这么大的页面。

发射前应保证矩形使用布局约定的文档坐标。若使用者是滚动视图，还需要由视图把文档矩形映射到视口坐标。

### `void updateBlock(const QTextBlock &block)`

通知某个 block 的显示内容或几何发生变化。适合精确更新 block 相关控件。传递的 block 必须仍属于关联文档；文档结构变化后不要保存并复用已经失效的 block 值。

### `void documentSizeChanged(const QSizeF &newSize)`

通知总文档尺寸发生变化。滚动区域、打印预览或页面容器通常据此更新范围。只有尺寸语义确实改变时才应发射，避免在每次字符变化时无条件触发昂贵的滚动区域重算。

### `void pageCountChanged(int newPages)`

通知页数变化。分页预览、页码导航和打印 UI 可以据此更新。`newPages` 应与 `pageCount()` 返回值一致。

## 8. 保护 API

### `virtual void documentChanged(int from, int charsRemoved, int charsAdded) = 0`

文档内容变化时由 Qt 调用的纯虚入口。派生类必须更新排版状态。它是“内容变化通知”，不是可以主动调用来伪造文档编辑的公共 API。

在该函数中不要再次修改同一个文档，否则容易产生递归变化通知和缓存不一致。处理大文档时可以只重排受影响范围，并把后续 block 的位置增量平移。

### `virtual void resizeInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

为内嵌对象计算或调整尺寸。默认实现不做任何处理。`item` 是当前排版中的值对象，`posInDocument` 是对象在文档中的字符位置，`format` 描述对象格式。

如果派生布局支持自定义对象，应在这里设置宽度、高度和基线相关信息。不要把 `posInDocument` 当成像素坐标，也不要保存依赖临时排版过程的 `QTextInlineObject`。

### `virtual void positionInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

在内嵌对象已经得到尺寸后，把它定位到布局需要的位置。默认实现不做处理。它常用于根据行高、基线和对象对齐方式计算最终位置。

### `virtual void drawInlineObject(QPainter *painter, const QRectF &rect, QTextInlineObject object, int posInDocument, const QTextFormat &format)`

绘制内嵌对象。默认实现不做处理。`rect` 是布局计算的文档/绘制坐标矩形，具体坐标映射必须与 `draw()` 的 painter transform 约定一致。

不要保存 painter 或 object；如果对象由 `QTextObjectInterface` 处理，通常应把绘制委托给相应接口。

### `int formatIndex(int pos)`

根据文档位置查询内部格式索引。它是布局实现使用的保护辅助 API，返回值的具体索引含义由 Qt 的文本排版内部定义，不应把它当作 `QTextFormat::ObjectIndex` 或业务对象 ID。

只在派生布局需要复用 Qt 提供的格式查询路径时调用，并确保 `pos` 是关联文档中的有效字符位置。

### `QTextCharFormat format(int pos)`

根据文档位置取得字符格式快照。返回的是值类型，不是可写引用；修改返回值不会回写文档。无效位置应按空/无效格式处理。

它适合自定义布局在排版或命中测试时读取局部字符属性，不应替代对 `QTextCursor`、`QTextBlock` 和文档编辑 API 的正常使用。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `QAbstractTextDocumentLayout(QTextDocument *)` | 把布局关联到文档。 | 文档由外部拥有，必须保持有效。 |
| 生命周期 | `~QAbstractTextDocumentLayout()` | 销毁抽象布局。 | 不删除关联文档。 |
| 绘制 | `draw(QPainter *, const PaintContext &)` | 绘制文档内容。 | 纯虚；不保存 painter，不在绘制中修改文档。 |
| 命中 | `hitTest(QPointF, Qt::HitTestAccuracy)` | 点到字符位置的转换。 | 纯虚；找不到返回 `-1`，坐标约定必须一致。 |
| 查询 | `anchorAt(QPointF)` | 查询点处链接目标。 | 没有链接返回空字符串。 |
| 查询 | `imageAt(QPointF)` | 查询点处图片标识。 | 返回名称，不返回图像对象。 |
| 查询 | `formatAt(QPointF)` | 查询点处文本格式快照。 | 不修改文档。 |
| 查询 | `blockWithMarkerAt(QPointF)` | 查询点处的 marker block。 | 不是通用最近 block 查询。 |
| 几何 | `pageCount()` | 返回页数。 | 纯虚；须与分页和信号一致。 |
| 几何 | `documentSize()` | 返回总文档尺寸。 | 纯虚；是逻辑坐标尺寸。 |
| 几何 | `frameBoundingRect(QTextFrame *)` | 返回 frame 包围矩形。 | 纯虚；frame 由文档拥有。 |
| 几何 | `blockBoundingRect(QTextBlock)` | 返回 block 包围矩形。 | 纯虚；需和绘制、命中一致。 |
| 设备 | `setPaintDevice(QPaintDevice *)` | 设置排版参考设备。 | 非拥有指针；可能触发重新排版。 |
| 设备 | `paintDevice()` | 查询参考设备。 | 可能为 `nullptr`，不转移所有权。 |
| 文档 | `document()` | 返回关联文档。 | 返回非拥有指针。 |
| 对象 | `registerHandler(int, QObject *)` | 注册嵌入对象处理器。 | 不转移 QObject 所有权。 |
| 对象 | `unregisterHandler(int, QObject *)` | 移除对象处理器。 | 移除后需考虑重排和重绘。 |
| 对象 | `handlerForObject(int)` | 查询对象处理器接口。 | 可能返回 `nullptr`，不删除结果。 |
| 信号 | `update(QRectF)` | 请求局部或整体重绘。 | 矩形通常是文档坐标；空/大矩形需按约定解释。 |
| 信号 | `updateBlock(QTextBlock)` | 请求更新某个 block。 | block 必须仍属于当前文档。 |
| 信号 | `documentSizeChanged(QSizeF)` | 通知总尺寸改变。 | 参数应与 `documentSize()` 一致。 |
| 信号 | `pageCountChanged(int)` | 通知页数改变。 | 参数应与 `pageCount()` 一致。 |
| 保护 | `documentChanged(int, int, int)` | 处理文档内容变化。 | 纯虚；更新缓存，不要递归修改文档。 |
| 保护 | `resizeInlineObject(...)` | 计算嵌入对象尺寸。 | 默认空实现；位置参数是文档位置。 |
| 保护 | `positionInlineObject(...)` | 定位嵌入对象。 | 默认空实现；需和行基线一致。 |
| 保护 | `drawInlineObject(...)` | 绘制嵌入对象。 | 默认空实现；不保存 painter/object。 |
| 保护 | `formatIndex(int)` | 查询内部格式索引。 | 保护辅助 API，不是业务 ID。 |
| 保护 | `format(int)` | 查询字符格式快照。 | 返回值类型，不会回写文档。 |

### 一句话总结

`QAbstractTextDocumentLayout` 是 `QTextDocument` 的“排版后端”接口：派生类负责把文档变化变成几何缓存、绘制结果和命中测试，并用尺寸、页数和更新信号把变化传给控件；所有实现都必须先把文档坐标、绘制设备坐标和对象生命周期分清。
