# QKeyEvent：键盘动作、生成文本与快捷键语义

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QKeyEvent>`  
> 继承：`QInputEvent`

## 它解决什么问题

`QKeyEvent` 描述一个按键按下、释放或快捷键覆盖请求。它同时包含三层不应混淆的信息：

- `key()`：平台无关的 `Qt::Key`，适合导航、功能键和可移植快捷键。
- `text()`：该动作实际生成的 Unicode 文本，适合区分大小写、布局和可输入字符。
- `nativeScanCode()` / `nativeVirtualKey()` / `nativeModifiers()`：平台底层键位信息，适合少数平台集成需求。

键盘事件送到拥有键盘输入焦点的控件。它适合命令、导航、游戏控制和基本文本输入；但完整的中文、日文、韩文等复杂文字输入仍必须由 `QInputMethodEvent` 协议处理，不能把 `keyPressEvent()` 的 `text()` 当成输入法的替代品。

## 实际使用场景

- 用方向键、PageUp、Escape、F1 等 `Qt::Key` 实现导航和命令。
- 用 `matches(QKeySequence::Copy)` 等标准动作匹配跨平台快捷键。
- 用 `text()` 处理实际产生的字母、符号和控制字符。
- 根据 `isAutoRepeat()` 对长按移动、连发命令或游戏输入做节流。
- 在平台插件、快捷键系统或键盘布局工具中使用 native 键位信息。
- 用 `ShortcutOverride` 让控件抢占本应由上层 `QAction` 处理的快捷键。

## key、text、native code 各回答什么

```cpp
void Editor::keyPressEvent(QKeyEvent *event)
{
    if (event->matches(QKeySequence::Undo)) {
        undo();
        return;
    }

    if (event->key() == Qt::Key_Escape) {
        cancelCurrentOperation();
        return;
    }

    if (!event->text().isEmpty()) {
        insertPlainText(event->text());
        return;
    }

    event->ignore();
}
```

| 数据 | 用途 | 关键边界 |
| --- | --- | --- |
| `key()` | 逻辑按键，如 `Qt::Key_Left`、`Qt::Key_F5`、`Qt::Key_A`。 | 不区分大小写；若需 `'a'` 与 `'A'` 的实际输出，读 `text()`。 |
| `text()` | 本次动作生成的 Unicode 文本。 | 可为空，例如 Shift、Ctrl、Alt、Meta；也可含控制字符或私用区字符。 |
| `keyCombination()` | `key()` 与 modifiers 的强类型组合。 | 适合与 `QKeyCombination` 比较，但不等于完整多段 `QKeySequence`。 |
| native 三元组 | 扫描码、虚拟键/keysym、原生修饰键。 | 平台相关，可能为 0，即使事件有其他扩展数据。 |

`key() == 0` 或 `Qt::Key_unknown` 表示事件不对应已知逻辑键，例如 compose sequence、键盘宏或 key compression。此时不要强行把它映射成 ASCII；若有实际输入文字，优先看 `text()`。

## 标准快捷键优先使用 matches()

跨平台命令应匹配 `QKeySequence::StandardKey`，而非硬编码 `Ctrl+C`、`Meta+C` 等具体组合：

```cpp
if (event->matches(QKeySequence::Paste)) {
    paste();
    return;
}
```

`matches()` 让 Qt 按平台习惯解释标准动作，例如 macOS 的 Command 修饰键。它适合单个 key event 与标准命令的匹配；应用定义的多键序列、可配置绑定或冲突解决使用 `QKeySequence`/`QShortcut` 等更高层机制。

`keyCombination()` 自 Qt 6.0 提供，返回本事件的 key 和 modifiers。它是值对象比较的便捷方式，但仍受键盘布局、事件类型和 modifier 状态影响。

## modifiers 与 ShortcutOverride

`QKeyEvent::modifiers()` 返回事件发生后可见的修饰键 flags。它通常是本次快捷键判断依据，但在两侧 Shift 等同类修饰键同时按下、再释放其中一侧的边界情况下，平台无法总是提供完全可信的聚合状态。对安全敏感或低层键盘状态机，不要只依赖这一份简化 flags。

`KeyPress` 和 `KeyRelease` 事件默认已被接受；处理它们时通常无需再 `accept()`。调用 `ignore()` 会让事件沿父 widget 链继续传播，直到某个对象接受它或事件过滤器消费它。

`ShortcutOverride` 不同：想让当前控件覆盖上层快捷键处理时，必须显式 `accept()`。

```cpp
void CodeEditor::keyPressEvent(QKeyEvent *event)
{
    if (event->type() == QEvent::ShortcutOverride
        && event->matches(QKeySequence::Find)) {
        event->accept();
        return;
    }

    QWidget::keyPressEvent(event);
}
```

是否要覆盖快捷键是控件协作契约。编辑器在局部搜索、补全或 modal 文本模式下可接管；无条件接管通用快捷键会让菜单、`QAction` 和辅助功能键盘导航失效。

## 自动重复与 key compression

`isAutoRepeat()` 对初次按下返回 `false`，对系统长按连发返回 `true`。但启用 `Qt::WA_KeyCompression` 后，一个事件可能代表多个按键，其中部分来自自动重复；这种混合压缩事件的 auto-repeat 结果可能不确定。

`count()` 返回事件涉及的按键数；当 `text()` 非空时，等于 `text()` 的字符串长度。它不是用户按下物理键的可靠计数，也不是 Unicode grapheme 数。处理文本应把 `text()` 作为字符串整体插入，而不是按 `count()` 循环猜测字符。

长按行为若依赖精确“按住多久”，更可靠的方式是根据 `KeyPress`/`KeyRelease` 维护状态并使用计时器，而非假设所有平台都会以相同节奏投递 autorepeat。

## 构造与合成事件

两个构造函数只接受 `QEvent::KeyPress`、`KeyRelease` 或 `ShortcutOverride`。简化重载包含逻辑 key、modifier、text、autorep 与 count；完整重载额外携带 native 信息和来源键盘设备，默认设备为 `QInputDevice::primaryKeyboard()`。

```cpp
QKeyEvent event(QEvent::KeyPress,
                Qt::Key_Return,
                Qt::NoModifier,
                "\n");
