# QDesignerFormEditorInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerFormEditorInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QObject`

## 它解决什么问题

`QDesignerFormEditorInterface` 是嵌入式 Qt Widgets Designer 的核心对象入口。它把 Designer 的各个工作组件集中在一起：Widget Box、属性编辑器、对象查看器、动作编辑器、扩展管理器和窗体窗口管理器。

自定义 widget 插件的 `initialize(QDesignerFormEditorInterface *formEditor)` 参数就是当前 Designer core。插件通常不直接创建一个新 core，而是借这个对象取得当前环境中的服务，例如：

```cpp
void MyPlugin::initialize(QDesignerFormEditorInterface *formEditor)
{
    auto *manager = formEditor->extensionManager();
    manager->registerExtensions(
        new MyFactory(manager),
        Q_TYPEID(QDesignerTaskMenuExtension));
}
```

它适用于两类工作：

- **插件开发**：取得 extension manager，注册容器、属性表、任务菜单等扩展；
- **嵌入 Designer 的宿主程序**：组装或替换 Widget Box、属性编辑器、对象查看器和动作编辑器等面板。

普通单控件插件大多只需要 `extensionManager()`，其余 set/get API 更常出现在定制 Designer 主程序中。

## 它不是当前窗体

`QDesignerFormEditorInterface` 代表 Designer 整体环境，不是正在编辑的 `.ui` 文件。当前或全部窗体窗口应通过 `formWindowManager()` 查询；某个窗体的选择、属性修改、保存状态则由 `QDesignerFormWindowInterface` 及其 cursor API 处理。

```text
QDesignerFormEditorInterface
    -> QDesignerFormWindowManagerInterface
        -> QDesignerFormWindowInterface
            -> QDesignerFormWindowCursorInterface
```

这个层级很重要：不要把当前 form 的编辑命令直接发给 core，也不要把全局面板替换操作发给 form window。

## 面板接口的替换边界

`setActionEditor()`、`setObjectInspector()`、`setPropertyEditor()`、`setWidgetBox()` 是嵌入式 Designer 宿主用于安装组件的 API。对标准 Designer 插件来说，通常只读取相应指针；随意替换面板可能破坏宿主已经建立的对象关系和同步逻辑。

如果确实在自己的 Designer 宿主中组装这些组件，要确保：

- 面板属于同一个 form editor 环境；
- QWidget 父子关系、生命周期和布局由宿主管理；
- 面板会跟随 active form window 的变化正确刷新。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QDesignerFormEditorInterface(QObject *parent = nullptr)` | 创建 Designer core 接口对象。 | 插件通常不自行构造，而是使用 `initialize()` 传入的当前对象。 |
| 析构 | `virtual ~QDesignerFormEditorInterface()` | 销毁 Designer core 接口。 | 嵌入式 Designer 宿主应保证关联面板和管理器生命周期正确结束。 |
| 动作编辑器 | `actionEditor() const` | 返回 Designer 动作编辑器接口。 | 主要用于嵌入式 Designer 的动作管理；可能为空，调用前检查。 |
| 扩展管理器 | `extensionManager() const` | 返回当前 `QExtensionManager`。 | 自定义 widget 插件注册 Designer 扩展的主要入口。 |
| 窗体管理器 | `formWindowManager() const` | 返回窗体窗口管理器接口。 | 用它获取当前/所有正在编辑的窗体窗口。 |
| 对象查看器 | `objectInspector() const` | 返回对象查看器接口。 | 面向嵌入式 Designer 的对象层级面板控制。 |
| 属性编辑器 | `propertyEditor() const` | 返回属性编辑器接口。 | 处理属性面板焦点或当前对象时使用；普通属性读写仍应走 form window cursor。 |
| 安装动作编辑器 | `setActionEditor(QDesignerActionEditorInterface *actionEditor)` | 设置 Designer 使用的动作编辑器组件。 | 是宿主组装 API，不是普通插件初始化 API。 |
| 安装对象查看器 | `setObjectInspector(QDesignerObjectInspectorInterface *objectInspector)` | 设置 Designer 使用的对象查看器组件。 | 确保面板与同一 core 和窗体管理器协作。 |
| 安装属性编辑器 | `setPropertyEditor(QDesignerPropertyEditorInterface *propertyEditor)` | 设置 Designer 使用的属性编辑器组件。 | 替换后需保证选择变化能够正确同步。 |
| 安装 Widget Box | `setWidgetBox(QDesignerWidgetBoxInterface *widgetBox)` | 设置 Designer 使用的 Widget Box 组件。 | 不要在普通插件中替换全局 Widget Box。 |
| 顶层界面 | `topLevel() const` | 返回 Designer 的顶层 QWidget。 | 用于挂接宿主级对话框或定位，不等于当前编辑 form。 |
| Widget Box | `widgetBox() const` | 返回 Widget Box 接口。 | 用于嵌入式 Designer 定制可拖拽控件列表。 |

## 易错点

1. core 是 Designer 整体，不是某个 `.ui` 文档；操作当前窗体要经由 form window manager。
2. 自定义控件插件通常只需 `extensionManager()`，不要不必要地替换全局面板。
3. `topLevel()` 是 Designer 主界面，不是当前 form 的根 widget。
4. 返回的组件接口在嵌入式环境中可能尚未安装，使用前要检查空指针。

### 一句话总结

`QDesignerFormEditorInterface` 是 Designer 的服务总入口：插件用它注册扩展，嵌入式宿主用它访问或组装 Widget Box、属性编辑器、对象查看器和窗体管理器。
