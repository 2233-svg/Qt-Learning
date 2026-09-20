<!-- 依据 Qt 6.11.1 头文件 qgraphicslayout.h 整理。 -->

# QGraphicsLayout 深入笔记

> 头文件：`#include <QGraphicsLayout>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsLayoutItem -> QGraphicsLayout`  
> 性质：抽象布局基类，不能直接实例化

## 1. 它解决什么问题

`QGraphicsLayout` 是 Graphics View 体系的布局协议。它让 `QGraphicsWidget` 的子项不必依赖固定坐标，而是根据可用矩形、内容边距、尺寸提示和尺寸策略得到最终 `geometry`。

它与 QWidget 体系中的 `QLayout` 解决的是同一类问题，但服务的对象不同：

| 体系 | 容器与子项 | 常用布局 |
| --- | --- | --- |
| Widgets | `QWidget` | `QVBoxLayout`、`QGridLayout`、`QFormLayout` |
| Graphics View | `QGraphicsWidget` / `QGraphicsLayoutItem` | `QGraphicsLinearLayout`、`QGraphicsGridLayout`、`QGraphicsAnchorLayout` |

`QGraphicsLayout` 不定义“横向排”或“网格排”的具体规则。它只定义布局必须具备的骨架：保存子项、报告子项数量、按索引取出和移除子项，并在需要时计算几何位置。

```text
QGraphicsLayoutItem
  └─ QGraphicsLayout               // 抽象协议
       ├─ QGraphicsLinearLayout    // 一维线性排列
       ├─ QGraphicsGridLayout      // 行列网格
       └─ QGraphicsAnchorLayout    // 边缘约束
```

日常界面开发几乎总是直接使用这些具体类。只有在现有布局无法表达分配规则时，例如瀑布流、特殊拓扑图、时间轴轨道，才派生 `QGraphicsLayout` 自定义算法。

## 2. 安装到 `QGraphicsWidget` 后发生什么

布局最终必须由一个 `QGraphicsWidget` 承载：

```cpp
#include <QGraphicsLinearLayout>
#include <QGraphicsWidget>

auto *panel = new QGraphicsWidget;
auto *layout = new QGraphicsLinearLayout(Qt::Vertical);
panel->setLayout(layout);
```

也可以把 `QGraphicsWidget *` 作为布局构造参数。对于根 widget，这会让布局成为它的顶层布局：

```cpp
auto *panel = new QGraphicsWidget;
auto *layout = new QGraphicsLinearLayout(panel);
```

一个 `QGraphicsWidget` 同时只能有一个顶层布局。安装新布局会替换并销毁旧布局，因此不能把同一布局反复安装到多个 widget，也不要在已安装后手动删除它。

布局接到 `QGraphicsWidget` 的几何变化后，按如下过程工作：

```text
父布局或根 widget 获得新的 geometry
        ↓
QGraphicsLayout 计算自己的 contentsRect
        ↓
具体布局根据子项 size hint / QSizePolicy 分配区域
        ↓
对子项调用 setGeometry()
```

这里的 `contentsRect` 已扣除了 `contentsMargins`。边距属于布局和容器边缘之间；子项之间的间距由具体布局的 spacing 或锚点规则决定，`QGraphicsLayout` 基类不提供通用 `setSpacing()`。

## 3. 失效、激活和重算不是同一个动作

这三个 API 很容易被混为一谈：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 缓存失效 | `invalidate()` | 标记缓存的尺寸或几何信息已经过期 | 子项、边距或自定义布局参数改变时使用；不要把它当成立即重绘 |
| 立即布局 | `activate()` | 立刻执行一次待处理的布局计算 | 需要在当前调用点之后马上读取最新 geometry 时才用 |
| 向上通知 | `updateGeometry()` | 告诉父布局“我的尺寸提示变了” | 自定义布局的 size hint 改变时使用，让上层重新协商空间 |

通常业务代码只改具体布局的属性或子项大小，Qt 会安排一次延后的布局请求。这样同一轮事件循环里连续改十个属性不会强制重算十次。

例如动态显示一个区域后，只要修改 item 的可见性或尺寸策略即可；不要每步都调用 `activate()`。只有在“修改后立刻要读取子项最终矩形”这类确实需要同步结果的场景，才考虑：

```cpp
layout->activate();
const QRectF rect = layout->itemAt(0)->geometry();
```

频繁强制 `activate()` 会破坏布局合并更新的好处，复杂场景中可能导致拖动、缩放或动画卡顿。

`isActivated()` 表示布局当前是否处在激活后的有效状态；它不是“这个布局是否安装到 widget 上”的判断，也不表示子项一定可见。

## 4. 内容边距来自哪里

