# Qt QWidgetItem 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QWidgetItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QLayoutItem`  
> 定位：把 QWidget 的尺寸与 geometry 接入布局系统的适配项

## 1. QWidgetItem 解决什么问题

布局最终要摆放的是 `QWidget`，但布局算法不能只知道“这是一个按钮”或“这是一个输入框”。它还需要询问：

- 这个控件推荐多大？
- 最小和最大能多大？
- 多出来的空间它愿不愿意用？
- 它隐藏后是否还应占据布局空间？
- 宽度变小时，高度是否需要变化？
- 布局分配出一个矩形后，怎样应用到控件？

`QWidgetItem` 把这些 QWidget 相关信息翻译为 `QLayoutItem` 的统一接口。

```text
QPushButton / QLineEdit / QLabel / 自定义 QWidget
                    |
                    v
              QWidgetItem
                    |
                    v
         QLayout 的尺寸协商与 geometry 分配
```

它解决的是“让任意 QWidget 能以统一方式参与布局”，而不是创建一种新的可见控件。

## 2. 日常代码通常不会手动创建它

正常情况下写：

```cpp
auto *layout = new QVBoxLayout(&window);
layout->addWidget(new QLineEdit);
```

`addWidget()` 会为控件创建合适的 `QWidgetItem` 并交给布局管理。业务代码不需要保存该 item。

需要拿到它时，从布局查询：

```cpp
QLayoutItem *item = layout->itemAt(0);
QWidget *widget = item ? item->widget() : nullptr;
```

不要把 `QWidgetItem` 当作普通控件来调用 `show()`、`setText()` 或连接信号；这些操作应该对它包装的 `QWidget` 进行。

## 3. 什么时候需要直接接触 QWidgetItem

### 3.1 检查或遍历布局中的控件

```cpp
for (int i = 0; i < layout->count(); ++i) {
    QLayoutItem *item = layout->itemAt(i);
    if (QWidget *widget = item->widget()) {
        qDebug() << widget->objectName()
                 << widget->sizeHint()
                 << item->geometry();
    }
}
```

这适合动态表单、插件区域、可配置设置页。遍历时不要假设每一项都是 `QWidgetItem`，还可能遇到子布局或 spacer。

### 3.2 实现自定义 QLayout

自定义布局接受的是 `QLayoutItem *`：

```cpp
void MyLayout::addItem(QLayoutItem *item)
{
    items_.append(item);
}
```

当调用方把 QWidget 加入自定义布局时，通常应通过 `QLayout::addWidget()` 让 Qt 创建 `QWidgetItem`，或者按照 `QLayout` 的子控件管理规则正确接入控件。自定义布局内部只需按 `QLayoutItem` 接口测量和摆放，不需要针对 QPushButton、QLabel、QLineEdit 分别写算法。

### 3.3 排查隐藏控件留下空白

`QWidgetItem::isEmpty()` 在关联控件隐藏时返回 `true`。因此：

```cpp
widget->hide();
```

通常足以让布局在下一次计算时把空间让给其它可见项目。若空白没有消失，应检查：

- 是否隐藏的是实际被布局管理的控件；
- 控件是否位于更深层子布局；
- 是否还有 spacer 或固定行/列约束；
- 是否需要让父布局重新计算。

## 4. 它如何把 QWidget 的信息交给布局

### 4.1 尺寸信息

`QWidgetItem` 的 `sizeHint()`、`minimumSize()`、`maximumSize()` 不应被理解为独立于控件存在的另一套尺寸。它们基于关联 QWidget 的尺寸能力，并结合 `QSizePolicy` 转化为布局可以使用的数据。

```text
QWidget 的文字、图标、字体、最小/最大尺寸、QSizePolicy
                         |
                         v
                  QWidgetItem 的尺寸报告
                         |
                         v
                    QLayout 分配空间
```

因此，遇到“输入框不肯变宽”“标签被压缩”“按钮异常大”时，优先检查控件本身：

```cpp
widget->setMinimumWidth(120);
widget->setMaximumWidth(QWIDGETSIZE_MAX);
widget->setSizePolicy(
    QSizePolicy::Expanding,
    QSizePolicy::Fixed);
```

不要试图通过直接操作 `QWidgetItem` 修正业务控件尺寸。`QWidgetItem` 是适配层，尺寸策略的真正来源通常是 QWidget。

### 4.2 扩展方向与 `QSizePolicy`

```cpp
Qt::Orientations directions = item->expandingDirections();
```

该函数报告控件是否愿意使用超过 `sizeHint()` 的额外宽度或高度。结果主要由控件的 `QSizePolicy` 决定。

