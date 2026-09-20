# Qt QGroupBox 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QGroupBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QGroupBox`  
> 定位：带标题的视觉容器

## 1. 先建立整体认识：QGroupBox 到底解决什么问题

`QGroupBox` 是一个**视觉容器**。它会画出边框、标题和可选的勾选状态，但它本身并不负责自动把子控件排版好。子控件要靠布局来摆放。

它解决的问题主要有三个：

1. 给一组相关控件加上标题；
2. 用边框把一块设置区域或表单区域视觉上圈起来；
3. 在需要时把整组内容变成“可勾选启用/禁用”的区域。

```text
QWidget
  └─ QGroupBox
```

它和 `QButtonGroup` 很容易被混淆，但职责不同：

- `QGroupBox` 是画出来的容器；
- `QButtonGroup` 是逻辑分组器，不负责显示。

## 2. 直接结论：什么时候该用它

| 场景 | 建议 |
| --- | --- |
| 想把一组相关设置框起来 | 用 `QGroupBox` |
| 想给区域加标题 | 用 `QGroupBox` |
| 想让整组子控件随一个复选框启用/禁用 | 用 `checkable` 的 `QGroupBox` |
| 想管理单选按钮的互斥 | 用 `QButtonGroup` |
| 想要一个纯视觉边框、标题分区 | 用 `QGroupBox` |

它很适合设置页、参数面板和表单分区。

## 3. 最小可用代码

```cpp
#include <QApplication>
#include <QGroupBox>
#include <QVBoxLayout>
#include <QRadioButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QGroupBox groupBox("显示模式");
    auto *layout = new QVBoxLayout(&groupBox);
    layout->addWidget(new QRadioButton("浅色"));
    layout->addWidget(new QRadioButton("深色"));

    groupBox.show();
    return app.exec();
}
```

注意：`QGroupBox` 不会自动帮你摆放子控件。  
如果不加布局，子控件只是挂在里面，不会自动排列得整整齐齐。

## 4. 标题、对齐和助记键

### 4.1 `title`

`title` 是组框顶部显示的文字。它通常直接在构造函数中设置，也可以之后再改：

```cpp
groupBox->setTitle(tr("用户信息"));
```

标题里带 `&` 时，会生成助记键：

```cpp
groupBox->setTitle(tr("&User information"));
```

这样 `Alt+U` 可以把键盘焦点移动到组框的子控件之一。

### 4.2 `alignment`

`alignment` 控制标题在顶部的对齐方式，例如左对齐、右对齐或居中。

常见情况是默认左对齐，只有在版式需要时才调整。

## 5. flat、checkable、checked：三个很容易混的属性

### 5.1 `flat`

`flat` 决定组框是否以更扁平的方式绘制。  
开启后，很多样式会弱化侧边和底边框线，让区域看起来更轻。

这属于视觉风格，不是交互逻辑。

### 5.2 `checkable`

`checkable` 决定组框标题前是否显示一个复选框。  
启用后，组框就不只是标题容器了，还成了一个“总开关”。

```cpp
groupBox->setCheckable(true);
```

### 5.3 `checked`

如果组框是可勾选的，`checked` 表示这个总开关当前是否开启。  
当它被取消时，组内子控件通常会一起被禁用。

```cpp
groupBox->setChecked(false);
```

这里最重要的语义是：

- `checkable` 是模式；
- `checked` 是当前状态；
- `flat` 只是外观。

## 6. 组框和子控件的关系

`QGroupBox` 不会自动给子控件做布局，也不会自动决定你里面放什么。  
它只提供一个标题框和相关交互。

典型用法是：

1. 创建 `QGroupBox`；
2. 创建 `QVBoxLayout` 或 `QGridLayout`；
3. 把控件加入布局；
4. `setLayout()` 给组框。

这也是为什么官方示例里，组框几乎总是和布局一起出现。

## 7. 信号：clicked 和 toggled

### 7.1 `clicked(bool)`

当组框是可勾选的，并且用户通过鼠标或快捷键激活它时，会发出 `clicked()`。

### 7.2 `toggled(bool)`

当可勾选组框的状态变化时，会发出 `toggled(bool)`。  
如果你关心“启用/禁用整组内容”的变化，通常更应该接这个信号。

```cpp
connect(groupBox, &QGroupBox::toggled, this, [this](bool on) {
    qDebug() << "group enabled =" << on;
});
```

## 8. 典型使用场景

### 8.1 设置分区

```cpp
auto *group = new QGroupBox(tr("显示设置"), this);
auto *layout = new QVBoxLayout(group);
layout->addWidget(new QRadioButton(tr("浅色")));
layout->addWidget(new QRadioButton(tr("深色")));
```

### 8.2 可启用的高级选项区

```cpp
auto *advanced = new QGroupBox(tr("高级选项"), this);
advanced->setCheckable(true);
advanced->setChecked(false);
```

这适合“默认隐藏一部分复杂设置，但用户可以主动打开”的场景。

