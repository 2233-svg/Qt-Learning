# QLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QLayout`

## 1. 先建立直觉

### 这是什么

`QLayout` 是 Qt Widgets 的布局管理基类。它本身通常不直接出现在界面上，而是负责把一组 `QWidget`、子布局、弹簧和空白项安排到一个矩形区域里。

如果把 `QWidget` 看成“能显示和接收事件的对象”，`QLayout` 就是决定这些对象如何占据空间的规则系统。它综合每个控件的 `sizeHint()`、`minimumSize()`、`maximumSize()`、`QSizePolicy`、stretch、spacing、contents margins 和对齐方式，然后在窗口变化时重新分配几何。

### 适合使用的场景

- 给窗口或面板建立自适应界面，而不是用固定坐标摆控件。
- 组合多个控件、子布局、空白项，形成可伸缩的表单、工具条、编辑区。
- 编写自定义布局类，让控件按特殊规则排列，例如流式布局、瀑布流、非规则网格。
- 统一控制整个容器的边距、间距、尺寸约束和菜单栏占位。

### 不适合的场景

- 不要把 `QLayout` 当作可见控件；它没有绘制内容，也不接收普通用户输入。
- 不要在布局管理下继续手动 `setGeometry()` 子控件；下一次布局激活会覆盖你的设置。
- 不要用它解决业务状态同步；布局只关心几何，不关心数据模型正确性。

### 最小示例

```cpp
auto *panel = new QWidget;
auto *layout = new QVBoxLayout(panel);
layout->setContentsMargins(12, 12, 12, 12);
layout->setSpacing(8);
layout->addWidget(new QLabel(tr("Name")));
layout->addWidget(new QLineEdit);
panel->show();
```

布局的关键不是“把控件加进去”这么简单，而是让窗口变化、字体变化、平台 style 变化时，界面仍然能被重新计算。

## 2. 依赖与对象关系

- 头文件：`#include <QLayout>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QObject`、`QLayoutItem`
- 直接派生类：`QBoxLayout`、`QFormLayout`、`QGridLayout`、`QStackedLayout`

### 和 QWidget 的关系

一个 `QWidget` 只能安装一个顶层布局。可以在布局构造时传入父控件，也可以先创建布局再调用 `QWidget::setLayout()`。安装后，布局会接管子控件的几何管理。

布局对象不是普通子控件；它通过 `QObject` 父子关系参与生命周期，通过 `QLayoutItem` 接口参与尺寸计算。嵌套布局被加入父布局后，所有权转移给父布局。

### 和 QLayoutItem 的关系

布局内部管理的是 `QLayoutItem`。控件会被包装成 `QWidgetItem`，子布局本身也是布局项，spacer 则是 `QSpacerItem`。因此 `count()`、`itemAt()`、`takeAt()` 面向的是“布局项”，不是单纯的控件列表。

### 所有权边界

`addItem()` 接收的 `QLayoutItem` 所有权交给布局。`removeWidget()` 只把控件从布局管理中移除，不删除控件。`takeAt()` 把布局项取出来后，调用方要负责删除这个 item，并决定里面的 widget 或子布局如何处理。

