# Qt QSplitter 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QSplitter>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QFrame -> QSplitter`  
> 常见搭档：`QSplitterHandle`、`QTreeView`、`QListView`、`QTextEdit`

## 1. QSplitter 解决什么问题

`QSplitter` 用一条或多条可拖动的分隔条，把多个控件排成可调整大小的区域。用户拖动分隔条时，左右或上下控件会重新分配空间。

典型界面：

- 左侧文件树，右侧编辑器；
- 上方预览区，下方日志区；
- 三栏管理后台；
- IDE 中的项目树、编辑器、输出窗口。

它和 `QHBoxLayout` / `QVBoxLayout` 的根本区别是：

| 类型 | 解决的问题 |
| --- | --- |
| `QHBoxLayout` / `QVBoxLayout` | 按布局规则自动分配空间，用户不能直接拖动边界。 |
| `QSplitter` | 让用户在运行时拖动边界，主动决定各区域大小。 |

`QSplitter` 是一个 `QWidget` 容器，不是 `QLayout`。因此它直接管理子控件，不能把 `QLayout` 当成子项添加进去；如果一个区域内部还需要多个控件，应先用一个普通 `QWidget` 包住布局，再把这个 widget 放进 splitter。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QListView>
#include <QSplitter>
#include <QTextEdit>
#include <QTreeView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    auto *splitter = new QSplitter(Qt::Horizontal);
    splitter->addWidget(new QTreeView(splitter));
    splitter->addWidget(new QListView(splitter));
    splitter->addWidget(new QTextEdit(splitter));

    splitter->setSizes({180, 220, 600});
    splitter->resize(1000, 600);
    splitter->show();
    return app.exec();
}
```

默认方向是 `Qt::Horizontal`，子控件会从左到右排列。改成 `Qt::Vertical` 后，子控件会从上到下排列。

## 3. 添加控件和所有权

### 3.1 addWidget

```cpp
splitter->addWidget(leftPanel);
splitter->addWidget(mainPanel);
```

`addWidget()` 把控件追加到末尾，并把控件交给 splitter 管理。控件如果原本已经在这个 splitter 中，再调用 `addWidget()` 会把它移动到新的位置。

### 3.2 insertWidget

```cpp
splitter->insertWidget(0, navigationPanel);
```

`insertWidget(index, widget)` 把控件插入指定索引。索引无效时会追加到末尾。

### 3.3 replaceWidget

```cpp
QWidget *oldPanel = splitter->replaceWidget(1, newPanel);
if (oldPanel)
    oldPanel->deleteLater();
```

`replaceWidget()` 会用新控件替换指定位置的旧控件，并尽量继承旧控件的几何尺寸、可见状态和折叠状态。返回值是被替换下来的旧控件；它的 parent 会被清空，所以如果不再使用，应由调用方负责销毁。

如果索引无效，或者新控件已经是 splitter 的子控件，替换不会发生并返回 `nullptr`。

## 4. QSplitter 不能直接装布局

下面这样是不对的：

```cpp
auto *layout = new QVBoxLayout;
splitter->addWidget(layout); // 类型不对，QLayout 不是 QWidget
```

正确方式是用一个中间 widget：

```cpp
auto *panel = new QWidget;
auto *layout = new QVBoxLayout(panel);
layout->addWidget(new QLabel(tr("标题")));
layout->addWidget(new QTextEdit);

