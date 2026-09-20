# Qt QLayoutItem 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QLayoutItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：无  
> 定位：布局中“可被测量、可被摆放”的统一抽象项

## 1. QLayoutItem 解决什么问题

一个布局里不只有控件。

以一个常见的工具栏区域为例：

```text
QHBoxLayout
├─ 返回按钮
├─ 搜索输入框
├─ 可伸缩空白
└─ 设置按钮
```

这里的“返回按钮”“搜索输入框”“设置按钮”是 `QWidget`，而“可伸缩空白”是 `QSpacerItem`。更复杂时，某一项还可能是一个嵌套的 `QLayout`。

布局算法不应该为每种对象写一套完全不同的代码。它真正关心的只有：

- 这项希望多大、最小多大、最大多大；
- 它是否愿意在横向或纵向扩展；
- 父布局给它一个矩形后，怎样把矩形应用进去；
- 它是不是可见的有效内容；
- 它到底是控件、子布局，还是空白项。

`QLayoutItem` 就是把这些共同问题抽象出来的接口。它让 `QLayout` 可以用同一套逻辑管理控件、子布局和 spacer。

```text
QLayoutItem
├─ QWidgetItem     负责把 QWidget 接入布局
├─ QSpacerItem     负责提供不可见空白
└─ QLayout          负责把一个子布局作为一个布局项嵌套
```

因此，`QLayoutItem` 不代表一个可见控件，也不负责把控件加入布局。它代表的是：**布局算法眼中的一个可测量、可分配 geometry 的单位。**

## 2. 什么时候会直接接触它

普通界面开发通常写的是：

```cpp
layout->addWidget(button);
layout->addLayout(formLayout);
layout->addStretch();
```

你不会手动创建 `QWidgetItem` 或直接调用大部分 `QLayoutItem` 成员。直接接触 `QLayoutItem` 的常见场景有三类。

### 2.1 遍历或动态清空布局

```cpp
for (int i = 0; i < layout->count(); ++i) {
    QLayoutItem *item = layout->itemAt(i);
    if (QWidget *widget = item->widget()) {
        widget->setEnabled(false);
    }
}
```

`QLayout::itemAt()` 返回的就是 `QLayoutItem *`。它让调用方不必预先知道该位置装的是控件、子布局还是 spacer。

### 2.2 调试“为什么布局结果不对”

控件没有拉伸、间距异常、隐藏控件仍留下区域时，可以读取布局项报告的尺寸和 geometry：

```cpp
QLayoutItem *item = layout->itemAt(0);
qDebug() << "hint:" << item->sizeHint()
         << "min:" << item->minimumSize()
         << "max:" << item->maximumSize()
         << "rect:" << item->geometry()
         << "expand:" << item->expandingDirections();
```

这比只看控件的 `width()` 和 `height()` 更接近布局引擎实际使用的数据。

### 2.3 实现自定义布局

自定义 `QLayout` 内部保存的是 `QLayoutItem *`，而不是只保存 `QWidget *`。这样布局可以同时容纳控件、子布局和 spacer。

```cpp
void FlowLayout::addItem(QLayoutItem *item)
{
    items_.append(item);
}
```

`QLayoutItem` 本身也是抽象类。大多数时候应继承 `QLayout` 来实现自定义排列算法，而不是单独发明一种新的布局项类型。

## 3. 它和 QWidget、QLayout、QSpacerItem 的关系

这三类项目都可以由 `QLayoutItem *` 统一访问，但它们的真实对象和所有权规则并不相同。

| 运行时类型 | 代表什么 | 如何得到真实对象 | 常见业务操作 |
| --- | --- | --- | --- |
| `QWidgetItem` | 被布局管理的控件 | `item->widget()` | 显示、隐藏、启用、替换或删除控件 |
| `QLayout` | 被嵌套的子布局 | `item->layout()` | 递归遍历、动态清空或调整子布局 |
| `QSpacerItem` | 不可见空白区域 | `item->spacerItem()` | 读取或调整空白的尺寸策略 |

