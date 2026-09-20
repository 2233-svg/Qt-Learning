# Qt QRadioButton 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QRadioButton>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractButton -> QRadioButton`  
> 定位：单选按钮

## 1. 先建立整体认识：QRadioButton 到底解决什么问题

`QRadioButton` 用来表达“多个选项中只能选一个”。它适合回答“下列方案里选哪一个”“当前模式是哪一个”“用哪种输入方式”。

它和 `QCheckBox` 最大的不同是语义：

- `QCheckBox` 更适合多个独立开关；
- `QRadioButton` 更适合互斥选择。

如果用户选中了一个单选按钮，通常另一个单选按钮就要自动取消。这个“组内互斥”的特性是它的核心，不是附带功能。

它继承自 `QAbstractButton`，所以也有文本、图标、快捷键、点击信号和样式钩子；但它的默认行为更偏向“同组互斥、只能选一个”。

```text
QAbstractButton
  └─ QRadioButton
```

## 2. 直接结论：什么时候该用它

| 场景 | 推荐控件 |
| --- | --- |
| 多个选项里只能选一个 | `QRadioButton` |
| 需要一个默认可见的当前方案 | `QRadioButton` |
| 设置页中需要明确单选项 | `QRadioButton` |
| 每个选项可以独立开关 | `QCheckBox` |
| 点击后立即执行一次动作 | `QPushButton` |

如果你发现自己在做“选方案”，大概率应该想到单选按钮。  
如果你在做“打开/关闭某个功能”，则应该想到复选框。

## 3. 组内互斥：它最重要的语义

### 3.1 同一个父控件下的默认互斥

`QRadioButton` 默认是 `autoExclusive` 的。  
这意味着同一个父控件里的单选按钮会自动表现为互斥组：选中一个，其它同父的单选按钮会被取消。

```cpp
auto *light = new QRadioButton(tr("浅色"), this);
auto *dark  = new QRadioButton(tr("深色"), this);
auto *autoTheme = new QRadioButton(tr("跟随系统"), this);
```

如果三个按钮有相同父对象，默认就能形成互斥关系。

### 3.2 需要多个互斥组时，用 `QButtonGroup`

如果同一个父控件里需要两组彼此独立的单选按钮，就不能只靠 `autoExclusive`，而应显式使用 `QButtonGroup`：

```cpp
auto *group1 = new QButtonGroup(this);
group1->addButton(ui->lightRadio);
group1->addButton(ui->darkRadio);

auto *group2 = new QButtonGroup(this);
group2->addButton(ui->englishRadio);
group2->addButton(ui->chineseRadio);
```

这样可以让“主题选择”和“语言选择”两组单选按钮互不干扰。

### 3.3 单选按钮为什么通常不该单独使用

单个 `QRadioButton` 没有太大意义，因为它的价值来自“在一组里互斥”。  
真正应该思考的是“这一组选项怎么组织”，而不是“一个按钮怎么画”。

## 4. 构建与包含

### 4.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 4.2 头文件

```cpp
#include <QRadioButton>
```

## 5. 最小可用代码

```cpp
#include <QApplication>
#include <QRadioButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QRadioButton radioButton(QObject::tr("深色模式"));
    radioButton.show();

    return app.exec();
}
```

更常见的是把几个单选按钮放在一起，再根据 `toggled()` 或 `isChecked()` 读取当前选择：

```cpp
connect(darkRadio, &QRadioButton::toggled, this, [this](bool checked) {
    if (checked)
        applyDarkTheme();
});
```

## 6. 状态和信号怎么理解

`QRadioButton` 本质上仍然是一个 `QAbstractButton`，所以它最重要的状态还是 `checked` 和 `down`。

| 状态 | 含义 |
| --- | --- |
| `checked` | 当前是否被选中 |
| `down` | 当前是否处于按压中 |
| `autoExclusive` | 是否默认参与同父互斥 |

在单选语义里，最重要的是 `checked`。  
你通常关心的不是“按钮有没有按下去”，而是“这一组里现在是哪一个被选中”。

## 7. 文本、图标和助记键

`QRadioButton` 和 `QPushButton` 一样，可以有文本和图标：

```cpp
auto *radio = new QRadioButton(tr("搜&索当前文件"), this);
radio->setIcon(QIcon(":/icons/search.png"));
```

如果文本里有 `&`，会生成助记键。  
比如 `&` 后面的字符会成为快捷助记符，`&&` 表示字面量的 `&`。

在单选按钮上，文本应该直接描述“这个选项是什么”，不要写成笼统的按钮说明。  
例如：

- 好：`深色模式`
- 更清楚：`跟随系统`
- 不够准确：`设置主题`

## 8. 常见使用场景

### 8.1 主题选择

```cpp
auto *light = new QRadioButton(tr("浅色"), this);
auto *dark = new QRadioButton(tr("深色"), this);
auto *system = new QRadioButton(tr("跟随系统"), this);

dark->setChecked(true);
```

### 8.2 输入方式选择

```cpp
auto *textMode = new QRadioButton(tr("文本输入"), this);
auto *voiceMode = new QRadioButton(tr("语音输入"), this);
```

### 8.3 单一模式开关

```cpp
auto *basic = new QRadioButton(tr("基础模式"), this);
auto *advanced = new QRadioButton(tr("高级模式"), this);
```

这些都不是“能不能勾选”，而是“当前选哪一个”。

## 9. 关键公共 API

### 9.1 构造函数

`QRadioButton(QWidget *parent = nullptr)` 适合先建对象再设文本。  
`QRadioButton(const QString &text, QWidget *parent = nullptr)` 适合直接给文本。  
单选按钮不像命令按钮那样需要很多额外初始化，通常构造后加入布局即可。