QCoreApplication::sendEvent(target, &event);
```

手动投递适合单元测试和受控自动化。它不会模拟平台快捷键管理、输入法组合、物理键盘状态或原生事件队列；不要用合成 `QKeyEvent` 代替 `QInputMethodEvent` 来输入复杂文字。

## 常见错误

- 用 `key()` 判断大小写、符号或实际输入字符，而没有读 `text()`。
- 用 `text()` 实现导航或快捷键，受到键盘布局和输入法影响。
- 硬编码 `Ctrl` 组合，忽略 macOS 等平台的标准快捷键习惯。
- 把 `keyCombination()` 当作多段 `QKeySequence` 匹配器。
- 以为 native scan/virtual key 永远存在或跨平台可比较。
- 忽略 `key() == 0` / `Key_unknown` 的 compose、宏和压缩语义。
- 对 `KeyPress` 无条件 `ignore()`，让未处理的文字意外传播到父控件。
- 忘记 `ShortcutOverride` 必须显式 accept 才能覆盖快捷键。
- 用 `isAutoRepeat()` 作为压缩事件的精确物理重复判据。
- 在自定义文本编辑器中只处理 `QKeyEvent`，不实现输入法事件与查询协议。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 构造 | `QKeyEvent(Type, int key, KeyboardModifiers, QString text = {}, bool autorep = false, quint16 count = 1)` | 构造逻辑键事件；type 只能是 `KeyPress`、`KeyRelease` 或 `ShortcutOverride`。 |
| 构造 | 完整 `QKeyEvent` 重载 | 额外提供 native scan code、virtual key、native modifiers 和 `QInputDevice`；主要用于平台/测试集成。 |
| 键码 | `key() const` | 返回平台无关 `Qt::Key`；不区分大小写，0/`Key_unknown` 表示未知逻辑键。 |
| 文本 | `text() const` | 返回本次生成的 Unicode 文本；修饰键等可为空，也可含控制字符。 |
| 组合 | `keyCombination() const` | Qt 6.0 起。返回 key 与 modifiers 的 `QKeyCombination`。 |
| 快捷键 | `matches(QKeySequence::StandardKey) const` | 判断是否匹配标准跨平台动作，如 Copy、Paste、Undo。 |
| 修饰键 | `modifiers() const` | 返回事件后的 modifier flags；双侧同类修饰键释放等边界下不能完全信赖。 |
| 重复 | `isAutoRepeat() const` | 是否来自按键自动重复；混合压缩事件可能不确定。 |
| 重复 | `count() const` | 事件涉及的键数；text 非空时等于字符串长度，非可靠物理键次数。 |
| 原生 | `nativeScanCode() const` | 返回平台扫描码，缺失时为 0。 |
| 原生 | `nativeVirtualKey() const` | 返回平台 virtual key 或 keysym，缺失时为 0。 |
| 原生 | `nativeModifiers() const` | 返回平台原生 modifier，缺失时为 0；即使有扩展数据也可能为 0。 |
| 来源 | `device()` / `deviceType()` | 从 `QInputEvent` 继承；查询事件来源键盘和类型。 |
| 时序 | `timestamp()` | 从 `QInputEvent` 继承；窗口系统相对时间戳，不能当日期时间。 |
| 传播 | `accept()` / `ignore()` | `KeyPress`、`KeyRelease` 默认接受；ignore 会向父 widget 链传播。 |
| 覆盖 | `type() == QEvent::ShortcutOverride` | 想阻止上层快捷键处理时必须显式 accept。 |

## 相关类

- `QKeySequence`：标准快捷键与可配置多键序列。
- `QShortcut` / `QAction`：高层快捷键注册与命令路由。
- `QInputMethodEvent`：复杂文字组合与最终提交。
- `QInputDevice`：键盘来源及其平台描述。
- `QFocusEvent`：键盘焦点转移。

`QKeyEvent` 的稳健用法是：命令看 `key()` 或 `matches()`，可见文字看 `text()`，平台键位只在确有平台需求时看 native 数据。把这三层分开，快捷键与输入法就不会彼此踩踏。
