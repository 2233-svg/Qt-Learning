# QDesignerObjectInspectorInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerObjectInspectorInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QWidget`

## 它解决什么问题

`QDesignerObjectInspectorInterface` 是 Qt Widgets Designer 的对象查看器接口。对象查看器就是 Designer 中展示窗体对象树的面板：顶层窗体、子 widget、布局、动作等对象会以层次结构出现，用户可通过它定位需要编辑的对象。

它最核心的职责只有一个：**切换对象查看器正在展示的 form window**。当 IDE 集成或插件切换活动 `.ui` 窗体时，对象树也必须切换，否则树中显示的对象与属性编辑器、画布中的对象会来自不同窗体。

接口不应直接实例化。插件通常从 `QDesignerCustomWidgetInterface::initialize()` 得到的 form editor 获取它：

```cpp
auto *manager = core->formWindowManager();
auto *firstForm = manager->formWindow(0);

core->objectInspector()->setFormWindow(firstForm);
```

## 它不负责什么

- 它不是通用的 `QTreeView` 数据模型，不能用来随意维护应用自己的对象树；
- 它不直接提供“选中某个 widget”的 API；精确控制 Designer 选区应使用 `QDesignerFormWindowInterface::cursor()` 或选择 API；
- 它不拥有 form window，窗体的创建、销毁和活动状态由 `QDesignerFormWindowManagerInterface` 管理。

## 使用场景

最常见的场景是嵌入式 Designer 或插件面板同步：窗体管理器发生活动窗体切换后，调用 `setFormWindow()` 更新对象查看器。若没有可用窗体，可以按具体 Designer 实现传入空指针以清空上下文；调用方不应保留已经移除的窗体指针。

作为 `QWidget` 接口，它应只在 GUI 线程访问。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDesignerObjectInspectorInterface(QWidget *parent, Qt::WindowFlags flags = {})` | 构造对象查看器接口 widget。 | 正常由 Designer 创建；应用插件不应自行替代其对象树实现。 |
| 析构 | `~QDesignerObjectInspectorInterface()` | 销毁对象查看器接口。 | `core->objectInspector()` 返回的对象由 Designer 管理。 |
| 所属核心 | `core() const` | 返回当前 Designer 的 `QDesignerFormEditorInterface`。 | 用于回到其它 Designer 服务；返回指针不转移所有权。 |
| 切换窗体 | `setFormWindow(QDesignerFormWindowInterface *formWindow)` | 设置对象查看器当前显示和选择的 form window。 | 在窗体切换时同步调用；不要传入已被窗体管理器移除的对象。 |

## 易错点

1. 它切换的是整个对象查看器的窗体上下文，不等价于选中某一个对象。
2. 不要把它当作普通应用 UI 的对象树控件。
3. form window 生命周期归窗体管理器，接口只引用它。

### 一句话总结

`QDesignerObjectInspectorInterface` 是 Designer 对象树面板的窗体上下文入口，主要用于让对象查看器与当前 `.ui` 窗体保持同步。
