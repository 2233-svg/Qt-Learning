<!-- 依据 Qt 6.11.1 头文件 qgraphicslinearlayout.h 整理。 -->

# QGraphicsLinearLayout 深入笔记

> 头文件：`#include <QGraphicsLinearLayout>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsLayoutItem -> QGraphicsLayout -> QGraphicsLinearLayout`

## 1. 它解决什么问题

`QGraphicsLinearLayout` 是 Graphics View 中的“一行或一列”布局。它的任务和 `QHBoxLayout`、`QVBoxLayout` 类似：根据每个 `QGraphicsLayoutItem` 的尺寸提示、尺寸策略、伸缩因子、对齐方式与间距，把一组 item 沿一个主轴分配到可用矩形中。

但它服务的是 `QGraphicsWidget` / `QGraphicsLayoutItem`，不是普通 `QWidget`：

```text
QGraphicsWidget
  └─ QGraphicsLinearLayout
       ├─ QGraphicsWidget
       ├─ QGraphicsProxyWidget
       └─ 子 QGraphicsLayout
```

适合：

- 场景中的工具面板、节点内部区域、属性卡片。
- 一排按钮、一列标签和编辑器、图标与文本的简单组织。
- 可伸缩空白把末尾 item 推向另一端。

不适合：

- 行列交叉很多的表格式界面：`QGraphicsGridLayout` 更合适。
- 边与边需要精确约束：使用 `QGraphicsAnchorLayout`。
- 普通桌面 QWidget 窗口：优先 `QHBoxLayout` 或 `QVBoxLayout`。

## 2. 最小使用路径

```cpp
#include <QGraphicsLinearLayout>
#include <QGraphicsWidget>

auto *panel = new QGraphicsWidget;
auto *layout = new QGraphicsLinearLayout(Qt::Vertical, panel);

auto *title = new QGraphicsWidget;
auto *editor = new QGraphicsWidget;
auto *actions = new QGraphicsWidget;

layout->setContentsMargins(12, 10, 12, 10);
layout->setSpacing(8);
layout->addItem(title);
layout->addItem(editor);
layout->addStretch(1);
layout->addItem(actions);
```

构造时把 `panel` 传给布局，会让布局成为该 `QGraphicsWidget` 的顶层布局。一个 `QGraphicsWidget` 只能有一个顶层布局；不要把同一个布局安装到多个面板。

`addItem()` 不是单纯把指针加入列表。布局会把 item 接入布局树并在激活时为它分配 geometry。item 不能同时被两个布局管理。

## 3. 主轴：`orientation`

默认方向为 `Qt::Horizontal`：

```cpp
auto *row = new QGraphicsLinearLayout; // 默认横向
row->setOrientation(Qt::Vertical);     // 改为纵向
```

- `Qt::Horizontal`：主轴是宽度，item 从左到右排列。
- `Qt::Vertical`：主轴是高度，item 从上到下排列。

方向改变后，伸缩因子、item 间距和对齐的可见结果都会随主轴改变。运行时动态切换方向是合法的，但它会使布局失效并重新分配 geometry；频繁在动画每一帧切方向没有实际意义。

## 4. `stretch`：谁吸收剩余空间

`addStretch()` 或 `insertStretch()` 插入的是不可见的可伸缩空白：

```cpp
auto *row = new QGraphicsLinearLayout;
row->addItem(left);
row->addStretch(1);
row->addItem(right);
```

这会把 `right` 推向行末。伸缩因子只分配满足最小尺寸、边距、间距之后的剩余空间。

对普通 item，使用：

```cpp
layout->setStretchFactor(editor, 2);
layout->setStretchFactor(sidebar, 1);
```

`editor` 会比 `sidebar` 获得更多主轴剩余空间。`stretch == 0` 不等于“item 永不变大”，而是没有显式权重，Qt 仍会结合 `QSizePolicy` 和尺寸提示分配空间。若要限制 item，应该设置它自己的最小、首选、最大尺寸或尺寸策略。

`stretchFactor(item)` 只查询当前布局的直接 item；传入不属于本布局的指针时不能借它递归查找子布局内的对象。

