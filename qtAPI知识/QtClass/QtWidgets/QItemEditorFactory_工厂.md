# QItemEditorFactory：把 QVariant 类型映射到 item editor

> Qt 6.11.1 · `#include <QItemEditorFactory>` · 模块：`Qt6::Widgets`

`QItemEditorFactory` 是 item view 编辑器的注册表。delegate 根据模型 `Qt::EditRole` 中 `QVariant::userType()` 找到对应 creator，再创建编辑控件并知道该控件哪个属性承载值。

## 使用场景

如果某种数据类型在表格、树、列表中都要用同一个自定义 editor，不必在每个 delegate 里重写 `createEditor()`。创建 factory，注册 `QMetaType` 到 creator 的映射，再设置给某个 delegate 或设为全局默认 factory。

全局默认 factory 会影响依赖默认工厂的所有标准 delegate，适合统一应用行为，但也容易改变已有视图编辑体验。局部修改时优先给单个 delegate 设置工厂。

## 所有权和失败边界

`registerEditor()` 接管 creator 所有权。`createEditor()` 找不到映射可能返回 `nullptr`；`valuePropertyName()` 找不到映射可能返回空字节数组。不要把栈上 creator 注册进去。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QItemEditorFactory()` | 构造空工厂。 |
| `~QItemEditorFactory()` | 销毁工厂并释放已注册 creator。 |
| `createEditor(int userType, QWidget *parent) const` | 为指定元类型创建 editor；无映射时可返回 `nullptr`。 |
| `valuePropertyName(int userType) const` | 返回该类型 editor 的值属性名。 |
| `registerEditor(int userType, QItemEditorCreatorBase *creator)` | 注册类型到 creator；工厂接管 creator。 |
| `defaultFactory()` | 返回全局默认 editor factory。 |
| `setDefaultFactory(QItemEditorFactory *factory)` | 设置全局默认工厂；影响使用默认工厂的 delegate。 |
| 局部替换 | 用 delegate 的 `setItemEditorFactory()` 限定影响范围。 |