splitter->addWidget(panel);
```

这个中间 widget 是 splitter 的一个区域；区域内部的排版交给布局完成。复杂界面通常是“外层 splitter + 每个区域内部 layout”的组合。

## 5. 尺寸分配：sizes、setSizes 和 stretch

### 5.1 读取和设置当前尺寸

```cpp
QList<int> current = splitter->sizes();
splitter->setSizes({200, 1, 799});
```

`sizes()` 返回每个子控件沿 splitter 主方向的当前尺寸。水平 splitter 返回宽度，垂直 splitter 返回高度。

`setSizes()` 按子控件顺序设置尺寸。列表通常应和子控件数量对应；多出来的值会被忽略，缺少的项会按 Qt 的布局规则处理。实际尺寸还会受到控件最小尺寸、最大尺寸以及是否允许折叠的影响。

如果某个值为 0：

- 该控件可能被压到不可见；
- 如果允许折叠，用户也可以把它拖到 0；
- 重新 `show()` 或重新设置合理尺寸后可以恢复。

### 5.2 初始尺寸和 setStretchFactor

```cpp
splitter->setStretchFactor(0, 1);
splitter->setStretchFactor(1, 3);
```

`setStretchFactor(index, stretch)` 会影响 splitter 后续重新分配空间时的比例。它不是布局中精确的“永久百分比”，而是根据控件当前尺寸和 stretch 因子共同计算。

如果你需要明确的初始比例，常见做法是：

```cpp
splitter->setStretchFactor(0, 1);
splitter->setStretchFactor(1, 2);
splitter->setSizes({300, 600});
```

先设置 stretch 规则，再设置一组初始尺寸，通常更容易得到预期效果。

## 6. 折叠行为：childrenCollapsible 和 setCollapsible

默认情况下，子控件可以被用户拖到尺寸 0，即使它自己设置了非零的最小尺寸：

```cpp
splitter->setChildrenCollapsible(false);
```

这会全局禁止子控件被拖到 0。也可以针对某个索引单独控制：

```cpp
splitter->setCollapsible(0, false);
splitter->setCollapsible(1, true);
```

这适合导航栏或主编辑区这类“绝不能完全消失”的区域。

要注意两个概念：

- `setCollapsible()` 控制用户能不能把区域折叠为 0；
- `setMinimumSize()` 控制普通尺寸协商的最小值。

即使 `minimumSize()` 不为 0，只要允许折叠，用户仍可能把区域压到 0。

## 7. opaqueResize：拖动时是否实时重排

默认情况下，拖动分隔条时子控件会实时改变大小：

```cpp
splitter->setOpaqueResize(true);
```

如果子控件重绘很重，比如复杂图形视图、视频预览或大型表格，可以关闭：

```cpp
splitter->setOpaqueResize(false);
```

关闭后，拖动时通常只显示一个橡皮筋位置，松开鼠标后才真正调整子控件大小。默认值由当前 Qt Style 的 `SH_Splitter_OpaqueResize` 决定，因此跨平台时不要假设一定是 `true`。

## 8. 保存和恢复用户布局

`QSplitter` 很适合配合 `QSettings` 保存用户拖出来的区域比例：

```cpp
settings.setValue("editorSplitter", splitter->saveState());
```

下次创建完相同结构的 splitter 后恢复：

```cpp
splitter->restoreState(
    settings.value("editorSplitter").toByteArray());
```

`saveState()` 保存的是 splitter 的布局状态，不只是当前一组整数尺寸；`restoreState()` 返回 `true` 表示成功恢复，返回 `false` 通常表示数据为空、损坏、版本不兼容或当前子控件结构不匹配。

如果只是临时复制当前尺寸，`sizes()` / `setSizes()` 更直接；如果要跨会话保存用户布局，优先使用 `saveState()` / `restoreState()`。

## 9. 分隔条和 QSplitterHandle

每两个相邻区域之间有一个 `QSplitterHandle`。索引规则容易混淆：

- `widget(index)` 的索引对应子控件；
- `handle(index)` 返回位于第 `index` 个区域左侧或上方的 handle；
- `handle(0)` 总是隐藏，因为第一个区域前面没有真正的分隔条；
- 水平布局在从右到左语言环境中，视觉方向会反转。

```cpp
QSplitterHandle *handle = splitter->handle(1);
if (handle)
    handle->setToolTip(tr("Drag to resize"));
```

如果想完全改变分隔条外观，可以继承 `QSplitter` 并重写 `createHandle()`，返回自己的 `QSplitterHandle` 子类。普通项目只需要调整 `handleWidth` 或样式表，通常不必重写 handle。

## 10. 方向、索引和查询

```cpp
splitter->setOrientation(Qt::Vertical);
Qt::Orientation current = splitter->orientation();

