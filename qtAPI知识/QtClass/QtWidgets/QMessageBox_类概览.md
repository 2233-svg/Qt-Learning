# Qt QMessageBox 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QMessageBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QDialog -> QMessageBox`  
> 定位：消息框

## 1. 先建立整体认识：它到底解决什么问题

`QMessageBox` 是专门用来**向用户说明一件事，并让用户快速做一个选择**的对话框。

它通常处理这些场景：

- 提示信息；
- 警告；
- 错误；
- 询问是否继续；
- 让用户确认保存、丢弃、重试、关闭；
- 给用户一个带说明文字和详细信息的弹窗。

你可以把它理解成“带标准语义的短对话框”：

```text
QDialog
  └─ QMessageBox
```

它和普通 `QDialog` 的区别是，它已经帮你把最常见的消息框结构封装好了：

- 主文本；
- 辅助说明文本；
- 可展开的详细文本；
- 图标；
- 标准按钮；
- 默认按钮；
- Esc 按键；
- 结果值。

## 2. 什么时候该用它

| 场景 | 建议 |
| --- | --- |
| 只是提示用户一条简短消息 | 用 `QMessageBox` |
| 需要询问“是否保存” | 用 `QMessageBox` |
| 需要显示警告、错误、信息、问题 | 用 `QMessageBox` |
| 需要一条带“详情”按钮的提示 | 用 `QMessageBox` |
| 需要自由排版、复杂控件、表单输入 | 不要用它，改用 `QDialog` |

一句话：**它适合“说明 + 选择”，不适合“复杂交互”。**

## 3. 两套 API：属性式 API 和静态函数 API

这是 `QMessageBox` 最重要的分界线。

### 3.1 属性式 API

先构造对象，再逐个设置属性，最后 `exec()` 或 `open()`。

优点：

- 最灵活；
- 可以设置 `informativeText`；
- 可以设置 `detailedText`；
- 可以设置自定义按钮；
- 可以控制默认按钮、Esc 按钮、选项、文本格式。

这是 Qt 官方更推荐的方式。

### 3.2 静态函数 API

像这样直接弹：

```cpp
QMessageBox::warning(this, tr("标题"), tr("内容"));
```

优点是短。  
缺点是灵活性更弱，尤其不适合需要同时设置主文本、辅助说明和详细文本的场景。

所以我的建议很直接：

- 纯提示、纯确认，且结构简单 -> 静态函数；
- 只要你开始觉得“信息不够放” -> 属性式 API。

## 4. 三层文本：主文本、辅助文本、详细文本

### 4.1 `text`

这是主文本，最重要的一句。  
它应该短、明确、直接告诉用户发生了什么。

### 4.2 `informativeText`

这是辅助说明，用来补充上下文，比如：

- 会不会丢数据；
- 会不会退出；
- 有没有替代方案；
- 这一步做了以后会怎样。

### 4.3 `detailedText`

这是详细文本，适合放日志、错误细节、堆栈、额外诊断信息。  
它是纯文本，不走富文本解释。

这三个文本不是重复，而是分层：

| 层级 | 作用 |
| --- | --- |
| 主文本 | 一句话说清问题 |
| 辅助文本 | 帮用户做选择 |
| 详细文本 | 给愿意深挖的人看 |

## 5. 图标不是装饰，是消息类型

`QMessageBox::Icon` 不是随便挑的装饰图标，它表示这条消息属于哪种严重级别。

| 图标 | 含义 |
| --- | --- |
| `NoIcon` | 不显示图标 |
| `Question` | 询问用户 |
| `Information` | 普通信息 |
| `Warning` | 警告，可处理 |
| `Critical` | 严重错误 |

默认值是 `NoIcon`。  
如果你的消息是标准提示，最好按语义选图标，而不是随便放一张图片。

如果标准图标不合适，可以用 `iconPixmap` 换自定义图标。

## 6. 按钮语义：为什么它和 QDialogButtonBox 很像

