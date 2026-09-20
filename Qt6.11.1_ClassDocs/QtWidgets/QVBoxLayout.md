# QVBoxLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QVBoxLayout`

## 1. 先建立直觉

### 这是什么

`QVBoxLayout` 是方向固定为垂直的 `QBoxLayout`。它把控件和子布局从上到下堆叠，用父类的边距、间距、stretch 和 alignment 规则分配高度。

它最适合表达“页面结构”：顶部标题、中间内容、底部按钮区；或者一组设置项从上到下排列。多数复杂 Widgets 页面都是 `QVBoxLayout` 外层再嵌套若干 `QHBoxLayout` 或 `QFormLayout`。

### 适合使用的场景

- 对话框内容从上到下组织：说明文本、输入区、按钮区。
- 主窗口中央区域分成顶部工具区、中间编辑区、底部状态区。
- 设置页、属性页、分组控件中的纵向堆叠。
- 需要让某个主体控件吸收多余高度，例如文本编辑器、列表、表格。

### 不适合的场景

- 一行字段排列用 `QHBoxLayout`。
- 标签和值成对排列用 `QFormLayout`。
- 精确二维网格用 `QGridLayout`。
- 只想覆盖同一区域显示不同页面时，用 `QStackedLayout` 或 `QStackedWidget`。

### 最小示例

```cpp
auto *page = new QVBoxLayout(parent);
page->addWidget(titleLabel, 0);
page->addWidget(editor, 1);
page->addLayout(buttonRow, 0);
```

这里 `editor` 获得正 stretch，所以窗口变高时它会优先扩展；标题和按钮行维持接近推荐高度。

## 2. 依赖与对象关系

- 头文件：`#include <QVBoxLayout>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QBoxLayout`
- 直接派生类：类页未列出

`QVBoxLayout` 的排列方向固定为从上到下。其他操作几乎都来自 `QBoxLayout`：添加控件、添加子布局、插入空白、设置 stretch、设置 spacing、设置边距、动态取出项目。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QVBoxLayout()` | 创建未安装的垂直布局，之后应加入父布局或设置给控件。 |
| `QVBoxLayout(QWidget *parent)` | 创建垂直布局并直接安装为 `parent` 的顶层布局。 |
| `~QVBoxLayout()` | 销毁布局对象；控件对象的业务生命周期仍需单独考虑。 |

## 4. API 逐项说明

### `QVBoxLayout::QVBoxLayout()`

创建一个独立的垂直布局。它适合作为局部区块加入外层布局，例如一个右侧属性面板或一个 group box 内部内容。

```cpp
auto *section = new QVBoxLayout;
section->addWidget(header);
section->addWidget(details, 1);
outerLayout->addLayout(section, 1);
```

加入父布局后，父布局会管理它的所有权。

### `QVBoxLayout::QVBoxLayout(QWidget *parent)`

创建并安装为 `parent` 的顶层布局。新建页面控件时常用这个构造函数。

如果父控件已经有布局，不要再次用这个构造函数给它装第二个顶层布局；应复用 `parent->layout()` 或重新设计容器层级。

### `~QVBoxLayout()`

销毁布局对象。和其他布局一样，布局析构不是业务级“关闭页面”操作。动态页面切换时，应明确决定内部控件是保留、移动还是删除。

## 5. 深入实践与常见坑

### 垂直方向的 stretch 控制高度

在 `QVBoxLayout` 中，stretch 主要影响高度。让列表、表格、编辑器获得 `1`，让标题、说明、按钮区保持 `0`，通常能得到自然的页面结构。

### 外层控制大区块，内层控制行

不要把每一行的标签、输入框、按钮都直接塞进一个大 `QVBoxLayout`。更清晰的结构是：外层 `QVBoxLayout` 管页面上下关系，每一行用 `QHBoxLayout` 或 `QFormLayout` 管字段关系。

### 固定高度是最后手段

很多“页面不够好看”的问题，其实应该通过 stretch、spacing、contents margins、size policy 解决。固定高度会在字体变化、翻译变长、高 DPI 环境下变脆。
