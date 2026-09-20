# Qt QAbstractScrollArea 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QAbstractScrollArea>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QFrame -> QAbstractScrollArea`  
> 定位：自定义滚动视图的 viewport 与滚动条基础设施

## 1. QAbstractScrollArea 到底是什么

`QAbstractScrollArea` 是 Qt Widgets 滚动体系的底座。它提供 frame、viewport、水平/垂直滚动条、滚动条策略和事件转发，但它不知道“内容是什么、怎么画、滚动范围多大”。

```text
QAbstractScrollArea
  ├─ viewport              内容真正绘制、接收鼠标与滚轮事件的区域
  ├─ horizontalScrollBar
  ├─ verticalScrollBar
  ├─ cornerWidget          两根滚动条相交处的可选控件
  └─ scroll bar widgets    挂在滚动条两端的可选附属控件
```

名称里有 `Abstract`，但它不是 C++ 的纯抽象类，可以构造；只是直接构造得到的是没有内容逻辑的空滚动框。实际开发通常有三条路：

| 需求 | 应选类型 |
| --- | --- |
| 滚动一个已有 QWidget，例如长表单或图片 | `QScrollArea` |
| 显示大量项目或表格数据 | `QListView`、`QTableView`、`QTreeView` 等 `QAbstractItemView` |
| 自己绘制画布、时间轴、波形、无限/稀疏内容 | 继承 `QAbstractScrollArea` |

它解决的核心问题是把“内容坐标系”转换为“视口坐标系”。你负责内容尺寸与绘制，它负责可视区域和滚动条框架。

## 2. 自定义滚动区必须维护的四件事

继承后，不是重写一个 `paintEvent()` 就结束。每当内容大小或 viewport 大小变化时，你需要：

1. 计算水平、垂直滚动范围；
2. 设置每页步长（通常等于 viewport 宽高）；
3. 根据滚动条当前 value 在 viewport 中绘制正确区域；
4. 滚动条移动后刷新 viewport。

```text
content width  = 2000
viewport width =  600
horizontal range = [0, 1400]

viewport 左边显示的内容 x
  = horizontalScrollBar()->value()
```

默认 `Qt::ScrollBarAsNeeded` 下，只有滚动条存在非零可滚动范围时才显示。滚动条出现会挤占 viewport，viewport 变小又可能改变另一个方向的范围，因此更新逻辑必须基于当前 `viewport()->size()`，不能只用外层 widget 的 size。

## 3. 一个最小的自绘画布

下面的类显示一个 2000 x 1200 的逻辑画布。它没有创建一个同样大的 child widget，而是直接在 viewport 上绘制；这正是选择 `QAbstractScrollArea` 的典型理由。

```cpp
#include <QAbstractScrollArea>
#include <QPainter>
#include <QResizeEvent>
#include <QScrollBar>

class CanvasArea final : public QAbstractScrollArea
{
public:
    explicit CanvasArea(QWidget *parent = nullptr)
        : QAbstractScrollArea(parent)
    {
        updateScrollBars();
    }

protected:
    void paintEvent(QPaintEvent *event) override
    {
        QPainter painter(viewport());
        painter.fillRect(event->rect(), Qt::white);

        painter.translate(-horizontalScrollBar()->value(),
                          -verticalScrollBar()->value());
        painter.setPen(Qt::darkGray);
        painter.drawRect(QRect(0, 0, m_contentSize.width() - 1,
                               m_contentSize.height() - 1));
        painter.drawText(QPoint(40, 60), "内容坐标 (40, 60)");
    }

    void resizeEvent(QResizeEvent *event) override
    {
        QAbstractScrollArea::resizeEvent(event);
        updateScrollBars();
    }

    void scrollContentsBy(int dx, int dy) override
    {
        Q_UNUSED(dx);
        Q_UNUSED(dy);
        viewport()->update();
    }

private:
    void updateScrollBars()
    {
        const QSize pageSize = viewport()->size();

        horizontalScrollBar()->setPageStep(pageSize.width());
        horizontalScrollBar()->setRange(
            0, qMax(0, m_contentSize.width() - pageSize.width()));

        verticalScrollBar()->setPageStep(pageSize.height());
        verticalScrollBar()->setRange(
            0, qMax(0, m_contentSize.height() - pageSize.height()));
    }

    QSize m_contentSize = QSize(2000, 1200);
};
```

