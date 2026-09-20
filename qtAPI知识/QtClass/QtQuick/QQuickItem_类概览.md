# QQuickItem：Qt Quick 场景中的可视项、输入项与场景图同步入口

> Qt 6.11.1 · `#include <QQuickItem>` · 模块：`Qt6::Quick` · 继承：`QObject`, `QQmlParserStatus`

`QQuickItem` 是 QML 可视树的 C++ 基类。它本身不是 QWidget，也不直接用 `QPainter` 绘制；它管理几何、父子层级、输入、焦点、裁剪、状态和与场景图的同步，并在需要自绘时通过 `updatePaintNode()` 交出一棵 `QSGNode` 子树。

## 先分清两棵树

Item 树属于 QObject/QML 世界，运行在 GUI 线程，负责属性绑定、布局关系和事件分发。Scene graph 节点树属于渲染世界，主要在渲染线程使用，负责实际绘制。自定义 Item 最常见的错误，就是在 GUI 线程保存并修改 `QSGNode`，或在 `updatePaintNode()` 外部创建和操作 QSG 资源。

只有设置 `ItemHasContents` 的 Item 才应该调用 `update()` 并覆写 `updatePaintNode()`。`update()` 只是安排一次同步；真正的节点创建、复用和修改发生在 `updatePaintNode(oldNode, data)` 中。该函数运行时主线程会被阻塞，因此可以安全读取 Item 属性，但 QSG 操作仍应限制在这段回调里。

## 真实使用场景

普通 C++ Item 若只是组合 QML 子项，通常只设置尺寸、隐式尺寸、焦点和输入处理即可，不需要场景图节点。需要高性能绘制曲线、图像、网格、波形或自定义 shader 时，才启用 `ItemHasContents`，用 `QSGGeometryNode`、`QSGImageNode`、`QSGRenderNode` 等描述内容。

```cpp
MyItem::MyItem()
{
    setFlag(ItemHasContents, true);
}

QSGNode *MyItem::updatePaintNode(QSGNode *oldNode, UpdatePaintNodeData *)
{
    auto *node = static_cast<QSGGeometryNode *>(oldNode);
    if (!node)
        node = new QSGGeometryNode;
    // 在这里同步几何、材质和 dirty 标记。
    return node;
}
```

## 几何、层级与命中

`x/y/width/height` 定义 Item 局部矩形，`boundingRect()` 默认等于 `(0, 0, width, height)`。`implicitWidth/implicitHeight` 是给布局和使用者的尺寸建议，不会自动改变 `width/height`。`parentItem()` 决定可视父子关系；`QObject::parent()` 是对象生命周期关系，二者相关但不是同一个概念。

子项顺序、`z` 和 `stackBefore()`/`stackAfter()` 决定视觉堆叠，也会影响 tab 焦点遍历顺序。`contains()` 决定点是否位于 Item 内；若形状不是矩形，可覆写它或设置 `containmentMask`，这样鼠标命中和 `childAt()` 才能符合真实形状。

## 输入、焦点与渲染边界

鼠标事件需要 `setAcceptedMouseButtons()`，hover 需要 `setAcceptHoverEvents(true)`，触摸需要 `setAcceptTouchEvents(true)`。要拦截子项鼠标事件，开启 `setFiltersChildMouseEvents(true)` 并覆写 `childMouseEventFilter()`。事件处理函数默认通常接受事件；若想继续向下传递，应显式 `event->ignore()`。

