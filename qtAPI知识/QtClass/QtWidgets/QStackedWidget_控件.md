# Qt QStackedWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStackedWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QFrame -> QStackedWidget`  
> 定位：可直接放进界面的多页面容器控件

## 1. QStackedWidget 解决什么问题

`QStackedWidget` 是“只显示当前一页”的容器控件。它把若干页面 widget 放在同一位置，由整数索引或页面指针决定当前显示哪一页。

```text
外层布局
  ├─ 导航栏 / 按钮组 / 列表
  └─ QStackedWidget
       ├─ page 0：欢迎页
       ├─ page 1：账户页
       └─ page 2：完成页
```

它适合：

- 设置窗口左侧导航切换右侧内容；
- 多步骤向导的内容区；
- 登录前后、空状态与正常状态之间切换；
- 不需要标签栏、但希望自定义导航样式的页面容器。

`QStackedWidget` 与 `QTabWidget` 的区别是它没有自带 tab bar；与 `QStackedLayout` 的区别是它本身就是一个 `QFrame` 控件，可以直接 `addWidget()` 到外层布局，能设置 frame、样式、背景和 size policy。

它也没有内建的“下一页”按钮或页面标题模型。导航控件和页面名称由业务层维护，这给了你设计自由，也要求你处理好导航条与页面列表的同步。

## 2. 最小可用示例：按钮驱动的三步向导

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QStackedWidget>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *mainLayout = new QVBoxLayout(&window);

    auto *pages = new QStackedWidget;
    pages->addWidget(new QLabel("第 1 步：选择项目"));
    pages->addWidget(new QLabel("第 2 步：确认参数"));
    pages->addWidget(new QLabel("第 3 步：完成"));

    auto *previousButton = new QPushButton("上一步");
    auto *nextButton = new QPushButton("下一步");
    auto *buttonRow = new QHBoxLayout;
    buttonRow->addWidget(previousButton);
    buttonRow->addStretch();
    buttonRow->addWidget(nextButton);

    mainLayout->addWidget(pages, 1);
    mainLayout->addLayout(buttonRow);

    QObject::connect(previousButton, &QPushButton::clicked, [&] {
        pages->setCurrentIndex(qMax(0, pages->currentIndex() - 1));
    });
    QObject::connect(nextButton, &QPushButton::clicked, [&] {
        pages->setCurrentIndex(
            qMin(pages->count() - 1, pages->currentIndex() + 1));
    });

    window.resize(420, 220);
    window.show();
    return app.exec();
}
```

这个例子把 `QStackedWidget` 当作普通控件加入外层布局。页面切换只改变当前页，不会创建或销毁其他页面；需要延迟加载很重的页面时，应该在首次进入该页时再创建内容，而不是期待 stack 自动懒加载。

## 3. 页面所有权：addWidget 与 removeWidget 的关键差异

```cpp
auto *editorPage = new QWidget;
int index = pages->addWidget(editorPage);
```

`addWidget()` 与 `insertWidget()` 会把页面所有权交给 `QStackedWidget`。因此通常可以直接 `new QWidget` 后加入，不需要再手动 delete；容器销毁时，页面会随 QObject 父子树销毁。

移除则容易误解：

```cpp
pages->removeWidget(editorPage);
// editorPage 没被 delete，但仍是 pages 的 child，且已隐藏

editorPage->setParent(otherContainer);
otherLayout->addWidget(editorPage);
```

`removeWidget()` 不会 delete 页面，但页面的 QObject parent 和 QWidget parent 仍然是该 `QStackedWidget`。官方建议若要复用移除页，显式 reparent。否则它虽然不再是 stack 页面，仍会随着旧容器销毁，或者作为隐藏 child 留在对象树中。

这正是它和“从 `std::vector` 删除一个元素”不同的地方：界面对象同时有列表归属、父子对象归属和可见状态三层关系。

## 4. 索引不是稳定 ID

页面按内部顺序编号：

```cpp
int general = pages->addWidget(generalPage);
int network = pages->addWidget(networkPage);

pages->insertWidget(1, proxyPage);
// network 的旧索引可能已经改变
```

`insertWidget(index, widget)` 的规则：

- 索引在范围外时，页面被追加到末尾，返回实际索引；
- 空容器插入第一页时，该页自动成为当前页；
- 新页面插在当前页索引之前或正好当前位置时，当前页面对象不变，但 `currentIndex()` 会加一。

所以动态插件页、可选步骤或运行时增删页时：

- 只有结构固定时，才适合使用常量索引；
- 已持有页面对象时，优先 `setCurrentWidget(page)`；
- 需要找索引时调用 `indexOf(page)`，找不到返回 `-1`；
- 删除页、插入页后的导航标签也必须同步更新。

## 5. 当前页、信号与导航同步

```cpp
connect(sidebar, &QListWidget::currentRowChanged,
        pages, &QStackedWidget::setCurrentIndex);

connect(pages, &QStackedWidget::currentChanged,
        sidebar, &QListWidget::setCurrentRow);
