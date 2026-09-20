# Qt QScrollBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QScrollBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSlider -> QScrollBar`  
> 定位：用滑块位置表达可见窗口在可滚动内容中的位置

## 1. QScrollBar 与 QSlider 的区别

两者都来自 `QAbstractSlider`，都保存整数范围与当前 value；但它们表达的语义不同：

```text
QSlider:    “把音量设为多少？”
QScrollBar: “内容窗口的左上角现在位于哪里？”
```

滚动条通常由三类区域组成：

```text
[减小箭头] [滑块前 page 区] [slider] [滑块后 page 区] [增大箭头]
```

- 箭头触发 single step，适合精确前进一行、一项或若干像素；
- slider 可拖动，表示当前位置；
- page 区点击或 PageUp/PageDown 触发 page step；
- slider 的视觉长度通常表示“当前可见部分占总内容的比例”。

`QScrollArea`、`QAbstractItemView`、`QTextEdit` 等控件内部已经有滚动条。只有自己实现 `QAbstractScrollArea`、同步多个视图、或需要一个独立滚动位置控制器时，才常常直接构造 `QScrollBar`。

## 2. 滚动范围的正确计算

设内容共有 100 行，视口一次显示 20 行：

```cpp
scrollBar->setMinimum(0);
scrollBar->setMaximum(80);
scrollBar->setPageStep(20);
scrollBar->setSingleStep(1);
```

逻辑是：

```text
documentLength = maximum - minimum + pageStep
100            = 80      - 0       + 20
```

当 value 为 0，显示第 0 到 19 行；当 value 为 80，显示第 80 到 99 行。若 maximum 错设成 99，用户拖到底部时会得到不存在的“第 99 行作为首行、后面还应有 20 行”的语义。

适用于很多普通滚动模型的通用公式：

```cpp
const int maxValue = qMax(0, contentLength - visibleLength);
scrollBar->setRange(0, maxValue);
scrollBar->setPageStep(visibleLength);
```

scroll bar 的范围与控件在屏幕上的像素长度没有直接关系。内容可用“行号”“字符偏移”“时间单位”或“逻辑像素”表达，不一定是 widget 的真实像素。Qt 虽能处理很大整数，但当前屏幕上超过约 100,000 像素的直接滚动范围已很难精确操作；超大画布、海量行应改用缩放或分段映射。

## 3. 最小示例：用滚动条驱动自定义内容位置

```cpp
auto *bar = new QScrollBar(Qt::Vertical);
bar->setRange(0, 980);
bar->setPageStep(120);
bar->setSingleStep(20);

connect(bar, &QScrollBar::valueChanged,
        canvas, [canvas](int yOffset) {
    canvas->setVerticalOffset(yOffset);
    canvas->update();
});
```

如果 `canvas` 的逻辑内容高度是 1100、可见高度是 120，那么 maximum 应为 `1100 - 120 = 980`。在真正的 `QAbstractScrollArea` 子类里，应在内容大小和 `viewport()->size()` 变化时重新设置 range 和 pageStep，而不是只在构造时算一次。

## 4. 继承自 QAbstractSlider 的关键配置

```cpp
scrollBar->setRange(0, maximumOffset);
scrollBar->setValue(savedOffset);
scrollBar->setSingleStep(lineHeight);
scrollBar->setPageStep(viewportHeight);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 范围 | `minimum` / `maximum` | 定义允许的最小和最大滚动偏移 | 最大值通常不是内容总高度，而是 `内容大小 - 视口大小` |
| 当前位置 | `value` | 表示当前可见区域在内容中的偏移 | 业务滚动位置通常读写它；设置越界值会被夹到合法范围 |
| 步进 | `singleStep` | 定义方向键、箭头按钮、滚轮等小步移动量 | 常按一行、一格或一个逻辑单位设置；太大会让细粒度滚动困难 |
| 步进 | `pageStep` | 定义 PageUp/PageDown 和点击滑槽空白区域时的大步移动量 | 通常接近视口大小，也会影响 slider 长度的视觉比例 |
| 拖动提交 | `tracking` | 控制拖动 slider 时是否持续提交 `valueChanged()` | 内容重绘很重时可关闭，并在释放后再提交完整更新 |
| 拖动提交 | `sliderPosition` | 表示拖动过程中的手柄位置 | `tracking` 关闭时它可能还没同步成 `value`，适合轻量预览 |

绝大多数滚动条保持 tracking 开启，因为滚动通常需要拖动时实时更新。若内容重绘极重，可关闭 tracking，并用 `sliderMoved()` 绘制轻量预览、在 `sliderReleased()` 后提交完整渲染。

## 5. 键盘焦点与方向键

`QScrollBar` 默认的 `focusPolicy()` 是 `Qt::NoFocus`。这是为了避免普通界面中 Tab 焦点停到每一根滚动条上。若把它当独立导航控件使用，可显式启用焦点：

```cpp
scrollBar->setFocusPolicy(Qt::StrongFocus);
```

启用后，默认键盘行为是：

| 按键 | 行为 |
| --- | --- |
| Left / Right | 水平滚动条按 single step 移动。 |
| Up / Down | 垂直滚动条按 single step 移动。 |
| PageUp / PageDown | 按 page step 移动。 |
| Home / End | 跳到 minimum / maximum。 |

`invertedControls` 会反转键盘、滚轮的增减方向。`invertedAppearance` 对滚动条的视觉效果取决于 style，许多 style 会忽略它；不要依赖它实现右到左或倒序内容。

## 6. 信号与同步多个视图

滚动条继承 `QAbstractSlider` 的完整通知集，最常用的是：

```cpp
connect(leftView->verticalScrollBar(), &QScrollBar::valueChanged,
        rightView->verticalScrollBar(), &QScrollBar::setValue);
