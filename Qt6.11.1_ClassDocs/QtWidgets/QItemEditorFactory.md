# QItemEditorFactory

> Qt 6.11.1 · Qt Widgets · 来自 `QItemEditorFactory`

## 1. 先建立直觉

`QItemEditorFactory` 是 item delegate 的“编辑器注册表”：给它一个 QVariant 类型 id，它返回适合编辑这种数据的 QWidget，并告诉 delegate 应该读写这个控件的哪个属性。

它主要服务于 `QStyledItemDelegate` 和 `QItemDelegate`。如果你只是某一列要用特殊编辑器，重写 delegate 的 `createEditor()` 更直接；如果你希望某种数据类型在很多视图里都自动使用同一种编辑器，工厂更合适。

## 2. 类说明

- 头文件：`#include <QItemEditorFactory>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

工厂本身不显示界面；它在 delegate 需要编辑器时被调用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QItemEditorFactory()` | 创建编辑器工厂。 |
| `createEditor(userType, parent)` | 根据类型创建编辑器 QWidget。 |
| `registerEditor(userType, creator)` | 注册某类型对应的编辑器创建器；工厂接管 creator 所有权。 |
| `valuePropertyName(userType)` | 返回该类型编辑器用于读写值的属性名。 |
| `defaultFactory()` | 获取全局默认工厂。 |
| `setDefaultFactory(factory)` | 设置全局默认工厂，新旧 delegate 都会使用。 |

## 4. 关键用法

典型流程是创建工厂，注册类型到 `QItemEditorCreatorBase`，再交给 delegate：

```cpp
auto *factory = new QItemEditorFactory;
factory->registerEditor(QMetaType::Double, new QStandardItemEditorCreator<QDoubleSpinBox>);

auto *delegate = new QStyledItemDelegate(view);
delegate->setItemEditorFactory(factory);
view->setItemDelegate(delegate);
```

delegate 创建编辑器后，会通过 `valuePropertyName()` 对应的 Qt 属性把 model 数据写进控件，再从控件读回。控件的属性类型要能接受该 QVariant 类型，否则编辑器能显示但提交会不对。

全局 `setDefaultFactory()` 影响范围很大，适合应用统一风格；局部差异更推荐给某个 delegate 单独设置 factory。

## 5. 常见坑与经验

- `registerEditor()` 后工厂拥有 creator；不要再手动删除同一个 creator。
- 类型 id 要和 model 返回的 `EditRole` 数据类型一致。
- 编辑器必须有可读写的 value 属性或用户属性。
- 全局默认工厂会影响现有 delegate，库代码里慎用。
- 每个 index 都不同的编辑规则，不适合塞进 factory，直接写 delegate 更清晰。
