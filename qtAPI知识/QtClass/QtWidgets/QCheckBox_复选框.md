# Qt QCheckBox 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QCheckBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractButton -> QCheckBox`  
> 定位：复选框

## 1. 先建立整体认识：QCheckBox 到底解决什么问题

`QCheckBox` 用来表达一个可以独立打开或关闭的选项。它和命令按钮的区别是：

- `QPushButton` 重点是“点击后执行一次动作”；
- `QCheckBox` 重点是“当前选项处于什么状态”。

例如：

- 启用自动保存；
- 显示隐藏文件；
- 使用深色主题；
- 记住登录状态；
- 同时勾选多个过滤条件。

复选框通常和其他复选框互不影响。用户可以同时选中“自动保存”“压缩文件”“上传完成后关机”等多个选项。

它继承自 `QAbstractButton`，所以也拥有文本、图标、快捷键、点击信号和按钮事件处理；`QCheckBox` 自己增加的核心能力，是 `Qt::CheckState` 和可选的三态模式。

```text
QAbstractButton
  └─ QCheckBox
```

## 2. 直接结论：什么时候该用它

| 需求 | 推荐控件 |
| --- | --- |
| 多个选项可以同时成立 | `QCheckBox` |
| 一个选项只有开/关两种状态 | 默认二态 `QCheckBox` |
| 父项需要表示“部分子项已选” | 三态 `QCheckBox` |
| 多个选项必须只能选一个 | `QRadioButton` 或排他性的 `QButtonGroup` |
| 点击后立即执行一次动作，不保存选中状态 | `QPushButton` |

判断方法很简单：如果用户是在回答“这个选项要不要”，用复选框；如果用户是在命令程序“现在做某件事”，用命令按钮。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 3.2 头文件

```cpp
#include <QCheckBox>
```

## 4. 最小可用代码

```cpp
#include <QApplication>
#include <QCheckBox>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QCheckBox checkBox(QObject::tr("启用自动保存"));
    checkBox.show();

    return app.exec();
}
```

实际项目里，最常见的逻辑是读取初始状态、连接状态变化信号，再把状态写回配置：

```cpp
auto *autoSave = new QCheckBox(tr("启用自动保存"), this);
autoSave->setChecked(settings.value("autoSave", true).toBool());

connect(autoSave, &QCheckBox::checkStateChanged,
        this, [this](Qt::CheckState state) {
            settings.setValue("autoSave", state == Qt::Checked);
        });
```

如果项目需要兼容 Qt 6.6 或更早版本，`checkStateChanged` 不存在，需要在版本策略允许的前提下使用旧的 `stateChanged(int)`；对于 Qt 6.11 新代码，应优先使用类型明确的 `checkStateChanged(Qt::CheckState)`。

## 5. 二态和三态

### 5.1 默认二态

默认情况下：

```cpp
checkBox->setTristate(false);
```

复选框只有：

```text
Qt::Unchecked
Qt::Checked
```

这正是普通“启用/禁用”“显示/隐藏”选项需要的模型。

### 5.2 三态

三态会额外支持：

```text
Qt::PartiallyChecked
```

它通常不是一个独立业务选项，而是“部分内容已选中”或“当前没有统一决定”的中间状态。

典型场景是树形设置：

```text
[部分选中] 文档
    [选中]  文件 A
    [未选]  文件 B
```

开启三态：

```cpp
auto *documents = new QCheckBox(tr("文档"), this);
documents->setTristate(true);
documents->setCheckState(Qt::PartiallyChecked);
```

三态的关键不是“多一种好看的图标”，而是业务模型真的需要表达第三种状态。若业务只有开和关，就不要为了视觉效果开启三态。

## 6. `checked` 和 `checkState` 怎么选

### 6.1 只有二态时使用 `isChecked()`

如果你明确只使用二态，布尔接口最简单：

```cpp
if (checkBox->isChecked()) {
    enableAutoSave();
}
```

### 6.2 有三态时使用 `checkState()`

三态不能用一个 `bool` 完整表达，所以应使用：

```cpp
switch (checkBox->checkState()) {
case Qt::Unchecked:
    disableForAll();
    break;
case Qt::PartiallyChecked:
    applyToSome();
    break;
case Qt::Checked:
    enableForAll();
    break;
}
```

不要在三态业务里只依赖 `isChecked()`，否则 `PartiallyChecked` 的含义会被压扁成一个无法解释的布尔结果。需要区分三种状态时，`checkState()` 才是准确接口。

