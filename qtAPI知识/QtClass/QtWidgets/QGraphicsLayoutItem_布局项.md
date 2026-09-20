<!-- 依据 Qt 6.11.1 头文件 qgraphicslayoutitem.h 整理。 -->

# QGraphicsLayoutItem 深入笔记

> 头文件：`#include <QGraphicsLayoutItem>`  
> 模块：`Qt6::Widgets`  
> 性质：抽象布局项协议，不是 `QObject`，不能直接实例化

## 1. 它解决什么问题

`QGraphicsLayoutItem` 是 Graphics View 布局系统中“可被测量和摆放的东西”的共同接口。`QGraphicsWidget`、`QGraphicsLayout` 及其具体布局都通过它向父布局回答三个问题：

```text
我至少要多大？            minimum size
我希望多大？              preferred size
我最多能多大、能否扩张？   maximum size + QSizePolicy
```

父布局据此分配 `geometry`，item 再依据这个矩形绘制内容或继续布局子项。

它不是可视控件本身。一个 `QGraphicsLayoutItem` 可以关联 `QGraphicsItem`，也可以只是自定义布局对象；常见派生关系是：

```text
QGraphicsLayoutItem
  ├─ QGraphicsWidget        // 既是场景图元，又可参与布局
  └─ QGraphicsLayout        // 自己是 layout item，也管理其它 item
```

普通项目不应直接派生它。仅当你实现自定义 `QGraphicsWidget` 或自定义 `QGraphicsLayout` 时，才需要直接处理它的 `sizeHint()`、geometry 和所有权协议。

## 2. 布局协商的完整链条

```text
child 的 sizeHint() / QSizePolicy
        ↓
effectiveSizeHint() 合并显式最小、首选、最大限制
        ↓
父 QGraphicsLayout 分配 geometry
        ↓
child::setGeometry()
        ↓
child 依据 contentsRect() 绘制或继续摆放内部内容
```

这里有三个矩形，务必区分：

| 名称 | 含义 | 常见误解 |
| --- | --- | --- |
| `geometry()` | 父布局分配给本 item 的矩形。 | 不是 `QGraphicsItem::boundingRect()`。 |
| `contentsRect()` | `geometry` 扣掉本 item 内容边距后的可用内部区域。 | 不是父布局的 contents rect。 |
| `QGraphicsItem::boundingRect()` | 图元自身需要绘制和命中测试的本地范围。 | 不能直接代替布局尺寸提示。 |

一个自定义 item 的绘制范围变大时，若布局需要随之扩张，应更新 `sizeHint()` 依赖的数据并调用 `updateGeometry()`；只调用 `QGraphicsItem::update()` 只会重绘，不会重新协商尺寸。

## 3. 三套尺寸值不是互相替代

```cpp
item->setMinimumSize(80, 24);
item->setPreferredSize(180, 32);
item->setMaximumWidth(420);
item->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
```

- **minimum**：布局不能再压缩的下限。
- **preferred**：空间足够时希望得到的大小。
- **maximum**：布局不应继续增长的上限。
- **size policy**：在有额外空间或空间不足时，这个 item 愿意怎样伸缩。

`setMinimumWidth()`、`setPreferredWidth()`、`setMaximumWidth()` 是二维 setter 的 X 轴便捷写法；Height 版本同理。它们不是固定宽度 API，只有 `minimum == maximum` 才会把该方向锁死。

显式设置的值会参与 `effectiveSizeHint()`。传入无效尺寸可撤销对应的显式覆盖，重新让派生类的 `sizeHint()` 和 `QSizePolicy` 主导协商。

## 4. `sizeHint()` 与 `effectiveSizeHint()` 如何分工

派生类必须实现受保护的纯虚函数：

```cpp
QSizeF sizeHint(Qt::SizeHint which,
                const QSizeF &constraint = QSizeF()) const override;
```

它报告原始的最小、首选、最大尺寸建议。`constraint` 用于表达“给定一个方向后，另一个方向需要多大”，例如文本换行时可传入指定宽度来计算需要的高度。

业务代码和父布局通常读取的是：

```cpp
const QSizeF preferred =
    item->effectiveSizeHint(Qt::PreferredSize);
```

`effectiveSizeHint()` 会将原始 `sizeHint()`、显式 min/preferred/max 及 `QSizePolicy` 合并并缓存，得到布局真正使用的尺寸建议。不要在高频绘制中反复绕过它调用自己昂贵的尺寸计算；数据变化后调用 `updateGeometry()`，让布局失效和缓存更新走标准路径。

## 5. `geometry`、边距和可见性

父布局调用 `setGeometry(const QRectF &)` 后，本 item 的 `geometry()` 更新。基类会维护该矩形；派生类重写时通常应先调用基类，再基于 `contentsRect()` 更新内部子项。

```cpp
void MyWidget::setGeometry(const QRectF &rect)
{
    QGraphicsWidget::setGeometry(rect);
    const QRectF area = contentsRect();
    // 把内部布局或绘制区域安排到 area。
}
```

