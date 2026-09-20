# Qt Widgets 基础（上）：显示、按钮与文本输入

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Widgets  
> 核心类型：`QLabel`、`QAbstractButton`、`QPushButton`、`QToolButton`、`QCheckBox`、`QRadioButton`、`QButtonGroup`、`QLineEdit`、`QTextEdit`、`QPlainTextEdit`

## 1. 按用户意图选择控件

| 用户任务 | 推荐控件 |
|---|---|
| 显示短文本、图片或伙伴标签 | `QLabel` |
| 执行明确命令 | `QPushButton` / `QAction` |
| 紧凑工具命令 | `QToolButton` |
| 独立开关或多选 | `QCheckBox` |
| 少量互斥选项 | `QRadioButton` |
| 给多个按钮统一分组、映射 ID | `QButtonGroup` |
| 单行文本 | `QLineEdit` |
| 富文本编辑 | `QTextEdit` |
| 大量纯文本或日志 | `QPlainTextEdit` |

先根据交互语义选类，再调整样式。不要把可点击 QLabel 伪装成按钮，也不要用多行编辑器承载普通单行字段。

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. 最小可用代码：登录表单

```cpp
#include <QApplication>
#include <QCheckBox>
#include <QFormLayout>
#include <QLabel>
#include <QLineEdit>
#include <QMessageBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("登录");

    auto *nameEdit = new QLineEdit;
    nameEdit->setPlaceholderText("用户名");
    nameEdit->setClearButtonEnabled(true);

    auto *passwordEdit = new QLineEdit;
    passwordEdit->setEchoMode(QLineEdit::Password);

    auto *remember = new QCheckBox("记住我");
    auto *login = new QPushButton("登录");
    login->setDefault(true);

    auto *form = new QFormLayout;
    form->addRow("用户名：", nameEdit);
    form->addRow("密码：", passwordEdit);

    auto *layout = new QVBoxLayout(&window);
    layout->addLayout(form);
    layout->addWidget(remember);
    layout->addWidget(login);

    QObject::connect(login, &QPushButton::clicked,
                     &window, [=, &window] {
        if (nameEdit->text().trimmed().isEmpty()) {
            QMessageBox::warning(&window, "登录", "请输入用户名");
            nameEdit->setFocus();
            return;
        }
        QMessageBox::information(&window, "登录", "输入已提交");
    });

    window.resize(360, 210);
    window.show();
    return app.exec();
}
```

密码的隐藏显示只保护屏幕观察，不等于安全存储或安全传输。业务层仍需正确处理凭据。

## 4. QLabel：显示而不是编辑

```cpp
auto *label = new QLabel(tr("连接成功"), parent);
label->setAlignment(Qt::AlignCenter);
label->setWordWrap(true);
```

QLabel 可显示：

- 普通文本；
- 富文本；
- Pixmap；
- Movie 动画；
- 数字。

### 4.1 文本格式

```cpp
label->setTextFormat(Qt::PlainText);
label->setText(userProvidedText);
```

默认 `AutoText` 会猜测字符串是否富文本。如果文本来自用户或外部数据，应明确用 `PlainText`，避免内容被当作 HTML 解释。

需要富文本时：

```cpp
label->setTextFormat(Qt::RichText);
label->setText("<b>警告：</b>文件不存在");
```

### 4.2 图片与缩放

```cpp
label->setPixmap(pixmap);
label->setAlignment(Qt::AlignCenter);
```

`setScaledContents(true)` 会强行把内容拉伸到 Label 尺寸，可能破坏比例并在每次调整时重采样。通常先按目标尺寸和 `KeepAspectRatio` 生成合适 Pixmap。

### 4.3 伙伴控件与快捷键

```cpp
auto *nameLabel = new QLabel(tr("&用户名："));
auto *nameEdit = new QLineEdit;
nameLabel->setBuddy(nameEdit);
```

用户按平台对应的 Alt+U 时，焦点移动到伙伴输入框。`&` 标记助记键；要显示文字 `&` 应写 `&&`。

### 4.4 文本选择和链接

```cpp
label->setTextInteractionFlags(
    Qt::TextSelectableByMouse |
    Qt::LinksAccessibleByMouse);
label->setOpenExternalLinks(false);
```

