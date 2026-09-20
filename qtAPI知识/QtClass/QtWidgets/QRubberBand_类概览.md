# Qt QRubberBand 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRubberBand>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QRubberBand`  
> 定位：临时选择框与拖拽边界提示

## 1. QRubberBand 解决什么问题

`QRubberBand` 是一个用于显示“临时范围”的轻量控件。最典型的例子是用户按住鼠标拖出一个矩形选择区域，或者在拖动、调整大小时显示一条临时边界线。

它解决的是“交互进行中，需要把当前范围画出来，但这个范围本身还不是最终内容”的问题。

```text
鼠标按下
   ↓
创建/显示 QRubberBand
   ↓
随着鼠标移动更新 geometry
   ↓
鼠标释放后隐藏并读取最终 QRect
```

它只负责视觉反馈，不负责根据范围选中数据。最终选中哪些对象，仍然要由你的业务代码判断。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 矩形拖拽选择

```cpp
#include <QMouseEvent>
#include <QRubberBand>
#include <QWidget>

class Canvas : public QWidget
{
public:
    using QWidget::QWidget;

protected:
    void mousePressEvent(QMouseEvent *event) override
    {
        origin = event->position().toPoint();
        if (!band)
            band = new QRubberBand(QRubberBand::Rectangle, this);
        band->setGeometry(QRect(origin, QSize()));
        band->show();
    }

    void mouseMoveEvent(QMouseEvent *event) override
    {
        if (band)
            band->setGeometry(QRect(origin,
                                    event->position().toPoint()).normalized());
    }

    void mouseReleaseEvent(QMouseEvent *) override
    {
        if (!band)
            return;
        const QRect selection = band->geometry();
        band->hide();
        processSelection(selection);
    }

private:
    void processSelection(const QRect &rect);

    QPoint origin;
    QRubberBand *band = nullptr;
};
```

这里 `QRubberBand` 只是画出选择范围，`processSelection()` 才是业务逻辑。

## 3. 核心使用模型

### 3.1 先选形状，再不断更新 geometry

构造时指定形状：

- `Line`：显示一条线；
- `Rectangle`：显示一个矩形。

然后用 `setGeometry()`、`move()` 或 `resize()` 更新它的范围。

### 3.2 反向拖拽时要 normalized

用户可能从右下角向左上角拖。直接用起点和终点构造矩形，可能得到负宽度或负高度；通常应调用：

```cpp
QRect rect = QRect(origin, current).normalized();
```

### 3.3 它通常只在交互过程中显示

创建后先隐藏，操作开始时 `show()`，操作结束时 `hide()`。不要把它当成长期存在的边框控件。

### 3.4 样式由当前 QStyle 决定

`QRubberBand` 会通过 `QStyleOptionRubberBand` 让当前样式决定线条、透明度和边界表现。不同平台上看到的具体样式可能不同。

## 4. 适合用在哪里

- 桌面画布的框选；
- 图片裁剪范围；
- 窗口拖动或调整大小的临时提示；
- 自定义列表、表格或场景的拖拽选区；
- 需要显示临时线段的交互。

如果范围需要长期存在并承载业务状态，应该使用真正的模型对象或自定义绘制，而不是一直保留一个 rubber band。

## 5. 常见误区

### 5.1 以为它会自动选中对象

不会。它只显示范围，选中逻辑要自己实现。

### 5.2 忘记处理反向拖拽

应使用 `QRect::normalized()`，否则从反方向拖动时范围可能不正确。

### 5.3 把它放进布局

它是覆盖在父控件上的临时视觉层，不应该占据布局空间。

### 5.4 坐标系用错

如果 rubber band 是某个画布的子控件，传给它的 geometry 应该是画布局部坐标；跨窗口或跨控件操作时要先做坐标映射。

### 5.5 操作结束后不隐藏

它的用途是临时反馈，完成后应及时隐藏或销毁。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Shape` | 定义 rubber band 的形状类型。 | `Line` 用于线条，`Rectangle` 用于矩形范围。 |
| 构造 | `QRubberBand(Shape shape, QWidget *parent = nullptr)` | 创建一个指定形状的临时范围控件。 | 形状在构造时确定。 |
| 析构 | `~QRubberBand()` | 销毁临时范围控件。 | 通常由父控件管理。 |
| 查询 | `shape() const` | 返回当前 rubber band 的形状。 | 创建后通常不改变。 |
| 几何 | `setGeometry(const QRect &rect)` | 设置临时范围的矩形。 | 拖拽更新时最常用；坐标应属于父控件坐标系。 |
| 几何 | `setGeometry(int x, int y, int w, int h)` | 用四个整数设置范围矩形。 | 是 `QRect` 重载的便捷形式。 |
| 几何 | `move(int x, int y)` | 移动 rubber band 的左上角。 | 不改变宽高。 |
| 几何 | `move(const QPoint &p)` | 用点移动 rubber band。 | 不改变宽高。 |
| 几何 | `resize(int w, int h)` | 修改 rubber band 的宽高。 | 不改变左上角位置。 |
| 几何 | `resize(const QSize &size)` | 用 `QSize` 修改宽高。 | 是整数重载的便捷形式。 |
| 事件 | `event(QEvent *event)` | 处理控件级通用事件。 | 由 Qt 内部协调显示和状态变化。 |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制临时线条或矩形边界。 | 通常由框架调用。 |
| 样式 | `initStyleOption(QStyleOptionRubberBand *option) const` | 准备给当前样式绘制的选项。 | 子类化定制时要保留 shape 和状态。 |
| 状态 | `changeEvent(QEvent *event)` | 处理样式、字体等状态变化。 | 让外观随应用设置更新。 |
| 状态 | `showEvent(QShowEvent *)` | 处理 rubber band 显示。 | 可用于开始一次临时交互。 |
| 状态 | `resizeEvent(QResizeEvent *)` | 处理范围尺寸改变。 | 通常不需要业务层重写。 |
| 状态 | `moveEvent(QMoveEvent *)` | 处理范围位置改变。 | 通常不需要业务层重写。 |

## 7. 一句话总结

`QRubberBand` 是交互过程中的临时范围提示层，最适合拖拽框选、裁剪和边界反馈；它画范围，但不替你完成范围背后的业务逻辑。
