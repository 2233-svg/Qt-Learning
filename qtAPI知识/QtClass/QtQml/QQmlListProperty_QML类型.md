# QQmlListProperty：把 QObject 列表作为 QML 的对象子列表公开

> Qt 6.11.1 | `#include <QQmlListProperty>` | CMake: `Qt6::Qml`

`QQmlListProperty<T>` 是 C++ 对象给 QML 暴露“可放多个 `T` 对象的属性”的桥梁。它不是容器，也不拥有元素；本质上是一组回调函数和一个 owner/data 指针。QML 引擎通过这些回调向列表追加、读取或清空对象。

最典型的需求是让 QML 以声明式子对象语法构造 C++ 对象树，而不是让调用者先创建 `QList<T *>` 再塞给 setter。

## 一个真实的声明式入口

下面的 `Chart` 把 `Slice` 列表暴露为只读属性。虽然 `slices` 没有 setter，QML 仍可在对象初始化时向它追加子项。

```cpp
class Chart : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QQmlListProperty<Slice> slices READ slices)

public:
    QQmlListProperty<Slice> slices()
    {
        return QQmlListProperty<Slice>(this, &m_slices);
    }

private:
    QList<Slice *> m_slices;
};
```

```qml
Chart {
    slices: [
        Slice { label: "Desktop" },
        Slice { label: "Mobile" }
    ]
}
```

`QQmlListProperty<Slice>(this, &m_slices)` 是优先选择：Qt 为 `QList<T *>` 提供了 append、count、at、clear、replace、removeLast 的完整实现。`Chart` 只保存指针；是否把 `Slice` 的 QObject 父对象设为 `Chart`、何时删除它们，仍是应用的所有权设计。

## 为什么通常不要写 setter

列表属性的目标是让 QML 引擎对“项目”操作。为 `Q_PROPERTY(QQmlListProperty<T> ...)` 再添加普通 setter，容易让赋值、追加与替换的语义相互冲突。惯用写法是只提供 `READ` getter，并让返回的 `QQmlListProperty` 决定可用操作。

最小契约是 `append`。`count`、`at`、`clear`、`replace` 和 `removeLast` 都可选，但少实现功能就意味着 QML 和 `QQmlListReference` 能做的事更少。Qt 能基于其它回调模拟一部分操作，例如通过 clear + append 模拟 replace；那会反复重建列表，性能和副作用都可能更差。

当底层不是 `QList<T *>` 时，使用回调构造函数，把 `data` 指向私有存储或拥有该存储的上下文：

```cpp
static void appendSlice(QQmlListProperty<Slice> *property, Slice *slice)
{
    auto *chart = static_cast<Chart *>(property->object);
    chart->addSlice(slice);
}
```

回调不得让 `property->object` 或 `property->data` 失效。它们在这份 list property 被引擎使用期间必须保持有效。

## QML 赋值策略不是小细节

当派生类型重新声明继承来的列表属性时，QML 的 `items: [...]` 到底是追加还是替换，需要显式设定类信息宏：

```cpp
class Chart : public QObject
{
    Q_OBJECT
    QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE
    Q_PROPERTY(QQmlListProperty<Slice> slices READ slices)
};
```

`APPEND` 保留已有列表并继续追加；`REPLACE` 先清空再接受新列表；`REPLACE_IF_NOT_DEFAULT` 在属性未被其声明处的默认值占用时替换。选择策略前先确认组件继承和默认子对象规则，否则很容易出现“基类的项为什么消失了”或“重复追加”的问题。

## 使用边界

- `T` 是 `QObject` 派生类型；该模板传递和返回的是 `T *`。
- list property 的复制只是复制回调和指针，不会深拷贝列表或对象。
- 若只实现 `append`，QML 可以构建列表，但 C++ 反射访问不一定能读取或整体修改它。
- 不要把短生命周期局部 `QList<T *>` 的地址交给构造函数；getter 返回后就会悬空。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlListProperty(QObject *, QList<T *> *)` | 用现成 `QList` 构建完整列表适配器 | 列表对象必须比 property 的使用期长 |
| 回调构造函数 | 为自定义存储提供操作能力 | `object`、`data` 与回调的组合必须长期有效 |
| `AppendFunction` | 向列表追加一个 `T *` | 所有列表属性都必须支持 append |
| `CountFunction` / `AtFunction` | 提供长度和按下标读取 | 缺少它们就不能可靠读取列表 |
| `ClearFunction` | 清空列表 | 不等于销毁对象；所有权由实现决定 |
| `ReplaceFunction` / `RemoveLastFunction` | 原生替换、尾删能力 | 缺失时 Qt 可能用其它回调模拟，代价更高 |
| `toList<List>()` | 从可读 property 拷贝元素指针到容器 | 需要 `count` 和 `at`；不转移所有权 |
| `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND` | QML 再赋值时追加 | 适合聚合式列表，可能产生重复项 |
| `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE` | QML 再赋值时替换列表 | 需要清空语义正确，注意基类默认项 |
| `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT` | 仅在非默认赋值情形替换 | 用于兼顾继承的默认内容与显式赋值 |

## 相关类型

- `QQmlListReference`：不依赖模板参数地检查和操作一个已暴露的列表属性。
- `Q_PROPERTY`：将 getter 返回的 `QQmlListProperty<T>` 注册为元对象属性。
- `QObject` 父子关系：常用于配合列表元素的生命周期，但并非 `QQmlListProperty` 自动完成。
