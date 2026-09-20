# Qt Widgets 基础（下）：动态布局与自定义 Layout

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Widgets  
> 核心类型：`QLayout`、`QLayoutItem`、`QWidgetItem`、`QSpacerItem`  
> 本篇目标：安全地动态增删界面、理解布局失效与尺寸约束，并掌握自定义流式布局的核心实现。

## 1. 动态布局比静态布局难在哪里

静态界面在构造时建立一次。动态界面还要处理：

- 插入和移除后的索引变化；
- LayoutItem 与 QWidget 的两层所有权；
- 隐藏和删除的区别；
- 尺寸建议缓存失效；
- 焦点和 Tab 顺序；
- 正在处理事件的对象不能立即删除；
- 批量更新时的闪烁和重复布局；
- 异步结果到达时目标页面可能已销毁。

安全动态界面的核心是：先定义对象寿命和数据身份，再修改布局。

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. 最小可用代码：动态添加和删除行

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

class ListEditor : public QWidget
{
public:
    ListEditor()
    {
        rows_ = new QVBoxLayout;
        auto *add = new QPushButton("添加一行");

        auto *mainLayout = new QVBoxLayout(this);
        mainLayout->addLayout(rows_);
        mainLayout->addStretch();
        mainLayout->addWidget(add);

        connect(add, &QPushButton::clicked,
                this, &ListEditor::addRow);
        addRow();
    }

private:
    void addRow()
    {
        auto *rowWidget = new QWidget(this);
        auto *row = new QHBoxLayout(rowWidget);
        row->setContentsMargins(0, 0, 0, 0);

        row->addWidget(new QLineEdit);
        auto *remove = new QPushButton("删除");
        row->addWidget(remove);

        connect(remove, &QPushButton::clicked,
                rowWidget, &QObject::deleteLater);
        rows_->addWidget(rowWidget);
    }

    QVBoxLayout *rows_ = nullptr;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    ListEditor window;
    window.resize(480, 300);
    window.show();
    return app.exec();
}
```

用一个 rowWidget 封装整行后，只需删除容器，内部布局和控件随 QObject 树一起清理。比逐个移除 LayoutItem 更不易出错。

## 4. 动态插入

标准布局通常提供 insert API：

```cpp
box->insertWidget(index, widget);
box->insertLayout(index, childLayout);
box->insertSpacing(index, 8);
box->insertStretch(index, 1);
```

Grid 和 Form 按行列或角色插入：

```cpp
grid->addWidget(widget, row, column);
form->insertRow(row, label, field);
```

插入后所有后续位置可能变化。业务对象不要用布局下标作为永久 ID。

## 5. removeWidget、takeAt 和删除

### 5.1 removeWidget

```cpp
layout->removeWidget(widget);
```

停止布局管理，但 Widget 仍存在、parent 通常不变，也不自动隐藏。

### 5.2 takeAt

```cpp
QLayoutItem *item = layout->takeAt(index);
```

返回从布局中取出的 Item，调用者接管该 LayoutItem 的删除责任。

```cpp
if (QLayoutItem *item = layout->takeAt(index)) {
    if (QWidget *widget = item->widget())
        widget->deleteLater();
    delete item;
}
```

删除 Item 不等于删除它包装的 Widget；必须分别决定。

### 5.3 replaceWidget

```cpp
QLayoutItem *oldItem = layout->replaceWidget(oldWidget, newWidget);
if (oldItem) {
    oldWidget->hide();
    oldWidget->deleteLater();
    delete oldItem;
}
```

返回的 Item 不再由布局管理，调用者负责删除。替换搜索默认可递归进入子布局；多个位置可能出现同类 Widget 时，应传准确指针而不是按类型猜测。

## 6. 递归清空布局

通用清空函数必须同时处理 Widget、子 Layout 和 Spacer：

```cpp
void clearLayout(QLayout *layout)
{
    while (QLayoutItem *item = layout->takeAt(0)) {
        if (QWidget *widget = item->widget()) {
            widget->deleteLater();
        } else if (QLayout *child = item->layout()) {
            clearLayout(child);
            delete child;
        }

        delete item;
    }
}
```

注意：

- 如果 Widget 要复用，不要删除；先 hide，再加入其他布局；
- `deleteLater()` 依赖事件循环；
- 子 Layout 不是 QWidget，不能调用 deleteLater；
- 删除 parent Widget 通常比递归清空更简单；
- 不能在遍历 `itemAt(i)` 时一边删除一边递增 i，否则索引移动会跳项。

## 7. 优先删除容器，而不是拆布局

动态卡片、表单行、面板最好有独立 QWidget 根：

```text
rowsLayout
  └─ rowWidget
       └─ rowLayout
            ├─ editor
            └─ removeButton