```

| 信号 | 滚动场景中的用途 |
| --- | --- |
| `valueChanged(int)` | 位置已提交；同步内容、保存滚动位置、联动另一个视图。 |
| `sliderMoved(int)` | 用户拖动中；做缩略图预览或悬浮位置提示。 |
| `sliderPressed()` / `sliderReleased()` | 拖动开始与结束；暂停昂贵刷新或最后一次提交。 |
| `rangeChanged(int, int)` | 内容或 viewport 尺寸变化后范围更新。 |
| `actionTriggered(int)` | 箭头、翻页、Home/End、拖动等动作发生。 |

两个 scroll bar 双向连接时要小心反馈。Qt 在 value 没变时不会反复发 `valueChanged()`，简单同步通常可行；若还要按比例换算、互相改变 range 或做动画，使用 `QSignalBlocker` 或一个统一控制器更可靠。

## 7. 右键菜单与样式扩展

Qt 6.10 引入了标准右键菜单创建 API：

```cpp
void MyScrollBar::contextMenuEvent(QContextMenuEvent *event)
{
    QMenu *menu = createStandardContextMenu(event->pos());
    menu->addAction("回到顶部", this, [this] {
        setValue(minimum());
    });
    menu->exec(event->globalPos());
    delete menu;
}
```

`createStandardContextMenu()` 返回的 `QMenu *` 所有权交给调用者。可以立即 `exec()` 后 delete，也可以保存后设置 `Qt::WA_DeleteOnClose`。若完全不想提供右键菜单，设置 `setContextMenuPolicy(Qt::NoContextMenu)`；style 也可通过 `SH_ScrollBar_ContextMenu` 影响默认行为。

自定义 QScrollBar 外观时，用 `initStyleOption(QStyleOptionSlider *)` 准备当前状态给 `QStyle`，不要靠猜测 slider rect 或手写与平台 style 脱节的箭头几何。

## API 速查表
### 8.1 QScrollBar 自身 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QScrollBar(QWidget *parent = nullptr)` | 创建一个滚动条控件 | 默认用于垂直滚动条场景；独立使用时通常马上设置方向、range、page step |
| 构造 | `QScrollBar(Qt::Orientation orientation, QWidget *parent = nullptr)` | 创建指定方向的滚动条 | 横向独立滚动条显式传 `Qt::Horizontal`；方向决定键盘和样式绘制 |
| 生命周期 | `~QScrollBar()` | 销毁滚动条 | 如果滚动条来自 `QScrollArea`、item view 或文本控件，通常不应手工 delete |
| 菜单 | `createStandardContextMenu(QPoint position)` | 创建标准滚动条右键菜单 | Qt 6.10 引入；未禁用 context menu 时可用，返回的 `QMenu *` 所有权归调用者 |
| 菜单 | `contextMenuEvent(QContextMenuEvent *event)` | 处理右键菜单事件 | 重写可禁用、替换或扩展菜单；完全禁用可设置 `Qt::NoContextMenu` |
| 样式 | `initStyleOption(QStyleOptionSlider *option) const` | 填充当前滚动条的样式参数 | 派生类想沿用平台样式绘制时使用，不要自己猜测箭头和滑块几何 |
| 尺寸 | `sizeHint() const` | 返回推荐尺寸 | 由当前 style、方向和平台指标决定，不由内容总长度直接决定 |
| 事件 | `event(QEvent *event)` | 处理通用事件入口 | 普通业务代码不直接调用，派生类重写时要保留父类滚动语义 |
| 事件 | `hideEvent(QHideEvent *event)` | 处理隐藏事件 | 派生类可在这里清理悬浮提示、拖动状态或临时菜单 |
| 鼠标 | `mousePressEvent(QMouseEvent *event)` | 处理箭头、page 区或 slider 被按下 | 重写时要维持 single step、page step 和拖动开始语义 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *event)` | 处理 slider 拖动 | 通常让基类更新 `sliderPosition` 和 `value`；重写容易破坏平台交互 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *event)` | 处理拖动或点击结束 | 影响 `sliderReleased()` 以及 `tracking=false` 时的提交时机 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制滚动条各个子控件 | 自定义风格优先用 `QStyle` 或 stylesheet，保持平台一致性 |
| 变化通知 | `sliderChange(SliderChange change)` | range、value、step 等滑块状态改变时被调用 | 派生类可用来更新内部几何缓存或触发重绘 |
| 滚轮 | `wheelEvent(QWheelEvent *event)` | 处理鼠标滚轮滚动 | 受 `singleStep()`、`pageStep()` 和 `invertedControls()` 影响 |