它与布局 stretch 的职责不同：

- `QSizePolicy` 告诉布局“我能否变大”；
- stretch 告诉布局“多个可变大项目如何按比例分额外空间”。

例如两个 `QLineEdit` 都允许水平扩展，`QHBoxLayout` 里给它们 stretch `1` 和 `2`，第二个输入框才会优先拿到更多剩余宽度。

### 4.3 控件类型信息

```cpp
QSizePolicy::ControlTypes types = item->controlTypes();
```

`QWidgetItem::controlTypes()` 返回关联控件的 control type。Qt style 和布局系统可利用这类信息做更符合控件语义的间距与尺寸处理。

业务代码通常不必自行判断这个值；在自定义布局、style 或调试尺寸问题时才有价值。

## 5. geometry：布局和控件之间的最后一步

布局完成计算后，会把矩形交给 item：

```cpp
item->setGeometry(QRect(16, 40, 280, 32));
```

`QWidgetItem::setGeometry()` 会把布局结果应用到它包装的 QWidget。之后：

```cpp
QRect actual = item->geometry();
```

可以取得该 item 当前覆盖的区域。

这也是为什么不要在控件已经被布局管理后，持续手动调用：

```cpp
widget->move(...);
widget->resize(...);
widget->setGeometry(...);
```

手动结果会在下一次布局更新时被 item 的 `setGeometry()` 覆盖。应改用布局、margin、spacing、stretch、alignment、最小/最大尺寸和 size policy 表达需求。

## 6. 隐藏与 `isEmpty()` 的真正含义

对 `QWidgetItem` 来说：

```cpp
item->isEmpty()
```

在关联 QWidget 被隐藏时返回 `true`。

这带来两个重要结论：

1. `hide()` 不会删除 QWidget；控件对象仍可 `show()` 恢复。
2. 布局可以把隐藏控件视为暂时没有可见内容，从而把空间重新分配给其它项。

这很适合“高级选项展开/收起”“根据复选框显示附加字段”“无权限时临时隐藏操作区”等场景。

但 `isEmpty()` 只是布局语义，不是生命周期语义。它返回 `true` 不表示控件可以安全删除，也不表示它已从布局中移除。

## 7. 宽度影响高度：把 QWidget 的能力传递给布局

自动换行标签的高度会随着可用宽度改变：

```cpp
auto *label = new QLabel(longText);
label->setWordWrap(true);
layout->addWidget(label);
```

`QWidgetItem` 会通过以下接口把 QWidget 的宽高依赖传递给布局：