```

删除 rowWidget 就能让对象树回收内部 Widget，布局也随 parent 销毁。只有需要保留内部控件或搬迁布局时才逐 Item 操作。

## 8. 隐藏、移除、删除如何选

| 需求         | 操作                               |
| ---------- | -------------------------------- |
| 临时不显示，稍后恢复 | `setVisible(false)`              |
| 移到另一个布局    | `removeWidget()` 后 `addWidget()` |
| 永久销毁       | `deleteLater()`                  |
| 只切换多个固定页面  | `QStackedWidget/Layout`          |
| 一整组动态消失    | 删除组的根容器 Widget                   |

频繁创建销毁昂贵页面时可隐藏复用；页面状态必须重置时重建更简单。根据寿命和状态成本选择。

## 9. QFormLayout 动态行

Qt 6.4 起可直接隐藏整行：

```cpp
form->setRowVisible(advancedEdit, false);
bool visible = form->isRowVisible(advancedEdit);
```

它会一起处理标签和字段，比分别 hide 更可靠。

删除并销毁：

```cpp
form->removeRow(field);
```

取出保留：

```cpp
QFormLayout::TakeRowResult result = form->takeRow(field);
// result.labelItem 和 result.fieldItem 由调用方处理
```

TakeRowResult 返回的是 Item，不是简单的两个 QWidget 指针；可能包装 Widget 或 Layout，必须检查类型并安排所有权。

## 10. delete 与 deleteLater

在按钮自己的 clicked 槽中删除整行时：

```cpp
rowWidget->deleteLater();
```

比立即 `delete rowWidget` 更稳妥，因为当前事件调用栈可能仍使用发送者或其祖先。deleteLater 在控制返回所属线程事件循环后删除。

但应用退出后或没有事件循环的线程中，延迟删除时机需单独确认。GUI Widget 必须在 GUI 线程销毁。

## 11. 批量修改和界面更新

大量添加 Widget 会反复触发布局和绘制。可以短暂关闭容器更新：

```cpp
container->setUpdatesEnabled(false);

for (const Item &item : items)
    addRow(item);

container->setUpdatesEnabled(true);
container->update();
```

必须保证所有退出路径都重新启用。更好的性能方案通常是 Model/View，而不是创建成千上万个 Widget。

不要通过频繁 `processEvents()` 让批量创建“看起来响应”，它可能引发重入和对象在中途被删除。真正耗时的数据处理放后台线程，UI 分批构建或使用视图虚拟化。

## 12. invalidate、activate 与 update

### 12.1 invalidate

```cpp
layout->invalidate();
```

清除布局缓存的尺寸和几何信息，等待重新计算。标准控件属性变化通常会自动触发，不应到处手动调用。

### 12.2 activate

```cpp
bool changed = layout->activate();
```

立即重做布局，若重新布局则返回 true。一般事件循环会自动处理；只有后续同步代码必须立刻读取新 geometry 时才考虑。

### 12.3 QWidget::updateGeometry

控件的 sizeHint 变化时由控件调用，通知父布局。

### 12.4 QWidget::update

只请求重绘，不负责重新协商理想尺寸。

```text
内容外观变化       → update()
内容理想尺寸变化   → updateGeometry()
布局内部缓存无效   → invalidate()
必须同步完成布局   → activate()
```

## 13. sizeConstraint

布局可以约束其父 Widget：

```cpp
layout->setSizeConstraint(QLayout::SetMinimumSize);
```

常见值：

| 约束                     | 含义                |
| ---------------------- | ----------------- |
| `SetDefaultConstraint` | 默认策略              |
| `SetFixedSize`         | 父控件固定为布局 sizeHint |
| `SetMinimumSize`       | 父控件最小值来自布局        |
| `SetMaximumSize`       | 父控件最大值来自布局        |
| `SetMinAndMaxSize`     | 同时设置最小和最大         |
| `SetNoConstraint`      | 不施加约束             |

`SetFixedSize` 会让窗口无法由用户调整，翻译或动态内容变化时也可能产生突兀跳动，应谨慎使用。

### 13.1 Qt 6.10 独立方向约束

```cpp
layout->setSizeConstraints(
    QLayout::SetMinimumSize, // horizontal
    QLayout::SetFixedSize);  // vertical
