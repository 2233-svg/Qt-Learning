# Qt QScrollArea 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QScrollArea>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QFrame -> QAbstractScrollArea -> QScrollArea`  
> 定位：在带滚动条的视口内显示一个内容 widget

## 1. QScrollArea 解决什么问题

`QScrollArea` 不是“给任意布局加两根滚动条”。它的模型是：一个带 frame 的滚动容器，内部有 viewport，viewport 中只承载**一个内容 widget**。

```text
QScrollArea
  ├─ frame
  ├─ viewport
  │    └─ content widget  <- setWidget() 设置的唯一内容
  ├─ horizontal QScrollBar
  └─ vertical QScrollBar
```

当内容 widget 的尺寸超过 viewport 时，`QScrollArea` 通过滚动条让用户看到其余区域。典型场景：

- 放大后的图片、PDF 页面预览、地图或自定义画布；
- 很长的设置页、动态增删字段的表单；
- 放满一列可展开卡片、日志条目或检查项的编辑面板。

若你要滚动的是大量同构数据，优先考虑 `QListView`、`QTableView`、`QTreeView` 等 model/view 控件；它们有虚拟化，不会像 `QScrollArea` 一样为每个项目都创建一个 QWidget。若只需给主窗口整体内容滚动，`QScrollArea` 很合适。

## 2. 先记住：只能放一个直接内容 widget

正确结构是先准备一个“内容根控件”，把许多子控件放进它的布局，再把这个根控件交给 scroll area：

```cpp
auto *content = new QWidget;
auto *contentLayout = new QVBoxLayout(content);
contentLayout->addWidget(new QLabel("第一项"));
contentLayout->addWidget(new QLineEdit);

auto *scrollArea = new QScrollArea;
scrollArea->setWidget(content);
```

不要连续调用：

```cpp
scrollArea->setWidget(new QLabel("A"));
scrollArea->setWidget(new QLabel("B"));
```

第二次调用会替换并销毁先前的内容 widget。多个项目必须先装进一个 root widget 的 layout。

## 3. 两种最常见的尺寸模型

### 3.1 内容尺寸主导：图片、画布、流程图

默认 `widgetResizable` 为 `false`。此时 scroll area 尊重内容 widget 自己的尺寸；内容大于 viewport 时出现滚动条。

```cpp
auto *imageLabel = new QLabel;
imageLabel->setPixmap(pixmap);
imageLabel->resize(pixmap.size());

auto *scrollArea = new QScrollArea;
scrollArea->setWidget(imageLabel);
scrollArea->setWidgetResizable(false);
```

这适合内容具有明确坐标系的情况。放大图片或画布时，调用内容 widget 的 `resize()`，scroll area 会自动更新滚动范围。

### 3.2 视口尺寸主导：设置页、属性编辑页

`widgetResizable` 设为 `true` 后，scroll area 会尽量把内容 widget 调整到 viewport 大小，以避免本可避免的滚动条并利用多余空间。内容的最小尺寸仍然会限制它，因此内容超过 viewport 后照样可以滚动。

```cpp
auto *content = new QWidget;
auto *form = new QFormLayout(content);
form->addRow("名称：", new QLineEdit);
form->addRow("说明：", new QPlainTextEdit);

auto *scrollArea = new QScrollArea;
scrollArea->setWidgetResizable(true);
scrollArea->setWidget(content);
```

这是长设置页最常用的模式：窗口变宽时，内容根控件跟随撑宽；字段越来越多、最小高度超过 viewport 时，纵向滚动条出现。

| `widgetResizable` | 内容尺寸来源 | 典型用途 |
| --- | --- | --- |
| `false`（默认） | 内容 widget 的 size、size hint 和显式 resize。 | 图片、画布、缩放预览。 |
| `true` | scroll area 尽量让内容 widget 填满 viewport，但受内容最小/最大约束限制。 | 表单、长页面、普通垂直内容。 |

## 4. 完整示例：可动态增加字段的滚动设置页

```cpp
#include <QApplication>
#include <QFormLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *outer = new QVBoxLayout(&window);

    auto *content = new QWidget;
    auto *form = new QFormLayout(content);
    form->setSizeConstraint(QLayout::SetMinAndMaxSize);
    form->addRow("服务地址：", new QLineEdit);
    form->addRow("访问令牌：", new QLineEdit);

    auto *scrollArea = new QScrollArea;
    scrollArea->setWidgetResizable(true);
    scrollArea->setWidget(content);

    auto *addButton = new QPushButton("添加字段");
    QObject::connect(addButton, &QPushButton::clicked, [form, scrollArea] {
        auto *field = new QLineEdit;
        form->addRow("自定义字段：", field);
        scrollArea->ensureWidgetVisible(field, 8, 8);
    });

    outer->addWidget(scrollArea, 1);
    outer->addWidget(addButton);

    window.resize(420, 260);
    window.show();
    return app.exec();
}
```

