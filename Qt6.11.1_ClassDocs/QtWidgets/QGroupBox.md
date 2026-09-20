# QGroupBox

> Qt 6.11.1 · Qt Widgets · 来自 `QGroupBox`

## 1. 先建立直觉

### 这是什么

`QGroupBox` 是带标题的分组容器。它把一组相关控件视觉上和语义上归在一起，还可以变成可勾选分组：勾选时启用内部内容，取消勾选时禁用内部内容。

它和 `QFrame` 的区别是：`QFrame` 只是边框或线；`QGroupBox` 表达“这一组控件属于同一个设置主题”。标题、助记符、可勾选状态都是它的重要语义。

### 适合使用的场景

- 设置页中分组相关选项。
- 表单中给一组选项加标题。
- 可选功能区：勾选启用高级设置、代理配置、自动保存等。
- 需要平台原生 group box 外观。

### 不适合的场景

- 只需要分隔线，用 `QFrame`。
- 只需要页面级容器，用普通 `QWidget` 加布局。
- 复杂折叠面板需要动画或展开收起行为时，可能要自定义控件。

## 2. 依赖与对象关系

- 头文件：`#include <QGroupBox>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

`QGroupBox` 本身不自动排列子控件。创建后通常要给它设置布局，再把相关控件加入该布局。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `title : QString` | 分组标题，可包含 `&` 助记符。 |
| `alignment : Qt::Alignment` | 标题水平对齐。 |
| `checkable : bool` | 标题是否带复选框。 |
| `checked : bool` | 可勾选分组当前是否启用内部内容。 |
| `flat : bool` | 是否使用更轻的边框样式。 |
| `QGroupBox(QWidget *parent)` | 创建无标题分组。 |
| `QGroupBox(const QString &title, QWidget *parent)` | 创建带标题分组。 |
| `setTitle()` / `title()` | 设置或读取标题。 |
| `setAlignment()` / `alignment()` | 设置或读取标题对齐。 |
| `setCheckable()` / `isCheckable()` | 设置或读取是否可勾选。 |
| `setChecked()` / `isChecked()` | 设置或读取勾选状态。 |
| `setFlat()` / `isFlat()` | 设置或读取平面样式。 |
| `clicked(bool)` | 用户点击标题复选框或助记符激活时发出。 |
| `toggled(bool)` | 勾选状态变化时发出。 |
| `minimumSizeHint()` | 根据标题、frame 和子控件返回最小建议尺寸。 |
| `initStyleOption(QStyleOptionGroupBox *)` | 为绘制准备 style option。 |
| 事件函数 | 处理标题点击、焦点、子对象、尺寸和绘制。 |

## 4. API 逐项说明

### `title`

分组标题。可用 `&` 设置助记符，例如 `"&Network"`。触发助记符时，焦点会移动到 group box 或内部焦点链。

标题应该描述内部控件共同主题，不要写成句子式说明。

### `alignment`

控制标题水平对齐，常见为左对齐、右对齐或居中。默认通常左对齐。

不要用它控制内部控件布局；内部控件对齐由 group box 的 layout 决定。

### `checkable`

开启后标题旁显示复选框。勾选表示内部设置启用；取消勾选时，子控件通常会被禁用。

这是表达“启用这一整组配置”的好方式，比如“使用代理服务器”下面跟主机和端口。

### `checked`

当前勾选状态。可勾选 group box 默认通常是 checked。取消勾选会禁用子控件，但 group box 自身仍可操作。

不建议在未勾选时单独启用某些子控件，否则用户会不明白这一组到底是否生效。

### `flat`

平面样式通常只画较轻的边框或顶部线，具体效果依赖平台 style。

密集设置页中 flat 可以降低视觉重量；重要分组则保持完整边框更清楚。

### 构造和析构

可以创建无标题或带标题分组。析构由父控件负责，内部子控件按 QObject 父子关系销毁。

创建后记得设置布局，否则子控件不会自动排版。

### `clicked(bool)` / `toggled(bool)`

`clicked()` 偏用户动作，调用 `setChecked()` 不会触发它；`toggled()` 表示状态变化，程序设置也可触发。

同步业务状态通常连 `toggled()`；只关心用户点击标题复选框时连 `clicked()`。

### `initStyleOption()` 和事件函数

`initStyleOption()` 填充标题、勾选、frame、状态等绘制信息。鼠标事件处理标题复选框点击，`childEvent()` 和 `resizeEvent()` 维护内部子控件状态和布局区域。

普通使用不需要重写；用属性和布局即可。

## 5. 深入实践与常见坑

### GroupBox 需要布局

`new QGroupBox("Options")` 之后仍要 `setLayout()`。它不是自动垂直排列的容器。

### 可勾选分组表达启用关系

如果只是想在标题旁放一个复选框，但它不控制内部内容，最好分开使用 `QCheckBox` 和普通容器，避免误导。

### 标题不是帮助文本

标题要短。详细说明放在 label、tooltip 或 whatsThis 中，避免 group box 变得臃肿。