```

也可分别设置 `horizontalSizeConstraint` 和 `verticalSizeConstraint`。这适合宽度可调但高度由内容固定的工具条式窗口。

## 14. closestAcceptableSize

```cpp
QSize accepted = QLayout::closestAcceptableSize(widget, requested);
```

它根据 Widget 和布局约束返回最接近的可接受尺寸。适合程序恢复历史窗口尺寸时做约束，而不是自己重复实现全部 min/max 和 height-for-width 逻辑。

## 15. 布局调试方法

### 15.1 给层级临时着色

开发期间为容器设置不同背景或边框，可定位是谁占了空间。诊断后删除样式，避免影响 size hint。

### 15.2 输出约束

```cpp
qDebug() << widget
         << "geometry" << widget->geometry()
         << "hint" << widget->sizeHint()
         << "min" << widget->minimumSize()
         << "max" << widget->maximumSize()
         << "policy" << widget->sizePolicy();
```

同时输出布局 margins、spacing、count、stretch 和 alignment。

### 15.3 从外到内排查

1. 顶层窗口实际大小；
2. 父容器 contentsRect；
3. 顶层 Layout margins；
4. 子布局分到的 geometry；
5. 目标 Item 的 min/hint/max；
6. size policy 和 stretch；
7. alignment；
8. 隐藏状态、Spacer 和跨行列设置。

只盯着目标按钮的 width，通常看不到真正约束来源。

## 16. 何时需要自定义 Layout

标准布局无法自然表达以下算法时再自定义：

- 标签像文本一样自动换行；
- 非规则环形或边界布局；
- 领域特定排列；
- 需要严格控制 Item 几何算法。

只是“左边栏 + 内容”用 Box/Grid/Splitter 即可。自定义 Layout 的测试成本很高，需要处理最小尺寸、RTL、动态增删和 height-for-width。

## 17. FlowLayout 的目标

```text
宽： [A] [BBBB] [CC] [D]

窄： [A] [BBBB]
     [CC] [D]
```

Item 沿水平轴排列，放不下时换到下一行。布局高度取决于可用宽度，所以必须支持 height-for-width。

## 18. 自定义 Layout 必需接口

```cpp
class FlowLayout : public QLayout
{
public:
    explicit FlowLayout(QWidget *parent = nullptr);
    ~FlowLayout() override;

    void addItem(QLayoutItem *item) override;
    int count() const override;
    QLayoutItem *itemAt(int index) const override;
    QLayoutItem *takeAt(int index) override;

    QSize sizeHint() const override;
    QSize minimumSize() const override;
    void setGeometry(const QRect &rect) override;

    bool hasHeightForWidth() const override;
    int heightForWidth(int width) const override;

private:
    int doLayout(const QRect &rect, bool testOnly) const;
    QList<QLayoutItem *> items_;
};
```

至少实现 addItem、count、itemAt、takeAt、sizeHint、setGeometry；实践中还应提供 minimumSize。流式布局还实现 heightForWidth。

## 19. Item 容器与析构

```cpp
void FlowLayout::addItem(QLayoutItem *item)
{
    items_.append(item);
}

int FlowLayout::count() const
{
    return items_.size();
}

QLayoutItem *FlowLayout::itemAt(int index) const
{
    return items_.value(index);
}

QLayoutItem *FlowLayout::takeAt(int index)
{
    if (index < 0 || index >= items_.size())
        return nullptr;
    return items_.takeAt(index);
}

FlowLayout::~FlowLayout()
{
    while (QLayoutItem *item = takeAt(0))
        delete item;
}
```

`addItem()` 传入后，Layout 接管 LayoutItem，所以析构必须删除仍持有的 Item。Widget 自身仍按 QObject 父子树销毁；删除 QWidgetItem 不直接删除 Widget。

## 20. 最小尺寸

```cpp
QSize FlowLayout::minimumSize() const
{
    QSize size;
    for (QLayoutItem *item : items_)
        size = size.expandedTo(item->minimumSize());

    const QMargins m = contentsMargins();
    return size + QSize(m.left() + m.right(),
                        m.top() + m.bottom());
}

QSize FlowLayout::sizeHint() const
{
    return minimumSize();
}
```

这只是保守实现。生产布局可根据典型行宽估算更合适 size hint，但结果应稳定、计算应快速。

## 21. heightForWidth 与测试布局

```cpp
bool FlowLayout::hasHeightForWidth() const
{
    return true;
}