### 8.2 继承自 QAbstractSlider、但滚动条最常用的 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 范围 | `minimum() const` / `setMinimum(int)` | 读取或设置最小滚动偏移 | 通常为 `0`，表示内容开头 |
| 范围 | `maximum() const` / `setMaximum(int)` | 读取或设置最大滚动偏移 | 常用 `contentLength - visibleLength`，不要误设为内容最后一个索引 |
| 范围 | `setRange(int min, int max)` | 一次设置可滚动偏移范围 | 内容尺寸或 viewport 尺寸变化后要重新计算 |
| 位置 | `value() const` / `setValue(int value)` | 读取或设置当前滚动位置 | 通常表示可见窗口左上角在内容中的偏移 |
| 位置 | `sliderPosition() const` / `setSliderPosition(int position)` | 读取或设置拖动中的 slider 位置 | `tracking=false` 时可用于拖动预览，未必等于已提交 `value()` |
| 步长 | `pageStep() const` / `setPageStep(int step)` | 设置或读取一次翻页距离 | 通常等于可见长度，也常影响 slider 视觉长度 |
| 步长 | `singleStep() const` / `setSingleStep(int step)` | 设置或读取小步滚动距离 | 文本常用一行高度，图像或画布常用固定逻辑像素 |
| 提交策略 | `hasTracking() const` / `setTracking(bool enable)` | 控制拖动 slider 时是否立即提交 `value` | 实时滚动通常保持 `true`；重绘极重时可关闭并在释放后提交 |
| 动作 | `triggerAction(SliderAction action)` | 主动触发标准滚动动作 | 自定义按钮、快捷键或同步控制器可用它复用滚动条语义 |
| 方向 | `invertedControls() const` / `setInvertedControls(bool)` | 反转滚轮和键盘增减方向 | 不等于反转内容坐标，也不等于完整 RTL 布局支持 |
| 方向 | `invertedAppearance() const` / `setInvertedAppearance(bool)` | 请求反转视觉方向 | 对滚动条是否明显生效取决于 style，不应作为业务坐标设计的唯一依据 |
| 信号 | `valueChanged(int value)` | 滚动位置提交变化时发出 | 同步内容位置、保存滚动状态、联动另一个视图最常用 |
| 信号 | `rangeChanged(int min, int max)` | 滚动范围变化时发出 | 内容或 viewport resize 后同步附属 UI |
| 信号 | `sliderMoved(int position)` | 拖动中手柄位置变化时发出 | 大内容可用它显示缩略预览或位置提示 |
| 信号 | `sliderPressed()` / `sliderReleased()` | slider 拖动开始和结束时发出 | 可用于暂停昂贵刷新、显示/隐藏浮层、最后一次提交 |
| 信号 | `actionTriggered(int action)` | 标准滚动动作发生后发出 | 用于区分 single step、page step、Home/End、拖动等来源 |

## 9. 一句话总结

`QScrollBar` 的 value 不是“内容总长度”，而是可见窗口的偏移；正确的 `maximum` 通常等于内容长度减去 page step，page step 同时表达一次翻页距离和可见比例。