安全识别一个项目的方式：

```cpp
void inspectItem(QLayoutItem *item)
{
    if (QWidget *widget = item->widget()) {
        qDebug() << "widget:" << widget;
    } else if (QLayout *childLayout = item->layout()) {
        qDebug() << "child layout:" << childLayout;
    } else if (QSpacerItem *spacer = item->spacerItem()) {
        qDebug() << "spacer:" << spacer->sizeHint();
    }
}
```

`layout()` 和 `spacerItem()` 是安全的类型识别接口：不是对应类型就返回 `nullptr`。

`widget()` 也会在没有关联控件时返回 `nullptr`，但它不是把 `QLayoutItem` 强制转换成 `QWidget`。`QWidget` 不继承 `QLayoutItem`；`QWidgetItem` 只是保存了一个控件指针并替布局转发尺寸与 geometry。

## 4. 尺寸协商：QLayoutItem 最重要的职责

布局分配空间时，首先会查询每一项的尺寸能力。

```text
minimumSize <= 实际分配的大小 <= maximumSize
                 ^
              sizeHint 是推荐值
```

### 4.1 推荐、最小和最大尺寸

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸建议 | `sizeHint()` | 返回项目在正常情况下最希望获得的尺寸 | 它是推荐值，不是硬约束；实际大小还会受父布局、size policy、stretch 和窗口空间影响 |
| 尺寸下限 | `minimumSize()` | 返回项目可以接受的最小尺寸 | 用来防止内容被压缩到不可用；自定义 item 应让它和真实绘制需求一致 |
| 尺寸上限 | `maximumSize()` | 返回项目允许的最大尺寸 | 用来限制无意义的无限拉伸；过小会让布局无法分配合理空间 |

`sizeHint()` 不是硬性大小。一个输入框的推荐宽度可能是 200，但如果父窗口更大且它的 `QSizePolicy` 允许扩展，实际宽度可以更大；如果父窗口太小，布局又会尝试向最小尺寸收缩。

### 4.2 `expandingDirections()` 不是 stretch

`expandingDirections()` 报告该项是否愿意使用超过 `sizeHint()` 的额外空间：

- `Qt::Horizontal`：愿意横向变大；
- `Qt::Vertical`：愿意纵向变大；
- 两者按位或：两个方向都愿意；
- 空值：不主动要求额外空间。

它与 `QBoxLayout` 的 stretch 有关但不是一回事：

- `QSizePolicy` / `expandingDirections()` 表达“我可不可以变大”；
- stretch 表达“多项都能变大时，剩余空间按什么比例分”。

因此，设置了较大的 stretch 仍然可能看不到变化：项目的最大尺寸或 size policy 可能不允许它扩展。

### 4.3 `geometry()` 与 `setGeometry()`

布局计算完成后，父布局会调用：

```cpp
item->setGeometry(targetRect);
```

项目保存或应用这个矩形；之后可以通过：

```cpp
QRect currentRect = item->geometry();
```

读取最终区域。

对 `QWidgetItem` 来说，`setGeometry()` 最终会影响关联 `QWidget` 的位置和大小。对 `QSpacerItem` 来说，它没有可见控件，但仍需要 geometry，以便布局计算和调试保持一致。

业务代码不应绕过布局、频繁对受布局管理的控件调用 `setGeometry()`；下一次布局更新会覆盖手动设置的矩形。

## 5. 对齐不是每个项目都支持

```cpp
item->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
Qt::Alignment alignment = item->alignment();
```

alignment 表示项目在布局给它的单元格中如何摆放，例如靠右、居中或靠底部。

它解决的是“布局单元格比项目实际尺寸大时，项目放在哪里”的问题，而不是“项目能获得多大空间”的问题。

例如一行按钮的可用宽度比按钮自身需要的宽度大，右对齐可以让按钮贴近单元格右侧；是否把多余宽度分给按钮本身，则仍由 size policy、最大尺寸和外层布局规则决定。

注意两点：

