# Qt QLineEdit 深入笔记

> 适用版本：Qt 6 Widgets（Qt 5 的核心用法基本一致）  
> 头文件：`#include <QLineEdit>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QLineEdit`  
> 定位：单行文本编辑器

## 1. 先建立整体认识：它解决什么问题

`QLineEdit` 不是“一个能输入文字的框”这么简单，它解决的是**单行、纯文本、可控输入**这件事。

它适合处理这类需求：

- 用户只需要输入一条字符串，而不是一段文章；
- 这条字符串要能被程序实时读取、校验、回填；
- 输入过程要支持撤销、重做、复制、粘贴、拖拽；
- 输入值可能是密码、手机号、编号、邮箱、搜索词、标签名；
- 界面上还要放前缀图标、清除按钮、补全提示、输入掩码。

很多看起来不像输入框的控件，内部其实也把它当编辑核心：

- `QComboBox`
- `QAbstractSpinBox`
- `QDateTimeEdit`

所以理解 `QLineEdit`，不只是理解一个控件，而是理解 Qt 里“单值编辑”的基础件。

## 2. 什么时候该用它

| 场景 | 为什么用它 |
| --- | --- |
| 登录名、邮箱、手机号、编号 | 单行输入 + 验证器/掩码 |
| 密码输入 | `echoMode` 可隐藏真实文本 |
| 搜索框、筛选框 | 可配补全、清除按钮、前缀图标 |
| 表单中的普通字段 | 配合 `QFormLayout` 很顺手 |
| 只显示但不允许改 | `setReadOnly(true)` |
| 需要一边输入一边约束格式 | `inputMask` / `QValidator` |

不适合它的场景也很明确：

- 段落输入、富文本编辑：用 `QTextEdit`
- 多行纯文本编辑：用 `QPlainTextEdit`
- 复杂结构化数据：别硬塞进单行框

## 3. 先把几个最容易混淆的概念分开

### 3.1 `text()` 和 `displayText()`

- `text()` 是真实内容。
- `displayText()` 是屏幕上看到的内容。

密码模式下，这两个值通常不一样：真实值还在，显示值会被掩码。

### 3.2 `textChanged()` 和 `textEdited()`

- `textChanged()`：只要文本变了就发，程序里 `setText()` 也算。
- `textEdited()`：只有用户真的在编辑时才发，程序改值不算。

做数据绑定时，这两个信号用途不一样。  
想知道“界面内容变了”看 `textChanged()`，想知道“用户改了”看 `textEdited()`。

### 3.3 `returnPressed()` 和 `editingFinished()`

- `returnPressed()`：按下 Enter / Return 时发。
- `editingFinished()`：按下 Enter / Return，或者失焦且内容变过时发。

如果设置了 `validator()` 或 `inputMask()`，这两个信号只有在输入是 `Acceptable` 时才会发。

### 3.4 `inputMask`、`validator`、`maxLength`

这三层是在解决不同层次的问题：

- `maxLength`：长度别超。
- `inputMask`：格式别乱，比如手机号、日期、验证码。
- `validator`：语义别错，比如整数范围、邮箱、正则表达式。

它们不是替代关系，而是可以叠加。

### 3.5 `modified`

这个标记不是给 Qt 内部用的，主要给你做业务判断用。

- 用户真的改过内容，它会变成 `true`。
- `setText()` 会把它重置回 `false`。

这在“表单有没有被手动修改过”这种需求里很有价值。

### 3.6 `readOnly` 和 `echoMode`

- `readOnly` 是“能不能改”。
- `echoMode` 是“怎么显示”。

只读框还能复制、还能拖拽；密码框则是把显示层隐藏掉。

## 4. 最小可用代码

### 4.1 普通输入框

```cpp
QLineEdit *edit = new QLineEdit;
edit->setPlaceholderText("请输入用户名");
edit->setMaxLength(32);
```

### 4.2 受约束输入

```cpp
QLineEdit *emailEdit = new QLineEdit;
emailEdit->setPlaceholderText("name@example.com");
emailEdit->setValidator(new QRegularExpressionValidator(
    QRegularExpression(R"([^\s@]+@[^\s@]+\.[^\s@]+)"),
    emailEdit));

connect(emailEdit, &QLineEdit::editingFinished, this, [emailEdit] {
    if (emailEdit->hasAcceptableInput())
        saveEmail(emailEdit->text());
});
```

