# QRangeModel：把现有 C++ 范围接入 Qt 模型视图，而不手写模型骨架

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.10  
> 头文件：`#include <QRangeModel>`  
> 模块：`Qt6::Core`  
> 基类：`QAbstractItemModel`

`QRangeModel` 是一个把现有 C++ 范围映射为 `QAbstractItemModel` 的通用模型。它解决的核心问题是：程序里已经有 `std::vector`、`std::array`、`QList`、嵌套容器或树形领域数据时，怎样让 `QListView`、`QTableView`、Qt Quick 视图使用它们，而不为每种容器重复实现索引、角色、编辑和结构变更通知。

它不是“给容器加一个只读显示层”。范围是否由模型拥有、是否可写、能否增删行列、元素如何映射为列或角色，都由传入范围的类型、传递方式和定制点共同决定。

## 最小使用：先决定范围的所有权

```cpp
#include <QRangeModel>
#include <QListView>
#include <vector>

std::vector<int> numbers = {1, 2, 3, 4, 5};

QRangeModel model(&numbers);  // 模型操作会作用于 numbers
QListView view;
view.setModel(&model);
```

范围至少要能通过 `std::begin()` / `std::end()` 遍历，迭代器需满足 `std::forward_iterator`。提供 `std::size()` 和随机访问迭代器会让部分模型操作更高效。

### 按值、引用和指针不是小差别

| 构造方式 | 模型持有/操作的对象 | 修改模型是否改原容器 |
| --- | --- | --- |
| `QRangeModel model(numbers)` | `numbers` 的副本 | 否 |
| `QRangeModel model(&numbers)` | 外部 `numbers` | 是 |
| `QRangeModel model(std::ref(numbers))` | 外部 `numbers` | 是 |
| `QRangeModel model(sharedPtr)` | 由智能指针共同持有的范围 | 取决于传入智能指针所指对象，但生命周期更易管理 |

传指针或引用包装器时，调用方必须保证底层范围活得比模型久。把模型交给视图以后，**不能再直接修改该范围**。视图不知道外部改动，结构变化尤其可能破坏模型维护的 `QPersistentModelIndex`。要在模型之外安全操作同一范围，使用 `QRangeModelAdapter`，让它负责同步模型通知。

## 范围会被表示成列表、表格还是树

`QRangeModel` 把外层范围元素视为“行”：

- 行是简单值时，通常表现为单列表；
- 行本身是范围或实现 C++ tuple 协议时，通常表现为多列表；
- 行是带元对象的 `Q_GADGET` 或 `QObject` 时，属性可成为列或角色；
- 树形范围需要第二个构造函数传入遍历协议，协议负责说明子节点范围和父子关系。

固定大小行类型，例如 `std::array`、`std::tuple`、结构体，能显示和编辑可写字段，但不能插入或删除列。固定大小外层范围也不能插入或删除行。不要因为 `insertRows()` 出现在 `QAbstractItemModel` 接口中，就假定它对任何范围都可用。

## 写入与结构变更的真实条件

对 const 范围、总是产生 const 值的范围，或者缺少所需容器操作的范围，写 API 会直接失败并返回 `false`。

- 改单元格通常要求可变迭代器以及能给目标赋值；
- 插入行要求外层范围可动态扩容并提供相应 `insert(...)`；
- 删除行要求外层范围提供 `erase(const_iterator, size_t)`；
- 插入或删除列要求每一行都是可动态调整的行容器，并提供相应 `insert` / `erase`；
- 树模型不能通过默认实现插入、删除列。

例如 `std::array<int, 5>` 可通过 `setData()` 改值，但 `insertRows()` 必然失败；把它声明为 `const` 后连改值也会失败。

## 数据角色、属性和 `roleNames`

普通值的 `Qt::DisplayRole` 与 `Qt::EditRole` 会映射到该值。关联容器若以 `int`、`Qt::ItemDataRole` 或 `QString` 映射到 `QVariant`，其键值可以成为多角色数据。