`paintEvent()` 中的 `QPainter` 必须绘制到 `viewport()`，不是 `this`。`QAbstractScrollArea` 会把与 viewport 对应的鼠标、滚轮、绘制和 resize 事件路由到适当的处理函数。

这里的 `scrollContentsBy()` 没有手动移动像素，而是刷新 viewport 后按照新的 scroll bar value 重画。对于复杂画布这通常足够清晰；若要优化平移，可利用 `dx`、`dy` 做像素滚动。不要为了编程滚动而直接调用 `scrollContentsBy()`，应设置 `horizontalScrollBar()->setValue()` 或 `verticalScrollBar()->setValue()`。

## 4. viewport 不是 content widget

`viewport()` 是 QAbstractScrollArea 的内部可视窗口，返回一个 QWidget。它并不等于 `QScrollArea::widget()`：

```text
QScrollArea
  └─ QAbstractScrollArea::viewport()
       └─ QScrollArea::widget()   // QScrollArea 的内容根控件
```

在 `QAbstractScrollArea` 子类中有两种内容策略：

- **自绘内容**：像上例那样，在 `paintEvent()` 用滚动条 value 平移坐标系。这适合稀疏、超大或无限内容。
- **移动 child widget**：把一个大 widget 设为 viewport 的 child，在 `scrollContentsBy()` 中把它移动到 `(-hValue, -vValue)`。`QScrollArea` 已经替你实现了这种平滑像素滚动。

当你希望替换 viewport 本身，例如为其设置特殊 OpenGL、事件过滤或绘制能力，可以调用 `setViewport(customViewport)`。该函数接管 viewport 所有权；传 `nullptr` 时 QAbstractScrollArea 会创建一个新的普通 QWidget。`setupViewport()` 会在新 viewport 设置后被调用，是初始化新 viewport 的扩展点。

## 5. 滚动条：范围、page step、策略与替换

```cpp
auto *hbar = horizontalScrollBar();
auto *vbar = verticalScrollBar();

hbar->setRange(0, maxX);
hbar->setPageStep(viewport()->width());
hbar->setSingleStep(20);

setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOn);
```

- `range` 表示内容可滚动的范围，通常从 `0` 到 `max(0, contentSize - viewportSize)`。
- `pageStep` 是 PageUp/PageDown 或滑块页跳的距离，通常用 viewport 尺寸。
- `singleStep` 是方向键、滚轮等小步距离，按内容单位设定。
- `ScrollBarAsNeeded` 是横、纵策略的默认值；无有效范围时滚动条隐藏，viewport 会扩展。

可以替换 Qt 默认滚动条：

```cpp
setVerticalScrollBar(new QScrollBar(Qt::Vertical));
```

`setVerticalScrollBar()` / `setHorizontalScrollBar()` 会把旧滚动条的 slider 属性复制到新滚动条后删除旧对象。只有确实需要自定义 `QScrollBar` 子类时才替换，不要保存旧滚动条指针。

`maximumViewportSize()` 返回“假设两根滚动条均没有有效滚动范围”时 viewport 能达到的最大尺寸，适合在布局计算中判断是否可能无需滚动条。

## 6. viewport 边距、角控件与滚动条附属控件

`setViewportMargins()` 是自定义标题行、冻结行列或标尺的基础。它从 viewport 周围预留空白，而不是给内容增加 padding：

