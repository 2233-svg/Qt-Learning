# QStandardItemEditorCreator：用 editor 的 USER 属性注册编辑器

> Qt 6.11.1 · `#include <QItemEditorFactory>` · 模块：`Qt6::Widgets` · 继承：`QItemEditorCreatorBase`

`QStandardItemEditorCreator<T>` 是注册 item editor 最常用的模板。它创建 `T(parent)`，并自动使用 `T::staticMetaObject.userProperty()` 作为值属性。

## 使用场景

当你的 editor 类已经在 `Q_PROPERTY` 中用 `USER true` 标出编辑值属性时，用这个模板最省事。delegate 可以通过元对象系统读写该属性，不需要你手写 creator 子类或传属性名。

如果 editor 没有 user property，或者要用非 user 属性，改用 `QItemEditorCreator<T>`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QStandardItemEditorCreator<T>()` | 从 `T` 的 user property 记录值属性名。 |
| `createWidget(QWidget *parent) const` | 返回 `new T(parent)`。 |
| `valuePropertyName() const` | 返回 `T` 的 user property 名称。 |
| 前提 | `T` 应有可用的 USER 属性，并可用 `QWidget *parent` 构造。 |
| 典型用途 | 注册自定义日期、颜色、枚举等类型的 editor。 |
