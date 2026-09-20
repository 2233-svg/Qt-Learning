# Qt QGraphicsTextItem 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGraphicsTextItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QGraphicsObject -> QGraphicsTextItem`  
> 定位：场景文本项

## 1. QGraphicsTextItem 解决什么问题

`QGraphicsTextItem` 是 Graphics View 里的文本项。它把文本内容放进 `QGraphicsScene`，既能显示富文本，也能参与场景中的移动、缩放、旋转和事件分发。

它常见于：

- 流程图节点标题；
- 图形化标注；
- 画布上的说明文字；
- 需要在场景中直接编辑的文本。

它和 `QPlainTextEdit`、`QTextEdit` 不一样。后两者是 Widgets 控件，强调输入和编辑界面；`QGraphicsTextItem` 强调的是“文本作为场景中的一个图元”。

```text
QGraphicsItem
  └─ QGraphicsObject
       └─ QGraphicsTextItem
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 把文本项放进场景

```cpp
#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsTextItem>
#include <QGraphicsView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QGraphicsScene scene;
    auto *textItem = scene.addText("Hello <b>Graphics View</b>");
    textItem->setPos(40, 40);

    QGraphicsView view(&scene);
    view.resize(640, 420);
    view.show();

    return app.exec();
}
```

### 2.3 让文本可编辑

```cpp
textItem->setTextInteractionFlags(Qt::TextEditorInteraction);
textItem->setOpenExternalLinks(true);
```

当文本需要输入、选中、复制或链接点击时，这些交互标志就很重要。

## 3. 核心使用模型

### 3.1 它的文本内容来自 QTextDocument

`QGraphicsTextItem` 内部依赖 `QTextDocument` 管理文本内容、格式和光标状态。你可以直接用 `setHtml()`、`setPlainText()`，也可以取出 `document()` 继续做更细的排版控制。

### 3.2 它既是图元，也是文本编辑器承载体

当只做显示时，它就是一个文本图元；当开启文本交互时，它又能像一个小编辑器一样处理键盘、鼠标、输入法和选择。

### 3.3 文本宽度会影响换行和尺寸

`setTextWidth()` 决定文本项的换行宽度，进而影响 `boundingRect()` 和 `sizeHint()`。做画布标注时，这个参数通常比你想的更重要。

### 3.4 链接和外部打开

如果文本里有链接，可以通过 `linkActivated`、`linkHovered` 监听交互，也可以用 `setOpenExternalLinks(true)` 让外部链接直接打开。

## 4. 适合用在哪里

- 画布上的富文本标签；
- 节点标题和说明；
- 场景里的可编辑注释；
- 需要少量文本交互但不想放一个完整 QWidget 的地方。

如果只是普通窗体里的文本输入，还是用 `QLineEdit`、`QTextEdit` 更合适。

## 5. 常见误区

### 5.1 把它当成普通 QWidget 文本控件

它是图元，不是控件。它的几何、变换和事件都遵循 Graphics View 规则。

### 5.2 忽略 textWidth

不设宽度时，富文本换行和尺寸计算很容易和你预期不同。

### 5.3 把 document() 当成可随便替换的普通对象

可以替换，但要清楚替换后文本、格式和光标状态会跟着变。不要在不理解的情况下直接改文档对象。

### 5.4 以为 openExternalLinks 会自动处理所有链接逻辑

它只负责自动打开外部链接。更复杂的链接跳转逻辑还是要自己接信号处理。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsTextItem(QGraphicsItem *parent = nullptr)` | 创建空文本项。 | 常和 `setPlainText()` 或 `setHtml()` 配套。 |
| 构造 | `QGraphicsTextItem(const QString &text, QGraphicsItem *parent = nullptr)` | 创建并初始化文本内容。 | 适合直接显示初始文本。 |
| 析构 | `~QGraphicsTextItem()` | 销毁文本项。 | 作为图元时由场景和对象树协同管理。 |
| 内容 | `setHtml(const QString &html)` | 以 HTML/富文本方式设置内容。 | 适合格式化文本。 |
| 内容 | `toHtml() const` | 取出当前内容的 HTML 表示。 | 结果是文档序列化形式，不一定适合直接做业务存储。 |
| 内容 | `setPlainText(const QString &text)` | 以纯文本方式设置内容。 | 会清掉富文本格式。 |
| 内容 | `toPlainText() const` | 取出当前纯文本内容。 | 适合搜索、日志和数据提取。 |
| 字体 | `setFont(const QFont &font)` | 设置文本字体。 | 影响文本渲染和尺寸。 |
| 字体 | `font() const` | 读取当前文本字体。 | 返回的是项使用的字体。 |
| 颜色 | `setDefaultTextColor(const QColor &c)` | 设置默认文字颜色。 | 只影响默认文本颜色，不等于所有格式都被改掉。 |
| 颜色 | `defaultTextColor() const` | 读取默认文字颜色。 | 用于恢复或检查当前颜色。 |
| 宽度 | `setTextWidth(qreal width)` | 设置文本换行宽度。 | 影响换行、包围盒和布局。 |
| 宽度 | `textWidth() const` | 读取文本换行宽度。 | 便于同步画布布局。 |
| 尺寸 | `adjustSize()` | 根据当前内容自动调整文本项尺寸。 | 内容变化后用于重新收紧包围盒。 |
| 文档 | `setDocument(QTextDocument *document)` | 替换底层文档对象。 | 替换前要考虑内容、格式和生命周期。 |
| 文档 | `document() const` | 返回当前底层文档对象。 | 可以继续做更细排版控制。 |
| 交互 | `setTextInteractionFlags(Qt::TextInteractionFlags flags)` | 设置文本是否可选中、可编辑、可链接操作。 | 交互能力由这些标志决定。 |
| 交互 | `textInteractionFlags() const` | 读取当前文本交互标志。 | 可用来检查是否处于编辑状态。 |
| 交互 | `setTabChangesFocus(bool b)` | 设置 Tab 是插入字符还是切换焦点。 | 纯文本编辑里很常见。 |
| 交互 | `tabChangesFocus() const` | 读取 Tab 行为设置。 | 与焦点导航配套。 |
| 链接 | `setOpenExternalLinks(bool open)` | 设置是否自动打开外部链接。 | 适合文档浏览场景。 |
| 链接 | `openExternalLinks() const` | 读取是否自动打开外部链接。 | 和链接点击事件一起看。 |
| 光标 | `setTextCursor(const QTextCursor &cursor)` | 设置当前文本光标。 | 常用于编辑定位。 |
| 光标 | `textCursor() const` | 读取当前文本光标。 | 可拿到选区和当前位置。 |
| 尺寸/几何 | `boundingRect() const` | 返回文本项的绘制边界。 | 布局和重绘依赖它。 |
| 命中 | `shape() const` | 返回文本项的命中路径。 | 影响点击和碰撞检测。 |
| 命中 | `contains(const QPointF &point) const` | 判断点是否落在文本项内。 | 和 shape/boundingRect 配合。 |
| 绘制 | `paint(QPainter *, const QStyleOptionGraphicsItem *, QWidget *)` | 绘制文本项。 | 通常由框架调用。 |
| 事件 | `sceneEvent(QEvent *event)` | 处理场景事件总入口。 | 编辑、选择、链接和输入法都可能经过这里。 |
| 事件 | `mousePressEvent(...)` / `mouseMoveEvent(...)` / `mouseReleaseEvent(...)` | 处理鼠标交互。 | 影响选中、拖拽和编辑。 |
| 事件 | `mouseDoubleClickEvent(...)` | 处理双击。 | 常用于编辑或选择词语。 |
| 事件 | `contextMenuEvent(...)` | 处理右键菜单。 | 可做复制、选择和链接菜单。 |
| 事件 | `keyPressEvent(...)` / `keyReleaseEvent(...)` | 处理键盘输入。 | 编辑模式下尤其关键。 |
| 事件 | `focusInEvent(...)` / `focusOutEvent(...)` | 处理焦点进入和离开。 | 编辑状态切换常依赖它。 |
| 事件 | `dragEnterEvent(...)` / `dragLeaveEvent(...)` / `dragMoveEvent(...)` / `dropEvent(...)` | 处理拖放。 | 适合文本拖入或拖出。 |
| 事件 | `inputMethodEvent(...)` | 处理输入法组合输入。 | 中文输入必须正确支持。 |
| 悬停 | `hoverEnterEvent(...)` / `hoverMoveEvent(...)` / `hoverLeaveEvent(...)` | 处理鼠标悬停。 | 适合链接高亮。 |
| 查询 | `inputMethodQuery(Qt::InputMethodQuery query) const` | 给输入法查询光标、选区等信息。 | 文本编辑体验依赖它。 |
| 信号 | `linkActivated(const QString &)` | 链接被激活时发出。 | 用于跳转或打开目标。 |
| 信号 | `linkHovered(const QString &)` | 鼠标悬停在链接上时发出。 | 可用于状态栏提示。 |

## 7. 一句话总结

`QGraphicsTextItem` 是场景中的文本图元，适合富文本展示、链接交互和少量编辑，核心是围绕 `QTextDocument` 工作，而不是围绕普通 Widgets 文本控件工作。