```cpp
layout->setContentsMargins(12.0, 8.0, 12.0, 8.0);

qreal left;
qreal top;
qreal right;
qreal bottom;
layout->getContentsMargins(&left, &top, &right, &bottom);
```

参数顺序固定为左、上、右、下。默认边距会受样式和布局层级影响：顶层布局通常使用窗口相关的样式边距，嵌套布局的默认值往往更小或为零。

因此，“为什么内容离面板边缘太远”先检查 `contentsMargins`；“为什么相邻控件距离太大”则检查具体布局的 spacing。两者不是同一回事。

## 5. 自定义布局至少要实现什么

`QGraphicsLayout` 是抽象类，下面三个函数必须实现：

```cpp
int count() const override;
QGraphicsLayoutItem *itemAt(int index) const override;
void removeAt(int index) override;
```

但这三个函数只让布局能保存和管理 item，并不会自动摆放它们。实际自定义布局还通常要重写：

- `setGeometry(const QRectF &rect)`：把可用区域分配给每个 child。
- `sizeHint(Qt::SizeHint, const QSizeF &) const`：向父布局报告最小、首选和最大尺寸建议。

示意性的一维自定义布局：

```cpp
class TrackLayout final : public QGraphicsLayout
{
public:
    void addItem(QGraphicsLayoutItem *item)
    {
        addChildLayoutItem(item);
        m_items.append(item);
        invalidate();
    }

    int count() const override { return m_items.size(); }

    QGraphicsLayoutItem *itemAt(int index) const override
    {
        return m_items.value(index, nullptr);
    }

    void removeAt(int index) override
    {
        if (QGraphicsLayoutItem *item = m_items.takeAt(index))
            item->setParentLayoutItem(nullptr);
        invalidate();
    }

    void setGeometry(const QRectF &rect) override
    {
        QGraphicsLayout::setGeometry(rect);

        const QRectF area = contentsRect();
        const qreal height = m_items.isEmpty()
            ? 0.0 : area.height() / m_items.size();

        for (qsizetype i = 0; i < m_items.size(); ++i) {
            m_items.at(i)->setGeometry(QRectF(
                area.left(), area.top() + i * height,
                area.width(), height));
        }
    }

protected:
    QSizeF sizeHint(Qt::SizeHint which,
                    const QSizeF &constraint = QSizeF()) const override;

private:
    QList<QGraphicsLayoutItem *> m_items;
};
```

这个例子刻意省略真实的最小/首选/最大尺寸协商，只展示职责分界：`addChildLayoutItem()` 建立布局父子关系，`setGeometry()` 决定位置，`sizeHint()` 决定上层如何看待这个布局的大小。

## 6. `addChildLayoutItem()` 不是普通追加函数

自定义布局的 `addItem()` 必须调用受保护的 `addChildLayoutItem()`，而不只是把指针塞进容器。它会建立 `QGraphicsLayoutItem` 的父布局关系，使其参与布局树、事件通知和几何传播。

加入一个已经属于其它布局的 item 前，应先将它从原布局移除；一个 item 不能同时被两个布局管理。子布局也同理。

`QGraphicsLayout` 不像 `QObject` 那样以 QObject 父子关系管理所有内容。item 的所有权由具体布局类的 API 契约决定。写自定义布局时必须明确约定：

- 布局析构时是否删除它管理的 item。
- `removeAt()` 是否把 item 所有权交给调用者。
- item 从布局摘下后是否需要 `setParentLayoutItem(nullptr)`。

内置布局各自已有行为约定；不要把其中一个类的移除语义机械套用到所有自定义布局。

## 7. `widgetEvent()`：布局为何能跟上宿主变化

当关联的 `QGraphicsWidget` 收到与布局有关的事件时，布局会先经由 `widgetEvent(QEvent *)` 得到通知。基类用它跟踪诸如尺寸、样式、布局方向和内容变化等影响几何协商的事件。

派生布局可重写它来监听自定义关心的 widget 事件，但应先理解基类行为；通常先调用：

```cpp
void MyLayout::widgetEvent(QEvent *event)
{
    QGraphicsLayout::widgetEvent(event);
    // 仅处理本布局额外关心的事件。
}
```

不要在每一个事件里无条件做昂贵计算。绝大多数场景只需 `invalidate()`，让框架合并后续激活。

## 8. 全局失效传播开关

`setInstantInvalidatePropagation(bool)` 和 `instantInvalidatePropagation()` 是静态 API，控制布局树中的失效状态是否立即向上传播。它们影响整个进程内的 Graphics View 布局行为，而不是单个布局对象。

这类全局开关通常只适合 Qt 自身、框架集成或非常明确的诊断场景。普通应用不应把它当作“刷新不及时”的常规修复手段：它会改变所有相关布局的更新时机，问题往往应通过正确的 `invalidate()`、`updateGeometry()` 或 item 尺寸提示来解决。

