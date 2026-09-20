# QItemEditorCreatorBase

> Qt 6.11.1 · Qt Widgets · 来自 `QItemEditorCreatorBase`

## 1. 先建立直觉

`QItemEditorCreatorBase` 是编辑器创建器的抽象基类。`QItemEditorFactory` 不直接知道如何创建每一种 QWidget，它只保存一组 creator；真正创建控件、报告值属性名的工作由这个接口完成。

你一般不会直接使用它，除非标准模板创建器不能满足需求，例如编辑器构造后还要设置范围、精度、候选项或验证器。

## 2. 类说明

- 头文件：`#include <QItemEditorCreatorBase>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：`QItemEditorCreator`、`QStandardItemEditorCreator`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

这是非 QObject 抽象接口，被 `QItemEditorFactory` 持有和调用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `~QItemEditorCreatorBase()` | 虚析构，允许通过基类指针删除。 |
| `createWidget(parent)` | 纯虚函数；创建一个新的编辑器 QWidget。 |
| `valuePropertyName()` | 纯虚函数；返回 delegate 读写编辑值的属性名。 |

## 4. 关键用法

实现 creator 时，`createWidget()` 每次都要返回一个新控件，并把传入的 `parent` 交给构造函数。不要复用同一个编辑器实例；一个 editor 同一时刻只能服务一个单元格。

`valuePropertyName()` 返回的属性应当是控件的真实 Qt 属性，例如 `value`、`text`、`currentIndex`。`QStyledItemDelegate` 会用这个属性和 model 的 `EditRole` 交换数据。

如果控件有 Qt user property，delegate 可能优先使用 user property。需要完全控制读写过程时，重写 delegate 的 `setEditorData()` 和 `setModelData()` 更直接。

## 5. 常见坑与经验

- creator 由 factory 接管所有权后，不要在外部删除。
- 属性名拼错不会在编译期报错，通常表现为编辑器显示空值或提交失败。
- 编辑器初始化配置放在 `createWidget()` 里，例如范围、步长、suffix。
- 如果同一数据类型在不同列需要不同控件，不要注册成全局 creator。