### 4.3 搜索框

```cpp
QLineEdit *searchEdit = new QLineEdit;
searchEdit->setClearButtonEnabled(true);
searchEdit->addAction(QIcon(":/icons/search.svg"), QLineEdit::LeadingPosition);
searchEdit->setTextMargins(24, 0, 0, 0);
```

这个组合很常见：左边一个搜索图标，右边一个清除按钮，文本区留出空间避免压住图标。

## 5. 这类 API 应该怎么读

`QLineEdit` 的 API 其实可以按四条线来记：

1. **文本线**：`text()`、`setText()`、`insert()`、`clear()`
2. **约束线**：`inputMask()`、`setInputMask()`、`setValidator()`、`hasAcceptableInput()`
3. **编辑线**：光标、选择区、撤销栈、剪贴板相关 API
4. **扩展线**：`addAction()`、`createStandardContextMenu()`、`cursorRect()`、`initStyleOption()`

如果你先盯着这些主线，再看零散的事件重写函数，就不会被成员列表冲散。

## 6. 逐组 API 说明

### 6.1 成员类型

`ActionPosition` 不是抽象概念，它就是“动作放在左边还是右边”。  
`EchoMode` 则决定文字是正常显示、完全隐藏，还是编辑时短暂可见。

### 6.2 文本和状态

`text` 是真实值，`displayText` 是显示值。  
`placeholderText` 负责在空白时给用户提示；`maxLength` 防止输入过长；`frame` 控制边框是否显示；`clearButtonEnabled` 让右侧清除按钮变成现成能力。  
`modified` 用来记录用户有没有真正改过；`readOnly` 用来把输入框变成只读展示；`undoAvailable` 和 `redoAvailable` 则是在告诉你编辑历史里还有没有可用动作。

### 6.3 光标和选择

这部分 API 主要解决两件事：**光标在哪**、**选中了什么**。

- `cursorPosition` / `setCursorPosition` / `cursorPositionAt` 负责定位。
- `cursorForward` / `cursorBackward` / `cursorWordForward` / `cursorWordBackward` / `home` / `end` 负责移动。
- `setSelection` / `deselect` / `selectAll` / `hasSelectedText` / `selectedText` / `selectionStart` / `selectionEnd` / `selectionLength` 负责选择区。

如果你要做自定义右键菜单、文本高亮、查找定位，先盯这组。

### 6.4 验证和补全

`inputMask` 适合“格式固定”的输入。  
`validator` 适合“规则固定”的输入。  
`QCompleter` 适合“候选值固定但用户不想手打”的输入。

典型组合是：

- 手机号：`inputMask`
- 整数范围：`QIntValidator`
- 浮点数：`QDoubleValidator`
- 邮箱/账号：`QRegularExpressionValidator`
- 搜索提示：`QCompleter`

### 6.5 编辑动作和历史

`backspace()`、`del()`、`undo()`、`redo()`、`cut()`、`copy()`、`paste()`、`insert()` 这些 API 是把输入框当作“编辑器”来用，而不是当作静态文本。

其中最容易忽略的是：

- `setText()` 是程序回填；
- `insert()` 更像用户输入；
- `cut()` / `paste()` 会受 `readOnly` 和验证规则影响；
- `setText()` 会清掉撤销/重做历史。

### 6.6 视觉和布局辅助

`alignment` 控制文本在框里的对齐，不是布局对齐。  
`cursorMoveStyle` 在双向文本时才真正关键。  
`textMargins` 适合给图标、按钮、前后缀预留空间。  
`addAction()` 是做前缀/后缀动作的入口。  
`sizeHint()` 和 `minimumSizeHint()` 则告诉布局：这个编辑框大概需要多宽。

### 6.7 事件和扩展点

`event()`、`inputMethodQuery()`、`timerEvent()` 这几个函数说明 `QLineEdit` 不是简单的字符串容器，它要和 IME、光标闪烁、输入法状态协作。

如果你在写子类，重点看这几个钩子：

- `cursorRect()`：拿到光标所在矩形，常用于弹层定位
- `initStyleOption()`：填充样式信息，方便自定义绘制
- `paintEvent()`：需要重画时才碰它
- `contextMenuEvent()`：扩展右键菜单
- `keyPressEvent()` / `mousePressEvent()` / `focusInEvent()` 等：编辑交互主链路

