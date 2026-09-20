# Qt QStackedLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStackedLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QLayout -> QStackedLayout`  
> 定位：在同一块矩形区域中管理多个页面或覆盖层的布局

## 1. QStackedLayout 解决什么问题

一个设置窗口通常一次只显示一个页面：常规、网络、外观、快捷键。不同页面共享同一块内容区域，切换时不应手动 hide/show 一堆控件，也不应为每页单独弹出窗口。

`QStackedLayout` 把多个子 `QWidget` 视为按索引排列的页面：

```text
导航列表                  同一个内容矩形
+----------+        +-----------------------+
| 常规     | -----> | 当前页面：常规设置     |
| 网络     |        |                       |
+ 外观     +        +-----------------------+
+----------+
```

它负责页面的几何、可见性和当前页；它**不提供**标签栏、列表或上一页/下一页按钮。页面怎样切换由应用决定，常见做法是把 `QListWidget::currentRowChanged`、`QComboBox` 或按钮连接到 `setCurrentIndex()`。

```text
QTabWidget       = 标签页导航 UI + 堆叠页面
QStackedWidget   = QWidget 容器 + 内部 QStackedLayout
QStackedLayout   = 仅布局机制，适合嵌入自定义界面
```

需要一个直接可放进父布局的页面容器时，通常用 `QStackedWidget` 更省事；已经有外层 `QWidget` 或想将堆叠区嵌入某个复合布局时，`QStackedLayout` 更轻。

## 2. 最小可用示例：导航列表驱动三页设置

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QListWidget>
#include <QStackedLayout>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *mainLayout = new QHBoxLayout(&window);

    auto *navigation = new QListWidget;
    navigation->addItems({"常规", "网络", "外观"});

    auto *pageHost = new QWidget;
    auto *pages = new QStackedLayout(pageHost);
    pages->addWidget(new QLabel("常规设置页面"));
    pages->addWidget(new QLabel("网络设置页面"));
    pages->addWidget(new QLabel("外观设置页面"));

    mainLayout->addWidget(navigation);
    mainLayout->addWidget(pageHost, 1);

    QObject::connect(navigation, &QListWidget::currentRowChanged,
                     pages, &QStackedLayout::setCurrentIndex);
    navigation->setCurrentRow(0);

    window.resize(520, 300);
    window.show();
    return app.exec();
}
```

`QStackedLayout(pageHost)` 使它成为 `pageHost` 的顶层布局；`pageHost` 再被加入外层水平布局。直接把一个无 parent 的 `QStackedLayout` 加到 `QHBoxLayout` 中也可以，但用独立 host widget 往往更清楚，尤其是页面区域需要边框、背景或单独的 size policy 时。

## 3. 页面、索引和当前页

页面在内部列表中的位置就是索引。首个加入的 widget 会自动成为当前页：

```cpp
int generalIndex = pages->addWidget(generalPage); // 通常为 0
int networkIndex = pages->addWidget(networkPage); // 通常为 1

