# Qt QButtonGroup 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QButtonGroup>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QObject -> QButtonGroup`  
> 定位：按钮逻辑分组

## 1. 先建立整体认识：QButtonGroup 到底解决什么问题

`QButtonGroup` 不是一个可见控件，它不负责在界面上画出一个“组框”，而是负责**管理一组按钮的逻辑关系**。

它主要解决两类问题：

1. **互斥管理**：一组按钮里只能选一个；
2. **ID 映射**：把按钮和整数 id 互相对应，方便和枚举、配置项、模型数据联动。

你可以把它理解成按钮的“逻辑中枢”：

- 按钮本身负责显示和交互；
- `QButtonGroup` 负责组内关系、选中项和信号转发。

```text
QObject
  └─ QButtonGroup
```

它最常和这些类一起出现：

- `QRadioButton`
- `QCheckBox`
- `QPushButton`
- `QToolButton`

## 2. 直接结论：什么时候该用它

| 场景 | 建议 |
| --- | --- |
| 一组单选按钮需要统一管理 | 用 `QButtonGroup` |
| 一组按钮需要排他选择 | 用 `QButtonGroup` + `setExclusive(true)` |
| 想把按钮映射到枚举值 | 用 `QButtonGroup::setId()` |
| 想快速知道当前是哪个按钮 | 用 `checkedButton()` / `checkedId()` |
| 只是想把几个控件放到一起看起来整齐 | 用 `QGroupBox`，不是 `QButtonGroup` |

`QGroupBox` 是视觉容器，`QButtonGroup` 是逻辑容器。  
这两个名字很像，但职责完全不同。

## 3. 互斥语义：exclusive 是它最重要的属性

### 3.1 默认就是互斥

`exclusive` 默认是 `true`。  
这意味着组里的按钮在逻辑上会互斥：选中一个后，其他可检查按钮会被关闭。

```cpp
auto *group = new QButtonGroup(this);
group->setExclusive(true);
```

### 3.2 互斥组的一个重要规则

在互斥组里，当前被选中的按钮一般不能通过再次点击自己来取消。  
如果你需要“点一下能选中，再点一下能取消”，那不是标准单选组语义。

### 3.3 复选框和单选按钮都能进组，但语义不同

`QButtonGroup` 可以管理 `QRadioButton`、`QCheckBox`，甚至可检查的 `QPushButton`。  
但它们进入组后要保持和界面语义一致：

- `QRadioButton` 更自然地和互斥组配合；
- `QCheckBox` 通常更自然地表示非互斥多选；
- `QPushButton` 进组更多是为了统一 id 或动作映射。

## 4. 构建与包含

### 4.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 4.2 头文件

```cpp
#include <QButtonGroup>
```

## 5. 最小可用代码

```cpp
#include <QApplication>
#include <QButtonGroup>
#include <QRadioButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *group = new QButtonGroup(&window);
    auto *a = new QRadioButton("A", &window);
    auto *b = new QRadioButton("B", &window);
    group->addButton(a, 1);
    group->addButton(b, 2);
    a->setChecked(true);

    window.show();
    return app.exec();
}
```

这段代码的关键不在显示两个按钮，而在于 `group` 让它们有了统一的选中管理和 id 映射。

## 6. 组内成员：add、remove、查询

### 6.1 `addButton()`

```cpp
group->addButton(button, 42);
```

`addButton()` 把按钮加入逻辑组。  
`id` 默认是 `-1`，这时 Qt 会自动分配一个负 id；如果你自己指定 id，建议使用正数，避免和自动分配冲突。

### 6.2 `removeButton()`

```cpp
group->removeButton(button);
```

这只是把按钮从组里移除，不会删除按钮对象本身。

### 6.3 `buttons()`

返回当前组里所有按钮的列表。  
这适合遍历、批量设置和调试。

### 6.4 `button(int id)` 和 `id(QAbstractButton *)`

这两个函数是双向映射：

- `button(id)`：通过 id 找按钮；
- `id(button)`：通过按钮找 id。

这就是 `QButtonGroup` 很适合把 UI 和枚举值连起来的原因。

## 7. 当前选择：checkedButton() 和 checkedId()

### 7.1 `checkedButton()`

返回当前被选中的按钮。如果没有按钮被选中，返回 `nullptr`。

### 7.2 `checkedId()`

返回当前被选中按钮的 id；如果没有选中按钮，返回 `-1`。

```cpp
if (auto *checked = group->checkedButton()) {
    qDebug() << "checked id =" << group->id(checked);
}
```

在互斥组里，这两个接口非常实用，因为它们直接告诉你“当前选的是谁”。

