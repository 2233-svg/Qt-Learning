# Qt QLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QObject`、`QLayoutItem`  
> 定位：所有 QWidget 布局管理器共同遵守的抽象基类

## 1. QLayout 解决的不是“排成一行”，而是尺寸协商

`QLayout` 是 Qt Widgets 布局系统的抽象基类。它不直接定义“横向排列”“网格排列”或“表单排列”这些具体规则；这些工作由 `QBoxLayout`、`QGridLayout`、`QFormLayout`、`QStackedLayout` 等派生类完成。

它解决的核心问题是：**父控件可用的矩形，怎样在子控件之间可靠地分配。**

如果用固定坐标摆放控件：

```cpp
button->move(100, 80);
button->resize(120, 32);
```

那么窗口大小、DPI 缩放、字体、主题和翻译文本一变化，这些坐标就可能失效。布局系统则要求每个项目提供尺寸信息：

- `sizeHint()`：推荐多大；
- `minimumSize()`：最小能多小；
- `maximumSize()`：最大能多大；
- `QSizePolicy`：是否愿意吸收额外空间；
- `heightForWidth()`：宽度变化时，高度是否也会变化。

布局据此计算每个子项的最终 geometry，并在窗口大小、内容、字体或样式变化后重新计算。

## 2. 它在布局体系中的位置

```text
QObject
  └─ QLayout
       ├─ QBoxLayout
       │    ├─ QHBoxLayout
       │    └─ QVBoxLayout
       ├─ QGridLayout
       ├─ QFormLayout
       └─ QStackedLayout

QLayoutItem
  ├─ QLayout
  ├─ QWidgetItem
  └─ QSpacerItem
```

`QLayout` 同时具有两种身份：

1. 它是 `QObject`，因此有父子对象和生命周期管理。
2. 它也是 `QLayoutItem`，因此一个布局可以作为另一个布局的子项。

```cpp
auto *mainLayout = new QVBoxLayout(parentWidget);
auto *buttons = new QHBoxLayout;

mainLayout->addLayout(buttons);
```

`buttons` 既是布局，也是在 `mainLayout` 眼中的一个布局项。

## 3. 日常开发怎么选布局

绝大多数业务代码不需要直接继承 `QLayout`。

| 界面结构 | 推荐类 | 解决的问题 |
| --- | --- | --- |
| 单行或单列 | `QHBoxLayout` / `QVBoxLayout` | 按一条主轴排列控件 |
| 标签与字段配对 | `QFormLayout` | 表单标签列与输入列对齐 |
| 行列和跨格 | `QGridLayout` | 网格、表格和仪表盘布局 |
| 多个页面只显示一个 | `QStackedLayout` | 页面切换，避免手动管理 geometry |
| 特殊流式、环形或领域规则排列 | 自定义 `QLayout` | 现有布局无法表达的排列算法 |

例如普通设置页面应优先组合现成布局：

```cpp
#include <QCheckBox>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

class SettingsWidget final : public QWidget
{
public:
    SettingsWidget()
    {
        auto *mainLayout = new QVBoxLayout(this);

        auto *formLayout = new QFormLayout;
        formLayout->addRow("服务器：", new QLineEdit);
        formLayout->addRow("自动保存：", new QCheckBox);
        mainLayout->addLayout(formLayout);

        auto *buttons = new QHBoxLayout;
        buttons->addStretch();
        buttons->addWidget(new QPushButton("取消"));
        buttons->addWidget(new QPushButton("应用"));
        mainLayout->addLayout(buttons);
    }
};
```

这些具体布局都遵守 `QLayout` 的尺寸、所有权和更新规则。

## 4. 顶层布局、嵌套布局与对象所有权

### 4.1 给 QWidget 设置顶层布局

```cpp
QWidget window;
auto *layout = new QVBoxLayout(&window);
```

传入 `&window` 后，该布局会成为 `window` 的顶层布局。这等价于：

```cpp
QWidget window;
auto *layout = new QVBoxLayout;
window.setLayout(layout);
```

一个 `QWidget` 只能有一个顶层布局。多个区域应该使用嵌套布局表达：

```text
窗口
└─ 顶层 QVBoxLayout
   ├─ 标题控件
   ├─ QFormLayout
   └─ 按钮 QHBoxLayout
```

