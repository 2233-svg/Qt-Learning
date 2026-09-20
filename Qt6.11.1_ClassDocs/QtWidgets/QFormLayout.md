# QFormLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QFormLayout`

## 1. 先建立直觉

### 这是什么

`QFormLayout` 是专门为“标签 + 字段”界面准备的布局。它不像 `QGridLayout` 那样要求你手动维护所有行列规则，而是把每一行理解成一个表单项：左边是说明这个字段含义的 label，右边是可编辑或可展示的 field。

它的价值不只是少写几行 `addWidget()`。`QFormLayout` 会根据平台 style 决定标签对齐、字段增长、行是否换行、默认间距，并且 `addRow(QString, QWidget*)` 会自动创建 `QLabel` 和 buddy 关系，让快捷键、可访问性和键盘导航更自然。

### 适合使用的场景

- 设置页、属性页、连接配置、导出选项等“字段说明 + 输入控件”界面。
- 标签列需要统一对齐，字段列需要按平台风格增长。
- 需要在窄窗口下把字段换到标签下方。
- 需要动态隐藏某几行配置，而不是删除后重建整个表单。

### 不适合的场景

- 任意二维排布用 `QGridLayout` 更直接。
- 一行工具按钮或左右分栏用 `QHBoxLayout`。
- 数据表格展示不是表单布局职责，应使用模型/视图。
- 每行有多个复杂区域时，可以让 field 是一个子布局，但如果每行结构差异很大，表单布局可能不再是最清楚的表达。

### 最小示例

```cpp
auto *form = new QFormLayout(parent);
form->addRow(tr("&Name:"), nameEdit);
form->addRow(tr("&Port:"), portSpinBox);
form->addRow(tr("Use TLS:"), tlsCheckBox);
form->setFieldGrowthPolicy(QFormLayout::AllNonFixedFieldsGrow);
```

带 `&` 的标签文本会给自动创建的 `QLabel` 设置快捷键，并把对应字段设为 buddy。

## 2. 依赖与对象关系

- 头文件：`#include <QFormLayout>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QLayout`
- 直接派生类：类页未列出

### 行与角色

每一行最多有三种角色：`LabelRole`、`FieldRole`、`SpanningRole`。普通字段行使用 label + field 两列；说明文字、分隔区域、按钮组等可以用 spanning row 横跨两列。

这和 `QGridLayout` 的任意行列不同。`QFormLayout` 的结构更受约束，但也因此更适合平台一致的表单。

### 标签伙伴关系

使用 `addRow(const QString &labelText, QWidget *field)` 时，Qt 会创建 `QLabel`，并把 field 设为 label 的 buddy。用户可以通过标签快捷键把焦点跳到字段上，这对键盘用户和可访问性都很重要。

如果你自己传入 label widget，要自己决定是否调用 `QLabel::setBuddy()`。

### 所有权

