# Qt QSizePolicy 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QSizePolicy>`  
> 所属模块：`Qt6::Widgets`  
> 定位：控件向布局系统声明“尺寸可伸缩意愿”的值类型

## 1. QSizePolicy 解决什么问题

窗口变大时，布局必须决定：哪些控件应该变大，哪些控件保持接近原尺寸；窗口变小时，又该优先压缩谁。

`QSizePolicy` 不是控件的实际尺寸，也不是 `setFixedSize()` 的替代品。它表达的是控件对布局的偏好：

```text
QWidget::sizeHint()      我觉得多大合适
QWidget::minimumSize()   我最小能多小
QWidget::maximumSize()   我最大能多大
QSizePolicy              我愿不愿意变大或变小
QBoxLayout stretch       多个项目争夺余量时按什么比例分
```

布局引擎综合这些信息，而不是只看其中一个。

典型现象：

- 输入框应随窗口变宽，按钮通常不必变宽；
- 分隔线可以被压缩，编辑区应优先获得空间；
- 自动换行标签变窄后需要变高；
- 隐藏某个控件时，可能需要保留原位置以避免界面跳动。

这些都是 `QSizePolicy` 的职责范围。

## 2. 最常见的使用方式

`QSizePolicy` 是值类型，通常从控件取出、修改再设回去：

```cpp
auto policy = editor->sizePolicy();
policy.setHorizontalPolicy(QSizePolicy::Expanding);
policy.setVerticalPolicy(QSizePolicy::Fixed);
editor->setSizePolicy(policy);
```

也可以直接设置：

```cpp
editor->setSizePolicy(
    QSizePolicy::Expanding,
    QSizePolicy::Fixed);
```

注意：修改 policy 后，若控件已经显示，Qt 会安排布局更新；动态复杂界面中可调用 `updateGeometry()` 通知父布局重新读取尺寸信息。

```cpp
editor->updateGeometry();
```

## 3. 先理解 Policy：每个方向各有一套规则

一个 QSizePolicy 同时保存：

- 水平方向 policy；
- 垂直方向 policy；
- 水平/垂直 stretch；
- 宽高是否互相依赖；
- 隐藏时是否保留空间；
- 控件类型提示。

因此，下面的配置很常见：

```cpp
QSizePolicy(
    QSizePolicy::Expanding,
    QSizePolicy::Fixed);
```

它表达“横向尽量利用额外空间，纵向保持正常高度”，常用于 `QLineEdit`、内容编辑区或工具栏中的可扩展字段。

### 3.1 七种尺寸策略

| Policy | sizeHint 的含义 | 能变小 | 能变大 | 典型场景 |
| --- | --- | --- | --- | --- |
| `Fixed` | 唯一可接受大小 | 否 | 否 | 按钮的垂直方向 |
| `Minimum` | 足够且最小的大小 | 否 | 可以，但没有额外收益 | 按钮的水平方向 |
| `Maximum` | 可接受的最大大小 | 可以 | 否 | 分隔线等可压缩内容 |
| `Preferred` | 最合适，但可调整 | 可以 | 可以，但不特别需要 | 普通 QWidget 默认策略 |
| `Expanding` | 合适大小，但额外空间有价值 | 可以 | 可以，且应优先获得 | 滑块、编辑区、主要内容区 |
| `MinimumExpanding` | 当前是最小充分大小，额外空间有价值 | 否 | 可以，且应优先获得 | 不能比 hint 小的主内容区 |
| `Ignored` | 忽略 sizeHint | 可以 | 可以，尽量占空间 | 由外部规则完全决定大小的特殊控件 |

`Minimum` 与 `MinimumExpanding` 的区别很关键：

- 两者都不应缩小到 size hint 以下；
- `MinimumExpanding` 明确表示额外空间对它有价值，因此会在布局协商中更积极。

`Preferred` 与 `Expanding` 的区别也很关键：

- 两者都可以缩小和变大；
- `Expanding` 表示“请优先把多余空间给我”。

不要滥用 `Ignored`。忽略 size hint 可能让控件在极端窗口尺寸下变得不符合内容需要；它应是非常明确的布局设计选择。

