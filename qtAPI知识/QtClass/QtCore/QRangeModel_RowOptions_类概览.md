# QRangeModel::RowOptions：指定自定义行应显示为列还是角色

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.10  
> 所属头文件：`#include <QRangeModel>`  
> 所属类型：`QRangeModel` 的类模板定制点

`QRangeModel::RowOptions<T>` 用于改变 `QRangeModel` 对范围元素类型 `T` 的默认表示方式。它解决的是“同一个领域对象究竟是一行中的多列，还是一个带多个 role 的项目”这个模型语义问题。

默认推断大多数时候已经足够，但在一维范围中，带元对象的 gadget 或 `QObject` 往往会被理解为多列行。若你要把它交给 `QListView` 或 QML 列表，并希望属性以 `title`、`color`、`toolTip` 等角色暴露，而不是被当成表格列，就用 `RowOptions` 明确选择 `MultiRoleItem`。

## 典型场景

以下类型含有多个可展示属性：

```cpp
class ColorEntry
{
    Q_GADGET
    Q_PROPERTY(QString display MEMBER colorName)
    Q_PROPERTY(QColor decoration READ decoration)
    Q_PROPERTY(QString toolTip READ toolTip)

public:
    QString colorName;

    QColor decoration() const;
    QString toolTip() const;
};
```

如果 `QList<ColorEntry>` 需要作为“每个元素一条列表项、属性作为角色”提供给 QML 或列表代理，特化为：

```cpp
template <>
struct QRangeModel::RowOptions<ColorEntry>
{
    static constexpr auto rowCategory =
        QRangeModel::RowCategory::MultiRoleItem;
};
```

现在 `ColorEntry` 会被作为多角色项处理，而不是默认拆成一行里的多个列。角色名仍由 `QRangeModel::roleNames()` 的默认元对象推断或 `setRoleNames()` 控制。

## 两种 `RowCategory` 的实际含义

| 分类 | 含义 | 适用情况 |
| --- | --- | --- |
| `Default` | 交给 `QRangeModel` 按范围与行类型推断。 | 简单值、嵌套行容器、tuple，或你接受默认 gadget 表示方式时。 |
| `MultiRoleItem` | 把带元对象的项当成一个多角色项目，即使在一维范围中也是如此。 | QML `ListView`、`QListView` 的富项目、以属性名读取多份数据的代理。 |

这只改变“行的表示分类”，不改变领域对象本身，也不自动让它可编辑。可写性仍取决于范围是否可变、属性是否可写、`setData()` 能否完成转换。

## `RowOptions` 与其他定制点的分工

- `RowOptions<T>`：决定默认把 `T` 看成什么类型的行；
- `ItemAccess<T>`：定义每个 role 实际怎样读写；
- `roleNames`：定义 role 整数在 QML/代理中的名字；
- `autoConnectPolicy`：当项为 `QObject` 时，决定何时把属性 NOTIFY 信号连接为 `dataChanged()`。

不要把 `RowOptions` 当作角色访问代码的入口。它没有 `readRole()` 或 `writeRole()`，不能在这里实现类型转换或校验；需要这种控制时使用 `ItemAccess<T>`。

## 使用边界

特化应在 `T` 的定义对当前编译单元可见之后写出，并放在所有会构造 `QRangeModel` 的翻译单元可见的头文件中。否则有的翻译单元会按默认分类实例化模型，有的会看到特化，导致行为不一致。

只为你拥有的类型特化。给第三方库类型做全局模板特化会使该类型在整个程序中的 `QRangeModel` 语义发生变化，升级依赖库时也可能出现冲突。

若 `T` 已经特化 `ItemAccess<T>`，Qt 会把它隐式视为多角色项；再写 `RowOptions<T>::rowCategory = MultiRoleItem` 通常是重复声明，没有额外收益。

## 常见错误

1. 希望 QML 按属性名访问 gadget，却忘记设为 `MultiRoleItem`，结果模型呈现为多列行。
2. 只特化 `RowOptions`，却期待自定义角色读写逻辑。它只分类，不定义访问规则。
3. 把 `MultiRoleItem` 用在需要表格多列的编辑器中，结果列语义与视图预期不一致。
4. 在一个 `.cpp` 中私有地定义特化，而其他地方已经构造模型。模板定制必须在实例化点可见。
5. 为不属于自己的类型提供特化，导致项目其他模块得到意外模型行为。

## API 速查表

| API / 契约 | 作用 | 边界与注意事项 |
| --- | --- | --- |
| `template <> struct QRangeModel::RowOptions<T>` | 为行类型 `T` 覆盖表示分类。 | 编译期全局特化，应在构造模型前可见。 |
| `static constexpr RowCategory rowCategory` | 指定 `T` 的行分类。 | 必须是公开的编译期常量。 |
| `RowCategory::Default` | 使用 Qt 默认推断。 | 默认行为取决于 `T` 是简单值、范围、tuple、gadget 或 QObject。 |
| `RowCategory::MultiRoleItem` | 将元对象项表示为多角色项目。 | 适合一维列表中的属性 role，不等同于自定义角色读写。 |
| `QRangeModel::roleNames()` | 为多角色项公开角色名。 | 默认从元对象属性推断；可由 `setRoleNames()` 覆盖。 |
| `QRangeModel::ItemAccess<T>` | 定义真实的角色读写。 | 需要改变 role 映射或验证时用它，而非 `RowOptions`。 |

## 一句话总结

`QRangeModel::RowOptions<T>` 只回答“`T` 应如何呈现为一行”：想让一维范围中的 gadget 或 `QObject` 成为可按属性名访问的列表项目，就将 `rowCategory` 设为 `MultiRoleItem`；真实读写规则交给 `ItemAccess`。