`focus` 表示此 Item 请求焦点，`activeFocus` 表示它实际拥有键盘焦点。焦点作用域通过 `ItemIsFocusScope` 管理局部焦点；`forceActiveFocus()` 可主动抢焦点并带上原因。输入法相关 Item 需要 `ItemAcceptsInputMethod`、覆写 `inputMethodQuery()`，并在查询值变化时调用 `updateInputMethod()`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QQuickItem(parent)` / `~QQuickItem()` | 创建/销毁 Item；可视父项用 `setParentItem()` 管理，不等同于 QObject parent。 |
| `setFlag(flag, enabled)` / `setFlags(flags)` / `flags()` | 管理 Item 标志；自绘必须启用 `ItemHasContents`。 |
| `update()` | 安排下一次 `updatePaintNode()`；只允许有内容的 Item 调用。 |
| `updatePaintNode(oldNode, data)` | 渲染线程同步入口；创建或复用 QSG 子树并返回根节点。 |
| `releaseResources()` | 释放图形资源；场景图失效或资源回收时调用。 |
| `polish()` / `updatePolish()` / `ensurePolished()` | 延迟执行布局和整理工作，适合合并多次属性变化。 |
| `geometryChange(new, old)` | 几何变化通知；替代旧的 `geometryChanged()` 路径。 |
| `itemChange(change, data)` | 父项、子项、窗口、可见性、焦点等状态变化通知。 |
| `x/y/z/width/height` 与 setter | 控制位置、堆叠值和显式尺寸。 |
| `setSize()` / `setPosition()` | 同时设置尺寸或位置，减少分散更新。 |
| `implicitWidth/implicitHeight` / `setImplicitSize()` | 提供布局建议；不会强制改变实际宽高。 |
| `boundingRect()` | 默认返回本地边界；自定义命中或绘制边界可覆写相关逻辑。 |
| `clip` / `clipRect()` | 控制子项是否裁剪到 Item 形状；自定义视口场景可覆写裁剪矩形。 |
| `visible` / `enabled` / `opacity` | 控制显示、输入启用和透明度；透明度会沿子树累积。 |
| `rotation` / `scale` / `transformOrigin` / `transform` | 管理 Item 变换；影响坐标映射、命中和渲染。 |
| `mapToItem()` / `mapFromItem()` | 在两个 Item 坐标系之间映射点或矩形。 |
| `mapToScene()` / `mapFromScene()` | 与 scene 坐标互转。 |
| `mapToGlobal()` / `mapFromGlobal()` | 与屏幕全局坐标互转。 |
| `parentItem()` / `setParentItem()` | 读取或改变可视父项。 |
| `childItems()` / `childAt()` | 读取子项列表或命中指定本地点的子项。 |
| `stackBefore()` / `stackAfter()` | 调整同父项下顺序，同时影响绘制和 tab 顺序。 |
| `window()` / `windowChanged()` | 读取或监听所属 `QQuickWindow`。 |
| `setAcceptedMouseButtons()` / `acceptedMouseButtons()` | 控制能接收哪些鼠标按键事件。 |
| `setAcceptHoverEvents()` / `acceptHoverEvents()` | 控制 hover 事件。 |
| `setAcceptTouchEvents()` / `acceptTouchEvents()` | 控制触摸事件。 |
| `grabMouse()` / `ungrabMouse()` / `setKeepMouseGrab()` | 管理鼠标抓取。 |
| `grabTouchPoints()` / `ungrabTouchPoints()` / `setKeepTouchGrab()` | 管理触摸点抓取。 |
| `setFiltersChildMouseEvents()` / `childMouseEventFilter()` | 让父项过滤子项鼠标事件。 |
| `contains(point)` / `containmentMask` | 控制命中测试形状。 |
| `setCursor()` / `unsetCursor()` | 设置或清除悬停光标。 |
| `setFocus()` / `hasFocus()` / `hasActiveFocus()` | 请求或查询焦点状态。 |
| `forceActiveFocus(reason)` | 主动获得活动焦点。 |
| `setFocusPolicy()` / `focusPolicy()` | Qt 6.7 起设置焦点策略。 |
| `nextItemInFocusChain()` / `scopedFocusItem()` | 查询焦点链和焦点作用域中的当前项。 |
| `keyPressEvent()` / `keyReleaseEvent()` | 处理键盘事件。 |
| `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()` / `mouseDoubleClickEvent()` | 处理鼠标事件。 |
| `touchEvent()` / `wheelEvent()` / `hover*Event()` | 处理触摸、滚轮和 hover 事件。 |
| `dragEnterEvent()` / `dragMoveEvent()` / `dropEvent()` | 处理拖放，通常配合 `ItemAcceptsDrops`。 |
| `inputMethodQuery()` / `inputMethodEvent()` / `updateInputMethod()` | 输入法查询、提交和状态刷新。 |
| `grabToImage()` | 异步抓取 Item 渲染结果；返回 `QQuickItemGrabResult`。 |
| `isTextureProvider()` / `textureProvider()` | 暴露 Item 生成的纹理，默认不提供。 |
| `dumpItemTree()` | Qt 6.3 起调试输出 Item 树。 |