## 4. PolicyFlag：Policy 的底层组成

`Policy` 本质上由 flags 组合而成，业务代码通常选择 `Policy` 枚举即可，不必手工组合 flags。

| Flag | 含义 |
| --- | --- |
| `GrowFlag` | 可以超过 size hint 增长 |
| `ExpandFlag` | 能有效利用额外空间，应优先参与扩展 |
| `ShrinkFlag` | 空间不够时可以小于 size hint |
| `IgnoreFlag` | 忽略 size hint |

它们主要用于理解 policy 行为或实现自定义控件，不是日常设置 API。

## 5. QSizePolicy stretch 与布局 stretch 的关系

`QSizePolicy` 自己也有水平和垂直 stretch，范围是 `0..255`：

```cpp
auto leftPolicy = leftPane->sizePolicy();
leftPolicy.setHorizontalStretch(2);
leftPane->setSizePolicy(leftPolicy);

auto rightPolicy = rightPane->sizePolicy();
rightPolicy.setHorizontalStretch(1);
rightPane->setSizePolicy(rightPolicy);
```

在同一水平布局中，两个相邻且允许扩展的控件可按 `2 : 1` 取得宽度比例。

但需要区分：

| 名称 | 设置位置 | 作用 |
| --- | --- | --- |
| `QBoxLayout::addWidget(widget, stretch)` | 某个布局的直接项目 | 当前布局主轴上的余量分配 |
| `QBoxLayout::setStretch()` | 某个布局的直接项目 | 修改当前布局主轴权重 |
| `QSizePolicy::setHorizontalStretch()` | QWidget 自身 | 控件的水平尺寸偏好 |
| `QSizePolicy::setVerticalStretch()` | QWidget 自身 | 控件的垂直尺寸偏好 |

对于一个明确的 `QBoxLayout`，优先用布局的 stretch API，因为它把权重写在实际布局关系旁边。QSizePolicy stretch 更适合控件在多个布局上下文中都应保持某种偏好，或实现自定义控件时声明默认行为。

## 6. 宽高依赖：自动换行为何能长高

某些控件的推荐高度取决于宽度。自动换行 QLabel 是最常见的例子：

```cpp
auto *label = new QLabel(longText);
label->setWordWrap(true);
```

窗口变窄后，文字行数变多，布局必须为 label 分更多高度。QSizePolicy 用标志声明这件事：

