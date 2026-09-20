# QLabel

> Qt 6.11.1 · Qt Widgets · 来自 `QLabel`

## 1. 先建立直觉

### 这是什么

`QLabel` 是 Widgets 中最常用的展示控件：它可以显示普通文本、富文本、链接、图片、动画和 `QPicture`，也可以作为表单字段的标签，通过 buddy 机制把助记符焦点转给另一个控件。

它不是“只能放几个字”的控件。`QLabel` 的复杂度主要来自内容模式：文本模式、pixmap 模式、movie 模式、picture 模式互相替换；设置新内容通常会清掉旧内容。理解这一点，才能避免“为什么图片没了”“为什么 buddy 失效”“为什么富文本变可交互”这些问题。

### 适合使用的场景

- 表单字段标签、说明文字、状态文字、错误提示。
- 显示小图标、预览缩略图、简单动画。
- 显示少量富文本或链接。
- 给输入控件设置带助记符的 buddy 标签。

### 不适合的场景

- 多行可编辑文本用 `QTextEdit` 或 `QPlainTextEdit`。
- 大型富文本文档用只读 `QTextEdit`，不要塞进 `QLabel`。
- 大量列表/表格数据用模型视图，不要创建成千上万个 label。
- 需要按钮行为时用按钮类，不要让 label 伪装成按钮。

### 最小示例

```cpp
auto *nameEdit = new QLineEdit(this);
auto *label = new QLabel(tr("&Name:"), this);
label->setBuddy(nameEdit);
label->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
```

用户按下标签助记符时，焦点会转到 `nameEdit`。这就是 `QLabel` 在表单里真正有价值的地方之一。

## 2. 依赖与对象关系

- 头文件：`#include <QLabel>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QFrame`
- 直接派生类：类页未列出

### 内容模式

`QLabel` 一次主要显示一种内容：`text`、`pixmap`、`movie`、`picture`。调用 `setText()` 会清除之前的图片/动画内容；调用 `setPixmap()` 也会清除文本内容。

### 和 QFrame 的关系

因为继承 `QFrame`，`QLabel` 可以有 frame shape、shadow、line width 等边框能力。`margin` 和 `indent` 又会影响内容在 frame 内部的位置。

### 和输入控件的关系

`setBuddy()` 让 label 成为另一个控件的说明标签。文本中的 `&` 定义助记符，触发后焦点交给 buddy。这对键盘操作和可访问性都很重要。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `alignment : Qt::Alignment` | 控制内容在标签区域内的对齐方式。 |
| `indent : int` | 文本缩进，受对齐方向和 frame width 影响。 |
| `margin : int` | 内容和 frame 内边缘之间的空白。 |
| `text : QString` | 标签文本，可为纯文本或富文本。 |
| `textFormat : Qt::TextFormat` | 指定纯文本、富文本或自动识别。 |
| `wordWrap : bool` | 是否自动换行。 |
| `textInteractionFlags : Qt::TextInteractionFlags` | 控制文本是否可选、链接是否可点击等交互。 |
| `openExternalLinks : bool` | 是否自动用 `QDesktopServices::openUrl()` 打开链接。 |
| `hasSelectedText : bool` / `selectedText : QString` | 查询用户选中的文本。 |
| `pixmap : QPixmap` | 当前显示的 pixmap 内容。 |
| `scaledContents : bool` | 是否把 pixmap 缩放填满标签区域。 |
| `QLabel(...)` | 创建空标签或文本标签。 |
| `~QLabel()` | 销毁标签。 |
| `setText()` / `text()` | 设置或读取文本内容。 |
| `setPixmap()` / `pixmap()` | 设置或读取图片内容。 |
| `setMovie()` / `movie()` | 设置或读取动画内容。 |
| `setPicture()` / `picture()` | 设置或读取 `QPicture` 内容。 |
| `setNum(int)` / `setNum(double)` | 把数字转换为文本显示。 |
| `clear()` | 清除当前内容。 |
| `setBuddy(QWidget *)` / `buddy() const` | 设置或读取助记符目标控件。 |
| `setSelection(start, length)` / `selectionStart()` | 设置或读取文本选择。 |
| `setResourceProvider()` / `resourceProvider()` | Qt 6.1 起，为富文本资源提供自定义加载器。 |
| `heightForWidth(int)` | 自动换行文本按宽度计算高度。 |
| `sizeHint()` / `minimumSizeHint()` | 返回推荐尺寸。 |
| `linkActivated(QString)` / `linkHovered(QString)` | 链接激活或悬停时发出。 |
| `paintEvent()` | 绘制文本、图片、动画帧或边框。 |
| `event()` / `changeEvent()` | 处理通用事件与状态变化。 |
| `contextMenuEvent()` | 文本可交互时的上下文菜单入口。 |
| `focusInEvent()` / `focusOutEvent()` / `focusNextPrevChild()` | 文本可键盘选择或链接可访问时处理焦点。 |
| `keyPressEvent()` / `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()` | 文本选择、链接交互等输入事件。 |

## 4. API 逐项说明

### `alignment`

控制内容在标签矩形中的位置，常见组合是 `Qt::AlignLeft | Qt::AlignVCenter`、`Qt::AlignRight | Qt::AlignVCenter`、`Qt::AlignCenter`。

它影响的是内容整体，不是富文本内部每个段落的排版。富文本内部排版应由 HTML/CSS 子集控制。

### `indent` / `margin`

`margin` 是内容和 frame 内边缘之间的四周空白；`indent` 是沿对齐方向的文本缩进。`indent` 默认 `-1`，表示 Qt 根据 frame width 和字体估算。

