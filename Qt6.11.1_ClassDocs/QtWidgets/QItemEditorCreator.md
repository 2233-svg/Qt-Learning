# QItemEditorCreator

> Qt 6.11.1 · Qt Widgets · 来自 `QItemEditorCreator`

## 1. 先建立直觉

`QItemEditorCreator<T>` 是一个模板 creator，用来告诉 `QItemEditorFactory`：“编辑这种数据时创建 `T` 这个 QWidget，并用指定属性读写值。”它比手写 `QItemEditorCreatorBase` 子类更省事。

它适合已有编辑控件满足需求，只需要指定值属性名的情况。若你还要在创建后设置范围、选项、验证器，通常用 `QStandardItemEditorCreator<T>` 或自定义 creator 更方便。

## 2. 类说明

- 头文件：`#include <QItemEditorCreator>`
- 模块：`Qt6::Widgets`
- 继承自：`QItemEditorCreatorBase`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

这是模板工具类，不是 QWidget。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QItemEditorCreator(valuePropertyName)` | 指定编辑器值属性名。 |
| `createWidget(parent)` | 创建模板参数 `T` 类型的编辑器。 |
| `valuePropertyName()` | 返回构造时传入的属性名。 |

## 4. 关键用法

`QItemEditorCreator` 的核心参数是属性名。例如编辑 `QLineEdit` 的文本用 `text`，编辑 `QSpinBox` 的数值用 `value`。属性名必须是 Qt meta-object 能识别的 `Q_PROPERTY`。

```cpp
auto *factory = new QItemEditorFactory;
factory->registerEditor(QMetaType::Int,
    new QItemEditorCreator<QSpinBox>("value"));
```

如果属性名选错，例如给 `QCheckBox` 写成 `checkable` 而不是表达状态的属性，界面可能能显示控件，但数据读写语义不对。确认属性时看控件类的 `Q_PROPERTY`，不要凭直觉猜。

## 5. 常见坑与经验

- `T` 必须是 QWidget 派生类，并且能用 `QWidget *parent` 构造。
- 只适合简单属性映射，不适合复杂初始化。
- creator 被注册后由 factory 管理。
- delegate 默认使用 `EditRole` 数据进行编辑，模型类型要和注册类型匹配。
