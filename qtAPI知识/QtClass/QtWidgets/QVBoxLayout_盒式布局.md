# Qt QVBoxLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QVBoxLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QBoxLayout`  
> 定位：固定从上到下排列的盒式布局便捷类

## 1. QVBoxLayout 解决什么问题

`QVBoxLayout` 把控件、子布局和空白项按**从上到下**的顺序堆叠。它等价于方向固定为 `QBoxLayout::TopToBottom` 的 `QBoxLayout`。

它是 Widgets 页面最常见的外层结构：

```text
设置页面
├─ 页面标题
├─ 说明文字
├─ 表单或内容区
├─ 可伸缩空白
└─ 按钮行
```

选择 `QVBoxLayout` 表达的是“这个界面的主要阅读和操作顺序是纵向的”。它的 stretch 只分配额外**高度**，这正适合让中间内容区域扩展、把操作按钮稳定地放在底部。

## 2. 最小可用示例

```cpp
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

class LoginWidget final : public QWidget
{
public:
    LoginWidget()
    {
        auto *main = new QVBoxLayout(this);
        main->addWidget(new QLabel("登录"));
        main->addWidget(new QLineEdit);
        main->addWidget(new QLineEdit);

        auto *buttons = new QHBoxLayout;
        buttons->addStretch();
        buttons->addWidget(new QPushButton("取消"));
        buttons->addWidget(new QPushButton("登录"));
        main->addLayout(buttons);
    }
};
```

外层 `QVBoxLayout` 管理页面区块，内层 `QHBoxLayout` 管理一行按钮。这种“外层纵向、局部横向”的组合比在一个布局中硬塞所有规则更容易维护。

## 3. 两种构造方式

### 3.1 直接成为 QWidget 的顶层布局

```cpp
auto *layout = new QVBoxLayout(parentWidget);
```

该布局会立刻成为 `parentWidget` 的顶层布局。一个 QWidget 只能有一个顶层布局，加入布局的控件会以该 QWidget 为父对象。

### 3.2 创建子布局后再嵌套

```cpp
auto *section = new QVBoxLayout;
section->addWidget(new QLabel("高级选项"));
section->addWidget(new QCheckBox("启用缓存"));

mainLayout->addLayout(section);
```

无 parent 构造的 QVBoxLayout 是子布局，必须加入父布局后才能获得实际 geometry。它适合分组、页面分区和可复用的局部结构。

## 4. 常见页面结构

### 4.1 标题、内容、底部操作

```cpp
auto *main = new QVBoxLayout;
main->addWidget(title);
main->addWidget(description);
main->addWidget(content, 1);
main->addLayout(buttonRow);
```

`content` 的 stretch 为 `1`，在垂直方向优先吸收多余高度。标题、说明与按钮行通常保持接近其 size hint 的高度。

### 4.2 把底部按钮固定在底部

```cpp
auto *main = new QVBoxLayout;
main->addWidget(content);
main->addStretch();
main->addLayout(buttonRow);
```

中间的可伸缩空白吞掉额外高度，因此 `buttonRow` 会停在底部。不要用固定 `addSpacing(400)`，窗口高度变化时会立刻失效。

### 4.3 多个可扩展区域

```cpp
main->addWidget(editor, 3);
main->addWidget(preview, 2);
```

窗口增高后，编辑区和预览区按 `3 : 2` 分配额外高度。stretch 只分配剩余空间，仍受最小/最大尺寸与 `QSizePolicy` 限制。

## 5. 垂直主轴带来的实际差异

继承的 `QBoxLayout` API 在 QVBoxLayout 中仍然可用，但意义随主轴改变：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 主轴伸缩 | `addWidget(widget, stretch)` | 把控件加入垂直布局，并用 stretch 参与额外高度分配 | 在 QVBoxLayout 中 stretch 主要影响高度；控件变宽仍取决于横向 size policy |
| 弹性空白 | `addStretch()` | 加入可伸缩空白，把后续项目推向底部或分隔区域 | 它吃掉的是垂直剩余空间；与固定 `addSpacing()` 不同 |
| 垂直主轴外的约束 | `addStrut(size)` | 提高垂直布局在水平方向上的最小宽度 | 不添加可见控件；用于保证一列内容不要被压得太窄 |
| 对齐 | `Qt::AlignBottom` | 让项目在分配到的单元格内靠下 | 对齐只决定放置位置，不改变项目获得多少空间 |
| 项间距 | `setSpacing()` | 设置上下相邻项目之间的间距 | 未显式设置时可能来自 style 或父布局，不同平台默认值不一定相同 |