`getContentsMargins()` 默认读取 item 的内容边距；布局类可能重写它并向样式系统询问默认值。

`isEmpty()` 用于告诉布局“此 item 当前是否应该占据空间”。在 Qt 6 中，隐藏 item 通常被视为 empty，除非尺寸策略启用了 `retainSizeWhenHidden`。这解释了“隐藏后其它控件自动补位”和“想隐藏但保留位置”的区别。

## 6. 布局父子关系与所有权

`parentLayoutItem()` / `setParentLayoutItem()` 管的是**布局树**，不等于 `QGraphicsItem::parentItem()` 管的图元树。

当一个 `QGraphicsWidget` 加入布局时，两个树往往都存在：

```text
QGraphicsItem parent-child tree      QGraphicsLayoutItem parent-child tree
panel -> childWidget                 panelLayout -> childWidget
```

`ownedByLayout()` 表示该 item 是否由布局负责销毁。它存在的原因正是避免布局树和 `QGraphicsItem` 树都尝试删除同一对象。一般应用不要直接调用受保护的 `setOwnedByLayout()`；内置布局和自定义复合 item 会按自身所有权模型设置它。

移除 item 时，先让布局解除 `parentLayoutItem` 关系，再按实际图元父子关系决定由谁删除。不要只看一个树就调用 `delete`。

## 7. 自定义 item 的边界

- `setGraphicsItem(QGraphicsItem *)`：将 layout item 和一个场景图元关联。只适合派生实现建立这种映射，普通业务代码不应调用。
- `isLayout()`：判断该对象是否被构造为布局。它用于框架区分普通 item 和布局 item，不是“当前有没有 child”的查询。
- `graphicsItem()`：取得关联图元，可能为空；不保证它仍在 scene 中。
- 私有构造 `QGraphicsLayoutItem(QGraphicsLayoutItemPrivate &)`：Qt 内部 d-pointer 入口，不属于自定义应用 API。