## 7. 设置状态：`setChecked()` 和 `setCheckState()`

### 7.1 `setChecked(bool)`

这是从 `QAbstractButton` 继承来的二态写法：

```cpp
checkBox->setChecked(true);
```

它适合业务只有开关的情况。

### 7.2 `setCheckState(Qt::CheckState)`

这是 `QCheckBox` 自己提供的状态接口：

```cpp
checkBox->setCheckState(Qt::PartiallyChecked);
```

它适合需要明确指定 `Unchecked`、`PartiallyChecked`、`Checked` 的场景。

选择原则：

| 业务模型 | 写法 |
| --- | --- |
| 只有开/关 | `setChecked(bool)` |
| 需要三态或希望代码明确表达 Qt 状态 | `setCheckState(Qt::CheckState)` |

## 8. 监听状态变化：优先用 `checkStateChanged`

### 8.1 Qt 6.7 及以后

`checkStateChanged(Qt::CheckState state)` 从 Qt 6.7 开始提供。它每次状态变化时发出，参数直接使用 `Qt::CheckState`：

```cpp
connect(checkBox, &QCheckBox::checkStateChanged,
        this, [](Qt::CheckState state) {
            qDebug() << "new state =" << state;
        });
```

它比传递整数的旧信号更不容易误用。

### 8.2 `stateChanged(int)` 的迁移

旧的：

```cpp
connect(checkBox, &QCheckBox::stateChanged,
        this, [](int state) {
            // 旧代码
        });
```

`stateChanged(int)` 在 Qt 6.9 已废弃。新代码使用：

```cpp
connect(checkBox, &QCheckBox::checkStateChanged,
        this, [](Qt::CheckState state) {
            // 新代码
        });
```

不要为了迁就旧代码，把新的 `Qt::CheckState` 又强行转回 `int`。保持枚举类型可以让状态分支更清晰。

## 9. 复选框和 QButtonGroup 的关系

多个复选框默认表达多个可以同时成立的选项：

```text
[x] 自动保存
[x] 启用压缩
[ ] 完成后关机
```

如果业务上需要把复选框放进一个逻辑组，`QButtonGroup` 可以帮助管理它们；但按钮组本身没有可见界面，只负责逻辑关系。

如果一组按钮必须互斥，也就是只能选一个，通常优先选择 `QRadioButton`。虽然 `QButtonGroup` 也可以让可检查按钮形成排他关系，但控件的视觉语义也应该和行为一致。

## 10. 文本、图标和助记键

复选框和其他按钮一样，可以显示文字和图标：

```cpp
auto *caseSensitive = new QCheckBox(tr("区分大小写"), this);
caseSensitive->setIcon(QIcon(":/icons/case-sensitive.png"));
```

文本中的 `&` 可以生成助记键：

```cpp
auto *checkBox = new QCheckBox(tr("区分大&小写"), this);
```

要显示字面量 `&`，使用 `&&`。

复选框的文本应该描述“选中后会启用什么”，而不是只写抽象名词。例如：

- 好：`启用自动保存`
- 不够清楚：`自动保存`

## 11. 自定义复选框与样式扩展点

### 11.1 `initStyleOption()`

如果派生类要使用 Qt Style 绘制复选框，`initStyleOption(QStyleOptionButton *)` 可以把当前复选框的状态、文字、图标等信息填入样式选项。

这样可以复用当前平台的复选框外观，而不是重新猜测选中、半选、禁用和焦点状态。

### 11.2 `nextCheckState()`

这个函数决定用户点击后状态如何前进。`QCheckBox` 重写它，是因为它需要处理二态和三态逻辑。

自定义三态循环或特殊状态切换时，可以从这里扩展，但应先明确状态循环是否符合用户预期。

### 11.3 `checkStateSet()`

当外部代码使用 `setChecked()` 或其他方式直接设置状态时，`checkStateSet()` 是同步内部中间状态的扩展点。

如果自定义复选框还有额外的内部状态，必须确保“外部直接设状态”和“用户点击切换状态”都能让内部状态保持一致。

### 11.4 `hitButton()`

它决定鼠标点在哪里算命中。普通复选框通常使用默认点击区域；如果自定义了形状或热点区域，才需要重写。

### 11.5 `paintEvent()`

它负责绘制复选框。自定义绘制时，要同时考虑：

- `Unchecked`；
- `PartiallyChecked`；
- `Checked`；
- 禁用状态；
- 获得焦点状态；
- 高 DPI 和当前平台样式。

