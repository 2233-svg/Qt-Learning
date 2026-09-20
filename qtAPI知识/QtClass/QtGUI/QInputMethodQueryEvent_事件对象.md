# QInputMethodQueryEvent：输入法向焦点编辑器索取上下文的请求

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QInputMethodQueryEvent>`  
> 继承：`QEvent`

## 它解决什么问题

`QInputMethodQueryEvent` 是输入法上下文主动发送给当前输入对象的同步查询事件。输入法需要知道光标在哪里、选中什么、周边文本是什么、是否允许输入、应使用哪些 hints，才能正确完成候选窗定位、预测、reconversion 和虚拟键盘策略。

事件不直接携带答案：构造时只带一组 `Qt::InputMethodQueries` 请求位，焦点对象根据自身编辑状态逐项调用 `setValue()` 填答，然后 `accept()`。

它与 `QInputMethodEvent` 方向相反：

```text
QInputMethodEvent       输入法 -> 编辑器：提交/更新组合文本
QInputMethodQueryEvent  输入法 <- 编辑器：查询编辑上下文
```

标准 Qt 文本控件已经实现该协议。自定义文本控件若只处理 `QInputMethodEvent` 而不能回答 query，简单文字可能能输入，但候选窗位置、周边文本转换、选择和移动端输入体验会明显不完整。

## 实际使用场景

- 输入法查询 `ImCursorRectangle`，把候选窗放到当前光标附近。
- 输入法查询 `ImSurroundingText`、`ImCursorPosition` 与 `ImAnchorPosition`，执行预测或 reconversion。
- 虚拟键盘查询 `ImHints`，选择数字、邮箱、密码等键盘布局。
- 输入法查询 `ImCurrentSelection`，对选中内容进行替换或转换。
- 自定义编辑器在文本、光标、选区变化后通过 `QInputMethod::update()` 触发下一轮查询。

## 处理模型：按请求位同步填答

`queries()` 是 flags，而不是单个枚举。接收者必须检查每个被请求的 bit，只返回自己能正确提供的值，并在完成后接受事件。

```cpp
bool CustomEditor::event(QEvent *event)
{
    if (event->type() != QEvent::InputMethodQuery) {
        return QWidget::event(event);
    }

    auto *queryEvent = static_cast<QInputMethodQueryEvent *>(event);
    const auto queries = queryEvent->queries();

    if (queries.testFlag(Qt::ImCursorRectangle)) {
        queryEvent->setValue(Qt::ImCursorRectangle, cursorRectInWindow());
    }
    if (queries.testFlag(Qt::ImSurroundingText)) {
        queryEvent->setValue(Qt::ImSurroundingText, surroundingText());
    }
    if (queries.testFlag(Qt::ImCursorPosition)) {
        queryEvent->setValue(Qt::ImCursorPosition, cursorPosition());
    }

    queryEvent->accept();
    return true;
}
```

对 QWidget，自定义控件通常更适合重写 `inputMethodQuery(Qt::InputMethodQuery)`，让 QWidget 的事件分发参与这套协议；上例展示的是 `QInputMethodQueryEvent` 本身要求的“检查 requests、设置 values、accept”顺序。

这是同步事件。不要把 event 指针投给异步任务后再 `setValue()`；等异步结果回来时，输入法早已得到空答案并继续进行下一轮状态转换。

## 常见查询及 QVariant 类型

实际可用 queries 由 `Qt::InputMethodQuery` 定义。下面是自定义编辑器最常需要回答的项目：

| 查询 | 通常应返回 | 用途 |
| --- | --- | --- |
| `ImEnabled` | `bool` | 当前对象是否接受输入法。 |
| `ImCursorRectangle` | `QRectF` | 光标在窗口坐标中的几何，候选窗定位依赖它。 |
| `ImAnchorRectangle` | `QRectF` | 选区锚点的窗口坐标矩形。 |
| `ImSurroundingText` | `QString` | 光标附近或完整可供转换的文本上下文。 |
| `ImCurrentSelection` | `QString` | 当前选中正文。 |
| `ImCursorPosition` | `int` | 光标在 surrounding text 中的字符串位置。 |
| `ImAnchorPosition` | `int` | 选区锚点在 surrounding text 中的位置。 |
| `ImHints` | `Qt::InputMethodHints` | 输入类型提示，如数字、邮箱、密码等。 |
| `ImPreferredLanguage` | `QLocale` | 编辑器偏好的输入语言。 |
| `ImMaximumTextLength` | `int` | 可接受的最大文本长度。 |

同一 query 的值类型不能凭猜测替换。例如 `ImCursorRectangle` 返回 widget 局部坐标或 `QRect` 而不是所需 `QRectF`/窗口坐标，会导致候选窗口偏移；将 `ImCursorPosition` 按 UTF-8 字节偏移回答，则复杂 Unicode 文本的转换范围会错位。

若不支持某项，宁可不设置或返回符合该 query 约定的无效值，也不要编造看似合理的数据。输入法会据此决定是否降级；错误的 surrounding text 或 selection 更可能造成错误替换。

## 与编辑器状态同步

`QInputMethodQueryEvent` 本身只在输入法主动询问时出现。编辑器状态变化后，需要通过 `QGuiApplication::inputMethod()->update(queries)` 通知输入法重新询问：

```cpp
void CustomEditor::setSelection(int anchor, int cursor)
{
    m_anchor = anchor;
    m_cursor = cursor;
    QGuiApplication::inputMethod()->update(Qt::ImQueryInput);
}
```

光标变化通常也会改变 selection、surrounding text 和候选窗位置，Qt 将常见输入 query 组合为 `Qt::ImQueryInput`。只有改变了某个明确属性时也可以发送更窄的 flags，避免无谓的重算。

查询值、文本模型和 preedit 必须保持同一时刻的视图。若在回复 `ImSurroundingText` 后异步改变光标、再回复旧的 `ImCursorPosition`，输入法可能按过期位置进行替换。

## 构造与手动发送

`QInputMethodQueryEvent(queries)` 可用于测试或输入法集成，构造后只有请求集合，没有已填答案：

```cpp
QInputMethodQueryEvent event(
    Qt::ImCursorRectangle | Qt::ImSurroundingText);