加入表单的控件和子布局由 Qt 父子关系与布局系统管理。`removeRow()` 会移除并删除该行项目；`takeRow()` 会移除但把项目交还给调用方，适合移动或复用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `struct TakeRowResult` | `takeRow()` 的返回结果，保存取出的 label 和 field item。 |
| `enum FieldGrowthPolicy` | 控制字段列如何随表单变宽而增长。 |
| `enum ItemRole` | 标识一行中的 label、field 或跨列项目。 |
| `enum RowWrapPolicy` | 控制窄空间下字段是否换到标签下方。 |
| `fieldGrowthPolicy : FieldGrowthPolicy` | 字段增长策略。 |
| `formAlignment : Qt::Alignment` | 整个表单内容在可用区域内的对齐方式。 |
| `labelAlignment : Qt::Alignment` | 标签列内部的文本/控件对齐方式。 |
| `rowWrapPolicy : RowWrapPolicy` | 行换行策略。 |
| `horizontalSpacing : int` | 标签列和字段列之间的水平间距。 |
| `verticalSpacing : int` | 行与行之间的垂直间距。 |
| `QFormLayout(QWidget *parent)` | 创建表单布局，可直接安装到父控件。 |
| `~QFormLayout()` | 销毁表单布局。 |
| `addRow(...)` | 在末尾添加字段行或跨列行。 |
| `insertRow(...)` | 在指定行插入字段行或跨列行。 |
| `setWidget(row, role, widget)` | 在指定行和角色位置设置控件。 |
| `setLayout(row, role, layout)` | 在指定行和角色位置设置子布局。 |
| `setItem(row, role, item)` | 在指定行和角色位置设置底层布局项。 |
| `itemAt(row, role) const` | 按行和角色取布局项。 |
| `itemAt(index) const` | 按布局项索引取项目。 |
| `getItemPosition(index, row, role)` | 按索引反查行和角色。 |
| `getWidgetPosition(widget, row, role)` | 按控件反查行和角色。 |
| `getLayoutPosition(layout, row, role)` | 按子布局反查行和角色。 |
| `labelForField(QWidget *field)` | 查找某字段对应的标签控件。 |
| `labelForField(QLayout *field)` | 查找某字段布局对应的标签控件。 |
| `rowCount() const` | 返回表单行数。 |
| `removeRow(...)` | 删除一行及其布局项。 |
| `takeRow(...)` | 取出一行并把 item 所有权交给调用方。 |
| `setRowVisible(...)` / `isRowVisible(...)` | Qt 6.4 起按行、控件或布局显示/隐藏表单行。 |
| `setFieldGrowthPolicy(...)` / `fieldGrowthPolicy()` | 设置或读取字段增长策略。 |
| `setFormAlignment(...)` / `formAlignment()` | 设置或读取表单整体对齐。 |
| `setLabelAlignment(...)` / `labelAlignment()` | 设置或读取标签对齐。 |
| `setRowWrapPolicy(...)` / `rowWrapPolicy()` | 设置或读取行换行策略。 |
| `setHorizontalSpacing(...)` / `horizontalSpacing()` | 设置或读取水平间距。 |
| `setVerticalSpacing(...)` / `verticalSpacing()` | 设置或读取垂直间距。 |
| `setSpacing(int)` / `spacing() const` | 同时设置或读取通用间距。 |
| `count()` / `takeAt(index)` | 遍历或移除底层布局项。 |
| `setGeometry(const QRect &rect)` | 重新计算所有行的实际几何。 |
| `sizeHint()` / `minimumSize()` | 汇总表单推荐尺寸和最小尺寸。 |
| `hasHeightForWidth()` / `heightForWidth(int)` | 支持换行策略下的宽度影响高度。 |
| `expandingDirections()` / `invalidate()` | 汇总扩展方向、使布局缓存失效。 |

## 4. API 逐项说明

### `enum QFormLayout::FieldGrowthPolicy`

字段增长策略决定右侧字段列在表单变宽时如何扩展。

- `FieldsStayAtSizeHint`：字段保持接近推荐宽度，常见于 macOS 风格。
- `ExpandingFieldsGrow`：只有 size policy 允许扩展的字段增长。
- `AllNonFixedFieldsGrow`：所有非固定字段都尽量增长，许多桌面风格下更常见。

如果你希望输入框、下拉框、路径选择器填满可用宽度，通常选择 `AllNonFixedFieldsGrow` 或确保字段本身的 horizontal size policy 是 expanding。

### `enum QFormLayout::ItemRole`

`LabelRole` 表示标签列，`FieldRole` 表示字段列，`SpanningRole` 表示跨两列的项目。跨列行适合放说明文字、分组标题、错误提示或按钮行。

不要把多个互不相关的控件硬塞进同一个 field；如果它们共同构成一个字段，可以放在子布局里作为 field。

### `enum QFormLayout::RowWrapPolicy`

行换行策略决定空间不足时 label 和 field 如何排布。

- `DontWrapRows`：字段始终在标签旁边。
- `WrapLongRows`：空间不足时过长行换行。
- `WrapAllRows`：所有字段都放到标签下方。

窄侧栏、移动尺寸窗口或翻译文本较长的界面，`WrapLongRows` 往往比固定宽度更稳。需要上下结构的设置页可以直接用 `WrapAllRows`。

### `fieldGrowthPolicy`

读取或设置字段列增长策略。这个属性影响的是字段区域如何吃掉额外宽度，不改变标签列本身含义。

如果表单变宽但输入框不变宽，先看这个策略，再看字段控件的 `QSizePolicy`。

### `formAlignment`

控制整个表单内容在布局几何中的位置。例如表单不愿意横向填满时，可以居中或靠左。

它不是标签文本对齐；标签对齐由 `labelAlignment` 控制。

### `labelAlignment`

