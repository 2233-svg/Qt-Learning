# QInputMethodQueryEvent

> Qt 6.11.1 · Qt GUI · 来自 `QInputMethodQueryEvent`

## 1. 先建立直觉

`QInputMethodQueryEvent` 是输入法向当前焦点编辑器发出的“信息请求单”。输入法要决定候选窗放在哪里、如何做上下文预测、是否有选中内容、当前输入方向是什么，就必须向控件查询光标矩形、周围文本、选区、字体等信息。

它和 `QInputMethodEvent` 构成双向协议：前者是输入法问编辑器“你现在是什么状态”，后者是输入法告诉编辑器“用户确认了什么、预编辑文本是什么”。

## 2. 类说明

`QInputMethodQueryEvent` 继承自 `QEvent`，通常由 Qt 在 `QWidget::inputMethodQuery()` 或 `event()` 流程中处理。事件构造时带有一组 `Qt::InputMethodQuery` 位标志，控件只需为请求的项目填写值。

类说明只用于表明这些 API 来自 `QInputMethodQueryEvent`：具体查询项由 `Qt::InputMethodQuery` 枚举定义，控件需要根据自己的文本模型提供相应 `QVariant`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QInputMethodQueryEvent(queries)` | 构造携带多个输入法查询请求的事件。 |
| `queries() const` | 返回输入法实际请求的查询位标志集合。 |
| `setValue(query, value)` | 为某一查询项写入答案。 |
| `value(query) const` | 读取已填写的查询结果，常用于测试、代理或调试。 |
| `type()` | 来自 `QEvent`，通常为 `QEvent::InputMethodQuery`。 |

常见查询项包括 `Qt::ImCursorRectangle`、`Qt::ImAnchorRectangle`、`Qt::ImSurroundingText`、`Qt::ImCurrentSelection`、`Qt::ImCursorPosition`、`Qt::ImAnchorPosition`、`Qt::ImInputItemClipRectangle`、`Qt::ImHints` 和 `Qt::ImPreferredLanguage`。

## 4. 关键用法

### 只回答输入法真正请求的内容

```cpp
bool CustomEditor::event(QEvent *event)
{
    if (event->type() == QEvent::InputMethodQuery) {
        auto *queryEvent = static_cast<QInputMethodQueryEvent *>(event);
        const auto queries = queryEvent->queries();

        if (queries.testFlag(Qt::ImCursorRectangle))
            queryEvent->setValue(Qt::ImCursorRectangle, cursorRectInWindow());
        if (queries.testFlag(Qt::ImSurroundingText))
            queryEvent->setValue(Qt::ImSurroundingText, surroundingText());
        if (queries.testFlag(Qt::ImCursorPosition))
            queryEvent->setValue(Qt::ImCursorPosition, cursorPosition());
        if (queries.testFlag(Qt::ImCurrentSelection))
            queryEvent->setValue(Qt::ImCurrentSelection, selectedText());

        queryEvent->accept();
        return true;
    }

    return QWidget::event(event);
}
```

先检查 `queries()` 能避免为了不需要的信息做昂贵文本提取。大型文档编辑器尤其应该这样写。

### 候选窗位置取决于正确的光标矩形

`ImCursorRectangle` 的坐标必须符合输入法预期的窗口坐标体系。自定义画布或有滚动/缩放变换的编辑器，必须把文档光标位置正确映射出来，否则候选窗会漂移到错误位置。

### 周围文本需要控制范围

`ImSurroundingText` 让输入法理解上下文，但没必要每次传整篇文档。通常返回光标附近合理窗口范围，并确保 cursor/anchor position 与返回字符串坐标一致。

## 5. 使用场景

`QInputMethodQueryEvent` 用于自定义文本编辑器、富文本编辑器、代码编辑器、终端、表格单元格编辑器、游戏内聊天框和任何自行维护文字与光标的控件。

使用 Qt 标准编辑控件时，框架已处理这些查询。只有当你自己实现文本模型或自绘文本时，才需要直接回答。

## 6. 常见坑与经验

不要只实现 `QInputMethodEvent` 而忽略 query。没有光标矩形和周围文本，输入法候选窗与预测功能常常异常。

不要为未请求的 query 强行计算全部数据。输入法查询可能高频发生，复杂文本提取应按需执行。

不要返回错误类型。每个 `Qt::InputMethodQuery` 对应期望的 `QVariant` 载荷，例如矩形、字符串、整数、布局方向或 hints。

不要让 surrounding text 中的光标位置和实际 `ImCursorPosition` 不一致。输入法会据此做替换与候选推断。

不要泄露敏感输入内容。密码框和隐私字段应通过 input method hints 与查询策略限制周围文本暴露。

## 7. 知识点覆盖

学习 `QInputMethodQueryEvent` 应覆盖输入法双向协议、`Qt::InputMethodQueries`、光标矩形、锚点矩形、周围文本、选择文本、光标位置、滚动/缩放坐标映射、输入法性能和隐私字段。
