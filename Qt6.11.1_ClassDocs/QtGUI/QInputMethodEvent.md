# QInputMethodEvent

> Qt 6.11.1 · Qt GUI · 来自 `QInputMethodEvent`

## 1. 先建立直觉

`QInputMethodEvent` 是输入法与文本控件之间的协议事件。它把输入过程拆成两部分：

- `preeditString()`：正在组合、尚未确认的预编辑文本，例如拼音、日文假名转换中的候选片段。
- `commitString()`：已经确认，应真正插入文档的数据。

这是写自定义编辑器时必须守住的边界。把 preedit 直接写进文档会造成重复字符、撤销记录混乱、候选转换异常；忽略 preedit 又会让用户看不到输入法组合过程。

## 2. 类说明

`QInputMethodEvent` 继承自 `QEvent`，类型为 `QEvent::InputMethod`。文本控件通常在 `inputMethodEvent()` 中处理它，并在 `inputMethodQuery()` 中回答输入法的反向查询。

类说明只用于表明这些 API 来自 `QInputMethodEvent`：预编辑字符串、提交字符串、替换范围和属性列表由此事件提供；文档模型、光标、撤销栈和渲染策略由控件自己维护。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum AttributeType` | 定义预编辑文本附加信息：格式、光标、语言、Ruby、选择、MIME 数据。 |
| `class Attribute` | 保存一种输入法属性的类型、起点、长度和值。 |
| `QInputMethodEvent()` | 构造空输入法事件。 |
| `QInputMethodEvent(preeditText, attributes)` | 构造带预编辑文本与显示属性的输入法事件。 |
| `preeditString() const` | 返回尚未确认的组合文本，只用于临时显示。 |
| `commitString() const` | 返回已确认、应插入或替换到文档中的文本。 |
| `setCommitString(text, replaceFrom, replaceLength)` | 设置提交文本及其相对当前光标的替换范围。 |
| `replacementStart() const` | 返回替换起点，相对预编辑锚点或当前编辑位置。 |
| `replacementLength() const` | 返回要替换的字符数。 |
| `attributes() const` | 返回预编辑文本的格式、光标、语言等属性。 |

## 4. 关键用法

### 正确处理“提交”和“预编辑”

```cpp
void PlainEditor::inputMethodEvent(QInputMethodEvent *event)
{
    if (!event->commitString().isEmpty()) {
        replaceAroundCursor(
            event->replacementStart(),
            event->replacementLength(),
            event->commitString());
    }

    m_preeditText = event->preeditString();
    m_preeditAttributes = event->attributes();
    updateInputMethodCursor();
    update();

    event->accept();
}
```

文档只接收 `commitString()`。`m_preeditText` 则作为视觉叠加层画在真实文档光标位置附近，下一次输入法事件会替换它。

### 处理替换范围

输入法不总是简单地在光标处追加文字。候选确认、自动更正、组合字符回退都可能要求替换光标附近内容。`replacementStart()` 和 `replacementLength()` 就是这种修改的准确描述。

```cpp
replaceAroundCursor(event->replacementStart(),
                    event->replacementLength(),
                    event->commitString());
```

不要只做 `insertText(commitString())`。对英文输入似乎能工作，但遇到组合输入、重转换或输入法自动替换就会出错。

### 根据 Attribute 渲染预编辑文本

输入法属性常包含：

- `TextFormat`：预编辑片段的下划线、前景色、背景色等。
- `Cursor`：输入法内部光标位置及是否可见。
- `Language`：片段语言。
- `Ruby`：日文注音等辅助文本。
- `Selection`：对周围文档的选择范围调整。
- `MimeData`：提交内容的富数据表示。

自定义编辑器至少应支持 `TextFormat` 和 `Cursor`，否则候选区分和输入法光标提示会明显变差。

### 自定义文本控件必须配合查询事件

输入法还需要知道当前光标矩形、周围文本、选区和输入方向等，这些通过 `QInputMethodQueryEvent` 或 `inputMethodQuery()` 提供。只实现 `inputMethodEvent()` 往往仍会导致候选窗位置错误或上下文预测失效。

## 5. 使用场景

`QInputMethodEvent` 用于自定义代码编辑器、富文本编辑器、终端模拟器、聊天输入框、表格内编辑器、公式编辑器、游戏内文本框和任何自行管理文本模型的控件。

使用现成的 `QLineEdit`、`QTextEdit`、`QPlainTextEdit` 时通常不需要直接处理；它们已实现输入法协议。只有当你绕开这些控件自己绘制/管理文本时，才必须接管。

## 6. 常见坑与经验

不要用 `QKeyEvent::text()` 替代输入法事件。键盘事件不能完整表达候选、组合、替换和预编辑格式。

不要把 preedit 放进撤销栈。预编辑是暂态，只有 commit 才应成为用户可撤销的文档修改。

不要忽略空 commit。一次事件可能只更新预编辑显示，不提交任何真实字符。

不要只保存 preedit 字符串而丢掉 attributes。至少要考虑输入法光标位置和下划线/选中格式。

不要在输入法事件里进行缓慢排版或网络操作。它跟随每次候选和组合更新，卡顿会直接破坏输入体验。

## 7. 知识点覆盖

学习 `QInputMethodEvent` 应覆盖输入法协议、预编辑与提交、替换范围、输入法属性、组合文本渲染、输入法光标、撤销栈边界、富文本 MIME、`inputMethodQuery()` 和国际化文本输入。
