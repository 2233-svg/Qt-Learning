# QInputMethod：平台输入法、预编辑文本与虚拟键盘的协调器

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QInputMethod>`  
> 继承：`QObject`

## 它解决什么问题

`QInputMethod` 是应用与平台文本输入系统之间的协调对象。它让文本编辑器能与拼音、日文假名转换、韩文组合、预测输入、候选词窗和虚拟键盘协作，也让视图层可查询虚拟键盘是否可见、键盘占据的窗口区域以及光标应避让的位置。

它不是键盘事件分发器，也不是应用自行创建的输入法实例。构造和析构是私有的，应用通过 `QGuiApplication::inputMethod()` 获得进程中的平台输入法对象；Qt Quick 中对应 `Qt.inputMethod`。

普通的 `QLineEdit`、`QTextEdit`、Qt Quick `TextInput` 已完成这套协议。只有自定义文本编辑器、嵌入式场景或需要随虚拟键盘移动内容的界面，才直接处理这些 API。

## 实际使用场景

- 自定义富文本编辑器接收预编辑文字，显示候选组合状态并提交最终文本。
- 移动端登录页根据 `keyboardRectangle()` 避免输入框被软键盘遮挡。
- Canvas/QQuick 嵌入场景将输入项局部坐标正确映射到窗口坐标。
- 程序化移动光标、插入文本或切换文档前，先处理正在进行的输入法组合。
- 候选词、拼写建议或选择菜单依据 `cursorRectangle()` 与 `anchorRectangle()` 定位。
- UI 根据 input locale 和方向调整候选面板或编辑行为。

## 获取对象与观察虚拟键盘

`show()`、`hide()` 与 `setVisible()` 都只是向平台**请求**打开或关闭虚拟键盘。没有虚拟键盘的桌面平台上，即使调用 `show()`，`isVisible()` 仍可保持 `false`。正常流程由可编辑控件获得或失去焦点自动触发，应用不应在每次点击时强制 show/hide。

```cpp
QInputMethod *im = QGuiApplication::inputMethod();

connect(im, &QInputMethod::keyboardRectangleChanged, this, [this, im] {
    updateBottomInset(im->keyboardRectangle());
});

connect(im, &QInputMethod::visibleChanged, this, [this, im] {
    setKeyboardAvoidanceEnabled(im->isVisible());
});
```

`keyboardRectangle()` 是窗口坐标中的虚拟键盘几何。它可能为空，例如 Android 的浮动键盘无法报告可靠矩形；空矩形不表示“键盘一定隐藏”。布局需要同时看 `isVisible()` 和矩形是否有效，并为平台差异保留回退策略。

`isAnimating()` 表示虚拟键盘正打开或关闭：`isAnimating() && isVisible()` 通常表示打开过程，`isAnimating() && !isVisible()` 通常表示关闭过程。要做平滑避让动画，应跟随相关 changed 信号，而非假设键盘立即到达最终位置。

## 自定义文本控件的输入法协议

输入法文本不是连续 `QKeyEvent::text()` 的简单替代。复杂语言输入可先产生可变的 preedit string，再在用户确认候选词时产生 commit string。自定义 QWidget 至少应：

1. 设定 `Qt::WA_InputMethodEnabled`，否则不会收到 `QInputMethodEvent`。
2. 重写 `inputMethodEvent()`，正确维护和绘制 preedit/commit。
3. 重写 `inputMethodQuery()`，回答光标矩形、选区、周边文本、输入 hints 等查询。
4. 编辑器状态变化后调用 `QInputMethod::update()`，通知平台重新查询。

```cpp
CustomEditor::CustomEditor(QWidget *parent)
    : QWidget(parent)
{
    setAttribute(Qt::WA_InputMethodEnabled);
}

