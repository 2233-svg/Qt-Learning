# QGraphicsAnchor

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsAnchor`

## 1. 先建立直觉

`QGraphicsAnchor` 是 `QGraphicsAnchorLayout` 中的一条锚点约束。它连接两个布局项的边，例如“按钮左边距面板左边 8 像素”或“输入框右边贴住容器右边”。

它本身不可见，也不直接管理 item。它只是布局求解中的一条关系，可以设置间距和尺寸策略。

## 2. 类说明

`QGraphicsAnchor` 继承自 `QObject`。通常不手动构造，而是由 `QGraphicsAnchorLayout::addAnchor()` 返回。拿到 anchor 后可以设置 spacing、size policy。

锚点布局适合关系式布局，而不是简单行列布局。布局项之间的边缘关系越明确，anchor 越有价值。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setSpacing(qreal)` / `spacing()` | 设置或读取该锚点连接的间距。 |
| `unsetSpacing()` | 清除自定义间距，恢复布局默认或自动间距。 |
| `setSizePolicy(QSizePolicy::Policy)` / `sizePolicy()` | 设置或读取锚点在空间分配中的策略。 |
| `QGraphicsAnchorLayout::addAnchor()` | 创建并返回 anchor 的主要入口。 |
| `QGraphicsAnchorLayout::anchor()` | 查询已有 anchor。 |

## 4. 关键用法

```cpp
auto *layout = new QGraphicsAnchorLayout;

auto *anchor = layout->addAnchor(leftItem, Qt::AnchorRight,
                                 rightItem, Qt::AnchorLeft);
anchor->setSpacing(12);
```

给边距关系设置弹性：

```cpp
anchor->setSizePolicy(QSizePolicy::Expanding);
```

## 5. 使用场景

适合场景内浮动面板、相对定位控件、需要边缘对齐和弹性间距的图形 UI、复杂节点内部布局。

如果只是垂直堆叠或行列表单，linear/grid layout 更清楚。Anchor layout 的优势在“关系”，不是“列表”。

## 6. 常见坑与经验

锚点关系太多会让布局难懂。写 anchor 布局时最好把每条边缘约束当作设计规则，而不是随手加连接。

spacing 是锚点上的属性，不是 item 的属性。不同边可以有不同间距。

不要保存过期 anchor。移除布局项或重建布局后，旧 anchor 的意义可能已经不存在。
