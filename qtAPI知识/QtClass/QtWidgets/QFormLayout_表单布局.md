# Qt QFormLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QFormLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QLayout -> QFormLayout`  
> 定位：带有“标签 - 字段”语义的两列表单布局

## 1. QFormLayout 解决什么问题

设置页、属性页和登录表单经常有这种结构：

```text
用户名： [________________]
端口：   [____]
启用代理： [x]
          [测试连接]          <- 独占一行
```

用 `QGridLayout` 当然也能做，但你必须自己记住标签在哪一列、输入控件在哪一列、标签是否要设 buddy、窄窗口怎样换行。`QFormLayout` 把这套约定直接做成布局规则：

- 左列是 `LabelRole`，右列是 `FieldRole`；
- 单独添加的 widget 或 layout 使用 `SpanningRole`，横跨两列；
- `addRow("名称：", editor)` 自动创建 `QLabel`，并把 `editor` 设为它的 buddy；
- 可以按 style 自动决定标签对齐、字段是否扩展，以及窗口变窄时是否换行。

它适合“字段名对应一个输入项”的界面；需要任意行列跨度、复杂表格或仪表盘时，使用 `QGridLayout` 更自然。它也不是数据模型：表单数据仍由 `QLineEdit`、`QSpinBox`、`QCheckBox` 等控件保存。

```text
QLayout
  ├─ QBoxLayout       一维排列
  ├─ QGridLayout      任意二维网格
  └─ QFormLayout      标签列 + 字段列 + 可选跨列行
```

## 2. 最小可用示例：一个连接设置页

```cpp
#include <QApplication>
#include <QCheckBox>
#include <QFormLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QSpinBox>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *form = new QFormLayout(&window);

    auto *hostEdit = new QLineEdit;
    auto *portSpin = new QSpinBox;
    portSpin->setRange(1, 65535);
    portSpin->setValue(443);

    auto *proxyCheck = new QCheckBox("使用系统代理");
    auto *testButton = new QPushButton("测试连接");

    form->addRow("&主机：", hostEdit);
    form->addRow("&端口：", portSpin);
    form->addRow(proxyCheck);       // 跨两列
    form->addRow(testButton);       // 跨两列

    window.setWindowTitle("连接设置");
    window.resize(360, 180);
    window.show();
    return app.exec();
}
```

`"&主机："` 中的 `&` 是助记符。这个重载会创建 `QLabel` 并自动调用 `label->setBuddy(hostEdit)`：用户按 `Alt+主` 时，焦点会移到 `hostEdit`。手工传入 `QWidget *label` 的重载不会替你建立 buddy 关系，需要时自己调用 `QLabel::setBuddy()`。

构造 `QFormLayout(&window)` 会立刻把它安装为 `window` 的顶层布局，等价于随后调用 `window.setLayout(form)`。一个 `QWidget` 只能有一个顶层布局。

## 3. 一行到底长什么样

普通行不是“第 0、1 列”这种纯坐标概念，而是有角色的布局项：

```text
row 0: LabelRole  -> QLabel("主机：")
       FieldRole  -> QLineEdit

row 1: LabelRole  -> QLabel("端口：")
       FieldRole  -> QSpinBox

row 2: SpanningRole -> QCheckBox("使用系统代理")
```

`LabelRole` 与 `FieldRole` 是同一行的两部分；`SpanningRole` 表示该项占据两列。不要在同一行同时混用跨列项和两列项。若目标单元格已有内容，`setWidget()`、`setLayout()` 或 `setItem()` 不会替换它，Qt 会输出错误并拒绝插入。

`rowCount()` 返回的是逻辑行数，而 `count()` 返回的是内部 `QLayoutItem` 数量。因此，一行标签加字段通常令 `count()` 增加 2，一条跨列行通常增加 1；不要把两者混为一谈。

## 4. 字段为什么有时会拉伸，有时不拉伸

