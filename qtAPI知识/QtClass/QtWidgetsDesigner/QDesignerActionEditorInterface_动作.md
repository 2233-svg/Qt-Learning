# QDesignerActionEditorInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerActionEditorInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QWidget`

## 它解决什么问题

`QDesignerActionEditorInterface` 是 Qt Widgets Designer 中“动作编辑器”面板的接口。动作编辑器专门管理 `.ui` 窗体里的 `QAction`，例如菜单栏、工具栏或快捷键会使用的“打开”“保存”“退出”等命令。

它解决的是插件或 Designer 集成需要控制动作编辑器内容的问题：

- 把某个 `QAction` 纳入 Designer 管理，使其出现在动作编辑器中；
- 让一个动作不再出现在动作编辑器中；
- 当活动 `.ui` 窗体切换时，让面板跟随新的 form window。

这不是应用程序中创建菜单的类，也不负责触发 `QAction`。它管理的是 **Designer 编辑阶段** 哪些动作可见、当前面板面对哪个 form window。

该接口不应直接实例化。自定义 widget 插件在 `QDesignerCustomWidgetInterface::initialize()` 获得 `QDesignerFormEditorInterface *core` 后，可通过 `core->actionEditor()` 取得现有动作编辑器。

```cpp
auto *editor = core->actionEditor();
editor->manageAction(exportAction);

// 切换插件关注的设计窗体时，动作编辑器也需要切换。
editor->setFormWindow(formWindow);
```

## 受管动作与普通动作的区别

调用 `manageAction(action)` 后，该动作会进入 Designer 动作编辑器，用户可以在编辑器中看到并编辑它。调用 `unmanageAction(action)` 后，Designer 忽略该动作，动作不会显示在动作编辑器里。

“不受管”不等于销毁，也不等于从 `QMenu` 或 `QToolBar` 移除。`QAction` 的对象所有权、连接关系和运行时行为仍由你的程序维护。此接口只改变 Designer 对该动作的编辑范围。

## 实现接口时的边界

`manageAction()`、`unmanageAction()` 与 `setFormWindow()` 都是纯虚函数，真正实现由 Designer 提供。一般插件只调用从 `core->actionEditor()` 得到的对象；只有重做 Designer 集成或内部面板时才需要派生实现。

因为它是 `QWidget`，访问它以及管理的 UI 状态应留在 GUI 线程。传入的 `QAction *` 应具有有效生命周期，且通常应属于当前或目标 form window 的对象树。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDesignerActionEditorInterface(QWidget *parent, Qt::WindowFlags flags = {})` | 构造动作编辑器接口 widget。 | 接口通常由 Designer 创建；插件不应自己构造替代品。 |
| 析构 | `~QDesignerActionEditorInterface()` | 销毁动作编辑器接口。 | 不要在 Designer 仍使用对象时手工释放从 `core->actionEditor()` 得到的指针。 |
| 所属核心 | `core() const` | 返回当前 Qt Widgets Designer 的 `QDesignerFormEditorInterface`。 | 返回指针由 Designer 持有；用于取得其它 Designer 服务，不要自行删除。 |
| 纳入管理 | `manageAction(QAction *action)` | 要求 Designer 管理指定动作，使它出现在动作编辑器中。 | 只改变 Designer 编辑器可见性，不改变动作的父对象、菜单归属或触发连接。 |
| 切换窗体 | `setFormWindow(QDesignerFormWindowInterface *formWindow)` | 将动作编辑器当前选中的 form window 改为 `formWindow`。 | 在多窗体 Designer 集成中调用；传入窗体必须仍由 Designer 管理。 |
| 取消管理 | `unmanageAction(QAction *action)` | 要求 Designer 忽略指定动作，使它不再显示在动作编辑器中。 | 不会销毁 `QAction`，也不会自动把它从菜单或工具栏移走。 |

## 易错点

1. `manageAction()` 管的是 Designer 动作编辑器，不是把动作添加进 `QMenu`。
2. `unmanageAction()` 后动作仍可能在运行时存在并正常触发。
3. 多个 `.ui` 窗体并存时，先确认动作编辑器当前的 `formWindow`。
4. 不要长期保存一个已经关闭的 form window 或动作指针。

### 一句话总结

`QDesignerActionEditorInterface` 是 Designer 动作编辑器的控制入口，用来决定哪些 `QAction` 可在编辑器中被设计和编辑，并让面板跟随当前 `.ui` 窗体。
