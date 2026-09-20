# QItemEditorCreatorBase：item editor 创建器的抽象接口

> Qt 6.11.1 · `#include <QItemEditorFactory>` · 模块：`Qt6::Widgets`

`QItemEditorCreatorBase` 是 `QItemEditorFactory` 中“某种 QVariant 类型如何创建编辑器”的抽象接口。每个 creator 负责创建一种 editor widget，并告诉 delegate 哪个属性承载编辑值。

## 解决的问题

item delegate 需要把模型中的 `QVariant` 值放进某个 widget，再从 widget 取回值。不同 widget 的值属性不同：`QLineEdit::text`、`QSpinBox::value`、自定义控件的 `dateTime`。creator 把“创建控件”和“值属性名”封装起来，供 factory 按类型查找。

如果 editor 定义了 `USER` 属性，delegate 会优先通过元对象系统使用它；没有 user property 时才依赖 `valuePropertyName()`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `~QItemEditorCreatorBase()` | 虚析构，支持通过基类指针释放 creator。 |
| `createWidget(QWidget *parent) const` | 纯虚函数；返回新建 editor，必须使用传入 parent。 |
| `valuePropertyName() const` | 纯虚函数；返回编辑值属性名。 |
| 注册位置 | 通过 `QItemEditorFactory::registerEditor(userType, creator)` 注册。 |
| 所有权 | 注册后 creator 由 factory 管理。 |
| user property | editor 有 USER 属性时，delegate 通常不调用 `valuePropertyName()`。 |
