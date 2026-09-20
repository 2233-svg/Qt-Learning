# QKeyEvent

> Qt 6.11.1 · Qt GUI · 来自 `QKeyEvent`

## 1. 先建立直觉

`QKeyEvent` 描述键盘事件：按键按下、释放，以及快捷键覆盖判断。它看起来只是“哪个键被按了”，实际要同时处理三层信息：Qt 抽象键值、键盘布局产生的文本、平台原生扫描码。

最容易误解的是 `key()` 和 `text()`。`key()` 适合判断方向键、功能键、快捷键这类“按的是哪个键”；`text()` 适合文本输入，因为它考虑键盘布局、修饰键、组合输入，可能产生一个或多个 Unicode 字符，也可能为空。

## 2. 类说明

`QKeyEvent` 继承自 `QInputEvent`。常规代码会在 `QWidget::keyPressEvent()`、`QWidget::keyReleaseEvent()`、`QWindow::keyPressEvent()`、`eventFilter()` 或 `QEvent::ShortcutOverride` 分支中接触它。

类说明只用于表明这些 API 来自 `QKeyEvent`：按键码、自动重复、标准快捷键匹配、原生键盘数据都属于键盘事件本身，而不是某个具体控件的能力。控件只决定是否接受事件、是否继续交给基类处理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QKeyEvent(type, key, modifiers, text, autorep, count)` | 构造普通键盘事件，常用于测试、自定义事件派发或输入模拟。 |
| `QKeyEvent(type, key, modifiers, nativeScanCode, nativeVirtualKey, nativeModifiers, text, autorep, count, device)` | 构造带平台原生键盘数据的事件，快捷键系统更依赖这些字段。 |
| `key() const` | 返回 Qt 抽象按键码，如 `Qt::Key_A`、`Qt::Key_Left`。 |
| `text() const` | 返回该按键生成的 Unicode 文本，文本输入应优先看它。 |
| `modifiers() const` | 返回事件中的键盘修饰符组合。 |
| `keyCombination() const` | 把 `key()` 和 `modifiers()` 合成 `QKeyCombination`。 |
| `matches(QKeySequence::StandardKey) const` | 判断是否匹配平台标准快捷键，如 Copy、Paste、Undo。 |
| `isAutoRepeat() const` | 判断事件是否来自长按后的自动重复。 |
| `count() const` | 返回事件涉及的按键/文本数量，压缩事件和组合输入时尤其要注意。 |
| `nativeScanCode() const` | 返回平台扫描码，偏硬件位置。 |
| `nativeVirtualKey() const` | 返回平台虚拟键或 keysym，偏操作系统键值。 |
| `nativeModifiers() const` | 返回平台原生修饰符。 |

## 4. 关键用法

### 命令控制看 `key()`，文本输入看 `text()`

方向键、删除键、Esc、F1 这类控制按键应该用 `key()` 判断。

```cpp
void Editor::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Escape) {
        cancelCompletion();
        event->accept();
        return;
    }

    if (!event->text().isEmpty() && !event->text().at(0).isControl()) {
        insertPlainText(event->text());
        event->accept();
        return;
    }

    QWidget::keyPressEvent(event);
}
```

不要用 `key()` 自己推导字符大小写。不同键盘布局、输入法、死键组合会让这种推导很快失效。

### 标准快捷键用 `matches()`

跨平台快捷键不要硬编码 `Ctrl+C`。macOS 上复制通常显示为 Command+C，而 `matches()` 会按平台标准判断。

```cpp
void TextView::keyPressEvent(QKeyEvent *event)
{
    if (event->matches(QKeySequence::Copy)) {
        copySelection();
        event->accept();
        return;
    }

    QWidget::keyPressEvent(event);
}
```

如果你实现的是应用专属快捷键，可以用 `QShortcut` 或 `QAction`；如果你正在控件内部拦截标准编辑命令，`matches()` 更合适。

### 自动重复要按交互类型决定是否接受

长按方向键连续移动光标是合理的；长按保存快捷键连续保存通常不是。

```cpp
void Player::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Space) {
        if (!event->isAutoRepeat())
            togglePaused();
        event->accept();
        return;
    }

    QWidget::keyPressEvent(event);
}
```

`isAutoRepeat()` 对压缩键盘事件可能不够精细，所以对高频输入场景，最好结合业务状态做二次防护。

### `ShortcutOverride` 要明确接受

当事件类型是 `QEvent::ShortcutOverride` 时，控件有机会阻止全局快捷键。例如文本框在输入时可能要保留某些组合键给自己。只有调用 `accept()`，Qt 才会认为你覆盖了快捷键。

```cpp
bool SearchBox::event(QEvent *event)
{
    if (event->type() == QEvent::ShortcutOverride) {
        auto *keyEvent = static_cast<QKeyEvent *>(event);
        if (keyEvent->key() == Qt::Key_Escape) {
            keyEvent->accept();
            return true;
        }
    }

    return QLineEdit::event(event);
}
```

## 5. 使用场景

`QKeyEvent` 是自定义控件键盘可用性的基础。列表、表格、画布、编辑器、游戏控制、终端模拟器都需要通过它处理方向键、确认取消、文本输入和模式切换。

它也用于快捷键体系的边界处理。普通命令建议交给 `QAction`、`QShortcut` 和菜单系统；但当某个控件需要在局部上下文里覆盖或解释快捷键时，就会直接处理 `QKeyEvent`。

在输入法相关场景里，`QKeyEvent` 只是一部分。真正的预编辑文本、候选确认和复杂组合输入还会涉及 `QInputMethodEvent`。如果你在做文本编辑控件，不要只靠键盘事件实现输入法。

## 6. 常见坑与经验

不要用 `key()` 处理普通文字输入。`Qt::Key_A` 不等于用户想输入 `a`，更不等于所有语言文字输入。

不要忘记调用基类实现。控件默认的 Tab 焦点移动、文本编辑快捷键、助记符和平台行为都可能依赖基类处理。

不要把 native 字段写进跨平台业务逻辑。`nativeScanCode()`、`nativeVirtualKey()`、`nativeModifiers()` 适合诊断、快捷键底层匹配或平台适配，不适合作为普通功能分支的主依据。

不要假设修饰键状态绝对可靠。某些平台和键盘组合可能出现边界情况；关键命令应以当前事件和应用状态共同判断。

## 7. 知识点覆盖

学习 `QKeyEvent` 应覆盖 Qt 事件系统、键盘布局、Unicode 文本输入、快捷键覆盖、自动重复、标准快捷键、`QKeyCombination`、平台原生键盘码、输入法事件和控件默认键盘行为。真正写好键盘交互，重点不是记函数名，而是分清“按键控制”和“文本输入”这两条线。