表单剩余宽度如何处理由 `FieldGrowthPolicy` 和字段自身的 `QSizePolicy` 共同决定。

| 策略 | 行为 | 适合什么情况 |
| --- | --- | --- |
| `FieldsStayAtSizeHint` | 字段不会长到超过有效 `sizeHint()`。 | macOS 风格、紧凑偏好页。 |
| `ExpandingFieldsGrow` | 水平 policy 为 `Expanding` 或 `MinimumExpanding` 的字段填充剩余宽度，其他字段维持 size hint。 | 有输入框也有固定按钮、下拉框的常规窗口。 |
| `AllNonFixedFieldsGrow` | 所有允许增长的字段填充剩余宽度。 | 希望字段列尽可能整齐铺满的设置页。 |

```cpp
form->setFieldGrowthPolicy(QFormLayout::ExpandingFieldsGrow);
```

默认策略由应用 style 决定，不能把某个桌面平台的默认行为当成跨平台契约。若没有字段可以增长，剩余空间会按 `formAlignment` 放置整张表单。

这里的“能否增长”来自字段的 `QSizePolicy`。例如 `QLineEdit` 默认很适合占满字段列；一个 `QPushButton` 通常只保留合适宽度。想固定某个字段时，应先考虑其 `QSizePolicy` 或最小/最大尺寸，而不是误以为 `QFormLayout` 会无条件拉伸所有控件。

## 5. 窄窗口：并排、长行换行、全部上下排列

`rowWrapPolicy` 决定标签与字段在宽度不足时的关系：

| 策略 | 布局结果 | 使用场景 |
| --- | --- | --- |
| `DontWrapRows` | 标签始终在字段左侧。 | 桌面设置对话框，横向空间充足。 |
| `WrapLongRows` | 标签列先满足最宽标签；某行的标签加字段最小宽度放不下时，字段落到下一行。 | 可缩窄面板、平板或需要兼顾桌面和窄窗口的表单。 |
| `WrapAllRows` | 每个标签始终位于字段上方。 | 手机式窄栏、字段很宽或标签文本较长的界面。 |

```cpp
form->setRowWrapPolicy(QFormLayout::WrapLongRows);
```

`WrapLongRows` 不等于每一行都会变成上下结构；它只在该行的最小宽度不能容纳时换行。翻译后的标签可能更长，所以有多语言需求时，至少在目标语言下测试窗口最小宽度。

## 6. 对齐与间距：它们调的不是一回事

```cpp
form->setLabelAlignment(Qt::AlignRight | Qt::AlignVCenter);
form->setFormAlignment(Qt::AlignLeft | Qt::AlignTop);
form->setHorizontalSpacing(12);
form->setVerticalSpacing(8);
```

- `labelAlignment`：标签在左列自己的单元格里如何对齐，常用 `AlignLeft` 或 `AlignRight`。
- `formAlignment`：整张表单在布局可用矩形里如何放置。当字段没有把多余空间吃掉时，这个设置特别明显。
- `horizontalSpacing`：同一行标签与字段之间的距离。
- `verticalSpacing`：不同逻辑行之间的距离。
- `setSpacing(n)`：同时设置横向和纵向间距；随后 `spacing()` 只有在两者相等时才返回该值，否则返回 `-1`。

未显式设置横纵间距时，Qt 会从父布局或当前 style 的像素度量获取默认值。一般应保留这一机制，让界面跟随平台风格；只有需要统一设计规范时再覆盖。

## 7. 添加、插入和跨列行

```cpp
auto *credentials = new QFormLayout;
credentials->addRow("&账号：", new QLineEdit);
credentials->addRow("&密码：", new QLineEdit);

auto *advanced = new QCheckBox("显示高级选项");
credentials->addRow(advanced); // SpanningRole

credentials->insertRow(1, "&域：", new QLineEdit);
```

选择 API 的简单规则：