当行或项为 `Q_GADGET` / `QObject` 且类型一致时，默认 `roleNames` 会把元对象属性名映射到从 `Qt::UserRole` 开始的角色，并提供 `modelData` 访问该 gadget 或对象实例。显式调用 `setRoleNames(nonEmptyMap)` 会覆盖这个推断；传空映射或调用 `resetRoleNames()` 恢复默认推断。

```cpp
QHash<int, QByteArray> roles;
roles.insert(Qt::UserRole + 1, "title");
roles.insert(Qt::UserRole + 2, "priority");
model.setRoleNames(roles);
```

对 gadget 或 `QObject`，`setData()` 按 `roleNames` 找属性并执行类型转换。找不到属性、值不能转换、范围只读时返回 `false`。`setItemData()` 写入多个角色时，对可复制的相关项采用事务语义：只要有一个角色写失败，原项目不会被部分更新。

不要在子类中随意重写 `roleNames()`。Qt 明确指出这可能破坏 `roleNames` 属性的行为；优先使用 `setRoleNames()`。

## QObject 属性变化的自动通知

`autoConnectPolicy` 自 Qt 6.11 引入，用于把底层 `QObject` 属性的 NOTIFY 信号自动连接到模型的 `dataChanged()`。它只连接与角色名匹配的属性；对“QObject 行”则按列连接到 `Qt::DisplayRole`。

| 策略 | 行为 | 代价与适用性 |
| --- | --- | --- |
| `None` | 不自动连接，默认值。 | 适合手动发模型通知或底层不是 QObject 的场景。 |
| `Full` | 立即连接所有相关 QObject 属性，后来新插入的行列也会连接。 | 更新覆盖完整，但大量对象和属性会消耗大量连接内存。 |
| `OnRead` | 首次读到某属性时才建立连接。 | 首屏成本低，但滚动浏览会持续增加连接和记账内存。 |

改变该属性会断开已有自动连接并按新策略重建。若你直接把范围中的一个 `QObject *` 换成另一个对象，模型不会自动为这次替换拆建连接；应通过模型 API 更新，或显式重设策略/模型。

`Q_GADGET` 没有信号机制，不能从 `autoConnectPolicy` 获益。对普通 C++ 值，直接经模型 API 写入时，模型本身会发出必要的数据变化通知。

## 定制点与扩展边界

- `QRangeModel::RowOptions<T>`：改变类型 `T` 被视为普通行还是多角色项；
- `QRangeModel::ItemAccess<T>`：完全接管单个 `T` 的角色读写；
- 树形构造函数的 `Protocol`：定义树的子范围与导航方式。

`ItemAccess` 特化优先于 Qt 的预定义推断，并会把该类型隐式视为 `MultiRoleItem`。只为你拥有的类型特化它；为第三方类型写全局模板特化会污染程序的类型行为。

## 生命周期、线程与二进制兼容性

`QRangeModel` 是 `QObject`，不可复制、不可移动。作为 `QAbstractItemModel`，模型、附着的视图和对模型的修改应放在对象所属线程；从工作线程获得新数据时，用排队信号把修改切回模型线程。类文档标注“可重入”只说明不同实例可并发使用，不等于同一模型实例可跨线程随意读写。

类本身不是模板，因此以指针或引用传过库边界、或作为库公开类的值成员是二进制安全的。但构造函数是内联模板，会为范围类型实例化实现。不要在库的内联公开 API 中调用该构造函数，否则使用不同 Qt 版本编译库与应用时可能造成 ODR 或二进制兼容问题。

## 常见错误