## 12. 常见使用场景

### 12.1 设置页中的独立开关

```cpp
auto *notifications = new QCheckBox(tr("启用桌面通知"), this);
notifications->setChecked(true);

connect(notifications, &QCheckBox::toggled,
        this, &SettingsPage::setNotificationsEnabled);
```

只有开和关时，`toggled(bool)` 也很方便。若统一按 `Qt::CheckState` 处理，则使用 `checkStateChanged`。

### 12.2 父子选项的部分选中

```cpp
auto *allFiles = new QCheckBox(tr("全部文件"), this);
allFiles->setTristate(true);
allFiles->setCheckState(Qt::PartiallyChecked);
```

父项显示 `PartiallyChecked`，说明子项中有一部分被选中，但不是全部。

### 12.3 过滤条件

多个复选框可以独立组合：

```text
[x] 图片
[ ] 视频
[x] 文档
```

这比把多个条件塞进一个下拉框更直观，适合搜索和筛选界面。

## 13. 常见误区与排查顺序

### 13.1 “为什么复选框不应该使用 clicked 作为唯一状态来源”

`clicked()` 表示一次点击动作，`checkStateChanged()` 表示状态真的变化。  
如果状态可能被代码、模型同步或父子逻辑修改，应该监听状态变化信号。

### 13.2 “三态复选框为什么用 isChecked 不够”

`bool` 只能表达两种情况。需要区分“全部未选”“部分选中”“全部选中”时，必须使用 `checkState()`。

### 13.3 “用了 stateChanged，编译器提示 deprecated”

从 Qt 6.9 开始，使用 `checkStateChanged(Qt::CheckState)` 替代 `stateChanged(int)`。

### 13.4 “一组复选框为什么只能选一个”

检查是否放进了排他性的 `QButtonGroup`，以及是否设置了 `autoExclusive`。复选框默认更适合多选，不要让视觉语义和逻辑行为相冲突。

### 13.5 “父复选框和子复选框状态不同步”

不要只在点击信号里临时改图标。应该把父项状态计算成明确的三态模型：

- 所有子项未选：`Unchecked`
- 所有子项已选：`Checked`
- 其他情况：`PartiallyChecked`

### 13.6 “点击文字没有反应”

检查 `hitButton()` 是否被自定义重写，以及控件尺寸和布局是否覆盖了文本区域。默认情况下应让复选框的正常可点击区域保持完整。

## 14. 逐项 API 说明

### 属性

#### `tristate : bool`

**作用：** 控制复选框是否支持第三种 `Qt::PartiallyChecked` 状态。

**默认值：** `false`，也就是普通二态复选框。

### 成员函数

#### `[explicit] QCheckBox::QCheckBox(QWidget *parent = nullptr)`

**作用：** 构造一个没有文本的复选框。

#### `[explicit] QCheckBox::QCheckBox(const QString &text, QWidget *parent = nullptr)`

**作用：** 构造一个带文本的复选框。

#### `[virtual noexcept] QCheckBox::~QCheckBox()`

**作用：** 销毁复选框。

#### `Qt::CheckState QCheckBox::checkState() const`

**作用：** 返回当前复选框状态。

**关键点：** 三态场景应使用它，不要只读 `isChecked()`。

#### `void QCheckBox::setCheckState(Qt::CheckState state)`

**作用：** 直接设置 `Unchecked`、`PartiallyChecked` 或 `Checked`。

#### `bool QCheckBox::isTristate() const`

**作用：** 查询是否开启三态模式。

#### `void QCheckBox::setTristate(bool y = true)`

**作用：** 开启或关闭三态模式。

### 信号

#### `[signal, since 6.7] void QCheckBox::checkStateChanged(Qt::CheckState state)`

**作用：** 每当复选框状态发生变化时发出，参数是新的 `Qt::CheckState`。

**推荐：** Qt 6.7 及以后新代码优先使用。

### 受保护函数

#### `[override virtual protected] void QCheckBox::checkStateSet()`

**作用：** 外部设置检查状态后的扩展钩子。

#### `[override virtual protected] bool QCheckBox::event(QEvent *e)`

**作用：** 统一事件入口。

#### `[override virtual protected] bool QCheckBox::hitButton(const QPoint &pos) const`

**作用：** 判断鼠标位置是否命中复选框。

#### `[virtual protected] void QCheckBox::initStyleOption(QStyleOptionButton *option) const`

