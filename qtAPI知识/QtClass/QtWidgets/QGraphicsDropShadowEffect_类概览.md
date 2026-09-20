<!-- 依据 Qt 6.11.1 头文件 qgraphicseffect.h 整理。 -->

# QGraphicsDropShadowEffect 深入笔记

> 头文件：`#include <QGraphicsDropShadowEffect>`  
> 模块：`Qt6::Widgets`  
> 继承：`QObject -> QGraphicsEffect -> QGraphicsDropShadowEffect`

## 1. 它解决什么问题

`QGraphicsDropShadowEffect` 会先绘制目标内容的半透明副本，再按指定偏移和模糊半径把它放到原内容后面，从而制造悬浮、层级和深度感。

它适合：

- 弹窗、卡片、菜单与浮动工具栏：把前景从背景中分离出来。
- 无边框控件：用柔和阴影提示控件边缘。
- Graphics View 中的节点：强调被选中或可拖动的图元。

它不适合：

- 对整张大页面或持续滚动的复杂列表长期做大阴影。
- 需要内阴影、多个光源、非均匀模糊或严格符合设计软件渲染结果的场景。
- 把阴影当布局间距。阴影是绘制效果，不会替控件系统留下布局空间。

## 2. 最小可用代码与所有权

```cpp
#include <QGraphicsDropShadowEffect>
#include <QWidget>

auto *shadow = new QGraphicsDropShadowEffect;
shadow->setBlurRadius(16.0);
shadow->setOffset(0.0, 4.0);
shadow->setColor(QColor(0, 0, 0, 76));

card->setGraphicsEffect(shadow);
```

调用 `QWidget::setGraphicsEffect()` 或 `QGraphicsItem::setGraphicsEffect()` 后，目标会接管效果对象。不要再手动删除 `shadow`，也不要把它安装到第二个目标上。

一个目标只能有一个 `QGraphicsEffect`。再调用一次 `setGraphicsEffect()` 会替换当前阴影，而不是把多个阴影或“阴影 + 模糊”自动叠加。复合效果要么拆到父子对象，要么实现自定义效果。

## 3. 阴影由四个量决定

### `offset`、`xOffset`、`yOffset`

`offset` 决定阴影相对原内容平移多少。默认是 `(8, 8)`，即向右下投射。

```cpp
shadow->setOffset(QPointF(6.0, 8.0)); // 完整二维偏移
shadow->setOffset(6.0, 8.0);          // 同上
shadow->setOffset(5.0);               // X 和 Y 都设为 5
shadow->setXOffset(0.0);              // 只改 X
shadow->setYOffset(3.0);              // 只改 Y
```

这里最容易误解的一点是：阴影偏移使用**设备坐标**，不是控件或图元的逻辑坐标。控件本身缩放或 Graphics View 视图缩放时，内容的几何关系可能变化，但阴影偏移仍以设备坐标定义。想得到稳定的视觉距离时，这正是优点；想让阴影与图元一起按比例缩放时，则要额外设计或使用自定义效果。

`xOffset` 与 `yOffset` 是 `offset` 的分量属性，它们没有独立的通知信号。无论是 `setOffset()`、`setXOffset()` 还是 `setYOffset()`，变化都通过 `offsetChanged(const QPointF &)` 通知。

### `blurRadius`

`blurRadius` 决定阴影边缘扩散程度，默认值为 `1`。数值越大，阴影越柔和、覆盖面积越大、绘制代价也越高。

```cpp
shadow->setBlurRadius(0.0);  // 硬边投影
shadow->setBlurRadius(12.0); // 常见柔和卡片阴影
shadow->setBlurRadius(28.0); // 很柔和，但成本明显增加
```

半径并不会自动让阴影更深。阴影的“轻重”要同时看 `color` 的 alpha、偏移距离和模糊半径：大半径加高不透明度会变成脏灰块，小半径加低 alpha 往往更接近细锐阴影。

### `color`

`color` 是阴影颜色，默认是深灰色。实际 UI 通常更应调 alpha，而非简单把颜色改成纯黑：