外部链接最好监听 `linkActivated()` 后自行校验协议和目标，再决定是否打开。不要无条件允许不可信内容启动任意 URL。

## 5. QAbstractButton：按钮共同模型

`QPushButton`、`QToolButton`、`QCheckBox`、`QRadioButton` 都继承它，共享：

```cpp
button->setText("执行");
button->setIcon(icon);
button->setCheckable(true);
button->setChecked(false);
button->setAutoRepeat(false);
button->setShortcut(QKeySequence("Alt+R"));
```

常用信号：

| 信号 | 时机 |
|---|---|
| `pressed()` | 按下时 |
| `released()` | 释放时 |
| `clicked(bool)` | 完成一次有效点击时 |
| `toggled(bool)` | checkable 状态改变时 |

大多数命令连接 `clicked()`；持续按压反馈才使用 pressed/released；状态模型连接 toggled。

程序调用 `setChecked()` 会发出 `toggled()`，但不会伪造用户 `clicked()`。这一区别适合区分状态变化和用户意图。

## 6. QPushButton：明确命令

```cpp
auto *save = new QPushButton(QIcon::fromTheme("document-save"),
                             tr("保存"));
connect(save, &QPushButton::clicked,
        this, &Editor::save);
```

按钮文本使用动词或明确结果，例如“保存”“重新连接”，不要只写模糊的“确定”而让用户猜结果。

### 6.1 default 与 autoDefault

在 QDialog 中，默认按钮响应 Enter：

```cpp
save->setDefault(true);
cancel->setAutoDefault(false);
```

对话框按钮默认可能启用 autoDefault，获得焦点后成为 Enter 目标，并为默认边框预留空间。破坏性操作不要设为默认按钮。

### 6.2 按钮菜单

```cpp
auto *menu = new QMenu(button);
menu->addAction(tr("导出 PNG"));
menu->addAction(tr("导出 JPEG"));
button->setMenu(menu);
```

`setMenu()` 不接管菜单所有权，因此示例把 menu 的 parent 设为 button。只有相关命令集合才用菜单按钮；主要动作和下拉扩展并存时，考虑专用分裂按钮交互或工具按钮模式。

## 7. QToolButton：紧凑工具命令

```cpp
auto *button = new QToolButton;
button->setDefaultAction(saveAction);
button->setToolButtonStyle(Qt::ToolButtonIconOnly);
button->setPopupMode(QToolButton::MenuButtonPopup);
```

常见 popup mode：

- `DelayedPopup`：按住后弹菜单；
- `MenuButtonPopup`：主体执行默认动作，箭头弹菜单；
- `InstantPopup`：点击立即弹菜单，不执行默认动作。

只显示图标时设置 tooltip，并使用可辨识图标。工具栏通常直接 `addAction()`，让工具栏自动创建 ToolButton。

## 8. QCheckBox：独立布尔或三态

```cpp
auto *check = new QCheckBox(tr("自动保存"));
connect(check, &QCheckBox::toggled,
        settings, &Settings::setAutoSave);
```

适合彼此独立、可以同时选择多个的选项。

### 8.1 三态

```cpp
check->setTristate(true);
check->setCheckState(Qt::PartiallyChecked);
```

三种状态：

- `Unchecked`；
- `PartiallyChecked`；
- `Checked`。

部分选中常表示“多个子项值不一致”，不应随意用作第三个业务枚举值。

Qt 6.7 起可连接类型明确的信号：

```cpp
connect(check, &QCheckBox::checkStateChanged,
        this, &Panel::applyCheckState);
```

只关心二态时使用 `toggled(bool)`。

## 9. QRadioButton：互斥单选

同一父控件下的 RadioButton 默认 autoExclusive：

```cpp
auto *small = new QRadioButton(tr("小"), groupBox);
auto *large = new QRadioButton(tr("大"), groupBox);
small->setChecked(true);
```

应确保组内有合理初始选择，除非“未选择”本身是合法状态。

同一父控件中需要多组互斥选项时，使用多个 `QButtonGroup`，不要依赖创建顺序或视觉间距分组。

## 10. QButtonGroup：逻辑分组，不是视觉容器

