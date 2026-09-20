# QDesignerPropertyEditorInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerPropertyEditorInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QWidget`

## 它解决什么问题

`QDesignerPropertyEditorInterface` 是 Qt Widgets Designer 的属性编辑器接口。它对应 Designer 中显示 `objectName`、`geometry`、`text`、`font` 等属性的面板，并提供“当前对象”“当前属性”“只读状态”和“属性修改通知”这几个协作点。

它适用于自定义 widget 插件、IDE 集成或 Designer 扩展需要：

- 知道当前正在编辑哪个 `QObject`；
- 得到当前高亮的属性名称；
- 监听用户在属性面板中完成的修改；
- 改变属性编辑器当前对象或写保护状态；
- 从外部刷新某个属性在编辑器中的值和 changed 标记。

接口不应直接构造。插件初始化时取得 `QDesignerFormEditorInterface *core`，再调用 `core->propertyEditor()`。

```cpp
auto *propertyEditor = core->propertyEditor();
connect(propertyEditor, &QDesignerPropertyEditorInterface::propertyChanged,
        this,
        [this](const QString &name, const QVariant &value) {
            if (name == "objectName")
                updateLabel(value.toString());
        });
```

## 当前对象、当前属性与变更信号

`object()` 返回属性面板当前对应的对象，`currentPropertyName()` 返回用户当前聚焦的属性行。它们适合做上下文感知的插件 UI，例如仅在用户选中 `text` 属性时显示辅助编辑工具。

`propertyChanged(name, value)` 在属性编辑器中的某属性改变时发出。它是观察用户编辑结果的好入口，但处理代码不应再次无条件调用 `setPropertyValue()`，否则容易造成重复刷新甚至反馈循环。

## `setPropertyValue()` 中 `changed` 的真实含义

`setPropertyValue(name, value, changed)` 除了设置显示值，还会决定属性在属性编辑器中是否标记为“不同于默认值”。默认 `changed = true`，表示该值应被视为显式修改。

这并不自动等于“设计操作已经进入撤销栈”。需要进行可撤销的用户级修改时，优先用 `QDesignerFormWindowCursorInterface::setWidgetProperty()`；属性编辑器接口更适合面板同步和属性状态维护。

## 只读状态

`setReadOnly(true)` 让属性编辑器进入写保护状态，`isReadOnly()` 用来查询。它影响面板能否编辑，不会自动阻止其它代码通过 `QObject::setProperty()` 改对象，也不会替代 Designer 的权限或业务校验。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDesignerPropertyEditorInterface(QWidget *parent, Qt::WindowFlags flags = {})` | 构造属性编辑器接口 widget。 | 通常通过 `QDesignerFormEditorInterface::propertyEditor()` 取得，不直接创建。 |
| 析构 | `~QDesignerPropertyEditorInterface()` | 销毁属性编辑器接口。 | 返回接口归 Designer 所有，不要由插件删除。 |
| 所属核心 | `core() const` | 返回当前 `QDesignerFormEditorInterface`。 | 指针非拥有型，可用来访问窗体管理器等 Designer 服务。 |
| 当前属性 | `currentPropertyName() const` | 返回属性面板当前选中属性的名称。 | 属性名是稳定的内部属性名，不是本地化显示标题。 |
| 只读查询 | `isReadOnly() const` | 判断属性面板是否处于写保护状态。 | 只反映编辑器交互状态，不保证对象在其它路径不可修改。 |
| 当前对象 | `object() const` | 返回 Designer 当前正在显示属性的对象。 | 可能为空；对象可能随选择改变而失效，不要无保护地长期缓存。 |
| 修改通知 | `propertyChanged(const QString &name, const QVariant &value)` | 当属性编辑器中某属性发生改变时发出，携带属性名和新值。 | 用作观察入口；槽中再次设置同一属性时要避免反馈循环。 |
| 选择对象 | `setObject(QObject *object)` | 将属性编辑器当前对象切换为指定对象。 | 对象应属于当前 Designer 工作区；切换后当前属性行也可能变化。 |
| 设置属性值 | `setPropertyValue(const QString &name, const QVariant &value, bool changed = true)` | 更新指定属性的值，并标记它是否不同于默认值。 | `changed` 影响 Designer 的属性状态；可撤销的窗体编辑优先走 form window cursor。 |
| 写保护 | `setReadOnly(bool readOnly)` | 开启或关闭属性编辑器的写保护。 | 只控制面板编辑能力，不等同于冻结对象或撤销权限。 |

## 易错点

1. `currentPropertyName()` 不是当前对象名称，当前对象应由 `object()` 获取。
2. `setReadOnly()` 仅限制属性面板，不能作为业务层的只读保护。
3. `setPropertyValue()` 的 `changed` 表示与默认值的差异，不是一般的“操作是否成功”。
4. 响应 `propertyChanged()` 时要避免重新写回同一值形成循环。

### 一句话总结

`QDesignerPropertyEditorInterface` 是 Designer 属性面板的状态与通知接口：它把当前对象、当前属性、写保护和属性变更连接到插件或 IDE 集成中。
