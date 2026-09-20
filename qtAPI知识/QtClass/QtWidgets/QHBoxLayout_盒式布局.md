# Qt QHBoxLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QHBoxLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QBoxLayout`  
> 定位：固定从左到右排列的盒式布局便捷类

## 1. QHBoxLayout 解决什么问题

`QHBoxLayout` 把控件、子布局和空白项按**从左到右**的顺序排成一行。它等价于方向固定为 `QBoxLayout::LeftToRight` 的 `QBoxLayout`。

它适合表达天然属于“一行”的界面结构：

```text
文件路径： [________________________] [浏览...]

[状态文字]                         [取消] [确定]

[上一页] [下一页] [刷新]
```

选择 `QHBoxLayout` 的意义不只是少写一个方向枚举，更重要的是把界面意图写进类型：读到它就知道这一层布局的主轴是水平的，stretch 只分配额外宽度。

## 2. 最小可用示例

```cpp
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QWidget>

class PathRow final : public QWidget
{
public:
    PathRow()
    {
        auto *layout = new QHBoxLayout(this);
        layout->addWidget(new QLabel("文件："));
        layout->addWidget(new QLineEdit, 1);
        layout->addWidget(new QPushButton("浏览..."));
    }
};
```

这里输入框的 stretch 是 `1`，因此在窗口变宽时优先吸收额外**宽度**。按钮的横向大小仍会受它的 `QSizePolicy`、最小尺寸和最大尺寸限制。

## 3. 两种构造方式

### 3.1 作为 QWidget 的顶层布局

```cpp
auto *layout = new QHBoxLayout(parentWidget);
```

传入 `parentWidget` 后，布局立即成为它的顶层布局。布局中的控件会被重设为该控件的子对象。

一个 QWidget 只能有一个顶层布局：

```cpp
auto *main = new QVBoxLayout(window);
auto *row = new QHBoxLayout;
main->addLayout(row);
```

复杂界面应把 `QHBoxLayout` 作为子布局加入主布局，而不是给同一个 QWidget 设置第二个顶层布局。

### 3.2 先创建，再加入父布局

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QPushButton("取消"));
row->addWidget(new QPushButton("保存"));

parentLayout->addLayout(row);
```

无 parent 构造的 `QHBoxLayout` 是一个尚未接入界面的子布局。必须把它加入父布局，才能获得 geometry 并真正管理区域。

## 4. 最常见的水平布局模式

### 4.1 标签、字段、操作按钮

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QLabel("地址："));
row->addWidget(new QLineEdit, 1);
row->addWidget(new QPushButton("测试连接"));
```

适合表单中单行字段。若页面中有很多类似“标签-字段”对，整体更适合 `QFormLayout`；不要用大量独立 `QHBoxLayout` 手工模拟统一的标签列。

### 4.2 按钮靠右

```cpp
auto *buttons = new QHBoxLayout;
buttons->addStretch();
buttons->addWidget(new QPushButton("取消"));
buttons->addWidget(new QPushButton("确定"));
```

`addStretch()` 创建可伸缩空白，吸收按钮前面的额外宽度。不要用 `addSpacing(300)`，那会把窗口宽度假设写死。

### 4.3 两端分布

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QLabel("已连接"));
row->addStretch();
row->addWidget(new QPushButton("断开"));
```

这是状态信息在左、动作在右的常见结构。

## 5. 什么时候不该用 QHBoxLayout

| 需求 | 更合适的选择 | 原因 |
| --- | --- | --- |
| 上下堆叠区域 | `QVBoxLayout` | 主轴应该是高度，不是宽度 |
| 标签列需要对齐 | `QFormLayout` | 自动维护字段与标签列 |
| 二维行列或跨格 | `QGridLayout` | 不必嵌套很多水平行模拟表格 |
| 宽窄模式间需要横竖切换 | `QBoxLayout` | 可使用 `setDirection()` |
| 工具栏语义和 action 管理 | `QToolBar` | 提供溢出、拖拽、action 等工具栏能力 |

## 6. 从 QBoxLayout 继承的关键能力

`QHBoxLayout` 自己只声明构造与析构；实际添加控件、stretch、spacing、插入和动态删除能力来自 `QBoxLayout` 与 `QLayout`。

使用时最重要的继承 API：

```cpp
layout->addWidget(widget, stretch, alignment);
layout->addLayout(childLayout, stretch);
layout->addSpacing(12);
layout->addStretch(1);
layout->setSpacing(6);
layout->setContentsMargins(12, 8, 12, 8);
```

在 `QHBoxLayout` 中：

- stretch 只影响宽度；
- `addStrut(size)` 设置最小高度；
- `addStretch()` 把后续项目推向右侧；
- `Qt::AlignRight` 只控制项目在其单元格内的位置；
- `setContentsMargins()` 控制边缘留白，`setSpacing()` 控制相邻项间距。

完整签名与所有权、动态插入、`takeAt()`、尺寸协商规则见 `QBoxLayout` 和 `QLayout` 笔记；此处不重复复制。

## 7. 常见误区

### 7.1 以为 stretch 会让控件变高

在 QHBoxLayout 中，stretch 只沿水平方向分额外空间。需要纵向结构或高度 stretch 时，使用外层 `QVBoxLayout`。

### 7.2 用固定空白实现右对齐

```cpp
layout->addSpacing(240); // 不适应窗口大小
```

改为 `addStretch()`，让布局随窗口宽度自动变化。

### 7.3 多行表单全部用手工水平布局

单行字段可以使用 QHBoxLayout；多行表单应考虑 QFormLayout，避免标签列在不同窗口和翻译文本下错位。

### 7.4 把 QHBoxLayout 当作可以翻转方向的类

它固定使用从左到右方向。需要运行时切换到垂直排列时，创建 `QBoxLayout` 并调用 `setDirection()`。

## API 速查表
下表列出 QHBoxLayout 自己声明的 API。它继承的 `addWidget()`、`addStretch()`、`setSpacing()`、`takeAt()` 等 API 由 QBoxLayout/QLayout 提供。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QHBoxLayout()` | 创建一个尚未接入父控件的水平布局。 | 必须之后加入父布局，或通过 `QWidget::setLayout()` 安装到 QWidget。 |
| 构造函数 | `QHBoxLayout(QWidget *parent)` | 创建并直接设为 `parent` 顶层布局的水平布局。 | 一个 QWidget 只能有一个顶层布局；加入的控件会以 parent 为父对象。 |
| 析构函数 | `virtual ~QHBoxLayout()` | 销毁这个水平布局及其管理的布局项。 | 布局不会直接销毁关联 QWidget；控件通常由父 QWidget 的对象树管理。 |

## 9. 继续学习

1. `QBoxLayout`：理解完整的 stretch、spacing、动态插入与方向机制。
2. `QVBoxLayout`：理解同一组规则如何作用到垂直主轴。
3. `QFormLayout`：处理多行标签-字段结构。
4. `QSizePolicy`：理解控件为什么愿意或拒绝吸收额外宽度。

### 一句话总结

`QHBoxLayout` 是固定从左到右的 QBoxLayout 便捷类。它最适合字段行、按钮行和左右两端分布的操作区；用 stretch 管理额外宽度，用嵌套布局组织复杂页面，而不是靠固定坐标或固定空白凑位置。