最容易犯的错误是沿用水平布局的直觉，以为 `addWidget(editor, 1)` 会让编辑器变宽。它在 QVBoxLayout 中优先分配的是高度；控件变宽仍取决于 QWidget 自身的 size policy 和布局可用宽度。

## 6. 什么时候要配合 QScrollArea

纵向页面内容很多时，QVBoxLayout 本身不会自动产生滚动条。若最小内容高度可能超过窗口高度，应把内容容器放进 `QScrollArea`：

```cpp
auto *content = new QWidget;
auto *layout = new QVBoxLayout(content);
layout->addWidget(...);

scrollArea->setWidget(content);
scrollArea->setWidgetResizable(true);
```

不要靠把每一项强行压小来适应有限高度。需要完整浏览的表单、偏好设置和详情页通常更适合滚动区域。

## 7. 什么时候不该用 QVBoxLayout

| 需求 | 更合适的选择 | 原因 |
| --- | --- | --- |
| 一行字段或按钮 | `QHBoxLayout` | 主要空间分配应发生在宽度 |
| 标签-字段多行表单 | `QFormLayout` | 自动处理两列对齐 |
| 复杂二维行列 | `QGridLayout` | 不必用多层纵横嵌套模拟网格 |
| 宽窄模式横竖切换 | `QBoxLayout` | 可在运行时 `setDirection()` |
| 同时只显示一个页面 | `QStackedLayout` | 页面切换比 hide/show 更清晰 |

## 8. 常见误区

### 8.1 以为 stretch 会让项目更宽

QVBoxLayout 的 stretch 只分配额外高度。宽度由父布局可用宽度、margin、项目最小/最大宽度和 QSizePolicy 协商。

### 8.2 用固定空白把按钮推到底部

```cpp
main->addSpacing(500);
```

这依赖窗口高度。应使用 `main->addStretch()`。

### 8.3 内容太多却没有滚动区域

窗口高度不够时，控件会被压缩或窗口最小尺寸变大。需要浏览的长页面应使用 QScrollArea。

### 8.4 给同一个 QWidget 设置多个纵向布局

一个 QWidget 只能有一个顶层布局。用嵌套 QVBoxLayout/QHBoxLayout 组织分区。

## API 速查表
下表列出 QVBoxLayout 自己声明的 API。`addWidget()`、`addStretch()`、`setSpacing()`、`takeAt()` 等能力来自 QBoxLayout/QLayout，应结合对应笔记阅读。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QVBoxLayout()` | 创建一个尚未接入父控件的纵向布局。 | 必须之后加入父布局，或通过 `QWidget::setLayout()` 安装到 QWidget。 |
| 构造函数 | `QVBoxLayout(QWidget *parent)` | 创建并直接设为 `parent` 顶层布局的纵向布局。 | 一个 QWidget 只能有一个顶层布局；加入的控件会以 parent 为父对象。 |
| 析构函数 | `virtual ~QVBoxLayout()` | 销毁这个纵向布局及其管理的布局项。 | 布局不会直接销毁关联 QWidget；控件通常由父 QWidget 的对象树管理。 |

## 10. 继续学习

1. `QBoxLayout`：理解完整的 stretch、spacing、动态插入与方向机制。
2. `QSizePolicy`：理解控件为什么愿意或拒绝吸收额外高度。
3. `QFormLayout`：构建标签-字段表单。
4. `QScrollArea`：容纳高度超出窗口的纵向内容。

### 一句话总结

`QVBoxLayout` 是固定从上到下的 QBoxLayout 便捷类，最适合作为页面和分区的外层结构。用垂直 stretch 让内容区扩展或把按钮行推到底部，用嵌套水平布局组织局部行，而不是用固定高度和手动坐标维持页面。
