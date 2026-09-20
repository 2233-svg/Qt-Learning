# QLineEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QLineEdit`

## 1. 先建立直觉

### 这是什么

`QLineEdit` 是单行文本输入控件。它负责编辑一段短文本，并围绕这段文本提供光标、选择、剪贴板、撤销重做、输入法、校验、输入掩码、占位提示、密码显示、补全器和内嵌 action。

它适合“一个字段”的输入：用户名、搜索词、路径、端口、邮箱、短标题。它不适合长文档，也不适合富文本编辑。理解 `QLineEdit` 的关键，是区分“正在变化的文本”和“用户确认完成的文本”：`textChanged()` 很高频，`editingFinished()` 和 `returnPressed()` 才更接近提交时机。

### 适合使用的场景

- 单行短文本输入、搜索框、路径框、登录名、邮箱。
- 密码或令牌输入，配合 `EchoMode`。
- 格式固定的输入，配合 `inputMask`。
- 需要语法合法性判断的输入，配合 `QValidator`。
- 需要候选提示的输入，配合 `QCompleter`。
- 需要输入框内嵌清除、搜索、浏览等图标 action。

### 不适合的场景

- 多行文本用 `QTextEdit` 或 `QPlainTextEdit`。
- 复杂数值输入优先用 `QSpinBox`、`QDoubleSpinBox`、`QDateTimeEdit`。
- 下拉选择用 `QComboBox`，不要用补全器伪装所有选择场景。
- 敏感信息不要长期保留在普通 QString 日志或调试输出中。

### 最小示例

```cpp
auto *edit = new QLineEdit(this);
edit->setPlaceholderText(tr("Search"));
edit->setClearButtonEnabled(true);
edit->addAction(QIcon(":/icons/search.svg"), QLineEdit::LeadingPosition);

connect(edit, &QLineEdit::returnPressed, this, [this, edit] {
    runSearch(edit->text().trimmed());
});
```

搜索框通常响应 `returnPressed()`，而不是每次 `textChanged()` 都立即执行昂贵查询。

## 2. 依赖与对象关系

- 头文件：`#include <QLineEdit>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

### 三层约束

`inputMask` 约束字符位置格式，`QValidator` 判断整段文本是否合法，业务校验判断这个值在当前业务中是否可用。它们不是同一层东西：IP 地址掩码能限制形状，但范围仍需要 validator 或业务校验。

### 显示文本和真实文本

`text()` 返回真实内容，`displayText()` 返回显示内容。密码模式下二者不同；输入掩码下，`text()` 可能去掉空白占位，`displayText()` 更接近用户看到的内容。

### 输入法和光标

`QLineEdit` 是完整的文本编辑控件，支持输入法预编辑、双向文本、逻辑/视觉光标移动、选择和剪贴板。不要用键盘事件自己拼字符，除非你在做非常特殊的控件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum ActionPosition` | 输入框内嵌 action 的位置：前导或尾随。 |
| `enum EchoMode` | 文本显示方式：正常、不显示、密码、编辑时短暂显示。 |
| `text : QString` / `displayText : QString` | 真实文本与显示文本。 |
| `placeholderText : QString` | 空内容时显示的提示文字。 |
| `maxLength : int` | 最大输入长度。 |
| `inputMask : QString` | 位置格式掩码，例如日期、MAC 地址。 |
| `acceptableInput : bool` | 当前文本是否同时满足掩码和 validator。 |
| `echoMode : EchoMode` | 密码/普通显示控制。 |
| `readOnly : bool` | 是否禁止用户编辑但允许复制。 |
| `modified : bool` | 用户是否修改过内容。 |
| `alignment : Qt::Alignment` | 文本在输入框内的对齐。 |
| `cursorPosition : int` | 当前光标位置。 |
| `cursorMoveStyle : Qt::CursorMoveStyle` | 双向文本中的逻辑/视觉移动规则。 |
| `hasSelectedText` / `selectedText` | 是否有选择以及选择内容。 |
| `undoAvailable` / `redoAvailable` | 撤销/重做是否可用。 |
| `dragEnabled : bool` | 是否允许拖拽选中文本。 |
| `frame : bool` | 是否绘制输入框边框。 |
| `clearButtonEnabled : bool` | 非空时是否显示内置清除按钮。 |
| `QLineEdit(...)` | 创建空输入框或带初始文本的输入框。 |
| `setText()` / `text()` / `clear()` | 设置、读取、清空文本。 |
| `insert()` | 在光标处插入文本，并遵守长度和校验限制。 |
| `copy()` / `cut()` / `paste()` | 剪贴板操作。 |
| `undo()` / `redo()` | 撤销和重做。 |
| `selectAll()` / `deselect()` / `setSelection()` | 文本选择控制。 |
| `selectionStart()` / `selectionEnd()` / `selectionLength()` | 查询选择范围。 |
| `backspace()` / `del()` | 删除光标前或光标后的字符。 |
| `cursorForward()` / `cursorBackward()` / `cursorWordForward()` / `cursorWordBackward()` | 移动光标，可选择文本。 |
| `home()` / `end()` | 移动到开头或结尾，可选择文本。 |
| `cursorPositionAt(const QPoint &pos)` | 根据坐标计算光标位置。 |
| `cursorRect() const` | 返回光标矩形。 |
| `addAction(...)` | 在输入框内添加 action 图标。 |
| `setCompleter()` / `completer()` | 设置或读取补全器。 |
| `setValidator()` / `validator()` | 设置或读取校验器。 |
| `setTextMargins(...)` / `textMargins()` | 设置或读取文本边距，为内嵌按钮留空间。 |
| `createStandardContextMenu()` | 创建默认右键菜单，可追加自定义动作。 |
| `textChanged(QString)` | 文本变化时发出，包括程序修改。 |
| `textEdited(QString)` | 用户编辑导致文本变化时发出。 |
| `editingFinished()` | 编辑结束且条件满足时发出。 |
| `returnPressed()` | 用户按 Return/Enter 且输入可接受时发出。 |
| `inputRejected()` | 输入被掩码、长度或 validator 拒绝时发出。 |
| `selectionChanged()` | 选择范围变化时发出。 |
| `cursorPositionChanged(old, new)` | 光标位置变化时发出。 |
| `sizeHint()` / `minimumSizeHint()` | 推荐尺寸。 |
| `inputMethodQuery()` / `inputMethodEvent()` | 输入法查询和预编辑处理。 |
| 各类鼠标、键盘、拖放、焦点、绘制事件 | 支撑编辑器完整交互。 |