```cpp
shadow->setColor(QColor(0, 0, 0, 64));   // 柔和黑色阴影
shadow->setColor(QColor(20, 60, 120, 70)); // 有色环境光
```

在浅色界面，低 alpha 的中性暗色通常比纯黑更自然；在深色界面，阴影可能不够可见，应该根据背景对比度调整，而不是机械复用同一套参数。

## 4. 参数如何搭配

| 目标视觉 | 典型组合 | 说明 |
| --- | --- | --- |
| 轻微悬浮 | 半径 `8-12`，偏移 `(0, 2-4)`，低 alpha | 适合表单卡片、菜单。 |
| 明显浮层 | 半径 `16-24`，偏移 `(0, 6-10)`，中低 alpha | 适合模态框、拖拽中的项目。 |
| 贴边层级 | 半径 `4-8`，偏移 `(0, 1-2)`，低 alpha | 适合工具栏、输入框。 |
| 硬投影 | 半径接近 `0`，明显偏移 | 更像像素风或刻意的平面设计。 |

这些是视觉起点而非固定配方。最终数值应根据控件尺寸、背景色、屏幕 DPI 和产品整体阴影系统统一调整。

## 5. 有效边界、裁剪和性能

阴影可在目标原始矩形外绘制，偏移和模糊半径越大，输出边界越大。`QGraphicsDropShadowEffect::boundingRectFor()` 会根据原矩形推导可容纳阴影的有效边界，框架用它避免把阴影裁掉。

业务代码不应自己调用 `boundingRectFor()` 来绘制阴影；遇到裁边问题应先排查：

1. 父控件、视图或滚动区域是否显式裁剪了子内容。
2. 阴影目标是否贴着可视区域边缘。
3. 是否将效果换成了自定义效果却忘记扩大自己的 `boundingRectFor()`。

每次修改偏移、半径、颜色，都可能让框架重新生成效果输出。对大尺寸目标做连续属性动画会有可见成本。拖动窗口、滚动长列表或缩放复杂场景时，可以暂时禁用阴影，交互结束后再恢复。

## 6. 与 `QGraphicsBlurEffect` 的边界

阴影也会产生模糊边缘，但它模糊的是目标的一个偏移副本，并把原内容保持清晰地叠在上面；`QGraphicsBlurEffect` 则直接模糊目标内容本身。

```text
DropShadowEffect: 清晰的原内容 + 模糊、偏移的副本
BlurEffect:       模糊后的原内容
```

因此，给文字加 `QGraphicsDropShadowEffect` 后文字仍清晰；给文字加 `QGraphicsBlurEffect` 后文字本身会模糊。

## 7. API 逐项说明

### 属性读写

- `offset()` / `setOffset(...)`：读取或修改二维阴影偏移；提供 `QPointF`、`(dx, dy)` 与单个 `d` 三种设置方式。
- `xOffset()` / `setXOffset(qreal)`：只读取或修改 X 分量。
- `yOffset()` / `setYOffset(qreal)`：只读取或修改 Y 分量。
- `blurRadius()` / `setBlurRadius(qreal)`：读取或修改阴影柔化范围。
- `color()` / `setColor(const QColor &)`：读取或修改阴影颜色和 alpha。

### 框架接口与通知

- `boundingRectFor(const QRectF &rect) const`：计算能够装下阴影的有效边界。
- `draw(QPainter *)`：受保护的实际绘制实现；现成类已经完成，业务代码不调用。
- `offsetChanged()`、`blurRadiusChanged()`、`colorChanged()`：对应属性改变时发出。