控制标签在标签列中的对齐方式。不同平台默认不同：有些风格偏向右对齐标签以贴近字段，有些偏向左对齐以便阅读。

跨平台应用若追求原生观感，少改这个值；若追求产品统一视觉，可以显式设置。

### `rowWrapPolicy`

控制行是否换行。启用换行后，表单高度可能随宽度变化，这也是 `hasHeightForWidth()` 相关 API 有意义的原因。

设置换行策略时要检查对话框最小宽度，不要让表单在临界宽度附近频繁跳变导致视觉抖动。

### `horizontalSpacing` / `verticalSpacing`

水平间距通常是标签和字段之间的距离，垂直间距是行距。未显式设置时使用父布局或 style 默认值。

表单里不建议通过插入空白行来调普通行距；使用 vertical spacing 更一致。

### `QFormLayout(QWidget *parent = nullptr)`

创建表单布局。传入父控件时直接安装为顶层布局；不传时可加入外层布局。

表单通常作为页面中的一个区块存在，因此也经常被放进 `QVBoxLayout` 或 `QGroupBox` 内。

### `~QFormLayout()`

销毁布局。普通业务代码无需直接调用析构，但动态移除表单区块时要明确控件是否仍会被复用。

### `addRow(...)`

在末尾添加一行。重载分三类：传 label 和 field，传一个跨列 widget/layout，或传字符串让 Qt 自动创建 label。

最推荐字段表单使用字符串重载：

```cpp
form->addRow(tr("&User name:"), userNameEdit);
```

这样会自动建立 `QLabel` 与字段控件的 buddy 关系。若 field 是一个子布局，字符串重载会创建标签，但 buddy 关系无法像单个 widget 那样直接指向具体输入控件，需要你自己处理焦点逻辑。

### `insertRow(...)`

和 `addRow()` 类似，但插入到指定行。`row` 超出范围时通常追加到末尾。

动态配置页中，插入行比重建整个表单更平滑。不过插入后后续行号会变化，保存行索引时要小心。

### `setWidget(int row, ItemRole role, QWidget *widget)`

在指定行和角色位置设置控件。`role` 可以是 `LabelRole`、`FieldRole` 或 `SpanningRole`。

如果目标位置已有项目，应先清楚旧项目如何处理。表单布局不会替你决定旧控件的业务生命周期。

### `setLayout(int row, ItemRole role, QLayout *layout)`

在指定位置设置子布局。常见用法是字段区域由多个控件组成，例如路径输入框加浏览按钮。

把子布局放到 `LabelRole` 通常不常见；大多数情况下它应该作为 `FieldRole` 或 `SpanningRole`。

### `setItem(int row, ItemRole role, QLayoutItem *item)`

底层设置入口，适合 spacer 或自定义 item。普通控件和子布局应优先使用 `setWidget()`、`setLayout()`。

传入后 item 所有权交给表单布局。

### `itemAt(int row, ItemRole role) const` / `itemAt(int index) const`

前者按表单语义查行和角色，后者按底层布局项索引查项目。表单代码优先使用行/角色版本，可读性更好。

底层 index 会受 label、field、spanning row 的内部排列影响，不适合作为长期业务标识。

### `getItemPosition()` / `getWidgetPosition()` / `getLayoutPosition()`

这些函数用于反查某个 item、widget 或 layout 位于哪一行、哪个角色。找不到时行号会设为 `-1`。

它们适合动态表单：从某个字段控件出发，定位整行，然后隐藏、移除或插入邻近行。

### `labelForField(QWidget *field)` / `labelForField(QLayout *field)`

返回字段对应的标签控件。自动字符串重载添加的行可以通过它拿回标签，便于设置提示、禁用、样式或可访问性文本。

返回类型是 `QWidget *`，实际通常是 `QLabel *`，需要时再安全转换。

### `rowCount() const`

返回表单行数。它统计的是表单逻辑行，不是底层 item 数量；一行 label+field 仍算一行。

这比 `count()` 更适合业务代码理解表单规模。

### `removeRow(...)`

按行号、字段控件或子布局移除整行并删除相关布局项。它适合永久移除某个配置项。

如果只是临时隐藏高级选项，Qt 6.4 起优先用 `setRowVisible(false)`，保留行结构更简单。

### `takeRow(...)`

按行号、字段控件或子布局取出整行，返回 `TakeRowResult`。取出后项目不再属于表单布局，调用方负责处理返回的 label item 和 field item。

