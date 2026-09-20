# QKeySequenceEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QKeySequenceEdit`

## 1. 先建立直觉

`QKeySequenceEdit` 是“快捷键录制框”。用户把焦点放进去后按下 `Ctrl+K`、`Ctrl+Shift+P` 这类组合键，控件会把它记录成 `QKeySequence`。它只负责采集和编辑快捷键，不负责让快捷键在应用里真正触发动作。

真正执行快捷键通常由 `QAction::setShortcut()` 或 `QShortcut` 完成。因此它最常出现的位置不是主窗口工具栏，而是“首选项 / 快捷键设置 / 自定义命令”这样的配置界面。

## 2. 类说明

`QKeySequenceEdit` 继承自 `QWidget`。它把用户按键组合转换成 `QKeySequence`，并通过 `keySequenceChanged()`、`editingFinished()` 等信号把结果交给业务层。

一个好用的快捷键配置页通常会把它和冲突检测、默认值恢复、平台标准快捷键、持久化设置结合起来。`QKeySequenceEdit` 是输入端，不是完整快捷键管理器。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QKeySequenceEdit(QWidget *)` | 创建空的快捷键录制控件。 |
| `QKeySequenceEdit(const QKeySequence &, QWidget *)` | 创建时带一个已有快捷键，适合编辑配置。 |
| `setKeySequence(const QKeySequence &)` / `keySequence()` | 设置或读取当前录制的快捷键序列。 |
| `clear()` | 清空当前快捷键。常接“清除快捷键”按钮。 |
| `setClearButtonEnabled(bool)` / `isClearButtonEnabled()` | 控制内置清除按钮，Qt 6.4 起可用。 |
| `setMaximumSequenceLength(qsizetype)` / `maximumSequenceLength()` | 限制序列长度。多数桌面快捷键用 1 段就够，复杂编辑器可允许多段。 |
| `setFinishingKeyCombinations(...)` | 指定哪些按键组合结束录制，Qt 6.5 起可用。 |
| `finishingKeyCombinations()` | 读取结束录制的按键组合列表。 |
| `keySequenceChanged(const QKeySequence &)` | 用户修改快捷键时发出，适合即时做冲突检测。 |
| `editingFinished()` | 录制结束时发出，适合保存或应用设置。 |

## 4. 关键用法

配置页里常见流程是：显示已有快捷键，用户修改后先检查冲突，再写回 `QAction`。

```cpp
auto *edit = new QKeySequenceEdit(action->shortcut(), this);
edit->setClearButtonEnabled(true);
edit->setMaximumSequenceLength(1);

connect(edit, &QKeySequenceEdit::editingFinished, this, [=] {
    const QKeySequence seq = edit->keySequence();
    if (!hasShortcutConflict(seq, action)) {
        action->setShortcut(seq);
        settings.setValue("shortcuts/open", seq.toString());
    }
});
```

如果你正在做命令面板或专业编辑器，可以允许多段序列，例如 `Ctrl+K, Ctrl+C`。这时 `maximumSequenceLength()` 不应盲目设为 1，但一定要在帮助文本和冲突检测里把多段序列作为一等规则处理。

## 5. 使用场景

它适合快捷键设置页、插件命令配置、宏录制设置、IDE/编辑器自定义键位、辅助功能键位映射，以及需要让用户自己指定 `QAction` 快捷键的桌面工具。

它不适合作为普通文本输入框，也不适合在业务表单中捕获单个字符。需要文本就用 `QLineEdit`；需要响应已经定义好的快捷键就用 `QShortcut`；需要菜单命令快捷键就配置 `QAction`。

## 6. 常见坑与经验

录到的快捷键不等于已经生效。把 `keySequence()` 存起来后，还要同步给 `QAction`、`QShortcut` 或自己的命令系统。

必须做冲突检测。用户把两个命令都设成 `Ctrl+S` 时，Qt 不会自动知道你的业务优先级，结果往往变成“看起来保存失灵”。

跨平台时不要硬编码所有快捷键文案。显示给用户的字符串建议使用 `QKeySequence::toString()`，并考虑 `QKeySequence::StandardKey`，让系统习惯参与进来。