关键点不是 `addRow()`，而是 `form->setSizeConstraint(QLayout::SetMinAndMaxSize)`。内容布局动态增减时，该约束会让内容 widget 的尺寸范围更新，进而让 scroll area 重新计算滚动范围。没有合理的 `sizeHint()`、最小尺寸或 layout size constraint 时，常见现象是“控件已经添加，但滚动区高度不更新”。

## 5. setWidget() 的所有权和调用顺序

`setWidget()` 的规则非常严格：

1. 内容 widget 会成为 scroll area 的 child。
2. scroll area 销毁，或设置新的内容 widget 时，旧内容会被销毁。
3. 内容 widget 的 `autoFillBackground` 会被设为 `true`。
4. 内容 widget 的布局必须在调用 `setWidget()` **之前**装好。
5. 如果 scroll area 已经可见，之后再调用 `setWidget(content)`，还需要显式 `content->show()`。

因此应采用下面的顺序：

```cpp
auto *content = new QWidget;
auto *layout = new QVBoxLayout(content); // 先装 layout
layout->addWidget(new QLabel("内容"));

scrollArea->setWidget(content);          // 后交给 QScrollArea
```

不要先 `setWidget(content)`，之后才 `content->setLayout(...)`。Qt 文档明确说明这种顺序会导致内容不可见，之后再 `show()` 也不能补救。

需要更换或复用当前内容时，使用 `takeWidget()`：

```cpp
QWidget *oldContent = scrollArea->takeWidget();
// oldContent 的所有权已交还给调用者
oldContent->setParent(nullptr); // 仅在希望完全脱离原对象树时需要
```

`takeWidget()` 不会 delete 内容；调用者必须把它加入新容器、重新设置 parent，或在适当时机删除。

## 6. 对齐：内容比 viewport 小时放在哪里

当内容 widget 比 viewport 小，且没有被 `widgetResizable` 撑满时，`alignment` 决定它停在何处。默认是左上角：

```cpp
scrollArea->setAlignment(Qt::AlignHCenter | Qt::AlignTop);
```

可用标志包括：

- 水平：`Qt::AlignLeft`、`Qt::AlignHCenter`、`Qt::AlignRight`；
- 垂直：`Qt::AlignTop`、`Qt::AlignVCenter`、`Qt::AlignBottom`。

图片预览常使用水平、垂直居中；长表单通常保持左上角，以避免内容随着窗口增高而浮在中间。若 `widgetResizable=true` 且内容已填满 viewport，alignment 基本不会产生可见差异。

## 7. 把某个位置或控件滚动到可见区域

```cpp
scrollArea->ensureVisible(420, 760, 16, 16);
scrollArea->ensureWidgetVisible(errorField, 12, 12);
```

- `ensureVisible(x, y, xmargin, ymargin)`：将内容坐标系中的点尽量滚入 viewport，四周预留像素 margin；无法精确到达时滚到最近有效位置。
- `ensureWidgetVisible(childWidget, xmargin, ymargin)`：将内容根 widget 的某个**子控件**滚入 viewport。

典型用途是校验失败后跳到第一个错误字段、搜索命中后定位到匹配条目、或新增动态字段后保证它可见。`ensureWidgetVisible()` 的参数必须是 `scrollArea->widget()` 的后代控件；把不相关窗口中的 widget 传进去没有意义。

## 8. 滚动条由 QAbstractScrollArea 提供

`QScrollArea` 继承自 `QAbstractScrollArea`，所以滚动条策略和滚动条对象来自基类：

```cpp
scrollArea->setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
scrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

scrollArea->verticalScrollBar()->setValue(
    scrollArea->verticalScrollBar()->maximum());
```

常用规则：

- `Qt::ScrollBarAsNeeded`：内容需要时显示，通常是默认且合理的选择。
- `Qt::ScrollBarAlwaysOff`：禁止某个方向滚动条；只有确信内容不会溢出时使用。
- `verticalScrollBar()` / `horizontalScrollBar()` 可访问实际 `QScrollBar`，用于“滚到最底部”或保存/恢复滚动位置。

要在内容前后留固定的标题、标尺或自定义滚动条附属控件时，继续阅读 `QAbstractScrollArea` 的 `setViewportMargins()`、`addScrollBarWidget()` 和 `setCornerWidget()`；不要试图把这些区域塞进 `setWidget()` 的内容根中来冒充 viewport 外的 UI。

## 9. 自定义子类时的重实现点

普通使用不需要重实现这些函数；它们属于 scroll area 的内部事件和几何路径：