## 8. id 映射为什么有用

`QButtonGroup` 的 id 机制适合把界面选择和程序枚举对应起来：

```cpp
enum ThemeMode {
    FollowSystem = 1,
    LightMode = 2,
    DarkMode = 3
};

group->addButton(systemRadio, FollowSystem);
group->addButton(lightRadio, LightMode);
group->addButton(darkRadio, DarkMode);
```

这样业务层就不必关心具体按钮对象，只要读 `checkedId()` 就知道当前模式。

这在设置页、模式切换和表单配置里特别顺手。

## 9. 信号：既能收按钮对象，也能收 id

`QButtonGroup` 提供两类信号：

| 类型 | 用途 |
| --- | --- |
| `button*` 系列 | 直接拿到按钮对象 |
| `id*` 系列 | 直接拿到整数 id |

例如：

```cpp
connect(group, &QButtonGroup::idClicked, this, &SettingsPage::onModeChanged);
```

如果业务层只关心枚举值，`idClicked(int)` 最直接。  
如果你还要操作按钮对象本身，比如改样式或检查更多属性，就用 `buttonClicked(QAbstractButton *)`。

## 10. 组和父对象不是一回事

这是最容易混的地方之一。

- `parent` 决定 QObject 生命周期；
- `QButtonGroup` 决定按钮逻辑关系。

```cpp
auto *group = new QButtonGroup(this);   // parent 负责生命周期
group->addButton(button);              // group 负责逻辑关系
```

按钮加入组，并不会自动把它变成组的子对象。  
组只是记录和管理它，不是视觉容器，也不是父子所有权容器。

## 11. 常见使用场景

### 11.1 单选模式选择

```cpp
auto *group = new QButtonGroup(this);
group->addButton(ui->radioA, 0);
group->addButton(ui->radioB, 1);
group->addButton(ui->radioC, 2);
ui->radioA->setChecked(true);
```

### 11.2 枚举映射

```cpp
connect(group, &QButtonGroup::idToggled,
        this, [this](int id, bool checked) {
            if (checked)
                setMode(static_cast<Mode>(id));
        });
```

### 11.3 逻辑分组但视觉上分散

有时按钮在界面上分布在不同位置，但业务上仍属于同一个选择集合。  
这时 `QButtonGroup` 比单靠布局更可靠。

## 12. 常见误区与排查顺序

### 12.1 “按钮加进组里后没有互斥”

检查：

1. `exclusive` 是否为 `true`；
2. 按钮是否真的是可检查按钮；
3. 是否有代码手动把状态又改回去了；
4. 是否把同组按钮分到了不同 parent 下，导致默认互斥语义变化。

### 12.2 “移除按钮后它还在界面上”

这是正常的。`removeButton()` 只是不再让组管理它，不会删控件。

### 12.3 “checkedId 返回 -1”

表示当前没有按钮被选中，或者组里没有可检查按钮处于选中状态。

### 12.4 “自动分配的 id 是多少”

自动 id 是负数，且从 `-2` 开始。  
如果你要手工指定 id，最好用正数。

### 12.5 “QButtonGroup 和 QGroupBox 搞混”

一个是逻辑容器，一个是视觉容器。  
想画边框和标题，用 `QGroupBox`；想管按钮关系，用 `QButtonGroup`。

## 13. 逐项 API 说明

### 属性

#### `exclusive : bool`

**作用：** 控制按钮组是否互斥。

**默认值：** `true`。

### 成员函数

#### `[explicit] QButtonGroup::QButtonGroup(QObject *parent = nullptr)`

**作用：** 构造一个空按钮组。

#### `[virtual noexcept] QButtonGroup::~QButtonGroup()`

**作用：** 销毁按钮组。

#### `void QButtonGroup::setExclusive(bool)`

**作用：** 设置按钮组是否互斥。

#### `bool QButtonGroup::exclusive() const`

**作用：** 查询按钮组是否互斥。

#### `void QButtonGroup::addButton(QAbstractButton *button, int id = -1)`

**作用：** 把按钮加入组中，并可为其分配 id。

#### `void QButtonGroup::removeButton(QAbstractButton *button)`

**作用：** 把按钮从组中移除。

#### `QList<QAbstractButton *> QButtonGroup::buttons() const`

**作用：** 返回组内全部按钮。

#### `QAbstractButton *QButtonGroup::checkedButton() const`

**作用：** 返回当前被选中的按钮。

#### `int QButtonGroup::checkedId() const`

**作用：** 返回当前被选中按钮的 id。

#### `QAbstractButton *QButtonGroup::button(int id) const`

**作用：** 通过 id 查询按钮。

