# Qt QLabel 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QLabel>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QFrame -> QLabel`  
> 定位：文本、图片和轻量富文本展示控件

## 1. 先建立整体认识：它解决什么问题

`QLabel` 的主要任务是**展示内容**，不是让用户编辑内容。

它可以显示：

- 普通文本；
- 富文本；
- `QPixmap` 图片；
- `QPicture` 绘图记录；
- `QMovie` 动画；
- 整数或浮点数；
- 带链接的 HTML 片段。

它还承担两个很实用的界面职责：

- 给输入控件提供说明文字；
- 通过 mnemonic/buddy 让用户按快捷键跳到对应控件。

```text
姓名： [ QLineEdit ]
```

这里左边通常就是 `QLabel`，右边是它的 buddy。

## 2. 什么时候该用它

| 场景 | 用法 |
| --- | --- |
| 字段标题、说明文字 | 普通文本 |
| 图片预览、图标、状态图 | `setPixmap()` |
| 富文本帮助、带链接说明 | `setTextFormat(Qt::RichText)` |
| 动画提示 | `setMovie()` |
| 表单快捷键 | `setBuddy()` + 文本中的 `&` |
| 可复制的错误信息 | 文本交互标志 + 选择 API |

不要把 `QLabel` 当成编辑器。  
用户需要输入或修改文字时，应使用 `QLineEdit`、`QTextEdit` 或 `QPlainTextEdit`。

## 3. QLabel 的内容是互斥的

`QLabel` 同一时间主要展示一种内容。调用下面任意一种设置函数，都会清掉之前的内容：

- `setText()`
- `setPixmap()`
- `setPicture()`
- `setMovie()`
- `setNum()`

例如先 `setPixmap()`，再 `setText()`，图片就不再是当前内容。

## 4. 文本格式要主动指定

`QLabel` 会尝试猜测传入字符串是普通文本还是富文本。  
如果文本来自网络、配置文件或用户输入，不要完全依赖自动猜测。

```cpp
label->setTextFormat(Qt::PlainText);
label->setText(untrustedText);
```

显示自己控制的富文本时，可以明确写：

```cpp
label->setTextFormat(Qt::RichText);
label->setText("<b>提示：</b>请输入有效邮箱");
```

安全边界很重要：来自外部的数据如果不应该被解析成 HTML，就用 `Qt::PlainText`。

## 5. 最小可用代码

### 5.1 普通文本

```cpp
auto *label = new QLabel("用户名：", this);
label->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
```

### 5.2 图片

```cpp
auto *preview = new QLabel(this);
preview->setPixmap(QPixmap(":/images/logo.png"));
preview->setScaledContents(false);
preview->setAlignment(Qt::AlignCenter);
```

### 5.3 表单 buddy

```cpp
auto *nameLabel = new QLabel("&姓名：", this);
auto *nameEdit = new QLineEdit(this);
nameLabel->setBuddy(nameEdit);
```

用户按 `Alt+N` 时，焦点会跳到 `nameEdit`。  
实际快捷键由文本中 `&` 后面的字符决定。

### 5.4 可点击链接

```cpp
auto *help = new QLabel(
    "<a href=\"https://example.com/help\">查看帮助</a>", this);
help->setTextFormat(Qt::RichText);
help->setTextInteractionFlags(Qt::LinksAccessibleByMouse);
help->setOpenExternalLinks(false);

connect(help, &QLabel::linkActivated, this,
        [](const QString &url) {
            qDebug() << "用户点击了" << url;
        });
```

## 6. 对齐、换行、边距和缩放

### 6.1 `alignment`

它控制内容在 `QLabel` 自己矩形里的位置：

```cpp
label->setAlignment(Qt::AlignCenter);
```

这和布局里的 `alignment` 不是一回事：

- `QLayout` 的对齐控制控件在布局单元中的位置；
- `QLabel::alignment` 控制内容在控件内部的位置。

### 6.2 `wordWrap`

```cpp
label->setWordWrap(true);
```