## API 速查表
这张表按“文本状态、光标选择、输入约束、编辑动作和外观扩展”分组。查 API 时先问自己要解决的是哪一类问题：约束输入优先看 validator 和 input mask，实时联动优先看 `textEdited()` / `textChanged()`，提交时机则看 `returnPressed()` / `editingFinished()`。

### 成员类型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QLineEdit::ActionPosition` | 描述附加动作放在输入框哪一侧 | 给搜索图标、清除外的自定义按钮、状态动作定位时使用 |
| 枚举值 | `LeadingPosition` | 把动作放在输入框的起始侧 | 左到右语言里通常是左侧；方向布局下“起始侧”不一定等于物理左边 |
| 枚举值 | `TrailingPosition` | 把动作放在输入框的结束侧 | 常用于清除、可见性切换等靠末尾的动作 |
| 枚举 | `QLineEdit::EchoMode` | 描述真实文本在屏幕上如何显示 | 只影响显示，不改变 `text()` 返回的真实内容 |
| 枚举值 | `Normal` | 正常显示真实文本 | 普通账号、搜索词、编号等使用 |
| 枚举值 | `NoEcho` | 不显示任何输入内容 | 适合极少数安全输入场景；用户可用性较差 |
| 枚举值 | `Password` | 始终以密码掩码显示 | `displayText()` 会是掩码文本，`text()` 仍是真实内容 |
| 枚举值 | `PasswordEchoOnEdit` | 编辑时短暂显示，失焦后掩码 | 兼顾输入确认和隐私，但仍不能替代安全存储策略 |

### 属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 校验属性 | `acceptableInput : bool` | 只读属性，表示当前内容是否满足 input mask 和 validator | 提交表单前可查；它不等于“用户已经完成编辑” |
| 外观属性 | `alignment : Qt::Alignment` | 控制文本在输入框内部的对齐 | 不是布局对齐；数值输入常右对齐，普通文本常左对齐 |
| 动作属性 | `clearButtonEnabled : bool` | 控制是否显示内置清除按钮 | 只影响内置按钮显示；自定义动作仍通过 `addAction()` 添加 |
| 光标属性 | `cursorMoveStyle : Qt::CursorMoveStyle` | 控制双向文本中光标按逻辑顺序还是视觉顺序移动 | 普通单语言输入很少改；阿拉伯语/希伯来语等双向文本更重要 |
| 光标属性 | `cursorPosition : int` | 当前光标位置 | 位置按字符串内部索引，不是屏幕像素 |
| 文本属性 | `displayText : QString` | 只读属性，表示屏幕上实际显示的文本 | 密码模式下会被掩码；需要真实值用 `text()` |
| 拖拽属性 | `dragEnabled : bool` | 控制是否允许拖拽选中文本 | 只读框仍可复制和拖拽，取决于交互设置 |
| 文本属性 | `echoMode : EchoMode` | 控制文本显示方式 | 不改变真实文本，不应被当作安全存储机制 |
| 外观属性 | `frame : bool` | 控制是否绘制输入框边框 | 搜索框、嵌入式编辑器常关闭边框配合外层样式 |
| 选择属性 | `hasSelectedText : bool` | 只读属性，表示当前是否有选区 | 只是查询状态；获取内容用 `selectedText()` |
| 校验属性 | `inputMask : QString` | 固定格式输入掩码 | 适合电话、日期片段、验证码等格式固定场景 |
| 文本属性 | `maxLength : int` | 限制最大输入长度 | 超长输入会被拒绝并可能发 `inputRejected()` |
| 状态属性 | `modified : bool` | 记录内容是否被用户改过 | `setText()` 会把它重置为 `false`，适合表单脏状态判断 |
| 文本属性 | `placeholderText : QString` | 空内容时显示提示文本 | 不能替代字段标签；有居中对齐时显示方式可能受样式影响 |
| 编辑属性 | `readOnly : bool` | 控制是否允许修改文本 | 只读仍可选择、复制；禁用控件才是不参与交互 |
| 历史属性 | `redoAvailable : bool` | 只读属性，表示是否可重做 | `setText()` 会清空撤销/重做历史 |
| 选择属性 | `selectedText : QString` | 只读属性，返回当前选中文本 | 无选区时为空；密码输入不应暴露给无关 UI |
| 文本属性 | `text : QString` | 输入框保存的真实文本 | 数据绑定、校验提交、业务计算都应以它为准 |
| 历史属性 | `undoAvailable : bool` | 只读属性，表示是否可撤销 | 程序化重置文本后通常不可撤销 |