`QMessageBox` 里也有 `ButtonRole` 和 `StandardButton`，因为它本质上就是“带语义的按钮盒 + 对话框”。

标准按钮里最常见的是：

- `Ok`
- `Cancel`
- `Save`
- `Discard`
- `Yes`
- `No`
- `Retry`
- `Ignore`
- `Help`
- `Close`
- `Apply`
- `Reset`
- `RestoreDefaults`

这些按钮会映射到不同角色：

- 接受型；
- 拒绝型；
- 破坏性；
- 帮助；
- 应用；
- 重置；
- 是/否。

它们的排列顺序是平台相关的。  
比如 `Save` 和 `Cancel` 在 Windows、macOS 上的顺序就可能不同。

## 7. 默认按钮和 Esc 怎么决定

### 7.1 默认按钮

默认按钮就是按 Enter 时触发的按钮。

你可以显式指定：

```cpp
msgBox.setDefaultButton(QMessageBox::Save);
```

也可以让 Qt 自动挑一个合适的默认按钮。

### 7.2 Esc 按钮

Esc 会触发 escape button。  
如果你没显式指定，`QMessageBox` 会按规则自动找：

1. 只有一个按钮时，它就是 escape button。
2. 如果有 `Cancel` 按钮，通常它就是 escape button。
3. macOS 上，若只有一个 `RejectRole` 按钮，也可能被当成 escape button。

如果找不到，Esc 可能没有效果。

## 8. 最小可用代码

### 8.1 最简单的信息框

```cpp
QMessageBox::information(this, tr("提示"), tr("保存完成"));
```

### 8.2 带选择的保存确认

```cpp
QMessageBox msgBox(this);
msgBox.setText(tr("文档已修改。"));
msgBox.setInformativeText(tr("是否保存更改？"));
msgBox.setStandardButtons(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
msgBox.setDefaultButton(QMessageBox::Save);

int ret = msgBox.exec();
```

### 8.3 需要自定义按钮

```cpp
QMessageBox msgBox(this);
QPushButton *connectButton = msgBox.addButton(tr("连接"), QMessageBox::ActionRole);
QPushButton *abortButton = msgBox.addButton(QMessageBox::Abort);
msgBox.exec();

if (msgBox.clickedButton() == connectButton) {
    // ...
}
```

## 9. 静态函数：什么时候适合，什么时候不适合

`information()`、`question()`、`warning()`、`critical()` 都是静态工厂函数。

它们的特点很简单：

- 写起来快；
- 直接返回点击的标准按钮；
- 默认是应用模态；
- 适合简单场景。

但它们有一个天然限制：**不方便设置 `informativeText` 和 `detailedText`**。  
所以一旦你的消息开始变长，或者需要更完整的说明，最好回到属性式 API。

## 10. 属性式 API：更完整，也更值得掌握

这套 API 适合你真正想控制消息框外观和行为的时候。

常用属性有：

- `text`
- `informativeText`
- `detailedText`
- `icon`
- `iconPixmap`
- `standardButtons`
- `textFormat`
- `textInteractionFlags`
- `options`

其中最容易踩坑的是：

- `text` 和 `informativeText` 可能被识别成富文本；
- `detailedText` 永远按纯文本；
- `options` 最好在显示前设置；
- `DontUseNativeDialog` 会影响底层实现方式。

## 11. 返回值和结果

`QMessageBox` 的 `exec()` 返回的是它自己的 `StandardButton`，不是普通 `QDialog::DialogCode`。

这点很重要：

- `QDialog` 里通常看 `Accepted` / `Rejected`；
- `QMessageBox` 里通常看 `Save` / `Discard` / `Cancel` / `Yes` / `No` 这些按钮值。

如果你用了自定义按钮，`clickedButton()` 更可靠，因为返回值可能只是一个不透明整数。

## 12. 常见使用场景

### 12.1 保存确认

最经典的场景。  
用户点关闭时，问他要不要保存。

### 12.2 破坏性操作确认

比如删除文件、清空缓存、恢复出厂设置。

