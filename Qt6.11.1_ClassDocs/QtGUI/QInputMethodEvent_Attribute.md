# QInputMethodEvent::Attribute

> Qt 6.11.1 · Qt GUI · 来自 `QInputMethodEvent::Attribute`

## 1. 先建立直觉

`QInputMethodEvent::Attribute` 描述预编辑字符串中的一个属性片段。它不是单独的输入事件，而是 `QInputMethodEvent::attributes()` 返回列表里的元素，用于告诉文本控件“这段组合文本该怎样显示或解释”。

一个属性由四部分组成：类型、起始位置、长度和值。起始位置和长度通常相对于 `preeditString()`，而不是整个文档；值的 `QVariant` 类型由属性类型决定。

## 2. 类说明

`QInputMethodEvent::Attribute` 是值类型，定义在 `QInputMethodEvent` 内部。它不会主动发送通知，也没有对象所有权问题；文本控件从当前输入法事件中读取它，在下一次事件到来时更新自己的预编辑渲染状态。

类说明只用于表明这些 API 来自 `QInputMethodEvent::Attribute`。属性类型枚举定义在 `QInputMethodEvent` 中，真正的预编辑与提交流程由 `QInputMethodEvent` 处理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `Attribute(type, start, length, value)` | 构造带值的输入法属性片段。 |
| `Attribute(type, start, length)` | 构造无值属性片段，适合不需要附加值的属性。 |
| `type` | 属性类型，例如 TextFormat、Cursor、Language、Ruby、Selection、MimeData。 |
| `start` | 属性开始位置，通常相对预编辑字符串。 |
| `length` | 属性覆盖的字符长度；Cursor 等类型对长度有特殊语义。 |
| `value` | 附加值，通常是 `QTextCharFormat`、`QColor`、`QLocale`、`QString` 或 `QMimeData` 等。 |

## 4. 关键用法

### 用 TextFormat 渲染候选状态

输入法常以不同下划线或背景色标识已转换、待转换、当前候选的预编辑片段。

```cpp
for (const auto &attribute : event->attributes()) {
    if (attribute.type != QInputMethodEvent::TextFormat)
        continue;

    const auto format = attribute.value.value<QTextCharFormat>();
    drawPreeditRange(attribute.start, attribute.length, format);
}
```

范围应裁剪到 `preeditString()` 长度内。输入法实现通常正确，但自定义控件不应因为异常范围直接越界。

### 用 Cursor 画输入法内部光标

`Cursor` 的 `start` 表示预编辑字符串内的光标位置，`length` 用于表示可见性，`value` 若为 `QColor` 可作为光标颜色。

```cpp
if (attribute.type == QInputMethodEvent::Cursor && attribute.length != 0)
    drawPreeditCursor(attribute.start, attribute.value.value<QColor>());
```

这和真实文档光标不是同一个概念：输入法内部光标位于尚未提交的 preedit 文本中。

### 其他属性按能力渐进支持

`Language`、`Ruby`、`Selection`、`MimeData` 对专业编辑器和国际化排版很有价值，但普通纯文本控件可先保证 TextFormat 和 Cursor 正确，再按需求扩展。

## 5. 使用场景

`QInputMethodEvent::Attribute` 适合自绘文本编辑器、富文本编辑器、代码编辑器、终端模拟器、日文 Ruby 支持、带输入法候选显示的游戏或专业工具。

现成的 Qt 文本控件已经处理这些属性；直接使用 `QLineEdit`、`QTextEdit`、`QPlainTextEdit` 时，通常不需要创建或解释它们。

## 6. 常见坑与经验

不要把 `start` / `length` 当成整个文档位置。大多数属性范围相对于当前 preedit 字符串。

不要假设 `value` 的类型固定。读取前应根据 `type` 使用正确的 `QVariant` 转换，并为无效值保留降级显示。

不要同时给同一字符叠加多份冲突的 `TextFormat` 并期待 Qt 自动合并。自定义渲染时要自己定义优先级。

不要把 Attribute 缓存到下一轮输入法事件后仍直接使用。它是当前预编辑状态的描述，新的事件可能完全替换范围与格式。

## 7. 知识点覆盖

学习 `QInputMethodEvent::Attribute` 应覆盖预编辑范围、TextFormat、输入法内部光标、`QVariant`、`QTextCharFormat`、语言属性、Ruby 注音、选择属性、富文本输入和自定义编辑器渲染。