### 成员函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QLineEdit(QWidget *parent = nullptr)` | 创建空的单行输入框 | 创建后通常设置 placeholder、长度、校验器或初始文本 |
| 构造 | `QLineEdit(const QString &contents, QWidget *parent = nullptr)` | 创建时直接填入初始文本 | 适合编辑已有值；初始化文本不是“用户修改” |
| 生命周期 | `~QLineEdit()` | 销毁输入框及内部编辑状态 | 通常由父对象负责销毁 |
| 文本 | `text() const` / `setText(const QString &text)` | 读取或程序化设置真实文本 | `setText()` 会清空选择和撤销历史、把光标移到末尾，并把 `modified` 置回 `false` |
| 文本 | `displayText() const` | 读取屏幕实际显示文本 | 密码模式下返回掩码文本；日志和业务提交不要用它代替真实值 |
| 文本 | `placeholderText() const` / `setPlaceholderText(const QString &)` | 查询或设置空白提示 | 提示不是字段名称，复杂表单仍应配 `QLabel` |
| 文本 | `maxLength() const` / `setMaxLength(int)` | 查询或限制最大字符数 | 只是长度限制；语义正确性仍靠 validator 或业务校验 |
| 外观 | `hasFrame() const` / `setFrame(bool)` | 查询或控制是否绘制边框 | 嵌入工具栏、搜索框时常关闭，由外层容器提供边界 |
| 外观 | `isClearButtonEnabled() const` / `setClearButtonEnabled(bool)` | 查询或开关内置清除按钮 | 清空动作会改变文本；如果要确认删除，应自己提供动作 |
| 显示 | `echoMode() const` / `setEchoMode(EchoMode)` | 查询或设置文本显示模式 | 密码模式只保护视觉显示，真实文本仍在内存和 `text()` 中 |
| 编辑 | `isReadOnly() const` / `setReadOnly(bool)` | 查询或设置只读状态 | 只读仍可选择复制；要让控件不可交互应考虑 `setEnabled(false)` |
| 校验 | `validator() const` / `setValidator(const QValidator *)` | 查询或设置输入校验器 | validator 对提交信号有影响；对象所有权通常通过父对象管理 |
| 补全 | `completer() const` / `setCompleter(QCompleter *)` | 查询或设置自动补全器 | 候选值固定但允许用户输入时使用；补全不等于校验 |
| 尺寸 | `sizeHint() const` / `minimumSizeHint() const` | 返回布局建议尺寸 | 由字体、边框、按钮和样式影响，通常交给 layout 使用 |
| 光标 | `cursorPosition() const` / `setCursorPosition(int)` | 查询或设置当前光标位置 | 位置是文本索引，设置越界值会被控件约束 |
| 光标 | `cursorPositionAt(const QPoint &pos)` | 根据控件内坐标反查光标位置 | 自定义点击、悬浮提示、拖放插入点时有用 |
| 外观 | `alignment() const` / `setAlignment(Qt::Alignment)` | 查询或设置内部文本对齐 | 数字输入右对齐常见；不要和布局对齐混淆 |
| 光标 | `cursorForward(bool mark, int steps = 1)` / `cursorBackward(bool mark, int steps = 1)` | 按字符向前或向后移动光标 | `mark=true` 会扩展选择区；方向受文本方向和 cursor move style 影响 |
| 光标 | `cursorWordForward(bool mark)` / `cursorWordBackward(bool mark)` | 按单词移动光标 | 适合快捷键或自定义编辑命令 |
| 编辑 | `backspace()` / `del()` | 删除光标左侧或右侧内容 | 会走只读、选择区和校验逻辑，不只是字符串删除 |
| 光标 | `home(bool mark)` / `end(bool mark)` | 移到行首或行尾 | `mark=true` 时从当前位置选到首/尾 |
| 状态 | `isModified() const` / `setModified(bool)` | 查询或设置用户修改标记 | `setText()` 会重置它；保存表单后可手动设回 `false` |
| 选择 | `setSelection(int start, int length)` | 选中指定范围文本 | `length` 可为负；索引应按字符串位置理解 |
| 选择 | `hasSelectedText() const` / `selectedText() const` | 查询是否有选区并读取选中文本 | 密码/敏感输入不应随意把选中文本同步到别处 |
| 选择 | `selectionStart() const` / `selectionEnd() const` / `selectionLength() const` | 读取选区起点、终点和长度 | 没有选区时起点通常为 `-1` |
| 历史 | `isUndoAvailable() const` / `isRedoAvailable() const` | 查询撤销或重做是否可用 | 程序化 `setText()` 会清掉历史 |
| 拖拽 | `dragEnabled() const` / `setDragEnabled(bool)` | 查询或设置是否能拖拽选中文本 | 常用于可复制字段；拖放输入仍会受校验和只读状态影响 |
| 光标 | `cursorMoveStyle() const` / `setCursorMoveStyle(Qt::CursorMoveStyle)` | 查询或设置双向文本的光标移动风格 | 多语言输入场景才常需要显式设置 |
| 掩码 | `inputMask() const` / `setInputMask(const QString &inputMask)` | 查询或设置固定格式输入掩码 | 适合格式固定输入；语义范围仍应由 validator 或业务层判断 |
| 校验 | `hasAcceptableInput() const` | 判断当前文本是否完整可接受 | 常用于启用提交按钮；中间态输入可能暂时不是 acceptable |
| 内边距 | `textMargins() const` / `setTextMargins(const QMargins &)` / `setTextMargins(int, int, int, int)` | 查询或设置文本绘制区域边距 | 给内嵌图标、动作按钮、前后缀留空间，避免文字压住控件 |
| 动作 | `addAction(QAction *action, ActionPosition position)` | 把已有动作放进输入框左侧或右侧 | 动作对象生命周期按 Qt action 机制管理，常用于搜索图标或状态按钮 |
| 动作 | `addAction(const QIcon &icon, ActionPosition position)` | 创建并添加一个图标动作 | 返回 `QAction *`，可继续连接 triggered、设置 tooltip |
| 菜单 | `createStandardContextMenu()` | 创建默认右键菜单 | 返回的 `QMenu *` 所有权归调用者，扩展后要自己执行和销毁 |
| 选择 | `deselect()` | 取消当前选择区 | 不改变文本内容，只改变选择状态 |
| 编辑 | `insert(const QString &newText)` | 在光标处插入文本 | 会走输入掩码、validator、maxLength 等规则，比直接拼字符串更接近用户输入 |
| 事件 | `event(QEvent *event)` | Qt 通用事件入口 | 普通业务代码不调用；派生类重写时要保留输入法、快捷键、拖放等行为 |
| 输入法 | `inputMethodQuery(Qt::InputMethodQuery query) const` | 向输入法报告光标、选区、周围文本等状态 | IME 候选窗定位、预编辑文本依赖它 |
| 输入法 | `inputMethodQuery(Qt::InputMethodQuery property, QVariant argument) const` | 带参数查询输入法相关状态 | Qt 可调用的重载；通常只在复杂输入法协作或测试中涉及 |
| 定时 | `timerEvent(QTimerEvent *event)` | 处理内部定时事件 | 例如光标闪烁；派生类重写时不要打断内部计时 |

