# QShortcut

> Qt 6.11.1 · Qt GUI · 来自 `QShortcut`

## 1. 先建立直觉

`QShortcut` 是独立快捷键对象。它把一个或多个 `QKeySequence` 绑定到某个父对象/窗口范围，触发时发出 `activated()`。

如果快捷键对应菜单或工具栏命令，优先用 `QAction::setShortcut()`；如果只是某个控件内部的临时快捷键或没有 action 的行为，用 `QShortcut` 更直接。

## 2. 类说明

`QShortcut` 继承自 `QObject`。它依赖父 widget/window 的事件体系，`context` 决定快捷键在哪个范围生效：当前 widget、窗口、应用等。

当同一按键序列匹配多个快捷键时，可能发出 `activatedAmbiguously()`。大型应用要集中规划快捷键，避免用户按下后结果不确定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QShortcut(QKeySequence, parent, ...)` | 创建快捷键并绑定回调或成员函数。 |
| `QShortcut(QKeySequence::StandardKey, parent, ...)` | 使用平台标准快捷键。 |
| `setKey()` / `key()` | 设置或读取单个快捷键。 |
| `setKeys()` / `keys()` | 设置或读取多个快捷键。 |
| `setContext()` / `context()` | 设置生效范围。 |
| `setEnabled()` / `isEnabled()` | 启用或禁用快捷键。 |
| `setAutoRepeat()` / `autoRepeat()` | 控制按住时是否重复触发。 |
| `setWhatsThis()` / `whatsThis()` | 设置帮助文本。 |
| `parentWidget()` | 返回关联父 widget。 |
| `activated()` | 快捷键明确激活时发出。 |
| `activatedAmbiguously()` | 快捷键匹配有歧义时发出。 |

## 4. 关键用法

```cpp
auto *shortcut = new QShortcut(QKeySequence(Qt::CTRL | Qt::Key_L), editor);
shortcut->setContext(Qt::WidgetShortcut);

connect(shortcut, &QShortcut::activated, editor, &Editor::selectCurrentLine);
```

使用标准键：

```cpp
new QShortcut(QKeySequence::Find, this, this, &MainWindow::showFindBar);
```

多个键序列：

```cpp
shortcut->setKeys({ QKeySequence("Ctrl+/"), QKeySequence("Ctrl+K, Ctrl+C") });
```

## 5. 使用场景

适合控件内部快捷键、隐藏命令、无菜单动作的局部操作、临时模式快捷键、编辑器局部行为。

如果命令也出现在菜单或工具栏，用 `QAction` 更好，因为文本、图标、启用状态和快捷键能统一维护。

## 6. 常见坑与经验
快捷键范围要收窄。能用 `WidgetShortcut` 就别随便用 `ApplicationShortcut`，否则容易抢走其他窗口输入。

`activatedAmbiguously()` 是信号，不是异常。出现它通常说明快捷键设计冲突。

文本输入控件里设置快捷键要谨慎。用户输入法、系统快捷键和编辑快捷键都可能冲突。