- 文字标签加字段：优先 `addRow(const QString &, QWidget *)` 或 `insertRow()` 对应重载，能获得自动创建的 `QLabel` 和 buddy。
- 已有标签对象：传 `QWidget *label`，适合富文本标签、带图标的自定义标签，或需要自己管理 buddy。
- 字段由多个控件组成：把一个嵌套 `QLayout` 放在 `FieldRole`；例如“起始时间 - 结束时间”可放一个 `QHBoxLayout`。
- 一整行开关、说明、按钮栏或分组标题：使用只有 `QWidget *` 或 `QLayout *` 参数的重载，使它跨两列。

`insertRow(row, ...)` 中 `row` 越界时，Qt 会追加到末尾，而不是报错。要插到最后，直接使用 `addRow()` 可读性更好。

## 8. 动态界面最容易出错的地方：隐藏、删除和取出

Qt 6.4 起，可直接隐藏一整行：

```cpp
form->setRowVisible(proxyCheck, false);
if (form->isRowVisible(proxyCheck)) {
    // 此行仍有可见项目
}
```

这适合“勾选高级模式后出现额外字段”的界面。`isRowVisible()` 的含义是该行中**有项目可见**，不是“标签和字段都可见”。

真正移除一行时，先区分两个 API：

```cpp
form->removeRow(portSpin); // 删除这一行中的标签、字段以及可能的嵌套布局

QFormLayout::TakeRowResult result = form->takeRow(0);
// result.labelItem 和 result.fieldItem 已脱离 layout；此函数不 delete 它们
```

- `removeRow()` 会删除该行占用的 widgets 和嵌套 layouts。调用后保留原始裸指针会成为悬空指针；需要观察对象是否已销毁可使用 `QPointer`。
- `takeRow()` 只把这一行的两个 `QLayoutItem *` 取出，不删除任何对象。调用者随后必须决定如何重新加入布局或删除 item 与它们承载的对象。
- `takeAt(index)` 只按内部项目索引取一个 `QLayoutItem`，并不等同于取一整行。想按行移动或复用内容，使用 `takeRow()`。

`TakeRowResult` 本身只有两个成员：`labelItem` 和 `fieldItem`。对跨列行，内容会出现在与其角色对应的结果项中；处理前先判空。

## 9. 用坐标式 API 构造或检查表单

绝大多数业务代码使用 `addRow()`、`insertRow()` 就够了。以下 API 主要服务于表单编辑器、运行时动态建表单，或需要检查既有布局的位置：

```cpp
int row = -1;
QFormLayout::ItemRole role;
form->getWidgetPosition(hostEdit, &row, &role);

if (role == QFormLayout::FieldRole) {
    QLayoutItem *label = form->itemAt(row, QFormLayout::LabelRole);
}
```

`setWidget()` 与 `setLayout()` 会在必要时补出空行；它们要求目标格为空。`setItem()` 接受的是已经构造好的 `QLayoutItem`，不能用它添加子 layout 或 widget item，官方明确建议分别使用 `setLayout()`、`setWidget()`。这三者适合“按行号填表”的程序化构造，不是普通表单的首选。