int FlowLayout::heightForWidth(int width) const
{
    return doLayout(QRect(0, 0, width, 0), true);
}
```

`testOnly=true` 只计算所需高度，不调用 Item 的 `setGeometry()`。布局系统可能多次查询，测试计算不能修改可观察状态。

## 22. 核心换行算法

```cpp
int FlowLayout::doLayout(const QRect &rect, bool testOnly) const
{
    const QMargins margins = contentsMargins();
    const QRect area = rect.adjusted(
        margins.left(), margins.top(),
        -margins.right(), -margins.bottom());

    const int hSpace = spacing() >= 0 ? spacing() : 6;
    const int vSpace = spacing() >= 0 ? spacing() : 6;

    int x = area.x();
    int y = area.y();
    int lineHeight = 0;

    for (QLayoutItem *item : items_) {
        const QSize itemSize = item->sizeHint();
        const int nextX = x + itemSize.width() + hSpace;

        if (nextX - hSpace > area.right() && lineHeight > 0) {
            x = area.x();
            y += lineHeight + vSpace;
            lineHeight = 0;
        }

        if (!testOnly)
            item->setGeometry(QRect(QPoint(x, y), itemSize));

        x += itemSize.width() + hSpace;
        lineHeight = qMax(lineHeight, itemSize.height());
    }

    return y + lineHeight - rect.y() + margins.bottom();
}
```

真正通用实现还应：

- 从 QStyle 查询水平/垂直 spacing，而非固定 6；
- 处理空布局；
- 处理 Item alignment 和最大尺寸；
- 考虑 RTL；
- 对单个超宽 Item 定义策略；
- 处理子 Item 的 height-for-width；
- 缓存昂贵计算并在 invalidate 时清除。

## 23. setGeometry

```cpp
void FlowLayout::setGeometry(const QRect &rect)
{
    QLayout::setGeometry(rect);
    doLayout(rect, false);
}
```

先让基类记录 Layout 自身 geometry，再实际分配子项。

不要从 `setGeometry()` 调用父 Widget 的 resize，容易产生布局递归和抖动。布局只应在给定矩形内安排子项。

## 24. 从 QStyle 取得 spacing

顶层布局的默认间距通常来自 Widget Style，子布局可继承父布局 spacing。自定义 Layout 不应硬编码同一个像素值跨平台使用。

```cpp
int value = parentWidget()->style()->pixelMetric(
    QStyle::PM_LayoutHorizontalSpacing);
```

更完整实现可使用 `combinedLayoutSpacing()`，按相邻控件的 ControlType 和方向查询。没有 parentWidget 时还要处理 parent layout。

## 25. RTL 与自定义布局

FlowLayout 在 RTL 下通常应从右向左放置，换行规则也相应镜像。可读取：

```cpp
Qt::LayoutDirection direction = parentWidget()
    ? parentWidget()->layoutDirection()
    : QApplication::layoutDirection();
