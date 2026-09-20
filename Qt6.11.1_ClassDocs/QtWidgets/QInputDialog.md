# QInputDialog

> Qt 6.11.1 · Qt Widgets · 来自 `QInputDialog`

## 1. 先建立直觉

`QInputDialog` 是用于临时获取一个简单输入值的标准对话框：一段文本、一个整数、一个浮点数，或从列表里选一项。它适合“重命名”“输入数量”“选择分类”这种单问题交互。

如果输入之间有依赖、需要多字段校验、需要复杂说明或布局，应该写自定义 `QDialog`。`QInputDialog` 的优势是快速、标准、低成本，不是表单框架。

## 2. 类说明

- 头文件：`#include <QInputDialog>`
- 模块：`Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它可以用静态函数同步获取结果，也可以实例化后配置范围、按钮文本、实时信号和异步打开。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `getText()` | 获取单行文本，可设置 echo mode。 |
| `getMultiLineText()` | 获取多行文本。 |
| `getInt()` | 获取整数，带范围和步长。 |
| `getDouble()` | 获取浮点数，带范围、小数位和步长。 |
| `getItem()` | 从字符串列表中选择或输入一项。 |
| `setInputMode()` / `inputMode()` | 切换文本、整数、浮点模式。 |
| `setLabelText()` / `labelText()` | 设置提示标签。 |
| `setOkButtonText()` / `setCancelButtonText()` | 自定义按钮文本。 |
| `setTextValue()` / `textValue()` | 文本模式当前值。 |
| `setTextEchoMode()` / `textEchoMode()` | 密码、普通文本等回显模式。 |
| `setIntRange()` / `setIntMinimum()` / `setIntMaximum()` | 整数输入范围。 |
| `setIntValue()` / `intValue()` | 整数当前值。 |
| `setIntStep()` / `intStep()` | 整数步进。 |
| `setDoubleRange()` / `setDoubleMinimum()` / `setDoubleMaximum()` | 浮点范围。 |
| `setDoubleValue()` / `doubleValue()` | 浮点当前值。 |
| `setDoubleDecimals()` | 小数位数。 |
| `setDoubleStep()` | 浮点步进。 |
| `setComboBoxItems()` / `comboBoxItems()` | 下拉候选项。 |
| `setComboBoxEditable()` | 候选项是否允许用户编辑。 |
| `setOption()` / `setOptions()` / `testOption()` | 无按钮、列表视图、多行文本控件等选项。 |
| `open(receiver, member)` | 异步打开并连接选中信号。 |
| `textValueChanged()` / `textValueSelected()` | 文本变化与最终确认。 |
| `intValueChanged()` / `intValueSelected()` | 整数变化与最终确认。 |
| `doubleValueChanged()` / `doubleValueSelected()` | 浮点变化与最终确认。 |

## 4. 关键用法

### 静态函数必须看 `ok`

`getText()`、`getInt()` 等取消时仍会返回一个值，通常是初始值或当前控件值。必须检查 `ok`，否则用户点取消也会被当成输入成功。

### 选择正确输入模式

整数和浮点不要用文本框再自己解析，直接用 `IntInput` 或 `DoubleInput` 能得到范围、步长、键盘输入限制和更清晰的错误边界。密码或敏感输入用 `setTextEchoMode(QLineEdit::Password)`。

### 实时模式需要取消策略

设置 `NoButtons` 后，value changed 信号会让你做实时预览，但没有确认/取消按钮。应用要提供撤销或在关闭时决定是否保留修改。

### 列表选择不是复杂选择器

`getItem()` 适合短列表。候选项很多、需要搜索、分组、图标或多列信息时，用自定义对话框加 `QListView`/`QComboBox` 更好。

## 5. 常见坑与经验

- 不要用 `QInputDialog` 做多字段业务表单。
- `doubleValue` 文档里有时容易被误读，实际读写是 `double`。
- 范围和步长要符合业务单位，不要沿用默认极大范围。
- `UsePlainTextEditForTextInput` 适合多行长文本，比普通文本编辑更轻。
- 输入结果仍要经过业务校验，例如名称重复、权限、文件名非法字符。
