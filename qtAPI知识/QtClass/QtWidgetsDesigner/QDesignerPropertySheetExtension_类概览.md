# QDesignerPropertySheetExtension 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerPropertySheetExtension>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerPropertySheetExtension` 是 Qt Widgets Designer 属性编辑器的适配接口。它让 Designer 能以统一方式读取和调整某个 widget 的属性列表，同时决定这些属性在属性编辑器中的可见性、分组、是否可编辑、是否已改变、能否恢复默认值，以及是否需要写入 `.ui` 文件。

它适合以下情况：

- 自定义 widget 的属性需要在 Designer 中重命名、隐藏、重新分组；
- 某些属性只用于 Designer 内部状态，不应写进 `.ui`；
- 属性默认值、已修改状态或 reset 行为需要自定义；
- 需要为非标准属性模型提供属性编辑器桥接。

对于普通 `Q_PROPERTY`，Designer 已能处理大量常规需求，不必轻易实现完整 property sheet。该接口需要维护完整且稳定的索引模型，适合确实要改变 Designer 属性编辑行为的插件。

## 属性索引模型

所有成员都围绕属性索引工作。你需要保证：

- `count()` 给出属性数；
- `indexOf(name)`、`propertyName(index)` 互相对应；
- `property(index)` 返回当前值；
- `isChanged(index)` 与 `setChanged(index, ...)` 描述相同的修改状态；
- `propertyGroup(index)` 与 `setPropertyGroup(index, ...)` 描述相同的分组。

可以用一张内部属性表存储名称、值、默认值、可见性、分组和 attribute 标记。不要把每个 API 各自临时计算成不同顺序，否则 Designer 会把属性值写到错误的属性上。

## `setProperty()` 不是带撤销的编辑入口

`setProperty()` 可以直接改 property sheet 的属性值，但 Qt 文档明确说明：**它不会更新 Qt Widgets Designer 的撤销栈**。如果是在响应 Designer 命令、任务菜单、专用编辑对话框后修改 widget 属性，并希望用户能撤销，应使用：

```cpp
QDesignerFormWindowCursorInterface *cursor = formWindow->cursor();
cursor->setWidgetProperty(widget, "title", "New Title");
```

或者使用 `QDesignerFormWindowCursorInterface::setProperty()`。`QDesignerPropertySheetExtension::setProperty()` 更适合 property sheet 自己实现其底层读写契约，而不是作为插件命令的高级修改入口。

## `isAttribute()` 的含义

这里的 attribute 不是 C++ attribute，也不是 XML 元素属性。若 `isAttribute(index)` 为 `true`，Designer 会把对应属性从生成的 `.ui` 文件中排除。它适合仅供 Designer 内部使用、或不应持久化到 UI 文件的状态。

不要把需要在运行时恢复的业务配置误标为 attribute；那样保存再加载 `.ui` 后它会丢失。

## reset、changed 与默认值

`hasReset()` 决定属性编辑器是否显示恢复按钮，`reset()` 负责真正恢复默认值，`isChanged()` 表示当前值是否不同于默认值。三者必须一致：

- `hasReset(index)` 为真时，`reset(index)` 应能返回 `true` 并恢复默认值；
- reset 成功后通常应令 `isChanged(index)` 变为假；
- `setChanged(index, true)` 不应只改 UI 标记而不维护实际默认值比较逻辑。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerPropertySheetExtension()` | 销毁属性表扩展接口。 | 实现类通常由扩展 factory 创建，生命周期应与 Designer 扩展系统协调。 |
| 属性数量 | `count() const` | 返回当前 widget 的属性数量。 | 所有以 `index` 为参数的 API 都必须遵守同一范围和顺序。 |
| 重置能力 | `hasReset(int index) const` | 判断属性编辑器是否应为该属性显示恢复默认值按钮。 | 返回真时应保证 `reset(index)` 能处理该属性。 |
| 按名查找 | `indexOf(const QString &name) const` | 返回属性名对应的索引。 | 找不到应返回无效索引；与 `propertyName(index)` 保持双向一致。 |
| UI 文件排除标记 | `isAttribute(int index) const` | 判断属性是否作为 Designer attribute，从 `.ui` 文件排除。 | 这会影响持久化；不要隐藏必须随 UI 保存的业务属性。 |
| 修改状态 | `isChanged(int index) const` | 判断当前属性值是否不同于默认值。 | 影响 Designer 的属性保存和显示逻辑；要与 reset、setChanged 一致。 |
| 启用状态 | `isEnabled(int index) const` | 判断属性编辑器中该属性是否可编辑。 | 禁用只影响编辑器交互，不必然改变 widget 的运行时可写性。 |
| 可见状态 | `isVisible(int index) const` | 判断属性是否在属性编辑器中显示。 | 隐藏不等于不保存；是否保存由 `isAttribute()` 等规则决定。 |
| 属性值 | `property(int index) const` | 返回指定属性当前值。 | `QVariant` 类型要能被 Designer 正确编辑和序列化。 |
| 属性分组 | `propertyGroup(int index) const` | 返回属性编辑器中的分组名。 | 默认分组通常是定义属性的类名；分组仅影响编辑器组织。 |
| 属性名 | `propertyName(int index) const` | 返回指定属性名称。 | 应是稳定、可查找的属性标识，不要只返回本地化显示文本。 |
| 重置 | `reset(int index)` | 将属性恢复为默认值，成功返回 `true`。 | 重置后要同步实际值与 changed 状态；没有默认值时返回 `false`。 |
| UI 文件排除标记 | `setAttribute(int index, bool attribute)` | 设置属性是否从 `.ui` 输出排除。 | 改变持久化语义，使用前确认重新打开 UI 后不需要该属性。 |
| 修改状态 | `setChanged(int index, bool changed)` | 标记属性是否不同于默认值。 | 应与当前值、默认值和 `reset()` 结果一致。 |
| 设置属性值 | `setProperty(int index, const QVariant &value)` | 设置指定属性的值。 | **不会更新 Designer 撤销栈**；用户可撤销的操作要改用 form window cursor 的设置 API。 |
| 属性分组 | `setPropertyGroup(int index, const QString &group)` | 修改属性在属性编辑器中的分组。 | 不改变 widget 属性值或元对象定义。 |
| 可见状态 | `setVisible(int index, bool visible)` | 显示或隐藏属性编辑器中的属性。 | 只改 Designer 呈现；与是否写入 `.ui` 是两件事。 |

## 易错点

1. property sheet 管的是属性编辑器，不是信号槽编辑器；后者应使用 `QDesignerMemberSheetExtension`。
2. `setProperty()` 不会记入撤销栈。由插件命令触发的可撤销改动应走 `QDesignerFormWindowCursorInterface`。
3. `isAttribute()` 为真会让属性从 `.ui` 排除，不是单纯“在编辑器里隐藏”。
4. 属性索引必须稳定一致，否则 Designer 会读写错误属性。
5. 隐藏属性、禁用属性、排除 UI 文件是三种不同的语义，不能混为一谈。

### 一句话总结

`QDesignerPropertySheetExtension` 是自定义 widget 的 Designer 属性编辑器模型：它描述属性值、默认值、分组、可见性和持久化规则；涉及用户编辑时要特别避开 `setProperty()` 的撤销栈陷阱。