## 4. API 逐项说明

### `enum QLineEdit::ActionPosition`

`LeadingPosition` 和 `TrailingPosition` 表示内嵌 action 放在文本前侧还是后侧。它们会考虑布局方向：左到右界面中 leading 在左，右到左界面中 leading 在右。

搜索图标常放 leading，清除、浏览、显示密码这类动作常放 trailing。

### `enum QLineEdit::EchoMode`

`Normal` 显示真实文本；`NoEcho` 不显示内容；`Password` 显示平台密码掩码；`PasswordEchoOnEdit` 编辑时短暂显示，非编辑时掩码。

密码框不要连接调试日志打印 `text()`，也不要把密码塞进 placeholder。placeholder 是提示，不是默认值。

### `text` / `displayText`

`text()` 是真实值，提交业务时通常读取它。`displayText()` 是用户看到的显示值，密码和输入掩码场景下可能不同。

需要保存用户输入时用 `text()`；需要测量、调试显示效果时看 `displayText()`。

### `placeholderText`

占位文字在输入框为空时显示，用来提示输入格式或目的。它不是默认值，不会出现在 `text()` 里。

不要把关键说明只放 placeholder。用户一旦输入，提示就消失；重要规则应放在 label、tooltip 或校验错误里。

### `maxLength`

限制最大字符数。设置文本超过限制时会被截断。

它是 UI 层保护，不是数据库或协议层校验的替代。后端限制仍要在提交前检查。

### `inputMask`

输入掩码描述每一位允许输入什么字符，适合固定格式：日期、MAC 地址、许可证号。它还可以指定占位字符。

掩码只保证形状，不保证业务范围。例如 `999.999.999.999` 不能保证 IP 每段小于 256；要配合 validator 或业务校验。

### `acceptableInput`

只读属性，表示当前内容是否满足输入掩码和 validator。`returnPressed()`、`editingFinished()` 的触发会受到可接受状态影响。

它不等于业务有效。例如路径格式合法，不代表文件存在；端口数字合法，不代表端口可连接。

### `validator`

通过 `setValidator(const QValidator *)` 限制输入。validator 通常由外部对象持有或以合适 parent 管理；`validator()` 返回当前校验器。

`QIntValidator`、`QDoubleValidator`、`QRegularExpressionValidator` 是常见选择。复杂校验建议写在提交逻辑中，并用 validator 做即时反馈。

### `echoMode`

控制显示隐私。`Password` 模式下复制和拖拽能力会受限制，具体行为遵循平台安全习惯。

切换显示/隐藏密码时，通常用 trailing action，并且注意不要改变真实文本和光标体验。

### `readOnly`

只读时用户不能编辑，但通常仍可复制文本。它适合展示可复制的路径、令牌片段、生成结果。

