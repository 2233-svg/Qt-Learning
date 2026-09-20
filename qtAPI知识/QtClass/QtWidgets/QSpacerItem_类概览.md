# Qt QSpacerItem 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QSpacerItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QLayoutItem`  
> 定位：布局中的不可见空白项

## 1. QSpacerItem 解决什么问题

界面中的空白并不总是“没有东西”。很多时候，空白本身就是布局规则的一部分：

- 两组控件之间需要固定 12 像素距离；
- 按钮行需要把“确定”和“取消”推到右侧；
- 左右两侧控件之间需要一块能随窗口变宽而增长的区域；
- 网格布局中某一列需要占据可伸缩的余量。

`QSpacerItem` 就是这种不可见空间的布局项。它没有可绘制内容，也不是 `QWidget`，但它和控件一样会报告推荐尺寸、最小尺寸、最大尺寸、扩展方向和 geometry。

```text
QHBoxLayout
├─ QLabel("文件名：")
├─ QLineEdit
├─ QSpacerItem       <- 不可见，但可吸收空间
└─ QPushButton("浏览...")
```

它解决的是“如何把空白纳入布局协商”，而不是“如何画一个透明控件”。

## 2. 优先使用布局的便捷 API

大多数情况不需要直接创建 `QSpacerItem`。Qt 的布局类已经提供了更清晰的高层表达。

### 2.1 固定空白：`addSpacing()`

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QPushButton("上一步"));
row->addSpacing(12);
row->addWidget(new QPushButton("下一步"));
```

`addSpacing(12)` 表达“这里始终保留 12 像素空白”。窗口变大时，这块空白不会主动吸收额外空间。

### 2.2 可伸缩空白：`addStretch()`

```cpp
auto *buttons = new QHBoxLayout;
buttons->addStretch();
buttons->addWidget(new QPushButton("取消"));
buttons->addWidget(new QPushButton("确定"));
```

这会在按钮前加入一个可伸缩空白，把按钮推到右侧。多个 stretch 同时存在时，额外空间按 stretch 因子比例分配。

### 2.3 网格布局优先控制行列

在 `QGridLayout` 中，通常不需要手工塞 spacer，而是直接表达行列约束：

```cpp
grid->setColumnStretch(1, 1);
grid->setColumnMinimumWidth(0, 120);
```

这比在每一行重复插入 `QSpacerItem` 更符合网格布局的语义，也更容易维护。

## 3. 什么时候需要直接使用 QSpacerItem

以下场景才值得直接创建它。

### 3.1 需要同时精确控制宽高和两方向策略

```cpp
auto *gap = new QSpacerItem(
    24, 0,
    QSizePolicy::Fixed,
    QSizePolicy::Minimum);

layout->addItem(gap);
```

这表示：

- 水平方向推荐宽度为 24，且固定；
- 垂直方向推荐高度为 0，但允许布局按最小要求协商。

`addSpacing()` 只能表达沿当前布局主轴的固定间隔；`QSpacerItem` 可以独立指定水平、垂直的推荐尺寸和策略。

### 3.2 运行时改变空白规则

例如侧边栏收起时，需要缩小中间的空白：

```cpp
gap->changeSize(
    sideBarVisible ? 24 : 0,
    0,
    QSizePolicy::Fixed,
    QSizePolicy::Minimum);

layout->invalidate();
```

`changeSize()` 只修改 spacer 自己保存的尺寸信息。若它已经在布局中，必须让布局失效，新的尺寸才会参加下一次布局计算。

### 3.3 编写自定义布局

自定义 `QLayout` 的 `addItem()` 接口接收 `QLayoutItem *`。如果你的算法要支持空白项，`QSpacerItem` 是现成实现，不需要自己写一个透明 QWidget。

## 4. 它如何参与尺寸协商

`QSpacerItem` 的构造参数为：

```cpp
QSpacerItem(
    int w,
    int h,
    QSizePolicy::Policy hPolicy = QSizePolicy::Minimum,
    QSizePolicy::Policy vPolicy = QSizePolicy::Minimum);
