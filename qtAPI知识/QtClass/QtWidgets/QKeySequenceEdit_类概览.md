# Qt QKeySequenceEdit 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QKeySequenceEdit>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget -> QKeySequenceEdit`
> 常见搭档：`QKeySequence`、`QAction`、`QShortcut`

## 1. QKeySequenceEdit 解决什么问题

`QKeySequenceEdit` 是专门用来让用户录入键盘快捷键的控件。它看起来像一个输入框，但它录入的不是普通字符串，而是 `QKeySequence`。

它适合放在：

- 快捷键设置页；
- 菜单项的快捷键编辑器；
- 插件或脚本系统的按键绑定界面；
- 需要把用户按下的组合键保存为 `QKeySequence` 的工具。

它解决的是“怎样让用户可靠地录入组合键”这个问题。用 `QLineEdit` 自己解析文本，会遇到平台键名、修饰键顺序、国际键盘、连续组合键和非法输入等问题；`QKeySequenceEdit` 把这些录入规则交给 Qt。

它**不负责**把快捷键绑定到某个动作。录入完成后，通常还要把 `keySequence()` 交给 `QAction::setShortcut()` 或 `QShortcut`。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 录入一个 QAction 的快捷键

```cpp
#include <QAction>
#include <QApplication>
#include <QKeySequenceEdit>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *editor = new QKeySequenceEdit(&window);
    editor->setKeySequence(QKeySequence(Qt::CTRL | Qt::Key_S));

    auto *saveAction = new QAction(QObject::tr("保存"), &window);
    QObject::connect(editor, &QKeySequenceEdit::editingFinished,
                     &window, [editor, saveAction] {
                         saveAction->setShortcut(editor->keySequence());
                     });

    auto *layout = new QVBoxLayout(&window);
    layout->addWidget(editor);
    window.show();
    return app.exec();
}
```

`editingFinished()` 适合做“用户录入结束后提交”的动作；如果希望每次录入内容变化都立即同步，则连接 `keySequenceChanged()`。

## 3. 先理解 QKeySequence 的录入模型

### 3.1 一个 sequence 不一定只有一个组合键

`QKeySequence` 可以由多个连续的 `QKeyCombination` 组成，例如：

```cpp
QKeySequence sequence(Qt::CTRL | Qt::Key_K,
                      Qt::CTRL | Qt::Key_C);
editor->setKeySequence(sequence);
```

这对应常见的前缀快捷键。`maximumSequenceLength` 限制的是组合键数量，不是字符串长度。

### 3.2 `keySequenceChanged` 和 `editingFinished` 不是一回事

- `keySequenceChanged(const QKeySequence &)`：当前序列被修改时通知；
- `editingFinished()`：Qt 判断这次录入已经结束时通知，例如控件失去焦点、达到最大长度或按下结束组合键。

保存配置时，通常使用 `editingFinished()`；实时显示或实时校验时，使用 `keySequenceChanged()`。

### 3.3 结束组合键

Qt 6.5 增加了 `finishingKeyCombinations`。它允许指定某些组合键作为“录入结束”的信号，而不是继续等待下一段组合键。这个机制适合自定义快捷键编辑体验。

结束组合键的含义是“结束本次编辑”，不等于“自动执行 QAction”。真正的动作绑定仍要由应用完成。

## 4. 常用配置

### 4.1 初始值和长度

```cpp
editor->setKeySequence(QKeySequence(QStringLiteral("Ctrl+Alt+P")));
editor->setMaximumSequenceLength(2);
```

如果通过 `setKeySequence()` 设置的序列超过最大长度，Qt 会截断它。设置最大长度后，已有序列也可能被限制到新的长度范围内，因此应在加载配置时先设置长度，再设置初始值。

### 4.2 清空按钮

```cpp
editor->setClearButtonEnabled(true);
```

清空按钮只是控件提供的便利入口，实际清空仍等价于调用 `clear()`，并会使 `keySequence()` 变为空序列。

### 4.3 把录入结果写入动作

```cpp
QObject::connect(editor, &QKeySequenceEdit::editingFinished,
                 action, [editor, action] {
                     action->setShortcut(editor->keySequence());
                 });
```

如果有多个动作共享同一个快捷键配置页，还应在提交前检查冲突。`QKeySequenceEdit` 只负责录入，不会替你判断快捷键是否已经被其它动作占用。

## 5. 常见误区

### 5.1 不要把显示文本当作持久化格式

`QKeySequence::toString()` 适合显示给用户，但保存配置时最好使用 Qt 支持的标准序列化方式，并明确使用哪种 `QKeySequence::SequenceFormat`。显示文本可能随平台键名和本地化变化。

### 5.2 不要只监听 `editingFinished`

如果用户输入过程中需要即时提示“快捷键冲突”或更新预览，只监听 `editingFinished()` 会等到提交时才得到通知；这时应连接 `keySequenceChanged()`。

