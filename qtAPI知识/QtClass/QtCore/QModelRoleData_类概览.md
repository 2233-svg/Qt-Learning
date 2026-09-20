# Qt QModelRoleData 角色数据槽位笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QModelRoleData>`  
> 所属模块：`Qt6::Core`  
> 类型性质：为一个模型 role 保存角色编号和待填充的 `QVariant`  
> 相关类型：`QModelIndex`、`QModelRoleDataSpan`、`QAbstractItemModel::multiData()`

## 1. 它解决什么问题

`QModelRoleData` 是 Qt 6 的多角色读取协议中的一个槽位。它把两件事放在一起：

```text
role 编号
  +
模型要填入的 QVariant 数据
```

`QModelIndex::multiData()` 或 `QAbstractItemModel::multiData()` 接收一组 `QModelRoleData`，模型根据每个槽位的 `role()` 把结果写入对应的 `data()`：

```text
调用方准备 role 槽位
        |
        v
index.multiData(span)
        |
        v
模型按 role 填充每个槽位的 QVariant
```

它主要解决：

- 一次读取 Display、Decoration、CheckState 等多个 role；
- 让模型实现有机会批量完成节点查找和数据准备；
- 避免调用方为每个 role 单独组织一套临时变量；
- 让 `QModelIndex`、视图和代理模型共享明确的 role/value 存储协议。

`QModelRoleData` 不是模型中的永久字段，也不是一个自动连接到模型的数据绑定。它只是一次 `multiData()` 调用期间由调用方提供给模型填写的可写槽位。

## 2. 它不是什么

`QModelRoleData` 不是：

- 模型内部某个 role 的永久缓存；
- `QPair<int, QVariant>` 的完全等价替代品；
- 自动向模型请求数据的对象；
- role 的元数据描述器；
- 保证 `data()` 一定非空的结果对象；
- 只读 value。

构造时只设置 role 编号，`QVariant` 默认为空。只有模型的 `multiData()` 实现真正填充后，`data()` 才代表本次请求得到的结果。

## 3. 最小使用场景

### 3.1 准备多个 role

```cpp
#include <QModelIndex>
#include <QModelRoleData>

QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::DecorationRole),
    QModelRoleData(Qt::CheckStateRole)
};

index.multiData(roles);

const QVariant display = roles[0].data();
const QVariant decoration = roles[1].data();
const QVariant checkState = roles[2].data();
```

数组元素的 role 编号决定模型填充什么，数组下标只是调用方自己的组织方式。不要假设 `roles[0]` 一定是 DisplayRole，除非你自己这样初始化。

### 3.2 模型实现批量填充

自定义模型可以重写：

```cpp
void MyModel::multiData(const QModelIndex &index,
                        QModelRoleDataSpan span) const
{
    const Node *node = nodeFromIndex(index);
    for (QModelRoleData &roleData : span) {
        switch (roleData.role()) {
        case Qt::DisplayRole:
            roleData.setData(node->text());
            break;
        case Qt::UserRole + 1:
            roleData.setData(node->id());
            break;
        default:
            roleData.clearData();
            break;
        }
    }
}
```

模型必须按 role 编号解释槽位，并把结果写入同一个槽位。不要把一个 role 的结果写到另一个数组位置。

## 4. 构造后的状态

```cpp
QModelRoleData display(Qt::DisplayRole);
```

构造函数：

- 保存 `Qt::DisplayRole`；
- 默认构造内部 `QVariant`；
- 不访问模型；
- 不检查 role 是否被模型支持。

因此：

```cpp
QModelRoleData role(Qt::DisplayRole);
Q_ASSERT(role.role() == Qt::DisplayRole);
Q_ASSERT(!role.data().isValid());
```

“当前 data 无效”只说明槽位尚未被填充，不能说明模型一定没有该 role。

## 5. role 编号和 data 的关系

### 5.1 `role()` 是不可变查询

```cpp
const int requestedRole = roleData.role();
```

`QModelRoleData` 没有公开的 `setRole()`。一个槽位构造后，role 编号保持不变；如果要请求另一个 role，应构造新的 `QModelRoleData`。

### 5.2 `data()` 是可写结果槽

```cpp
QVariant &result = roleData.data();
result = QStringLiteral("ready");
```

