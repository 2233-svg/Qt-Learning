# QStandardItemEditorCreator

> Qt 6.11.1 · Qt Widgets · 来自 `QStandardItemEditorCreator`

## 1. 先建立直觉

`QStandardItemEditorCreator<T>` 是最省心的编辑器创建器：它创建 `T` 类型 QWidget，并从控件的 Qt user property 推断用于读写值的属性名。很多标准输入控件已经声明了合适的 user property。

如果控件的 user property 正好就是你要编辑的值，使用它比手写属性名更稳；如果不是，就改用 `QItemEditorCreator<T>` 指定属性名，或自定义 creator。

## 2. 类说明

- 头文件：`#include <QStandardItemEditorCreator>`
- 模块：`Qt6::Widgets`
- 继承自：`QItemEditorCreatorBase`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

这是模板工具类，用于 `QItemEditorFactory`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStandardItemEditorCreator()` | 创建标准 editor creator。 |
| `createWidget(parent)` | 创建模板参数 `T` 类型的编辑器。 |
| `valuePropertyName()` | 返回 `T` 的 user property 名称。 |

## 4. 关键用法

常见注册方式：

```cpp
auto *factory = new QItemEditorFactory;
factory->registerEditor(QMetaType::Double,
    new QStandardItemEditorCreator<QDoubleSpinBox>);
```

`QStandardItemEditorCreator` 的优势是不需要写 `"value"`、`"text"` 这类字符串；它依赖控件 meta-object 的 user property。标准控件通常没问题，自定义控件则要用 `Q_PROPERTY(... USER true)` 标出用户属性。

如果你要设置 `QDoubleSpinBox` 的范围、小数位、suffix 等，仅靠标准 creator 不够。此时写一个继承 `QItemEditorCreatorBase` 的 creator，在 `createWidget()` 里配置控件。

## 5. 常见坑与经验

- `T` 必须能用 `QWidget *parent` 构造。
- 自定义控件没有 user property 时，`valuePropertyName()` 不会得到你想要的属性。
- 标准 creator 解决创建和属性名，不负责业务校验。
- 同一类型在不同列需要不同范围时，不要只靠一个全局 factory。