int count = splitter->count();
QWidget *panel = splitter->widget(0);
int index = splitter->indexOf(panel);
```

`indexOf()` 找不到控件时返回 `-1`。它也能处理 splitter handle，但日常业务代码一般只对自己的子控件查询。

`getRange(index, &min, &max)` 可查询某个分隔位置当前允许移动的最小和最大范围：

```cpp
int minimum = 0;
int maximum = 0;
splitter->getRange(1, &minimum, &maximum);
```

它适合做自定义拖动限制或调试布局约束。

## API 速查表
### 11.1 构造和属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSplitter(QWidget *parent = nullptr)` | 创建默认水平排列的 splitter。 | 等价于使用 `Qt::Horizontal`；子控件要通过 `addWidget()` 等接口加入。 |
| 构造 | `QSplitter(Qt::Orientation, QWidget *parent = nullptr)` | 按水平或垂直方向创建 splitter。 | `Horizontal` 是左右分区，`Vertical` 是上下分区。 |
| 析构 | `~QSplitter()` | 销毁 splitter 及其对象树中的子控件。 | splitter 管理的是 `QWidget`，不要把外部仍在使用的控件误删。 |
| 方向 | `orientation()` / `setOrientation(Qt::Orientation)` | 读取或设置子区域排列的主方向。 | 改方向会重新计算所有区域几何和 handle 方向。 |
| 折叠 | `childrenCollapsible()` / `setChildrenCollapsible(bool)` | 读取或设置子区域是否允许被拖到 0。 | 关闭它只影响折叠行为，不会取消普通最小尺寸约束。 |
| 实时调整 | `opaqueResize()` / `setOpaqueResize(bool)` | 读取或设置拖动 handle 时是否实时调整子控件。 | 重绘昂贵的视图、视频或大表格可以关闭。 |
| 分隔条 | `handleWidth()` / `setHandleWidth(int)` | 读取或设置 handle 的宽度。 | 太小会难以抓取；值为 0 或 1 时 Qt 可能让实际抓取区域覆盖相邻控件几像素。 |

### 11.2 子控件管理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 添加 | `addWidget(QWidget *)` | 把控件追加成 splitter 的最后一个区域。 | splitter 会接管控件的父子关系；已在其他位置的控件会被重新安置。 |
| 插入 | `insertWidget(int, QWidget *)` | 把控件插入指定区域索引。 | 索引无效时通常追加到末尾；插入会改变后续控件索引。 |
| 替换 | `replaceWidget(int, QWidget *)` | 用新控件替换指定索引处的旧控件。 | 返回旧控件；旧控件会脱离 splitter，通常需要由调用方决定复用或 `deleteLater()`。 |
| 数量 | `count()` | 返回当前 splitter 管理的子控件数量。 | 它统计 widget，不要把 handle 数量当成区域数量。 |
| 查询 | `widget(int)` | 按索引返回一个子控件。 | 索引无效返回 `nullptr`；动态增删后不要缓存旧索引。 |
| 查询 | `indexOf(QWidget *)` | 返回控件在 splitter 中的区域索引。 | 找不到返回 `-1`；只对 splitter 管理的控件有意义。 |
| 折叠 | `setCollapsible(int, bool)` | 单独设置某个区域是否允许被拖到 0。 | 局部设置用于覆盖全局策略；索引变化后要重新确认目标区域。 |
| 折叠 | `isCollapsible(int)` | 查询某个区域的折叠许可。 | 索引无效时不要依赖返回值，应先检查 `count()`。 |

### 11.3 尺寸、范围和状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸 | `sizes()` | 返回每个区域沿 splitter 主方向的当前尺寸。 | 水平 splitter 返回宽度，垂直 splitter 返回高度；列表顺序对应 `widget(index)`。 |
| 尺寸 | `setSizes(const QList<int> &)` | 设置所有区域的目标尺寸。 | 实际结果仍受最小尺寸、最大尺寸和折叠策略限制；适合设置初始比例。 |
| 伸缩 | `setStretchFactor(int, int)` | 设置某个区域后续参与空间分配的伸缩倾向。 | 它不是永久百分比；窗口大小变化时还会受当前尺寸和 size policy 影响。 |
| 范围 | `getRange(int, int *, int *)` | 查询指定 handle 当前允许移动的最小和最大位置。 | 输出参数可传 `nullptr`；索引语义是 handle/分隔条位置。 |
| 保存 | `saveState()` | 把 splitter 的方向、区域尺寸和折叠状态编码成 `QByteArray`。 | 适合交给 `QSettings`，恢复时应保持相同的子控件结构。 |
| 恢复 | `restoreState(const QByteArray &)` | 恢复之前保存的 splitter 状态。 | 返回是否成功；版本或子控件结构变化后旧状态可能失效。 |
| 尺寸提示 | `sizeHint()` | 返回 splitter 的推荐尺寸。 | 通常由父布局调用，不建议在业务代码里反复手动覆盖。 |
| 尺寸提示 | `minimumSizeHint()` | 返回结合子控件和 handle 的最小推荐尺寸。 | 不能保证用户永远不能拖得更小，折叠策略仍会影响结果。 |
| 刷新 | `refresh()` | 让 splitter 重新整理内部区域状态。 | 主要供 Qt 内部使用；普通布局问题应先检查子控件、sizes 和约束。 |