void CustomEditor::moveCaret(int position)
{
    m_caret = position;
    QGuiApplication::inputMethod()->update(Qt::ImQueryInput);
}
```

尤其是光标位置变化时，应通知 `Qt::ImQueryInput`：光标变化通常同时影响 surrounding text、selection 和候选窗定位。若不调用 `update()`，输入法可能仍向旧坐标询问或按旧文本上下文给候选。

`queryFocusObject(query, argument)` 会向当前焦点对象发送输入法查询并返回 `QVariant` 结果。它属于输入法/平台集成的查询通道，不是绕过对象封装的通用属性读取工具；调用方必须了解对应 `Qt::InputMethodQuery` 所期待的类型和坐标系。

## 预编辑状态：commit、reset 与光标移动

`commit()` 将用户当前正在组合的词提交给编辑器。对于预测输入、转写或输入字符脚本与最终插入脚本不同的输入法，在下列操作前应 flush 组合状态：

- 将光标移动到别处；
- 切换编辑位置或文档；
- 执行会打断组合的命令。

否则新位置可能仍承接旧 preedit，或候选文本被提交到意外位置。

`reset()` 重置输入法状态。焦点编辑器改变时 Qt 会自动 reset；编辑器若要直接插入文本并准备接受新的输入，也可能在插入前调用它。`reset()` 与 `commit()` 的目的不同：前者让输入法重新同步状态，后者要求提交当前组合，不能在不理解编辑器行为时互换使用。

`invokeAction(Action, cursorPosition)` 由输入项在用户点击正在组合的词时调用。`Click` 和 `ContextMenu` 用于让输入法提供更多候选或相关操作；它是对输入法的语义通知，不会替你生成鼠标事件、移动光标或弹出 QWidget 菜单。

## 两套坐标系：输入项坐标与窗口坐标

`inputItemRectangle()` 是输入项自己的局部坐标；`inputItemTransform()` 将该局部坐标映射到窗口坐标。`setInputItemRectangle()` 与 `setInputItemTransform()` 主要面向 QQuickCanvas 一类“输入项嵌入在可变换场景中”的高级宿主，焦点项移动、缩放或焦点切换时必须更新。

以下矩形都在**窗口坐标**中：

| 几何 | 用途 |
| --- | --- |
| `cursorRectangle()` | 光标矩形，候选窗和预测提示通常跟随它。 |
| `anchorRectangle()` | 选择锚点矩形，选区相关提示可跟随它。 |
| `inputItemClipRectangle()` | 输入项实际可见的裁剪区域，虚拟键盘可据此估计可用空间。 |
| `keyboardRectangle()` | 平台报告的虚拟键盘区域。 |

不要将 `inputItemRectangle()` 直接与 `keyboardRectangle()` 做相交判断，也不要把变换后的 scene 坐标再额外映射一次。普通 QWidget/QML 文本控件由框架维护这组几何；手动设置 API 只适用于自己承担嵌入与坐标转换责任的宿主。

## locale、方向与状态信号

`locale()` 是当前输入法 locale，而非整个应用的 locale；例如用户可在英文 UI 中切换到日文输入法。`inputDirection()` 是当前文本输入方向，候选面板、光标附近控件和自定义编辑器的布局若要跟随输入法，应监听 `localeChanged()` / `inputDirectionChanged()`。

输入法状态会在平台设置、焦点、键盘动画或当前编辑器改变时变化。使用下列通知更新 UI，而非缓存首个读到的值：

- `cursorRectangleChanged()`、`anchorRectangleChanged()`
- `keyboardRectangleChanged()`、`inputItemClipRectangleChanged()`
- `visibleChanged()`、`animatingChanged()`
- `localeChanged()`、`inputDirectionChanged(Qt::LayoutDirection)`

## 常见错误

- 手动构造 `QInputMethod`，或把它当作每个窗口独占的对象。
- 没有虚拟键盘的平台仍强制依赖 `show()` 成功。
- 只在获得焦点时读取一次键盘矩形，忽略旋转、浮动键盘或动画变化。
- 看到空 `keyboardRectangle()` 就断言键盘不可见。
- 自定义文本控件未设置 `WA_InputMethodEnabled`，却期待收到组合输入。
- 只处理 commit text，不维护和绘制 preedit text 与 cursor/format attributes。
- 光标、选区或周边文本改变后未调用 `update(Qt::ImQueryInput)`。
- 将 `commit()` 和 `reset()` 混为同一种“清空输入法”操作。
- 混用输入项局部坐标与窗口坐标，导致候选框位置漂移。
- 用 `inputDirection()` 替代控件内容本身的 bidi 排版逻辑。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 获取 | `QGuiApplication::inputMethod()` | 非成员入口，取得 Qt 管理的全局输入法对象；`QInputMethod` 不可由应用构造或销毁。 |
| 类型 | `Action` | `Click` 表示点击组合词，`ContextMenu` 表示右键/长按上下文操作。 |
| 输入项几何 | `inputItemRectangle()` | 返回输入项局部坐标中的几何。 |
| 输入项几何 | `setInputItemRectangle(QRectF)` | 设置局部输入项几何；高级嵌入宿主在项移动或焦点改变时更新。 |
| 输入项变换 | `inputItemTransform()` | 返回从输入项局部坐标到窗口坐标的变换。 |
| 输入项变换 | `setInputItemTransform(QTransform)` | 设置该变换；普通文本控件通常无需调用。 |
| 光标/选区 | `cursorRectangle()` | 返回窗口坐标中的光标矩形，用于候选窗定位。 |
| 光标/选区 | `anchorRectangle()` | 返回窗口坐标中的 selection anchor 矩形。 |
| 可见区域 | `inputItemClipRectangle()` | 返回窗口坐标中的输入项裁剪区域，输入法据此评估可用空间。 |
| 键盘 | `keyboardRectangle()` | 返回窗口坐标的虚拟键盘矩形；平台无法获知时可为空。 |
| 键盘 | `isVisible()` / `setVisible(bool)` | 查询键盘是否可见，或请求 show/hide；没有虚拟键盘时请求可不生效。 |
| 键盘 | `show()` / `hide()` | 请求打开/关闭虚拟键盘；正常情况下由焦点变化自动管理。 |
| 键盘 | `isAnimating()` | 虚拟键盘是否正在打开或关闭；结合 `isVisible()` 判断方向。 |
| 语言 | `locale()` | 返回当前输入法 locale，不等同于应用 UI locale。 |
| 语言 | `inputDirection()` | 返回当前输入方向，用于输入相关 UI 适配。 |
| 查询 | `static queryFocusObject(Qt::InputMethodQuery, QVariant)` | 向当前焦点对象发送输入法查询并取得结果；argument/返回值类型由 query 决定。 |
| 状态同步 | `update(Qt::InputMethodQueries)` | 告知输入法哪些 query 属性已变；光标变化通常使用 `Qt::ImQueryInput`。 |
| 组合状态 | `commit()` | 提交当前组合词；移动光标等打断组合的操作前调用。 |
| 组合状态 | `reset()` | 重置输入法状态；焦点编辑器改变时自动发生，直接插入文本前可用于重新同步。 |
| 组合交互 | `invokeAction(Action, int cursorPosition)` | 告知输入法用户点击/长按组合词的位置，便于给出候选或操作。 |
| 信号 | `cursorRectangleChanged()` / `anchorRectangleChanged()` | 光标或 selection anchor 的窗口坐标变化。 |
| 信号 | `keyboardRectangleChanged()` / `inputItemClipRectangleChanged()` | 键盘区域或输入项可见裁剪区域变化。 |
| 信号 | `visibleChanged()` / `animatingChanged()` | 虚拟键盘可见状态或动画状态变化。 |
| 信号 | `localeChanged()` / `inputDirectionChanged(Qt::LayoutDirection)` | 当前输入法语言或输入方向变化。 |

## 相关类

- `QInputMethodEvent`：承载 preedit、commit 和属性的事件。
- `QInputMethodQueryEvent`：输入法向焦点对象查询编辑上下文的事件。
- `QGuiApplication`：提供全局 `inputMethod()` 入口。
- `QWidget::inputMethodEvent()` / `inputMethodQuery()`：自定义 Widget 编辑器的实现点。
- `QTextInput`、`TextArea`：Qt Quick 中已实现输入法协议的常用控件。

`QInputMethod` 的核心是保持编辑器、输入法和布局对“当前正在组合什么、光标在哪里、虚拟键盘占了多少空间”拥有同一份事实。只要焦点、文本或坐标变化后及时同步，复杂语言输入就不需要被拆成脆弱的按键猜测。