```cpp
policy.setHeightForWidth(true);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 宽高依赖 | `hasHeightForWidth()` | 查询控件推荐高度是否依赖分配到的宽度 | Widgets 布局中最常见；仅有 policy 标志不够，自定义控件还要实现 `heightForWidth()` |
| 宽高依赖 | `setHeightForWidth(bool)` | 设置 height-for-width 标志 | 用于自动换行标签等“越窄越高”的控件；改变后通常需要触发布局重新计算 |
| 宽高依赖 | `hasWidthForHeight()` | 查询宽度是否依赖分配到的高度 | Widgets 布局通常不使用，主要由 `QGraphicsLayout` 子类支持 |
| 宽高依赖 | `setWidthForHeight(bool)` | 设置 width-for-height 标志 | 不要和 height-for-width 同时作为普通 Widgets 方案使用，容易形成无法求解的尺寸关系 |

在 Widgets 布局中，常用的是 height-for-width。width-for-height 仅由 `QGraphicsLayout` 子类支持；同时启用两种依赖不可行。

自定义 QWidget 不能只设置 policy 标志，还应正确实现 `hasHeightForWidth()`、`heightForWidth()` 与 size hint，布局才能得到真实高度。

## 7. 控件类型：为 style 提供语义

`ControlType` 不决定控件能否伸缩。它是给 Qt style 的语义提示，用于计算不同控件之间更恰当的间距。

例如某些平台风格会让按钮之间、单选按钮之间使用不同标准距离。普通 QWidget 会自动提供合适的 control type；只有实现自定义控件或自定义布局/style 时，才有理由手动设置。

| ControlType | 表示的控件 |
| --- | --- |
| `DefaultType` | 未指定的默认类型 |
| `ButtonBox` | `QDialogButtonBox` |
| `CheckBox` | `QCheckBox` |
| `ComboBox` | `QComboBox` |
| `Frame` | `QFrame` |
| `GroupBox` | `QGroupBox` |
| `Label` | `QLabel` |
| `Line` | `QFrame::HLine` / `QFrame::VLine` |
| `LineEdit` | `QLineEdit` |
| `PushButton` | `QPushButton` |
| `RadioButton` | `QRadioButton` |
| `Slider` | `QAbstractSlider` |
| `SpinBox` | `QAbstractSpinBox` |
| `TabWidget` | `QTabWidget` |
| `ToolButton` | `QToolButton` |

`ControlTypes` 是 `QFlags<ControlType>`，可以保存多个 ControlType 的按位或组合。通常由 `QLayoutItem::controlTypes()` 汇总布局内项目后使用。

## 8. 隐藏时是否保留布局空间

默认情况下：

```cpp
widget->hide();
```

会让布局把原空间让给其它可见项目。

若不希望界面在隐藏控件时跳动：

```cpp
auto policy = widget->sizePolicy();
policy.setRetainSizeWhenHidden(true);
widget->setSizePolicy(policy);
```

此时隐藏控件不显示，但布局仍为它保留尺寸。

适合：

- 状态图标短暂隐藏但列表列宽不应跳动；
- 表格型工具面板切换状态时希望保持稳定；
- 动画期间需要保留空间。

不适合：

- “高级选项”收起后希望其它控件向上填补；
- 临时隐藏区域应彻底让出空间；
- 需要减少窗口最小高度的场景。

## 9. 转置策略

当同一控件从横向用法变成纵向用法时，可以交换 policy 和 stretch：

```cpp
QSizePolicy policy = widget->sizePolicy();
policy.transpose();
widget->setSizePolicy(policy);
```

`transpose()` 原地修改；`transposed()` 返回修改后的副本：

```cpp
const QSizePolicy verticalPolicy = widget->sizePolicy().transposed();
```

这只交换水平/垂直 policy 与 stretch，不会旋转控件、不会改变 size hint，也不会自动更改布局方向。

## 10. 常见误区与排查

### 10.1 设置 `Expanding` 后控件仍不变大

检查：

1. 父布局是否真的有剩余空间；
2. 控件是否被最大尺寸或 `setFixedWidth()` 限制；
3. 同级项目是否有更高的 QBoxLayout stretch；
4. 当前布局主轴是否与期望方向一致；
5. 控件是否真的已调用 `setSizePolicy()` 应用修改。

### 10.2 把 `Preferred` 当成“固定推荐尺寸”

`Preferred` 可以缩小也可以变大，只是 size hint 是最理想的尺寸。需要强限制时组合最小/最大尺寸，或在确实必要时使用 `Fixed`。

### 10.3 用 QSizePolicy 替代布局结构

policy 只能声明单个控件的尺寸意愿，不能表达“按钮靠右”“两列对齐”“标题在顶部”。这些结构问题仍应由 QBoxLayout、QGridLayout、QFormLayout 等解决。

### 10.4 隐藏控件后仍然占位

检查 `retainSizeWhenHidden()` 是否为 true。它默认 false，但可能被 Designer、自定义控件或旧代码修改。

### 10.5 只设置 height-for-width 标志

必须同时提供对应的 `heightForWidth()` 实现与合理的 size hint；否则布局只知道存在依赖，却得不到正确高度。

## API 速查表
### 11.1 类型与枚举

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QSizePolicy::ControlType` | 为 style 提供控件语义。 | 不负责伸缩；普通 QWidget 通常自动提供正确类型。 |
| 标志 | `QSizePolicy::ControlTypes` | `ControlType` 的按位或组合。 | 布局项汇总控件类型时使用；业务代码很少手工创建。 |
| 控件类型 | `DefaultType` | 未指定的默认控件类型。 | 自定义控件没有更合适语义时使用。 |
| 控件类型 | `ButtonBox` / `CheckBox` / `ComboBox` | 对话框按钮盒、复选框、下拉框语义。 | 主要供 style 计算控件间距。 |
| 控件类型 | `Frame` / `GroupBox` / `Label` / `Line` | 框架、分组框、标签、分隔线语义。 | 自定义控件应选择与视觉功能最接近的类型。 |
| 控件类型 | `LineEdit` / `PushButton` / `RadioButton` | 输入框、按钮、单选按钮语义。 | 影响部分 style 的标准间距。 |
| 控件类型 | `Slider` / `SpinBox` / `TabWidget` / `ToolButton` | 滑块、数值框、标签页、工具按钮语义。 | 同上；一般不需要手工设置。 |
| 枚举 | `QSizePolicy::Policy` | 定义每个方向的增长、收缩与 size hint 处理策略。 | 水平和垂直独立设置。 |
| 策略 | `Fixed` | 不能增长或收缩。 | 只在尺寸确实不可变时使用。 |
| 策略 | `Minimum` | 不能小于 size hint，可变大但不特别需要。 | 按钮宽度等“够用即可”的方向。 |
| 策略 | `Maximum` | 可缩小但不能超过 size hint。 | 分隔线或可随时让出空间的内容。 |
| 策略 | `Preferred` | size hint 最理想，可变大也可变小。 | 普通 QWidget 默认策略。 |
| 策略 | `Expanding` | 可变大可变小，且应优先获得额外空间。 | 主编辑区、滑块、主要内容区。 |
| 策略 | `MinimumExpanding` | 不能小于 hint，且应优先获得额外空间。 | 最小可用尺寸明确的主内容区。 |
| 策略 | `Ignored` | 忽略 size hint，尽可能占用空间。 | 特殊布局设计；不要作为默认选择。 |
| 枚举 | `QSizePolicy::PolicyFlag` | Policy 的底层组合标志。 | 理解或扩展 policy 时使用，日常直接选择 `Policy`。 |
| 标志 | `GrowFlag` | 可超过 size hint 增长。 | Policy 内部语义。 |
| 标志 | `ExpandFlag` | 能有效利用额外空间。 | 决定 `expandingDirections()` 是否包含该方向。 |
| 标志 | `ShrinkFlag` | 可小于 size hint 收缩。 | 空间不足时允许让步。 |
| 标志 | `IgnoreFlag` | 忽略 size hint。 | 对应 `Ignored` 策略。 |