QCoreApplication::sendEvent(editor, &event);

if (event.isAccepted()) {
    const QRectF caret =
        event.value(Qt::ImCursorRectangle).toRectF();
}
```

普通应用通常不会主动创建它；平台输入法和 Qt 会向焦点对象发送。手工测试时应验证 `isAccepted()`、`QVariant::isValid()` 和预期类型，不能把未设置 value 当成空字符串、零或空矩形的成功答案。

## 常见错误

- 忽略 `queries()` 的 flags，只回答自己习惯的一两个属性。
- 未设置任何值就 `accept()`，令输入法以为编辑器支持但没有上下文。
- 返回了不符合 query 约定的 `QVariant` 类型或错误坐标系。
- 把位置按 UTF-8 字节偏移而非 Qt 字符串索引回答。
- 将 surround text、cursor position 与 selection 从不同版本的文档状态分别读取。
- 文本/光标变化后从不调用 `QInputMethod::update()`。
- 把 `QInputMethodQueryEvent` 当异步请求并保存裸 event 指针。
- 手动构造事件来替代实现 `inputMethodQuery()`，却遗漏 QWidget 的正常事件路径。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 构造 | `explicit QInputMethodQueryEvent(Qt::InputMethodQueries queries)` | 构造带一组请求位的 `QEvent::InputMethodQuery`；初始不含答案。 |
| 请求 | `queries() const` | 返回被输入法查询的 flags；逐项 `testFlag()` 后再填答。 |
| 应答 | `setValue(Qt::InputMethodQuery query, const QVariant &value)` | 为某项请求设置答案；value 类型和坐标系必须符合该 query 契约。 |
| 读取 | `value(Qt::InputMethodQuery query) const` | 取得已设置答案；未提供时不要把无效 QVariant 当作有效默认值。 |
| 继承 | `accept()` / `ignore()` / `isAccepted()` | 焦点对象填完可支持的 requested values 后接受事件；用于表明查询已处理。 |
| 继承 | `type()` | 返回 `QEvent::InputMethodQuery`。 |

## 相关类

- `QInputMethod`：调用 `update()` 触发输入法重新查询焦点对象。
- `QInputMethodEvent`：反向传递 preedit 与 commit 结果。
- `Qt::InputMethodQuery` / `Qt::InputMethodQueries`：请求项和请求 flags 的定义。
- `QWidget::inputMethodQuery()`：自定义 Widget 编辑器的首选实现点。
- `QGuiApplication::inputMethod()`：取得当前平台输入法协调对象。

`QInputMethodQueryEvent` 的价值在于让输入法拿到编辑器的真实即时上下文。每一项 query 都是一个类型和坐标系契约；同步、完整且一致地回答，输入法才能正确放置候选、处理选择并完成复杂文本转换。