### 4.2 布局管理 geometry，不等于它删除了所有控件

控件加入布局后，布局负责控件的位置和尺寸；控件通常由父 `QWidget` 的对象树管理。移除控件时要明确目标：

```cpp
layout->removeWidget(editor); // 解除布局关系，不删除 editor
editor->deleteLater();        // 确实不再需要时才删除
```

- 临时不显示：`editor->hide()`；
- 移到新位置：移除后加入新布局；
- 永久删除：`deleteLater()` 或在可控生命周期中 `delete`。

### 4.3 QLayoutItem 是布局保存的真正单位

布局内部保存的不是纯 `QWidget *`，而是 `QLayoutItem *`：

- 控件会包装成 `QWidgetItem`；
- 子布局本身是一个 `QLayoutItem`；
- 空白项是 `QSpacerItem`。

这也是自定义布局必须实现 `addItem()`、`itemAt()` 和 `takeAt()` 的原因：Qt 需要统一地管理三种项目。

## 5. 一次布局计算是如何进行的

可以把一次布局过程理解为：

1. 父控件或父布局把可用 `QRect` 交给当前布局。
2. 当前布局扣除 `contentsMargins()`。
3. 它读取每个项目的最小尺寸、推荐尺寸、最大尺寸和扩展能力。
4. 它按具体算法处理 spacing、stretch、alignment 和 `QSizePolicy`。
5. 它对每个子项调用 `setGeometry()`。
6. 子布局再递归把自己的矩形分给下一级项目。

`QLayout` 的价值在于建立这一套契约。它不规定具体算法，却规定每种布局如何告诉 Qt：

- 我有多少直接子项；
- 某个索引上是什么项目；
- 取走某项目时所有权如何交接；
- 我推荐、至少、至多需要多大；
- 父布局给我矩形时，我如何分配给子项。

## 6. 尺寸协商：最常见问题的根源

布局的尺寸不是由单一 API 决定，而是多个约束共同作用。

| 信息 | 含义 | 典型影响 |
| --- | --- | --- |
| `sizeHint()` | 推荐尺寸 | 按钮文字、输入框内容影响初始合适大小 |
| `minimumSize()` | 最小尺寸 | 窗口再小也尽量不能低于它 |
| `maximumSize()` | 最大尺寸 | 防止控件无限拉伸 |
| `QSizePolicy` | 扩展/收缩意愿 | 哪些控件优先获得或让出空间 |
| stretch | 剩余空间的相对分配 | `QBoxLayout`、`QGridLayout` 中尤其重要 |

例如 stretch 没有让输入框变宽时，排查顺序应是：

1. 父窗口是否真的有剩余空间；
2. 输入框是否被 `setFixedWidth()` 或最大尺寸限制；
3. `QSizePolicy` 是否允许水平扩展；
4. 其它子项是否占满了可用空间；
5. stretch 是否设置在正确的布局和正确的主轴上。

不要把 `stretch = 0` 理解成“永远不变大”；它只是不给该项额外的伸缩权重，Qt 仍会参考尺寸策略。

## 7. 尺寸约束：限制的是父控件，不是每个子控件

`QLayout::SizeConstraint` 控制布局对**父控件尺寸**施加的约束：

```cpp
layout->setSizeConstraint(QLayout::SetFixedSize);
```

这不是把每个子控件固定成同样的尺寸，而是让布局所在窗口根据布局需求调整可接受的大小。

| 枚举值 | 作用 | 适合什么场景 |
| --- | --- | --- |
| `SetDefaultConstraint` | 使用默认约束 | 普通窗口 |
| `SetNoConstraint` | 不额外限制父控件 | 自己在外部管理窗口尺寸 |
| `SetFixedSize` | 父控件固定为布局推荐尺寸 | 内容决定大小的小工具对话框 |
| `SetMinimumSize` | 父控件不能缩小到布局最小尺寸以下 | 防止表单被压到无法操作 |
| `SetMaximumSize` | 父控件不能超过布局允许的最大尺寸 | 限制弹出窗口无限放大 |
| `SetMinAndMaxSize` | 同时应用最小与最大限制 | 需要严格尺寸范围的窗口 |