这也是清空布局时最容易出错的地方：删除 layout item 不等于一定删除 widget；删除 widget 也不等于自动整理你的业务指针。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum SizeConstraint` | 约束父控件尺寸：固定、最小、最大、最小最大或不约束。 |
| `contentsMargins : QMargins` | 布局外圈边距，决定内容区离父控件边缘多远。 |
| `spacing : int` | 布局项之间的间距；未设置时通常来自父布局或平台 style。 |
| `sizeConstraint : SizeConstraint` | 对父控件整体施加尺寸约束。 |
| `horizontalSizeConstraint : SizeConstraint` | Qt 6.10 起单独控制水平方向约束。 |
| `verticalSizeConstraint : SizeConstraint` | Qt 6.10 起单独控制垂直方向约束。 |
| `QLayout(QWidget *parent)` | 创建顶层布局并可直接安装到父控件。 |
| `activate()` | 立即尝试重新布局；通常由 Qt 自动调用。 |
| `addItem(QLayoutItem *item)` | 自定义布局必须实现的添加入口，取得 item 所有权。 |
| `addWidget(QWidget *w)` | 把控件交给布局管理，内部会调用 `addItem()`。 |
| `count() const` | 返回当前布局项数量。 |
| `itemAt(int index) const` | 查看指定索引的布局项，不转移所有权。 |
| `takeAt(int index)` | 移除并返回指定布局项，所有权交给调用方。 |
| `indexOf(const QWidget *widget)` | 查找控件在当前布局中的索引。 |
| `indexOf(const QLayoutItem *item)` | 查找布局项在当前布局中的索引。 |
| `removeWidget(QWidget *widget)` | 取消布局对某控件的管理。 |
| `removeItem(QLayoutItem *item)` | 从布局中移除某布局项。 |
| `replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options)` | 在布局树中用一个控件替换另一个控件。 |
| `setAlignment(QWidget *w, Qt::Alignment)` | 设置某控件在它分配到的空间内如何对齐。 |
| `setAlignment(QLayout *l, Qt::Alignment)` | 设置子布局在它分配到的空间内如何对齐。 |
| `setContentsMargins(...)` | 设置布局外圈边距。 |
| `unsetContentsMargins()` | Qt 6.1 起恢复 style 默认边距。 |
| `contentsMargins() const` | 返回当前边距。 |
| `getContentsMargins(...) const` | 用指针形式读取四个方向边距。 |
| `contentsRect() const` | 返回扣除边距后的内容矩形。 |
| `setSpacing(int)` / `spacing() const` | 设置或读取布局项间距。 |
| `setEnabled(bool)` / `isEnabled() const` | 启用或停用布局管理。 |
| `setMenuBar(QWidget *widget)` / `menuBar() const` | 为顶层布局预留菜单栏区域。 |
| `parentWidget() const` | 返回此布局管理的父控件。 |
| `update()` | 请求重新布局。 |
| `invalidate()` | 使缓存尺寸计算失效。 |
| `setGeometry(const QRect &r)` / `geometry() const` | 设置或读取布局占据的矩形。 |
| `minimumSize() const` / `maximumSize() const` | 汇总布局内容的最小和最大尺寸。 |
| `expandingDirections() const` | 描述布局是否愿意在水平或垂直方向扩展。 |
| `controlTypes() const` | 汇总布局内部控件类型，供 style 决定间距等细节。 |
| `layout()` | 作为 `QLayoutItem` 时返回自身。 |
| `isEmpty() const` | 判断布局项是否为空。 |
| `closestAcceptableSize(widget, size)` | 计算满足控件尺寸约束且最接近目标值的尺寸。 |
| `addChildLayout(QLayout *childLayout)` | 自定义布局添加子布局时登记父子关系。 |
| `addChildWidget(QWidget *w)` | 自定义布局添加控件前登记布局管理关系。 |
| `alignmentRect(const QRect &r) const` | 根据对齐和尺寸提示计算实际占用矩形。 |
| `childEvent(QChildEvent *e)` | 处理 QObject 子对象变化。 |

## 4. API 逐项说明

### `enum QLayout::SizeConstraint`

`SizeConstraint` 决定布局是否把自己的尺寸计算结果反向施加到父控件上。它常用于对话框：内容变化后，窗口应固定、只允许变大，或同时限制最小最大尺寸。

- `SetDefaultConstraint`：默认策略；通常设置合理的最小尺寸。
- `SetFixedSize`：父控件固定为 `sizeHint()`，适合不可伸缩的短对话框。
- `SetMinimumSize`：把 `minimumSize()` 作为父控件最小尺寸。
- `SetMaximumSize`：把 `maximumSize()` 作为父控件最大尺寸。
- `SetMinAndMaxSize`：同时设置最小和最大范围。
- `SetNoConstraint`：不对父控件施加额外约束。

Qt 6.10 起可以分别设置水平和垂直约束，这让“宽度可变、高度固定”这类界面更容易表达。

### `contentsMargins`

边距是布局边界到内容区之间的距离。它控制的是整组子项离外框多远，不是子项之间的距离。默认值来自平台 style，因此同一份代码在 Windows、macOS、Linux 桌面上可能有细微差异。

设置边距时要考虑层级：父容器已经有边距，子布局再设置很大的边距，界面会显得松散。复杂界面里通常只在页面外层设置较明显边距，在内部布局使用更小间距。

### `spacing`

间距是相邻布局项之间的距离。未显式设置时，布局会尝试继承父布局或使用 style 默认值。`QGridLayout` 和 `QFormLayout` 支持水平、垂直间距分开设置；当两个方向不同，通用 `spacing()` 可能返回 `-1`。

调 UI 时不要到处给控件加固定空白控件。优先调整 `spacing`、stretch 和 size policy，界面会更稳定。

### `sizeConstraint` / `horizontalSizeConstraint` / `verticalSizeConstraint`

`sizeConstraint` 一次控制两个方向；Qt 6.10 的两个方向属性允许拆开控制。典型例子是设置对话框高度固定但宽度允许拉伸，或者让内容区增加后窗口自动增大。

如果尺寸约束看起来没生效，要检查父控件是否已有显式 `minimumSize` / `maximumSize`，以及子控件自己的尺寸策略是否给出了冲突信号。

### `QLayout(QWidget *parent = nullptr)`

构造布局。传入 `parent` 时会把布局设为该控件的顶层布局；没有 parent 时，它必须被加入另一个布局或通过 `setLayout()` 安装到控件上。

一个控件只能有一个顶层布局。重复安装布局通常会产生警告，也会让所有权变得混乱。

### `activate()` / `update()` / `invalidate()`

这三个函数都和重新布局有关，但层级不同：

- `invalidate()` 表示已有尺寸缓存不可信了。
- `update()` 请求稍后重新布局。
- `activate()` 立即尝试执行布局，并返回是否真的重新计算。

应用代码很少需要主动调用 `activate()`。大多数情况下，添加控件、改变尺寸策略、改变文本后，Qt 会在合适时机重新布局。

### `addItem(QLayoutItem *item)`

这是纯虚函数，自定义布局必须实现。它接收一个布局项并取得所有权。标准布局的 `addWidget()`、`addLayout()`、`addSpacing()` 等最终都会转成具体的布局项加入内部结构。

实现自定义布局时，`addItem()` 只负责保存 item；真正计算位置通常在 `setGeometry()` 中完成，尺寸汇总通常在 `sizeHint()`、`minimumSize()` 等函数中完成。

### `addWidget(QWidget *w)`

把控件加入布局管理。对于不同子类，插入位置和排列方式不同；例如盒布局追加到末尾，网格布局通常使用自己的重载指定行列。

当控件被布局管理后，不要再用固定坐标控制它。需要影响它的空间分配时，设置 `sizePolicy`、最小尺寸、最大尺寸、stretch 或对齐方式。

### `count()` / `itemAt(int)` / `takeAt(int)`

这是遍历布局的核心三件套。`count()` 返回项目数，`itemAt()` 查看但不移除，`takeAt()` 移除并把 item 所有权交给调用方。

清空布局时要从 `takeAt(0)` 循环取出项目，然后分别处理 `item->widget()`、`item->layout()` 和 item 本身。是否删除 widget 取决于你是不是还要复用它。

### `indexOf(...)`

`indexOf(QWidget *)` 查控件，`indexOf(QLayoutItem *)` 查布局项。默认实现通常遍历 `itemAt()`，因此大布局里不要在高频路径反复查找。

它只搜索当前布局的直接项目，不等价于在整个对象树中递归查找。

### `removeWidget(QWidget *widget)` / `removeItem(QLayoutItem *item)`

这两个函数只解除布局管理关系。控件或布局项后续怎么销毁，由调用方负责。

如果只是临时隐藏控件，通常用 `widget->hide()` 更简单；如果要彻底改变布局结构，再使用 remove/take。

### `replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options)`

在布局中把一个控件替换为另一个控件，并返回被替换控件对应的布局项。它适合运行时切换编辑器、占位控件换成真实控件、或根据权限替换交互组件。

默认可递归查找子布局。替换后要注意旧控件并不会自动删除，返回的 item 也需要妥善处理。

### `setAlignment(QWidget *w, Qt::Alignment)` / `setAlignment(QLayout *l, Qt::Alignment)`

设置某个控件或子布局在分配到的格子/区域中如何贴边或居中。它不是设置文本对齐，也不是改变布局整体方向。

对齐通常只在项目没有填满可用空间时可见；如果控件的 size policy 要求扩展，它可能把空间全部占掉，看起来就像对齐无效。

### `setContentsMargins(...)` / `contentsMargins()` / `getContentsMargins(...)` / `contentsRect()`

这些函数控制和查询外圈边距。`contentsRect()` 返回的是 `geometry()` 扣掉 margins 之后真正用来摆放项目的矩形。

新代码优先使用 `QMargins` 版本，旧代码或需要分别填充四个整数指针时再用 `getContentsMargins()`。

### `unsetContentsMargins()`

Qt 6.1 起提供，用于撤销自定义边距并恢复 style 默认值。这比手动猜一个平台默认像素值更可靠。

它适合主题切换、动态紧凑模式恢复、或组件库里让调用方回到默认视觉密度。

### `setSpacing(int)` / `spacing() const`

设置或读取布局项之间的距离。值越大界面越松，值越小越密。不要用负值表达紧凑布局；使用 style、边距和控件尺寸策略更可控。

如果子类有水平/垂直独立间距，通用 `spacing()` 返回 `-1` 时表示“两个方向不一致”。

### `setEnabled(bool)` / `isEnabled() const`

禁用布局后，布局不会继续管理子项几何。它不等于禁用里面的控件，用户仍可能和控件交互。

这个 API 很少用于普通业务界面，更多用于特殊容器或过渡状态。需要让整块界面不可操作时，应禁用父控件或具体控件。

### `setMenuBar(QWidget *widget)` / `menuBar() const`

给顶层布局预留菜单栏位置。它主要服务传统窗口结构，让菜单栏不占用普通内容区域。

在 `QMainWindow` 中通常不要手动用这个函数；主窗口已经有自己的菜单栏、工具栏、状态栏布局模型。

### `parentWidget() const`

返回被此布局管理的父控件。没有安装到控件上的布局可能返回空指针。

自定义布局和调试布局问题时，这个函数很有用：你可以确认布局到底挂在哪个控件上，而不是只看 QObject parent。

### `setGeometry(const QRect &r)` / `geometry() const`

`setGeometry()` 是布局真正分配位置的入口。标准布局会在这里给每个 item 计算矩形；自定义布局也主要重写这个函数。

应用代码通常不直接调用它。直接设置布局几何容易和父控件的自动布局流程冲突。

### `minimumSize()` / `maximumSize()` / `expandingDirections()`

这些函数汇总布局内容的尺寸能力。`minimumSize()` 表示再小会挤坏内容，`maximumSize()` 表示能接受的最大范围，`expandingDirections()` 表示是否愿意吃掉额外空间。

布局表现异常时，要沿着这条链排查：子控件 size hint、子控件 size policy、布局 stretch、布局约束、父控件约束。

### `controlTypes() const`

返回布局内部控件类型的汇总。Qt style 会利用这些信息决定默认间距，例如按钮之间、标签和输入框之间、不同控件组之间可能有不同视觉规则。

这也是为什么硬编码像素间距常常不如遵循 style 自然：平台样式其实知道哪些控件应该贴近，哪些应该分组。

### `layout()` / `isEmpty()`

因为 `QLayout` 也是 `QLayoutItem`，`layout()` 返回自身，方便父布局统一处理“控件项、布局项、空白项”。`isEmpty()` 用来判断布局项是否包含实际内容。

在自定义布局中，正确实现这些语义能让嵌套布局和父布局协同工作。

### `closestAcceptableSize(const QWidget *widget, const QSize &size)`

静态工具函数，返回一个满足控件所有尺寸约束、同时尽量接近目标尺寸的值。它会考虑 `heightForWidth()` 这类非线性尺寸关系。

当你想根据用户拖拽、保存的窗口尺寸或外部配置恢复大小时，它能避免把窗口恢复到一个违反约束的尺寸。

### `addChildLayout(QLayout *childLayout)` / `addChildWidget(QWidget *w)`

这两个保护函数服务自定义布局。添加子布局或控件时先调用它们，让 Qt 正确维护父子关系、布局管理关系和警告检查。

顺序很重要：通常先登记 child，再把对应 item 放入自己的数据结构。否则一个控件可能同时被两个布局认为自己管理，后续几何会混乱。

### `alignmentRect(const QRect &r) const`

根据布局的尺寸提示、扩展方向和对齐方式，从给定矩形中计算实际应占用的矩形。它常用于自定义布局实现对齐行为。

返回矩形不会大于输入矩形；如果布局可以扩展，结果往往就是原矩形。

### `childEvent(QChildEvent *e)`

处理 QObject 子对象变化。普通应用代码基本不会碰它；它存在是为了让布局对象在 QObject 父子关系变化时维护内部状态。

自定义布局若没有非常明确的理由，通常不需要重写它。

## 5. 深入实践与常见坑

### 布局不是“自动好看”

布局只执行规则。界面是否舒服，取决于你是否给对了 `sizePolicy`、stretch、边距、间距和层级。一个常见经验是：外层控制页面呼吸感，内层控制字段关系，控件自身表达扩展意愿。

### 清空布局要处理所有权

`takeAt()` 之后拿到的是布局项。删除 item 之前，如果里面有子布局，需要递归清空；如果里面有控件，要决定是 `deleteLater()`、隐藏、还是转移到新布局。不要只 `delete item` 然后以为界面对象都消失了。

### 不要用固定尺寸掩盖布局问题

看到控件挤压时，先查尺寸策略和 stretch。过早 `setFixedSize()` 会让界面在高 DPI、翻译文本变长、系统字体变化时失去弹性。

### 自定义布局的最小职责

一个可用的自定义布局至少要实现 `addItem()`、`count()`、`itemAt()`、`takeAt()`、`setGeometry()` 和尺寸提示相关函数。只实现能编译的几个函数，往往会得到一个能显示但不能正确缩放的布局。