```cpp
enum class Quality { Low = 0, Medium = 1, High = 2 };

auto *group = new QButtonGroup(this);
group->addButton(lowButton, int(Quality::Low));
group->addButton(mediumButton, int(Quality::Medium));
group->addButton(highButton, int(Quality::High));

connect(group, &QButtonGroup::idClicked,
        this, [](int id) {
    auto quality = Quality(id);
    applyQuality(quality);
});
```

- 默认 exclusive 为 true；
- ID `-1` 保留表示没有对应按钮；
- ButtonGroup 是 QObject，不负责绘制边框或排列按钮；
- 视觉分组用 `QGroupBox` 和 Layout；
- 加入 ButtonGroup 不会改变按钮的 QObject parent 或所有权。

## 11. QLineEdit：单行文本模型

```cpp
auto *edit = new QLineEdit;
edit->setPlaceholderText(tr("搜索"));
edit->setClearButtonEnabled(true);
edit->setMaxLength(100);
```

占位文字不是标签：字段已有内容时会消失，也不应承担必填、单位或格式说明。正式表单仍要配 QLabel。

## 12. textChanged 与 textEdited

```cpp
connect(edit, &QLineEdit::textChanged,
        this, &Panel::onAnyTextChange);

connect(edit, &QLineEdit::textEdited,
        this, &Panel::onUserEdit);
```

- `textChanged`：用户输入和 `setText()` 都触发；
- `textEdited`：只在用户编辑时触发。

从模型刷新界面时如果连接 textChanged 又反写模型，容易形成反馈回路。可使用 textEdited 表达用户意图，或在程序批量更新时用 `QSignalBlocker`。

```cpp
QSignalBlocker blocker(edit);
edit->setText(model.name());
```

## 13. returnPressed 与 editingFinished

```cpp
connect(edit, &QLineEdit::returnPressed,
        this, &Panel::submit);
connect(edit, &QLineEdit::editingFinished,
        this, &Panel::commitField);
```

`editingFinished` 通常在内容修改后失去焦点，或按 Enter 时发出；没有修改就失焦时不一定发出。

设置 Validator 或 Mask 后，Enter 引发的 `returnPressed` / `editingFinished` 只有在输入达到 Acceptable 时才发出。不能只依赖“用户按了 Enter”推断提交信号必到达。

## 14. 输入验证的三层

### 14.1 长度

```cpp
edit->setMaxLength(32);
```

长度不等于业务合法性。

### 14.2 Input Mask

适合固定位置格式：

```cpp
edit->setInputMask("0000-00-00;_");
```

Mask 控制字符位置，但不保证日期如 2025-99-99 在业务上有效。

### 14.3 Validator

```cpp
auto *validator = new QIntValidator(1, 65535, edit);
edit->setValidator(validator);
```

Validator 状态：

- `Acceptable`：可最终提交；
- `Intermediate`：编辑过程合理但尚未完成；
- `Invalid`：当前输入不可接受。

```cpp
if (!edit->hasAcceptableInput())
    showInlineError();
```

UI Validator 改善输入体验，但服务端或业务层仍必须再次验证。

## 15. 密码模式

```cpp
password->setEchoMode(QLineEdit::Password);
```

模式包括 `Normal`、`NoEcho`、`Password`、`PasswordEchoOnEdit`。

注意：

- `text()` 仍返回真实内容；
- `displayText()` 返回屏幕显示形式；
- 避免写入日志、崩溃报告和剪贴板；
- 不能仅靠控件掩码保护进程内存；
- 不可信页面或插件仍可能访问应用内对象。

## 16. 输入操作与附加 Action

```cpp
QAction *searchAction = edit->addAction(
    QIcon::fromTheme("edit-find"), QLineEdit::LeadingPosition);
connect(searchAction, &QAction::triggered,
        this, &Panel::startSearch);
```

尾部可放清除、显示密码等图标动作。熟悉图标提供 tooltip 和可访问名称。

剪贴板操作：

```cpp
edit->selectAll();
edit->copy();
edit->cut();
edit->paste();
```

只读不等于禁用：`setReadOnly(true)` 允许选择和复制，更适合展示可复制的不可编辑值。

## 17. QCompleter

```cpp
auto *completer = new QCompleter(cities, edit);
completer->setCaseSensitivity(Qt::CaseInsensitive);
completer->setCompletionMode(QCompleter::PopupCompletion);
edit->setCompleter(completer);
```