## API 速查表
### 10.1 成员类型与属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `FieldGrowthPolicy` | 指定字段列如何使用多余宽度。 | 用 `setFieldGrowthPolicy()` 显式消除平台 style 差异。 |
| 枚举值 | `FieldsStayAtSizeHint` | 字段不超过有效 size hint。 | 紧凑表单；默认于 `QMacStyle`。 |
| 枚举值 | `ExpandingFieldsGrow` | 只让水平可扩展的字段变宽。 | 常用的跨控件混排策略。 |
| 枚举值 | `AllNonFixedFieldsGrow` | 所有允许增长的字段变宽。 | 希望字段列充分利用宽度。 |
| 枚举 | `ItemRole` | 描述项目处于标签列、字段列还是跨列位置。 | 与 `itemAt(row, role)`、`setWidget()` 等搭配。 |
| 枚举值 | `LabelRole` | 左侧标签项。 | 一般由文字标签重载自动创建。 |
| 枚举值 | `FieldRole` | 右侧字段项。 | 放输入控件或字段子布局。 |
| 枚举值 | `SpanningRole` | 横跨标签列和字段列的项目。 | 放复选框、提示、按钮行、分隔区。 |
| 枚举 | `RowWrapPolicy` | 指定窄宽度下标签和字段是否分行。 | 对多语言或可窄化界面尤其重要。 |
| 枚举值 | `DontWrapRows` | 始终左右并排。 | 常规桌面表单。 |
| 枚举值 | `WrapLongRows` | 仅放不下的行让字段换到标签下方。 | 自适应窄窗口。 |
| 枚举值 | `WrapAllRows` | 每行都使用上下结构。 | 极窄栏或移动式面板。 |
| 结构 | `TakeRowResult` | `takeRow()` 返回的两个布局项。 | 通过 `labelItem`、`fieldItem` 接管并安排后续所有权。 |
| 属性 | `fieldGrowthPolicy` | 表单字段的增长策略。 | `fieldGrowthPolicy()` / `setFieldGrowthPolicy()` 访问。 |
| 属性 | `formAlignment` | 整体内容在可用区域中的对齐。 | 所有字段不增长时决定空白留在哪。 |
| 属性 | `horizontalSpacing` | 同行两列之间的间距。 | 未设置时继承父布局或 style。 |
| 属性 | `labelAlignment` | 标签列内的水平对齐。 | 常按平台习惯设左对齐或右对齐。 |
| 属性 | `rowWrapPolicy` | 行的换行策略。 | `WrapLongRows` 适合宽度会变化的表单。 |
| 属性 | `verticalSpacing` | 行与行之间的间距。 | 与 `horizontalSpacing` 可独立设置。 |