### 5.3 `maximumSequenceLength` 不是字符串长度

`Ctrl+K, Ctrl+C` 有两个组合键，但显示文本有更多字符。把最大长度当作字符数会得到错误的限制。

### 5.4 录入控件和快捷键执行是两条链

推荐把流程拆开：

```text
QKeySequenceEdit
    -> QKeySequence
    -> 冲突检查 / 配置保存
    -> QAction::setShortcut() 或 QShortcut
```

这样快捷键编辑界面不会和动作执行逻辑互相缠绕。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QKeySequenceEdit(QWidget *parent = nullptr)` | 创建一个空的快捷键序列编辑器。 | 需要放入布局或设置 parent；控件本身不绑定任何 QAction。 |
| 构造 | `QKeySequenceEdit(const QKeySequence &keySequence, QWidget *parent = nullptr)` | 创建编辑器并设置初始快捷键序列。 | 如果序列超过 `maximumSequenceLength`，会按最大长度截断。 |
| 析构 | `~QKeySequenceEdit()` | 销毁快捷键编辑器。 | QWidget 的父子对象规则负责常规生命周期。 |
| 属性 | `keySequence : QKeySequence` | 读取或修改当前正在编辑的快捷键序列。 | 这是组合键序列，不是普通文本；修改后会发出 `keySequenceChanged`。 |
| 属性 | `clearButtonEnabled : bool` | 控制是否显示清空按钮。 | 该属性从 Qt 6.4 提供；按钮只是便利入口，核心操作仍是 `clear()`。 |
| 属性 | `maximumSequenceLength : qsizetype` | 限制一个序列最多包含多少个组合键。 | 从 Qt 6.5 提供；设置值或设置序列时可能发生截断。 |
| 属性 | `finishingKeyCombinations : QList<QKeyCombination>` | 指定哪些组合键可以结束本次录入。 | 从 Qt 6.5 提供；结束编辑不等于执行快捷键动作。 |
| 查询 | `keySequence() const` | 返回当前快捷键序列。 | 空序列表示当前没有录入快捷键。 |
| 修改 | `setKeySequence(const QKeySequence &keySequence)` | 以程序方式设置当前序列。 | 超过最大长度时会截断；适合加载配置或恢复默认值。 |
| 查询 | `isClearButtonEnabled() const` | 查询清空按钮是否启用。 | 只反映控件配置，不代表当前序列是否为空。 |
| 修改 | `setClearButtonEnabled(bool enable)` | 开启或关闭清空按钮。 | 适合按界面空间和交互需求配置。 |
| 查询 | `maximumSequenceLength() const` | 返回允许的最大组合键数量。 | 不要把返回值理解为字符数。 |
| 修改 | `setMaximumSequenceLength(qsizetype count)` | 设置最大组合键数量。 | 修改后要重新检查已有 `keySequence()` 是否被截断。 |
| 查询 | `finishingKeyCombinations() const` | 返回当前的结束组合键列表。 | 用于调试或保存自定义录入规则。 |
| 修改 | `setFinishingKeyCombinations(const QList<QKeyCombination> &finishingKeyCombinations)` | 设置结束录入的组合键集合。 | 只改变录入结束条件，不负责动作绑定。 |
| 槽 | `clear()` | 清空当前快捷键序列。 | 通常会触发 `keySequenceChanged`；适合“恢复为无快捷键”。 |
| 信号 | `editingFinished()` | 通知一次快捷键录入已经结束。 | 适合提交配置、做冲突检查或写入 QAction。 |
| 信号 | `keySequenceChanged(const QKeySequence &keySequence)` | 通知当前序列发生变化。 | 适合实时预览和实时冲突提示。 |
| 受保护函数 | `event(QEvent *event)` | 处理控件级事件分发。 | 派生类重写时要保留基类对焦点和键盘事件的处理。 |
| 受保护函数 | `keyPressEvent(QKeyEvent *event)` | 接收并解析按下的键组合。 | 这是快捷键录入的核心扩展点；不要把它当普通文本输入处理。 |
| 受保护函数 | `keyReleaseEvent(QKeyEvent *event)` | 处理键释放事件。 | 与内部组合键收集和录入结束判断有关。 |
| 受保护函数 | `timerEvent(QTimerEvent *event)` | 处理内部定时事件。 | 通常不需要业务层重写；重写时要避免破坏录入超时逻辑。 |
| 受保护函数 | `focusOutEvent(QFocusEvent *event)` | 处理控件失去焦点。 | 失焦可能触发 `editingFinished()`，适合提交前确认这条语义。 |

### 一句话总结

`QKeySequenceEdit` 负责把键盘操作录入为结构化的 `QKeySequence`；它解决“怎么录入”的问题，快捷键冲突检查和动作绑定仍由应用负责。
