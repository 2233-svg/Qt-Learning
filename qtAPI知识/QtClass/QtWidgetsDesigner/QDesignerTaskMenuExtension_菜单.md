# QDesignerTaskMenuExtension 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerTaskMenuExtension>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerTaskMenuExtension` 用来给自定义 widget 增加 Qt Widgets Designer 右键任务菜单项。它适合那些“设计期专用操作”无法仅通过属性编辑器表达的控件，例如：

- 打开专用编辑对话框编辑图表数据；
- 编辑状态机状态；
- 生成或清除内部页面；
- 导入一段 Designer 专用配置。

它不会替代控件运行时的普通右键菜单。这里返回的 `QAction` 是 Designer 选中该 widget 后，在设计器任务菜单中出现的编辑动作。

## 最小实现

具体扩展类通常继承 `QObject` 和 `QDesignerTaskMenuExtension`。动作对象应由扩展对象或另一个稳定 QObject 作为父对象，不能在 `taskActions()` 内临时创建后直接丢出去。

```cpp
class MyTaskMenuExtension final
    : public QObject
    , public QDesignerTaskMenuExtension
{
    Q_OBJECT
    Q_INTERFACES(QDesignerTaskMenuExtension)

public:
    MyTaskMenuExtension(MyWidget *widget, QObject *parent = nullptr)
        : QObject(parent), widget(widget)
    {
        editAction = new QAction(tr("Edit Data..."), this);
        connect(editAction, &QAction::triggered,
                this, &MyTaskMenuExtension::editData);
    }

    QList<QAction *> taskActions() const override
    {
        return {editAction};
    }

    QAction *preferredEditAction() const override
    {
        return editAction;
    }

private slots:
    void editData();

private:
    MyWidget *widget;
    QAction *editAction;
};
```

实现后还要通过 `QExtensionFactory` 注册到 manager，IID 使用 `Q_TYPEID(QDesignerTaskMenuExtension)`。Designer 通常在用户对 widget 打开任务菜单时才创建该扩展。

## `preferredEditAction()` 的规则

`preferredEditAction()` 是可选的。它用于决定选中 widget 后按 `F2` 触发哪个编辑动作。

返回的动作必须同时存在于 `taskActions()` 的返回列表中。若不重写或返回空指针，按 `F2` 不会为该扩展触发任何动作。这不影响右键菜单中其他动作的显示。

## 设计期动作的边界

任务菜单动作通常会改动当前 `.ui` 表单中的 widget 属性或子树。实现时应尽量通过 Designer 的表单编辑接口或可设计属性体系完成，使修改能被 Designer 感知、保存，并进入撤销栈。直接只改某个临时预览状态，可能在保存或撤销时丢失。

对于打开对话框的动作，注意对话框应面向设计期配置，不要依赖应用程序运行时尚未初始化的服务、文件路径或全局单例。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerTaskMenuExtension()` | 销毁任务菜单扩展接口。 | 具体实现一般继承 `QObject`，让 QObject parent 管理其生命周期。 |
| 默认编辑动作 | `preferredEditAction() const` | 返回选中 widget 后按 `F2` 应触发的动作。 | 返回值必须是 `taskActions()` 中的某一项；无默认动作时返回 `nullptr`。 |
| 菜单动作 | `taskActions() const` | 返回要加入 Designer 任务菜单的一组 `QAction`。 | 必须返回稳定存在的动作指针，不能返回已销毁或临时构造的动作。 |

## 易错点

1. 这不是运行时 context menu 的替代品，而是 Qt Designer 编辑期的任务菜单扩展。
2. 只实现接口还不够，必须经由 `QExtensionFactory` 和 `QExtensionManager` 注册。
3. `preferredEditAction()` 返回的动作如果不在 `taskActions()` 里，`F2` 行为不符合接口约定。
4. 动作修改的状态应能被 Designer 保存和撤销；不要只改设计预览的瞬态数据。

### 一句话总结

`QDesignerTaskMenuExtension` 为自定义 widget 的 Designer 右键菜单提供 `QAction` 列表，并可指定其中一个作为 `F2` 默认编辑动作。
