# Qt QStyleOptionRubberBand 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionRubberBand>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionRubberBand`  
> 常见协作者：`QRubberBand`、`QStyle`

## 1. 它解决什么问题

拖拽选择文件、框选画布对象、调整分割条或拖出一个停靠面板时，界面需要即时显示“当前将覆盖/选择的区域”。这种临时视觉提示称为 rubber band。

早期 GUI 常用 XOR 方式直接在底图上反复画线和擦线，但底层窗口若在中间重绘，原图与橡皮筋线就可能无法正确恢复。`QRubberBand` 改用独立覆盖控件来解决这个问题：它位于父控件的子控件层级中，显示、移动、隐藏都由 Qt 正常的窗口与重绘体系管理。

`QStyleOptionRubberBand` 则是 `QRubberBand` 交给 `QStyle` 的绘制参数：

```text
鼠标拖动
  -> QRubberBand::setGeometry()
  -> QRubberBand::paintEvent()
  -> QStyleOptionRubberBand
  -> QStyle::CE_RubberBand
  -> 当前 style 画轮廓或半透明选择区域
```

它不是可见控件，不能调用 `show()` 或 `setGeometry()`；要创建和控制的是 `QRubberBand`。

## 2. 何时使用 `QRubberBand`，何时使用 option

| 需求 | 应使用的类型 | 原因 |
| --- | --- | --- |
| 在鼠标拖动时显示框选区域 | `QRubberBand` | 它是实际的 `QWidget` 覆盖层。 |
| 显示一条临时分隔/插入线 | `QRubberBand(QRubberBand::Line, ...)` | line shape 是给 style 的绘制提示。 |
| 自定义 rubber band 外观 | `QStyle` / `QProxyStyle` + `QStyleOptionRubberBand` | option 描述当前 shape、矩形与透明度要求。 |
| 读取一个 `QRubberBand` 的真实绘制状态 | `QRubberBand::initStyleOption()` | 子类中由真实控件填充 option。 |

普通业务代码直接使用 `QRubberBand`。只有自定义 style、派生 `QRubberBand` 或排查绘制逻辑时，才需要直接了解这个 option。

## 3. 构建与完整拖选示例

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 鼠标拖动框选区域

```cpp
#include <QMouseEvent>
#include <QRubberBand>
#include <QWidget>

class SelectionSurface final : public QWidget
{
public:
    SelectionSurface()
    {
        setMinimumSize(420, 280);
    }

protected:
    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() != Qt::LeftButton)
            return;

        origin_ = event->position().toPoint();

        if (!rubberBand_) {
            rubberBand_ = new QRubberBand(QRubberBand::Rectangle, this);
        }

        rubberBand_->setGeometry(QRect(origin_, QSize()));
        rubberBand_->show();
    }

    void mouseMoveEvent(QMouseEvent *event) override
    {
        if (!rubberBand_)
            return;

        const QRect selection(origin_, event->position().toPoint());
        rubberBand_->setGeometry(selection.normalized());
    }

    void mouseReleaseEvent(QMouseEvent *event) override
    {
        if (event->button() != Qt::LeftButton || !rubberBand_)
            return;

        rubberBand_->hide();
        const QRect selection = rubberBand_->geometry();

        // 用 selection 与子项几何相交关系完成实际选择。
    }

private:
    QPoint origin_;
    QRubberBand *rubberBand_ = nullptr;
};
```

`normalized()` 不能省略。用户可能从右下往左上拖动；未规范化的 `QRect` 会产生负方向边界，导致几何和命中判断异常。

`QRubberBand` 的 parent 是 `SelectionSurface`，因此它会被父控件销毁时自动删除，并且只显示在父控件区域内、覆盖其他子控件之上。鼠标释放时一般 `hide()` 后复用同一对象，不必每次拖拽都重新分配。

## 4. `shape`：这是绘制提示，不是几何限制

`shape` 的类型是 `QRubberBand::Shape`：

| 值 | 表示什么 | 常见用途 |
| --- | --- | --- |
| `QRubberBand::Line` | 一条水平或垂直的临时指示线。 | splitter 拖动、插入位置、停靠预览。 |
| `QRubberBand::Rectangle` | 一个矩形范围。 | 框选文件、画布对象、截图区域。 |

它告诉 style 应把矩形按“线”还是“框”的语义绘制；不是几何约束。即使是 `Line`，仍通过 `rect` 指定区域，许多 style 会让线填满该矩形。

`QStyleOptionRubberBand` 默认 `shape` 是 `QRubberBand::Line`。实际 `QRubberBand` 的 shape 在构造函数中指定，并且之后不能修改：

```cpp
auto *line = new QRubberBand(QRubberBand::Line, parent);
auto *rectangle = new QRubberBand(QRubberBand::Rectangle, parent);
```

若交互流程需要在线和矩形之间切换，创建/维护两个不同实例，或在模式切换时重新创建；不要试图在 option 上改 `shape` 来改变已存在 `QRubberBand` 的行为。

## 5. `opaque`：绘制要求，不是业务透明度开关

`opaque` 表示 rubber band 是否**要求 style 以不透明方式绘制**，默认值为 `true`。

它不是：

- `QWidget::windowOpacity` 的直接替代。
- “当前 alpha 必然为 1.0”的保证。
- 控制鼠标事件是否穿透的标志。

不同 style 可以将 `Rectangle` 画成细边框、带 mask 的边界，或半透明填充。尤其某些原生平台 style 会使用半透明矩形来表达选择区域。`opaque` 是传给 style 的绘制上下文，而最终像素效果由 style 和平台决定。

若你在自定义 style 中处理 `CE_RubberBand`，应尊重这一字段，而不是无论场景都画固定半透明蓝框。