### 10.2 创建与添加行

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFormLayout(QWidget *parent = nullptr)` | 创建表单布局，传 `parent` 时成为其顶层布局 | 一个 `QWidget` 只能有一个顶层布局 |
| 生命周期 | `~QFormLayout()` | 销毁表单布局 | 由父对象或顶层窗口销毁时，Qt 管理布局生命周期 |
| 添加行 | `addRow(QWidget *label, QWidget *field)` | 追加“已有标签控件 + 字段控件”行 | 已自定义标签外观或 buddy 时使用 |
| 添加行 | `addRow(QWidget *label, QLayout *field)` | 追加“已有标签控件 + 字段子布局”行 | 一个字段区域含多个控件时使用 |
| 添加行 | `addRow(const QString &labelText, QWidget *field)` | 自动创建文字标签并追加字段控件 | 最常用；自动把字段设为 label 的 buddy |
| 添加行 | `addRow(const QString &labelText, QLayout *field)` | 自动创建文字标签并追加字段子布局 | 标签会创建出来；layout 本身不是可聚焦 buddy 目标 |
| 添加行 | `addRow(QWidget *widget)` | 追加一个跨两列控件 | 复选框、说明文本、完整宽度按钮等 |
| 添加行 | `addRow(QLayout *layout)` | 追加一个跨两列子布局 | 按钮栏、分隔区域或复杂一整行内容 |
| 插入行 | `insertRow(int row, QWidget *label, QWidget *field)` | 在指定行前插入已有标签和字段 | `row` 越界时追加到末尾 |
| 插入行 | `insertRow(int row, QWidget *label, QLayout *field)` | 在指定行前插入已有标签和字段子布局 | 适合动态插入复合字段 |
| 插入行 | `insertRow(int row, const QString &labelText, QWidget *field)` | 在指定行前插入自动标签和字段 | 自动创建 label 并设 buddy |
| 插入行 | `insertRow(int row, const QString &labelText, QLayout *field)` | 在指定行前插入自动标签和字段子布局 | 用于带文字标签的复合字段 |
| 插入行 | `insertRow(int row, QWidget *widget)` | 在指定行前插入跨列控件 | 动态插入开关、说明或分隔控件 |
| 插入行 | `insertRow(int row, QLayout *layout)` | 在指定行前插入跨列子布局 | 动态插入按钮栏等横跨整行内容 |
| 底层添加 | `addItem(QLayoutItem *item)` | `QLayout` 的重实现，向表单加入原始布局项 | 自定义 layout 实现使用；普通代码优先 `addRow()` |

### 10.3 查询、定位与关联标签

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 行数 | `rowCount() const` | 返回逻辑行数 | 不等同于 `count()`；普通两列行是一行但可能有两个 item |
| 项数 | `count() const` | 返回内部 `QLayoutItem` 总数 | 一条普通两列行通常算两个项目，跨列行通常算一个 |
| 查询 | `itemAt(int index) const` | 按内部线性索引取得项目 | 与 `QLayout` 线性索引一致；越界返回 `nullptr` |
| 查询 | `itemAt(int row, ItemRole role) const` | 按逻辑行和角色取得项目 | 读取标签、字段或跨列项时优先使用此重载 |
| 定位 | `getItemPosition(int index, int *rowPtr, ItemRole *rolePtr) const` | 将内部项目索引反查为行号和角色 | 索引越界时 `*rowPtr` 设为 `-1` |
| 定位 | `getWidgetPosition(QWidget *widget, int *rowPtr, ItemRole *rolePtr) const` | 查询某控件位于哪一行、什么角色 | 找不到时 `*rowPtr` 为 `-1` |
| 定位 | `getLayoutPosition(QLayout *layout, int *rowPtr, ItemRole *rolePtr) const` | 查询某子布局位于哪一行、什么角色 | 用于动态维护嵌套字段布局 |
| 标签 | `labelForField(QWidget *field) const` | 返回字段控件关联的标签 | 对自动创建的 label 很实用；不存在时返回 `nullptr` |
| 标签 | `labelForField(QLayout *field) const` | 返回字段子布局关联的标签 | 字段是复合布局时使用 |
| 可见性 | `isRowVisible(int row) const` | 查询指定行是否仍有可见项目 | Qt 6.4 引入；不是“所有项目都可见”的判断 |
| 可见性 | `isRowVisible(QWidget *widget) const` | 按控件找到其行并查询可见性 | Qt 6.4 引入；找不到时按无效行处理 |
| 可见性 | `isRowVisible(QLayout *layout) const` | 按子布局找到其行并查询可见性 | Qt 6.4 引入，适合复合字段行 |

### 10.4 配置、显示与按单元格填充

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 字段增长 | `fieldGrowthPolicy() const` | 读取字段增长策略 | 默认受当前 style 影响，不同平台可能不同 |
| 字段增长 | `setFieldGrowthPolicy(FieldGrowthPolicy policy)` | 设置字段列如何使用多余宽度 | 用来稳定跨平台视觉效果 |
| 对齐 | `formAlignment() const` | 读取整张表单的内容对齐 | 字段不扩展时最明显 |
| 对齐 | `setFormAlignment(Qt::Alignment alignment)` | 设置整张表单在可用区域中的对齐 | 常用 `AlignLeft | AlignTop` 或居中 |
| 对齐 | `labelAlignment() const` | 读取标签列内对齐 | 通常只需要水平对齐标志 |
| 对齐 | `setLabelAlignment(Qt::Alignment alignment)` | 设置标签列内对齐 | 右对齐能使标签文字靠近字段列 |
| 换行 | `rowWrapPolicy() const` | 读取窄宽度下的行换行策略 | 默认依赖 style |
| 换行 | `setRowWrapPolicy(RowWrapPolicy policy)` | 设置标签和字段是否/何时分行 | 需要响应窄宽度时选 `WrapLongRows` |
| 间距 | `horizontalSpacing() const` | 读取两列之间的间距 | 未显式设置时可能来自 style 或父布局 |
| 间距 | `setHorizontalSpacing(int spacing)` | 设置两列之间的间距 | 使用像素值；保持与其他布局一致 |
| 间距 | `verticalSpacing() const` | 读取逻辑行之间的间距 | 未显式设置时可能来自 style 或父布局 |
| 间距 | `setVerticalSpacing(int spacing)` | 设置逻辑行之间的间距 | 不影响同一行标签与字段的距离 |
| 间距 | `spacing() const` | 读取统一间距 | 横纵间距不同则返回 `-1` |
| 间距 | `setSpacing(int spacing)` | 同时设置横、纵间距 | 之后两个方向都为该值 |
| 可见性 | `setRowVisible(int row, bool on)` | 显示或隐藏整个逻辑行 | Qt 6.4 引入；适合条件字段 |
| 可见性 | `setRowVisible(QWidget *widget, bool on)` | 按其中一个控件显示或隐藏整行 | Qt 6.4 引入，避免先手动查行号 |
| 可见性 | `setRowVisible(QLayout *layout, bool on)` | 按其中一个子布局显示或隐藏整行 | Qt 6.4 引入，适合复合字段行 |
| 单元格填充 | `setWidget(int row, ItemRole role, QWidget *widget)` | 把控件放入指定行和角色位置，必要时补空行 | 目标格已占用会失败；普通场景优先 `addRow()` |
| 单元格填充 | `setLayout(int row, ItemRole role, QLayout *layout)` | 把子布局放入指定行和角色位置 | 目标格已占用会失败，子布局不能已有其他父布局 |
| 单元格填充 | `setItem(int row, ItemRole role, QLayoutItem *item)` | 把原始布局项放入指定行和角色位置 | 不可用于添加 widget item 或 child layout；优先用 `setWidget()` / `setLayout()` |

### 10.5 移除、接管与布局计算

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 移除 | `removeRow(int row)` | 删除指定行以及其中 widgets、标签和嵌套 layouts | 会删除对象，不可继续使用旧裸指针 |
| 移除 | `removeRow(QWidget *widget)` | 删除包含该控件的整行及其内容 | 适合动态字段；会连同配对标签删除 |
| 移除 | `removeRow(QLayout *layout)` | 删除包含该子布局的整行及其内容 | 会删除该布局及同一行标签 |
| 接管 | `takeRow(int row)` | 取出一整行但不删除其中项目 | 调用者接管 `labelItem`、`fieldItem` 的后续处理 |
| 接管 | `takeRow(QWidget *widget)` | 按控件取出其整行且不删除 | 用于移动、暂存或复用字段行 |
| 接管 | `takeRow(QLayout *layout)` | 按子布局取出其整行且不删除 | 用于复用复合字段布局 |
| 接管 | `takeAt(int index)` | 按内部项目索引取出一个项目 | 不删除项目；不是按逻辑行操作 |
| 缓存 | `invalidate()` | 使缓存的布局计算失效 | 动态改 size hint、可见性或项目后 Qt 通常会调用；自定义代码很少直接需要 |
| 尺寸协商 | `expandingDirections() const` | 报告布局可有效利用额外空间的方向 | 供父布局计算使用 |
| 高宽相关 | `hasHeightForWidth() const` | 查询高度是否依赖可用宽度 | 含可换行标签等内容时可能为真 |
| 高宽相关 | `heightForWidth(int width) const` | 计算给定宽度下所需高度 | 父布局处理窄窗口和文本换行时调用 |
| 尺寸协商 | `minimumSize() const` | 返回当前内容约束下的最小尺寸 | 窗口最小尺寸和父布局计算使用 |
| 尺寸协商 | `sizeHint() const` | 返回推荐尺寸 | 受字段、标签、间距、换行策略影响 |
| 几何分配 | `setGeometry(const QRect &rect)` | 将最终矩形分配给各行、各项目 | Qt 布局过程调用；应用代码不要手动摆子控件 |