### 12.3 错误提示

比如连接失败、文件打开失败、权限不足。

### 12.4 额外说明的提示

比如“这项操作会影响全部设备”。

### 12.5 关于信息

`about()` 和 `aboutQt()` 属于这类。

## 13. 常见误区

### 13.1 “我用了静态函数，但想加详细说明”

静态函数不适合这个。  
改成属性式 API。

### 13.2 “按 Esc 没反应”

先看有没有 `Cancel`，再看有没有显式设置 escape button。

### 13.3 “按钮顺序和我写的不一样”

这是平台风格决定的，不是 bug。

### 13.4 “我改了标准按钮对象的属性，原生对话框没变化”

原生实现不一定完全暴露按钮对象细节。  
要深度定制，考虑 `DontUseNativeDialog`，或者用自定义按钮。

### 13.5 “result() 怎么不是 Accepted/Rejected”

这对 `QMessageBox` 来说正常。  
它返回的是 `StandardButton` 值。

## 14. 逐项 API 说明

### 成员类型

#### `enum QMessageBox::ButtonRole`

**作用：** 描述按钮在消息框中的语义。

#### `enum QMessageBox::Icon`

**作用：** 描述消息框的严重级别和图标类型。

#### `enum class QMessageBox::Option`

**作用：** 消息框选项。

#### `flags QMessageBox::Options`

**作用：** 组合多个选项。

#### `enum QMessageBox::StandardButton`

**作用：** 消息框标准按钮。

#### `flags QMessageBox::StandardButtons`

**作用：** 组合多个标准按钮。

### 属性

#### `text : QString`

**作用：** 主文本。  
**默认值：** 空字符串。  
**注意：** 可能被当成富文本。

#### `informativeText : QString`

**作用：** 辅助说明。  
**默认值：** 空字符串。  
**注意：** 可能是富文本或纯文本。

#### `detailedText : QString`

**作用：** 详细信息。  
**默认值：** 空字符串。  
**注意：** 永远按纯文本解释。

#### `icon : Icon`

**作用：** 消息类型图标。  
**默认值：** `NoIcon`

#### `iconPixmap : QPixmap`

**作用：** 自定义图标。  
**默认值：** 未定义

#### `standardButtons : StandardButtons`

**作用：** 标准按钮集合。  
**默认值：** 无按钮

#### `textFormat : Qt::TextFormat`

**作用：** 控制主文本和辅助文本的解释方式。  
**默认值：** `Qt::AutoText`

#### `textInteractionFlags : Qt::TextInteractionFlags`

**作用：** 控制消息文本如何响应用户交互。  
**默认值：** 取决于样式

#### `options : Options`

**作用：** 控制消息框行为选项。  
**注意：** `DontUseNativeDialog` 应在显示前设置。

### 成员函数

#### `[explicit] QMessageBox::QMessageBox(QWidget *parent = nullptr)`

**作用：** 构造一个空的、应用模态消息框。

#### `QMessageBox::QMessageBox(QMessageBox::Icon icon, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = NoButton, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint)`

**作用：** 直接构造带图标、标题、正文和标准按钮的消息框。

#### `[virtual noexcept] QMessageBox::~QMessageBox()`

**作用：** 销毁消息框。

#### `void QMessageBox::addButton(QAbstractButton *button, QMessageBox::ButtonRole role)`

**作用：** 加入自定义按钮并指定角色。

#### `QPushButton *QMessageBox::addButton(const QString &text, QMessageBox::ButtonRole role)`

**作用：** 创建并加入自定义按钮。

#### `QPushButton *QMessageBox::addButton(QMessageBox::StandardButton button)`

**作用：** 加入标准按钮。

#### `void QMessageBox::removeButton(QAbstractButton *button)`

**作用：** 移除按钮，但不删除它。

#### `QList<QAbstractButton *> QMessageBox::buttons() const`

**作用：** 返回所有按钮。

#### `QMessageBox::ButtonRole QMessageBox::buttonRole(QAbstractButton *button) const`