```

`currentIndex()` 是当前显示页的索引；容器没有页面时为 `-1`。`currentWidget()` 返回页面指针；容器为空时为 `nullptr`。切换时发出 `currentChanged(int)`，参数是新的索引，空容器时为 `-1`。

上面的双向连接在简单场景可用，但动态增删页时更推荐指定一个单向数据源，或更新前先比较值。否则一个导航更新可能再次触发页面切换，调试时会看到重复信号。

Qt 6.9 还提供：

- `widgetAdded(int index)`：页面被追加或插入；
- `widgetRemoved(int index)`：页面被移除。

它们特别适合同步一个自定义侧栏、页面计数器或动态创建的导航菜单。

## 6. QStackedWidget、QStackedLayout 与 QTabWidget 怎么选

| 类型 | 选它的理由 | 不适合的情况 |
| --- | --- | --- |
| `QStackedWidget` | 想把页面容器直接加入布局，并通过 `QFrame` 外观包装它。 | 需要页面同时叠加显示。 |
| `QStackedLayout` | 页面区只是现有 QWidget 内部的一个布局，或需要 `StackAll` 覆盖层模式。 | 希望获得一个独立可视控件。 |
| `QTabWidget` | 希望 Qt 提供 tab bar、可选关闭按钮和标签页交互。 | 导航不是标签页，或需要完全自定义导航。 |

无论使用 `QStackedWidget` 还是 `QStackedLayout`，都要自己提供“用户如何切换”的交互；它们不像 `QTabWidget` 那样天然可点击。

## 7. 尺寸、外观与页面设计

`QStackedWidget` 是 `QFrame`，因此可以使用 `setFrameShape()`、`setFrameShadow()`、style sheet 等继承能力给内容区画边界。它放在外层布局里时，外层负责分配它的矩形，当前页面填充这个矩形。

实际页面设计上有两个常见问题：

- 某个页面的最小尺寸很大时，stack 的整体最小尺寸会被它抬高；不要把巨型预览、日志或表格直接塞进固定尺寸的向导页。
- 页面切换并不自动调整顶层窗口到“当前页刚好大小”。窗口要随内容调整时，结合 `adjustSize()`、`QLayout::SetFixedSize` 或你自己的窗口策略，不要依赖 stack 的默认行为。

## API 速查表
### 8.1 创建、页面列表与当前页

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStackedWidget(QWidget *parent = nullptr)` | 创建可视的堆叠页面容器 | 可直接作为 widget 加入外层 layout |
| 生命周期 | `~QStackedWidget()` | 销毁容器与它拥有的资源 | 已加入的页面通常随 QObject 父子树销毁 |
| 页面 | `addWidget(QWidget *widget)` | 将页面追加到末尾并返回索引 | 容器原本为空时，该页自动成为当前页；所有权转交给容器 |
| 页面 | `insertWidget(int index, QWidget *widget)` | 将页面插入指定位置并返回实际索引 | 越界时追加；插到当前页之前会改变 current index |
| 页面 | `removeWidget(QWidget *widget)` | 从 stack 页面列表移除页面 | 不 delete；仍以 stack 为 parent 且会隐藏。复用前显式 `setParent()` |
| 页面 | `count() const` | 返回当前页面数量 | 初始为 0 |
| 查询 | `indexOf(const QWidget *widget) const` | 返回指定页面的索引 | 不是 child 时返回 `-1` |
| 查询 | `widget(int index) const` | 返回指定索引页面 | 索引无效时返回 `nullptr` |
| 当前页 | `currentIndex() const` | 返回当前显示页索引 | 空容器为 `-1` |
| 当前页 | `currentWidget() const` | 返回当前显示页 | 空容器为 `nullptr` |
| 切换 | `setCurrentIndex(int index)` | 切换到指定索引的页面 | 常与列表当前行、组合框索引或按钮逻辑连接 |
| 切换 | `setCurrentWidget(QWidget *widget)` | 切换到已包含的指定页面 | 目标页必须已经属于该 stack |

### 8.2 通知与框架扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `currentChanged(int index)` | 当前页改变时发出 | 连接导航 UI、标题和按钮启用状态；空 stack 时为 `-1` |
| 信号 | `widgetAdded(int index)` | 页面被添加或插入时发出 | Qt 6.9 引入；用于维护动态创建的导航列表 |
| 信号 | `widgetRemoved(int index)` | 页面被移除时发出 | 处理后续页索引变化；不要缓存旧索引 |
| 事件 | `event(QEvent *event)` | `QFrame::event()` 的重实现 | 自定义派生控件拦截事件时才涉及；普通使用不直接调用 |

### 8.3 继承但很常用的能力

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 框架 | `setFrameShape()` / `setFrameShadow()`（继承自 `QFrame`） | 设置内容区的边框形状和阴影 | 需要明显内容边界时使用；现代扁平界面通常保持简洁 |
| 伸缩 | `setSizePolicy()`（继承自 `QWidget`） | 声明 stack 在外层布局中如何伸缩 | 中央内容区常设为可扩展 |
| 尺寸 | `setMinimumSize()` / `setMaximumSize()`（继承自 `QWidget`） | 限制容器尺寸边界 | 不要用它取代各页面正确的 layout |
| 可见性 | `show()` / `hide()`（继承自 `QWidget`） | 显示或隐藏整个页面容器 | 与切换当前内部页面是两件事 |