## 9. API 逐项说明

### 容器协议

- `count()`：报告当前管理的子项数量。
- `itemAt(int)`：按索引返回子项；无效索引应返回空指针。
- `removeAt(int)`：移除指定子项；派生类必须明确 item 的后续所有权。
- `addChildLayoutItem()`：把 item 接入布局树的受保护辅助函数。

### 生命周期和几何协商

- `activate()`：立即执行待处理的布局。
- `invalidate()`：作废本布局缓存。
- `isActivated()`：查询布局是否已激活。
- `updateGeometry()`：把尺寸提示变化传递给父布局。
- `widgetEvent()`：接收宿主 `QGraphicsWidget` 的相关事件。
- `setContentsMargins()` / `getContentsMargins()`：设置或读取布局边距。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsLayout(QGraphicsLayoutItem *parent = nullptr)` | 创建布局基类部分，并可指定布局树父项。 | 抽象类；实际创建派生布局，安装到 `QGraphicsWidget` 后由其管理。 |
| 析构 | `~QGraphicsLayout()` | 销毁布局。 | 已作为 widget 顶层布局安装时通常不手动删除。 |
| 设置 | `void setContentsMargins(qreal left, qreal top, qreal right, qreal bottom)` | 设置内容区与布局外框之间的四边边距。 | 参数顺序是左、上、右、下；不是 item 之间的 spacing。 |
| 查询 | `void getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const` | 读取当前四边内容边距。 | 传入可写地址；可用于诊断样式默认值。 |
| 命令 | `void activate()` | 立即完成一次待处理的布局计算。 | 仅在必须同步读取最新 geometry 时使用。 |
| 查询 | `bool isActivated() const` | 查询布局是否已处于激活状态。 | 不代表 widget 可见或布局已永久稳定。 |
| 失效 | `virtual void invalidate()` | 标记布局缓存过期。 | 常规属性变化通常已自动调用；自定义参数变化时使用。 |
| 几何通知 | `virtual void updateGeometry()` | 通知父布局本布局的尺寸提示发生改变。 | 自定义 `sizeHint()` 依赖的状态变化后调用。 |
| 事件钩子 | `virtual void widgetEvent(QEvent *e)` | 接收宿主 `QGraphicsWidget` 的布局相关事件。 | 派生时通常先调用基类实现，避免遗漏基础处理。 |
| 抽象容器接口 | `virtual int count() const = 0` | 返回管理的子项数量。 | 派生类必须实现，并与 `itemAt()` 保持一致。 |
| 抽象容器接口 | `virtual QGraphicsLayoutItem *itemAt(int i) const = 0` | 返回指定索引的子项。 | 无效索引应返回 `nullptr`，不转移所有权。 |
| 抽象容器接口 | `virtual void removeAt(int index) = 0` | 移除指定索引的子项。 | 派生类必须处理父关系和 item 所有权。 |
| 受保护函数 | `void addChildLayoutItem(QGraphicsLayoutItem *layoutItem)` | 将 item 接入布局树。 | 自定义 `addItem()` 必须调用；item 不能同时属于两个布局。 |
| 受保护构造 | `QGraphicsLayout(QGraphicsLayoutPrivate &, QGraphicsLayoutItem *)` | Qt 私有实现使用的构造入口。 | 参数类型是私有实现，普通应用和普通派生类不要调用。 |
| 全局设置 | `static void setInstantInvalidatePropagation(bool enable)` | 设置布局失效是否立即向布局树上传播。 | 影响整个进程；普通业务代码不应依赖。 |
| 全局查询 | `static bool instantInvalidatePropagation()` | 查询当前的即时失效传播设置。 | 用于框架级诊断，不是单个布局状态。 |

## 11. 排查清单

1. 子项没有重新排布：确认改变的是尺寸提示相关状态，并让布局失效；不要只改绘制而期待 geometry 改变。
2. 读取到旧 geometry：在同一调用栈内修改后确需读取时，调用 `activate()`；平时让事件循环合并更新。
3. 自定义布局里 item 消失：确认添加时调用了 `addChildLayoutItem()`，并在 `setGeometry()` 中给每个 item 分配矩形。
4. 移除 item 后崩溃或泄漏：明确 `removeAt()` 的父关系和所有权策略，不要只从指针容器中移除。
5. 边距与间距不对：`contentsMargins` 管外侧，具体布局的 spacing 或 anchor 管 item 之间。

### 一句话总结

`QGraphicsLayout` 是 Graphics View 的布局骨架：具体类负责排列算法，基类负责布局树、边距、失效传播和几何协商；自定义时最重要的是子项关系、尺寸提示和延后激活这三件事。