1. 并非所有 `QLayoutItem` 子类都有可见对象可对齐。Qt 的公共布局项里，`QSpacerItem` 是例外，它表示空白，没有可见对齐效果。
2. 常规业务代码更常通过 `QBoxLayout::addWidget(..., alignment)` 或 `QLayout::setAlignment(widget, alignment)` 设置，而不是直接操作 `QLayoutItem`。

## 6. 隐藏项与 `isEmpty()`

`isEmpty()` 不是简单地问“指针是否为空”，而是问该项目是否应被视为没有有效内容。

最常见的行为：

- `QWidgetItem` 在控件隐藏时报告为空；
- `QSpacerItem` 始终报告为空，因为它不包含控件；
- 子布局是否为空取决于其内部项目。

这解释了一个常见现象：把控件 `hide()` 后，布局通常会重新安排其它可见控件占用的空间。控件对象没有被删除，但对应布局项在本次布局计算中可能不再作为可见内容参与。

不要把 `isEmpty()` 当作“能否安全删除”的判断；它只服务于布局语义，和对象所有权无关。

## 7. 宽度决定高度：换行布局的关键契约

有些内容的高度取决于宽度。典型例子是自动换行的 `QLabel`：宽度变窄，文本行数变多，高度也需要增加。

`QLayoutItem` 用三组函数表达它：