### 11.4 分隔条和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查询 | `handle(int)` | 返回指定索引对应的 `QSplitterHandle`。 | `handle(0)` 通常隐藏，因为第一个区域前没有可见分隔条；索引不要和 widget 索引混淆。 |
| 信号 | `splitterMoved(int pos, int index)` | 分隔条移动后通知新位置和 handle 索引。 | `pos` 是主方向位置，`index` 是被移动的分隔条，不是右侧 widget 的索引。 |
| 工厂 | `createHandle()` | 创建 splitter 使用的 handle 对象。 | 派生 `QSplitter` 重写它即可替换 handle 外观和交互；返回对象应以当前 splitter 为 parent。 |

### 11.5 QSplitterHandle 的直接 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSplitterHandle(Qt::Orientation, QSplitter *)` | 创建一个属于指定 splitter 的分隔条控件。 | 通常由 `QSplitter::createHandle()` 创建，不建议业务代码单独拥有。 |
| 析构 | `~QSplitterHandle()` | 销毁分隔条。 | splitter 销毁时会按对象树处理。 |
| 方向 | `orientation()` / `setOrientation(...)` | 读取或设置 handle 的水平/垂直方向。 | 要和所属 splitter 方向一致，否则绘制和拖动反馈会错位。 |
| 状态 | `opaqueResize()` | 查询所属 splitter 是否实时调整子控件。 | handle 的拖动显示应与这个状态保持一致。 |
| 所属关系 | `splitter()` | 返回当前 handle 所属的 splitter。 | 未正确挂到 splitter 时不要依赖非空结果。 |
| 尺寸 | `sizeHint()` | 返回 handle 的推荐尺寸。 | 最终还会受到 splitter 的 `handleWidth` 和 style 影响。 |
| 拖动 | `moveSplitter(int)` / `closestLegalPosition(int)` | 移动 handle 或把目标位置限制到合法范围。 | 适合自定义 handle 交互；合法范围由 splitter 的尺寸约束决定。 |

### 11.6 受保护函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 子类移动 | `moveSplitter(int pos, int index)` | 将指定分隔条移动到尽量接近目标位置的位置。 | 受最小尺寸、最大尺寸和折叠策略限制；一般由 handle 调用。 |
| 合法范围 | `closestLegalPosition(int pos, int index)` | 把目标位置限制到当前允许的范围内。 | 用于自定义拖动时避免突破区域约束。 |
| 橡皮筋 | `setRubberBand(int pos)` | 显示、移动或隐藏非实时调整时的橡皮筋位置。 | 只影响拖动反馈；真正尺寸在合适时机由 splitter 更新。 |
| 事件 | `changeEvent(QEvent *)` | 响应 style、字体等变化。 | 重写后通常调用基类，确保 handle 和尺寸策略同步。 |
| 子对象 | `childEvent(QChildEvent *)` | 响应子控件加入、移除或变化。 | 只在派生类需要维护额外索引时重写。 |
| 尺寸 | `resizeEvent(QResizeEvent *)` | splitter 尺寸变化时重新分配区域。 | 自定义布局前先确认 `setSizes()` 和 stretch 是否已经满足需求。 |
| 事件 | `event(QEvent *)` | splitter 的总事件入口。 | 只在需要处理特殊事件时重写；普通拖动行为由 Qt 已实现。 |

## 12. 常见误区

### 12.1 把 QSplitter 当布局使用

它只能直接管理 `QWidget`，不能直接管理 `QLayout`。需要布局时，用一个 `QWidget` 作为区域容器。

### 12.2 只设置了 stretch，初始比例却不对

stretch 主要影响后续空间分配。启动时想要明确比例，配合 `setSizes()` 设置一组初始尺寸。

### 12.3 用 resize(0, 0) 隐藏区域

如果目的是让用户可折叠，使用 `setCollapsible()` 和 `childrenCollapsible()`；如果是程序临时隐藏，直接 `widget->hide()` 更清晰。

### 12.4 replaceWidget 后忘记处理旧控件

`replaceWidget()` 返回旧控件并把它脱离 splitter。旧控件不再使用时要自己 `deleteLater()`，否则可能泄漏或继续占用资源。

### 12.5 把 handle 索引和 widget 索引混为一谈

`handle(1)` 是第一个真正可见分隔条附近的 handle，而 `widget(1)` 是第二个子控件。处理拖动信号时要根据 `index` 的语义核对清楚。

---

### 一句话总结

`QSplitter` 是可由用户拖动分配空间的 QWidget 容器：用 `addWidget/insertWidget` 管理区域，用 `setSizes/setStretchFactor` 控制尺寸，用 `setCollapsible` 控制折叠，用 `saveState/restoreState` 保存用户布局。