## 6. 从真实控件初始化 option

`QRubberBand` 提供受保护的 `initStyleOption()`，给子类在需要自定义绘制时使用：

```cpp
class CustomRubberBand final : public QRubberBand
{
public:
    using QRubberBand::QRubberBand;

protected:
    void inspectStyleState() const
    {
        QStyleOptionRubberBand option;
        initStyleOption(&option);

        // option.rect、option.shape、option.opaque
        // 都来自当前 QRubberBand 的真实状态。
    }
};
```

只调用继承的 `QStyleOption::initFrom(this)` 不够完整：它能填通用 state、palette 和 rect，但 `shape`、`opaque` 等 rubber band 专属字段应由 `QRubberBand::initStyleOption()` 填充。

## 7. 在自定义 style 中绘制

`QStyle::CE_RubberBand` 使用的 option 类型是 `QStyleOptionRubberBand`：

```cpp
#include <QProxyStyle>
#include <QStyleOptionRubberBand>

class SelectionStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_RubberBand) {
            if (const auto *band =
                    qstyleoption_cast<const QStyleOptionRubberBand *>(option)) {
                if (band->shape == QRubberBand::Line) {
                    // 可以为线形预览提供与矩形框选不同的局部外观。
                }
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

不要在 `drawControl()` 中改变 `QRubberBand` 的 geometry 或调用 `show()/hide()`。几何更新属于鼠标事件流程；绘制函数只根据当前快照画图。

## 8. 生命周期与常见误区

`QStyleOptionRubberBand` 是轻量值类型，不拥有 `QRubberBand`、父控件或 `QPainter`。通常在当前 `paintEvent()` 栈上创建，填入后立即传给 style。

### 8.1 “反复绘制框选区域会留下残影”

不要用 XOR 自己在父控件上画线再画一次“擦除”。使用 `QRubberBand` 覆盖层，并在拖动时调用 `setGeometry()`；Qt 会处理它的重绘与擦除。

### 8.2 “从右往左拖动时框选区域错位”

用 `QRect(origin, current).normalized()`。这同样影响后续 `contains()` 和 `intersects()` 的选择逻辑。

### 8.3 “选框被其他子控件盖住”

确认 `QRubberBand` 的 parent 是你希望覆盖的容器，而不是某个更深层子控件。带 parent 的 rubber band 只在该 parent 内显示，但会保持在它的其他子控件上方。

### 8.4 “我改了 `QStyleOptionRubberBand::shape`，可见 rubber band 没变化”

option 只影响一次绘制输入。`QRubberBand` 的 shape 在构造时确定，不能用修改临时 option 的方式切换。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionRubberBand()` | 创建并以默认值初始化一份 rubber band 绘制参数。 | 默认 `shape` 是 `Line`、`opaque` 为 `true`；真实控件状态仍应由 `QRubberBand` 填充。 |
| 构造 | `QStyleOptionRubberBand(const QStyleOptionRubberBand &other)` | 创建另一个 rubber band option 的值副本。 | 复制绘制数据，不拥有可见覆盖控件、父控件或 painter。 |
| 类型常量 | `StyleOptionType::Type` | 提供值为 `SO_RubberBand` 的运行时类型标识。 | style 接收基类指针时用 `qstyleoption_cast()` 安全识别。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示 rubber band option 的数据布局版本，Qt 6.11.1 中为 `1`。 | 用于兼容识别，不是控件的显示状态。 |
| 公共字段 | `QRubberBand::Shape shape` | 指定 style 按线形还是矩形语义绘制覆盖层。 | 不是几何约束；真实 `QRubberBand` 的 shape 在构造时确定，不能靠临时 option 切换。 |
| 公共字段 | `bool opaque` | 向 style 提示是否要求以不透明方式绘制 rubber band。 | 不是 `windowOpacity` 替代品，也不直接决定鼠标事件穿透。 |
| 继承字段 | `QStyleOption::rect` | 指定当前 rubber band 应绘制的矩形区域。 | 即使是 `Line` 也要提供有效矩形；拖动计算通常使用 `normalized()`。 |
| 继承函数 | `QStyleOption::initFrom(const QWidget *)` | 填充方向、调色板、状态和矩形等通用控件绘制状态。 | 不会填充本类的 `shape` 和 `opaque`，不能替代 `QRubberBand::initStyleOption()`。 |
| 构造控件 | `QRubberBand(QRubberBand::Shape, QWidget *)` | 创建真正可见的 rubber band 覆盖控件。 | 传入合适 parent 可限制显示区域并获得对象树自动析构。 |
| 几何 | `QRubberBand::setGeometry(const QRect &)` | 更新覆盖层在 parent 坐标中的位置和尺寸。 | 从右下向左上拖动时应传 `rect.normalized()`，避免负方向几何。 |
| 初始化 | `QRubberBand::initStyleOption(QStyleOptionRubberBand *)` | 从真实 rubber band 填充完整的 style option。 | 是 `QRubberBand` 子类获取 shape、opaque 和基类状态的正确入口。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_RubberBand, ...)` | 让当前 style 绘制线形或矩形 rubber band。 | 自定义 style 应尊重 `shape`、`opaque` 和主题，不要在绘制函数里改 geometry。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionRubberBand *>(option)` | 从基类 option 安全识别 rubber band option。 | 失败返回空指针；只在当前绘制调用期间读取。 |

---

### 一句话总结

`QStyleOptionRubberBand` 是 `QRubberBand` 的绘制快照：实际交互中用 `QRubberBand` 作为覆盖控件，拖动时更新经过 `normalized()` 的 geometry，`shape` 提示线或矩形语义，`opaque` 向 style 描述绘制要求；自定义外观时再通过 `CE_RubberBand` 读取 option。