### 公共槽

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 文本 | `clear()` | 清空输入框内容 | 会改变文本并触发相应信号；只读状态下行为受控件规则影响 |
| 剪贴板 | `copy() const` | 把当前选区复制到剪贴板 | 没有选区时通常无效果；敏感字段要谨慎开放复制 |
| 剪贴板 | `cut()` | 剪切选区到剪贴板 | 会修改文本，受 `readOnly`、校验和选区状态影响 |
| 剪贴板 | `paste()` | 把剪贴板文本插入光标处 | 插入内容仍受 input mask、validator、maxLength 限制 |
| 历史 | `redo()` | 重做上一步被撤销的编辑 | 只有 `isRedoAvailable()` 为真时才有意义 |
| 选择 | `selectAll()` | 选中全部文本 | 表单获得焦点后全选常用于快速替换已有值 |
| 文本 | `setText(const QString &text)` | 程序化设置真实文本 | 与成员函数同一 API；会重置 modified 和撤销历史 |
| 历史 | `undo()` | 撤销上一步用户编辑 | 只有 `isUndoAvailable()` 为真时才有意义 |

### 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 光标信号 | `cursorPositionChanged(int old, int now)` | 光标位置改变时发出 | 适合状态栏、辅助提示或自定义高亮同步 |
| 提交信号 | `editingFinished()` | 编辑完成时发出 | 常见于失焦或按回车；有 validator/input mask 时通常要求内容可接受 |
| 校验信号 | `inputRejected()` | 用户输入被拒绝时发出 | 超长、掩码不匹配或 validator 拒绝都可能触发 |
| 提交信号 | `returnPressed()` | 用户按 Enter/Return 时发出 | 有 validator/input mask 时通常只有 acceptable 输入才发 |
| 选择信号 | `selectionChanged()` | 选区变化时发出 | 可用于更新复制、剪切按钮状态 |
| 文本信号 | `textChanged(const QString &text)` | 文本改变时发出 | 程序 `setText()` 和用户输入都会触发，适合“内容已变化”同步 |
| 文本信号 | `textEdited(const QString &text)` | 用户编辑文本时发出 | 程序 `setText()` 不触发，适合标记用户改动或实时搜索 |