1. 写 `QRangeModel model(items)` 后以为编辑会改 `items`。按值构造的是副本，应传 `&items` 或 `std::ref(items)`。
2. 模型已被视图使用，却直接 `items.push_back(...)`。视图和持久索引不会收到正确通知，应经模型 API 或 `QRangeModelAdapter` 修改。
3. 用 `std::array` 期待动态增删。它可修改元素，但行数固定。
4. 开启 `Full` 处理数万 QObject，忽略连接内存；或长期滚动列表时忽略 `OnRead` 的连接累积。
5. 修改了底层 QObject 指针却期待自动连接更新。策略不会跟踪直接替换。
6. 用未知角色写简单值。简单值默认只支持 `DisplayRole` / `EditRole`。
7. 在库的 inline 头文件中构造模型。模板实现会把 Qt 版本细节带进 ABI 边界。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QRangeModel(Range &&range, QObject *parent)` | 从列表或表格范围构造模型。 | 按值复制，指针/引用包装器引用外部范围；外部范围寿命必须覆盖模型。 |
| `QRangeModel(Range &&range, Protocol &&protocol, QObject *parent)` | 从树范围和遍历协议构造。 | `Protocol` 决定子范围与父子导航；仅在树模型需要时使用。 |
| `~QRangeModel()` | 销毁模型及内部适配实现。 | 不自动延长裸指针范围的寿命。 |
| `RowOptions<T>` | 行表示方式的模板定制点。 | 通过特化的 `rowCategory` 覆盖默认推断。 |
| `ItemAccess<T>` | 单项角色读写的模板定制点。 | 特化必须提供静态 `readRole` / `writeRole`；只特化自有类型。 |
| `RowCategory::Default` | 让 Qt 按类型推断行表示。 | gadget 在一维范围中默认可能被视为多列行。 |
| `RowCategory::MultiRoleItem` | 把带元对象的项表示为多角色项。 | 即使位于一维范围中也按角色而非多列展示。 |
| `AutoConnectPolicy::None` | 不自动接 QObject 属性通知。 | 默认值；需要自己保持数据变化通知一致。 |
| `AutoConnectPolicy::Full` | 连接所有相关 QObject 属性通知。 | 覆盖完整，但大量连接消耗内存。 |
| `AutoConnectPolicy::OnRead` | 首次读属性时才连接通知。 | 节省初始成本，但浏览更多项会增长连接记录。 |
| `autoConnectPolicy()` | 读取当前自动连接策略。 | 仅影响 QObject 属性且角色名匹配的场景。 |
| `setAutoConnectPolicy(policy)` | 更换自动连接策略。 | 会断开现有连接；直接替换范围中的 QObject 不会被跟踪。 |
| `autoConnectPolicyChanged(policy)` | 自动连接策略变更信号。 | Qt 6.11 起可用。 |
| `roleNames()` | 返回角色号到名称的映射。 | 可重写但可能破坏属性行为，优先使用 setter。 |
| `setRoleNames(names)` | 显式覆盖默认角色映射。 | 非空映射覆盖元对象推断，也决定属性角色映射。 |
| `resetRoleNames()` | 恢复默认角色映射。 | 等价于把角色映射恢复为空的默认推断状态。 |
| `roleNamesChanged()` | 角色映射变化信号。 | QML 或代理依赖角色名时需要重新评估绑定。 |
| `index(row, column, parent)` | 创建模型索引。 | 列表/表格的 parent 通常无效；树模型由协议决定。 |
| `parent(child)` | 返回父索引。 | 列表和表格模型始终返回无效索引；树模型使用协议。 |
| `sibling(row, column, index)` | 快速取得同父的另一个单元格索引。 | 目标不存在时返回无效索引。 |
| `rowCount(parent)` | 返回 parent 下的行数。 | 根范围对应无效 parent；列表/表格的有效 parent 通常为 0 行。 |
| `columnCount(parent)` | 返回列数。 | 简单值通常为 1；嵌套范围、tuple、元对象行可为多列。 |
| `hasChildren(parent)` | 查询是否有子项。 | 列表/表格没有树子项，树模型依协议判断。 |
| `data(index, role)` | 读取角色数据。 | 简单值通常仅支持 `DisplayRole` / `EditRole`；无效索引或未知角色返回无效值。 |
| `multiData(index, roles)` | 一次读取多个角色。 | 供高效批量角色请求使用；角色语义同 `data()`。 |
| `itemData(index)` | 读取一项的多个预定义角色。 | 关联容器、gadget、QObject 会按其角色机制导出数据。 |
| `setData(index, value, role)` | 写一个角色数据。 | 只读范围、未知角色、属性不存在或转换失败时返回 `false`。 |
| `setItemData(index, values)` | 批量写角色数据。 | 相关可复制项具事务语义，失败不会留下部分写入。 |
| `clearItemData(index)` | 清除项角色数据。 | 能否清除取决于项类型和可写能力。 |
| `flags(index)` | 返回可选、可编辑、可拖放等标志。 | 只读范围会去掉编辑能力。 |
| `headerData(section, orientation, role)` | 读取表头数据。 | 取决于模型所表示的行/列结构。 |
| `setHeaderData(section, orientation, value, role)` | 尝试写表头数据。 | 并非所有范围类型都有可写表头，检查返回值。 |
| `insertRows(row, count, parent)` | 在指定处插入空行。 | 外层范围必须可变、动态大小且支持 `insert`。 |
| `removeRows(row, count, parent)` | 删除行。 | 外层范围须支持 `erase`；固定或只读范围直接失败。 |
| `moveRows(sourceParent, sourceRow, count, destParent, destRow)` | 移动连续行。 | 受范围与树协议能力限制，检查 `bool` 结果。 |
| `insertColumns(column, count, parent)` | 在每一行插入空列。 | 行类型必须动态可变且支持 `insert`；树模型不支持默认列插入。 |
| `removeColumns(column, count, parent)` | 从每一行删除列。 | 行类型必须支持 `erase`；tuple、array、struct 等固定列失败。 |
| `moveColumns(sourceParent, sourceColumn, count, destParent, destColumn)` | 移动连续列。 | 受行容器能力限制，检查返回值。 |
| `canFetchMore(parent)` / `fetchMore(parent)` | 供视图的延迟加载协作。 | 不是把普通范围自动变成异步数据源的接口。 |
| `buddy(index)` | 为编辑操作返回关联索引。 | 通常由视图框架调用。 |
| `match(start, role, value, hits, flags)` | 查找匹配的模型项。 | 在大范围中可能是线性成本，勿在热路径反复全表搜索。 |
| `sort(column, order)` | 请求按列排序。 | 是否能改变底层范围及排序含义由范围类型决定。 |
| `mimeTypes()` / `mimeData(indexes)` | 导出拖拽 MIME 数据。 | 由模型的拖放实现与项类型决定。 |
| `canDropMimeData(...)` / `dropMimeData(...)` | 预检和执行放置操作。 | 不要绕过模型直接改范围；检查返回值。 |
| `supportedDragActions()` / `supportedDropActions()` | 声明支持的拖放动作。 | 仅声明能力，不代表底层范围必然能完成每种操作。 |
| `span(index)` | 返回视图单元格跨行跨列尺寸。 | 多数普通模型不使用跨格；主要供视图查询。 |
| `event(event)` / `eventFilter(object, event)` | 处理模型内部 QObject 事件与过滤。 | 受保护实现细节，不是外部数据同步入口。 |
| `resetInternalData()` | 模型 reset 后清理内部缓存。 | 受保护槽；供模型生命周期调用，外部不应把它当公开刷新 API。 |

## 一句话总结

`QRangeModel` 让已有 C++ 范围成为真正的 Qt 模型，但它不会替你解决所有权、外部直接修改和 QObject 通知问题：先决定范围传递方式，再把一切修改经由模型或 `QRangeModelAdapter`，最后按数据规模谨慎选择自动连接策略。
