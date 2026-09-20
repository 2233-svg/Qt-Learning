# QQmlListReference：在不知道模板元素类型时检查和操作 QML 列表

> Qt 6.11.1 | `#include <QQmlListReference>` | CMake: `Qt6::Qml`

`QQmlListReference` 是 `QQmlListProperty<T>` 的类型擦除视图。它解决的是工具、框架和通用 C++ 代码的难题：只拿到一个 `QObject *` 和属性名时，元素类型 `T` 在编译期未知，怎样仍然安全地读取或修改那个 QML 列表属性。

它不保存列表的快照；持有的是对属性操作回调的引用。owner 对象被销毁后，引用会自动变为无效。

## 常见场景：通用对象树检查器

例如设计器、测试工具或组件容器只知道目标对象和 `children` 属性名。它可以先创建 reference，再逐项确认可读性：

```cpp
QQmlListReference children(item, "children");
if (!children.isReadable())
    return;

for (qsizetype i = 0; i < children.count(); ++i) {
    QObject *child = children.at(i);
    inspect(child);
}
```

构造还可以来自保存了 list property 的 `QVariant`。这在通过 Qt 元对象系统读取属性后很方便：

```cpp
const QVariant value = item->property("children");
QQmlListReference children(value);
```

`isValid()` 只表示“引用构造到了一个有效的列表属性”；它不保证每一项操作都存在。列表可以只支持 append，或者只支持读取。

## 先问能力，再做动作

泛型代码应遵循这个顺序：

1. 用 `isValid()` 排除失效或非列表属性。
2. 对读取使用 `canCount()` 和 `canAt()`，再调用 `count()`、`at()`。
3. 对写入使用对应的 `canAppend()`、`canClear()`、`canReplace()`、`canRemoveLast()`。
4. 调用 `append()` 或 `replace()` 前，用 `listElementType()` 检查候选对象的元对象类型是否兼容。

```cpp
if (children.canAppend()) {
    const QMetaObject *expected = children.listElementType();
    if (expected && widget->metaObject()->inherits(expected))
        children.append(widget);
}
```

`append()`、`replace()` 会做元素类型检查并用 `bool` 返回结果；不要据此省略自己的能力检查。`at(index)` 在操作失败时可返回空指针，但下标范围仍由调用方保证，必须小于 `count()`。

## 可读与可操作并不等价

`isReadable()` 意味着能够 count 和 at。`isManipulable()` 要求能读取、追加，并且能 clear 或 removeLast；`replace` 与 `removeLast` 可以被框架用“暂存后重建”模拟，因此它们不是 `isManipulable()` 的硬前提。

这个区别很重要：一个只读列表能被检查器遍历，却不能被编辑器修改；一个只能 append 的列表也不一定能安全实现“删除第 N 项”。

两个分别构造、但都指向同一个对象同一个属性的 `QQmlListReference` 不要求 `operator==` 为真。相等性比较的是内部引用身份，不是“逻辑上指向同一列表”，因此不要用它判断属性路径是否相同。

## 生命周期和版本边界

`QQmlListReference` 跟踪其对象的销毁，失效后 `isValid()` 为 false，`object()` 与 `listElementType()` 返回空。该保护不能让原本失效的元素指针重新有效：从 `at()` 取出的对象仍遵守自身 QObject 生命周期。

Qt 6.4 前有带 `QQmlEngine *` 参数的构造函数；Qt 6.11.1 中它们仍可见但已弃用。新代码使用不带 engine 的构造函数。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlListReference(QObject *, const char *)` | 按 owner 和属性名引用 list property | 属性不是兼容列表时 reference 无效 |
| `QQmlListReference(const QVariant &)` | 从含 list property 的 QVariant 建立引用 | QVariant 必须确实承载该属性类型 |
| `isValid()` | 判断 owner 和列表引用仍有效 | 不代表所有读写回调都可用 |
| `object()` | 取得列表所属对象 | 无效时返回 `nullptr` |
| `listElementType()` | 返回元素的 `QMetaObject` | 无效时为 `nullptr`；用于预先做类型兼容性判断 |
| `canAppend()` / `canReplace()` 等 | 查询单项操作是否被实现 | 每个操作独立，不可由 `isValid()` 推断 |
| `isReadable()` | 判断是否可 count 并按下标读取 | 读取前仍要控制 `at()` 的下标范围 |
| `isManipulable()` | 判断可读取、追加且可清空/尾删 | 不代表每个高阶操作都有原生实现 |
| `append(QObject *)` | 尝试追加兼容元素 | 返回 false 表示不支持或类型不匹配 |
| `at(qsizetype)` / `count()` | 读取元素或长度 | 调用者确保 `0 <= index < count()` |
| `clear()` / `replace()` / `removeLast()` | 修改底层列表 | 返回 false 时不可假设发生了部分修改 |

## 相关类型

- `QQmlListProperty<T>`：列表能力的实际提供者。
- `QMetaObject`：用来判断候选 `QObject` 是否是列表元素类型或其派生类。
- `QVariant`：通过动态属性和元对象 API 传递 list property 的载体。