### 11.2 构造、查询与设置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QSizePolicy()` | 创建水平和垂直均为 `Fixed` 的 policy。 | 默认 policy 不等于大多数控件的默认 policy；通常从 QWidget 读取现有 policy 再修改。 |
| 构造函数 | `QSizePolicy(Policy horizontal, Policy vertical, ControlType type = DefaultType)` | 用指定横向、纵向策略和控件类型创建 policy。 | 构造后再设给 QWidget；必要时继续设置 stretch 或宽高依赖。 |
| 查询 | `ControlType controlType() const` | 返回当前控件类型提示。 | 主要供 style/自定义控件使用。 |
| 查询 | `Qt::Orientations expandingDirections() const` | 返回控件能有效使用额外空间的方向。 | 只有 `Expanding` 或 `MinimumExpanding` 会报告相应方向。 |
| 查询 | `bool hasHeightForWidth() const` | 返回推荐高度是否依赖宽度。 | 自动换行/流式内容的重要提示。 |
| 查询 | `bool hasWidthForHeight() const` | 返回宽度是否依赖高度。 | Widgets 中很少使用；主要针对 QGraphicsLayout。 |
| 查询 | `Policy horizontalPolicy() const` | 返回水平尺寸策略。 | 排查控件为何不愿变宽时读取。 |
| 查询 | `int horizontalStretch() const` | 返回水平 stretch，范围为 `0..255`。 | 与同级控件比较相对权重。 |
| 查询 | `bool retainSizeWhenHidden() const` | 返回隐藏控件时是否保留其布局空间。 | 默认 false；排查隐藏后仍占位时检查。 |
| 设置 | `void setControlType(ControlType type)` | 设置控件类型提示。 | 自定义控件需要 style 间距语义时使用。 |
| 设置 | `void setHeightForWidth(bool dependent)` | 设置高度是否依赖宽度。 | 还必须实现控件实际的 `heightForWidth()`。 |
| 设置 | `void setHorizontalPolicy(Policy policy)` | 设置水平尺寸策略。 | 常用于让编辑区 `Expanding`、按钮保持 `Minimum`。 |
| 设置 | `void setHorizontalStretch(int stretchFactor)` | 设置水平 stretch。 | 有效范围 `0..255`；明确布局关系时优先用 layout stretch。 |
| 设置 | `void setRetainSizeWhenHidden(bool retainSize)` | 设置隐藏时是否保留空间。 | 需要避免布局跳动时设 true；可收起区域通常保持 false。 |
| 设置 | `void setVerticalPolicy(Policy policy)` | 设置垂直尺寸策略。 | 主编辑区常为 `Expanding`，按钮高度常为 `Fixed`。 |
| 设置 | `void setVerticalStretch(int stretchFactor)` | 设置垂直 stretch。 | 有效范围 `0..255`；在纵向布局中与同级项目比较。 |
| 设置 | `void setWidthForHeight(bool dependent)` | 设置宽度是否依赖高度。 | 只受 QGraphicsLayout 子类支持，不能与 height-for-width 同时使用。 |
| 转置 | `void transpose()` | 原地交换水平/垂直 policy 与 stretch。 | 控件横竖使用场景互换时使用，不改变控件或布局方向。 |
| 转置 | `QSizePolicy transposed() const` | 返回交换水平/垂直信息后的副本。 | 想保留原 policy 时使用。 |
| 查询 | `Policy verticalPolicy() const` | 返回垂直尺寸策略。 | 排查控件为何不愿变高时读取。 |
| 查询 | `int verticalStretch() const` | 返回垂直 stretch，范围为 `0..255`。 | 与同级控件比较高度余量权重。 |
| 转换 | `operator QVariant() const` | 把 QSizePolicy 包装为 QVariant。 | 属性系统、通用数据容器或动态属性传递时使用。 |
| 比较 | `bool operator==(const QSizePolicy &other) const` | 判断两个 policy 的所有状态是否相同。 | 缓存、测试或条件更新时使用。 |
| 比较 | `bool operator!=(const QSizePolicy &other) const` | 判断两个 policy 是否不同。 | 与 `operator==` 相反。 |