#### `void QButtonGroup::setId(QAbstractButton *button, int id)`

**作用：** 为按钮设置 id。

**关键点：** `id` 不能是 `-1`。

#### `int QButtonGroup::id(QAbstractButton *button) const`

**作用：** 查询某个按钮的 id。

### 信号

#### `[signal] void QButtonGroup::buttonClicked(QAbstractButton *button)`

**作用：** 某个按钮被点击时发出。

#### `[signal] void QButtonGroup::buttonPressed(QAbstractButton *button)`

**作用：** 某个按钮被按下时发出。

#### `[signal] void QButtonGroup::buttonReleased(QAbstractButton *button)`

**作用：** 某个按钮被松开时发出。

#### `[signal] void QButtonGroup::buttonToggled(QAbstractButton *button, bool checked)`

**作用：** 某个按钮状态切换时发出。

#### `[signal] void QButtonGroup::idClicked(int id)`

**作用：** 某个 id 对应的按钮被点击时发出。

#### `[signal] void QButtonGroup::idPressed(int id)`

**作用：** 某个 id 对应的按钮被按下时发出。

#### `[signal] void QButtonGroup::idReleased(int id)`

**作用：** 某个 id 对应的按钮被松开时发出。

#### `[signal] void QButtonGroup::idToggled(int id, bool checked)`

**作用：** 某个 id 对应的按钮状态切换时发出。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `exclusive : bool` | 控制是否互斥 | 默认 `true`，是组行为核心 |
| 成员函数 | `[explicit] QButtonGroup::QButtonGroup(QObject *parent = nullptr)` | 构造按钮组 | `parent` 只管生命周期 |
| 成员函数 | `[virtual noexcept] QButtonGroup::~QButtonGroup()` | 销毁按钮组 | 不会自动删除按钮控件 |
| 成员函数 | `void QButtonGroup::setExclusive(bool)` | 设置是否互斥 | 和单选语义直接相关 |
| 成员函数 | `bool QButtonGroup::exclusive() const` | 查询是否互斥 | 调试组行为时先看它 |
| 成员函数 | `void QButtonGroup::addButton(QAbstractButton *button, int id = -1)` | 加入按钮并分配 id | 自动 id 为负数，手工 id 建议用正数 |
| 成员函数 | `void QButtonGroup::removeButton(QAbstractButton *button)` | 移除按钮 | 不删除按钮对象 |
| 成员函数 | `QList<QAbstractButton *> QButtonGroup::buttons() const` | 返回全部按钮 | 可用于遍历和调试 |
| 成员函数 | `QAbstractButton *QButtonGroup::checkedButton() const` | 返回当前选中按钮 | 无选中时是 `nullptr` |
| 成员函数 | `int QButtonGroup::checkedId() const` | 返回当前选中 id | 无选中时是 `-1` |
| 成员函数 | `QAbstractButton *QButtonGroup::button(int id) const` | 通过 id 找按钮 | id 不存在时返回 `nullptr` |
| 成员函数 | `void QButtonGroup::setId(QAbstractButton *button, int id)` | 设置按钮 id | `id` 不能为 `-1` |
| 成员函数 | `int QButtonGroup::id(QAbstractButton *button) const` | 查询按钮 id | 找不到时返回 `-1` |
| 信号 | `[signal] void QButtonGroup::buttonClicked(QAbstractButton *button)` | 按钮点击通知 | 直接拿按钮对象 |
| 信号 | `[signal] void QButtonGroup::buttonPressed(QAbstractButton *button)` | 按钮按下通知 | 适合过程反馈 |
| 信号 | `[signal] void QButtonGroup::buttonReleased(QAbstractButton *button)` | 按钮释放通知 | 适合过程反馈 |
| 信号 | `[signal] void QButtonGroup::buttonToggled(QAbstractButton *button, bool checked)` | 按钮状态切换通知 | 适合状态同步 |
| 信号 | `[signal] void QButtonGroup::idClicked(int id)` | id 点击通知 | 枚举映射最方便 |
| 信号 | `[signal] void QButtonGroup::idPressed(int id)` | id 按下通知 | 过程反馈 |
| 信号 | `[signal] void QButtonGroup::idReleased(int id)` | id 释放通知 | 过程反馈 |
| 信号 | `[signal] void QButtonGroup::idToggled(int id, bool checked)` | id 状态切换通知 | 业务映射最常用 |

---

### 一句话总结

`QButtonGroup` 不负责显示，只负责组织按钮关系。它最重要的价值是互斥管理和 id 映射：前者让单选语义可靠，后者让按钮和枚举、配置项、业务状态连接起来。