**作用：** 查询按钮角色。

#### `void QMessageBox::setStandardButtons(QMessageBox::StandardButtons buttons)`

**作用：** 设置标准按钮集合。

#### `QMessageBox::StandardButtons QMessageBox::standardButtons() const`

**作用：** 查询标准按钮集合。

#### `QMessageBox::StandardButton QMessageBox::standardButton(QAbstractButton *button) const`

**作用：** 反查标准按钮枚举。

#### `QAbstractButton *QMessageBox::button(QMessageBox::StandardButton which) const`

**作用：** 通过标准按钮枚举找按钮。

#### `QPushButton *QMessageBox::defaultButton() const`

**作用：** 查询默认按钮。

#### `void QMessageBox::setDefaultButton(QMessageBox::StandardButton button)`

**作用：** 设置默认按钮。

#### `void QMessageBox::setDefaultButton(QPushButton *button)`

**作用：** 直接指定默认按钮对象。

#### `QAbstractButton *QMessageBox::escapeButton() const`

**作用：** 查询 Esc 按钮。

#### `void QMessageBox::setEscapeButton(QAbstractButton *button)`

**作用：** 设置 Esc 按钮对象。

#### `void QMessageBox::setEscapeButton(QMessageBox::StandardButton button)`

**作用：** 设置 Esc 按钮为某个标准按钮。

#### `QAbstractButton *QMessageBox::clickedButton() const`

**作用：** 返回用户最后点击的按钮。

#### `QString QMessageBox::text() const`

**作用：** 查询主文本。

#### `void QMessageBox::setText(const QString &text)`

**作用：** 设置主文本。

#### `QMessageBox::Icon QMessageBox::icon() const`

**作用：** 查询图标类型。

#### `void QMessageBox::setIcon(QMessageBox::Icon)`

**作用：** 设置图标类型。

#### `QPixmap QMessageBox::iconPixmap() const`

**作用：** 查询自定义图标。

#### `void QMessageBox::setIconPixmap(const QPixmap &pixmap)`

**作用：** 设置自定义图标。

#### `Qt::TextFormat QMessageBox::textFormat() const`

**作用：** 查询文本格式策略。

#### `void QMessageBox::setTextFormat(Qt::TextFormat format)`

**作用：** 设置文本格式策略。

#### `void QMessageBox::setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**作用：** 设置文本交互方式。

#### `Qt::TextInteractionFlags QMessageBox::textInteractionFlags() const`

**作用：** 查询文本交互方式。

#### `void QMessageBox::setCheckBox(QCheckBox *cb)`

**作用：** 设置附加复选框。

#### `QCheckBox *QMessageBox::checkBox() const`

**作用：** 查询附加复选框。

#### `void QMessageBox::setOption(QMessageBox::Option option, bool on = true)`

**作用：** 设置单个选项。

#### `bool QMessageBox::testOption(QMessageBox::Option option) const`

**作用：** 查询某个选项是否启用。

#### `void QMessageBox::setOptions(QMessageBox::Options options)`

**作用：** 设置整组选项。

#### `QMessageBox::Options QMessageBox::options() const`

**作用：** 查询整组选项。

#### `void QMessageBox::setInformativeText(const QString &text)`

**作用：** 设置辅助说明文本。

#### `QString QMessageBox::informativeText() const`

**作用：** 查询辅助说明文本。

#### `void QMessageBox::setDetailedText(const QString &text)`

**作用：** 设置详细文本。

#### `QString QMessageBox::detailedText() const`

**作用：** 查询详细文本。

#### `void QMessageBox::setWindowTitle(const QString &title)`

**作用：** 设置窗口标题。

#### `void QMessageBox::setWindowModality(Qt::WindowModality windowModality)`

**作用：** 设置窗口模态。

#### `[override virtual slot] int QMessageBox::exec()`

**作用：** 模态显示消息框并返回点击结果。

#### `void QMessageBox::open(QObject *receiver, const char *member)`