普通表单标签通常不需要手动设置这两个值；需要边框提示或小型状态框时才常用。

### `text` / `textFormat`

`setText()` 设置文本，并清除旧的非文本内容。默认 `Qt::AutoText` 会自动判断是否按富文本解释。

如果文本来自用户、日志、文件名或网络内容，建议显式 `setTextFormat(Qt::PlainText)`，避免类似 `<b>...</b>` 的内容被当成富文本。需要显示富文本时，再明确使用 `Qt::RichText`。

### `wordWrap`

开启后文本会按可用宽度换行，并通过 `heightForWidth()` 把“宽度影响高度”的关系告诉布局。

说明文字和错误提示常开启；字段标签一般不开启，除非你愿意表单行高随窗口宽度变化。

### `textInteractionFlags`

控制用户能否选择文本、点击链接、通过键盘访问链接。默认通常允许鼠标访问链接。

开启键盘链接访问或键盘文本选择时，label 可能获得焦点策略。界面上要能看出焦点在哪里，否则键盘用户会迷路。

### `openExternalLinks`

为真时，点击链接会直接调用 `QDesktopServices::openUrl()`；为假时，发出 `linkActivated()`，由你决定怎么处理。

外部内容里的链接不要随便自动打开。需要审计、拦截、记录或只允许内部协议时，应关闭自动打开并连接 `linkActivated()`。

### `hasSelectedText` / `selectedText` / `setSelection()` / `selectionStart()`

这些 API 只有在交互标志允许文本选择时才有实际意义。`setSelection(start, length)` 可以程序化选择一段文本。

如果只是显示状态文字，不要开启文本选择；如果是错误详情、路径、ID 等用户可能要复制的文本，开启选择会很贴心。

### `pixmap` / `setPixmap()`

显示 `QPixmap`。设置 pixmap 会清除文本、movie 等其他内容，并禁用 buddy 快捷语义。

高 DPI 下要注意 pixmap 的 device pixel ratio。不要把大图原样塞进 label 再依赖 `scaledContents` 粗暴缩放；预先按目标尺寸准备更清晰。

### `scaledContents`

开启后，pixmap 会缩放填满标签可用区域。它简单但可能拉伸变形，因为不保证保持宽高比。

展示头像、缩略图时，通常更推荐自己按比例缩放 pixmap，再设置给 label。

### `setMovie()` / `movie()`

显示 `QMovie` 动画，例如 GIF。label 不拥有 movie 的全部业务生命周期，通常应给 movie 合适 parent。

动画会带来持续重绘，列表里大量动画 label 会影响性能。

### `setPicture()` / `picture()`

显示 `QPicture` 记录的绘图命令。这个 API 使用频率不高，更多出现在需要重放 Qt 绘制指令的场景。

Qt 6.0 起提供 `picture()` 读取。

### `setNum(int)` / `setNum(double)`

把数字转换成文本显示。它是便利槽函数，适合直接连接数值变化信号。

需要本地化格式、小数位控制、单位拼接时，自己格式化字符串再 `setText()` 更明确。

### `clear()`

清除当前内容。无论当前是文本、图片还是其他内容，都会回到空标签状态。

清空后 size hint 可能变化，布局会重新计算。

### `setBuddy(QWidget *buddy)` / `buddy() const`

设置标签助记符目标。文本中的 `&` 定义快捷键，触发时焦点移动到 buddy。

表单里使用 `QFormLayout::addRow(QString, QWidget*)` 会自动创建 label 并设置 buddy；手写布局时要自己调用。

### `setResourceProvider()` / `resourceProvider()`

Qt 6.1 起，可为富文本资源提供自定义加载方式，例如控制 `<img>` 资源如何解析。

这适合受控的富文本展示；不要把它变成任意文件或网络资源加载入口，安全边界要清楚。

### `heightForWidth()` / `sizeHint()` / `minimumSizeHint()`

这些函数向布局报告标签希望占用的大小。文本换行、图片尺寸、frame、margin、indent 都会影响结果。

如果 label 把布局撑得很宽，检查长文本是否未换行；如果高度频繁变化，检查 word wrap 和富文本内容。

### `linkActivated()` / `linkHovered()`

当用户激活或悬停链接时发出。只有文本格式和交互标志允许链接时才有意义。

内部帮助链接、设置跳转、文档链接通常连接 `linkActivated()` 自己处理，比直接开启外部链接更可控。

### 事件与绘制函数

`paintEvent()` 绘制当前内容；鼠标和键盘事件处理文本选择、链接激活、焦点移动；`contextMenuEvent()` 可在可选文本上提供复制等菜单。

普通使用不需要重写这些函数。自定义 label 交互时，要先确认是不是应该改用按钮、文本编辑器或自定义 widget。

## 5. 深入实践与常见坑

### AutoText 方便也危险

`Qt::AutoText` 会把看起来像富文本的字符串按富文本渲染。显示外部输入时显式使用 `Qt::PlainText`，这是最省心的防线。

### Label 可以是表单可访问性的关键

`setBuddy()` 让标签和字段建立关系。没有 buddy 的表单标签只是旁边一段文字；有 buddy 的标签能参与键盘导航。

### 图片缩放要考虑比例和高 DPI

`scaledContents` 只是填满区域。需要专业观感时，自己按 `KeepAspectRatio` 缩放，并准备高 DPI pixmap。

### QLabel 不是富文本浏览器

小段富文本可以，长文档、滚动、复杂交互、选择复制体验都应该交给只读 `QTextEdit` 或专门视图。
