# QMessageBox

> Qt 6.11.1 · Qt Widgets · 来自 `QMessageBox`

## 1. 先建立直觉

`QMessageBox` 是用于提示、确认、警告和错误说明的标准对话框。它的价值不只是弹个框，而是用平台一致的图标、按钮顺序、默认按钮和 Escape 行为，让用户快速判断“发生了什么、我能做什么”。

适合场景包括删除确认、保存前询问、错误提示、操作成功提示、带详细信息的故障说明。不要把复杂表单塞进消息框；超过一个勾选框或一段详细信息时，通常应该写自定义 `QDialog`。

## 2. 类说明

- 头文件：`#include <QMessageBox>`
- 模块：`Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

消息框可以用静态函数快速显示，也可以实例化后细调按钮、详细文本、复选框和异步打开方式。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `information()` / `warning()` / `critical()` / `question()` | 快速显示常见模态消息框并返回标准按钮。 |
| `about()` / `aboutQt()` | 显示关于应用或关于 Qt 的对话框。 |
| `QMessageBox(icon, title, text, buttons, parent, flags)` | 构造可细调的消息框。 |
| `setText()` / `text()` | 主消息，一句话说明核心事实。 |
| `setInformativeText()` | 补充说明影响、原因或建议操作。 |
| `setDetailedText()` | 可展开的详细信息，适合错误日志和技术细节。 |
| `setIcon()` / `icon()` | 使用标准信息、警告、错误、问题图标。 |
| `setIconPixmap()` | 使用自定义图标 pixmap。 |
| `setStandardButtons()` / `standardButtons()` | 设置标准按钮组合。 |
| `addButton()` | 添加标准按钮、自定义文本按钮或现有按钮。 |
| `removeButton()` | 移除按钮。 |
| `button()` / `standardButton()` | 在标准按钮和实际按钮对象之间转换。 |
| `buttonRole()` | 查询按钮角色，如接受、拒绝、破坏性操作。 |
| `buttons()` | 获取所有按钮。 |
| `setDefaultButton()` / `defaultButton()` | 设置 Enter 默认触发按钮。 |
| `setEscapeButton()` / `escapeButton()` | 设置 Esc 或关闭窗口对应按钮。 |
| `clickedButton()` | 对话框结束后查询用户点击的按钮。 |
| `setCheckBox()` / `checkBox()` | 加入“不要再提示”等复选框。 |
| `setTextFormat()` / `textFormat()` | 控制文本按纯文本、富文本或自动格式解析。 |
| `setTextInteractionFlags()` | 允许选择、复制或点击链接。 |
| `setOption()` / `setOptions()` / `testOption()` | Qt 6.6 起控制选项，如不使用原生对话框。 |
| `exec()` | 同步模态显示，返回结果。 |
| `open(receiver, member)` | 异步打开，并把按钮结果连接到槽。 |
| `buttonClicked(button)` | 用户点击按钮时发出。 |

## 4. 关键用法

### 静态函数适合简单结论

一行警告、一个确认、一个错误提示，用 `QMessageBox::warning()` 这类静态函数很清楚。它们会阻塞到用户选择，并返回 `StandardButton`。例如删除确认应使用 `Question` 或 `Warning` 语义，并把破坏性按钮设置清楚。

### 实例化适合细节和自定义按钮

需要 detailed text、复选框、自定义按钮文本、默认按钮、异步打开时，创建 `QMessageBox` 实例更好。主文本应短，解释放在 `informativeText`，堆栈、路径、错误码放在 `detailedText`。

### 默认按钮和 Escape 按钮是安全设计

破坏性操作不要把默认按钮设成“删除”或“丢弃”。`setDefaultButton()` 决定 Enter 行为，`setEscapeButton()` 决定 Esc/关闭窗口行为。保存确认这类对话框尤其要显式设计这两个行为。

### 富文本要谨慎

`Qt::AutoText` 会猜测文本格式。如果消息来自用户输入、文件名或网络，最好用 `setTextFormat(Qt::PlainText)`，避免尖括号内容被当成富文本。需要可复制错误信息时设置 `textInteractionFlags`。

## 5. 常见坑与经验

- 消息框不要承载复杂决策；按钮过多时用户会失去判断。
- `detailedText` 按纯文本处理，适合日志，不适合排版。
- `clickedButton()` 只有对话框交互后才有意义。
- 原生对话框和 Qt 对话框在外观细节上可能不同；`DontUseNativeDialog` 要在显示前设置。
- GUI 线程中连续弹多个消息框会打断用户流程，批量错误更适合汇总展示。