```cpp
if (item->hasHeightForWidth()) {
    const int preferred = item->heightForWidth(240);
    const int minimum = item->minimumHeightForWidth(240);
}
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 宽高依赖 | `hasHeightForWidth()` | 声明项目的推荐高度是否依赖给定宽度 | 布局应先查它再调用计算函数；不要靠 `heightForWidth()` 是否返回 `-1` 表达能力 |
| 宽高依赖 | `heightForWidth(int w)` | 返回宽度为 `w` 时项目希望获得的高度 | 自动换行、流式布局常用；计算昂贵时要缓存，否则可能拖慢布局 |
| 宽高依赖 | `minimumHeightForWidth(int w)` | 返回宽度为 `w` 时项目允许的最小高度 | 默认通常跟随 `heightForWidth()`；自定义 item 要保证最小值不大于推荐值 |

默认实现中：

- `hasHeightForWidth()` 返回 `false`；
- `heightForWidth()` 返回 `-1`，表示推荐高度与宽度无关；
- `minimumHeightForWidth(w)` 默认调用 `heightForWidth(w)`。

自定义流式布局应先调用 `hasHeightForWidth()` 判断，再调用 `heightForWidth()`；不要每次都通过“返回值是否为 `-1`”判断。前者表达意图更清楚，也更高效。

如果 `heightForWidth()` 的计算需要遍历所有子项并可能触发换行，应该缓存结果。Qt 文档特别指出：缺少缓存的实现可能造成指数级布局计算时间。输入宽度、子项尺寸、边距或间距改变后，再通过 `invalidate()` 清掉缓存。

## 8. `invalidate()` 解决缓存过期问题

布局项可以缓存尺寸、行数、换行位置等计算结果。缓存提高性能，但布局输入变化后必须失效：

```cpp
void FlowLayout::invalidate()
{
    cachedWidth_ = -1;
    cachedHeight_ = -1;
    QLayout::invalidate();
}
```

常见的失效条件：

- 子项被添加、移除、隐藏或显示；
- 字体、文本、图标或 size policy 改变；
- margin、spacing、stretch 或布局方向改变；
- 自定义布局的可用宽度改变。

`invalidate()` 只表示“旧计算不能再用”，不等价于立刻完成一次可见的重新排版。它通常会与 `QLayout::update()` 或 Qt 的下一次事件循环中的布局请求配合。

## 9. 所有权：不要因为拿到 QLayoutItem 就随意 delete

`QLayoutItem` 不是 `QObject`，也没有统一的父对象树规则。其真实对象可能是包装控件的 `QWidgetItem`、子布局，或 spacer。

因此，动态操作必须区分“查看”和“取走”：

```cpp
QLayoutItem *viewOnly = layout->itemAt(0); // 不转移所有权
QLayoutItem *owned = layout->takeAt(0);    // 调用方接管 item
```

`itemAt()` 返回的指针仍归布局管理，不能删除。

`takeAt()` 返回的项目则需要调用方明确处理：

```cpp
if (QLayoutItem *item = layout->takeAt(0)) {
    if (QWidget *widget = item->widget())
        widget->deleteLater();
    delete item;
}
```

是否删除控件取决于业务目标和控件父对象，而不是 `QLayoutItem` 的存在与否。需要迁移控件时，不要删除控件；只处理包装项并把控件加入目标布局。

## 10. 自定义布局与自定义布局项

对绝大多数定制布局需求，应该继承 `QLayout`，让 Qt 自动使用现成的 `QWidgetItem`、`QSpacerItem` 和子布局项。

只有在“一个非 QWidget、非 layout、非 spacer 的对象也要参与尺寸协商”时，才考虑直接继承 `QLayoutItem`。派生类必须实现下列纯虚函数：

| 必须实现 | 目的 |
| --- | --- |
| `expandingDirections()` | 说明愿意在哪些方向扩展 |
| `geometry()` | 返回当前分配到的矩形 |
| `isEmpty()` | 报告是否有有效内容 |
| `maximumSize()` | 返回最大尺寸 |
| `minimumSize()` | 返回最小尺寸 |
| `setGeometry()` | 接收并应用父布局分配的矩形 |
| `sizeHint()` | 返回推荐尺寸 |

若该项支持自动换行或宽度相关高度，还应重写：

- `hasHeightForWidth()`；
- `heightForWidth()`；
- `minimumHeightForWidth()`；
- `invalidate()`。

一个高质量实现必须保证同一组输入下这些函数彼此一致。例如，`minimumSize()` 不应大于 `maximumSize()`；`hasHeightForWidth()` 返回 `true` 时，`heightForWidth()` 必须能够处理布局可能传入的任何非负宽度。

## 11. 常见误区与排查顺序

### 11.1 把 QLayoutItem 当作可见控件

它可能是控件、子布局或 spacer。使用 `widget()`、`layout()`、`spacerItem()` 判断真实类型，不能直接调用 QWidget API。

### 11.2 以为 `itemAt()` 返回的对象可以删除

`itemAt()` 只借出查看指针。要拿走所有权使用 `takeAt()`。

### 11.3 用 `isEmpty()` 判断是否能删除

隐藏控件和 spacer 都可能返回空，但对象仍有效。`isEmpty()` 是布局计算信息，不是生命周期信息。

### 11.4 只改 spacer 尺寸却没有重新布局

`QSpacerItem::changeSize()` 后，如果它已经加入布局，需要使布局失效，例如：

```cpp
spacer->changeSize(24, 0, QSizePolicy::Fixed, QSizePolicy::Minimum);
layout->invalidate();
```

### 11.5 自定义 `heightForWidth()` 不做缓存

换行布局的高度计算可能在一次布局过程中被反复调用。缓存最近宽度和结果，参数变化时通过 `invalidate()` 清除缓存。

### 11.6 手动给受布局管理的 QWidget 设置 geometry

布局项下一次 `setGeometry()` 会覆盖手动结果。应调整布局结构、size policy、stretch、margin 或 alignment。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QLayoutItem(Qt::Alignment alignment = Qt::Alignment())` | 创建布局项并保存初始对齐方式。 | 抽象类，不能直接实例化；并非所有派生类都支持对齐。 |
| 析构函数 | `virtual ~QLayoutItem()` | 销毁布局项对象。 | `QLayoutItem` 不是 QObject；实际删除责任取决于它是否已被布局接管。 |
| 查询 | `Qt::Alignment alignment() const` | 返回项目在布局单元格中的对齐标志。 | 对齐决定单元格内位置，不决定项目获得多少空间。 |
| 查询 | `QSizePolicy::ControlTypes controlTypes() const` | 返回该项目代表的控件类型集合，供 style 和尺寸协商参考。 | `QWidgetItem` 从控件的 `QSizePolicy` 获取；布局项则从内部内容推导。 |
| 必须实现 | `Qt::Orientations expandingDirections() const` | 说明项目能否使用超过 `sizeHint()` 的横向或纵向空间。 | 它表达扩展意愿，不是 stretch 权重；受最大尺寸和 size policy 限制。 |
| 必须实现 | `QRect geometry() const` | 返回项目当前覆盖的最终矩形。 | 用于调试布局结果；配对 API 是 `setGeometry()`。 |
| 可重写 | `bool hasHeightForWidth() const` | 声明推荐高度是否依赖宽度。 | 换行或流式布局应返回 `true`；默认 `false`。 |
| 可重写 | `int heightForWidth(int width) const` | 返回给定宽度下的推荐高度。 | 默认返回 `-1` 表示无宽高依赖；复杂计算应缓存结果。 |
| 可重写 | `void invalidate()` | 使尺寸、换行或 geometry 缓存失效。 | 输入尺寸依据改变后调用；它不保证同步完成重新布局。 |
| 必须实现 | `bool isEmpty() const` | 报告该项在布局语义上是否为空。 | 隐藏 widget 和 spacer 可能返回 `true`；不能据此决定是否删除对象。 |
| 类型识别 | `QLayout *layout()` | 若该项本身是子布局，返回该布局；否则返回 `nullptr`。 | 用于递归遍历和清空嵌套布局，是安全类型识别接口。 |
| 必须实现 | `QSize maximumSize() const` | 返回项目允许的最大尺寸。 | 与 `minimumSize()`、`sizeHint()` 保持一致，避免布局出现互相矛盾的约束。 |
| 可重写 | `int minimumHeightForWidth(int width) const` | 返回给定宽度下项目可接受的最小高度。 | 默认调用 `heightForWidth(width)`；宽度影响换行时应按实际最小需求重写。 |
| 必须实现 | `QSize minimumSize() const` | 返回项目允许的最小尺寸。 | 布局压缩空间时依赖它；应包含内容不可再压缩的边界。 |
| 设置 | `void setAlignment(Qt::Alignment alignment)` | 设置项目在布局单元格内的对齐方式。 | `QSpacerItem` 没有可见对齐效果；业务代码通常通过 layout 的高层 API 设置。 |
| 必须实现 | `void setGeometry(const QRect &r)` | 接收父布局分配的矩形并应用到项目。 | 对 widget item 会影响 QWidget；受布局管理的控件不要在外部反复手动改 geometry。 |
| 必须实现 | `QSize sizeHint() const` | 返回项目推荐尺寸。 | 是布局协商参考值，不是固定大小；可大于最小尺寸且小于最大尺寸。 |
| 类型识别 | `QSpacerItem *spacerItem()` | 若该项是 spacer，返回该对象；否则返回 `nullptr`。 | 用于识别和调整空白项；它不会返回控件或子布局。 |
| 类型识别 | `QWidget *widget() const` | 若项目管理一个 QWidget，返回该控件；否则返回 `nullptr`。 | QWidget 并不继承 QLayoutItem；这是取得关联对象，不是基类向下转型。 |

## 13. 下一步应该读什么

理解 `QLayoutItem` 后，建议继续看：

1. `QWidgetItem`：控件如何把自身的 `QSizePolicy`、size hint 和隐藏状态交给布局；
2. `QSpacerItem`：不可见空白如何参与伸缩和尺寸协商；
3. `QSizePolicy`：控件为何愿意扩展、收缩或保持大小；
4. `QLayout`：布局如何保存、遍历、取走并分配这些项目；
5. `QBoxLayout`：这些抽象信息如何在一条主轴上转化为实际排列。

### 一句话总结

`QLayoutItem` 是布局算法的统一语言：无论一项是控件、子布局还是空白，它都通过尺寸、扩展方向、对齐、geometry 和类型识别接口参与布局。普通项目通过具体布局类间接使用它；动态遍历、调试布局和编写自定义布局时，才需要直接理解它的契约。