```cpp
if (item->hasHeightForWidth()) {
    const int h = item->heightForWidth(240);
}
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 宽高依赖 | `hasHeightForWidth()` | 查询被包装控件是否声明“宽度会影响推荐高度” | 常见于自动换行文本；结果来自控件自身实现和 size policy |
| 宽高依赖 | `heightForWidth(int w)` | 返回被包装控件在给定宽度下建议使用的高度 | 布局用它给换行控件分配高度；自定义 QWidget 要配套实现相关 size hint |
| 尺寸建议 | `sizeHint()` | 返回被包装控件在普通情况下的推荐尺寸 | 没有特定宽度限制时使用；实际尺寸仍由父布局和控件策略共同决定 |

当窗口变窄时，上层布局据此增加自动换行标签的高度。若自己写自定义 QWidget，应正确提供 `sizeHint()`、`minimumSizeHint()`、`hasHeightForWidth()` 和 `heightForWidth()`，布局才能获得可靠信息。

## 8. QWidgetItem 的所有权边界

`QWidgetItem` 是一个包装项；它不是关联 QWidget 的 QObject 父对象。

在常规用法中：

```cpp
layout->addWidget(widget);
```

布局管理 item，控件通常由放置该布局的父 QWidget 的对象树管理。动态移除时：

```cpp
layout->removeWidget(widget); // 控件仍然存在
widget->deleteLater();        // 业务决定永久删除时才调用
```

如果使用：

```cpp
QLayoutItem *item = layout->takeAt(index);
```

调用方接管的是 item 本身。关联控件是否删除、迁移或保留，仍取决于业务意图和 QWidget 的父对象关系。

```cpp
if (QLayoutItem *item = layout->takeAt(index)) {
    if (QWidget *widget = item->widget()) {
        widget->setParent(targetPage);
        targetLayout->addWidget(widget);
    }
    delete item;
}
```

这段代码展示的是控件迁移：删除旧 `QWidgetItem` 包装项，但保留 QWidget 并加入新布局。

## 9. 常见误区

### 9.1 手动 new QWidgetItem 再调用 `addWidget()`

`addWidget()` 已经会创建并管理 item。不要为同一个控件同时手动创建包装项，否则容易造成重复管理或所有权混乱。

### 9.2 把 `item->widget()` 当成永远非空

布局项可能是子布局或 spacer。调用前必须判空。

### 9.3 隐藏控件后以为它被删除了

隐藏只是使 `QWidgetItem` 在布局中呈现 empty 状态；对象和布局关系都还在。

### 9.4 改 QWidget 的 geometry 对抗布局

下一次 layout pass 会把结果覆盖。修改尺寸策略或布局规则才是稳定做法。

### 9.5 以为 QWidgetItem 接管 QWidget 生命周期

控件的生命周期主要由 QWidget 父子对象关系管理。处理 `takeAt()` 返回项时，要分别决定 wrapper 和 widget 的去向。

## API 速查表
下表覆盖 `QWidgetItem` 自己声明和重写的 API；`QLayoutItem` 的其它通用接口请结合其笔记阅读。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QWidgetItem(QWidget *widget)` | 创建一个包装给定 QWidget 的布局项。 | 日常代码通常由 `QLayout::addWidget()` 自动创建；手动创建主要服务自定义布局。 |
| 析构函数 | `virtual ~QWidgetItem()` | 销毁控件包装项。 | 不应把它当作 QWidget 的父对象；控件生命周期仍按 QWidget 对象树和业务逻辑处理。 |
| 重写 | `QSizePolicy::ControlTypes controlTypes() const` | 返回关联控件的 control type。 | style 与布局协商可据此处理控件语义；业务代码很少直接使用。 |
| 重写 | `Qt::Orientations expandingDirections() const` | 返回控件愿意吸收额外空间的方向。 | 主要由 QWidget 的 `QSizePolicy` 决定；不是 stretch 权重。 |
| 重写 | `QRect geometry() const` | 返回 item 当前覆盖的布局矩形。 | 调试最终布局结果时使用；受下一次布局更新影响。 |
| 重写 | `bool hasHeightForWidth() const` | 返回控件推荐高度是否依赖宽度。 | 自动换行标签和自适应文本控件常见；布局会据此协商高度。 |
| 重写 | `int heightForWidth(int w) const` | 返回给定宽度 `w` 下控件的推荐高度。 | 与 `hasHeightForWidth()` 配合；通常由关联 QWidget 的实现提供。 |
| 重写 | `bool isEmpty() const` | 关联 QWidget 隐藏时返回 `true`。 | 隐藏控件会暂时让出布局空间；不表示对象已删除。 |
| 重写 | `QSize maximumSize() const` | 返回控件在布局中允许的最大尺寸。 | 排查控件为何不再变大时，检查 QWidget 最大尺寸和 size policy。 |
| 重写 | `QSize minimumSize() const` | 返回控件在布局中允许的最小尺寸。 | 防止控件被压得过小；来源受 QWidget 最小尺寸、hint 和策略影响。 |
| 重写 | `void setGeometry(const QRect &rect)` | 把布局计算的矩形应用到关联 QWidget。 | 由布局系统调用；不要在外部与布局反复争夺控件 geometry。 |
| 重写 | `QSize sizeHint() const` | 返回控件在布局中的推荐尺寸。 | 文字、图标、字体与 QWidget 的 `sizeHint()` 会影响结果；不是固定尺寸。 |
| 类型识别 | `QWidget *widget() const` | 返回该 item 包装的 QWidget。 | 遍历布局项时先判空；子布局和 spacer 会返回 `nullptr`。 |

## 11. 继续学习

读完这一篇后，推荐按下面顺序理解整个链路：

1. `QSizePolicy`：控件如何声明扩展、收缩和控件类型；
2. `QWidget`：控件自身怎样提供 size hint、最小/最大尺寸与宽高依赖；
3. `QLayoutItem`：布局怎样统一处理 widget、layout 和 spacer；
4. `QLayout`：布局怎样管理项目、尺寸约束和更新；
5. `QBoxLayout`：这些信息如何在一条主轴中转化为 stretch 和最终排列。

### 一句话总结

`QWidgetItem` 是 QWidget 与布局算法之间的适配层：它把控件的尺寸策略、隐藏状态、宽高依赖和 geometry 接入 `QLayoutItem` 契约。普通代码通过 `addWidget()` 间接使用它；动态遍历、迁移控件和实现自定义布局时，理解它能避免绝大多数布局与所有权误区。