它允许文本按词换行。对于中文等没有明显空格的文本，布局和字体仍会影响最终断行。

设置换行后，`heightForWidth()` 会让布局根据宽度计算合适高度。

### 6.3 `margin` 和 `indent`

- `margin`：内容四周统一留白；
- `indent`：在对齐方向上额外缩进。

如果只想让文字离左边远一点，通常先考虑 `indent` 或布局边距，不要随手把整个控件固定得很大。

### 6.4 `scaledContents`

图片标签开启后：

```cpp
label->setScaledContents(true);
```

图片会缩放去填满可用区域。  
它不保证保持原始比例，可能造成拉伸；需要保持比例时应自己先缩放 `QPixmap`，或使用更合适的绘制方案。

## 7. 文本交互：显示控件也可以被选中

默认 `QLabel` 不提供用户交互。  
要让用户选中文本或点击链接，需要设置 `textInteractionFlags`。

```cpp
label->setTextInteractionFlags(
    Qt::TextSelectableByMouse |
    Qt::LinksAccessibleByMouse);
```

常见组合：

| 需求 | 标志 |
| --- | --- |
| 鼠标选中文本 | `Qt::TextSelectableByMouse` |
| 键盘选中文本 | `Qt::TextSelectableByKeyboard` |
| 鼠标点击链接 | `Qt::LinksAccessibleByMouse` |
| 键盘访问链接 | `Qt::LinksAccessibleByKeyboard` |

只有打开相应选择标志后，`setSelection()`、`hasSelectedText()`、`selectedText()` 才有实际意义。

## 8. 外部链接和 `linkActivated`

默认 `openExternalLinks` 是 `false`。  
点击链接时，通常发出 `linkActivated()`，由程序决定怎么处理。

如果设置为 `true`，Qt 会尝试通过 `QDesktopServices::openUrl()` 打开外部链接，而不是只发信号。

因此：

- 想自己控制链接行为：保持 `false`；
- 想交给系统浏览器：设置为 `true`；
- 来自外部的链接仍然要做业务层审核。

## 9. `resourceProvider`：富文本资源从哪里来

Qt 6.1 起，`setResourceProvider()` 可以为富文本提供图片等资源。

它适合：

- 富文本中的图片来自自定义资源系统；
- 不想把资源全部写成文件路径；
- 需要集中处理富文本资源加载。

`QLabel` 不会替你管理 provider 的外部资源所有权，调用方要保证它在使用期间有效。

## API 速查表
### 属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 文本属性 | `text : QString` | 当前显示的文本内容 | 设置文本会替换图片、动画等其他内容；外部输入建议配合 `textFormat` 明确纯文本 |
| 文本属性 | `textFormat : Qt::TextFormat` | 指定文本按纯文本、富文本还是自动判断处理 | 不可信文本应设为 `Qt::PlainText`，避免被当成 HTML 解析 |
| 图片属性 | `pixmap : QPixmap` | 当前显示的图片内容 | 设置 pixmap 会清掉文本、movie、picture 等其他内容 |
| 图片属性 | `scaledContents : bool` | 是否把图片缩放到填满标签区域 | 不保证保持宽高比；需要等比显示时应先缩放 pixmap 或自定义绘制 |
| 布局属性 | `alignment : Qt::Alignment` | 控制内容在 label 内部的对齐 | 不是 layout 对齐；只影响内容在自身矩形中的位置 |
| 文本属性 | `wordWrap : bool` | 是否允许文本自动换行 | 开启后 `heightForWidth()` 会影响布局高度 |
| 边距属性 | `margin : int` | 内容四周统一留白 | 来自 `QFrame` 风格边界之外的内容边距，不要用固定大 margin 代替布局 |
| 边距属性 | `indent : int` | 内容在对齐方向上的额外缩进 | 常用于表单标签微调；比给控件固定宽度更灵活 |
| 链接属性 | `openExternalLinks : bool` | 是否自动用系统服务打开外部链接 | 设为 `true` 会绕过自己处理 `linkActivated` 的机会；外部 URL 仍要审核 |
| 交互属性 | `textInteractionFlags : Qt::TextInteractionFlags` | 控制是否可选中文本、点击链接、键盘访问链接 | 默认几乎不交互；要复制或点链接必须显式开启对应 flag |
| 选择属性 | `hasSelectedText : bool` | 只读属性，表示当前是否有选中文本 | 只有开启文本选择交互后通常才有意义 |
| 选择属性 | `selectedText : QString` | 只读属性，返回当前选中文本 | 可用于复制辅助逻辑；不要把敏感文本随意暴露到日志 |

