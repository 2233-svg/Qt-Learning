# QDesignerFormWindowManagerInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerFormWindowManagerInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QObject`

## 它解决什么问题

`QDesignerFormWindowManagerInterface` 是 Qt Widgets Designer 的多窗体工作区管理接口。一份 `.ui` 文件在 Designer 中对应一个 `QDesignerFormWindowInterface`；该管理器维护这些 form window 的集合、当前活动窗体、预览窗口和内置编辑动作。

它解决的是嵌入 Designer 或开发插件时的工作区协作问题：

- 创建、加入、移除和枚举多个 `.ui` form window；
- 设置当前活动窗体，让对象查看器、属性编辑器和画布同步；
- 获取 Designer 自己提供的剪切、撤销、布局和预览等 `QAction`；
- 打开预览、关闭全部预览或查看插件加载失败信息。

接口由 Designer 创建。插件通常从 `QDesignerCustomWidgetInterface::initialize(QDesignerFormEditorInterface *core)` 的参数取得：

```cpp
auto *manager = core->formWindowManager();
for (int i = 0; i < manager->formWindowCount(); ++i) {
    auto *form = manager->formWindow(i);
    // 处理每个当前打开的 .ui 窗体。
}
```

## 窗体集合和活动窗体

`createFormWindow()` 只负责创建一个 form window；要让它成为 Designer 工作区管理的一部分，还要调用 `addFormWindow()`。`removeFormWindow()` 则把窗体从集合中移除，不应想当然认为它必然销毁对象。

`activeFormWindow()` 返回当前活动窗体，`setActiveFormWindow()` 负责切换。插件不应通过给某个 `QWidget` 调 `setFocus()` 来替代它，因为 Designer 内部多个面板需要知道的是“活动 form window”，而不是普通键盘焦点。

应连接四个生命周期通知，在窗体集合变化时更新自己的缓存：

- `formWindowAdded()`：加入新窗体；
- `formWindowRemoved()`：移除窗体；
- `activeFormWindowChanged()`：活动窗体切换；
- `formWindowSettingsChanged()`：某个窗体的设置变化。

## `Action` 与 `ActionGroup`

`action(Action)` 返回 Designer 原有命令的 `QAction`，例如 `UndoAction`、`GridLayoutAction` 或 `DefaultPreviewAction`。这适合在 IDE 自己的菜单或工具栏中复用 Designer 的同一份命令和启用状态。

不要自己根据枚举实现一次“撤销”或“水平布局”来替代它。拿到的动作是 Designer 的原始动作，触发它才能沿用 Designer 当前窗体、撤销栈和启用状态。

`actionGroup(StyledPreviewActionGroup)` 返回风格化预览动作组，可用于在宿主 UI 中复用相互排斥的预览选项。

## 预览和插件诊断

`showPreview()` 用默认参数预览当前 form；`createPreviewPixmap()` 则返回当前活动 form 的预览图，适合做 IDE 缩略图。`closeAllPreviews()` 会关闭 Designer 目前打开的全部预览。

