# QRangeModel::ItemAccess：为领域类型定义角色读写规则

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 所属头文件：`#include <QRangeModel>`  
> 所属类型：`QRangeModel` 的类模板定制点

`QRangeModel::ItemAccess<T>` 不是一个要实例化的运行时对象，而是 `QRangeModel` 查找的编译期定制点。它解决的问题是：当范围里的元素是自定义领域类型，且 Qt 默认的“简单值、关联容器、gadget、QObject”推断不符合业务角色模型时，怎样明确规定某个角色应读哪个字段、写哪个字段。

例如订单条目既要以 `DisplayRole` 显示标题，又要通过自定义角色读取金额、状态和内部 ID。把这些规则散落在代理或视图中，会让数据展示与编辑逻辑脱节；`ItemAccess` 让它们集中在领域类型的模型适配层。

## 基本形式

为你拥有的类型做全特化，并提供两个 `static` 成员：

```cpp
#include <QRangeModel>
#include <QVariant>

struct Task
{
    QString title;
    int priority = 0;
    bool done = false;
};

template <>
struct QRangeModel::ItemAccess<Task>
{
    static QVariant readRole(const Task &task, int role)
    {
        switch (role) {
        case Qt::DisplayRole:
            return task.title;
        case Qt::UserRole + 1:
            return task.priority;
        case Qt::UserRole + 2:
            return task.done;
        default:
            return {};
        }
    }

    static bool writeRole(Task &task, const QVariant &value, int role)
    {
        switch (role) {
        case Qt::EditRole:
        case Qt::DisplayRole:
            if (!value.canConvert<QString>())
                return false;
            task.title = value.toString();
            return true;
        case Qt::UserRole + 1:
            if (!value.canConvert<int>())
                return false;
            task.priority = value.toInt();
            return true;
        case Qt::UserRole + 2:
            if (!value.canConvert<bool>())
                return false;
            task.done = value.toBool();
            return true;
        default:
            return false;
        }
    }
};
```

随后把 `Task` 放进范围，再用 `QRangeModel` 构造模型。`data()`、`multiData()`、`setData()` 和相关批量角色操作会优先走这套规则。

## 它覆盖了什么，又没有覆盖什么

一旦 `ItemAccess<T>` 被识别，优先级高于 Qt 的默认推断。即使 `T` 本身是 gadget、`QObject`、关联容器，模型也会使用你的角色读写函数，而不是自动按属性或键查找。

被特化的类型会隐式视为 `QRangeModel::RowCategory::MultiRoleItem`。这意味着它在一维范围里被看作“一行、多个角色”的项目，而不是自动拆成多个列。

`ItemAccess` 只控制领域项的角色访问，不负责：

- 底层范围是否可变、能否插入或删除行；
- 模型的 `roleNames` 映射；
- QObject 的属性 NOTIFY 自动连接；
- 结构变化通知和跨线程同步。

这些仍分别由范围类型、`setRoleNames()`、`autoConnectPolicy`、模型 API 和对象线程归属决定。

## `readRole()` 的契约

`readRole(const T &, int)` 必须是可访问的静态函数，返回值可转换为 `QVariant`。对已支持角色返回一个有效 `QVariant`；对未知、无意义或暂不可用的角色返回默认构造的无效 `QVariant`。

读取函数应当是无副作用的、快速的。Qt 视图在布局、绘制、代理评估时可能多次读取相同角色；把网络访问、惰性写回或昂贵数据库查询塞进其中，会直接反映为滚动卡顿和不可预测的调用次数。

如果范围保存的是 `T *` 或智能指针，特化的仍是底层 `T`。模型会把实际项目作为 `T` 的引用交给你的静态函数；因此空指针与已销毁对象的生命周期仍要由范围设计解决。

## `writeRole()` 的契约

`writeRole(T &, const QVariant &, int)` 必须是可访问的静态函数，返回值可转换为 `bool`：

- 返回 `true`：值已成功写入目标项；
- 返回 `false`：不支持该角色、类型转换失败、值不满足业务约束，或项不可编辑。