```

自定义布局若忽略这一点，会让标准控件已经镜像而排列方向仍反常。

## 26. 自定义布局的缓存

heightForWidth 可能被频繁调用。可缓存 `width -> height`，但必须在这些情况清除：

- Item 添加、移除、替换；
- 子控件 sizeHint 改变；
- 字体、样式或 DPI 改变；
- spacing 或 margins 改变；
- 布局方向改变。

重写 `invalidate()`：

```cpp
void FlowLayout::invalidate()
{
    cachedWidth_ = -1;
    cachedHeight_ = -1;
    QLayout::invalidate();
}
```

错误缓存比不缓存更危险，会造成只在字体或屏幕变化后出现的错位。

## 27. 测试自定义布局

至少覆盖：

1. 空布局；
2. 一个 Item；
3. 恰好放满一行；
4. 多次换行；
5. 单项宽于可用宽度；
6. 动态添加和 remove/take；
7. 不同 minimum/maximum/sizeHint；
8. 隐藏 Item；
9. RTL；
10. 高 DPI 和大字体；
11. 父窗口反复缩放；
12. 析构时无泄漏或二次删除。

几何测试应断言 Item 不重叠、不越过预期区域，且 heightForWidth 与实际 setGeometry 的结果一致。

## 28. 何时改用 Model/View

如果动态布局中有几百或几千个重复卡片，不要继续优化 Widget 创建循环。Model/View 只为可见项绘制，能显著降低：

- QObject 数量；
- 布局计算；
- 内存；
- 启动时间；
- 信号连接数量。

布局适合有限数量的独立控件；海量同构数据适合列表、表格或自定义 View/Delegate。

## 29. 常见错误

### 29.1 只 delete LayoutItem

Widget 仍在对象树中，可能继续显示或泄漏业务状态。分别处理 Item 和 Widget。

### 29.2 递增索引同时 takeAt

每次取出后剩余项左移，会跳过一半。始终循环 `takeAt(0)`。

### 29.3 立即删除信号发送者祖先

当前调用栈仍可能访问对象。使用 deleteLater，让事件返回后删除。

### 29.4 到处 activate

破坏 Qt 合并布局请求的优化并引发重复计算。只在确需同步读取新 geometry 时调用。

### 29.5 自定义 Layout 忘记删除 Item

addItem 转移 LayoutItem 所有权，析构必须清理。

### 29.6 heightForWidth 修改 geometry

查询函数应只计算。真正设置位置放在 setGeometry。

### 29.7 自定义布局硬编码 spacing

平台、字体和样式改变后不协调。查询 QStyle，处理父布局继承。

### 29.8 大量 Widget 强行动态布局

界面卡顿的根因是对象和布局规模。改用 Model/View 虚拟化。

## 30. API 速查表

| API                            | 用途              | 注意点              |
| ------------------------------ | --------------- | ---------------- |
| `insertWidget()`               | 指定位置插入          | 后续索引变化           |
| `removeWidget()`               | 解除布局管理          | 不删除、不隐藏          |
| `takeAt()`                     | 取出 LayoutItem   | 调用者删除 Item       |
| `replaceWidget()`              | 替换 Widget       | 返回旧 Item，调用者负责   |
| `QFormLayout::setRowVisible()` | 整行显隐            | Qt 6.4 起         |
| `QFormLayout::takeRow()`       | 取出并保留整行         | 处理 TakeRowResult |
| `invalidate()`                 | 清除布局缓存          | 通常自动调用           |
| `activate()`                   | 同步执行布局          | 不要滥用             |
| `updateGeometry()`             | 通知 size hint 变化 | 控件侧调用            |
| `setSizeConstraint()`          | 约束父 Widget 尺寸   | Fixed 谨慎使用       |
| `setSizeConstraints()`         | 分方向约束           | Qt 6.10 起        |
| `QLayout::addItem()`           | 自定义布局接收 Item    | 转移 Item 所有权      |
| `setGeometry()`                | 分配 Item 几何      | 不 resize 父控件     |
| `heightForWidth()`             | 给定宽度求高度         | 只计算、不改状态         |

## 31. 自测题

### 题 1：takeAt 返回后要处理哪两层

<details><summary>答案</summary>

处理 QLayoutItem 本身，并分别决定其中 QWidget 或子 Layout 的保留、转移或删除。删除 Item 不自动等于删除 Widget。

</details>

### 题 2：为什么循环 takeAt(0)

<details><summary>答案</summary>

取出元素后其余索引左移。递增索引会跳项，而反复取 0 直到 nullptr 能清空全部。

</details>

### 题 3：invalidate 和 update 有何不同

<details><summary>答案</summary>

invalidate 清除布局的尺寸/几何缓存；QWidget::update 请求重绘。尺寸建议变化通常还需要 updateGeometry。

</details>

### 题 4：FlowLayout 为什么实现 heightForWidth

<details><summary>答案</summary>

可用宽度决定每行能放多少 Item，进而决定总行数和高度，因此高度依赖宽度。

</details>

### 题 5：addItem 后谁删除 LayoutItem

<details><summary>答案</summary>

自定义 Layout 接管 Item，必须在 take/remove 后由接收方处理，或在 Layout 析构时删除仍持有的 Item。

</details>

## 32. 本篇总结

1. 动态布局同时涉及布局项和 QObject 两套所有权，remove、take 与 delete 必须分清。
2. 一组动态控件优先封装在根 Widget 中，通过删除容器简化清理。
3. 外观变用 update，尺寸建议变用 updateGeometry，布局缓存变用 invalidate。
4. Qt 6.10 可对水平和垂直方向分别设置布局尺寸约束。
5. 自定义 Layout 必须完整实现 Item 容器、尺寸建议和几何分配，并清理 Item。
6. FlowLayout 的高度依赖宽度，查询计算与实际 setGeometry 应共用同一算法。
7. 自定义算法必须考虑样式 spacing、RTL、动态变化和缓存失效。
8. 大规模重复项目不要用海量 Widget，下一章的 Model/View 才是合适工具。

至此，Qt Widgets 布局系统从标准布局、尺寸协商到动态和自定义 Layout 已完整覆盖。下一章进入 Model/View 架构。
