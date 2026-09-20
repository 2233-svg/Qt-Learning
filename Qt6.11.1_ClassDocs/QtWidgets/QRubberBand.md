# QRubberBand

> Qt 6.11.1 · Qt Widgets · 来自 `QRubberBand`

## 1. 先建立直觉

`QRubberBand` 是一个临时的视觉标记：用户拖动鼠标时出现的虚线框、选择框、拖拽目标轮廓，很多都可以用它完成。它不是布局控件，也不是选择模型；它只是把“当前用户正在划出的区域”用平台风格画出来。

它的价值在于轻：创建后设置父对象、调用 `setGeometry()`、`show()` / `hide()` 就能工作。你不必自己处理虚线、透明背景、平台主题差异，也不需要把临时选择框纳入正式 UI 布局。

## 2. 类说明

`QRubberBand` 继承自 `QWidget`，可以显示成矩形或线条。矩形常用于框选区域，线条常用于拖放插入位置、splitter 预览线或临时定位提示。

实际选择逻辑通常在外部控件完成，例如在 `QWidget::mousePressEvent()` 记录起点，在 `mouseMoveEvent()` 更新 rubber band 的 geometry，在 `mouseReleaseEvent()` 隐藏它并根据最终矩形选择对象。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QRubberBand(QRubberBand::Shape, QWidget *)` | 创建矩形或线形 rubber band。父控件决定坐标系和裁剪范围。 |
| `Shape::Line` | 显示为一条线，适合插入位置、拖拽落点、临时分隔线。 |
| `Shape::Rectangle` | 显示为矩形框，适合框选、截图区域、裁剪范围预览。 |
| `shape()` | 返回当前 rubber band 的形状。 |
| `setGeometry(const QRect &)` | 更新显示区域。拖动过程中最常用。 |
| `move()` / `resize()` | 分别移动或调整大小；简单场景可用，拖选更推荐一次性设置 geometry。 |
| `show()` | 显示临时标记。通常在鼠标按下或开始拖动后调用。 |
| `hide()` | 隐藏临时标记。通常在鼠标释放、取消操作或拖拽离开时调用。 |
| `paintEvent()` | Qt 内部按样式绘制。子类化时可自定义外观，但多数情况下不需要。 |
| `changeEvent()` | 样式、调色板变化时 rubber band 可随主题刷新。 |

## 4. 典型框选流程

```cpp
void Canvas::mousePressEvent(QMouseEvent *event)
{
    origin = event->pos();
    rubberBand->setGeometry(QRect(origin, QSize()));
    rubberBand->show();
}

void Canvas::mouseMoveEvent(QMouseEvent *event)
{
    rubberBand->setGeometry(QRect(origin, event->pos()).normalized());
}

void Canvas::mouseReleaseEvent(QMouseEvent *event)
{
    rubberBand->hide();
    const QRect selected = QRect(origin, event->pos()).normalized();
    selectItemsIn(selected);
}
```

`normalized()` 很重要：用户可能向左上拖，也可能向右下拖；不归一化会得到负宽高矩形，后续命中检测很容易出错。

## 5. 使用场景

在文件管理器里拖框选择图标、图形编辑器里框选对象、截图工具里标记捕获范围、表格或时间轴里显示拖拽范围、可视化设计器里提示控件插入位置，都是 `QRubberBand` 的典型场景。

如果你的目标是“持久显示一个边框”，不要用它。长期装饰应该交给 widget 样式表、`QFrame`、自定义 paint 或 delegate；`QRubberBand` 更适合短暂、交互中的视觉反馈。

## 6. 常见坑与经验

父对象会影响坐标。把 rubber band 放到画布子控件上时，geometry 用画布坐标；放到顶层窗口上时，可能需要 `mapTo()` / `mapFrom()` 转换。

`QRubberBand` 只显示范围，不替你维护选中项。框选结束后，应把最终矩形传给自己的模型、场景或数据结构，再更新真实选中状态。

在高 DPI 或复杂样式下，自己画虚线框很容易和平台观感不一致。除非产品需要强定制视觉，否则优先让 `QRubberBand` 走当前 style。