Qt 6.10 起可以分别设置横向与纵向约束：

```cpp
layout->setSizeConstraints(
    QLayout::SetMinimumSize,
    QLayout::SetMaximumSize);
```

这适合宽高规则不同的窗口，例如宽度至少容纳字段，而高度不能超过内容所允许的范围。

## 8. Margin、Spacing 和内容矩形

```cpp
layout->setContentsMargins(12, 8, 12, 8);
layout->setSpacing(6);

QMargins margins = layout->contentsMargins();
QRect content = layout->contentsRect();
```

三个概念必须区分：

| 概念 | 影响范围 | 用来解决什么 |
| --- | --- | --- |
| `contentsMargins` | 布局边缘到内容区 | 控件不要贴窗口边缘 |
| `spacing` | 相邻布局项之间 | 控件之间不要挤在一起 |
| `contentsRect` | 扣除边距后布局可使用的矩形 | 自定义布局计算每个项目位置 |

`setSpacing()` 不会修改窗口边缘的留白；边缘太宽或太窄时应检查 `contentsMargins()`。

如果希望恢复 Qt style 提供的默认边距：

```cpp
layout->unsetContentsMargins();
```

普通应用优先让 style 决定默认值。只有视觉规范明确要求固定留白时，才把像素值写死。

## 9. 动态界面：添加、移除、替换和清空

### 9.1 `addWidget()` 与 `addItem()`

普通业务代码最常用：

```cpp
layout->addWidget(editor);
```

这是把控件包装成布局项并追加到末尾的便利函数。具体派生布局通常提供额外参数，例如 `QBoxLayout::addWidget()` 的 stretch 和 alignment。

`addItem()` 是更底层的抽象接口，主要由自定义布局实现：

```cpp
void MyLayout::addItem(QLayoutItem *item)
{
    items_.append(item); // 接管 item 的所有权
}
```

### 9.2 三种移除 API 的区别

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 移除控件 | `removeWidget(QWidget *)` | 让指定控件不再参与当前布局 | 控件仍存在，调用方决定隐藏、换父对象、加入别处或删除 |
| 移除布局项 | `removeItem(QLayoutItem *)` | 从布局中移除指定布局项 | 调用方仍要处理该项以及它指向的 widget、子布局或 spacer |
| 取出布局项 | `takeAt(int index)` | 按索引移除项目，并把 `QLayoutItem` 所有权交给调用方 | 清空布局时最常用；返回项必须释放或重新安置，避免泄漏 |

清空布局时使用 `takeAt()`：

```cpp
void clearLayout(QLayout *layout)
{
    while (QLayoutItem *item = layout->takeAt(0)) {
        if (QWidget *widget = item->widget()) {
            widget->deleteLater();
        } else if (QLayout *childLayout = item->layout()) {
            clearLayout(childLayout);
            delete childLayout;
        }
        delete item;
    }
}
```

这里有两层资源：

1. `QLayoutItem` 是布局的包装项；
2. 包装项指向的 `QWidget` 或子 `QLayout` 也有各自的生命周期。

如果控件要迁移到另一个页面，就不应直接 `deleteLater()`；应把它取出、设置好新父控件，并加入目标布局。

### 9.3 `replaceWidget()` 用于保留原布局位置

```cpp
QLayoutItem *oldItem =
    layout->replaceWidget(oldEditor, newEditor);

delete oldItem;
oldEditor->deleteLater();
```

`replaceWidget()` 在布局树中查找旧控件，用新控件替换它，并保留原位置的布局信息。它适合：

- 登录后把“登录”控件区域换成账户信息；
- 把只读 `QLabel` 替换为编辑用 `QLineEdit`；
- 根据配置在同一位置切换不同编辑器。

函数返回的旧 `QLayoutItem *` 不归布局自动销毁，调用方必须处理。

## 10. 查询、对齐、菜单栏和更新

### 10.1 遍历布局项目

```cpp
for (int i = 0; i < layout->count(); ++i) {
    QLayoutItem *item = layout->itemAt(i);
    if (QWidget *widget = item ? item->widget() : nullptr)
        widget->setEnabled(false);
}
```

`itemAt()` 只查看，所有权仍属于布局。项目可能是控件、子布局或 spacer：