若同时使用 Validator，补全模型中的候选也必须合法。大数据集应使用模型并正确配置排序/过滤，而不是每次击键重建全部字符串列表。

## 18. QTextEdit 与 QPlainTextEdit

| 特性 | `QTextEdit` | `QPlainTextEdit` |
|---|---|---|
| 内容 | 富文本和纯文本 | 纯文本 |
| 底层 | QTextDocument | 针对段落/行优化 |
| 图片、表格、格式 | 支持 | 不支持富文本布局 |
| 大日志 | 通常不是首选 | 更合适 |
| 语法高亮 | 支持 | 常与 QSyntaxHighlighter 搭配 |

仅需要纯文本时优先 QPlainTextEdit，语义更明确、处理大型文档更高效。

## 19. QTextEdit：富文本

```cpp
auto *editor = new QTextEdit;
editor->setAcceptRichText(true);
editor->setHtml("<h2>标题</h2><p>正文</p>");
```

读取：

```cpp
QString plain = editor->toPlainText();
QString html = editor->toHtml();
QTextDocument *document = editor->document();
```

外部 HTML 可能引用资源或包含不需要的格式。粘贴和加载不可信富文本时应按业务限制内容；只要纯文本就设置：

```cpp
editor->setAcceptRichText(false);
```

### 19.1 QTextCursor

```cpp
QTextCursor cursor = editor->textCursor();
cursor.movePosition(QTextCursor::End);
cursor.insertText("追加内容\n");
editor->setTextCursor(cursor);
```

复杂编辑应使用 Cursor 和 Document API，而不是反复 `toHtml()`、拼字符串、`setHtml()`，后者会重建文档并破坏撤销栈和光标。

## 20. QPlainTextEdit：日志和代码

```cpp
auto *log = new QPlainTextEdit;
log->setReadOnly(true);
log->setMaximumBlockCount(5000);
log->appendPlainText(message);
```

`maximumBlockCount` 自动丢弃最早段落，可防止长期日志界面无限占用内存。它按文本块限制，不等同于严格的视觉行数。

### 20.1 保持滚动体验

新日志到达时不应总把正在查看历史的用户拉到底部。先判断滚动条是否接近末端，只在用户原本位于末端时自动跟随。

### 20.2 extraSelections

无需修改文档格式即可高亮当前行、搜索结果或错误区域：

```cpp
QTextEdit::ExtraSelection selection;
selection.cursor = textCursor();
selection.format.setBackground(QColor("#fff3b0"));
editor->setExtraSelections({selection});
```

## 21. 撤销、重做与只读

```cpp
editor->setUndoRedoEnabled(true);
connect(editor, &QPlainTextEdit::undoAvailable,
        undoAction, &QAction::setEnabled);
connect(editor, &QPlainTextEdit::redoAvailable,
        redoAction, &QAction::setEnabled);
```

菜单和工具栏复用同一 QAction。程序整体替换文档内容可能清空撤销历史；模型刷新与用户编辑要采用明确策略。

`setReadOnly(true)` 仍可允许选择、复制和滚动；`setEnabled(false)` 会阻止交互并显示禁用样式。

## 22. 防止信号反馈回路

典型回路：

```text
用户修改控件 → textChanged → 更新模型
模型发出 changed → setText → textChanged → 再更新模型
```

解决方式：

1. 用户意图使用 `textEdited()`；
2. 模型先比较新旧值，无变化不发信号；
3. 程序同步时使用 `QSignalBlocker`；
4. 表单采用“编辑缓冲，点击应用后统一提交”；
5. 不在每个字符变化时执行昂贵持久化。

## 23. 可访问性与键盘操作

- QLabel 使用 buddy 关联字段；
- 图标按钮设置 tooltip 和 accessibleName；
- 逻辑顺序设置合理 Tab order；
- 不只用颜色表达错误；
- 焦点框保持可见；
- RadioButton、CheckBox 使用原生控件语义，不用自绘 Label 模拟；
- 快捷键避免与文本输入和系统组合键冲突。

## 24. 常见错误

### 24.1 AutoText 显示外部字符串

内容可能被误识别为富文本。外部纯文本显式设置 `Qt::PlainText`。

### 24.2 把 placeholder 当字段标签

用户输入后说明消失，可访问性也受影响。使用持久 QLabel。