## 5. `spacing` 和 `itemSpacing` 的分工

```cpp
layout->setSpacing(8);          // 默认间距
layout->setItemSpacing(1, 16);  // 第 1 个 item 后的局部间距
```

`spacing` 是所有相邻 item 之间的默认距离。`itemSpacing(index)` / `setItemSpacing(index, spacing)` 针对某个索引后的空隙设置局部值。

例如表单标题与第一项较近、分组与分组之间较远：

```cpp
layout->setSpacing(6);
layout->setItemSpacing(0, 2);   // 标题后
layout->setItemSpacing(3, 16);  // 第一组最后一项后
```

局部间距由索引决定。动态插入或删除 item 后，索引会改变，因此不要把业务语义长期绑定到裸数字；变更结构后应重新设置需要的局部间距。

边距由继承的 `setContentsMargins()` 管理，位于布局外沿；`spacing` / `itemSpacing` 管理 item 之间，二者不要混淆。

## 6. 对齐只在单元格有余量时明显

```cpp
layout->setAlignment(button, Qt::AlignRight | Qt::AlignVCenter);
```

`setAlignment()` 设置某个 item 在它分配到的单元格内如何摆放。若 item 已被尺寸策略拉伸到填满单元格，对齐看不出效果；若 item 是固定宽度或最大尺寸有限，对齐才会让它靠左、靠右、居中或贴上/下。

`alignment(item)` 读取当前对齐方式。传入非直接子项时不应把返回值当成有效布局信息。

## 7. 插入、移除与所有权

```cpp
layout->insertItem(0, warning);
layout->insertStretch(2, 1);
```

`index < 0` 会追加到末尾。要替换位置或动态插入区域，优先用这两个 API，而不是先手工改 item 的 geometry。

移除有两种入口：

```cpp
layout->removeItem(editor);
layout->removeAt(1);
```

两者都会将 item 从布局中摘下，并把 item 的所有权交回调用者。此后 item 不再由该布局摆放；若不再使用，调用者负责删除，若要迁移则可加入另一个布局。

Graphics View 的 item 同时可能受 `QGraphicsItem` 父子树管理，不能只凭“布局移除了它”就推断对象已经销毁。动态 UI 里应明确选择一种所有权路径，避免布局树和图元父子树重复释放同一对象。

## 8. 需要框架调用的接口

- `setGeometry(const QRectF &rect)`：布局被分配可用区域时计算并写入每个 child 的 geometry。
- `sizeHint(...)`：根据所有 child 的尺寸提示与间距，报告本布局的最小、首选或最大尺寸。
- `invalidate()`：作废内部的尺寸和位置缓存。
- `count()` / `itemAt()`：用于遍历当前管理的 item。

业务代码不应频繁直接调 `setGeometry()`。要改变布局结果，改方向、边距、spacing、stretch、对齐或 child 的尺寸提示，再让 `QGraphicsLayout` 在适当时机激活。