```text
+----------------------------------------+
| 固定标题区域（top viewport margin）     |
+------+---------------------------------+
| 固定 | viewport                         |
| 列   |                                 |
+------+---------------------------------+
```

它是保护函数，只能在子类内部调用：

```cpp
setViewportMargins(48, 24, 0, 0);
```

随后你要自己把标尺、header 等控件放进预留区域，并在 resize 时安排它们的 geometry。`QTableView`、`QTreeView` 等 item view 频繁使用这个机制；如果你的类还要作为它们的子类基础，不应随意调用它。

另外两组 public API 用于滚动条周围的小控件：

- `setCornerWidget()`：设置两根滚动条交叉处的控件。替换前一个角控件会隐藏前者；被设置的角控件会由 scroll area 销毁，除非之后 reparent。
- `addScrollBarWidget()`：把控件放在横向滚动条左/右，或纵向滚动条上/下。要始终可见，相关滚动条策略通常要设为 `AlwaysOn`。

滚动条附属控件会根据 style 的滚动条几何自动调整厚度；例如挂在横向滚动条上的控件，高度会匹配该滚动条。

## 7. 事件路由：重写哪个函数

viewport 收到的事件并不需要你安装一串 event filter。QAbstractScrollArea 会把常见 QWidget 专用事件映射到 viewport：

| 需求 | 推荐重写 |
| --- | --- |
| 在内容区域绘制 | `paintEvent()`，`QPainter(viewport())` |
| 鼠标拖拽、框选、点击 | `mousePressEvent()`、`mouseMoveEvent()`、`mouseReleaseEvent()` |
| 滚轮缩放或自定义滚动 | `wheelEvent()` |
| 拖放数据 | `dragEnterEvent()`、`dragMoveEvent()`、`dragLeaveEvent()`、`dropEvent()` |
| 内容区域右键菜单 | `contextMenuEvent()` |
| viewport 尺寸变化，重算 range | `resizeEvent()` |
| 统一截获 viewport 事件 | `viewportEvent()`，但优先使用上面的专用函数 |

`event()` 处理的是外层 `QAbstractScrollArea` widget 自身的普通事件，不是 viewport 绘制区域。`keyPressEvent()` 默认处理 `PageUp`、`PageDown`、方向键并忽略其他按键；自定义快捷键时应让未处理按键继续交给基类或上层逻辑。

## 8. 大小提示策略

`SizeAdjustPolicy` 描述 scroll area 的 size hint 随 viewport 变化怎样调整：

| 策略 | 行为 | 注意点 |
| --- | --- | --- |
| `AdjustIgnored` | 不自动调整。默认值。 | 最可预测，适合多数可伸缩主界面。 |
| `AdjustToContents` | 总是按 viewport 调整。 | 修改后可能实际改变 scroll area 尺寸。 |
| `AdjustToContentsOnFirstShow` | 第一次显示时按 viewport 调整。 | 适合首次展示时希望贴合内容的浮动面板。 |

`sizeHint()` 以 `viewportSizeHint()` 为基础，必要时再加上滚动条所需空间；`viewportSizeHint()` 默认取 viewport 的 size hint，不包括滚动条。自定义视图应根据实际内容给出稳定、合理的 size hint，而不是在绘制函数里随意改变窗口尺寸。

## API 速查表
下表按 Qt 6.11.1 的 `qabstractscrollarea.h` 直接声明整理。读表时先分清“外层 scroll area”“viewport”“滚动条”三个对象，很多错误都是把事件或绘制目标放错对象造成的。