pages->setCurrentIndex(networkIndex);
QWidget *visible = pages->currentWidget();
```

三个概念要分清：

| 概念 | 含义 | 空布局时的结果 |
| --- | --- | --- |
| `count()` | 堆叠中页面的数量。 | `0` |
| `currentIndex()` | 当前页在内部列表中的索引。 | `-1` |
| `currentWidget()` | 当前页对象。 | `nullptr` |

页面增删会改变后续页面的索引。不要把 `1`、`2` 这类裸索引散落在业务逻辑中；要么保存 `addWidget()` 的返回值并在结构变化后更新，要么保存页面指针并通过继承自 `QLayout` 的 `indexOf()` 查询。

```cpp
pages->setCurrentWidget(networkPage); // networkPage 必须已在 pages 中
```

相比索引，`setCurrentWidget()` 更适合“我已经持有目标页面指针”的代码。传入不属于该 layout 的 widget 不满足此 API 的前提，先通过 `indexOf()` 检查更稳妥。

## 4. 添加与插入页面：索引变化的规则

```cpp
pages->addWidget(logPage);             // 追加并返回实际索引
pages->insertWidget(1, proxyPage);     // 插入第 1 位，并返回实际索引
```

- `addWidget()` 始终追加到末尾；空 stack 的第一个页面自动变成当前页。
- `insertWidget(index, widget)` 试图插入到 `index`；索引越界时改为追加，并返回实际插入位置。
- 如果新页面插入的位置小于或等于当前索引，当前页面**对象**不变，但它的 `currentIndex()` 加一。

最后一条是动态菜单或插件页最常见的坑：代码若只缓存当前索引，插入页面后可能指向另一页；若缓存 `currentWidget()` 指针，则仍能识别原页面。

## 5. StackOne 与 StackAll

`StackingMode` 决定 stack 怎样处理子页面的可见性：

| 模式 | 行为 | 使用场景 |
| --- | --- | --- |
| `StackOne` | 只有当前页可见。默认模式。 | 向导页、设置页、普通多页面界面。 |
| `StackAll` | 所有页面可见，但当前页会被 raise 到最上层。 | 覆盖层、画布上的辅助绘制、引导遮罩。 |

```cpp
pages->setStackingMode(QStackedLayout::StackAll);
pages->setCurrentWidget(selectionOverlay);
```

`StackAll` 不是普通的“多页面显示”。各 child widget 会占据同一几何区域，绘制和鼠标事件也可能相互影响。覆盖层通常需要透明背景、合适的属性、明确的 `raise()`/当前页管理和事件策略；若只是希望同时排多个控件，应使用 `QBoxLayout` 或 `QGridLayout`。

## 6. 删除、取出与对象生命周期

`QStackedLayout` 的析构不会直接销毁其页面 widgets；页面通常由所在的父 `QWidget` 对象树负责销毁。动态移除时，常用的基类 API 有两种：

```cpp
pages->removeWidget(networkPage);  // 解除页面与 layout 的关系，不 delete 页面

int index = pages->indexOf(logPage);
QLayoutItem *item = pages->takeAt(index); // 取出布局项，也不 delete
```

- `removeWidget()` 继承自 `QLayout`，适合只想停止管理一个页面。若不再使用该页面，调用者仍需决定何时删除它或安排新的父对象。
- `takeAt()` 取出的是 `QLayoutItem *`，不是 `QWidget *`。需要 `item->widget()` 才能取得其中页面，并且调用者要负责 item 的生命周期。
- 删除页面会触发 `widgetRemoved(index)`；如果当前页改变，还会触发 `currentChanged(index)`。在信号处理函数中不要假设旧索引仍然指向原 widget。

页面从 stack 移出后，其 parent widget 不会因此自动变成 `nullptr`。若要把它放到另一个容器，直接加入新布局即可；若要脱离界面对象树，再明确调用 `setParent(nullptr)` 并自行管理生命周期。

## 7. 信号：让导航 UI 与页面列表保持同步

```cpp
connect(pages, &QStackedLayout::currentChanged,
        navigation, &QListWidget::setCurrentRow);

connect(pages, &QStackedLayout::widgetAdded,
        this, [navigation](int index) {
            navigation->insertItem(index, "新页面");
        });
