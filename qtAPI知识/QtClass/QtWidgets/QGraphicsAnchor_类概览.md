# QGraphicsAnchor：锚点布局中的一条边缘约束

> Qt 6.11.1 · `#include <QGraphicsAnchor>` · 模块：`Qt6::Widgets` · 继承：`QObject`

`QGraphicsAnchor` 表示 `QGraphicsAnchorLayout` 中两个 `QGraphicsLayoutItem` 边缘之间的一条约束，例如“左侧 item 的右边到右侧 item 的左边保持 8 像素”。它不是控件，也不是单纯数值，而是布局求解器中的一条关系。

## 使用场景

当 Graphics View 中的面板需要边到边约束、局部间距覆盖、弹性空隙时，`QGraphicsAnchorLayout` 会返回 `QGraphicsAnchor` 让你调整这条关系。简单横纵排列优先用 `QGraphicsLinearLayout`；只有对齐关系较多时锚点布局才值得使用。

`QGraphicsAnchor` 不能直接构造，必须由 `QGraphicsAnchorLayout::addAnchor()` 或 `anchor()` 得到。生命周期由布局管理，析构 anchor 会把它从布局中移除。

## spacing 和 sizePolicy

`spacing` 是这条边缘关系的首选间距。调用 `setSpacing()` 会覆盖布局默认间距；`unsetSpacing()` 是撤销局部设置，回到布局默认值，不是设成 0。

`sizePolicy` 控制的是“这段空隙”能否伸缩，不是两端 item 的尺寸策略。默认 `Fixed` 表示空隙固定；设置为更可伸缩的策略后，它可在布局分配多余空间时变大。

## API 速查表

| API | 语义与边界 |
|---|---|
| `setSpacing(qreal spacing)` | 为当前 anchor 设置显式间距，覆盖布局默认。 |
| `unsetSpacing()` | 清除显式间距，恢复使用布局默认间距。 |
| `spacing() const` | 返回当前间距，可能来自显式设置或布局默认。 |
| `setSizePolicy(QSizePolicy::Policy)` | 设置空隙的伸缩策略；管间距，不管 item 本身大小。 |
| `sizePolicy() const` | 返回当前空隙策略。 |
| `~QGraphicsAnchor()` | 销毁并从布局移除该 anchor；通常不由业务代码直接 delete。 |
| 创建方式 | 通过 `QGraphicsAnchorLayout::addAnchor()`，不能直接 new。 |
| 默认策略 | `QSizePolicy::Fixed`，空隙默认不可伸缩。 |