### 9.1 类型、策略与基础结构

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAbstractScrollArea(QWidget *parent = nullptr)` | 创建带 frame、viewport 和两根滚动条的滚动区基类 | 可以实例化，但没有内容逻辑；通常由子类或 `QScrollArea` / item view 使用 |
| 生命周期 | `~QAbstractScrollArea()` | 销毁滚动区及其管理的 viewport、滚动条附属对象 | 自己持有的内容数据仍按你的所有权规则释放 |
| 枚举 | `AdjustIgnored` | size hint 不随 viewport 内容自动调整 | 默认值，适合主窗口中可伸缩的滚动区域 |
| 枚举 | `AdjustToContentsOnFirstShow` | 第一次显示时按内容调整 size hint | 适合初始贴合内容，之后交给布局管理 |
| 枚举 | `AdjustToContents` | 每次都尽量按内容调整 size hint | 内容变化频繁时可能引发布局抖动 |
| 尺寸策略 | `sizeAdjustPolicy() const` | 读取 size hint 调整策略 | 判断当前 scroll area 是否会随内容重新给出尺寸建议 |
| 尺寸策略 | `setSizeAdjustPolicy(SizeAdjustPolicy policy)` | 设置 size hint 调整策略 | 策略改变后可能影响外层布局给它的尺寸 |
| 尺寸 | `minimumSizeHint() const` | 返回最小推荐尺寸 | 给布局协商使用，不是强制不可压缩边界 |
| 尺寸 | `sizeHint() const` | 返回整个 scroll area 推荐尺寸 | 包括 frame、viewport hint 以及可能的滚动条空间 |
| 尺寸 | `maximumViewportSize() const` | 返回无滚动条有效范围时 viewport 可达到的最大尺寸 | 用于判断理想情况下内容可见区域，而不是当前 viewport 尺寸 |

### 9.2 滚动条与附属控件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 垂直滚动条 | `verticalScrollBarPolicy() const` | 读取垂直滚动条显示策略 | 默认通常是 `Qt::ScrollBarAsNeeded` |
| 垂直滚动条 | `setVerticalScrollBarPolicy(Qt::ScrollBarPolicy policy)` | 设置垂直滚动条显示策略 | `AlwaysOn` 可稳定 viewport 宽度，`AlwaysOff` 会禁用视觉滚动入口 |
| 垂直滚动条 | `verticalScrollBar() const` | 返回垂直 `QScrollBar` | 自定义内容尺寸变化后设置 range、value、pageStep |
| 垂直滚动条 | `setVerticalScrollBar(QScrollBar *scrollbar)` | 替换垂直滚动条对象 | 旧滚动条会被删除；不要继续保存旧指针 |
| 水平滚动条 | `horizontalScrollBarPolicy() const` | 读取水平滚动条显示策略 | 策略影响 viewport 高度 |
| 水平滚动条 | `setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy policy)` | 设置水平滚动条显示策略 | 滚动条出现/隐藏会改变 viewport 尺寸，需要重新计算范围 |
| 水平滚动条 | `horizontalScrollBar() const` | 返回水平 `QScrollBar` | 内容宽度大于 viewport 宽度时设置有效范围 |
| 水平滚动条 | `setHorizontalScrollBar(QScrollBar *scrollbar)` | 替换水平滚动条对象 | 仅在需要自定义滚动条子类时使用 |
| 角控件 | `cornerWidget() const` | 返回两根滚动条交叉处的控件 | 默认没有角控件 |
| 角控件 | `setCornerWidget(QWidget *widget)` | 设置或移除角控件 | 被设置的控件由 scroll area 管理；替换旧角控件时留意旧对象状态 |
| 附属控件 | `addScrollBarWidget(QWidget *widget, Qt::Alignment alignment)` | 在滚动条旁添加小控件 | `AlignLeft/Right` 对应水平滚动条，`AlignTop/Bottom` 对应垂直滚动条 |
| 附属控件 | `scrollBarWidgets(Qt::Alignment alignment)` | 查询某个方位上的滚动条附属控件 | 返回的是当前列表；不要用它替代布局管理 |

### 9.3 viewport 与边距

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| viewport | `viewport() const` | 返回真正显示内容、接收多数鼠标/绘制事件的子控件 | 自绘 `QPainter` 目标应是 `viewport()`，不是 `this` |
| viewport | `setViewport(QWidget *widget)` | 替换 viewport，并让 scroll area 接管它 | 传空指针时会创建普通 QWidget；替换后旧 viewport 生命周期由框架处理 |
| viewport | `setupViewport(QWidget *viewport)` | 新 viewport 安装后的初始化钩子 | 子类可设置属性、背景、事件策略或 OpenGL 相关 viewport |
| 边距 | `setViewportMargins(int left, int top, int right, int bottom)` | 在 viewport 四周预留固定区域 | 受保护函数；常用于固定 header、标尺、冻结区域 |
| 边距 | `setViewportMargins(const QMargins &margins)` | 用 `QMargins` 设置 viewport 预留区域 | 只预留空间，不会自动放置控件 |
| 边距 | `viewportMargins() const` | 读取当前 viewport 边距 | 子类布局 header/标尺时使用 |
| 尺寸 | `viewportSizeHint() const` | 返回 viewport 本身的推荐尺寸 | 受保护虚函数；自定义内容大小时可重写 |
| 派生构造 | `QAbstractScrollArea(QAbstractScrollAreaPrivate &dd, QWidget *parent = nullptr)` | 供 Qt 内部派生类传入私有实现 | 普通子类使用公开构造函数 |

### 9.4 滚动、绘制与事件扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件过滤 | `eventFilter(QObject *, QEvent *)` | 过滤相关内部对象事件 | 框架内部会用于 viewport/滚动条协调；子类重写需谨慎保留基类行为 |
| 事件 | `event(QEvent *)` | 处理外层 scroll area 的通用事件 | 不等于 viewport 内容区域事件 |
| viewport 事件 | `viewportEvent(QEvent *)` | 处理 viewport 的统一事件入口 | 能用专用事件函数时优先重写专用函数 |
| 尺寸事件 | `resizeEvent(QResizeEvent *)` | 处理滚动区和 viewport 尺寸变化 | 自定义内容必须在这里重算滚动范围和 page step |
| 绘制事件 | `paintEvent(QPaintEvent *)` | 绘制 viewport 内容 | `QPainter painter(viewport())`；坐标通常要减去滚动条 value |
| 鼠标 | `mousePressEvent(QMouseEvent *)` | 处理 viewport 鼠标按下 | 适合选择、拖动画布、记录起点 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *)` | 处理 viewport 鼠标释放 | 结束拖动、选择或手势 |
| 鼠标 | `mouseDoubleClickEvent(QMouseEvent *)` | 处理 viewport 双击 | 打开项目、重置缩放等 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *)` | 处理 viewport 鼠标移动 | 拖动、框选、悬停反馈 |
| 滚轮 | `wheelEvent(QWheelEvent *)` | 处理 viewport 滚轮事件 | 自定义缩放时要决定是否仍滚动内容 |
| 菜单 | `contextMenuEvent(QContextMenuEvent *)` | 处理 viewport 右键菜单 | 通常要把位置换算到内容坐标 |
| 拖放 | `dragEnterEvent(QDragEnterEvent *)` | 数据拖入 viewport 时触发 | 先检查 MIME 类型再接受 |
| 拖放 | `dragMoveEvent(QDragMoveEvent *)` | 拖放在 viewport 中移动时触发 | 更新投放位置反馈 |
| 拖放 | `dragLeaveEvent(QDragLeaveEvent *)` | 拖放离开 viewport 时触发 | 清除高亮和临时状态 |
| 拖放 | `dropEvent(QDropEvent *)` | 数据在 viewport 中放下时触发 | 将 viewport 坐标转换为内容坐标 |
| 键盘 | `keyPressEvent(QKeyEvent *)` | 处理键盘滚动和快捷键 | 基类处理方向键/Page 键；未处理按键应继续传播 |
| 滚动 | `scrollContentsBy(int dx, int dy)` | 滚动条 value 改变后通知内容滚动 | 不要直接调用它来滚动；设置滚动条 value |