```

- `currentChanged(index)`：当前页变化时发出；当 stack 变空时，参数为 `-1`。
- `widgetAdded(index)`：页面被添加或插入时发出，Qt 6.9 引入。
- `widgetRemoved(index)`：页面从 layout 移除时发出。

若导航控件的信号也会回写 `setCurrentIndex()`，双向连接可能造成重复通知或意外的 index 变化。通常选择一个“真源”：导航驱动 stack，或 stack 驱动导航；需要双向同步时，在更新前比较当前索引，或使用 `QSignalBlocker`。

## 8. 尺寸提示为何像“最大的一页”

虽然默认只显示一页，`QStackedLayout` 仍必须让父布局为页面切换预留合理空间。它重实现了 `minimumSize()`、`sizeHint()`、`hasHeightForWidth()` 和 `heightForWidth()`，把页面的尺寸需求合并后交给父布局。

这意味着：

- 某一个很大的隐藏页可能让整个窗口的推荐尺寸变大；
- 页面尺寸差异极大时，切页后窗口未必会自动缩小到新页面大小；
- 若外层窗口需随当前页收缩，必须结合 `adjustSize()`、最小/最大约束或自己的窗口策略设计，不能假定 stack 自动做窗口动画。

## API 速查表
### 9.1 类型、属性与构造

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `StackingMode` | 决定非当前页是否可见。 | 用 `stackingMode()` / `setStackingMode()` 访问。 |
| 枚举值 | `StackOne` | 仅显示当前页。默认值。 | 普通设置页、向导和页面切换。 |
| 枚举值 | `StackAll` | 所有页面可见，当前页只会被提升到顶层。 | 绘制覆盖层；注意事件与透明区域。 |
| 只读属性 | `count` | stack 内页数。 | 对应 `count()`。 |
| 属性 | `currentIndex` | 当前页索引。无当前页为 `-1`。 | 通过 `currentChanged(int)` 观察。 |
| 属性 | `stackingMode` | 子页面的可见性处理模式。 | 默认 `StackOne`。 |
| 构造函数 | `QStackedLayout()` | 创建无 parent 的堆叠布局。 | 之后必须安装到 QWidget 或加入父 layout 才生效。 |
| 构造函数 | `QStackedLayout(QLayout *parentLayout)` | 创建并立即插入父布局。 | 适合直接嵌入既有复合布局。 |
| 构造函数 | `QStackedLayout(QWidget *parent)` | 创建并作为 parent 的顶层布局。 | parent 只能拥有一个顶层布局。 |
| 析构函数 | `~QStackedLayout()` | 销毁布局。 | 不直接销毁页面 widgets。 |

### 9.2 页面增删、查找与切换

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 添加 | `addWidget(QWidget *widget)` | 追加页面并返回其索引 | 空 stack 的首个页面自动成为当前页 |
| 插入 | `insertWidget(int index, QWidget *widget)` | 在指定索引插入页面并返回实际索引 | 越界时追加；插到当前页之前会使 current index 增加但不切页 |
| 数量 | `count() const` | 返回页面数量 | 不包含被 `removeWidget()` 移出的页面 |
| 查询 | `widget(int index) const` | 返回指定索引页面 | 索引无效时返回 `nullptr` |
| 当前页 | `currentIndex() const` | 返回当前页索引 | 空 stack 时为 `-1` |
| 当前页 | `currentWidget() const` | 返回当前页对象 | 空 stack 时为 `nullptr` |
| 切换 | `setCurrentIndex(int index)` | 将有效索引对应的页面设为当前页 | 可直接连接导航控件的整数信号 |
| 切换 | `setCurrentWidget(QWidget *widget)` | 将已包含的 widget 设为当前页 | 页面指针比缓存裸索引更抗插入/删除 |
| 查询 | `itemAt(int index) const` | 按内部索引返回页面对应的布局项 | 需要 widget 时调用 `item->widget()` |
| 接管 | `takeAt(int index)` | 取出布局项 | 不删除 item 或 widget；调用者处理后续所有权 |
| 底层添加 | `addItem(QLayoutItem *item)` | `QLayout::addItem()` 的重实现 | 面向布局基础设施；页面代码用 `addWidget()` |
| 移除 | `removeWidget(QWidget *widget)`（继承） | 把页面从 layout 移除 | 不 delete widget；移除后可能导致 current page 变化 |
| 查找 | `indexOf(const QWidget *widget) const`（继承） | 查找页面索引 | 动态增删后不要信任旧索引 |

### 9.3 显示模式、通知与布局计算

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 模式 | `stackingMode() const` | 读取当前堆叠模式 | 判断当前是单页还是覆盖层模式 |
| 模式 | `setStackingMode(StackingMode stackingMode)` | 设置单页或全部叠放模式 | 从 `StackAll` 切回普通页面时记得检查覆盖页状态 |
| 信号 | `currentChanged(int index)` | 当前页改变时发出的信号 | 参数为新索引；变为空 stack 时为 `-1` |
| 信号 | `widgetAdded(int index)` | 页面被添加或插入时发出的信号 | Qt 6.9 引入；适合同步动态导航列表 |
| 信号 | `widgetRemoved(int index)` | 页面被移除时发出的信号 | 处理时不要假定索引对应旧页面 |
| 高宽相关 | `hasHeightForWidth() const` | 查询 stack 高度是否随可用宽度变化 | 含自动换行等页面内容时，父布局会用到 |
| 高宽相关 | `heightForWidth(int width) const` | 计算给定宽度需要的高度 | Qt 的尺寸协商过程调用 |
| 尺寸协商 | `minimumSize() const` | 返回页面集合要求的最小尺寸 | 一个大页面会影响整个 stack 的下限 |
| 尺寸协商 | `sizeHint() const` | 返回页面集合的推荐尺寸 | 影响外层窗口初始/推荐尺寸 |
| 几何 | `setGeometry(const QRect &rect)` | 将页面区域分配给 stack 的项目 | Qt 自动调用，不要手动给页控件设 geometry |