所有与 layout item、geometry 和图元关联的操作都应在 GUI 线程进行。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsLayoutItem(QGraphicsLayoutItem *parent = nullptr, bool isLayout = false)` | 初始化布局项基类并指定布局树父项/类型。 | 抽象类；通常只由 `QGraphicsWidget`、`QGraphicsLayout` 或自定义派生类调用。 |
| 析构 | `virtual ~QGraphicsLayoutItem()` | 销毁布局项。 | 先厘清布局树与图元树的所有权，避免重复删除。 |
| 尺寸策略 | `void setSizePolicy(const QSizePolicy &policy)` | 一次设置水平、垂直尺寸策略。 | 决定额外空间和压缩时的倾向，不直接等于固定尺寸。 |
| 尺寸策略 | `void setSizePolicy(QSizePolicy::Policy hPolicy, QSizePolicy::Policy vPolicy, QSizePolicy::ControlType controlType = QSizePolicy::DefaultType)` | 用两个方向策略设置尺寸策略。 | 适合只想明确某一方向是否可扩张。 |
| 尺寸策略 | `QSizePolicy sizePolicy() const` | 读取当前尺寸策略。 | 与最小/最大尺寸一起解读。 |
| 最小尺寸 | `void setMinimumSize(const QSizeF &size)` | 设置二维最小尺寸。 | 过大将挤压其它 item。 |
| 最小尺寸 | `void setMinimumSize(qreal w, qreal h)` | 以宽高设置二维最小尺寸。 | 是 `QSizeF` 重载的便捷写法。 |
| 最小尺寸 | `QSizeF minimumSize() const` | 读取有效最小尺寸。 | 结果已综合尺寸提示和显式限制。 |
| 最小尺寸 | `void setMinimumWidth(qreal width)` | 设置最小宽度。 | 不改变高度限制。 |
| 最小尺寸 | `qreal minimumWidth() const` | 读取有效最小宽度。 | 等价于有效最小尺寸的宽。 |
| 最小尺寸 | `void setMinimumHeight(qreal height)` | 设置最小高度。 | 不改变宽度限制。 |
| 最小尺寸 | `qreal minimumHeight() const` | 读取有效最小高度。 | 等价于有效最小尺寸的高。 |
| 首选尺寸 | `void setPreferredSize(const QSizeF &size)` | 设置二维首选尺寸。 | 是布局的目标值，不是强制固定值。 |
| 首选尺寸 | `void setPreferredSize(qreal w, qreal h)` | 以宽高设置二维首选尺寸。 | 是 `QSizeF` 重载的便捷写法。 |
| 首选尺寸 | `QSizeF preferredSize() const` | 读取有效首选尺寸。 | 受 min/max 和策略影响。 |
| 首选尺寸 | `void setPreferredWidth(qreal width)` | 设置首选宽度。 | 常用于编辑器或预览区初始宽度。 |
| 首选尺寸 | `qreal preferredWidth() const` | 读取有效首选宽度。 | 不是最终 geometry 宽度。 |
| 首选尺寸 | `void setPreferredHeight(qreal height)` | 设置首选高度。 | 多行内容可结合宽度约束动态算高。 |
| 首选尺寸 | `qreal preferredHeight() const` | 读取有效首选高度。 | 不是最终 geometry 高度。 |
| 最大尺寸 | `void setMaximumSize(const QSizeF &size)` | 设置二维最大尺寸。 | 可能阻止 item 吸收剩余空间。 |
| 最大尺寸 | `void setMaximumSize(qreal w, qreal h)` | 以宽高设置二维最大尺寸。 | 是 `QSizeF` 重载的便捷写法。 |
| 最大尺寸 | `QSizeF maximumSize() const` | 读取有效最大尺寸。 | 应始终不小于 minimum。 |
| 最大尺寸 | `void setMaximumWidth(qreal width)` | 设置最大宽度。 | 限制水平扩张。 |
| 最大尺寸 | `qreal maximumWidth() const` | 读取有效最大宽度。 | 检查 item 不变宽时的重要线索。 |
| 最大尺寸 | `void setMaximumHeight(qreal height)` | 设置最大高度。 | 限制垂直扩张。 |
| 最大尺寸 | `qreal maximumHeight() const` | 读取有效最大高度。 | 检查 item 不变高时的重要线索。 |
| 几何 | `virtual void setGeometry(const QRectF &rect)` | 接收父布局分配的矩形。 | 派生重写时通常先调用基类，再摆放内部内容。 |
| 几何 | `QRectF geometry() const` | 读取当前由布局分配的矩形。 | 不等于 `QGraphicsItem::boundingRect()`。 |
| 内容区 | `virtual void getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const` | 读取内容边距。 | 参数顺序为左、上、右、下。 |
| 内容区 | `QRectF contentsRect() const` | 返回 `geometry` 扣除内容边距后的区域。 | 用于内部布局和绘制区域，不是图元绘制边界。 |
| 尺寸协商 | `QSizeF effectiveSizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const` | 取得布局实际采用的缓存尺寸建议。 | 合并 `sizeHint`、min/preferred/max 与策略；高频路径不要重复做自算。 |
| 受保护尺寸协商 | `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const = 0` | 报告派生类原始尺寸建议。 | 自定义 item 必须实现，需支持最小/首选/最大请求。 |
| 几何通知 | `virtual void updateGeometry()` | 通知父布局重新协商尺寸。 | 改变 `sizeHint()` 依赖状态后调用；单纯 `update()` 不够。 |
| 可见性 | `virtual bool isEmpty() const` | 判断当前是否应占用布局空间。 | 隐藏 item 通常为空；`retainSizeWhenHidden` 可改变行为。 |
| 布局树 | `QGraphicsLayoutItem *parentLayoutItem() const` | 读取布局树父项。 | 不等同于 `QGraphicsItem::parentItem()`。 |
| 布局树 | `void setParentLayoutItem(QGraphicsLayoutItem *parent)` | 设置布局树父项。 | 一般由布局管理；手动迁移前先从旧布局移除。 |
| 类型 | `bool isLayout() const` | 判断此 item 是否为布局类型。 | 框架内部分类，不代表是否已有子项。 |
| 图元关联 | `QGraphicsItem *graphicsItem() const` | 读取关联的场景图元。 | 可能为空；不代表图元仍在 scene 中。 |
| 所有权 | `bool ownedByLayout() const` | 查询布局是否负责删除本 item。 | 用于协调布局树和图元树所有权。 |
| 受保护图元关联 | `void setGraphicsItem(QGraphicsItem *item)` | 关联一个场景图元。 | 仅派生实现使用，普通业务代码不要调用。 |
| 受保护所有权 | `void setOwnedByLayout(bool ownedByLayout)` | 指定布局是否拥有本 item。 | 仅自定义复合 item/布局实现时使用，错误设置会导致泄漏或重复删除。 |
| 受保护构造 | `QGraphicsLayoutItem(QGraphicsLayoutItemPrivate &dd)` | Qt 私有实现用构造入口。 | d-pointer 私有类型，普通派生类不要调用。 |

## 9. 排查清单

1. item 没随内容变大：确认 `sizeHint()` 依赖数据变化后调用了 `updateGeometry()`。
2. item 被压缩或不肯扩张：同时检查 minimum、maximum 和 `QSizePolicy`，不要只查 preferred。
3. 内部内容贴边：检查 `contentsRect()` 与内容边距，不要误用 `geometry()`。
4. 隐藏 item 后布局空了：这是 `isEmpty()` 的正常结果；需要保位时使用 `retainSizeWhenHidden`。
5. 动态移除后崩溃：检查 `parentLayoutItem()` 与图元 parent tree，明确谁拥有对象。

### 一句话总结

`QGraphicsLayoutItem` 是 Graphics View 布局的尺寸协商契约：`sizeHint` 提供原始需求，`effectiveSizeHint` 给出可用约束，父布局写入 `geometry`，`contentsRect` 留给内部内容，而布局树与图元树的所有权必须分别处理。