从 `QGraphicsEffect` 继承的 `setEnabled()`、`update()` 与 `enabledChanged()` 仍然可用；自定义效果相关接口见 [QGraphicsEffect_类概览.md](QGraphicsEffect_类概览.md)。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsDropShadowEffect(QObject *parent = nullptr)` | 创建阴影效果。 | 安装给目标后，目标接管对象。 |
| 析构 | `~QGraphicsDropShadowEffect()` | 销毁阴影效果。 | 已安装时通常无需手动删除。 |
| 属性 | `offset : QPointF` | 保存阴影的二维偏移。 | 默认 `(8, 8)`；使用设备坐标。 |
| 读取 | `QPointF offset() const` | 读取完整偏移量。 | 用于同时检查 X、Y 两个分量。 |
| 设置/槽 | `void setOffset(const QPointF &ofs)` | 设置完整偏移量。 | 是三个偏移 setter 最通用的版本。 |
| 设置/槽 | `void setOffset(qreal dx, qreal dy)` | 分别设置 X、Y 偏移。 | 等价于传入 `QPointF(dx, dy)`。 |
| 设置/槽 | `void setOffset(qreal d)` | 将 X、Y 都设置为 `d`。 | 适合对角线方向的等距投影。 |
| 属性 | `xOffset : qreal` | 保存偏移的 X 分量。 | 修改后发出的是 `offsetChanged()`。 |
| 读取 | `qreal xOffset() const` | 读取 X 偏移。 | 不会单独反映 Y 分量。 |
| 设置/槽 | `void setXOffset(qreal dx)` | 仅修改 X 偏移。 | 保留当前 Y 偏移。 |
| 属性 | `yOffset : qreal` | 保存偏移的 Y 分量。 | 修改后发出的是 `offsetChanged()`。 |
| 读取 | `qreal yOffset() const` | 读取 Y 偏移。 | 不会单独反映 X 分量。 |
| 设置/槽 | `void setYOffset(qreal dy)` | 仅修改 Y 偏移。 | 保留当前 X 偏移。 |
| 属性 | `blurRadius : qreal` | 保存阴影的模糊半径。 | 默认 `1`；增大时面积和成本也会增加。 |
| 读取 | `qreal blurRadius() const` | 读取模糊半径。 | 与颜色 alpha 一起决定视觉轻重。 |
| 设置/槽 | `void setBlurRadius(qreal blurRadius)` | 设置模糊半径。 | 动画大面积阴影前先评估性能。 |
| 属性 | `color : QColor` | 保存阴影颜色。 | alpha 往往比 RGB 更影响阴影自然度。 |
| 读取 | `QColor color() const` | 读取阴影颜色。 | 同时包含 alpha 通道。 |
| 设置/槽 | `void setColor(const QColor &color)` | 设置阴影颜色。 | 改颜色也会触发效果更新。 |
| 框架接口 | `QRectF boundingRectFor(const QRectF &rect) const` | 返回包含模糊和偏移后的有效边界。 | 框架调用，业务代码通常不直接调用。 |
| 信号 | `void offsetChanged(const QPointF &offset)` | 通知任意偏移分量发生变化。 | 没有单独的 X/Y 通知信号。 |
| 信号 | `void blurRadiusChanged(qreal blurRadius)` | 通知模糊半径变化。 | 动画过程中会高频触发。 |
| 信号 | `void colorChanged(const QColor &color)` | 通知阴影颜色变化。 | 可用于同步主题或属性面板。 |
| 受保护函数 | `void draw(QPainter *painter)` | 执行实际阴影绘制。 | 现成类已实现，普通业务代码不直接调用。 |

## 9. 排查清单

1. 阴影完全不可见：确认效果未被替换、未禁用，并检查 alpha 是否为 `0`。
2. 阴影方向不符合预期：检查 `offset()`，不要把它误当 scene 或布局坐标。
3. 阴影被裁掉：检查目标是否贴边，以及上层是否开启了裁剪。
4. 列表滚动卡顿：降低半径、作用面积或在交互中暂时禁用效果。
5. 设置 X/Y 后槽没有反应：监听 `offsetChanged()`，而不是寻找不存在的 `xOffsetChanged()`、`yOffsetChanged()`。

### 一句话总结

`QGraphicsDropShadowEffect` 通过“偏移副本 + 模糊 + 颜色 alpha”给目标制造层级；真正决定效果稳定性的，是设备坐标偏移、单效果所有权，以及对大面积动态阴影的性能克制。
