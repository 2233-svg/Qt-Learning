# QAbstractTextDocumentLayout

> Qt 6.11.1 · Qt GUI · 来自 `QAbstractTextDocumentLayout`

## 1. 先建立直觉

`QAbstractTextDocumentLayout` 是 `QTextDocument` 的排版与绘制引擎接口。文档存储“字符、段落、格式、图片和嵌入对象”，布局负责回答另一个问题：它们在页面上究竟占多大空间、画在何处、鼠标坐标对应哪个字符位置。

普通富文本使用 Qt 的默认布局，不需要自己继承。只有在实现代码编辑器、分页渲染器、特殊标记语言、嵌入式公式/控件或自定义文档视图时，才需要直接面对这个类。

## 2. 类说明

- 头文件：`#include <QAbstractTextDocumentLayout>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承关系：`QObject`；构造时绑定一个 `QTextDocument`。
- 现成子类：`QPlainTextDocumentLayout`；富文本的默认布局通常由 Qt 自动管理。

派生布局的中心职责是响应 `documentChanged()`：重新计算受影响文本块的几何数据，再正确发出大小、页数和脏区域通知。只画出来而不更新这些信息，滚动条、命中测试和局部重绘都会失真。

## 3. API 速查

| API | 用途 |
|---|---|
| `document()` | 取得被排版的 `QTextDocument`。 |
| `documentChanged(pos, removed, added)` | 文本变化时的纯虚回调；派生类的排版入口。 |
| `documentSize()` / `pageCount()` | 返回总尺寸和页数。 |
| `blockBoundingRect(block)` | 查询一个段落块的几何矩形。 |
| `frameBoundingRect(frame)` | 查询一个文本框架的几何矩形。 |
| `draw(painter, context)` | 按绘制上下文渲染整篇文档。 |
| `hitTest(point, accuracy)` | 坐标映射到文档字符位置，失败返回 `-1`。 |
| `anchorAt()` / `imageAt()` / `formatAt()` | 按位置查询链接、图片源或文本格式。 |
| `registerHandler(type, object)` | 为嵌入对象类型注册 `QTextObjectInterface` 处理器。 |
| `setPaintDevice(device)` | 设定影响字体度量和布局的绘图设备。 |
| `documentSizeChanged` / `pageCountChanged` | 通知视图更新滚动范围或分页 UI。 |
| `update(rect)` / `updateBlock(block)` | 通知视图重绘受影响区域或段落。 |
| `PaintContext` | 描述裁剪区、默认颜色、光标与选择高亮。 |
| `Selection` | 描述一段应以特定格式高亮的文本范围。 |

## 4. 关键用法

### 使用现有布局绘制文档

```cpp
QAbstractTextDocumentLayout::PaintContext context;
context.clip = exposedRect;

QPainter painter(this);
painter.translate(-horizontalOffset, -verticalOffset);
document->documentLayout()->draw(&painter, context);
```

`draw()` 不会替你建立 `QPainter`，也不会自动处理滚动偏移。视图需要将 painter 坐标系与文档坐标系对齐，并让 `context.clip` 尽可能贴近实际脏区以减少复杂富文本的绘制开销。

### 处理链接点击和光标定位

```cpp
auto *layout = document->documentLayout();
const QString href = layout->anchorAt(documentPosition);
const int offset = layout->hitTest(documentPosition, Qt::FuzzyHit);
```

`anchorAt()` 返回空字符串并不意味着位置没有文本，只表示该位置不属于锚点。`hitTest()` 的 `ExactHit` 适合严格命中字符；`FuzzyHit` 更适合鼠标点击空白边缘时将光标落到最近合理位置。

### 注册自定义内联对象

```cpp
document->documentLayout()->registerHandler(
    MyInlineObjectType, myObjectHandler);
```

注册的对象由布局**不拥有**。处理器销毁前应先 `unregisterHandler()`，或者使用 QObject 生命周期关系保证布局不会保存悬空指针。一个对象类型只对应一个处理器，不要期待同类型对象各自注册不同 renderer。

## 5. 派生实现的工作清单

| 必须或关键步骤 | 原因 |
|---|---|
| 实现 `documentChanged()` | 识别受影响块并更新排版缓存。 |
| 实现 `documentSize()`、`pageCount()` | 视图据此配置滚动条与分页。 |
| 实现 `blockBoundingRect()`、`frameBoundingRect()` | 选择、滚动、命中测试依赖正确几何。 |
| 实现 `draw()`、`hitTest()` | 提供显示与交互的最小闭环。 |
| 尺寸变化时发射 `documentSizeChanged()` | 否则视图范围保持旧值。 |
| 页数变化时发射 `pageCountChanged()` | 否则页码 UI 会过期。 |
| 受影响内容上发射 `update()` / `updateBlock()` | 让视图局部重绘，而不是保留旧画面。 |
| 按需重写内联对象的 position/resize/draw | 支持图片以外的行内内容。 |

## 6. 常见坑与经验

- 不要把这个 API 当作 `QWidget::paintEvent()` 的替代品；它只管理文档排版，宿主视图仍负责视口、滚动和重绘调度。
- `setPaintDevice()` 会影响字体度量。屏幕、打印机和高 DPI 设备若混用同一份布局缓存，换页与换行位置可能变化。
- 文档修改可以很频繁。`documentChanged()` 应增量更新；每次都从头排完整篇大文档会使编辑器输入卡顿。
- `QTextBlock::layout()` 提供块级 `QTextLayout`，但块位置、页码和 frame 几何仍是布局类的职责。
- GUI 对象与绘制必须在 GUI 线程；后台可以准备文本数据，但不能并发改同一个 `QTextDocument`。

## 7. 知识点覆盖

- 文档模型与排版模型的分工
- 段落、文本框架与内联对象
- 文档坐标、绘图坐标和命中测试
- 脏区域重绘、滚动范围和分页通知
- 绘图设备、字体度量与高 DPI
- 自定义富文本布局的生命周期与性能策略
