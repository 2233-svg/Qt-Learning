# QItemDelegate：为 item view 绘制和编辑模型数据

> Qt 6.11.1 · `#include <QItemDelegate>` · 模块：`Qt6::Widgets` · 继承：`QAbstractItemDelegate`

`QItemDelegate` 是 model/view 视图的委托类，负责把模型索引绘制成单元格，并在编辑时创建 editor widget、把模型数据写入 editor、再把 editor 的值提交回模型。

## 使用场景

它适合需要兼容旧代码或直接定制经典 item 绘制的场景。新代码通常优先从 `QStyledItemDelegate` 派生，因为它使用当前 style 绘制，更适合现代 Qt 风格和样式表。无论使用哪个委托，模型都应通过 `Qt::DisplayRole`、`EditRole`、`DecorationRole`、`CheckStateRole` 等角色提供数据。

若只是改变某种数据类型用什么编辑控件，不一定要派生 delegate；注册 `QItemEditorFactory` 往往更轻。

## 绘制与编辑边界

重写 `paint()` 时要按 `option.state` 处理选中、禁用、焦点、勾选等状态，并在修改 painter 状态后恢复。`clipping` 默认开启，避免超出单元格绘制。

编辑流程是 `createEditor()` 创建控件，`setEditorData()` 从模型填值，`updateEditorGeometry()` 放置控件，`setModelData()` 提交回模型。默认编辑器由 `QItemEditorFactory` 根据 `Qt::EditRole` 的 `QVariant` 类型决定。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QItemDelegate(QObject *parent = nullptr)` | 构造委托。 |
| `hasClipping() const` / `setClipping(bool)` | 控制绘制是否裁剪到 item 区域，默认开启。 |
| `paint(QPainter *, option, index)` | 绘制单元格；自定义绘制时要处理状态并恢复 painter。 |
| `sizeHint(option, index)` | 返回单元格推荐尺寸。 |
| `createEditor(parent, option, index)` | 创建编辑器，默认使用 item editor factory。 |
| `setEditorData(editor, index)` | 把模型数据写入编辑器。 |
| `setModelData(editor, model, index)` | 把编辑器数据写回模型。 |
| `updateEditorGeometry(editor, option, index)` | 设置编辑器几何位置。 |
| `itemEditorFactory() const` | 返回本 delegate 专用工厂；未设置时可为 null。 |
| `setItemEditorFactory(QItemEditorFactory *)` | 设置本 delegate 的编辑器工厂。 |
| `drawDisplay/drawDecoration/drawCheck/drawFocus` | 分块绘制钩子，适合局部定制经典绘制。 |
| `editorEvent(...)` | 处理不创建 editor 的交互，如复选框点击。 |
| `QStyledItemDelegate` | 新委托通常优先使用它，尤其涉及 style/style sheet 时。 |