- `event()`：处理通用事件；
- `eventFilter()`：观察内容 widget 或内部对象事件；
- `focusNextPrevChild()`：调整 Tab / Shift+Tab 焦点移动；
- `resizeEvent()`：viewport 尺寸改变时重新安排内容；
- `scrollContentsBy()`：滚动条值变化时移动内容；
- `viewportSizeHint()`：向父布局建议 viewport 尺寸；
- `sizeHint()`：向父布局建议整个 scroll area 的尺寸。

如果你实现的是高性能无限画布、缩略图视图或自行绘制的滚动区域，通常应直接从 `QAbstractScrollArea` 继承；`QScrollArea` 更适合已有单个 QWidget 内容的场景。

## API 速查表
### 10.1 内容 widget、尺寸模型与对齐

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QScrollArea(QWidget *parent = nullptr)` | 创建空的滚动容器 | 之后用 `setWidget()` 指定唯一内容根控件 |
| 生命周期 | `~QScrollArea()` | 销毁 scroll area 及其内容 widget | 用 `setWidget()` 交出的内容由它负责销毁 |
| 内容 | `setWidget(QWidget *widget)` | 设置唯一内容 widget，并接管所有权 | 先为 widget 安装 layout；替换时旧内容会被销毁；scroll area 已可见时显式 `widget->show()` |
| 内容 | `widget() const` | 返回当前内容根控件 | 未设置内容时为 `nullptr` |
| 内容 | `takeWidget()` | 取出内容并把所有权交还调用者 | 不删除内容；随后必须重新安排 parent 或生命周期 |
| 尺寸模型 | `widgetResizable() const` | 查询是否由 viewport 自动调整内容尺寸 | 默认 `false` |
| 尺寸模型 | `setWidgetResizable(bool resizable)` | 设置内容尺寸主导或 viewport 尺寸主导模式 | 图片/画布常设 `false`；表单/长页常设 `true` |
| 对齐 | `alignment() const` | 读取小内容在大 viewport 中的停放对齐 | 内容填满 viewport 时效果不明显 |
| 对齐 | `setAlignment(Qt::Alignment alignment)` | 设置小内容的对齐 | 默认左上；图片预览常用居中 |

### 10.2 滚动定位与继承的滚动条控制

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 定位 | `ensureVisible(int x, int y, int xmargin = 50, int ymargin = 50)` | 让内容坐标中的点尽量可见 | `x`、`y` 使用内容 widget 坐标；默认四周 margin 为 50 px |
| 定位 | `ensureWidgetVisible(QWidget *childWidget, int xmargin = 50, int ymargin = 50)` | 让内容根中的某个子控件尽量可见 | 校验错误字段、动态新增字段、搜索命中定位；参数必须是内容 widget 的后代 |
| 滚动条 | `verticalScrollBar()`（继承） | 取得纵向 `QScrollBar` | 可读写 `value()`、`maximum()` 来恢复位置或滚到底部 |
| 滚动条 | `horizontalScrollBar()`（继承） | 取得横向 `QScrollBar` | 图片、宽画布或横向内容时使用 |
| 滚动条策略 | `setVerticalScrollBarPolicy(Qt::ScrollBarPolicy)`（继承） | 设置纵向滚动条显示策略 | 一般用 `ScrollBarAsNeeded` |
| 滚动条策略 | `setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy)`（继承） | 设置横向滚动条显示策略 | 宽度不可溢出时才考虑 `AlwaysOff` |
| 视口扩展 | `setViewportMargins(...)`（继承，保护函数） | 在 viewport 四周预留区域 | 自定义子类为固定标尺、标题栏等预留空间 |

### 10.3 事件与几何重实现接口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `event(QEvent *event)` | `QAbstractScrollArea::event()` 的保护重实现 | 自定义子类接入特殊事件处理时使用 |
| 事件 | `eventFilter(QObject *watched, QEvent *event)` | 过滤内部或内容对象事件 | 需要谨慎保留基类行为 |
| 焦点 | `focusNextPrevChild(bool next)` | 重实现 Tab / Shift+Tab 焦点导航 | 内容很长时确保焦点跳转符合滚动预期 |
| 几何 | `resizeEvent(QResizeEvent *event)` | viewport / 外框尺寸变化时处理几何更新 | 子类通常调用基类实现后补充逻辑 |
| 滚动 | `scrollContentsBy(int dx, int dy)` | 滚动发生时移动内容 | 自定义滚动效果或内容同步时使用 |
| 尺寸 | `viewportSizeHint() const` | 返回 viewport 推荐尺寸 | 影响父布局对滚动区的尺寸协商 |
| 尺寸 | `sizeHint() const` | 返回整个 scroll area 推荐尺寸 | 由外层布局用来确定初始大小 |