**作用：** 用当前复选框状态初始化样式选项。

#### `[override virtual] QSize QCheckBox::minimumSizeHint() const`

**作用：** 返回最小推荐尺寸。

#### `[override virtual protected] void QCheckBox::mouseMoveEvent(QMouseEvent *e)`

**作用：** 处理鼠标移动和按压过程。

#### `[override virtual protected] void QCheckBox::nextCheckState()`

**作用：** 决定用户点击后进入哪一个检查状态。

#### `[override virtual protected] void QCheckBox::paintEvent(QPaintEvent *)`

**作用：** 绘制复选框。

#### `[override virtual] QSize QCheckBox::sizeHint() const`

**作用：** 返回复选框的推荐尺寸。

### 已废弃信号

#### `[signal, deprecated in 6.9] void QCheckBox::stateChanged(int state)`

**作用：** 旧版状态变化信号。

**迁移：** 使用 `checkStateChanged(Qt::CheckState)`。新代码不应继续使用这个信号。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `tristate : bool` | 控制是否支持 `PartiallyChecked` | 默认关闭，只有业务需要第三种状态时才开启 |
| 成员函数 | `[explicit] QCheckBox::QCheckBox(QWidget *parent = nullptr)` | 构造无文本复选框 | 可后续设置文字和图标 |
| 成员函数 | `[explicit] QCheckBox::QCheckBox(const QString &text, QWidget *parent = nullptr)` | 构造带文本复选框 | 最常见构造方式 |
| 成员函数 | `[virtual noexcept] QCheckBox::~QCheckBox()` | 销毁复选框 | 由 QObject 父子关系管理 |
| 成员函数 | `Qt::CheckState QCheckBox::checkState() const` | 查询三态状态 | 三态时优先使用 |
| 成员函数 | `void QCheckBox::setCheckState(Qt::CheckState state)` | 设置三态状态 | 可设置未选、部分选中、已选 |
| 成员函数 | `bool QCheckBox::isTristate() const` | 查询是否三态 | 只查询模式，不查询当前状态 |
| 成员函数 | `void QCheckBox::setTristate(bool y = true)` | 开关三态模式 | 不等于直接设置当前状态 |
| 信号 | `[signal, since 6.7] void QCheckBox::checkStateChanged(Qt::CheckState state)` | 状态变化通知 | Qt 6.7+ 推荐使用 |
| 受保护函数 | `[override virtual protected] void QCheckBox::checkStateSet()` | 外部设置状态后的钩子 | 自定义内部状态时注意同步 |
| 受保护函数 | `[override virtual protected] bool QCheckBox::event(QEvent *e)` | 统一事件入口 | 可扩展事件处理 |
| 受保护函数 | `[override virtual protected] bool QCheckBox::hitButton(const QPoint &pos) const` | 判断点击命中 | 自定义形状时重写 |
| 受保护函数 | `[virtual protected] void QCheckBox::initStyleOption(QStyleOptionButton *option) const` | 初始化样式选项 | 自定义绘制时复用平台状态 |
| 成员函数 | `[override virtual] QSize QCheckBox::minimumSizeHint() const` | 返回最小推荐尺寸 | 交给布局使用 |
| 受保护函数 | `[override virtual protected] void QCheckBox::mouseMoveEvent(QMouseEvent *e)` | 处理鼠标移动 | 与按压反馈有关 |
| 受保护函数 | `[override virtual protected] void QCheckBox::nextCheckState()` | 决定下一检查状态 | 三态或自定义循环时重点看 |
| 受保护函数 | `[override virtual protected] void QCheckBox::paintEvent(QPaintEvent *)` | 绘制复选框 | 要处理三态、禁用和焦点 |
| 成员函数 | `[override virtual] QSize QCheckBox::sizeHint() const` | 返回推荐尺寸 | 受文字、图标和样式影响 |
| 已废弃信号 | `[signal, deprecated in 6.9] void QCheckBox::stateChanged(int state)` | 旧状态变化通知 | 用 `checkStateChanged(Qt::CheckState)` 替代 |

---

### 一句话总结

`QCheckBox` 表达的是“一个可独立成立的选项”，而不是一次性命令。普通选项使用二态，父子层级或批量选择使用三态；二态可用 `isChecked()`，三态应使用 `checkState()`，状态监听在 Qt 6.7 及以后优先使用 `checkStateChanged(Qt::CheckState)`，不要再为新代码使用 Qt 6.9 已废弃的 `stateChanged(int)`。
