# QHBoxLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QHBoxLayout`

## 1. 先建立直觉

### 这是什么

`QHBoxLayout` 是方向固定为水平的 `QBoxLayout`。它把控件和子布局按一行排列，默认从左到右追加项目，并用 `QBoxLayout` 的边距、间距、stretch 和 alignment 规则分配宽度。

它不是一个“简单容器”的廉价别名，而是 Widgets 界面里最常用的基础积木：表单中的“标签 + 输入框”、对话框底部按钮行、工具按钮组、左右分栏的外层结构，通常都从它开始。

### 适合使用的场景

- 一行命令按钮，例如“取消 / 应用 / 确定”。
- 标签、输入框和操作按钮处在同一行。
- 左右两块区域按比例占宽度，例如导航栏和内容区。
- 在 `QVBoxLayout` 中嵌套一行局部控件。

### 不适合的场景

- 多行多列对齐应使用 `QGridLayout` 或 `QFormLayout`。
- 需要纵向堆叠页面区块时应使用 `QVBoxLayout`。
- 需要运行时切换水平/垂直方向时，直接使用 `QBoxLayout` 更自然。

### 最小示例

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QLabel(tr("Path:")), 0);
row->addWidget(pathEdit, 1);
row->addWidget(browseButton, 0);
```

这里输入框拿到正 stretch，所以窗口变宽时它会吸收主要宽度；标签和按钮保持接近自己的推荐宽度。

## 2. 依赖与对象关系

- 头文件：`#include <QHBoxLayout>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QBoxLayout`
- 直接派生类：类页未列出

`QHBoxLayout` 的公开 API 很少，因为它把绝大多数能力继承自 `QBoxLayout`：`addWidget()`、`addLayout()`、`addStretch()`、`setStretch()`、`insertWidget()`、`setSpacing()`、`setContentsMargins()` 等都来自父类。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QHBoxLayout()` | 创建未安装到控件上的水平布局，之后应加入父布局或设置给控件。 |
| `QHBoxLayout(QWidget *parent)` | 创建水平布局并直接安装为 `parent` 的顶层布局。 |
| `~QHBoxLayout()` | 销毁布局对象；被布局管理的控件对象不因这个析构自动按业务语义删除。 |

## 4. API 逐项说明

### `QHBoxLayout::QHBoxLayout()`

创建一个独立的水平布局。它还没有父控件，常用于作为子布局加入另一个布局：

```cpp
auto *buttons = new QHBoxLayout;
buttons->addStretch(1);
buttons->addWidget(cancelButton);
buttons->addWidget(okButton);
rootLayout->addLayout(buttons);
```

这种写法适合在垂直页面中嵌入一行局部操作。加入父布局后，所有权由父布局管理。

### `QHBoxLayout::QHBoxLayout(QWidget *parent)`

创建水平布局并安装到 `parent`。一个 `QWidget` 只能有一个顶层布局，所以这个构造函数通常用于新建页面或面板时的第一层布局。

如果 `parent` 已经有布局，应该取得现有布局并向里面添加内容，而不是再构造一个新的顶层 `QHBoxLayout(parent)`。

### `~QHBoxLayout()`

销毁布局对象。它会清理布局项，但从业务角度看，控件生命周期仍应由 Qt 父子对象树和你的对象持有策略共同决定。

动态拆界面时，不要把“析构布局”当成“所有控件都妥善删除”。如果要删除控件，明确调用 `deleteLater()` 或让合适的父对象销毁它们。

## 5. 深入实践与常见坑

### 水平方向的 stretch 控制宽度

在 `QHBoxLayout` 里，stretch 主要分配额外宽度。常见的 `label + edit + button` 中，只给 edit stretch，通常就是最符合用户预期的行为。

### 按钮靠右用 stretch，不用固定空白

对话框底部按钮行通常这样写：

```cpp
buttons->addStretch(1);
buttons->addWidget(cancelButton);
buttons->addWidget(okButton);
```

这比 `addSpacing(200)` 更稳定，因为窗口变宽、翻译文本变长、高 DPI 缩放时仍然能工作。

### 一行内容太多时要重新分层

如果一行里塞了很多控件，只靠 spacing 调整会越来越脆。把相关控件拆成多个子布局，或改用网格/表单布局，维护成本会低很多。