### 成员函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QLabel(QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 创建空标签 | 创建后通过 `setText()`、`setPixmap()`、`setMovie()` 等设置内容 |
| 构造 | `QLabel(const QString &text, QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 创建时直接设置文本 | 适合静态字段名和说明文字；不可信文本仍要显式设置 `Qt::PlainText` |
| 生命周期 | `~QLabel()` | 销毁标签控件 | 通常由父对象自动销毁 |
| 文本 | `text() const` / `setText(const QString &text)` | 读取或设置文本内容 | 设置文本会清掉图片、动画、picture 等当前内容 |
| 图片 | `pixmap() const` / `setPixmap(const QPixmap &pixmap)` | 读取或设置图片内容 | 设置 pixmap 会替换其他内容；Qt 6.6 前后存在兼容返回值重载 |
| 绘图记录 | `picture() const` / `setPicture(const QPicture &picture)` | 读取或设置 `QPicture` 绘图记录 | 需要启用 picture 支持；普通图片预览优先用 pixmap |
| 动画 | `movie() const` / `setMovie(QMovie *movie)` | 读取或设置动画对象 | 需要启用 movie 支持；`QLabel` 不接管 `QMovie` 的外部资源所有权，调用方要保证生命周期 |
| 文本格式 | `textFormat() const` / `setTextFormat(Qt::TextFormat format)` | 查询或设置文本解析方式 | 外部字符串用 `Qt::PlainText`，自己控制的 HTML 才用 `Qt::RichText` |
| 富文本资源 | `resourceProvider() const` / `setResourceProvider(const QTextDocument::ResourceProvider &provider)` | 查询或设置富文本资源提供器 | Qt 6.1 起用于自定义富文本图片等资源加载；provider 捕获的对象要保持有效 |
| 对齐 | `alignment() const` / `setAlignment(Qt::Alignment alignment)` | 查询或设置内容在 label 内的对齐 | 和布局对齐不同，只管 label 内部内容位置 |
| 换行 | `wordWrap() const` / `setWordWrap(bool on)` | 查询或设置文本自动换行 | 开启后 label 高度会随宽度变化，布局会调用 `heightForWidth()` |
| 缩进 | `indent() const` / `setIndent(int indent)` | 查询或设置内容缩进 | 常用于表单标签和边框内文字微调 |
| 边距 | `margin() const` / `setMargin(int margin)` | 查询或设置内容四周边距 | 影响文本和图片内容区域，不是布局间距 |
| 图片缩放 | `hasScaledContents() const` / `setScaledContents(bool enable)` | 查询或设置图片是否拉伸填满标签 | 可能拉伸变形；等比缩放要自己处理 pixmap 尺寸 |
| 尺寸 | `sizeHint() const` | 返回推荐尺寸 | 内容类型、字体、换行、图片大小都会影响结果 |
| 尺寸 | `minimumSizeHint() const` | 返回最小推荐尺寸 | 布局压缩时参考它，长文本换行场景尤其重要 |
| 快捷伙伴 | `setBuddy(QWidget *buddy)` / `buddy() const` | 设置或读取 mnemonic 快捷键跳转的伙伴控件 | 文本中的 `&` 决定快捷键；需要启用 shortcut 支持 |
| 高宽关联 | `heightForWidth(int width) const` | 根据给定宽度计算所需高度 | `wordWrap=true` 时特别关键，帮助布局正确分配高度 |
| 链接 | `openExternalLinks() const` / `setOpenExternalLinks(bool open)` | 查询或设置是否自动打开外部链接 | 想统一审核或内部路由链接时保持 `false` 并处理 `linkActivated()` |
| 交互 | `textInteractionFlags() const` / `setTextInteractionFlags(Qt::TextInteractionFlags flags)` | 查询或设置文本选择、链接访问等交互能力 | 不开启相应 flag，选择和链接 API 通常没有实际效果 |
| 选择 | `setSelection(int start, int length)` | 选择指定范围的文本 | 需要文本可选择；对图片、动画内容没有意义 |
| 选择 | `hasSelectedText() const` | 查询当前是否有选中文本 | 只有文本内容和交互 flag 支持时才有意义 |
| 选择 | `selectedText() const` | 读取当前选中文本 | 适合自定义复制逻辑；无选区时为空 |
| 选择 | `selectionStart() const` | 读取选区起点 | 没有选区时返回 `-1` |

### 公共槽

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 文本槽 | `setText(const QString &text)` | 把标签内容切换为文本 | 会清掉图片、动画等其他内容 |
| 图片槽 | `setPixmap(const QPixmap &pixmap)` | 把标签内容切换为图片 | 大图不会自动等比适配；结合 `scaledContents` 时注意变形 |
| 绘图槽 | `setPicture(const QPicture &picture)` | 把标签内容切换为绘图记录 | 适合回放 Qt 绘图命令，普通 UI 少用 |
| 动画槽 | `setMovie(QMovie *movie)` | 把标签内容切换为动画 | 不要传生命周期马上结束的临时 movie |
| 数字槽 | `setNum(int number)` | 将整数转为文本显示 | 只是便捷显示，不建立数值绑定 |
| 数字槽 | `setNum(double number)` | 将浮点数转为文本显示 | 使用默认格式转换；需要精度控制时自己格式化字符串 |
| 内容槽 | `clear()` | 清空当前内容 | 文本、图片、动画等当前展示都会被移除 |

### 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 链接信号 | `linkActivated(const QString &link)` | 用户激活富文本链接时发出 | `openExternalLinks=false` 时常用它自行路由或审核链接 |
| 链接信号 | `linkHovered(const QString &link)` | 鼠标悬停在链接上时发出 | 可用于状态栏预览 URL 或安全提示 |

### 重写的受保护函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `event(QEvent *event)` | 处理标签通用事件入口 | 普通使用不调用；交互文本、tooltip、shortcut 等会经过这里 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 处理键盘选择和链接访问 | 只有启用相应文本交互 flag 后才常需要关心 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制文本、图片、动画和 frame | 自定义展示控件时重写；普通样式调整优先用属性和样式表 |
| 状态变化 | `changeEvent(QEvent *event)` | 处理样式、字体、语言等变化 | 缓存文本布局、图片尺寸时要响应这些变化 |
| 鼠标 | `mousePressEvent(QMouseEvent *event)` | 处理鼠标按下 | 与文本选择、链接按下、焦点进入有关 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *event)` | 处理鼠标移动 | 用于文本选择拖动和链接 hover 状态 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *event)` | 处理鼠标释放 | 常在这里完成链接激活或选择结束 |
| 菜单 | `contextMenuEvent(QContextMenuEvent *event)` | 处理右键菜单 | 文本可选时可能出现复制菜单；自定义菜单要注意交互 flag |
| 焦点 | `focusInEvent(QFocusEvent *event)` | 处理获得焦点 | 链接键盘访问和文本选择可让 label 需要焦点 |
| 焦点 | `focusOutEvent(QFocusEvent *event)` | 处理失去焦点 | 清理键盘导航、选择视觉等状态 |
| 焦点 | `focusNextPrevChild(bool next)` | 处理焦点前后切换 | 有 buddy、链接或可键盘选择文本时影响 Tab 链路 |

---

### 一句话总结

`QLabel` 是轻量展示控件：文本、图片、动画、链接和表单快捷键都能处理，但它始终不是文本编辑器。