它适合把某行移动到别处，或在不删除控件的情况下重组表单。

### `struct TakeRowResult`

`TakeRowResult` 保存 `takeRow()` 取出的两个布局项，通常是 `labelItem` 和 `fieldItem`。跨列行一般只会有对应的 spanning item。

拿到结果后，要检查指针是否为空，并决定里面的 widget/layout 如何继续使用或销毁。

### `setRowVisible(...)` / `isRowVisible(...)`

Qt 6.4 起可以按行号、字段控件或字段布局显示/隐藏整行。这比逐个隐藏 label 和 field 更不容易漏掉一半。

它适合“高级选项展开/收起”“根据复选框显示额外字段”“不同连接类型显示不同配置项”等场景。

### `setFieldGrowthPolicy()` / `fieldGrowthPolicy()`

设置或读取字段增长策略。字段列不伸展时，检查这里；字段过度伸展时，也检查这里。

策略和单个字段的 size policy 会共同决定结果。

### `setFormAlignment()` / `formAlignment()`

设置或读取表单整体对齐。表单内容小于可用区域时才明显。

这适合小型设置面板居中显示，或让表单靠上靠左保持桌面软件的扫描习惯。

### `setLabelAlignment()` / `labelAlignment()`

设置或读取标签对齐。右对齐有利于字段紧凑配对，左对齐有利于长标签阅读。

如果多语言环境中标签长度差异大，左对齐加合理换行可能比强行右对齐更稳。

### `setRowWrapPolicy()` / `rowWrapPolicy()`

设置或读取行换行策略。它直接影响窄窗口下表单是否保持两列，还是变成上下结构。

宽桌面设置页通常用 `DontWrapRows`；可调整宽度的小对话框可以考虑 `WrapLongRows`。

### `setHorizontalSpacing()` / `horizontalSpacing()` / `setVerticalSpacing()` / `verticalSpacing()` / `setSpacing()` / `spacing()`

分别控制水平、垂直或通用间距。两个方向间距不同时，通用 `spacing()` 可能不能代表真实状态。

想让表单更紧凑，先调 spacing 和 margins；不要用负边距或固定坐标。

### `count()` / `takeAt(int index)`

底层布局遍历接口。`count()` 统计布局项，不是行数；`takeAt()` 按底层索引取出项目，不按表单行取。

业务代码需要移除整行时，优先用 `takeRow()` 或 `removeRow()`。

### `setGeometry(const QRect &rect)` / `sizeHint()` / `minimumSize()`

这些函数由布局系统调用，用来计算和汇总表单几何。换行策略、字段增长策略、label 最宽值、spacing 都会影响结果。

应用代码通常不直接调用；调试尺寸问题时，可以通过它们理解表单为什么需要某个宽高。

### `hasHeightForWidth()` / `heightForWidth(int width)`

当行换行启用或字段内容高度依赖宽度时，表单高度会随宽度变化。这组函数把这种关系报告给父布局。

如果表单放在滚动区域里，高度随宽度变化尤其常见，要确保父容器也能正确处理重新布局。

### `expandingDirections()` / `invalidate()`

`expandingDirections()` 描述表单整体是否愿意扩展；`invalidate()` 让缓存尺寸失效。改变行、策略、间距或子控件内容后，Qt 通常会自动处理。

自定义动态表单在大量变更后如布局没有及时刷新，可以调用 `invalidate()` 或父控件的 `updateGeometry()`。

## 5. 深入实践与常见坑

### 字符串重载的价值被低估

`addRow(tr("&Name:"), edit)` 不只是少写一个 `QLabel`。它同时建立标签、文本、快捷键和 buddy 关系。对表单这种高频输入界面，这些细节很重要。

### 隐藏行不要只 hide 字段

只隐藏 field 会留下 label 或空行。Qt 6.4 以后用 `setRowVisible()`；旧版本则要同时处理 label 和 field，必要时使用 `takeRow()`。

### 表单不是万能网格

当一行里有三个以上逻辑字段，或多列之间没有明确 label/field 关系时，继续用 `QFormLayout` 会让角色语义变别扭。此时换 `QGridLayout` 更直接。

### 字段不扩展通常不是布局坏了

先看 `fieldGrowthPolicy`，再看字段控件的 horizontal size policy，最后看外层布局是否给了表单足够宽度。三个条件缺一，输入框都可能不按预期变宽。