模型可以通过 `data()` 返回的非 const 引用写入任意 `QVariant`，也可以使用 `setData()`。调用方在 `multiData()` 返回后通过 const 或非 const overload 读取/修改结果。

### 5.3 不要用 data 的状态推断 role 是否支持

以下几种情况都可能得到无效 `QVariant`：

- 模型不实现该 role；
- 模型明确返回空 QVariant；
- 模型在 `multiData()` 中调用 `clearData()`；
- 调用方还没有调用 `multiData()`；
- 自定义模型没有正确填写槽位。

role 是否有意义应由模型的 role 协议决定。若模型需要区分“没有值”和“合法空值”，应使用明确的业务约定。

## 6. 逐项 API 语义

### 6.1 `QModelRoleData(int role)`

```cpp
explicit QModelRoleData(int role) noexcept;
```

创建一个指定 role 的数据槽位。构造函数是 `explicit`，避免整数意外隐式转换成角色槽位：

```cpp
QModelRoleData display(Qt::DisplayRole);
```

它只记录 role，不调用模型、不分配模型资源，也不保证 `role` 是 Qt 预定义或自定义的合法业务值。

### 6.2 `role() const`

```cpp
constexpr int role() const noexcept;
```

返回构造时保存的 role 编号。它是模型在 `multiData()` 中分派数据的关键：

```cpp
switch (roleData.role()) {
case Qt::DisplayRole:
    roleData.setData(text);
    break;
}
```

该函数不改变槽位，也不会查询模型。

### 6.3 `data()`

```cpp
constexpr QVariant &data() noexcept;
```

返回可写的内部 `QVariant`：

```cpp
roleData.data() = QStringLiteral("hello");
```

模型实现通常可以直接写入，也可以通过 `setData()` 使用类型推导。返回引用只在当前 `QModelRoleData` 对象仍存活时有效。

### 6.4 `data() const`

```cpp
constexpr const QVariant &data() const noexcept;
```

返回只读的内部 `QVariant`：

```cpp
const QModelRoleData &roleData = roles[0];
const QVariant result = roleData.data();
```

它不会复制数据，返回的引用依赖 `QModelRoleData` 对象生命周期。需要长期保存时复制 `QVariant`。

### 6.5 `setData(T &&value)`

```cpp
template <typename T>
constexpr void setData(T &&value)
    noexcept(noexcept(m_data.setValue(std::forward<T>(value))));
```

把任意适合 `QVariant::setValue()` 的值写入当前槽位：

```cpp
roleData.setData(QStringLiteral("ready"));
roleData.setData(42);
roleData.setData(QColor(Qt::red));
```

关键语义：

- role 编号不变，只替换 data；
- 具体存储类型由 `QVariant::setValue()` 决定；
- `T` 必须满足 QVariant 的值存储要求；
- 函数的 `noexcept` 取决于底层 `QVariant::setValue()` 对该类型的行为；
- 它不做 role 合法性检查，也不通知模型。

如果写入 `QVariant` 本身：

```cpp
QVariant value = QStringLiteral("ready");
roleData.setData(value);
```

最终 data 仍是一个 `QVariant` 值，具体是否产生嵌套包装由 `QVariant` 的 setValue 规则决定；普通模型代码按目标数据类型直接传值即可。

### 6.6 `clearData()`

```cpp
void clearData() noexcept;
```

清空内部 `QVariant`，但不改变 role：

```cpp
roleData.clearData();
Q_ASSERT(roleData.role() == Qt::DisplayRole);
Q_ASSERT(!roleData.data().isValid());
```

常见用途：

- 模型不支持该 role；
- 本次请求不应返回旧数据；
- 复用一个 role 数组前清理上一轮结果；
- 在模型实现中显式表达“没有结果”。

它不会把 role 改成无效，也不会从 span 中删除槽位。

## 7. 模型实现的责任边界

### 7.1 按 role 填写对应槽位

一个模型实现通常写成：

```cpp
void MyModel::multiData(const QModelIndex &index,
                        QModelRoleDataSpan roleDataSpan) const
{
    if (!checkIndex(index))
        return;

    for (QModelRoleData &roleData : roleDataSpan) {
        switch (roleData.role()) {
        case Qt::DisplayRole:
            roleData.setData(dataForDisplay(index));
            break;
        case Qt::EditRole:
            roleData.setData(dataForEdit(index));
            break;
        default:
            roleData.clearData();
            break;
        }
    }
}
```