**作用：** 异步打开消息框，并把完成信号连接到指定成员函数。

### 静态成员

#### `[static] QMessageBox::StandardButton QMessageBox::information(...)`

**作用：** 显示信息框。

#### `[static] QMessageBox::StandardButton QMessageBox::question(...)`

**作用：** 显示询问框。

#### `[static] QMessageBox::StandardButton QMessageBox::warning(...)`

**作用：** 显示警告框。

#### `[static] QMessageBox::StandardButton QMessageBox::critical(...)`

**作用：** 显示错误框。

#### `[static] void QMessageBox::about(...)`

**作用：** 显示关于对话框。

#### `[static] void QMessageBox::aboutQt(...)`

**作用：** 显示关于 Qt 的对话框。

### 信号

#### `[signal] void QMessageBox::buttonClicked(QAbstractButton *button)`

**作用：** 任意按钮被点击时发出。

### 受保护函数

#### `[override virtual protected] bool QMessageBox::event(QEvent *e)`

**作用：** 事件入口。

#### `[override virtual protected] void QMessageBox::resizeEvent(QResizeEvent *event)`

**作用：** 处理尺寸变化。

#### `[override virtual protected] void QMessageBox::showEvent(QShowEvent *event)`

**作用：** 处理显示事件。

#### `[override virtual protected] void QMessageBox::closeEvent(QCloseEvent *event)`

**作用：** 处理关闭事件。

#### `[override virtual protected] void QMessageBox::keyPressEvent(QKeyEvent *event)`

**作用：** 处理按键事件。

#### `[override virtual protected] void QMessageBox::changeEvent(QEvent *event)`