```

| 参数 | 含义 | 影响 |
| --- | --- | --- |
| `w` | 推荐宽度 | 布局空间足够时的水平参考值 |
| `h` | 推荐高度 | 布局空间足够时的垂直参考值 |
| `hPolicy` | 水平方向尺寸策略 | 能否或多大程度上吸收/让出额外宽度 |
| `vPolicy` | 垂直方向尺寸策略 | 能否或多大程度上吸收/让出额外高度 |

默认策略是两个方向的 `QSizePolicy::Minimum`。Qt 文档说明，这组默认值会产生一个“在没有其它项目想要空间时可以伸展”的间隔。

常用策略组合：

| 目标 | `w, h` | 水平策略 | 垂直策略 |
| --- | --- | --- | --- |
| 固定水平间隔 | `16, 0` | `Fixed` | `Minimum` |
| 把右侧按钮推开 | `0, 0` | `Expanding` | `Minimum` |
| 固定垂直间隔 | `0, 12` | `Minimum` | `Fixed` |
| 填充两方向剩余空间 | `0, 0` | `Expanding` | `Expanding` |

更高层的 `addStretch()` 通常比手写 `Expanding` spacer 更直观；直接创建 spacer 的价值在于你可以同时控制两个方向。

## 5. QSpacerItem 与 QWidget 的关键差异

| 特性 | `QSpacerItem` | `QWidget` |
| --- | --- | --- |
| 是否可见 | 否 | 通常可见 |
| 是否接收鼠标、键盘事件 | 否 | 可以 |
| 是否是 QObject | 否 | 是 |
| 是否有父对象树 | 否 | 有 |
| 是否参与布局尺寸协商 | 是 | 是 |
| 如何在 `QLayoutItem` 中识别 | `spacerItem()` | `widget()` |

`QSpacerItem::isEmpty()` 始终返回 `true`，这不代表它“没有作用”。这里的 empty 表示它不包含可见 widget；它仍然会通过自身的 size policy 和尺寸参与空间分配。

不要为了制造空白而创建透明 `QWidget`。透明控件会进入对象树、可能接收事件、需要额外管理样式和可见性，而 spacer 只表达布局空白，语义更准确。

## 6. 所有权与生命周期

`QSpacerItem` 不是 `QObject`，没有 parent 参数，也不会自动进入对象树。

把 spacer 交给布局后，布局接管该布局项的管理责任：

```cpp
auto *gap = new QSpacerItem(
    0, 0, QSizePolicy::Expanding, QSizePolicy::Minimum);
layout->addItem(gap);
```

因此不要把栈对象交给会长期保存它的布局：

```cpp
QSpacerItem gap(16, 0);
layout->addItem(&gap); // 错误：函数结束后 gap 已失效
```

动态移除时，使用 `takeAt()` 获取项并自行删除：

```cpp
if (QLayoutItem *item = layout->takeAt(index)) {
    if (QSpacerItem *spacer = item->spacerItem()) {
        Q_UNUSED(spacer);
    }
    delete item;
}
```

对 spacer 来说，`item` 就是 spacer 本身；不需要再删除第二个对象。对 widget item 或子布局项则不同，必须分别按关联对象的生命周期处理。

## 7. `changeSize()` 为什么一定要配合 `invalidate()`

下面的写法只改了 spacer 的内部数据：

```cpp
gap->changeSize(32, 0, QSizePolicy::Fixed, QSizePolicy::Minimum);
```

布局可能已经缓存过本次窗口尺寸下的 size hint、行列尺寸或项目 geometry。若不通知布局，屏幕上仍可能维持旧结果。

正确做法：

```cpp
gap->changeSize(32, 0, QSizePolicy::Fixed, QSizePolicy::Minimum);
layout->invalidate();
```

必要时还可以请求父控件更新：

```cpp
layout->parentWidget()->updateGeometry();
```

但通常 `invalidate()` 已足够让下一次布局更新重新计算。不要靠手动 `move()` 或 `resize()` 修补，因为 spacer 没有可见 widget 可以直接调整。

## 8. geometry、sizeHint 与 `sizePolicy()`

`QSpacerItem` 重写了 `QLayoutItem` 的尺寸函数：

- `sizeHint()`：返回推荐占用尺寸；
- `minimumSize()`：返回允许的最小尺寸；
- `maximumSize()`：返回允许的最大尺寸；
- `expandingDirections()`：返回可以扩展的方向；
- `geometry()`：返回布局最终分给它的矩形；
- `setGeometry()`：由布局调用，记录新的分配矩形。

`sizePolicy()` 则返回 spacer 当前的完整 `QSizePolicy`：

```cpp
QSizePolicy policy = gap->sizePolicy();
```

调试“为什么这块空白没变大”时，至少同时检查：

```cpp
qDebug() << gap->sizeHint()
         << gap->minimumSize()
         << gap->maximumSize()
         << gap->expandingDirections()
         << gap->sizePolicy();