### 24.3 所有变化都连 textChanged

程序回填也触发，容易回路。用户输入使用 textEdited，提交使用 editingFinished 或明确按钮。

### 24.4 只依赖 Validator 保护业务

Validator 只是 UI 层约束。保存、网络和服务边界仍要验证。

### 24.5 RadioButton 没有初始选择

exclusive 只保证选中后互斥，不会自动替你选择合理默认值。

### 24.6 认为 QButtonGroup 是可见容器

它只管理逻辑关系，不布局、不绘制、不改变按钮 parent。视觉分组使用 QGroupBox。

### 24.7 用 QTextEdit 显示无限日志

富文本布局成本和无界文档增长会拖慢程序。使用 QPlainTextEdit，并限制 block 数。

### 24.8 用 setText 重建编辑器每次更新

光标、选择、撤销历史和滚动位置可能丢失。增量修改使用 QTextCursor 或 append API。

## 25. API 速查表

| API / 信号 | 用途 | 注意点 |
|---|---|---|
| `QLabel::setTextFormat()` | 明确纯/富文本 | 外部文本用 PlainText |
| `QLabel::setBuddy()` | 标签助记键定位字段 | 文本中用 `&` |
| `clicked()` | 完整按钮点击 | 普通命令首选 |
| `toggled(bool)` | checkable 状态变化 | setChecked 也会触发 |
| `QPushButton::setDefault()` | 对话框 Enter 默认动作 | 避免破坏性默认值 |
| `QButtonGroup::idClicked()` | 按 ID 处理选项 | -1 保留 |
| `QLineEdit::text()` | 真实文本 | 密码模式也返回真实值 |
| `textChanged()` | 任意来源变化 | setText 也触发 |
| `textEdited()` | 用户编辑 | 程序设置不触发 |
| `editingFinished()` | 编辑提交时机 | Validator 非 Acceptable 时受限 |
| `hasAcceptableInput()` | 查询最终输入是否可接受 | 提交时检查 |
| `setReadOnly()` | 可选择但不可编辑 | 不同于禁用 |
| `QTextEdit::document()` | 访问富文本文档 | 复杂操作用 Cursor |
| `appendPlainText()` | 追加纯文本块 | 适合日志 |
| `setMaximumBlockCount()` | 限制文档块数 | 控制长期内存 |

## 26. 自测题

### 题 1：textChanged 和 textEdited 的区别

<details><summary>答案</summary>

textChanged 对用户和程序修改都发出；textEdited 只对用户编辑发出。模型回填避免反馈回路时常用后者。
</details>

### 题 2：QButtonGroup 是否拥有按钮

<details><summary>答案</summary>

不会因 addButton 改变按钮的 QObject parent，也不负责视觉布局。按钮仍由其 Widget 父对象拥有。
</details>

### 题 3：密码模式是否加密内容

<details><summary>答案</summary>

没有。它只改变屏幕回显，`text()` 仍可取得真实文本。传输、日志和存储安全需另行设计。
</details>

### 题 4：大日志选哪个编辑器

<details><summary>答案</summary>

QPlainTextEdit，并设置合理的 maximumBlockCount；它比富文本 QTextEdit 更适合大量纯文本。
</details>

### 题 5：Validator 的 Intermediate 有何意义

<details><summary>答案</summary>

表示当前还不能最终提交，但它是形成合法输入的合理中间状态，例如输入负号后尚未输入数字，因此不应立即阻止。
</details>

## 27. 本篇总结

1. QLabel 用于显示，字段说明用 buddy 建立助记键和焦点关系。
2. clicked 表示命令，toggled 表示状态；程序 setChecked 也会触发 toggled。
3. CheckBox 适合独立多选，RadioButton 适合少量互斥选项，ButtonGroup 只做逻辑分组。
4. QLineEdit 的 textChanged 与 textEdited 必须按数据流方向选择。
5. Mask 和 Validator 改善输入过程，但业务边界仍要重新验证。
6. 富文本选 QTextEdit，大型纯文本和日志选 QPlainTextEdit。
7. 使用 Cursor 做增量编辑，用 maximumBlockCount 控制日志内存。

下篇将继续讲数值输入、下拉选择、日期时间、滑块、进度、标签页、分组框、滚动区和分割器。