`dump(int indent = 0)` 会把布局结构输出到调试日志，适合排查 item 顺序、嵌套层级和尺寸分配问题。它是诊断工具，不应作为正式业务逻辑的输出接口。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsLinearLayout(QGraphicsLayoutItem *parent = nullptr)` | 创建默认横向布局。 | 默认 `Qt::Horizontal`；传入根 `QGraphicsWidget` 时成为其布局。 |
| 构造 | `QGraphicsLinearLayout(Qt::Orientation orientation, QGraphicsLayoutItem *parent = nullptr)` | 创建指定方向的线性布局。 | 横向分配宽度，纵向分配高度。 |
| 析构 | `virtual ~QGraphicsLinearLayout()` | 销毁布局。 | 安装到 widget 后通常由 widget 管理。 |
| 添加 | `void addItem(QGraphicsLayoutItem *item)` | 在末尾加入一个布局 item。 | item 只能属于一个布局；会被接入布局树。 |
| 添加 | `void addStretch(int stretch = 1)` | 在末尾加入可伸缩空白。 | 常用于把后续 item 推到主轴末端。 |
| 插入 | `void insertItem(int index, QGraphicsLayoutItem *item)` | 在指定位置插入 item。 | `index < 0` 追加到末尾；注意 item 不能已属于其它布局。 |
| 插入 | `void insertStretch(int index, int stretch = 1)` | 在指定位置插入可伸缩空白。 | 用于动态布局；因子只影响主轴剩余空间。 |
| 移除 | `void removeItem(QGraphicsLayoutItem *item)` | 从布局中移除指定 item。 | 所有权交回调用者；不等于图元已销毁。 |
| 移除 | `void removeAt(int index)` | 按索引移除 item。 | 所有权交回调用者；先用 `itemAt()` 核实索引。 |
| 查询 | `int count() const` | 返回直接管理的 item 数量。 | 不递归统计子布局内部 item。 |
| 查询 | `QGraphicsLayoutItem *itemAt(int index) const` | 返回指定位置的直接 item。 | 越界返回空指针；不转移所有权。 |
| 方向 | `void setOrientation(Qt::Orientation orientation)` | 设置横向或纵向主轴。 | 会触发布局重算；不要拿它做逐帧动画。 |
| 方向 | `Qt::Orientation orientation() const` | 读取当前布局方向。 | 用于根据主轴调整业务参数。 |
| 默认间距 | `void setSpacing(qreal spacing)` | 设置所有相邻 item 的默认间距。 | 与外侧 contents margins 不同。 |
| 默认间距 | `qreal spacing() const` | 读取默认间距。 | 局部 `itemSpacing` 可覆盖部分空隙。 |
| 局部间距 | `void setItemSpacing(int index, qreal spacing)` | 设置索引 item 后的间距。 | 插入/删除 item 后索引含义会变化。 |
| 局部间距 | `qreal itemSpacing(int index) const` | 读取索引 item 后的间距。 | 用于诊断局部覆盖是否生效。 |
| 伸缩 | `void setStretchFactor(QGraphicsLayoutItem *item, int stretch)` | 设置 item 的主轴剩余空间权重。 | `0` 并非禁止伸缩；还受 `QSizePolicy` 约束。 |
| 伸缩 | `int stretchFactor(QGraphicsLayoutItem *item) const` | 读取 item 的伸缩权重。 | 仅对本布局直接 item 有意义。 |
| 对齐 | `void setAlignment(QGraphicsLayoutItem *item, Qt::Alignment alignment)` | 设置 item 在其单元格内的对齐。 | item 填满单元格时视觉上不明显。 |
| 对齐 | `Qt::Alignment alignment(QGraphicsLayoutItem *item) const` | 读取 item 的对齐标志。 | 传入非子项时不要依赖结果。 |
| 布局生命周期 | `void setGeometry(const QRectF &rect)` | 分配可用区域并布局所有 child。 | 框架调用；不要用它替代约束/尺寸策略。 |
| 布局生命周期 | `void invalidate()` | 作废布局缓存。 | 常规 setter 已会触发；自定义外部状态变化时才需关注。 |
| 尺寸协商 | `QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const` | 返回布局尺寸建议。 | 由上层布局调用，考虑 child 尺寸和间距。 |
| 调试 | `void dump(int indent = 0) const` | 将布局树信息输出到调试日志。 | 用于排查，勿作为业务输出或高频调用。 |

## 10. 排查清单

1. item 排成了错误方向：检查 `orientation()`，默认值是横向。
2. stretch 没有效果：确认父容器确有剩余主轴空间，并检查 item 的最大尺寸和 `QSizePolicy`。
3. 某处间隔异常：先查 `itemSpacing(index)`，再查全局 `spacing()` 和 contents margins。
4. 删除后仍有空白或崩溃：确认 item 已从布局摘下，并由调用者按图元父子关系处理所有权。
5. 对齐设置看不出来：item 很可能已填满自己的单元格，检查最大尺寸或尺寸策略。

### 一句话总结

`QGraphicsLinearLayout` 用一个主轴管理 Graphics View 中的一行或一列：方向确定轴，stretch 分配剩余空间，spacing 管 item 之间距离，对齐处理单元格余量，移除时则必须明确 item 的后续所有权。
