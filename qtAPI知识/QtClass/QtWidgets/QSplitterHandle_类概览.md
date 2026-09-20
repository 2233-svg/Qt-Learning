# Qt QSplitterHandle 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QSplitterHandle>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget`

## 它解决什么问题

`QSplitterHandle` 是 `QSplitter` 中间那条可拖动分隔条。用户拖动它时，`QSplitter` 根据位置重新分配两侧 widget 的空间。多数程序只需要使用 `QSplitter`，不需要直接创建 handle；只有在你要改变分隔条外观、尺寸提示、鼠标行为或附加按钮时，才会派生 `QSplitterHandle`。

它解决的是“自定义 splitter 拖动手柄”问题，而不是普通布局问题。真正管理子控件尺寸、折叠策略、合法范围和状态保存的是 `QSplitter`。

## 实际使用场景

- 把普通分隔线画成更明显的拖动手柄。
- 在分隔条上放折叠按钮、更多菜单或方向图标。
- 改写拖动逻辑，让用户拖动时吸附到固定位置。
- 按产品设计统一 splitter 的 hover、pressed、focus 外观。
- 在复杂 IDE/编辑器布局中做可折叠面板边界。

如果只是想改分隔条宽度，用 `QSplitter::setHandleWidth()` 即可；如果只是想换颜色，优先考虑样式表或自定义 `QStyle`。只有行为或绘制确实需要代码控制时再派生 handle。

## 正确创建方式

`QSplitterHandle` 通常不由业务代码手动 new 后塞进布局，而是通过派生 `QSplitter` 并重写 `createHandle()`：

```cpp
class MySplitter : public QSplitter
{
protected:
    QSplitterHandle *createHandle() override
    {
        return new MySplitterHandle(orientation(), this);
    }
};
```

构造函数需要方向和所属 splitter。parent 必须是 `QSplitter *`，因为 handle 要回调 splitter 完成合法位置计算和尺寸调整。

## 拖动语义

`orientation()` 描述 splitter 的方向：水平 splitter 的 handle 左右拖动，垂直 splitter 的 handle 上下拖动。

`opaqueResize()` 来自 splitter 设置。为 true 时，拖动过程中实时调整子控件尺寸；为 false 时，拖动时通常显示橡皮筋，释放后再调整。这影响自定义鼠标事件里应如何给用户反馈。

派生类可以在鼠标事件中调用受保护的 `moveSplitter(pos)`。`pos` 是分隔条目标位置，按 splitter 坐标系从左或从上计算。Qt 文档特别强调，右到左布局下也按左侧坐标计算，不要自行反转。

`closestLegalPosition(pos)` 返回满足最小尺寸、最大尺寸、折叠规则后的最近合法位置。自定义吸附或快捷移动时，应先用它校正目标位置。

## 绘制与尺寸

默认 `paintEvent()` 会按当前 style 绘制 splitter handle。派生类如果完全自绘，可以使用 `QStyleOption` 和 `QStylePainter` 保持平台风格，也可以按产品设计绘制 hover/pressed 状态。

`sizeHint()` 给 splitter 计算 handle 占用空间。它和 `QSplitter::handleWidth()`、当前 style、方向都有关。不要让 size hint 在 hover 或 pressed 时大幅变化，否则拖动时布局会跳动。

## 常见误区

- 不要脱离 `QSplitter` 单独使用 `QSplitterHandle`；它依赖 splitter 计算合法位置和执行移动。
- 不要把 `moveSplitter()` 的位置理解为 handle 局部坐标；它是 splitter 坐标系中的位置。
- 不要在 RTL 布局下自行反转 `pos`，Qt 的规则仍然从左算。
- 自绘 handle 时别忽略高 DPI、hover、pressed、disabled 和 focus 状态。
- 只改宽度时不必派生 handle，`QSplitter::setHandleWidth()` 更直接。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSplitterHandle(Qt::Orientation orientation, QSplitter *parent)` | 创建属于某个 splitter 的 handle。 | parent 必须是对应 `QSplitter`；通常由 `QSplitter::createHandle()` 返回。 |
| 析构 | `~QSplitterHandle()` | 销毁 handle。 | 生命周期由所属 splitter 管理。 |
| 方向 | `void setOrientation(Qt::Orientation orientation)` | 设置 handle 对应的 splitter 方向。 | 一般由 splitter 内部同步，业务代码很少直接调用。 |
| 方向 | `Qt::Orientation orientation() const` | 返回 handle 方向。 | 决定拖动轴和绘制方向。 |
| 拖动模式 | `bool opaqueResize() const` | 查询拖动时是否实时调整子控件。 | 来自 splitter 设置，影响拖动反馈。 |
| 所属对象 | `QSplitter *splitter() const` | 返回拥有该 handle 的 splitter。 | 不转移所有权；不要删除返回指针。 |
| 尺寸 | `QSize sizeHint() const` | 返回 handle 推荐尺寸。 | 自定义时保持稳定，避免布局跳动。 |
| 绘制 | `void paintEvent(QPaintEvent *)` | 绘制分隔条。 | 自绘时注意当前 style、方向和状态。 |
| 鼠标 | `void mousePressEvent(QMouseEvent *)` | 处理开始拖动。 | 派生类改写时要保存必要的拖动起点。 |
| 鼠标 | `void mouseMoveEvent(QMouseEvent *)` | 处理拖动移动。 | 需要移动 splitter 时调用 `moveSplitter()`。 |
| 鼠标 | `void mouseReleaseEvent(QMouseEvent *)` | 处理拖动结束。 | 非 opaque resize 场景通常在释放时提交最终位置。 |
| 尺寸事件 | `void resizeEvent(QResizeEvent *)` | handle 尺寸变化时调用。 | 有内部按钮或热点区域时可在这里重新布局。 |
| 通用事件 | `bool event(QEvent *)` | 处理 hover、style、tooltip 等通用事件。 | 改写时保留基类处理，除非明确接管。 |
| 移动 | `void moveSplitter(int pos)` | 请求 splitter 把 handle 移到指定位置。 | `pos` 是 splitter 坐标系，从左或从上计算。 |
| 合法位置 | `int closestLegalPosition(int pos)` | 返回离目标最近的合法 splitter 位置。 | 会考虑子控件最小尺寸、折叠规则和 splitter 约束。 |

## 一句话总结

`QSplitterHandle` 是 `QSplitter` 的可拖动分隔条扩展点：自定义它时，外观可以自己画，但尺寸分配和合法位置仍要交给 splitter 规则。
