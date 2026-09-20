# QItemEditorCreator：用显式属性名注册编辑器类型

> Qt 6.11.1 · `#include <QItemEditorFactory>` · 模块：`Qt6::Widgets` · 继承：`QItemEditorCreatorBase`

`QItemEditorCreator<T>` 是一个模板 creator，用来告诉 `QItemEditorFactory`：编辑某种数据类型时 new 一个 `T(parent)`，并用指定属性名读写值。

## 使用场景

当 editor widget 没有合适的 `USER` 属性，或者你想明确指定某个属性作为编辑值时，使用 `QItemEditorCreator<T>("propertyName")`。如果 editor 已经声明了正确的 user property，`QStandardItemEditorCreator<T>` 更简洁。

`T` 必须是可用 `QWidget *parent` 构造的 widget 类型，并且指定属性应能接受注册的 `QMetaType` 对应值。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QItemEditorCreator<T>(const QByteArray &valuePropertyName)` | 保存 editor 值属性名。 |
| `createWidget(QWidget *parent) const` | 返回 `new T(parent)`。 |
| `valuePropertyName() const` | 返回构造时传入的属性名。 |
| 适用前提 | editor 无合适 USER 属性，或需要显式指定属性。 |
| 与 factory | 作为 `registerEditor()` 的 creator 参数，注册后由 factory 持有。 |