**作用：** 处理变化事件。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum QMessageBox::ButtonRole` | 描述按钮语义 | 和 `QDialogButtonBox` 一样重要 |
| 成员类型 | `enum QMessageBox::Icon` | 描述消息类型图标 | 用来表达严重级别 |
| 成员类型 | `enum class QMessageBox::Option` | 控制消息框选项 | `DontUseNativeDialog` 很关键 |
| 成员类型 | `flags QMessageBox::Options` | 组合选项 | `setOption` / `setOptions` 配合用 |
| 成员类型 | `enum QMessageBox::StandardButton` | 标准按钮枚举 | `exec()` 返回它 |
| 成员类型 | `flags QMessageBox::StandardButtons` | 组合标准按钮 | 适合 `Save | Cancel` |
| 属性 | `text : QString` | 主文本 | 可能被自动识别成富文本 |
| 属性 | `informativeText : QString` | 辅助说明 | 用来补上下文 |
| 属性 | `detailedText : QString` | 详细文本 | 永远是纯文本 |
| 属性 | `icon : Icon` | 图标类型 | 建议按语义选 |
| 属性 | `iconPixmap : QPixmap` | 自定义图标 | 代替标准图标 |
| 属性 | `standardButtons : StandardButtons` | 标准按钮集合 | 默认无按钮 |
| 属性 | `textFormat : Qt::TextFormat` | 文本格式策略 | 默认 `Qt::AutoText` |
| 属性 | `textInteractionFlags : Qt::TextInteractionFlags` | 文本交互方式 | 依赖样式 |
| 属性 | `options : Options` | 消息框选项 | 显示前设置最好 |
| 成员函数 | `[explicit] QMessageBox::QMessageBox(QWidget *parent = nullptr)` | 构造空消息框 | 默认应用模态 |
| 成员函数 | `QMessageBox::QMessageBox(QMessageBox::Icon icon, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = NoButton, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint)` | 快速构造消息框 | 适合简单场景 |
| 成员函数 | `[virtual noexcept] QMessageBox::~QMessageBox()` | 销毁消息框 | 会销毁其子对象 |
| 成员函数 | `void QMessageBox::addButton(QAbstractButton *button, QMessageBox::ButtonRole role)` | 加入自定义按钮 | 按钮盒接管所有权 |
| 成员函数 | `QPushButton *QMessageBox::addButton(const QString &text, QMessageBox::ButtonRole role)` | 创建并加入自定义按钮 | 适合“帮助”“更多” |
| 成员函数 | `QPushButton *QMessageBox::addButton(QMessageBox::StandardButton button)` | 加入标准按钮 | 无效按钮返回空 |
| 成员函数 | `void QMessageBox::removeButton(QAbstractButton *button)` | 移除按钮 | 不删除按钮 |
| 成员函数 | `QList<QAbstractButton *> QMessageBox::buttons() const` | 返回所有按钮 | 可遍历 |
| 成员函数 | `QMessageBox::ButtonRole QMessageBox::buttonRole(QAbstractButton *button) const` | 查询按钮角色 | 不存在时是 `InvalidRole` |
| 成员函数 | `void QMessageBox::setStandardButtons(QMessageBox::StandardButtons buttons)` | 设置标准按钮集合 | 适合保存确认框 |
| 成员函数 | `QMessageBox::StandardButtons QMessageBox::standardButtons() const` | 查询标准按钮集合 | 返回 `QFlags` |
| 成员函数 | `QMessageBox::StandardButton QMessageBox::standardButton(QAbstractButton *button) const` | 反查标准按钮 | 非标准按钮返回 `NoButton` |
| 成员函数 | `QAbstractButton *QMessageBox::button(QMessageBox::StandardButton which) const` | 通过枚举找按钮 | 找不到返回 `nullptr` |
| 成员函数 | `QPushButton *QMessageBox::defaultButton() const` | 查询默认按钮 | 没有时返回 `nullptr` |
| 成员函数 | `void QMessageBox::setDefaultButton(QMessageBox::StandardButton button)` | 设置默认按钮 | Enter 会触发它 |
| 成员函数 | `void QMessageBox::setDefaultButton(QPushButton *button)` | 直接指定默认按钮对象 | 更精确 |
| 成员函数 | `QAbstractButton *QMessageBox::escapeButton() const` | 查询 Esc 按钮 | 没有时可能返回空 |
| 成员函数 | `void QMessageBox::setEscapeButton(QAbstractButton *button)` | 设置 Esc 按钮对象 | 适合自定义按钮 |
| 成员函数 | `void QMessageBox::setEscapeButton(QMessageBox::StandardButton button)` | 设置标准 Esc 按钮 | 常用 `Cancel` |
| 成员函数 | `QAbstractButton *QMessageBox::clickedButton() const` | 返回最后点击的按钮 | 自定义按钮场景很有用 |
| 成员函数 | `void QMessageBox::setCheckBox(QCheckBox *cb)` | 设置附加复选框 | 消息框能带“记住选择” |
| 成员函数 | `QCheckBox *QMessageBox::checkBox() const` | 查询附加复选框 | 没有时返回 `nullptr` |
| 成员函数 | `void QMessageBox::setOption(QMessageBox::Option option, bool on = true)` | 设置单个选项 | 显示前设置 |
| 成员函数 | `bool QMessageBox::testOption(QMessageBox::Option option) const` | 查询单个选项 | Qt 6.6 起提供 |
| 成员函数 | `void QMessageBox::setOptions(QMessageBox::Options options)` | 设置选项集合 | `DontUseNativeDialog` 要早设 |
| 成员函数 | `QMessageBox::Options QMessageBox::options() const` | 查询选项集合 | 调试时看它 |
| 成员函数 | `QString QMessageBox::text() const` | 查询主文本 | 读主提示 |
| 成员函数 | `void QMessageBox::setText(const QString &text)` | 设置主文本 | 主消息要短 |
| 成员函数 | `QMessageBox::Icon QMessageBox::icon() const` | 查询图标 | 看消息类型 |
| 成员函数 | `void QMessageBox::setIcon(QMessageBox::Icon)` | 设置图标 | 推荐按语义选 |
| 成员函数 | `QPixmap QMessageBox::iconPixmap() const` | 查询自定义图标 | 没设就没意义 |
| 成员函数 | `void QMessageBox::setIconPixmap(const QPixmap &pixmap)` | 设置自定义图标 | 适合品牌图标 |
| 成员函数 | `Qt::TextFormat QMessageBox::textFormat() const` | 查询文本格式 | 默认自动识别 |
| 成员函数 | `void QMessageBox::setTextFormat(Qt::TextFormat format)` | 设置文本格式 | 防止误判富文本 |
| 成员函数 | `void QMessageBox::setTextInteractionFlags(Qt::TextInteractionFlags flags)` | 设置文本交互 | 影响复制选择等行为 |
| 成员函数 | `Qt::TextInteractionFlags QMessageBox::textInteractionFlags() const` | 查询文本交互 | 依赖样式 |
| 成员函数 | `QString QMessageBox::informativeText() const` | 查询辅助说明 | 补充上下文 |
| 成员函数 | `void QMessageBox::setInformativeText(const QString &text)` | 设置辅助说明 | 常和主文本配套 |
| 成员函数 | `QString QMessageBox::detailedText() const` | 查询详细文本 | 纯文本 |
| 成员函数 | `void QMessageBox::setDetailedText(const QString &text)` | 设置详细文本 | 常放诊断信息 |
| 成员函数 | `void QMessageBox::setWindowTitle(const QString &title)` | 设置窗口标题 | macOS 可能忽略 |
| 成员函数 | `void QMessageBox::setWindowModality(Qt::WindowModality windowModality)` | 设置模态 | Sheet 场景相关 |
| 成员函数 | `[override virtual slot] int QMessageBox::exec()` | 模态执行并返回结果 | 返回标准按钮值 |
| 成员函数 | `void QMessageBox::open(QObject *receiver, const char *member)` | 异步打开并连接完成信号 | 适合非阻塞流程 |
| 静态成员 | `[static] QMessageBox::StandardButton information(...)` | 显示信息框 | 简单提示首选 |
| 静态成员 | `[static] QMessageBox::StandardButton question(...)` | 显示询问框 | 常用于是否继续 |
| 静态成员 | `[static] QMessageBox::StandardButton warning(...)` | 显示警告框 | 非致命风险 |
| 静态成员 | `[static] QMessageBox::StandardButton critical(...)` | 显示错误框 | 严重错误 |
| 静态成员 | `[static] void about(...)` | 显示关于框 | 带应用图标 |
| 静态成员 | `[static] void aboutQt(...)` | 显示关于 Qt 框 | 帮助菜单常用 |
| 信号 | `[signal] void QMessageBox::buttonClicked(QAbstractButton *button)` | 任意按钮点击信号 | 自定义按钮时最有用 |
| 受保护函数 | `[override virtual protected] bool QMessageBox::event(QEvent *e)` | 事件入口 | 一般不重写 |
| 受保护函数 | `[override virtual protected] void QMessageBox::resizeEvent(QResizeEvent *event)` | 尺寸变化处理 | 布局相关 |
| 受保护函数 | `[override virtual protected] void QMessageBox::showEvent(QShowEvent *event)` | 显示事件处理 | 首次显示相关 |
| 受保护函数 | `[override virtual protected] void QMessageBox::closeEvent(QCloseEvent *event)` | 关闭事件处理 | 结果与关闭相关 |
| 受保护函数 | `[override virtual protected] void QMessageBox::keyPressEvent(QKeyEvent *event)` | 键盘事件处理 | Esc / Enter 相关 |
| 受保护函数 | `[override virtual protected] void QMessageBox::changeEvent(QEvent *event)` | 变化事件处理 | 样式或语言变化 |

---

### 一句话总结

`QMessageBox` 不是“一个能弹出来的框”这么简单，它是 Qt 的标准消息语义包装。简单提示可以直接用静态函数，复杂内容更适合属性式 API；只要你开始需要说明、详情、默认按钮、Esc 和自定义按钮，就应该认真按它的完整模型来用。