```cpp
if (item->widget()) {
    // QWidgetItem
} else if (item->layout()) {
    // 子 QLayout
} else if (item->spacerItem()) {
    // QSpacerItem
}
```

`indexOf()` 仅查找当前布局的直接项。控件位于更深层子布局时，需要自己递归遍历。

### 10.2 设置直接子项的对齐方式

```cpp
layout->setAlignment(button, Qt::AlignRight);
layout->setAlignment(buttonRow, Qt::AlignBottom);
```

这两个重载设置的是某个直接子项在其布局单元格内的对齐方式，不是改变整个布局的排列方向。返回 `false` 表示目标不属于当前布局。

### 10.3 `setMenuBar()`

```cpp
auto *menuBar = new QMenuBar;
layout->setMenuBar(menuBar);
```

该函数把指定控件作为布局的菜单栏，布局会在内容区上方为它留出空间。一般 `QWidget` 内部可以使用；对于 `QMainWindow`，应优先使用 `QMainWindow::setMenuBar()`，因为主窗口有专门的菜单、工具栏、状态栏和停靠窗口管理机制。

### 10.4 `invalidate()`、`activate()` 与 `update()`

```cpp
layout->invalidate();
layout->activate();
layout->update();
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 布局缓存 | `invalidate()` | 标记布局缓存、尺寸提示或几何计算结果已经过期 | 自定义布局内部数据变化时要调用；普通控件增删通常由 Qt 自动安排 |
| 立即重算 | `activate()` | 立即尝试重新计算并应用布局 | 只有修改后马上读取 geometry 时才需要；频繁调用会增加不必要的布局成本 |
| 延后更新 | `update()` | 请求稍后进行布局更新 | 适合一轮事件循环内合并多次变化；不保证调用后立刻获得新 geometry |

普通控件的增删和属性修改会触发 Qt 的更新安排，不要每次改动都手动 `activate()`。自定义布局维护了尺寸缓存时，才需要特别重视 `invalidate()`。

## 11. 什么时候必须自己继承 QLayout

现有布局不能表达需求时再继承，例如：

- 文本标签块要像网页一样流式换行；
- 控件沿圆弧、时间轴或画布规则排列；
- 项目分组、折叠和行高受复杂业务规则控制；
- 希望把一套特殊排列算法封装成可复用组件。

自定义布局至少必须实现：

| 必须实现的函数 | 解决的问题 |
| --- | --- |
| `addItem()` | 接收并保存新布局项，接管所有权 |
| `count()` | 告诉 Qt 当前有多少直接子项 |
| `itemAt()` | 让 Qt 和调用方按索引查看布局项 |
| `takeAt()` | 移除项目并把所有权交还给调用方 |
| `sizeHint()` | 告诉父布局推荐尺寸 |
| `setGeometry()` | 接收父布局分配矩形，再分给每个子项 |

通常还应按需要重写：

- `minimumSize()`、`maximumSize()`；
- `expandingDirections()`；
- `hasHeightForWidth()`、`heightForWidth()`、`minimumHeightForWidth()`；
- `invalidate()`。

### 11.1 一个自定义布局的最小骨架

```cpp
#include <QLayout>
#include <QList>

class SimpleLayout final : public QLayout
{
public:
    explicit SimpleLayout(QWidget *parent = nullptr)
        : QLayout(parent)
    {
    }

    ~SimpleLayout() override
    {
        while (QLayoutItem *item = takeAt(0))
            delete item;
    }

    void addItem(QLayoutItem *item) override
    {
        items_.append(item);
    }

    int count() const override
    {
        return items_.size();
    }

    QLayoutItem *itemAt(int index) const override
    {
        return index >= 0 && index < items_.size()
            ? items_.at(index)
            : nullptr;
    }

    QLayoutItem *takeAt(int index) override
    {
        return index >= 0 && index < items_.size()
            ? items_.takeAt(index)
            : nullptr;
    }

    QSize sizeHint() const override
    {
        return QSize(240, 120);
    }

