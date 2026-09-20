# QRadioButton

> Qt 6.11.1 · Qt Widgets · 来自 `QRadioButton`

## 1. 先建立直觉

### 这是什么

`QRadioButton` 是用于“同一组选项中只能选一个”的按钮控件。它继承 `QAbstractButton`，但默认具有单选语义：同一父控件下的 radio button 通常自动互斥，选中一个会取消另一个。

它表达的是选择一个模式、方案、级别或类别，而不是执行命令。用户看到单选按钮，会预期这一组选项彼此排斥，而且总能清楚知道当前选的是哪一个。

### 适合使用的场景

- 选项数量少、全部应同时可见。
- 用户需要在几个互斥方案中选择一个，例如方向、模式、编码、权限级别。
- 需要比下拉框更直观地展示所有可选值。
- 需要和 `QButtonGroup` 结合，把按钮映射到枚举或整数 id。

### 不适合的场景

- 多个选项可以同时选，用 `QCheckBox`。
- 选项很多或动态变化，用 `QComboBox`、列表或模型视图。
- 点击后立即执行命令，用 `QPushButton` 或 `QToolButton`。

### 最小示例

```cpp
auto *group = new QButtonGroup(this);
auto *compact = new QRadioButton(tr("Compact"), this);
auto *comfortable = new QRadioButton(tr("Comfortable"), this);

group->addButton(compact, 0);
group->addButton(comfortable, 1);
comfortable->setChecked(true);

connect(group, &QButtonGroup::idClicked, this, &Window::setDensityMode);
```

`QButtonGroup` 让分组关系和业务 id 都变得显式，比单靠共同 parent 更好维护。

## 2. 依赖与对象关系

- 头文件：`#include <QRadioButton>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractButton`
- 直接派生类：类页未列出

`QRadioButton` 的可点击、checked、文本、图标和信号语义来自 `QAbstractButton`。它自身公开 API 很少，主要差异在默认外观、默认互斥行为和绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QRadioButton(QWidget *parent)` | 创建无文本单选按钮。 |
| `QRadioButton(const QString &text, QWidget *parent)` | 创建带文本单选按钮。 |
| `~QRadioButton()` | 销毁单选按钮。 |
| `sizeHint() const` / `minimumSizeHint() const` | 返回单选按钮推荐尺寸。 |
| `initStyleOption(QStyleOptionButton *option) const` | 为自定义绘制准备 style option。 |
| `hitButton(const QPoint &pos) const` | 判断坐标是否命中按钮。 |
| `event()` / `mouseMoveEvent()` / `paintEvent()` | 事件处理与绘制实现。 |

## 4. API 逐项说明

### `QRadioButton(QWidget *parent = nullptr)`

创建无文本单选按钮。无文本 radio button 很少用于普通表单，因为用户难以理解它代表的选项。

如果旁边有独立 label，要确保点击 label 或键盘导航仍然可用，否则体验会不如带文本构造。

### `QRadioButton(const QString &text, QWidget *parent = nullptr)`

创建带文本单选按钮。文本可以包含 `&` 助记符，让用户通过键盘快速选择。

单选按钮文案通常应是名词或短语，而不是动词命令。例如“UTF-8”“GBK”“自动检测”，而不是“选择 UTF-8”。

### `~QRadioButton()`

销毁按钮对象。通常由父控件负责。

如果按钮属于 `QButtonGroup`，销毁时 QObject 关系会清理连接；但业务侧保存的 id 或指针仍需自己维护。

### `sizeHint()` / `minimumSizeHint()`

返回包含圆形指示器、文本和 style 间距的尺寸。不同平台 radio button 的指示器大小可能不同。

不要用固定宽度截断选项文案。互斥选项一旦读不全，用户就无法做可靠选择。

### `initStyleOption(QStyleOptionButton *option) const`

填充绘制所需的按钮状态。自定义 radio button 外观时使用它，能保留 checked、焦点、禁用、hover 等平台状态。

完全手绘单选按钮时，要格外注意焦点框和键盘可达性。

### `hitButton()` / `event()` / `mouseMoveEvent()` / `paintEvent()`

底层命中测试、事件处理和绘制接口。普通使用不需要重写。

如果重写命中区域，文本区域仍应可点击。用户不会期待只能点小圆点。

## 5. 深入实践与常见坑

### 分组关系要清楚

同一父控件下的 radio button 会自动排他，但复杂页面中父子层级不总能表达业务分组。使用 `QButtonGroup` 可以让分组独立于布局结构。

### 默认选项很重要

一组 radio button 通常应有一个已选中项。没有默认值会让表单状态不完整，也会让键盘用户难以判断当前选择。

### 选项太多就换控件

超过五六个互斥选项时，radio button 会占用大量空间。下拉框、列表或分组页面可能更合适。