### 受保护函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 几何 | `cursorRect() const` | 返回当前光标所在矩形 | 做输入法候选窗、补全弹层、自定义提示定位时有用 |
| 样式 | `initStyleOption(QStyleOptionFrame *option) const` | 填充当前输入框的样式参数 | 自定义绘制时先调用它，避免丢失边框、焦点、禁用等平台状态 |

### 重写的受保护函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态变化 | `changeEvent(QEvent *event)` | 处理字体、语言、样式、调色板等变化 | 派生类缓存尺寸或文本布局时要在这里更新 |
| 菜单 | `contextMenuEvent(QContextMenuEvent *event)` | 处理右键菜单 | 扩展菜单时可基于 `createStandardContextMenu()`，不要忘记菜单所有权 |
| 拖放 | `dragEnterEvent(QDragEnterEvent *event)` | 处理拖入输入框 | 只接受能转换成合适文本且符合场景的拖拽数据 |
| 拖放 | `dragMoveEvent(QDragMoveEvent *event)` | 处理拖拽在控件内移动 | 常用于更新插入光标位置 |
| 拖放 | `dragLeaveEvent(QDragLeaveEvent *event)` | 处理拖拽离开输入框 | 清理临时插入点或高亮状态 |
| 拖放 | `dropEvent(QDropEvent *event)` | 处理放下文本 | 放入内容仍应走掩码、validator 和业务安全检查 |
| 焦点 | `focusInEvent(QFocusEvent *event)` | 处理获得焦点 | 常见行为包括显示光标、更新选择、触发输入法状态 |
| 焦点 | `focusOutEvent(QFocusEvent *event)` | 处理失去焦点 | 会影响 `editingFinished()` 时机和密码显示模式 |
| 输入法 | `inputMethodEvent(QInputMethodEvent *event)` | 处理输入法预编辑和提交文本 | 中文、日文等 IME 输入依赖它，派生类不要轻易吞掉事件 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 处理按键输入和编辑快捷键 | Enter、撤销、删除、光标移动、文本插入都在这条链路上 |
| 键盘 | `keyReleaseEvent(QKeyEvent *event)` | 处理按键释放 | 普通文本处理很少重写，除非有明确快捷交互 |
| 鼠标 | `mouseDoubleClickEvent(QMouseEvent *event)` | 处理双击选择 | 通常用于按词选择，不要破坏标准选择习惯 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *event)` | 处理拖动选择或拖拽启动 | 与 selection、dragEnabled、光标定位相关 |
| 鼠标 | `mousePressEvent(QMouseEvent *event)` | 处理鼠标按下定位光标 | 自定义点击行为时要兼容选区、焦点和输入法 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *event)` | 处理鼠标释放 | 链接鼠标选择完成、上下文状态更新等 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制边框、背景、文本、光标和选区 | 改外观优先考虑样式表；完整重绘要保留平台状态 |

---

### 一句话总结

`QLineEdit` 是单行文本编辑的底座：它负责真实文本、显示文本、校验、补全、选择、撤销、光标和输入法协作。