    void setGeometry(const QRect &rect) override
    {
        QLayout::setGeometry(rect);

        int y = rect.top();
        for (QLayoutItem *item : items_) {
            const int height = item->sizeHint().height();
            item->setGeometry(QRect(rect.left(), y, rect.width(), height));
            y += height + spacing();
        }
    }

private:
    QList<QLayoutItem *> items_;
};
```

骨架展示的是约定，不是完整生产级算法：

- `addItem()` 必须保存指针，因为布局接管 item 所有权；
- `itemAt()` 只查看，不转移所有权；
- `takeAt()` 必须转移所有权；
- `setGeometry()` 必须真正给每个子项设置 geometry；
- 析构时清理仍由自己持有的 `QLayoutItem`。

完整实现还必须把 margins、minimum/maximum size、hidden item、`QSizePolicy` 和可能的换行考虑进去。

## 12. 宽度决定高度：`heightForWidth`

自动换行的 `QLabel` 是典型例子：宽度变小时，同一段文本会占更多行，因此高度需要增加。

布局体系用以下 API 表达这个关系：

```cpp
if (layout->hasHeightForWidth()) {
    const int neededHeight = layout->heightForWidth(320);
}
```

自定义流式布局、自动换行布局或任何宽度影响排版高度的布局，应做到：

1. `hasHeightForWidth()` 返回 `true`；
2. `heightForWidth(width)` 计算给定宽度下的推荐高度；
3. `minimumHeightForWidth(width)` 给出可接受的最小高度；
4. 项目、字体、间距或 margin 改变时让缓存失效。

如果漏掉这些契约，窗口变窄后父布局仍会按旧高度分配空间，容易出现裁剪或重叠。

## 13. 常见误区与排查

### 13.1 试图实例化 QLayout

`QLayout` 是抽象类，不能直接创建。普通界面应选择具体布局；需要特殊算法时才派生。

### 13.2 同一 QWidget 设置多个顶层布局

一个 QWidget 只能有一个顶层布局。多个区域应嵌套布局，而不是重复 `setLayout()`。

### 13.3 把 spacing 当成边距

`spacing` 管控相邻项目距离；窗口边缘留白由 `contentsMargins` 管控。

### 13.4 `removeWidget()` 后以为控件被删了

该函数只解除布局关系。控件仍存在，需要由代码决定隐藏、迁移还是删除。

### 13.5 清空布局时只删 QLayoutItem

布局项可能包装 widget 或子 layout。使用 `takeAt()` 后，分别处理 widget、子布局和布局项本身。

### 13.6 在 `resizeEvent()` 里手动摆所有控件

普通界面优先调整布局嵌套、size policy、stretch、margin 和 spacing。手动 `setGeometry()` 容易与布局系统下一次计算相互覆盖。

### 13.7 忽略最小/最大尺寸

stretch 只能分配现有剩余空间，不能突破最小/最大尺寸和 `QSizePolicy` 的限制。

## API 速查表
表中覆盖 `QLayout` 自己声明、重写和供派生类使用的 API；`QObject` 与 `QLayoutItem` 继承来的通用成员请结合对应类笔记阅读。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QLayout::SizeConstraint` | 定义布局如何约束父控件尺寸。 | 用于窗口/对话框尺寸策略，不是固定子控件大小。 |
| 枚举值 | `SetDefaultConstraint` | 使用布局的默认尺寸约束策略。 | 普通窗口的默认选择。 |
| 枚举值 | `SetNoConstraint` | 不额外通过布局限制父控件尺寸。 | 外部代码自行控制窗口大小时使用。 |
| 枚举值 | `SetFixedSize` | 将父控件限制为布局推荐尺寸。 | 内容大小固定的小对话框。 |
| 枚举值 | `SetMinimumSize` | 把布局最小尺寸施加到父控件。 | 防止窗口被缩到无法使用。 |
| 枚举值 | `SetMaximumSize` | 把布局最大尺寸施加到父控件。 | 限制窗口无限扩大。 |
| 枚举值 | `SetMinAndMaxSize` | 同时应用布局最小和最大尺寸。 | 父控件可调整范围需要严格受限时。 |
| 属性 | `contentsMargins : QMargins` | 保存内容区四边的内边距。 | 与 `spacing` 区分；修改用两个 `setContentsMargins()` 重载。 |
| 属性 | `sizeConstraint : SizeConstraint` | 保存统一的尺寸约束策略。 | 对话框大小由内容决定时常用。 |
| 属性 | `spacing : int` | 保存相邻布局项之间的间距。 | 不影响布局最外侧留白。 |
| 属性 | `horizontalSizeConstraint : SizeConstraint`（Qt 6.10） | 保存水平方向的尺寸约束。 | 宽高策略不同时使用，注意最低 Qt 版本。 |
| 属性 | `verticalSizeConstraint : SizeConstraint`（Qt 6.10） | 保存垂直方向的尺寸约束。 | 可与 horizontal 组合形成非对称约束。 |
| 构造函数 | `QLayout(QWidget *parent = nullptr)` | 创建布局；传入 QWidget 时成为其顶层布局。 | 一个 QWidget 只能有一个顶层布局；子布局通常不传 QWidget。 |
| 公共函数 | `bool activate()` | 立即尝试重新计算并应用布局。 | 只有需马上读取新 geometry 时调用；普通情况下 Qt 会自行更新。 |
| 公共函数 | `void addWidget(QWidget *w)` | 把控件加入布局末尾。 | 普通添加控件的入口；具体派生布局通常有带 stretch/alignment 的重载。 |
| 公共函数 | `QMargins contentsMargins() const` | 返回当前四边内容边距。 | 读取 margin；新代码通常优于指针形式的 getter。 |
| 公共函数 | `QRect contentsRect() const` | 返回扣除内容边距后的可用矩形。 | 自定义布局分配子项 geometry 时使用。 |
| 公共函数 | `void getContentsMargins(int *left, int *top, int *right, int *bottom) const` | 分别取得四边内容边距。 | 旧接口或需要四个独立整数时使用。 |
| 公共函数 | `SizeConstraint horizontalSizeConstraint() const`（Qt 6.10） | 返回水平方向的尺寸约束。 | 水平约束会覆盖统一的 `sizeConstraint`；需要 Qt 6.10 或更高版本。 |
| 公共函数 | `int indexOf(const QLayoutItem *layoutItem) const` | 返回直接布局项的索引。 | 找不到返回 `-1`；不递归子布局。 |
| 公共函数 | `int indexOf(const QWidget *widget) const` | 返回直接控件项的索引。 | 找不到返回 `-1`；深层嵌套需要自行遍历。 |
| 公共函数 | `bool isEnabled() const` | 查询布局是否启用。 | 不等同于禁用所有子控件。 |
| 公共函数 | `QWidget *menuBar() const` | 返回布局当前使用的菜单栏控件。 | `QMainWindow` 场景优先用主窗口专用 API。 |
| 公共函数 | `QWidget *parentWidget() const` | 返回布局的父控件。 | 动态更新时确认布局属于哪个 QWidget。 |
| 公共函数 | `void removeItem(QLayoutItem *item)` | 从布局中移除指定布局项。 | 移除不等于自动删除关联对象；后续生命周期需明确。 |
| 公共函数 | `void removeWidget(QWidget *widget)` | 从布局中移除指定控件。 | 控件仍存在，可隐藏、迁移或 `deleteLater()`。 |
| 公共函数 | `QLayoutItem *replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options = Qt::FindChildrenRecursively)` | 在布局树中用新控件替换旧控件。 | 适合保留原位置与布局参数；返回的旧 item 由调用方处理。 |
| 公共函数 | `bool setAlignment(QWidget *w, Qt::Alignment alignment)` | 设置直接控件项在单元格内的对齐。 | 返回 false 表示控件不在当前布局；不改变布局方向。 |
| 公共函数 | `bool setAlignment(QLayout *l, Qt::Alignment alignment)` | 设置直接子布局项在单元格内的对齐。 | 与 QWidget 重载区分参数类型。 |
| 公共函数 | `void setContentsMargins(const QMargins &margins)` | 通过 `QMargins` 设置四边内边距。 | 适合已经以值对象保存边距的代码。 |
| 公共函数 | `void setContentsMargins(int left, int top, int right, int bottom)` | 分别设置左、上、右、下内边距。 | 参数顺序固定；不修改 item 间距。 |
| 公共函数 | `void setEnabled(bool enable)` | 启用或停用布局的自动布局行为。 | 不用于批量禁用用户交互控件。 |
| 公共函数 | `void setHorizontalSizeConstraint(SizeConstraint constraint)`（Qt 6.10） | 设置水平方向的父控件尺寸约束。 | 设置后覆盖统一 `sizeConstraint` 在水平方向上的效果。 |
| 公共函数 | `void setMenuBar(QWidget *widget)` | 指定布局上方的菜单栏控件。 | 适用于普通 QWidget；主窗口优先自己的 API。 |
| 公共函数 | `void setSizeConstraint(SizeConstraint constraint)` | 设置统一的父控件尺寸约束。 | 改变窗口约束，不是子控件的 fixed size。 |
| 公共函数 | `void setSizeConstraints(SizeConstraint horizontal, SizeConstraint vertical)`（Qt 6.10） | 分别设置横向和纵向尺寸约束。 | 宽高需要不同规则时使用。 |
| 公共函数 | `void setSpacing(int spacing)` | 设置相邻布局项之间的距离。 | 只影响项之间；边缘留白另设 margins。 |
| 公共函数 | `void setVerticalSizeConstraint(SizeConstraint constraint)`（Qt 6.10） | 设置垂直方向的父控件尺寸约束。 | 设置后覆盖统一 `sizeConstraint` 在垂直方向上的效果。 |
| 公共函数 | `SizeConstraint sizeConstraint() const` | 返回统一尺寸约束策略。 | 检查当前父控件尺寸限制。 |
| 公共函数 | `int spacing() const` | 返回当前项间距。 | 可能返回 style/父布局决定的值；自定义布局计算间距时读取。 |
| 公共函数 | `int totalMinimumHeightForWidth(int w) const` | 返回包含边距和菜单栏在内的给定宽度最小高度。 | 需要按完整布局外框计算尺寸时使用，而不是只看内容项。 |
| 公共函数 | `int totalHeightForWidth(int w) const` | 返回包含边距和菜单栏在内的给定宽度推荐高度。 | height-for-width 布局需要估算父控件总高度时使用。 |
| 公共函数 | `QSize totalMinimumSize() const` | 返回包含边距和菜单栏的总最小尺寸。 | 与 `minimumSize()` 区分，后者是布局项自身尺寸协商结果。 |
| 公共函数 | `QSize totalMaximumSize() const` | 返回包含边距和菜单栏的总最大尺寸。 | 计算父控件允许最大尺寸时使用。 |
| 公共函数 | `QSize totalSizeHint() const` | 返回包含边距和菜单栏的总推荐尺寸。 | 对话框按布局内容调整大小时常比裸 `sizeHint()` 更接近最终需求。 |
| 公共函数 | `void unsetContentsMargins()`（Qt 6.1） | 取消显式边距并恢复默认边距。 | 希望重新交给 Qt style 决定边距时使用。 |
| 公共函数 | `void update()` | 请求稍后重新执行布局更新。 | 自定义布局状态改变后可调用；通常不是同步操作。 |
| 公共函数 | `SizeConstraint verticalSizeConstraint() const`（Qt 6.10） | 返回垂直方向的尺寸约束。 | 垂直约束会覆盖统一的 `sizeConstraint`；需要 Qt 6.10 或更高版本。 |
| 静态函数 | `QSize closestAcceptableSize(const QWidget *widget, const QSize &size)` | 计算最接近给定值、同时符合控件和布局约束的尺寸。 | 调整窗口前需要预估合法 QSize 时使用。 |
| 受保护函数 | `void addChildLayout(QLayout *childLayout)` | 把子布局接入布局对象树。 | 自定义布局接收子布局项时使用，保持 Qt 父子关系正确。 |
| 受保护函数 | `void addChildWidget(QWidget *w)` | 把控件接入当前布局的 QWidget 层级。 | 自定义布局添加控件项时使用，避免错误的 parent 关系。 |
| 受保护函数 | `bool adoptLayout(QLayout *layout)` | 尝试接管一个子布局并设置正确父子关系。 | 自定义布局处理传入子布局时使用，失败时不要继续把它当成已接管对象。 |
| 受保护函数 | `QRect alignmentRect(const QRect &r) const` | 按布局自身 alignment 从给定矩形算出实际使用矩形。 | 自定义布局需要遵守 alignment 时使用。 |
| 受保护函数 | `void widgetEvent(QEvent *event)` | 处理布局关联 widget 的事件。 | Qt 内部布局更新链路使用，普通派生布局很少直接碰。 |
| 受保护函数 | `void childEvent(QChildEvent *e)` | 处理 QObject 子对象增删事件。 | 通常由 Qt 内部调用；重写时保持基类行为。 |
| 受保护构造 | `QLayout(QLayoutPrivate &d, QLayout *layout, QWidget *widget)` | 供 Qt 内部或深度派生类使用的 d-pointer 构造入口。 | 普通自定义布局使用公开构造函数即可。 |
| 必须实现 | `void addItem(QLayoutItem *item)` | 接收并保存新布局项。 | 接管 item 所有权，不能只暂存 widget 指针。 |
| 必须实现 | `int count() const` | 返回直接布局项数量。 | 必须与 `itemAt()`、`takeAt()` 的索引范围一致。 |
| 必须实现 | `QLayoutItem *itemAt(int index) const` | 按索引查看项，不转移所有权。 | 越界返回 `nullptr`。 |
| 必须实现 | `QLayoutItem *takeAt(int index)` | 按索引取走项并转移所有权。 | 越界返回 `nullptr`；调用方处理返回对象。 |
| 必须实现 | `QSize sizeHint() const` | 返回整个布局推荐尺寸。 | 应综合子项、margin 和 spacing，不能随意硬编码。 |
| 必须实现 | `void setGeometry(const QRect &r)` | 将父布局给出的矩形分配给子项。 | 布局算法核心；通常先调用 `QLayout::setGeometry(r)`。 |
| 常重写 | `QSizePolicy::ControlTypes controlTypes() const` | 汇总子项控件类型信息。 | 与 style 和尺寸协商有关，通常从子项推导。 |
| 常重写 | `Qt::Orientations expandingDirections() const` | 报告布局愿意在哪些方向扩展。 | 自定义布局决定多余空间可在哪个方向被吸收。 |
| 常重写 | `QRect geometry() const` | 返回当前布局已被分配的矩形。 | 由 `setGeometry()` 更新，通常只读查询。 |
| 常重写 | `void invalidate()` | 使缓存的尺寸/位置结果失效。 | 子项、字体、margin、spacing 或算法数据变化后使用。 |
| 常重写 | `bool isEmpty() const` | 报告布局是否为空或没有有效可见项。 | 隐藏项和空子布局的语义要保持一致。 |
| 常重写 | `QLayout *layout()` | 让布局作为 `QLayoutItem` 时返回自己。 | Qt 递归遍历嵌套布局时使用。 |
| 常重写 | `QSize maximumSize() const` | 返回布局可接受的最大尺寸。 | 自定义布局有上限时综合子项约束计算。 |
| 常重写 | `QSize minimumSize() const` | 返回布局可接受的最小尺寸。 | 必须考虑子项最小尺寸、margin 和 spacing。 |
| 继承后常重写 | `bool hasHeightForWidth() const` | 报告高度是否依赖宽度。 | 流式换行或自动换行布局应正确实现。 |
| 继承后常重写 | `int heightForWidth(int width) const` | 返回指定宽度下的推荐高度。 | 与 `hasHeightForWidth()` 配合避免窗口变窄后裁剪。 |
| 继承后常重写 | `int minimumHeightForWidth(int width) const` | 返回指定宽度下的最小高度。 | 宽度影响换行时实现，供上层布局协商。 |

## 15. 建议的学习顺序

1. `QLayoutItem`：认识控件项、子布局项和 spacer 的统一接口。
2. `QSizePolicy`：理解“控件为什么不愿意拉伸/收缩”。
3. `QBoxLayout`：理解主轴、stretch、插入和嵌套布局。
4. `QGridLayout`：理解行列、跨度和行列拉伸。
5. `QFormLayout`：理解标签-字段语义。
6. `QWidget`：理解顶层布局、父子控件和最终 geometry。

### 一句话总结

`QLayout` 是 QWidget 布局系统的公共契约：它管理 `QLayoutItem`，参与尺寸协商，接收父级 geometry，并把几何区域递归分配给子项。普通项目选择具体布局类组合即可；只有现有布局无法表达排列规则时，才继承 `QLayout` 自己实现算法。
