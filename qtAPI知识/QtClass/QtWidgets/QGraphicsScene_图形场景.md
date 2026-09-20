# Qt QGraphicsScene 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QGraphicsScene>`
> 所属模块：`Qt6::Widgets`
> 继承：`QObject -> QGraphicsScene`
> 常见搭档：`QGraphicsView`、`QGraphicsItem`、`QGraphicsWidget`

## 1. QGraphicsScene 解决什么问题

`QGraphicsScene` 是图形视图架构里的“场景容器”。它负责管理一批 `QGraphicsItem`，并为视图提供可渲染、可选择、可碰撞检测、可接收事件的场景数据。

如果说 `QGraphicsView` 是“看图的窗口”，那 `QGraphicsScene` 就是“图本身的世界”。

适合场景：

- 自定义图形编辑器；
- 节点图、关系图、流程图；
- 带大量图元的可缩放画布；
- 需要 item 级别碰撞、选区、拖拽和焦点处理的界面。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QGraphicsScene scene;
    scene.addEllipse(QRectF(0, 0, 100, 100));
    scene.addText("Hello, scene");
    scene.setSceneRect(-50, -50, 300, 200);

    QGraphicsView view(&scene);
    view.show();

    return app.exec();
}
```

`QGraphicsScene` 自己不显示东西；必须交给 `QGraphicsView` 才能看见。

## 3. item 是场景的核心

### 3.1 addItem

```cpp
auto *item = new QGraphicsRectItem(QRectF(0, 0, 80, 40));
scene.addItem(item);
```

`addItem()` 会把 item 和它的子 item 一起加入场景，并且 **场景接管这个 item 的所有权**。

### 3.2 便利创建函数

```cpp
scene.addEllipse(...);
scene.addLine(...);
scene.addPath(...);
scene.addPixmap(...);
scene.addRect(...);
scene.addText(...);
scene.addSimpleText(...);
scene.addWidget(new QPushButton("OK"));
```

这些函数会直接创建 item 并返回指针，适合快速搭场景。

`addWidget()` 会把普通 `QWidget` 包装成 `QGraphicsProxyWidget`，适合在场景里嵌一个真正控件。

### 3.3 removeItem

```cpp
scene.removeItem(item);
delete item;
```

`removeItem()` 只把 item 从场景移除，**不会替你 delete**。  
移除后，所有权回到调用方。

这点和 `addItem()` 正好相反，写动态图元时一定别忘了。

## 4. 场景范围、索引和渲染

```cpp
scene.setSceneRect(-1000, -1000, 2000, 2000);
scene.setItemIndexMethod(QGraphicsScene::BspTreeIndex);
scene.setMinimumRenderSize(1.0);
```

### 4.1 sceneRect

`sceneRect` 是场景的逻辑边界。  
不设时，Qt 可能根据 `itemsBoundingRect()` 推断，但对大场景来说这很贵。

### 4.2 itemIndexMethod

```cpp
scene.setItemIndexMethod(QGraphicsScene::BspTreeIndex);
scene.setBspTreeDepth(8);
```

默认用 BSP 树，适合大场景、静态 item 较多的情况。  
如果 item 经常移动，索引开销和收益要自己权衡。

### 4.3 minimumRenderSize

当 item 缩得太小时可以不绘制它，适合大缩放场景。  
但注意：没画出来不代表没参与碰撞或交互。

## 5. 选择、焦点和活动窗口

```cpp
scene.setSelectionArea(path);
scene.clearSelection();
auto items = scene.selectedItems();
```

`selectionArea` 是场景级选区，适合框选和套索选择。

```cpp
scene.setFocusItem(item);
scene.setActivePanel(item);
scene.setActiveWindow(widget);
```

`focusItemChanged()`、`sceneRectChanged()`、`selectionChanged()` 是做状态同步最常用的信号。

`focusOnTouch` 会影响触摸设备上的焦点行为，偏交互型应用时要留意。

## 6. 和视图协作

`QGraphicsScene` 可以挂多个 `QGraphicsView`：

```cpp
QList<QGraphicsView *> views = scene.views();
```

一个场景可以被多个视图同时显示，每个视图可以有不同缩放、滚动和绘制策略。

场景自身也能渲染到 `QPainter`：

```cpp
scene.render(&painter);
```

这在导出图片、打印或离屏绘制时很方便。

## 7. 常用协作函数

```cpp
scene.update();
scene.invalidate();
scene.clear();
```

- `update()`：通知需要重绘；
- `invalidate()`：让某些层失效，通常和自定义背景/前景有关；
- `clear()`：清空场景里的所有 item。

`clear()` 会删除场景中的 item，所以它不是“只清空选择”，而是彻底清空内容。

## API 速查表
### 8.1 类型、构造和场景范围

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `ItemIndexMethod` | 指定场景如何建立 item 索引，目前主要是 `BspTreeIndex` 和 `NoIndex`。 | 静态大场景通常受益于 BSP；item 频繁移动时要评估维护索引的成本。 |
| 类型 | `SceneLayer` / `SceneLayers` | 表示 item、背景和前景这些可失效或刷新的场景层。 | `SceneLayers` 是 flags，使用 `|` 组合多个层。 |
| 构造 | `QGraphicsScene(QObject *parent = nullptr)` | 创建一个没有显式场景矩形的场景。 | 场景本身不显示，仍需交给 `QGraphicsView`。 |
| 构造 | `QGraphicsScene(const QRectF &sceneRect, QObject *parent = nullptr)` | 创建场景并立即指定逻辑边界。 | 适合需要稳定坐标范围的画布。 |
| 构造 | `QGraphicsScene(qreal x, qreal y, qreal width, qreal height, QObject *parent = nullptr)` | 用四个数值指定场景矩形。 | 与 `QRectF` 构造函数作用相同，只是写法更直接。 |
| 析构 | `~QGraphicsScene()` | 销毁场景及其管理的图元。 | 已经加入场景的 item 不要再由外部重复 `delete`。 |
| 范围 | `sceneRect()` / `setSceneRect(...)` | 读取或设置场景的逻辑坐标边界。 | 不设置时可能根据 item 的外接矩形推导；大场景建议显式设置。 |
| 范围 | `width()` / `height()` | 读取当前场景矩形的宽和高。 | 它们只是 `sceneRect()` 的便捷访问器，不是视口像素尺寸。 |
| 范围 | `itemsBoundingRect()` | 计算所有 item 的联合外接矩形。 | 适合自动适配内容，但大量 item 时可能较昂贵。 |
| 索引 | `itemIndexMethod()` / `setItemIndexMethod(...)` | 读取或设置 item 索引方式。 | `NoIndex` 适合动态场景或小场景；不是“关闭绘制”。 |
| 索引 | `bspTreeDepth()` / `setBspTreeDepth(int)` | 读取或设置 BSP 树深度。 | 只在 BSP 索引下有意义；深度过大不一定更快。 |

### 8.2 查找、碰撞、选择和分组

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查找 | `items(...)` | 按场景坐标中的点、矩形、多边形或路径查找图元，也可以返回全部图元。 | `Qt::ItemSelectionMode` 决定按形状还是包围矩形判断；返回顺序受 `Qt::SortOrder` 影响。 |
| 查找 | `itemAt(const QPointF &, const QTransform &)` | 返回指定场景位置最上层的图元。 | 设备变换会影响精确命中；从视图点击时通常先用 `QGraphicsView::mapToScene()`。 |
| 碰撞 | `collidingItems(const QGraphicsItem *, Qt::ItemSelectionMode)` | 查找与指定 item 相交的其他 item。 | 依赖 item 的 `shape()` 或 `boundingRect()` 选择模式；不等于物理引擎碰撞。 |
| 选择 | `selectedItems()` | 返回当前被选中的图元列表。 | item 必须设置可选标志；返回的是当前状态快照。 |
| 选择 | `selectionArea()` | 读取当前场景的选择路径。 | 适合保存或显示自定义套索区域。 |
| 选择 | `setSelectionArea(const QPainterPath &, ...)` | 用路径设置、追加或反选图元。 | 要明确选择操作、命中模式和设备变换，否则框选结果可能与预期不同。 |
| 选择 | `clearSelection()` | 清除所有 item 的选中状态。 | 只改选择状态，不删除任何图元。 |
| 分组 | `createItemGroup(const QList<QGraphicsItem *> &)` | 创建一个 item 组，把多个图元放到统一的父组下。 | 分组会改变 item 父子关系和坐标层级，适合整体移动、缩放。 |
| 分组 | `destroyItemGroup(QGraphicsItemGroup *)` | 解散 item 组并恢复组内图元。 | 解散的是层级关系，不是删除组内图元；组对象本身由场景处理。 |

### 8.3 图元增删和对象所有权

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 加入 | `addItem(QGraphicsItem *)` | 把已有图元加入场景，并递归纳入其子图元。 | 场景接管 item 的场景归属和最终销毁；同一个 item 不能同时属于两个场景。 |
| 创建 | `addEllipse(...)` | 创建并加入椭圆图元。 | 返回新建的 `QGraphicsEllipseItem *`，可继续设置位置、标志和数据。 |
| 创建 | `addLine(...)` | 创建并加入线段图元。 | 只适合简单线段；复杂连接线通常应自定义 `QGraphicsPathItem`。 |
| 创建 | `addPath(...)` | 创建并加入路径图元。 | 适合折线、曲线、复杂轮廓和自定义形状。 |
| 创建 | `addPixmap(...)` | 创建并加入像素图图元。 | 大量图片时要关注纹理尺寸、缓存和缩放质量。 |
| 创建 | `addPolygon(...)` | 创建并加入多边形图元。 | 适合规则或不规则多边形，但不提供复杂编辑器行为。 |
| 创建 | `addRect(...)` | 创建并加入矩形图元。 | 常用于节点背景、选区框和简单标注。 |
| 创建 | `addText(...)` | 创建可编辑、可设置字体的文本图元。 | 需要富文本或编辑行为时要继续配置返回的 `QGraphicsTextItem`。 |
| 创建 | `addSimpleText(...)` | 创建绘制开销更低的简单文本图元。 | 适合只显示、不需要文本编辑的标签。 |
| 嵌入控件 | `addWidget(QWidget *, Qt::WindowFlags)` | 把普通 `QWidget` 包装成 `QGraphicsProxyWidget` 加入场景。 | 只适合少量、确实需要真实控件行为的场景；大量控件会增加开销。 |
| 移除 | `removeItem(QGraphicsItem *)` | 把 item 从场景移除。 | 不会删除 item；移除后由调用者负责保存、重新加入或 `delete`。 |
| 清空 | `clear()` | 移除并删除场景中的所有图元。 | 这是破坏性操作，不是“清除选择”；外部不要继续使用旧 item 指针。 |

### 8.4 焦点、鼠标、样式和场景状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 焦点 | `focusItem()` / `setFocusItem(...)` | 读取或设置当前接收键盘事件的 item。 | item 需要支持焦点；设置后还要确认场景和视图本身处于可聚焦状态。 |
| 焦点 | `hasFocus()` / `setFocus(...)` / `clearFocus()` | 查询、获取或清除场景焦点。 | `clearFocus()` 会让键盘事件不再送给当前场景 item。 |
| 焦点 | `stickyFocus()` / `setStickyFocus(bool)` | 控制点击场景空白处时是否保留当前焦点。 | 编辑器中常用于避免点空白区域就丢失文本输入焦点。 |
| 鼠标 | `mouseGrabberItem()` | 查询当前抓取鼠标事件的 item。 | 主要用于调试拖拽、按下后移动和事件没有落到预期 item 的问题。 |
| 背景 | `backgroundBrush()` / `setBackgroundBrush(...)` | 读取或设置场景背景画刷。 | 它属于场景绘制；视图还可以用自己的背景画刷覆盖显示策略。 |
| 前景 | `foregroundBrush()` / `setForegroundBrush(...)` | 读取或设置场景前景画刷。 | 适合网格、辅助线或统一覆盖层；复杂绘制可重写 `drawForeground()`。 |
| 样式 | `style()` / `setStyle(...)` | 读取或设置场景内图形控件使用的样式。 | 主要影响 `QGraphicsWidget` 等控件型 item，不等于改变普通 item 的 `paint()`。 |
| 字体 | `font()` / `setFont(...)` | 读取或设置场景级默认字体。 | 场景中的文本和控件可能继承它；单个 item 仍可覆盖。 |
| 调色板 | `palette()` / `setPalette(...)` | 读取或设置场景级调色板。 | 用于统一场景控件的颜色语义，不能替代自定义图元自己的画笔和画刷。 |
| 活动状态 | `isActive()` | 判断场景当前是否处于活动状态。 | 一个场景可以被多个视图显示，活动状态与某个具体视图的焦点有关。 |
| 活动面板 | `activePanel()` / `setActivePanel(...)` | 读取或设置活动的 panel item。 | 适合场景内有面板化交互时使用，普通图形编辑通常不需要。 |
| 活动窗口 | `activeWindow()` / `setActiveWindow(...)` | 读取或设置活动的 `QGraphicsWidget` 窗口。 | 只对场景中的窗口型图形控件有意义。 |
| 事件发送 | `sendEvent(QGraphicsItem *, QEvent *)` | 把事件直接发送给指定图元。 | 这是绕过正常命中分发的低层接口，事件类型和生命周期必须由调用者负责。 |
| 触摸焦点 | `focusOnTouch()` / `setFocusOnTouch(bool)` | 控制触摸操作是否自动把焦点给触摸到的 item。 | 触摸设备或混合输入场景才需要特别调整。 |

### 8.5 渲染、刷新和关联对象

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 渲染 | `render(QPainter *, const QRectF &target, const QRectF &source, Qt::AspectRatioMode)` | 把场景或场景的一部分绘制到任意 `QPainter`。 | 适合导出图片、打印和离屏渲染；目标 painter 的状态由调用方管理。 |
| 刷新 | `update(const QRectF &rect = QRectF())` | 请求场景指定区域重新绘制。 | 只发出更新请求，不保证同步立即完成。 |
| 失效 | `invalidate(const QRectF &, SceneLayers)` | 让场景指定区域的指定层失效并重新准备绘制。 | 自定义背景、前景或缓存层时比单纯 `update()` 更合适。 |
| 动画步进 | `advance()` | 让场景中支持 advance 的 item 执行一轮动画更新。 | 只有 item 实现了相应的 `advance(int)` 才会产生效果。 |
| 视图 | `views()` | 返回当前显示该场景的所有 `QGraphicsView`。 | 一个场景可以同时绑定多个视图；不要假设列表里只有一个。 |
| 信号 | `changed(const QList<QRectF> &)` | 通知场景中有区域发生变化。 | 适合刷新外部缩略图、导出预览或调试脏区域。 |
| 信号 | `sceneRectChanged(const QRectF &)` | 场景矩形发生变化时发出。 | 用于同步标尺、滚动范围和属性面板。 |
| 信号 | `selectionChanged()` | 选择集合发生变化时发出。 | 属性编辑器、状态栏和批量操作按钮通常连接它。 |
| 信号 | `focusItemChanged(...)` | 当前焦点 item 发生变化时发出。 | 可根据 `Qt::FocusReason` 区分鼠标、键盘或程序设置焦点。 |

### 一句话总结

`QGraphicsScene` 是图形世界的总账本：item 归它管，选区归它管，渲染和碰撞也归它管；视图只是把这张账本显示出来。
