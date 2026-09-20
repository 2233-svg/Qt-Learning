# QInputMethodEvent：组合文本与最终提交文本的事件载体

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QInputMethodEvent>`  
> 继承：`QEvent`

## 它解决什么问题

`QInputMethodEvent` 让文本控件正确处理复杂输入法的三个阶段：开始组合、持续预编辑、确认或取消。它携带两种本质不同的文本：

- `preeditString()`：用户仍在组合、候选尚可改变的临时文本。
- `commitString()`：应立即插入正文或替换正文的最终文本。

拼音候选、日文假名转换、韩文组合、语音/预测文本等都不能只靠 `QKeyEvent::text()` 实现。若自定义编辑器把 preedit 当作普通正文写入 undo 栈，或在 commit 时忘记替换旧 preedit，常见结果就是重复文字、撤销历史混乱、候选下划线消失。

## 实际使用场景

- 实现自定义代码编辑器、富文本控件、终端模拟器或画布文本工具。
- 在 preedit 下绘制候选下划线、输入法光标、语言和 ruby 注音。
- 处理输入法提交时对选区或光标附近字符的替换。
- 接收 `MimeData` 属性并支持富文本/特殊粘贴式提交。
- 编写输入法插件、自动化测试或合成输入事件。

标准 `QLineEdit`、`QTextEdit` 和 Qt Quick 文本控件已处理这些细节。只有接管编辑模型和绘制的自定义控件才应重写 `inputMethodEvent()`。

## 先分清 preedit 与 commit

```text
输入法组合开始
  preedit: "ni"        -> 用户看到临时组合，不进入永久正文
  preedit: "nih"       -> 替换上一次 preedit
  commit:  "你"        -> 写入正文，再显示本次新的 preedit（若有）
```

`preeditString()` 是当前输入上下文的临时内容。它可以反复被替换、重排或清空，撤销/重做不应把每一步 preedit 当成独立正文编辑。

`commitString()` 是最终结果，通常应插在 preedit 之前，并作为一次真实编辑进入 undo 栈。事件可同时包含 commit 和新的 preedit：先完成正文替换/插入，再更新临时组合文本，不能简单地“只要有字符串就 append”。

## 自定义编辑器的处理顺序

自定义 QWidget 必须先启用输入法事件，并同时实现查询接口；只重写 `keyPressEvent()` 不能支持复杂输入。

```cpp
CustomEditor::CustomEditor(QWidget *parent)
    : QWidget(parent)
{
    setAttribute(Qt::WA_InputMethodEnabled);
}

void CustomEditor::inputMethodEvent(QInputMethodEvent *event)
{
    removeSelectedText();
    replaceAroundPreedit(event->replacementStart(),
                         event->replacementLength(),
                         event->commitString());

    setPreedit(event->preeditString(), event->attributes());
    event->accept();

    QGuiApplication::inputMethod()->update(Qt::ImQueryInput);
}
```

上述辅助函数由控件自己的文本模型实现，但顺序不能颠倒：

1. 有选区时先移除选区。
2. 以 `replacementStart()` / `replacementLength()` 指定的范围替换为 `commitString()`。
3. 若已有 preedit，用本次 `preeditString()` 替换它；否则在当前插入点创建新的 preedit。
4. 根据 attributes 渲染 preedit。

replacement 坐标相对于 preedit 起点，但替换时 preedit 区域本身被忽略。因此负的 `replacementStart()` 可以回退到 preedit 前的正文，范围也可跨越 preedit 两侧。不要把它误当成简单的“当前文档绝对 offset”。

## AttributeType：preedit 的局部语义

`attributes()` 是对本次 preedit 的局部描述。自定义编辑器至少必须正确处理 `TextFormat` 与 `Cursor`。

| 类型 | `start` / `length` / `value` 的语义 |
| --- | --- |
| `TextFormat` | 指定 preedit 子区间的 `QTextFormat`。至少应尊重背景色、文字色和下划线；同一字符覆盖多个该属性属于未定义行为。 |
| `Cursor` | 在 preedit 的 `start` 处显示输入法光标。`length == 0` 表示光标不可见；value 若为 `QColor`，用作光标颜色；每个事件最多一个。 |
| `Language` | value 为 `QLocale`，说明 preedit 某段语言；同一字符重复指定属于未定义行为。 |
| `Ruby` | value 是某段 preedit 的 ruby/注音文本；同一字符不应有多个 ruby 属性。 |
| `Selection` | 影响 surrounding text，而不是 preedit：commit 后把编辑光标移到 `start`，`length` 可指定新选区；value 未使用。 |
| `MimeData` | value 包含代表已提交文本的 `QMimeData`；`commitString()` 仍提供纯文本表示。 |

attributes 的 `start` 和 `length` 以 `QString` 字符索引描述，不是字节偏移，也不是渲染后的 glyph 数量。处理代理项、组合字形或富文本布局时，应在文本模型层维护一致的 UTF-16 索引语义。

## 构造与手动投递

默认构造得到 `QEvent::InputMethod` 类型、默认空字段的事件；带 `preeditText` 和 attributes 的构造函数初始化组合文本。两种构造都不会自动生成 commit text，如需合成最终提交，调用 `setCommitString()`。

```cpp
QInputMethodEvent event(
    "ni",
    { QInputMethodEvent::Attribute(
          QInputMethodEvent::Cursor, 2, 1, {}) });

