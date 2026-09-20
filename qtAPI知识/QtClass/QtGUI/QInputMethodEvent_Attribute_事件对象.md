# QInputMethodEvent::Attribute：描述组合文本局部状态的值对象

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QInputMethodEvent>`  
> 所属：`QInputMethodEvent` 的嵌套类型

## 它解决什么问题

`QInputMethodEvent::Attribute` 是一条附着在输入法 preedit string 上的局部描述：从哪个字符开始、覆盖多长、它表达的是格式、输入法光标、语言、注音、选区还是提交内容的附加 MIME 数据。

它不是富文本 span 的通用替代品，也不是文档正文格式。它服务于“用户正在组合、尚未最终提交”的 preedit 文本；控件收到下一次输入法事件后，这些属性可能整体被替换。

一个 Attribute 的四个公开字段共同才有意义：

```text
type  -> 决定 start / length / value 应如何解释
start -> preedit 或周边编辑文本中的起点
length -> 覆盖长度或特定状态标志
value -> 由 type 决定的 QVariant，有时刻意为空
```

## 实际使用场景

- 输入法实现为候选组合文字添加下划线、颜色或背景。
- 自定义编辑器读取 `Cursor` 属性，在 preedit 内绘制输入法光标。
- 日文等输入法为组合段提供语言或 ruby 注音。
- 输入法提交富内容时，携带 `QMimeData` 与纯文本 commit string。
- 自定义编辑器在单元测试中构造 `QInputMethodEvent` 来验证 preedit 渲染。

应用侧通常只从 `QInputMethodEvent::attributes()` 读取 Attribute。主动构造它更多见于输入法、平台集成和测试；普通“插入一段文本”无需制造输入法 attribute。

## 属性类型决定 value 的类型

| `AttributeType` | range 作用域 | `value` 的预期类型与规则 |
| --- | --- | --- |
| `TextFormat` | preedit 的 `[start, start + length)` | `QTextFormat`（可由 `QTextCharFormat` 提供）。至少要能表达背景、文字色和下划线；同一字符重叠多个格式属性是未定义行为。 |
| `Cursor` | preedit 内 `start` 位置 | `length` 为 0 时光标不可见；value 若为 `QColor` 则指定颜色，否则用周边文字色。每个事件最多一条 Cursor。 |
| `Language` | preedit 的局部段 | `QLocale`，表示该段语言；同一字符不应有多条 Language。 |
| `Ruby` | preedit 的局部段 | ruby/注音文本；同一字符不应有多条 Ruby。 |
| `Selection` | surrounding text，不是 preedit | value 未使用；commit 后将编辑器光标移至 `start`，`length` 可建立选区。 |
| `MimeData` | 已提交内容 | `QMimeData`，表示 commit 的富数据；`commitString()` 仍提供纯文本。 |

不要把任何 `QVariant` 都塞进 `value`。`Attribute` 本身不会动态校验类型，错误通常在接收控件 `value<T>()`、转换或渲染时才暴露，甚至被静默忽略。

## start 与 length 的坐标边界

除 `Selection` 外，大多属性定位 preedit string。`start` 和 `length` 是 `QString` 的字符索引，不是 UTF-8 字节偏移、屏幕像素或排版 glyph 索引。对于代理对、组合附加符和复杂脚本，编辑模型需沿用 Qt 字符串的 UTF-16 索引规则。

对每个 Attribute 都应验证：

- `start >= 0`；
- `length >= 0`；
- 需要覆盖 preedit 的属性满足 `start + length <= preedit.size()`；
- `Cursor` 的位置允许位于文本末尾；
- 同一类型的“至多一条”或“不重叠”要求不被破坏。

来自平台输入法的属性通常可信于 Qt 协议；手工构造、第三方输入法或测试数据仍应由控件防御性处理，避免异常范围破坏文本布局。

## 构造与使用

带 `QVariant` 的构造函数用于有实际值的属性；不带 value 的重载构造空 `QVariant`，适合 `Selection` 或只依赖位置的 `Cursor`。

```cpp
QTextCharFormat format;
format.setFontUnderline(true);

const QString preedit = "nih";
QList<QInputMethodEvent::Attribute> attributes {
    { QInputMethodEvent::TextFormat,
      0,
      preedit.size(),
      QVariant::fromValue(format) },
    { QInputMethodEvent::Cursor, 3, 1 }
};

QInputMethodEvent event(preedit, attributes);
```

Attribute 的字段是 public，便于轻量传递和构造，但也意味着修改后不会自动重新验证 value 类型或 range。更稳妥的模式是：创建时完成校验，随后将其视为不可变记录；不要在已投递事件的 attributes 列表中就地改动。

## 相等比较

`operator==` 同时比较 `type`、`start`、`length` 和 `value`；`operator!=` 是其反面。这是结构相等，不表示两条属性在屏幕上必然渲染相同效果：不同主题、字体、控件实现和平台输入法都可能让相同 `QTextFormat` 显示不同。

`QVariant` 的相等语义取决于所存类型。它适合测试期望 attribute 或做临时 diff，不适合当作跨进程持久化、哈希 key 或渲染缓存的唯一身份。

## 常见错误

- 把 `start`、`length` 当成 UTF-8 字节位置。
- 不看 `type` 就对 `value` 做固定类型转换。
- 用多个重叠 `TextFormat` 覆盖同一个字符，触发未定义行为。
- 为一个 event 放多条 `Cursor`，或忘记 `length == 0` 表示不可见。
- 把 `Selection` 画在 preedit 内，而不是在 commit 后移动 surrounding text 的编辑光标。
- 把 Attribute 作为永久文档格式保存到 undo 栈。
- 修改已投递事件内的属性，却期待输入法或其他过滤器自动同步。
- 用结构相等判断两段组合文本的视觉等价。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 构造 | `Attribute(AttributeType type, int start, int length, QVariant value)` | 创建带值属性；value 类型由 `type` 决定，构造不做动态类型校验。 |
| 构造 | `Attribute(AttributeType type, int start, int length)` | 创建空 value 属性，适合 value 未使用或可省略的类型。 |
| 字段 | `AttributeType type` | 决定 range 与 value 的解释方式；读取 value 前先分支判断。 |
| 字段 | `int start` | 属性起点，通常相对 preedit 的 `QString` 字符索引。 |
| 字段 | `int length` | 覆盖长度或状态参数；必须满足该属性类型的范围规则。 |
| 字段 | `QVariant value` | 属性载荷，如 `QTextFormat`、`QColor`、`QLocale`、ruby 文本或 `QMimeData`。 |
| 比较 | `operator==(const Attribute &, const Attribute &)` | 结构比较 type、start、length 与 QVariant value。 |
| 比较 | `operator!=(const Attribute &, const Attribute &)` | `operator==` 的否定。 |
| 上下文 | `QInputMethodEvent::attributes()` | 从所属事件取得 Attribute 列表；这些属性描述本次 preedit，不是持久文档样式。 |

## 相关类

- `QInputMethodEvent`：拥有 preedit、commit 与 Attribute 列表的事件。
- `QTextFormat` / `QTextCharFormat`：`TextFormat` attribute 的常见 value。
- `QColor`：`Cursor` attribute 的可选光标颜色。
- `QLocale`：`Language` attribute 的语言信息。
- `QMimeData`：`MimeData` attribute 的富提交内容。

`Attribute` 的小巧来自它不替你解释任何东西：type、range 与 QVariant 必须严格配套。把这份协议守住，自定义编辑器才能准确绘制输入法组合态，又不会把临时状态污染正文模型。