模型不要假设 span 中 role 的顺序，也不要只处理固定数组下标。

### 7.2 不要把旧值误当成模型结果

调用方可能复用 role 槽位：

```cpp
roles[0].setData(QStringLiteral("old"));
index.multiData(roles);
```

如果模型对未知 role 什么也不做，旧值可能残留。模型实现应对未处理 role 明确调用 `clearData()`；调用方在复用前也可以先清空全部槽位。

### 7.3 默认 `QAbstractItemModel::multiData()` 的性能预期

如果模型没有重写 `multiData()`，基类通常可以逐个调用 `data(index, role)` 填写槽位。自定义模型只有在能减少重复查找或批量构造数据时，才值得重写优化。

`QModelRoleData` 自己不提供性能优化；它只是让批量接口有统一可写存储。

## 8. 生命周期、引用和线程边界

### 8.1 data 引用不拥有结果

```cpp
QVariant &result = roleData.data();
```

这个引用只依附于 `roleData` 对象。不能返回引用、保存到异步任务，或在 `roleData` 销毁后继续使用。

### 8.2 角色槽位通常由调用方栈或容器拥有

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::EditRole)
};
index.multiData(roles);
```

模型只在调用期间使用它们。`QModelRoleData` 不持有模型，也不管理 span。

### 8.3 不提供线程同步

`QModelRoleData` 是普通值对象，但 `multiData()` 的模型访问仍受模型线程归属限制。把 role 槽位放到另一个线程，不会使跨线程调用模型变安全。

## 9. 常见错误

### 9.1 把 `QModelRoleData` 当成已经查询过的结果

**问题：** 构造后直接读取 `data()`，认为它包含模型数据。

**原因：** 构造函数只保存 role，默认 data 为空。

**处理：** 先通过 `index.multiData()` 或模型的 `multiData()` 填充。

### 9.2 试图修改 role 编号

**问题：** 想复用一个槽位，把 DisplayRole 改成 EditRole。

**原因：** 类没有公开 `setRole()`。

**处理：** 构造新的 `QModelRoleData(EditRole)`，或者重新建立数组。

### 9.3 用数组下标代替 role()

**问题：** 模型把 `span[0]` 永远当成 DisplayRole。

**原因：** 调用方可以按任意顺序准备 role。

**处理：** 始终使用 `roleData.role()` 分派。

### 9.4 未知 role 不清理旧值

**问题：** 模型复用槽位后，未支持 role 读到上一轮数据。

**原因：** `QModelRoleData` 的 data 不会因每次调用自动清空。

**处理：** 模型对未处理 role 调用 `clearData()`；调用方复用数组前也可清空。

### 9.5 从 data() 保存长期引用

**问题：** `QModelRoleData` 销毁或重新赋值后继续使用 `QVariant &`。

**原因：** data 返回的是成员引用。

**处理：** 需要延长生命周期时复制 `QVariant`。

### 9.6 误以为 setData 会通知模型

**问题：** 直接修改 role 槽位后期待模型或视图刷新。

**原因：** `setData()` 只改变这个槽位，不调用模型的 `setData()`，也不发信号。

**处理：** 修改模型数据应调用模型的编辑 API，并按模型协议发出 dataChanged。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QModelRoleData(int role)` | 创建指定 role 的结果槽位 | 只记录 role；data 初始为空；不访问模型 |
| `role() const` | 返回 role 编号 | 没有 setter；模型分派必须使用它 |
| `data()` | 返回可写 QVariant 槽位 | 引用依赖当前对象；写入不通知模型 |
| `data() const` | 返回只读 QVariant 槽位 | 引用不拥有数据；长期保存请复制 |
| `setData(T &&value)` | 用 QVariant setValue 规则写入结果 | `T` 必须可存入 QVariant；不改变 role |
| `clearData()` | 清空结果并保留 role | 适合未支持 role 或复用槽位前清理 |

## 11. 一句话总结

`QModelRoleData` 是一次 `multiData()` 请求中的“role + 可写 QVariant 槽位”：构造只设置 role，模型按 `role()` 把结果写入 `data()`，未知 role 应明确清空。它不主动访问模型、不拥有结果，也不会因为 `setData()` 而通知视图；真正的模型修改仍要走模型编辑 API。