```

还要确认父布局是否真的有多余空间。任何项目都无法吸收不存在的剩余空间。

## 9. 常见误区

### 9.1 用 spacer 给控件留 margin

窗口边缘留白应该优先用：

```cpp
layout->setContentsMargins(12, 8, 12, 8);
```

spacer 表示布局内部的一个项目。用它模拟四边 margin 会让布局结构难读且不利于嵌套。

### 9.2 用 `addSpacing()` 实现“按钮靠右”

固定空白在不同窗口宽度下不可靠：

```cpp
buttons->addSpacing(300); // 宽窗口不够，窄窗口又挤坏
```

应使用 `addStretch()` 或水平扩展 spacer。

### 9.3 修改 `changeSize()` 后没有刷新布局

这是 QSpacerItem 最典型的坑。它在加入布局后变更尺寸，必须调用所属布局的 `invalidate()`。

### 9.4 手动删除仍被布局管理的 spacer

布局仍持有项目指针时手动 `delete gap` 会留下悬空指针。先 `takeAt()` 或等待布局销毁。

### 9.5 误解 `isEmpty() == true`

对 spacer 而言，empty 指“不包含可见控件”，并不表示它不参与空间分配。

## API 速查表
下表列出 `QSpacerItem` 自己声明和重写的 API；`QLayoutItem` 继承的通用 API 请结合其笔记阅读。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QSpacerItem(int w, int h, QSizePolicy::Policy hPolicy = QSizePolicy::Minimum, QSizePolicy::Policy vPolicy = QSizePolicy::Minimum)` | 创建一个带推荐宽高和水平/垂直尺寸策略的不可见空间项。 | 直接控制双方向空白时使用；交给布局管理时通常在堆上创建。 |
| 析构函数 | `virtual ~QSpacerItem()` | 销毁 spacer。 | 已被布局管理时不要单独删除；先通过 `takeAt()` 取走。 |
| 设置 | `void changeSize(int w, int h, QSizePolicy::Policy hPolicy = QSizePolicy::Minimum, QSizePolicy::Policy vPolicy = QSizePolicy::Minimum)` | 修改推荐宽高和两方向尺寸策略。 | 加入布局后必须调用 `layout->invalidate()`，否则新尺寸可能不生效。 |
| 查询 | `QSizePolicy sizePolicy() const` | 返回当前完整尺寸策略。 | 排查 spacer 是否可扩展、可收缩时使用。 |
| 重写 | `Qt::Orientations expandingDirections() const` | 返回 spacer 可以吸收额外空间的方向。 | 由水平和垂直 `QSizePolicy` 决定；不等同于布局 stretch。 |
| 重写 | `QRect geometry() const` | 返回布局最终分给 spacer 的矩形。 | spacer 不可见，但 geometry 对调试布局结果有用。 |
| 重写 | `bool isEmpty() const` | 返回 `true`，表明 spacer 不包含可见控件。 | 不表示它不参与布局和空间分配。 |
| 重写 | `QSize maximumSize() const` | 返回 spacer 允许的最大尺寸。 | 与 size policy 一起限制它能吸收多少空间。 |
| 重写 | `QSize minimumSize() const` | 返回 spacer 允许的最小尺寸。 | 固定间隔与可压缩间隔的底线由它影响。 |
| 重写 | `void setGeometry(const QRect &r)` | 接收布局给 spacer 分配的矩形。 | 由布局系统调用；业务代码一般只读 `geometry()`。 |
| 重写 | `QSize sizeHint() const` | 返回 spacer 的推荐尺寸。 | 对应构造/`changeSize()` 传入的宽高，实际尺寸仍由布局协商。 |
| 类型识别 | `QSpacerItem *spacerItem()` | 返回 `this`，表明该布局项就是 spacer。 | 遍历 `QLayoutItem` 时用于安全识别空白项。 |

## 11. 继续学习

与 `QSpacerItem` 最相关的下一步是：

1. `QSizePolicy`：理解 `Fixed`、`Minimum`、`Expanding` 等策略如何改变尺寸协商；
2. `QWidgetItem`：理解可见控件如何作为布局项报告尺寸与隐藏状态；
3. `QBoxLayout`：理解 `addSpacing()`、`addStretch()` 和 `addSpacerItem()` 的主轴行为；
4. `QGridLayout`：理解用行列 stretch 代替重复 spacer 的方法。

### 一句话总结

`QSpacerItem` 是布局中的“有规则的空白”：它不可见、不是 QWidget，却通过 size hint、size policy 和 geometry 参与空间分配。固定间隔优先用 `addSpacing()`，可伸缩空白优先用 `addStretch()`；只有需要双方向策略或运行时改变空白规则时，才直接管理 `QSpacerItem`。