### 9.2 `sizeHint()` 和 `minimumSizeHint()`

这两个函数提供推荐尺寸。  
它们会受到文字、图标、样式和平台规则影响。

单选按钮通常希望自然地排成一列，所以尺寸一般由布局来管理，不必手写像素。

### 9.3 `setChecked()` 与 `toggled()`

设置当前选中项时，通常直接调用 `setChecked(true)`：

```cpp
dark->setChecked(true);
```

要响应用户切换，优先接 `toggled(bool)`：

```cpp
connect(system, &QRadioButton::toggled, this, [this](bool checked) {
    if (checked)
        useSystemTheme();
});
```

对单选按钮来说，`toggled()` 比 `clicked()` 更贴近“选择变化”这个语义。

## 10. 样式扩展点

### 10.1 `initStyleOption()`

如果你要自己画单选按钮，`initStyleOption(QStyleOptionButton *)` 可以把当前状态填到样式选项里，方便用 Qt Style 画出标准外观。

### 10.2 `hitButton()`

默认情况下，单选按钮的点击区域是控件自身区域。  
如果你要做特殊形状或更窄的点击热点，才需要重写它。

### 10.3 `paintEvent()`

这是按钮真正的绘制入口。  
自定义外观时，要同时考虑选中、禁用、焦点和按压状态。

## 11. 常见误区与排查顺序

### 11.1 “单选按钮为什么没有自动互斥”

先看它们是不是同一个父对象。  
再看 `autoExclusive` 是否被关掉。  
如果有复杂分组，再看是否应该显式使用 `QButtonGroup`。

### 11.2 “我能同时选中多个单选按钮”

这通常说明它们不在同一互斥范围内，或者分到了不同父对象里。  
单选按钮的语义前提就是“组内只保留一个选中项”。

### 11.3 “点击选项但当前状态没变”

检查是否有代码在 `toggled()` 里又把状态改回去了。  
这类问题通常是业务逻辑和按钮组互斥机制打架。

### 11.4 “一个父窗口里要两组单选项”

不要只靠视觉空白分隔。  
要用不同 `QButtonGroup` 或不同父容器明确分组。

### 11.5 “为什么选中态应当由按钮组管理”

因为单选按钮的真正问题不是单个按钮，而是“哪一个被保留为当前选择”。  
组管理比单个按钮更能表达这个语义。

## 12. 逐项 API 说明

### 成员函数

#### `[explicit] QRadioButton::QRadioButton(QWidget *parent = nullptr)`

**作用：** 构造一个没有文本的单选按钮。

#### `[explicit] QRadioButton::QRadioButton(const QString &text, QWidget *parent = nullptr)`

**作用：** 构造一个带文本的单选按钮。

#### `[virtual noexcept] QRadioButton::~QRadioButton()`

**作用：** 销毁单选按钮。

#### `[override virtual protected] bool QRadioButton::event(QEvent *e)`

**作用：** 处理统一事件入口。

#### `[override virtual protected] bool QRadioButton::hitButton(const QPoint &pos) const`

**作用：** 判断点击位置是否命中。

#### `[virtual protected] void QRadioButton::initStyleOption(QStyleOptionButton *option) const`

**作用：** 用当前状态初始化样式选项。

#### `[override virtual] QSize QRadioButton::minimumSizeHint() const`

**作用：** 返回最小推荐尺寸。

#### `[override virtual protected] void QRadioButton::mouseMoveEvent(QMouseEvent *e)`

**作用：** 处理鼠标移动。

#### `[override virtual protected] void QRadioButton::paintEvent(QPaintEvent *)`

**作用：** 绘制单选按钮。

#### `[override virtual] QSize QRadioButton::sizeHint() const`

**作用：** 返回推荐尺寸。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员函数 | `[explicit] QRadioButton::QRadioButton(QWidget *parent = nullptr)` | 构造无文本单选按钮 | 一般会再设置文本 |
| 成员函数 | `[explicit] QRadioButton::QRadioButton(const QString &text, QWidget *parent = nullptr)` | 构造带文本单选按钮 | 最常见构造方式 |
| 成员函数 | `[virtual noexcept] QRadioButton::~QRadioButton()` | 销毁单选按钮 | 由 QObject 父子关系管理 |
| 成员函数 | `[override virtual protected] bool QRadioButton::event(QEvent *e)` | 统一事件入口 | 可扩展行为 |
| 成员函数 | `[override virtual protected] bool QRadioButton::hitButton(const QPoint &pos) const` | 判断可点击区域 | 特殊形状才重写 |
| 成员函数 | `[virtual protected] void QRadioButton::initStyleOption(QStyleOptionButton *option) const` | 初始化样式选项 | 自定义绘制时很有用 |
| 成员函数 | `[override virtual] QSize QRadioButton::minimumSizeHint() const` | 返回最小推荐尺寸 | 交给布局决定最终大小 |
| 成员函数 | `[override virtual protected] void QRadioButton::mouseMoveEvent(QMouseEvent *e)` | 处理鼠标移动 | 与按压反馈有关 |
| 成员函数 | `[override virtual protected] void QRadioButton::paintEvent(QPaintEvent *)` | 绘制单选按钮 | 样式和状态都在这里体现 |
| 成员函数 | `[override virtual] QSize QRadioButton::sizeHint() const` | 返回推荐尺寸 | 会受样式和文字影响 |

---

### 一句话总结

`QRadioButton` 解决的是“多个选项里只能选一个”的问题。它的核心不是按钮本身，而是同父互斥和 `QButtonGroup` 分组；实际使用时，优先把它放进明确的选择组里，再用 `toggled()` 读取当前选项。