成功写入后，`QRangeModel` 会按模型协议发出相应的数据变化通知。不要在 `writeRole()` 内再手动发 `dataChanged()`；该函数拿到的只是领域对象，不应反向操纵模型，也不应自行触发一次重复更新。

把 `QVariant` 转为业务类型前应检查转换能力和业务约束。`toInt()`、`toBool()` 等转换本身不等于输入有效，例如优先级的合法范围、状态迁移是否允许，仍要由特化代码明确判断。

## 与 `roleNames` 的配合

`ItemAccess` 按整数 role 决策；`roleNames` 则为 QML 和通用模型消费者提供“角色号到名字”的映射。两者必须保持一致：

```cpp
QHash<int, QByteArray> roles;
roles.insert(Qt::UserRole + 1, "priority");
roles.insert(Qt::UserRole + 2, "done");
model.setRoleNames(roles);
```

若 `readRole()` 支持了 `Qt::UserRole + 1`，却没有给 QML 可见的 `roleNames`，QML 端不会自然获得 `priority` 这个属性名。反过来，声明一个不存在的角色名会让读写落到无效 `QVariant` 或 `false`。

## 设计边界与常见错误

1. 为第三方类型特化 `ItemAccess`。全局特化会影响所有使用该类型的代码，升级库后也容易冲突；仅对自己拥有的领域类型特化。
2. 只实现 `readRole()`。检测到定制点需要读写函数都满足签名；只读模型应让 `writeRole()` 明确返回 `false`。
3. `readRole()` 返回看似正常的默认值来表示未知角色。应返回无效 `QVariant`，否则代理无法区分“字段确实为 0/空串”和“角色不支持”。
4. `writeRole()` 先部分修改再返回 `false`。失败应尽量不留下半完成状态，特别是一个角色映射多个字段时。
5. 在 `writeRole()` 中改变范围结构，例如插入或删除行。结构变更必须由模型 API 管理通知，不能藏在单项角色写入里。
6. 同时依赖元对象自动映射和 `ItemAccess`。特化一旦存在就优先，元对象属性规则不会再兜底。

## API 速查表

| API / 契约 | 作用 | 边界与注意事项 |
| --- | --- | --- |
| `template <> struct QRangeModel::ItemAccess<T>` | 为类型 `T` 定义角色访问规则。 | 这是全局编译期特化，只为自己拥有的类型提供。 |
| `static QVariant readRole(const T &item, int role)` | 读取 `item` 的指定角色。 | 必须返回可转换为 `QVariant` 的值；不支持角色返回无效 `QVariant`。 |
| `static bool writeRole(T &item, const QVariant &value, int role)` | 将角色值写入 `item`。 | 成功返回 `true`，转换失败、非法值或不支持角色返回 `false`。 |
| `Qt::DisplayRole` / `Qt::EditRole` | 常用显示与编辑角色。 | 是否把两者映射到同一字段由特化决定，应保持视图编辑预期一致。 |
| 自定义 `Qt::UserRole + n` | 表达领域角色，例如状态、优先级。 | 同时用 `setRoleNames()` 为 QML 和代理声明角色名。 |
| 隐式 `MultiRoleItem` 分类 | 让 `T` 被表示为一个带多个角色的项。 | 不会自动生成列，也不会自动连接 QObject 属性变化。 |
| `QRangeModel::data()` / `multiData()` | 模型读取路径会调用 `readRole()`。 | 读取可能高频发生，函数必须快速、无副作用。 |
| `QRangeModel::setData()` / `setItemData()` | 模型写入路径会调用 `writeRole()`。 | 不要在其中直接改模型结构或自行补发 `dataChanged()`。 |

## 一句话总结

`QRangeModel::ItemAccess<T>` 是把领域类型映射为 Qt 角色数据的精确入口：`readRole()` 负责无副作用地读，`writeRole()` 负责验证后写并明确成败；它替代默认推断，但不替代范围生命周期、角色命名或模型变更通知。