### 8.3 和单选按钮一起使用

`QGroupBox` 很常见的内容就是一组 `QRadioButton`。  
它提供视觉分区，单选按钮负责选择语义。

## 9. 样式扩展点

### 9.1 `initStyleOption()`

这个函数会把组框当前状态填进 `QStyleOptionGroupBox`。  
如果你要自定义绘制，或者想在派生类里复用平台样式，就会用到它。

### 9.2 `paintEvent()`

负责真正绘制标题、边框和勾选状态。

### 9.3 `resizeEvent()`

当组框尺寸变化时，Qt 需要重新安排其内部视觉结果。  
这对标题区域、边框和布局更新都很重要。

### 9.4 `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()`

这些事件和组框的可勾选标题交互有关。  
普通视觉容器通常不需要手动碰它们，但理解它们能帮助你看懂 checkable 组框的行为。

## 10. 常见误区与排查顺序

### 10.1 “QGroupBox 能不能自动排版子控件”

不能。  
它只是容器外壳，布局还是要你自己加。

### 10.2 “QGroupBox 和 QButtonGroup 是不是一回事”

不是。  
一个负责画出来，一个负责逻辑管理。

### 10.3 “checked 了但子控件还能操作”

如果你手动给子控件重新启用了，效果就可能不再一致。  
默认语义是：checkable 组框取消后，子控件应整体失效。

### 10.4 “标题对齐没变化”

先确认样式是否支持明显的标题对齐差异，再看 `alignment` 是否真的设置成功。

### 10.5 “flat 没什么区别”

这是样式相关的正常现象。  
不同平台或不同 style 对 flat 的表现并不完全一样。

## 11. 逐项 API 说明

### 属性

#### `alignment : Qt::Alignment`

**作用：** 控制组框标题的对齐方式。

#### `checkable : bool`

**作用：** 控制组框标题前是否显示复选框。

#### `checked : bool`

**作用：** 控制或查询 checkable 组框当前是否被选中。

#### `flat : bool`

**作用：** 控制组框是否以更扁平的方式绘制。

#### `title : QString`

**作用：** 组框标题文本。

### 成员函数

#### `[explicit] QGroupBox::QGroupBox(QWidget *parent = nullptr)`

**作用：** 构造一个没有标题的组框。

#### `[explicit] QGroupBox::QGroupBox(const QString &title, QWidget *parent = nullptr)`

**作用：** 构造一个带标题的组框。

#### `[virtual noexcept] QGroupBox::~QGroupBox()`

**作用：** 销毁组框。

#### `QString QGroupBox::title() const`

**作用：** 查询标题文本。

#### `void QGroupBox::setTitle(const QString &title)`

**作用：** 设置标题文本。

#### `Qt::Alignment QGroupBox::alignment() const`

**作用：** 查询标题对齐方式。

#### `void QGroupBox::setAlignment(int alignment)`

**作用：** 设置标题对齐方式。

#### `QSize QGroupBox::minimumSizeHint() const`

**作用：** 返回组框的最小推荐尺寸。

#### `bool QGroupBox::isFlat() const`

**作用：** 查询是否扁平绘制。

#### `void QGroupBox::setFlat(bool flat)`

**作用：** 设置是否扁平绘制。

#### `bool QGroupBox::isCheckable() const`

**作用：** 查询是否可勾选。

#### `void QGroupBox::setCheckable(bool checkable)`

**作用：** 设置是否可勾选。

#### `bool QGroupBox::isChecked() const`

**作用：** 查询当前是否选中。

### 公共槽

#### `[slot] void QGroupBox::setChecked(bool checked)`

**作用：** 设置可勾选组框的当前状态。

### 信号

#### `[signal] void QGroupBox::clicked(bool checked = false)`

**作用：** 用户激活可勾选组框时发出。

#### `[signal] void QGroupBox::toggled(bool on)`

**作用：** 可勾选组框状态变化时发出。

### 受保护函数

#### `[override virtual protected] void QGroupBox::changeEvent(QEvent *ev)`

**作用：** 处理变化事件。

#### `[override virtual protected] void QGroupBox::childEvent(QChildEvent *c)`

**作用：** 处理子对象变化。

#### `[override virtual protected] bool QGroupBox::event(QEvent *e)`

**作用：** 统一事件入口。

#### `[override virtual protected] void QGroupBox::focusInEvent(QFocusEvent *fe)`

**作用：** 获得焦点时处理。

#### `[virtual protected] void QGroupBox::initStyleOption(QStyleOptionGroupBox *option) const`

**作用：** 初始化样式选项。

#### `[override virtual protected] void QGroupBox::mouseMoveEvent(QMouseEvent *event)`

**作用：** 处理鼠标移动。

#### `[override virtual protected] void QGroupBox::mousePressEvent(QMouseEvent *event)`

**作用：** 处理鼠标按下。

#### `[override virtual protected] void QGroupBox::mouseReleaseEvent(QMouseEvent *event)`

