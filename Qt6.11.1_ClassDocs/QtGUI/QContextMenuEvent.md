# QContextMenuEvent

> Qt 6.11.1 · Qt GUI · 来自 `QContextMenuEvent`

## 1. 先建立直觉

`QContextMenuEvent` 表示系统请求某个对象打开上下文菜单。它经常由鼠标右键触发，但也可以由键盘菜单键、`Shift+F10`、辅助技术或应用代码触发。

所以它表达的不是“右键按下”，而是“现在应该在这个位置提供上下文操作”。这一区分很重要：键盘触发时可能没有可靠的鼠标局部坐标，菜单应当以当前焦点对象或选区为上下文，而不是机械地使用一个坐标。

## 2. 类说明

`QContextMenuEvent` 继承自 `QInputEvent`。Widgets 通常在 `contextMenuEvent()` 中接收它，也可以在 `event()` 或事件过滤器里处理 `QEvent::ContextMenu`。

类说明只用于表明这些 API 来自 `QContextMenuEvent`：触发原因、局部位置和全局位置属于上下文菜单事件本身；菜单内容、动作状态和选区由接收控件决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum Reason` | 区分鼠标触发、键盘触发和其他来源。 |
| `QContextMenuEvent(reason, pos, globalPos, modifiers)` | 构造上下文菜单事件，指定来源和坐标。 |
| `reason() const` | 读取菜单请求的来源。 |
| `pos() const` | 返回相对于接收控件的局部位置；键盘触发时可能无效。 |
| `globalPos() const` | 返回屏幕或虚拟桌面位置。 |
| `x() const` / `y() const` | 读取局部坐标的整数分量。 |
| `globalX() const` / `globalY() const` | 读取全局坐标的整数分量。 |
| `modifiers() const` | 来自 `QInputEvent`，读取触发事件时的修饰键。 |

## 4. 关键用法

### 鼠标和键盘要分别选择菜单位置

```cpp
void DocumentView::contextMenuEvent(QContextMenuEvent *event)
{
    QPoint menuPos;
    if (event->reason() == QContextMenuEvent::Mouse)
        menuPos = event->globalPos();
    else
        menuPos = mapToGlobal(focusRect().center());

    QMenu menu(this);
    menu.addAction(actionCut);
    menu.addAction(actionCopy);
    menu.addAction(actionPaste);
    menu.exec(menuPos);
    event->accept();
}
```

键盘触发的上下文菜单应服务于当前焦点和选区。不要假设 `pos()` 总是有效，更不要在键盘触发时把菜单固定弹到屏幕左上角。

### 菜单动作状态由当前上下文决定

事件只告诉你“要开菜单”，不能替代选区、文档状态或权限判断。

```cpp
void TextEditor::contextMenuEvent(QContextMenuEvent *event)
{
    actionCut->setEnabled(textCursor().hasSelection());
    actionPaste->setEnabled(canPaste());
    actionUndo->setEnabled(document()->isUndoAvailable());
    m_contextMenu->exec(event->globalPos());
    event->accept();
}
```

### 未处理时交给基类

自定义控件只应拦截自己确实提供了菜单的区域；否则调用基类可以保留父控件或平台的默认行为。

## 5. 使用场景

`QContextMenuEvent` 适合文本编辑器、树/表视图、文件管理器、画布图元、属性面板、代码编辑器和设计器。右键菜单、键盘菜单键和辅助技术都可以统一进入这条路径。

它也适合实现“按焦点对象提供菜单”的无鼠标工作流。用户用 Tab 选中一个项目后按菜单键，菜单仍然应该出现在项目附近，并且动作状态对应当前项目。

## 6. 常见坑与经验

不要只重写 `mousePressEvent()` 里的右键分支来做上下文菜单。这样会漏掉键盘和辅助技术触发。

不要默认 `pos()` 有效。键盘来源可能没有鼠标位置，优先根据焦点、选区或控件几何体计算菜单锚点。

不要在 `QMenu::exec()` 返回后继续依赖事件对象的指针或位置做异步逻辑；事件生命周期只覆盖当前处理调用。

不要忘记 `accept()`。如果控件已经显示自己的菜单，就应明确告诉事件系统不要继续传播。

## 7. 知识点覆盖

学习 `QContextMenuEvent` 应覆盖上下文菜单语义、鼠标与键盘触发、局部和全局坐标、焦点菜单、选区状态、辅助技术、事件传播、`QMenu` 动态启用和平台菜单习惯。