禁用 `setEnabled(false)` 和只读不同：禁用表示当前控件不可操作，视觉也会弱化；只读表示值可看可复制但不可改。

### `modified`

记录用户是否修改过内容。`setText()` 会重置为 false，用户编辑会置为 true。

它适合“如果用户还没手动输入，就用自动推断默认值填充”的场景。

### `alignment`

控制文本对齐。数字输入常右对齐，搜索框和普通文本通常左对齐，短验证码可以居中。

垂直方向通常保持 `AlignVCenter`，否则输入框观感容易不自然。

### `cursorPosition` / `cursorMoveStyle`

`cursorPosition` 是逻辑光标位置。`cursorMoveStyle` 决定双向文本中方向键按逻辑顺序移动，还是按视觉方向移动。

面向混合中英文、阿拉伯语、希伯来语等文本时，不要自己假设左箭头永远是 position - 1。

### 选择相关 API

`hasSelectedText()`、`selectedText()`、`setSelection()`、`selectionStart()`、`selectionEnd()`、`selectionLength()` 用于管理选择范围。`selectAll()` 全选，`deselect()` 取消选择。

实现“获得焦点自动全选”时，注意不要和用户鼠标定位光标冲突；很多应用会只在首次 focus 或明确快捷键时全选。

### 编辑操作 API

`insert()`、`backspace()`、`del()`、`cut()`、`copy()`、`paste()`、`undo()`、`redo()` 提供编辑器常见动作，并遵守只读、长度、掩码和 validator 限制。

程序插入文本时优先用 `insert()`，它更接近用户编辑语义；直接 `setText()` 会替换全部文本并重置 modified。

### 光标移动 API

`cursorForward()`、`cursorBackward()`、`cursorWordForward()`、`cursorWordBackward()`、`home()`、`end()` 都带 `mark` 参数：为 true 时移动同时扩展选择。

这些 API 适合实现自定义快捷键或外部按钮控制输入框，不要通过模拟 key event 达成同样目的。

### 内嵌 action

`addAction(QAction *, ActionPosition)` 把已有 action 放入输入框；`addAction(QIcon, ActionPosition)` 创建并返回一个 action。

内嵌 action 会占据文本区域空间，必要时用 `setTextMargins()` 调整。不要把太多 action 塞进单行输入框，否则字段本身会变得狭窄。

### completer

`setCompleter(QCompleter *)` 设置补全器。补全器适合历史记录、命令名、文件路径、已知候选值。

补全不是校验。用户仍可能输入不在候选列表中的内容，除非你额外限制提交逻辑。

### text margins

`setTextMargins()` 给文本绘制区域留边，常用于和内嵌 action、自定义图标或外部覆盖控件配合。

如果文字被清除按钮或图标遮住，优先检查 text margins。

### context menu

`createStandardContextMenu()` 创建标准右键菜单，包含撤销、重做、剪切、复制、粘贴、删除、全选等动作。你可以取得后追加自定义动作再弹出。

不要完全替换标准菜单，除非你把基本编辑动作也补回来；用户会期待文本框右键能复制粘贴。

### 信号选择

`textChanged()` 包括程序修改和用户修改；`textEdited()` 只表示用户编辑。`returnPressed()` 适合提交搜索或表单字段；`editingFinished()` 适合焦点离开或回车后的最终处理。`inputRejected()` 适合提示输入被拒绝。

昂贵操作不要直接连 `textChanged()`；可以防抖，或等 `returnPressed()`。

### 拖放、输入法、事件和绘制

拖放事件支持拖入文本；输入法事件支持预编辑文本；鼠标键盘事件支撑选择、光标和编辑；`paintEvent()` 绘制边框、文本、选择和光标；`initStyleOption()` 给 style 准备 frame 信息。

普通业务使用不需要重写这些函数。若要改变输入行为，优先组合 validator、completer、action 和信号；重写事件是最后手段。

## 5. 深入实践与常见坑

### `textChanged` 很容易过度触发

用户每输入一个字符都会触发，程序 `setText()` 也会触发。搜索建议可以连它，但要防抖；提交保存不要直接连它。

### validator 不是业务校验

validator 能保证格式或局部规则，不能保证用户名存在、路径可写、端口可连接。提交前仍要做业务层检查。

### 密码模式保护的是显示，不是内存

`Password` 让屏幕上不显示明文，但 `text()` 仍能拿到字符串。不要日志输出，不要无意义地长期缓存。

### 输入掩码适合固定形状

日期、MAC、许可证号很适合；自然语言、文件路径、URL 通常不适合用 mask 强行限制。

### 只读比禁用更适合可复制内容

需要用户复制生成结果时，用 `setReadOnly(true)`，不要 `setEnabled(false)`。禁用控件往往连选择复制体验都变差。