`showPluginDialog()` 打开 Designer 的插件诊断对话框，能显示已加载插件以及插件加载失败信息。遇到自定义控件未出现在控件盒中时，它是排查入口之一。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Action` | 标识可从 `action()` 获取的 Designer 内置命令。 | 复用返回的 `QAction`，不要复制一套与 Designer 脱节的命令逻辑。 |
| 枚举值 | `CutAction` | 剪切当前选择。 | 依赖活动 form window 和当前选择。 |
| 枚举值 | `CopyAction` | 复制当前选择。 | 依赖活动 form window 和当前选择。 |
| 枚举值 | `PasteAction` | 粘贴到当前 form。 | 剪贴板内容和当前窗体状态决定是否启用。 |
| 枚举值 | `DeleteAction` | 删除当前选择。 | 是改变 `.ui` 的编辑命令，应交给 Designer 的撤销体系处理。 |
| 枚举值 | `SelectAllAction` | 选中当前 form 中可选对象。 | 作用域是活动 form，不是宿主应用的全部 widget。 |
| 枚举值 | `LowerAction` | 降低当前选择的叠放顺序。 | 主要对可叠放的设计对象有意义。 |
| 枚举值 | `RaiseAction` | 提高当前选择的叠放顺序。 | 主要对可叠放的设计对象有意义。 |
| 枚举值 | `UndoAction` | 撤销 Designer 最近一次编辑。 | 使用 Designer 原始动作以保持其撤销栈和 enabled 状态。 |
| 枚举值 | `RedoAction` | 重做 Designer 最近撤销的编辑。 | 使用 Designer 原始动作以保持其重做栈状态。 |
| 枚举值 | `HorizontalLayoutAction` | 将选择应用为水平布局。 | 选择是否可布局由 Designer 决定。 |
| 枚举值 | `VerticalLayoutAction` | 将选择应用为垂直布局。 | 选择是否可布局由 Designer 决定。 |
| 枚举值 | `SplitHorizontalAction` | 在水平方向拆分或布局选择。 | 只在 Designer 支持的上下文中启用。 |
| 枚举值 | `SplitVerticalAction` | 在垂直方向拆分或布局选择。 | 只在 Designer 支持的上下文中启用。 |
| 枚举值 | `GridLayoutAction` | 将选择应用为网格布局。 | 由当前选区和父容器决定是否可用。 |
| 枚举值 | `FormLayoutAction` | 将选择应用为表单布局。 | 适合标签加编辑控件的表单结构。 |
| 枚举值 | `BreakLayoutAction` | 解除当前布局。 | 会改变 widget 的布局关系，应让 Designer 记录操作。 |
| 枚举值 | `AdjustSizeAction` | 按推荐尺寸调整当前选择。 | 结果受 size hint、布局和容器约束影响。 |
| 枚举值 | `SimplifyLayoutAction` | 简化当前布局结构。 | 可能改变布局层次，触发前应理解当前选区。 |
| 枚举值 | `DefaultPreviewAction` | 用默认参数预览当前 form。 | 与 `showPreview()` 面向相同预览工作流。 |
| 枚举值 | `FormWindowSettingsDialogAction` | 打开 form window 设置对话框。 | 作用于当前活动 form window。 |
| 枚举 | `ActionGroup` | 标识可从 `actionGroup()` 获取的 Designer 动作组。 | 用于共享一组互斥或相关的 Designer 动作。 |
| 枚举值 | `StyledPreviewActionGroup` | 标识包含带样式预览选项的动作组。 | 通过 `actionGroup()` 取得，不自行创建脱节的动作组。 |
| 构造 | `QDesignerFormWindowManagerInterface(QObject *parent = nullptr)` | 构造窗体管理器接口。 | 正常由 Designer 创建，插件通过 `core->formWindowManager()` 获取。 |
| 析构 | `~QDesignerFormWindowManagerInterface()` | 销毁窗体管理器接口。 | 不要手工删除由 Designer 拥有的管理器。 |
| 获取动作 | `action(Action action) const` | 返回指定 Designer 内置命令的原始 `QAction`。 | 返回指针不转移所有权；其可用状态随 Designer 上下文变化。 |
| 获取动作组 | `actionGroup(ActionGroup actionGroup) const` | 返回指定 Designer 动作组。 | 对动作组添加宿主 UI 前确认不改变其互斥和所有权关系。 |
| 活动窗体 | `activeFormWindow() const` | 返回当前活动 form window。 | 可能为空；不要缓存并假设它一直活动。 |
| 活动窗体通知 | `activeFormWindowChanged(QDesignerFormWindowInterface *formWindow)` | 当活动 form window 变化时发出。 | 用此信号同步插件面板和缓存，而不是轮询。 |
| 加入窗体 | `addFormWindow(QDesignerFormWindowInterface *formWindow)` | 将 form window 加入管理器维护的集合。 | 通常先由 `createFormWindow()` 创建；确认对象仍有效。 |
| 关闭预览 | `closeAllPreviews()` | 关闭当前打开的全部 Designer 预览窗口。 | 会影响同一 Designer 会话中的所有预览。 |
| 所属核心 | `core() const` | 返回关联的 `QDesignerFormEditorInterface`。 | 指针由 Designer 持有。 |
| 创建窗体 | `createFormWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())` | 创建一个新的 form window。 | 创建后还需 `addFormWindow()` 才进入管理集合。 |
| 预览缩略图 | `createPreviewPixmap() const` | 创建当前活动 form 的预览 `QPixmap`。 | 当前 form 为空或状态不完整时结果依实现而定；用于缩略图而非长期缓存。 |
| 按索引取窗体 | `formWindow(int index) const` | 返回指定索引的 form window。 | 有效范围是 `0` 到 `formWindowCount() - 1`。 |
| 窗体加入通知 | `formWindowAdded(QDesignerFormWindowInterface *formWindow)` | 新 form window 被加入时发出。 | 可在此建立关联，不要假设它已成为活动窗体。 |
| 窗体数量 | `formWindowCount() const` | 返回管理器当前维护的 form window 数量。 | 集合会随打开和关闭变化，遍历时避免使用陈旧索引。 |
| 窗体移除通知 | `formWindowRemoved(QDesignerFormWindowInterface *formWindow)` | form window 从管理器集合移除时发出。 | 立即清理插件中的非拥有型缓存。 |
| 设置变更通知 | `formWindowSettingsChanged(QDesignerFormWindowInterface *formWindow)` | 某个 form window 设置改变时发出。 | 用来刷新依赖窗体设置的宿主 UI。 |
| 移除窗体 | `removeFormWindow(QDesignerFormWindowInterface *formWindow)` | 将 form window 从管理器集合移除。 | 移除不必然等于销毁，具体所有权仍由创建路径决定。 |
| 切换活动窗体 | `setActiveFormWindow(QDesignerFormWindowInterface *formWindow)` | 将指定窗体设为活动 form window。 | 使用它同步 Designer 工作区，不要只设置普通 QWidget 焦点。 |
| 插件诊断 | `showPluginDialog()` | 打开已加载插件及插件加载失败信息的对话框。 | 自定义 widget 未出现或加载失败时优先使用。 |
| 显示预览 | `showPreview()` | 用默认参数显示当前 form 的预览。 | 预览的是活动 form；可用 `closeAllPreviews()` 批量关闭。 |

## 易错点

1. `createFormWindow()` 后必须 `addFormWindow()`，否则它不属于 Designer 工作区集合。
2. `removeFormWindow()` 不能被理解为“删除对象”；所有权由具体创建和父对象关系决定。
3. 菜单中复用 `action()` 返回的动作，不要复制文字和槽函数重新实现 Designer 命令。
4. 通过 `activeFormWindowChanged()` 同步状态，比自己猜测哪个 widget 获得焦点可靠。

### 一句话总结

`QDesignerFormWindowManagerInterface` 管理 Designer 的多 `.ui` 工作区、活动窗体、预览和原始编辑动作，是嵌入式 Designer 集成的调度中心。