event.setCommitString("你", 0, 0);
QCoreApplication::sendEvent(editor, &event);
```

手工事件适合单元测试、输入法集成或受控模拟；它不会替你建立完整平台输入上下文，也不会替自定义控件实现 `inputMethodQuery()`。正常应用代码应处理 Qt 投递的事件，不要为了插入普通文本而模拟输入法事件。

## 与查询协议配套

输入法需要知道编辑器的光标矩形、选区、周边文本、可接受输入类型等，才能放置候选窗并进行 reconversion。实现 `inputMethodEvent()` 的控件还必须实现 `inputMethodQuery()`；编辑器状态改变后再通过 `QInputMethod::update(Qt::ImQueryInput)` 通知输入法刷新查询。

不实现查询协议时，简单的 commit 可能看似可用，但候选窗位置、长文本转换、选区替换和移动端软键盘行为通常会失真。

## 常见错误

- 把每次 preedit 更新写进 undo 栈，导致一次输入需要撤销很多步。
- 收到 commit 后 append，却不执行 `replacementStart` / `replacementLength` 规定的替换。
- 在插入 commit 之前先删除或插入 preedit，造成重复或错位。
- 忽略 `TextFormat` 与 `Cursor` 属性，组合状态没有下划线或输入法光标。
- 把 `Selection` 当成 preedit 内部光标属性。
- 把 attribute 的 `start`、`length` 当 UTF-8 字节偏移。
- 仅设 `WA_InputMethodEnabled`，却未重写 `inputMethodQuery()`。
- 保存事件或其 `attributes()` 引用给异步任务，越过事件生命周期。
- 用手工 `QInputMethodEvent` 代替普通程序化文本插入。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `AttributeType` | 定义 preedit 格式、光标、语言、ruby、周边选区和 mime 数据等局部语义。 |
| 类型 | `Attribute` | 一条属性记录，包含 type、start、length、value；详见 `QInputMethodEvent::Attribute`。 |
| 构造 | `QInputMethodEvent()` | 构造默认的 `QEvent::InputMethod`，preedit、commit、替换范围和属性均为默认值。 |
| 构造 | `QInputMethodEvent(const QString &preedit, const QList<Attribute> &)` | 构造带 preedit 和渲染属性的事件；commit 和替换范围随后用 `setCommitString()` 设置。 |
| 文本 | `preeditString() const` | 返回暂时组合文本；可替换和取消，不应作为永久正文逐步进入 undo 栈。 |
| 文本 | `commitString() const` | 返回应插入或替换到正文的最终文本，通常位于 preedit 前。 |
| 替换 | `replacementStart() const` | 返回相对 preedit 起点的替换位置；可为负，且替换时忽略 preedit 区域。 |
| 替换 | `replacementLength() const` | 返回要替换的字符数；0 时 `replacementStart` 表示 commit 插入位置。 |
| 替换 | `setCommitString(QString, int replaceFrom = 0, int replaceLength = 0)` | 设置合成事件的最终文本和相对替换范围。 |
| 属性 | `attributes() const` | 返回本次 preedit 的属性列表；引用仅在事件存活期间有效。 |
| 属性 | `TextFormat` | `value` 为 `QTextFormat`；至少渲染背景、文字色与下划线。 |
| 属性 | `Cursor` | preedit 内输入法光标；length 为 0 则不可见，value 可提供 `QColor`。 |
| 属性 | `Language` / `Ruby` | 给 preedit 段标注语言或 ruby 文本。 |
| 属性 | `Selection` | commit 后移动 surrounding text 的光标或选区，不作用于 preedit。 |
| 属性 | `MimeData` | 提供已提交文本的富数据；纯文本仍取自 `commitString()`。 |
| 继承 | `accept()` / `ignore()` | 标记输入法事件是否被控件处理；自定义编辑器成功更新模型后应明确接受。 |
| 继承 | `type()` | 返回 `QEvent::InputMethod`。 |

## 相关类

- `QInputMethod`：请求虚拟键盘、提交/重置组合状态并通知 query 更新。
- `QInputMethodEvent::Attribute`：单条 preedit 属性值类型。
- `QInputMethodQueryEvent`：平台/输入法向焦点对象索取编辑上下文。
- `QWidget::inputMethodEvent()` / `inputMethodQuery()`：自定义 Widget 的实现点。
- `QTextFormat`、`QTextCharFormat`：渲染 `TextFormat` 属性。

`QInputMethodEvent` 的关键是把“正在组合的显示层”和“已经提交的编辑操作”严格分开。先正确处理 commit replacement，再替换 preedit 并渲染属性，复杂语言输入才能和选择、撤销、光标移动共存。