**作用：** 处理鼠标释放。

#### `[override virtual protected] void QGroupBox::paintEvent(QPaintEvent *event)`

**作用：** 绘制组框。

#### `[override virtual protected] void QGroupBox::resizeEvent(QResizeEvent *e)`

**作用：** 处理尺寸变化。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `alignment : Qt::Alignment` | 控制标题对齐 | 通常只影响标题位置 |
| 属性 | `checkable : bool` | 控制是否带复选框 | 开启后组框变成总开关 |
| 属性 | `checked : bool` | 控制是否选中 | 只对 checkable 有意义 |
| 属性 | `flat : bool` | 控制是否扁平绘制 | 主要影响外观 |
| 属性 | `title : QString` | 组框标题 | 可带助记符 |
| 成员函数 | `[explicit] QGroupBox::QGroupBox(QWidget *parent = nullptr)` | 构造无标题组框 | 后续可再设标题 |
| 成员函数 | `[explicit] QGroupBox::QGroupBox(const QString &title, QWidget *parent = nullptr)` | 构造带标题组框 | 最常见构造方式 |
| 成员函数 | `[virtual noexcept] QGroupBox::~QGroupBox()` | 销毁组框 | 由 QObject 父子关系管理 |
| 成员函数 | `QString QGroupBox::title() const` | 查询标题 | 常和 `setTitle()` 配对 |
| 成员函数 | `void QGroupBox::setTitle(const QString &title)` | 设置标题 | 标题可带助记符 |
| 成员函数 | `Qt::Alignment QGroupBox::alignment() const` | 查询标题对齐 | 看标题在顶部如何排 |
| 成员函数 | `void QGroupBox::setAlignment(int alignment)` | 设置标题对齐 | 用 Qt 对齐标志组合 |
| 成员函数 | `QSize QGroupBox::minimumSizeHint() const` | 返回最小推荐尺寸 | 交给布局系统使用 |
| 成员函数 | `bool QGroupBox::isFlat() const` | 查询扁平状态 | 主要影响边框绘制 |
| 成员函数 | `void QGroupBox::setFlat(bool flat)` | 设置扁平状态 | 不改变逻辑行为 |
| 成员函数 | `bool QGroupBox::isCheckable() const` | 查询是否可勾选 | 只是一种总开关模式 |
| 成员函数 | `void QGroupBox::setCheckable(bool checkable)` | 设置是否可勾选 | 开启后会显示复选框 |
| 成员函数 | `bool QGroupBox::isChecked() const` | 查询是否选中 | 只对可勾选组框有意义 |
| 公共槽 | `[slot] void QGroupBox::setChecked(bool checked)` | 设置选中状态 | 会影响子控件启用状态 |
| 信号 | `[signal] void QGroupBox::clicked(bool checked = false)` | 用户激活时发出 | `setChecked()` 不会触发它 |
| 信号 | `[signal] void QGroupBox::toggled(bool on)` | 状态变化时发出 | 常用于同步子控件 |
| 受保护函数 | `[override virtual protected] void QGroupBox::changeEvent(QEvent *ev)` | 处理变化事件 | 样式/语言变化相关 |
| 受保护函数 | `[override virtual protected] void QGroupBox::childEvent(QChildEvent *c)` | 处理子对象变化 | 子控件动态加入时会涉及 |
| 受保护函数 | `[override virtual protected] bool QGroupBox::event(QEvent *e)` | 统一事件入口 | 派生扩展点 |
| 受保护函数 | `[override virtual protected] void QGroupBox::focusInEvent(QFocusEvent *fe)` | 焦点进入处理 | 与助记符相关 |
| 受保护函数 | `[virtual protected] void QGroupBox::initStyleOption(QStyleOptionGroupBox *option) const` | 初始化样式选项 | 自定义绘制很有用 |
| 受保护函数 | `[override virtual protected] void QGroupBox::mouseMoveEvent(QMouseEvent *event)` | 处理鼠标移动 | 与 checkable 行为相关 |
| 受保护函数 | `[override virtual protected] void QGroupBox::mousePressEvent(QMouseEvent *event)` | 处理鼠标按下 | checkable 标题交互会用到 |
| 受保护函数 | `[override virtual protected] void QGroupBox::mouseReleaseEvent(QMouseEvent *event)` | 处理鼠标释放 | checkable 标题交互会用到 |
| 受保护函数 | `[override virtual protected] void QGroupBox::paintEvent(QPaintEvent *event)` | 绘制组框 | 标题和边框都在这里体现 |
| 受保护函数 | `[override virtual protected] void QGroupBox::resizeEvent(QResizeEvent *e)` | 处理尺寸变化 | 影响内部布局区域 |

---

### 一句话总结

`QGroupBox` 是一个带标题和边框的视觉容器。它用来分区、命名和可选地提供总开关，但不会替你摆放子控件；真正的布局仍然要交给 `QLayout`，而逻辑互斥则要交给 `QButtonGroup`。