### 11.3 相关非成员

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 哈希 | `size_t qHash(QSizePolicy key, size_t seed = 0)` | 计算 QSizePolicy 的哈希值。 | 把 QSizePolicy 作为哈希键时由 Qt 容器使用。 |
| 序列化 | `QDataStream &operator<<(QDataStream &stream, const QSizePolicy &policy)` | 将 policy 写入 QDataStream。 | 二进制持久化时注意 stream 版本兼容。 |
| 反序列化 | `QDataStream &operator>>(QDataStream &stream, QSizePolicy &policy)` | 从 QDataStream 读回 policy。 | 数据来源需可信且读写双方的 stream 格式匹配。 |
| 调试输出 | `QDebug operator<<(QDebug dbg, const QSizePolicy &policy)` | 将 policy 写入 Qt 调试流。 | 排查布局问题时可直接 `qDebug() << widget->sizePolicy()`；依赖 debug stream 配置。 |

## 12. 继续学习

1. `QWidget`：控件自身如何提供 size hint、最小/最大尺寸和 `updateGeometry()`。
2. `QLayoutItem`：布局如何读取 policy 并把它转化为尺寸协商。
3. `QBoxLayout`：stretch、margin、spacing 如何共同作用。
4. `QFormLayout`、`QGridLayout`：二维和表单布局怎样利用控件的尺寸偏好。

### 一句话总结

`QSizePolicy` 是控件给布局系统的一份“尺寸意愿声明”：它分别描述横向和纵向能否增长、能否收缩、额外空间是否有价值，并携带宽高依赖、隐藏占位和控件类型信息。它要与 size hint、最小/最大尺寸及具体布局的 stretch 一起理解，不能单独替代布局结构。
