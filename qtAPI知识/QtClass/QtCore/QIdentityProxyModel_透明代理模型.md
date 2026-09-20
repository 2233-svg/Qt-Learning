# Qt QIdentityProxyModel 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QIdentityProxyModel>`  
> 所属模块：`Qt6::Core`  
> 继承：`QAbstractProxyModel -> QIdentityProxyModel`  
> 定位：保持源模型结构不变的透明代理模型

## 1. 它解决什么问题

`QIdentityProxyModel` 把一个源模型包装成另一个模型，但不改变源模型的行列结构、父子关系、排序结果或过滤结果。

可以把它理解成模型/视图体系中的“同构适配层”：

```text
source model
    │
    │ 结构、索引位置、选择范围保持对应
    ▼
QIdentityProxyModel
    │
    │ 可以在 data()、itemData() 等位置追加或改写表现
    ▼
view / selection model / delegate
```

它的价值不在于重新组织数据，而在于把“数据结构”和“数据表现”拆开。例如：

- 源模型提供 `QDateTime`，代理模型把 `Qt::DisplayRole` 改成指定格式的字符串；
- 源模型来自第三方库，不能修改源代码，但界面需要补充字体、背景色、工具提示或显示文本；
- 多个页面需要相同的展示规则，可以把展示逻辑封装成可复用代理；
- 需要在不影响源模型的情况下，把某个角色转换成视图更容易使用的值。

它不适合解决以下问题：

- 按条件隐藏或过滤行；
- 按列或角色排序；
- 把行列转置；
- 把多个源模型合并；
- 把树压平为列表，或改变父子层级；
- 为同一代理项拼接多个源项。

这些需求应优先考虑 `QSortFilterProxyModel`、`QTransposeProxyModel`，或者根据拓扑需求实现专用代理。

## 2. 先区分三个概念：源模型、代理模型、模型索引

### 2.1 源模型和代理模型是两个不同对象

```cpp
auto *source = new MyModel(this);
auto *proxy = new QIdentityProxyModel(this);

proxy->setSourceModel(source);
view->setModel(proxy);
```

视图看到的是 `proxy`，实际数据通常仍由 `source` 提供。代理模型默认不拥有源模型，也不会因为调用 `setSourceModel()` 就把源模型改成自己的子对象。

建议让两者具有清晰的共同生命周期，例如都挂在同一个控制对象下面：

```cpp
auto *source = new MyModel(controller);
auto *proxy = new QIdentityProxyModel(controller);
proxy->setSourceModel(source);
```

如果源模型被销毁，`QAbstractProxyModel` 会解除源模型关系，代理模型按空模型处理。此时行数通常为零，之前拿到的代理索引也不能继续使用。

### 2.2 代理索引不是源索引

即使行号和列号相同，下面两个索引仍属于不同模型：

```cpp
QModelIndex proxyIndex = proxy->index(2, 1);
QModelIndex sourceIndex = proxy->mapToSource(proxyIndex);

Q_ASSERT(proxyIndex.model() == proxy);
Q_ASSERT(sourceIndex.model() == source);
```

不能把 `sourceIndex` 直接传给代理模型的 `data()`、`setData()`、`parent()` 或视图，也不能把 `proxyIndex` 直接传给源模型。正确做法是显式调用：

```cpp
QModelIndex sourceIndex = proxy->mapToSource(proxyIndex);
QModelIndex proxyIndex = proxy->mapFromSource(sourceIndex);
```

### 2.3 “identity”指位置对应，不指对象复用

对于有效项，代理模型通常保留：

- 相同的 `row()`；
- 相同的 `column()`；
- 相同的父子层级；
- 相同的源模型内部指针映射；
- 相同的角色值，除非派生类重写了数据函数。

但是 `QModelIndex::model()` 必然不同。代理索引仍然是代理模型创建的索引，不能把“行列相同”误认为“索引可以互换”。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)

target_link_libraries(mytarget
    PRIVATE
        Qt6::Core
)
```

### 3.2 qmake

```qmake
QT += core
```

### 3.3 头文件

```cpp
#include <QIdentityProxyModel>
```

头文件中有 `QT_REQUIRE_CONFIG(identityproxymodel)`。如果使用裁剪过的 Qt 构建，需确认该功能没有被关闭。

## 4. 最小可用流程

下面的例子把 `QStandardItemModel` 放进透明代理，再交给视图使用：

```cpp
#include <QIdentityProxyModel>
#include <QStandardItemModel>
#include <QTableView>

auto *source = new QStandardItemModel(10, 3, parent);
auto *proxy = new QIdentityProxyModel(parent);

proxy->setSourceModel(source);
tableView->setModel(proxy);
```

此时：

- `proxy->rowCount()` 与源模型根节点的行数对应；
- `proxy->columnCount()` 与源模型根节点的列数对应；
- `proxy->index(row, column)` 对应源模型同一位置；
- 默认的 `data()`、`setData()`、`flags()`、拖放和编辑操作会沿映射转发；
- 源模型插入、删除、移动、重置等变化会被代理模型转成自己的模型变化通知。

如果只使用透明结构而不改写数据，通常不需要继承 `QIdentityProxyModel`。

## 5. 最常见的派生方式：只改表现，不改结构

Qt 文档中的典型用法是改写 `data()`，同时改写 `itemData()`，保证单角色读取和批量角色读取得到一致结果：

```cpp
#include <QDateTime>
#include <QIdentityProxyModel>
#include <QMap>
#include <QVariant>

class DateFormatProxyModel final : public QIdentityProxyModel
{
public:
    using QIdentityProxyModel::QIdentityProxyModel;

    void setDateFormatString(const QString &format)
    {
        if (m_format == format)
            return;

        m_format = format;

        // 通用树模型很难用一个简单范围精确覆盖所有受影响项。
        // reset 能保证视图重新查询所有数据，但代价比精确 dataChanged 更高。
        beginResetModel();
        endResetModel();
    }

    QVariant data(const QModelIndex &proxyIndex,
                  int role = Qt::DisplayRole) const override
    {
        if (role != Qt::DisplayRole || !proxyIndex.isValid())
            return QIdentityProxyModel::data(proxyIndex, role);

        const QModelIndex sourceIndex = mapToSource(proxyIndex);
        const QVariant raw = sourceModel()->data(sourceIndex, SourceClass::DateRole);
        const QDateTime dateTime = raw.toDateTime();
        if (!dateTime.isValid())
            return QIdentityProxyModel::data(proxyIndex, role);

        return dateTime.toString(m_format);
    }

    QMap<int, QVariant> itemData(const QModelIndex &proxyIndex) const override
    {
        QMap<int, QVariant> roles =
                QIdentityProxyModel::itemData(proxyIndex);
        roles.insert(Qt::DisplayRole, data(proxyIndex, Qt::DisplayRole));
        return roles;
    }

private:
    QString m_format;
};
```

这个例子包含几个重要规则：

1. 改写 `data()` 时，未处理的 role 应继续调用基类实现。
2. 在 `data()` 中读取源模型，使用 `mapToSource()`，不要用相同行列重新猜索引。
3. 只改写 `data()` 可能不足以覆盖 `itemData()` 的调用者，因此需要同步改写 `itemData()`。
4. 展示规则改变后必须通知视图。示例使用 reset，扁平表格也可以计算精确范围并发送 `dataChanged()`。
5. `sourceModel()` 可能为空，生产代码应在访问前确认；示例中的源模型在正常使用时应已设置。

如果代理新增了角色，还应考虑：

- 重写 `roleNames()`，让 QML 或其他按名称访问角色的代码能看到新角色；
- 必要时重写 `multiData()`，使批量角色读取和 `data()` 的语义一致；
- 为角色值变化发出正确范围的 `dataChanged()`，并携带受影响的 role 列表。

## 6. 运行时行为模型

### 6.1 读取数据

视图请求代理索引的数据时，典型路径是：

```text
view
  -> proxy.data(proxyIndex, role)
  -> mapToSource(proxyIndex)
  -> source.data(sourceIndex, role)
```

`QAbstractProxyModel` 提供了大部分通用转发逻辑。`QIdentityProxyModel` 负责把代理索引准确还原为源索引；派生类只需在确实改变语义的地方重写。

### 6.2 写入数据

默认写入路径类似：

```text
view / delegate
  -> proxy.setData(proxyIndex, value, role)
  -> mapToSource(proxyIndex)
  -> source.setData(sourceIndex, value, role)
```

这意味着代理默认是可编辑的，只要源模型接受对应 role 的写入。若代理只是改写显示文本，却不希望用户编辑，应该重写 `flags()` 收窄 `Qt::ItemIsEditable`，或者重写 `setData()` 明确拒绝某些 role。

### 6.3 结构变化

插入、删除和移动操作不会在代理内部复制一份数据。代理把操作转给源模型，源模型发出的结构信号再由代理转成自己的信号。

因此，代理模型的“结构透明”成立的前提是：

- 源模型正确调用 `beginInsertRows()` / `endInsertRows()` 等成对 API；
- 源模型发出的父索引属于源模型；
- 代理保留了对应的映射关系；
- 派生类没有另行改变行列拓扑。

### 6.4 选择变化

`QItemSelectionModel` 绑定的是某一个具体模型。视图使用代理模型时，选择也属于代理模型；如果业务逻辑要操作源模型，必须映射选择：

```cpp
QItemSelection sourceSelection =
        proxy->mapSelectionToSource(proxySelection);

QItemSelection proxySelection =
        proxy->mapSelectionFromSource(sourceSelection);
```

由于 `QIdentityProxyModel` 不过滤、不排序，选择范围通常可以一一对应。但索引所属模型仍然不同，不能省略映射。

## 7. 映射语义与索引边界

### 7.1 `mapToSource()` 和 `mapFromSource()` 应互相对应

对仍然存在的有效项，通常应满足：

```text
mapToSource(mapFromSource(sourceIndex)) == sourceIndex
mapFromSource(mapToSource(proxyIndex)) == proxyIndex
```

这里的“相等”表示对应同一模型、同一行列和同一内部项，而不是表示两个索引属于同一模型。

### 7.2 无效索引

以下情况应得到无效 `QModelIndex`：

- 输入本来就是无效索引；
- 没有设置源模型；
- 对应的项已经被源模型删除；
- 代理或源模型正在 reset，旧索引已失效。

可以这样检查：

```cpp
const QModelIndex sourceIndex = proxy->mapToSource(proxyIndex);
if (!sourceIndex.isValid())
    return;
```

不要用 `row() >= 0` 代替 `isValid()`。有效性还包含索引是否关联到一个模型。

### 7.3 索引必须属于正确的模型

传入错误模型的索引是编程错误：

```cpp
QModelIndex indexFromAnotherModel = otherModel->index(0, 0);
proxy->mapToSource(indexFromAnotherModel); // 不应这样做
```

调试构建中可能触发断言，发布构建也不能依赖未定义的映射结果。跨代理链操作时，每一层都要使用当前层的索引：

```text
source
  -> proxyA.mapFromSource(sourceIndex)
  -> proxyB.mapFromSource(proxyAIndex)
```

### 7.4 父索引与根节点

顶层项目的父索引是无效 `QModelIndex()`。映射时应保持这个约定：

```cpp
QModelIndex root;
int rows = proxy->rowCount(root);
```

树模型中，`rowCount(parent)`、`index(row, column, parent)`、`parent(child)` 必须使用同一层代理索引。不能把代理父索引转换成源父索引后，再把源索引误传给代理的其他函数。

### 7.5 内部指针和持久索引

透明代理需要在代理索引中保留源项的内部关联，才能把代理索引映射回源索引。Qt 提供的 `mapFromSource()` / `mapToSource()` 会处理这件事；使用者不应自行用行列号拼出替代索引。

源模型发生布局变化时，普通 `QModelIndex` 和 `QPersistentModelIndex` 的有效性由模型信号契约决定。代理默认会处理源模型的布局变化并维护相应的持久索引映射；如果关闭了自动处理，派生类必须承担这部分责任。

## 8. 源模型变化的转发

`QIdentityProxyModel` 的默认目标是让代理在结构上跟随源模型。可以按变化类型理解：

| 源模型变化 | 代理默认动作 |
| --- | --- |
| `rowsAboutToBeInserted()` / `rowsInserted()` | 映射父索引后转发代理行插入通知 |
| `rowsAboutToBeRemoved()` / `rowsRemoved()` | 映射父索引后转发代理行删除通知 |
| `rowsAboutToBeMoved()` / `rowsMoved()` | 映射源父索引和目标父索引后转发移动通知 |
| `columnsAboutToBeInserted()` / `columnsInserted()` | 映射父索引后转发代理列插入通知 |
| `columnsAboutToBeRemoved()` / `columnsRemoved()` | 映射父索引后转发代理列删除通知 |
| `columnsAboutToBeMoved()` / `columnsMoved()` | 映射源父索引和目标父索引后转发移动通知 |
| `dataChanged()` | 映射范围端点并转发相同的 role 列表 |
| `headerDataChanged()` | 转发相同的方向、section 范围和 role 语义 |
| `layoutAboutToBeChanged()` / `layoutChanged()` | 映射持久索引和父索引后转发布局变化 |
| `modelAboutToBeReset()` / `modelReset()` | 让代理模型进入并离开 reset 状态 |

其中结构变化和 reset 是透明代理的基本职责；Qt 6.8 新增的两个开关只影响数据变化和布局变化的自动连接。

## 9. Qt 6.8 的两个源变化开关

### 9.1 默认行为

默认情况下：

```cpp
proxy->handleSourceDataChanges();   // true
proxy->handleSourceLayoutChanges(); // true
```

代理会在 `setSourceModel()` 时连接源模型的：

- `dataChanged`；
- `layoutAboutToBeChanged`；
- `layoutChanged`。

这使得普通的透明代理无需自行转发这些信号。

### 9.2 为什么派生类可能要关闭它们

如果派生类对数据或布局有特殊处理，默认转发可能会重复发送或发送错误范围。例如：

- 代理把一个源 role 转换成另一个 role；
- 一个源项的变化会影响多个代理项；
- 代理需要先更新自己的缓存，再发 `dataChanged()`；
- 代理自己维护排序、分组或持久索引关系。

此时可在派生类构造阶段关闭自动处理：

```cpp
class CustomIdentityProxy : public QIdentityProxyModel
{
public:
    explicit CustomIdentityProxy(QObject *parent = nullptr)
        : QIdentityProxyModel(parent)
    {
        setHandleSourceDataChanges(false);
        setHandleSourceLayoutChanges(false);
    }
};
```

关闭之后，派生类必须自己连接源模型信号，并发出符合代理模型坐标的通知。只关闭而不补充转发，会导致视图不刷新或持久索引失效。

### 9.3 最容易误用的调用时序

`setHandleSourceDataChanges()` 和 `setHandleSourceLayoutChanges()` 是 protected 函数，并不是动态开关。

Qt 6.11 的实际连接选择发生在 `setSourceModel()` 建立源模型连接时。因此推荐顺序是：

```cpp
setHandleSourceDataChanges(false);
setHandleSourceLayoutChanges(false);
setSourceModel(sourceModel);
```

如果已经调用了 `setSourceModel(sourceModel)`，之后再修改这两个标志，并不会自动重建当前已有的信号连接。要让新的连接策略生效，应在设置标志后重新调用 `setSourceModel()`，或在派生类中自行管理连接。

这也是文档中“调用该方法只有在调用 `setSourceModel()` 后才会生效”容易引起歧义的地方：它实际指连接建立时读取该配置，而不是保证调用后立即重新连接。

### 9.4 两个 getter 的意义

```cpp
bool dataHandling = proxy->handleSourceDataChanges();
bool layoutHandling = proxy->handleSourceLayoutChanges();
```

它们只报告当前配置，不代表已经为某个源模型建立了连接，也不代表派生类已经正确发出自定义通知。

## 10. 与 `QAbstractProxyModel` 的关系

`QIdentityProxyModel` 继承了 `QAbstractProxyModel` 的通用转发能力。实际使用时，以下继承 API 同样重要：

- `sourceModel()`：读取当前源模型；
- `data()` / `setData()`：默认读取或写入映射后的源项；
- `itemData()` / `setItemData()`：批量读取或写入多个 role；
- `flags()`：默认转发编辑、拖放、可选等能力；
- `roleNames()`：默认转发源模型角色名称；
- `mimeData()`、`canDropMimeData()`、`dropMimeData()`：默认转发拖放；
- `canFetchMore()`、`fetchMore()`：默认转发懒加载；
- `setHeaderData()`：默认转发表头修改；
- `submit()`、`revert()`：默认转发缓存提交和撤销。

这些函数虽然不是 `QIdentityProxyModel` 自己重新声明的直接成员，但它们决定了“透明”在编辑、拖放和 QML 场景下是否成立。

如果代理只改写 `data()`，必须检查批量访问和写入路径是否仍然符合预期。尤其是：

- 重写了显示值，不代表 `itemData()` 自动使用了显示值；
- 重写了 `roleNames()`，不代表源模型仍然接受这些新 role 的写入；
- 改变了列语义，不应继续无条件使用基类的表头和拖放映射；
- 代理拒绝编辑时，最好同时修改 `flags()` 和 `setData()`，避免调用者绕过视图直接写入。

## 11. `setSourceModel()` 的生命周期边界

### 11.1 设置新源模型会使旧代理索引失效

更换源模型是结构级变化：

```cpp
proxy->setSourceModel(newSource);
```

更换前由旧源模型创建的代理索引、选择范围和持久索引都不能当作新模型中的有效对象使用。视图会收到 reset 相关通知并重新查询模型。

### 11.2 不要保存跨源模型的索引

以下做法有风险：

```cpp
QModelIndex saved = proxy->index(0, 0);
proxy->setSourceModel(anotherSource);
use(saved); // saved 已经不能代表当前 proxy 中的项
```

如果业务必须记住某个项，应保存业务主键，在新源模型建立后重新查找索引，而不是保存旧的 `QModelIndex`。

### 11.3 派生类重写时要调用基类

如果派生类需要重写 `setSourceModel()`，应保持 reset 和连接顺序。一个简化轮廓是：

```cpp
void MyProxy::setSourceModel(QAbstractItemModel *model)
{
    beginResetModel();

    disconnect(m_extraConnections);
    m_extraConnections.clear();

    QIdentityProxyModel::setSourceModel(model);

    if (model) {
        m_extraConnections = connect(
            model, &QAbstractItemModel::dataChanged,
            this, &MyProxy::handleSourceDataChanged);
    }

    rebuildCache();
    endResetModel();
}
```

实际项目要根据是否关闭自动处理来决定是否添加额外连接。不要在基类连接仍然存在时，再无条件发送同一范围的第二个 `dataChanged()`。

### 11.4 源模型的所有权

`setSourceModel()` 接收的是裸指针属性。代理通常只保存并观察它，不负责删除它。应保证：

- 源模型在代理使用期间仍然存活；
- 源模型和代理处于可安全通信的线程；
- 删除源模型前不再使用其索引；
- 通过 QObject 父子关系或其他明确所有权策略管理源模型。

## 12. 结构操作的共同规则

### 12.1 插入、删除和移动只请求源模型执行

`insertRows()`、`removeRows()`、`moveRows()` 以及列操作都返回源模型的结果。返回 `false` 表示源模型拒绝或无法完成操作，代理不会偷偷在本地创建备用数据。

### 12.2 `count` 和位置参数的边界由源模型决定

例如：

```cpp
bool ok = proxy->insertRows(row, count, parent);
```

代理保持 row、column、count 不变，只把 `parent` 映射到源模型。负数位置、越界位置、`count <= 0` 是否成功，最终遵循源模型实现的契约；调用者不应假设透明代理会替源模型修正参数。

### 12.3 行列移动需要源模型真正支持移动

`moveRows()` 与 `moveColumns()` 不等价于“删除后再插入”。源模型必须正确实现移动协议并发出成对的 about-to-move / moved 通知。否则应返回 `false`，不要在代理层模拟一个缺少正确索引维护的移动。

## 13. API 逐项说明

下面按 Qt 6.11.1 直接列出的成员逐项说明。继承自 `QAbstractProxyModel` 的常用 API 在上一节归纳；本节只展开 `QIdentityProxyModel` 自己声明的成员。

### 13.1 构造与析构

#### `explicit QIdentityProxyModel(QObject *parent = nullptr)`

**作用：** 创建一个透明代理模型对象。

**关键语义：**

- `parent` 遵守 QObject 父子对象规则；
- 构造后尚未设置实际源模型；
- 构造函数不会复制源数据，也不会自动发现某个源模型；
- 可以先配置 Qt 6.8 的两个处理标志，再调用 `setSourceModel()`。

**边界：**

- 没有源模型时，代理按空模型工作；
- 代理对象应在与视图和源模型兼容的线程中创建；
- 代理析构不等于源模型析构。

#### `virtual noexcept ~QIdentityProxyModel()`

**作用：** 销毁透明代理模型。

**关键语义：**

- 断开与源模型的连接；
- 释放代理自己的内部状态；
- 不负责删除没有作为其 QObject 子对象的源模型；
- 所有仍保存的代理索引在析构后都失效。

**边界：** 如果视图、选择模型或业务对象还保存代理索引，应先解除它们与代理的关系，再销毁代理。

### 13.2 结构与索引

#### `int columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用：** 返回代理中 `parent` 下的列数。

**关键语义：**

- 先把代理 `parent` 映射成源父索引；
- 返回源模型同一父项下的列数；
- 不改变列顺序，也不增加或隐藏列；
- 顶层查询使用无效父索引。

**边界：**

- `parent` 必须属于当前代理模型；
- 没有源模型或父项无效时，返回值遵循空模型/源模型语义，通常为零；
- 如果派生类改变了列结构，不能继续假设它与源模型相同。

#### `QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用：** 创建代理模型中指定位置的索引。

**关键语义：**

- 把 `parent` 映射到源父索引；
- 请求源模型创建相同 row、column 的源索引；
- 再把源索引映射回当前代理模型；
- 返回索引的 `model()` 是当前 `QIdentityProxyModel`，不是源模型。

**边界：**

- 越界位置返回无效索引；
- 不要用 `createIndex()` 自己重建源模型索引；
- 树模型必须使用属于同一代理的父索引；
- 结果只在模型结构未发生使其失效的变化前可靠。

#### `QModelIndex parent(const QModelIndex &child) const`

**作用：** 返回代理索引 `child` 的代理父索引。

**关键语义：**

- 先将 `child` 映射到源索引；
- 调用源模型的 `parent()`；
- 将返回的源父索引映射回代理；
- 顶层项的父索引是无效索引。

**边界：**

- `child` 必须属于当前代理；
- 对无效索引调用时返回无效索引；
- 代理没有改变层级时，父子关系与源模型一致。

#### `QModelIndex sibling(int row, int column, const QModelIndex &idx) const`

**作用：** 返回与 `idx` 具有相同父项、但位于指定 row 和 column 的代理索引。

**关键语义：**

- 将 `idx` 映射到源模型；
- 调用源模型的 `sibling()`；
- 将源结果映射回代理；
- 适合视图在同一父项内切换单元格时使用。

**边界：**

- `idx` 必须是当前代理索引；
- 目标位置不存在时返回无效索引；
- 派生类若改变行列拓扑，需重新评估 sibling 的语义。

#### `int rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用：** 返回代理中 `parent` 下的行数。

**关键语义：**

- 将代理父索引映射到源父索引；
- 返回源模型对应父项的行数；
- 不做过滤，因此不会因为 role 或文本内容隐藏源行。

**边界：**

- 源模型的懒加载、树层级和空父项规则仍然有效；
- `rowCount()` 不会触发 `fetchMore()`；
- 没有源模型时按空模型处理。

### 13.3 双向映射

#### `QModelIndex mapFromSource(const QModelIndex &sourceIndex) const`

**作用：** 把源模型索引转换为对应的代理索引。

**关键语义：**

- 保持 row、column 和父子结构对应；
- 创建一个属于当前代理模型的索引；
- 保留把代理索引再映射回源索引所需的内部关联；
- 源索引无效时返回无效代理索引。

**边界：**

- `sourceIndex` 必须属于当前 `sourceModel()`；
- 传入另一个源模型的索引属于编程错误；
- 源模型已删除或代理未设置源模型时不能继续使用旧索引。

#### `QModelIndex mapToSource(const QModelIndex &proxyIndex) const`

**作用：** 把代理索引转换为源模型索引。

**关键语义：**

- 返回的索引属于当前源模型；
- 保持索引的 row、column、层级和内部项对应；
- 代理数据读取、写入、拖放和选择转换都依赖这个方向；
- 代理索引无效时返回无效源索引。

**边界：**

- `proxyIndex` 必须属于当前 `QIdentityProxyModel`；
- 不要将代理索引保存到源模型长期使用；
- 更换源模型或 reset 后，旧代理索引不能继续映射。

#### `QItemSelection mapSelectionFromSource(const QItemSelection &selection) const`

**作用：** 把源模型中的选择范围转换成代理模型选择范围。

**关键语义：**

- 对选择中的范围端点进行映射；
- 因为 identity 代理不排序、不过滤，连续范围通常仍然对应连续范围；
- 返回的选择对象适用于绑定代理模型的 `QItemSelectionModel`。

**边界：**

- 输入选择中的索引必须属于当前源模型；
- 源模型变化后，旧选择可能已经失效；
- 如果派生类后来加入过滤、合并或重排，这个默认实现可能不再适合。

#### `QItemSelection mapSelectionToSource(const QItemSelection &selection) const`

**作用：** 把代理模型选择范围转换成源模型选择范围。

**关键语义：**

- 将代理选择中的范围映射到源模型；
- 适合把视图选中的代理项交给业务层或源模型处理；
- identity 代理不改变选择的行列关系。

**边界：**

- 输入选择必须是当前代理的选择；
- 不要把源选择直接传给这个函数；
- 复杂派生代理如果让一个代理项对应多个源项，需要自定义选择映射。

### 13.4 数据、表头与搜索

#### `QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用：** 返回代理模型的表头数据。

**关键语义：**

- `section`、方向和 role 原样交给源模型；
- identity 代理不改变表头的顺序和数量；
- 派生类只改单元格数据显示时，通常不需要重写它。

**边界：**

- 如果代理新增、隐藏或重排列，必须重新定义 section 到源 section 的映射；
- 表头变化仍由源模型的 `headerDataChanged()` 通知驱动；
- `DisplayRole` 只是默认 role，不是唯一可用 role。

#### `QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith | Qt::MatchWrap)) const`

**作用：** 从 `start` 开始搜索指定 role 等于或匹配 `value` 的代理索引。

**关键语义：**

- `start` 是代理索引；
- 搜索通常沿代理模型的列进行；
- 默认使用字符串前缀匹配并允许环回；
- `hits == -1` 表示搜索全部匹配项；
- 返回值中的索引属于代理模型，不是源模型。

**边界：**

- `Qt::MatchExactly`、`Qt::MatchContains`、正则和通配符等行为由 `flags` 决定；
- `hits` 为零时不会请求有效匹配；
- 搜索结果顺序不应作为稳定业务顺序依赖；
- 如果重写 `data()` 改变了 role 值，搜索应针对代理侧可见值理解。

### 13.5 拖放与结构修改

#### `bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用：** 在代理坐标中处理一次拖放数据。

**关键语义：**

- `parent` 映射到源父索引；
- row、column 和 `Qt::DropAction` 按 identity 关系传给源模型；
- 特殊的 `row == -1` 或 `column == -1` 位置语义由源模型继续处理；
- 返回源模型处理结果。

**边界：**

- 代理没有拖放能力时，源模型可能返回 `false`；
- 如果代理改写了 MIME 数据，需重写 `mimeData()` 和本函数保持一致；
- 代理坐标和源坐标相同不代表 parent 索引可以直接复用。

#### `bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用：** 请求在代理的 `parent` 下插入 `count` 列。

**关键语义：**

- 将 `parent` 映射到源父索引；
- 使用相同的 `column` 和 `count` 调用源模型；
- 返回源模型是否成功；
- 成功后的列变化通过源模型信号传播回代理。

**边界：**

- 不会在代理内部创建独立列；
- 插入位置和数量的合法性由源模型判断；
- 代理派生类若有列缓存，必须同步处理源列信号。

#### `bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用：** 请求在代理的 `parent` 下插入 `count` 行。

**关键语义：**

- `parent` 映射到源父索引；
- row 和 count 原样转发；
- 返回源模型结果；
- 代理本身不保存新行数据。

**边界：**

- 插入是否允许由源模型实现决定；
- 源模型必须正确发出行插入通知；
- 插入成功后，之前位于插入点之后的索引可能按模型规则变化。

#### `bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用：** 请求从代理的 `parent` 下删除一段列。

**关键语义：**

- 将父索引映射到源模型；
- 使用同一 column 和 count 调用源模型；
- 成功后的删除通知由代理转发。

**边界：**

- 删除会使被删除范围内的索引失效；
- 不要在 about-to-remove 通知之后继续把待删除索引当作有效索引；
- 代理不会恢复源模型拒绝的删除。

#### `bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用：** 请求从代理的 `parent` 下删除一段行。

**关键语义：**

- 将父索引映射到源模型；
- 使用同一 row 和 count 调用源模型；
- 返回源模型结果；
- 源模型负责真正删除数据和发出通知。

**边界：**

- 被删除项、其子项和相关持久索引都按模型删除规则处理；
- 业务层若需要保留选中项，应保存主键而不是保存被删除的索引；
- 源模型没有实现删除时通常返回 `false`。

#### `bool moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用：** 请求在代理中移动一段列。

**关键语义：**

- `sourceParent` 和 `destinationParent` 分别映射到源模型；
- `sourceColumn`、`count` 和 `destinationChild` 保持不变；
- 由源模型执行真正的移动；
- 返回源模型是否接受移动。

**边界：**

- 两个父索引都必须属于当前代理；
- 移动规则包括源范围和目标位置不能非法重叠；
- 不要把移动当作删除加插入，持久索引维护依赖源模型的移动协议。

#### `bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用：** 请求在代理中移动一段行。

**关键语义：**

- 两个父索引分别映射到源模型；
- row、count 和目标位置原样传给源模型；
- 源模型成功移动后，代理转发对应移动通知；
- 代理不重新排序，也不修改移动规则。

**边界：**

- 复杂树模型中源父项和目标父项可能不同；
- 目标位置使用 Qt 移动 API 的定义，不要自行按“删除后位置”重复调整；
- 源模型不支持移动时返回 `false`。

### 13.6 源模型设置与变化处理

#### `void setSourceModel(QAbstractItemModel *newSourceModel)`

**作用：** 设置代理要包装的源模型。

**关键语义：**

- 更换源模型时，代理会按基类契约重建源模型连接；
- 代理结构会随新源模型重新建立；
- 默认连接结构、header、reset，以及按配置决定的数据和布局变化；
- `newSourceModel == nullptr` 表示回到空模型状态。

**边界：**

- 源模型不由代理自动拥有；
- 更换源模型会使旧代理索引、选择和缓存失效；
- 派生类重写时应调用 `beginResetModel()`、基类实现和 `endResetModel()`；
- 调用 `setHandleSourceDataChanges()` / `setHandleSourceLayoutChanges()` 后再设置源模型，连接配置才会用于这次连接建立。

#### `bool handleSourceDataChanges() const`

**作用：** 查询代理是否配置为自动处理源模型的 `dataChanged()`。

**关键语义：**

- `true` 表示 `setSourceModel()` 建立连接时会自动转发数据变化；
- `false` 表示派生类准备自行处理源模型数据变化；
- 自 Qt 6.8 提供；
- 这是配置状态查询，不是“当前是否刚刚收到变化”的状态。

**边界：**

- 普通使用者不能直接修改该配置，因为 setter 是 protected；
- 读取到 `false` 后，派生类必须补充正确的源信号连接和代理信号；
- 只在当前源模型连接重建时体现配置变化。

#### `bool handleSourceLayoutChanges() const`

**作用：** 查询代理是否配置为自动处理源模型的布局变化。

**关键语义：**

- `true` 表示连接 `layoutAboutToBeChanged()` 和 `layoutChanged()`；
- `false` 表示派生类自行维护布局变化和持久索引；
- 自 Qt 6.8 提供；
- identity 代理默认开启。

**边界：**

- 关闭后不能只忽略布局信号；
- 如果代理持有缓存索引，必须在 about-to-change 阶段保存并在 changed 阶段更新；
- 改变 getter 对应的配置不会自动重新连接已经设置的源模型。

#### `protected void setHandleSourceDataChanges(bool b)`

**作用：** 设置代理在下一次建立源模型连接时是否自动处理 `dataChanged()`。

**关键语义：**

- `b == true` 使用内置数据变化转发；
- `b == false` 关闭内置数据变化转发；
- 默认值为 `true`；
- 自 Qt 6.8 提供；
- 只能在派生类中调用。

**推荐时序：**

```cpp
setHandleSourceDataChanges(false);
setSourceModel(sourceModel);
```

**边界：**

- 设置后不会自动替你连接自定义处理函数；
- 已有源模型连接不会因为标志变化而自动重建；
- 若关闭自动处理却继续依赖基类的 `dataChanged()`，视图可能不再刷新。

#### `protected void setHandleSourceLayoutChanges(bool b)`

**作用：** 设置代理在下一次建立源模型连接时是否自动处理布局变化。

**关键语义：**

- `b == true` 连接并转发源模型布局变化；
- `b == false` 由派生类自行处理布局变化；
- 默认值为 `true`；
- 自 Qt 6.8 提供；
- 只能在派生类中调用。

**边界：**

- 关闭后必须自己维护布局变化前后的持久索引；
- 已设置源模型时修改标志，不会自动断开或重新连接；
- 不要在内置转发和自定义转发同时启用时重复发信号。

## 14. 一个需要特别注意的 `itemData()` 问题

`QAbstractProxyModel::itemData()` 默认按源模型转发多个 role。假设派生类只改写：

```cpp
QVariant data(const QModelIndex &, int role) const override;
```

那么某些调用者执行：

```cpp
QMap<int, QVariant> allRoles = proxy->itemData(proxyIndex);
```

得到的 `Qt::DisplayRole` 可能仍然是源模型的原始值，而不是派生类 `data()` 返回的格式化值。Qt 文档中的日期代理因此显式重写 `itemData()`。

可以按如下原则处理：

- 改写单个 role 的显示语义时，同时检查 `itemData()`；
- 改写 role 名称或 QML 访问方式时，同时检查 `roleNames()`；
- 改写批量数据访问时，同时检查 `multiData()`；
- 改写写入语义时，同时检查 `setData()` 和 `setItemData()`。

## 15. 线程与事件边界

模型/视图 API 不是可以任意跨线程调用的普通容器 API。通常应满足：

- 源模型、identity 代理和使用它的视图处于同一线程；
- 不要从后台线程直接调用 GUI 线程中的代理或源模型；
- 后台任务完成后，通过信号、队列连接或其他线程安全方式把更新投递给模型所属线程；
- 不要在线程切换后继续使用旧的 `QModelIndex`；
- 更换源模型时确保没有其他线程正在读取旧索引。

`QIdentityProxyModel` 本身不提供线程同步，也不会把源模型操作自动转成线程安全请求。

## 16. 常见误区与排查顺序

### 16.1 把代理索引直接传给源模型

**现象：** 数据为空、断言、编辑了错误项或拖放位置不对。

**排查：**

```cpp
Q_ASSERT(proxyIndex.model() == proxy);
QModelIndex sourceIndex = proxy->mapToSource(proxyIndex);
```

### 16.2 以为 identity 代理不需要映射

虽然 row 和 column 通常相同，但索引的 `model()` 不同，源模型内部指针也需要由 Qt 正确保留。所有跨模型操作都应调用映射函数。

### 16.3 只重写 `data()`，忘了 `itemData()`

视图可能看起来正确，但导出、拖拽、QML 或其他批量调用者读到的仍是源值。按第 14 节同步检查。

### 16.4 关闭自动数据变化处理，却没有自己发信号

**现象：** 源数据确实变了，但视图不刷新。

**排查：**

- 是否在调用 `setSourceModel()` 之前关闭了开关；
- 是否自己连接了源模型的 `dataChanged()`；
- 是否将源范围映射成代理范围；
- 是否携带了正确的 role 列表；
- 是否误以为修改 setter 会自动重建已有连接。

### 16.5 关闭自动布局处理，却没有维护持久索引

**现象：** 排序、布局变化后，选择、展开状态或持久索引指向错误项。

**处理：** 要么保持默认自动处理，要么完整实现布局变化前后的索引保存、映射和通知。

### 16.6 用它做排序或过滤

`QIdentityProxyModel` 不会改变项目顺序和可见性。需要排序或过滤时使用 `QSortFilterProxyModel`，不要在 identity 代理中偷偷维护一套不一致的行号映射。

### 16.7 更换源模型后继续使用旧索引

`setSourceModel()` 是结构级切换。保存业务主键并重新查找，比保存旧 `QModelIndex` 更可靠。

### 16.8 把 reset 当成普通数据变化

如果源模型整体重建，应该由模型发出 reset 协议；调用者不要只手动发一个宽范围 `dataChanged()` 来掩盖行列结构已经变化的事实。

## 17. 与相近类的选择

| 需求 | 更合适的类型 | 原因 |
| --- | --- | --- |
| 只改显示文本、字体、颜色、提示或角色值 | `QIdentityProxyModel` | 结构完全透传，派生类只处理表现 |
| 按文本、角色或条件过滤 | `QSortFilterProxyModel` | 已有过滤映射和变化维护机制 |
| 按列排序或动态重排 | `QSortFilterProxyModel` | 专门维护排序后的索引关系 |
| 转置行列 | `QTransposeProxyModel` | 直接表达行列互换 |
| 完全自定义树/表拓扑 | `QAbstractProxyModel` | 需要自行实现索引拓扑和双向映射 |
| 自己保存一份独立数据 | `QAbstractItemModel` 派生类 | 不应把 identity 代理当作数据存储模型 |

多个代理可以串联：

```text
source
  -> identity proxy: 改日期显示
  -> sort/filter proxy: 排序或过滤
  -> view
```

串联后索引属于最外层代理。要访问源模型，需要按层逐次调用 `mapToSource()`；不要跨层直接传递索引。

## API 速查表
### 构造、生命周期与配置

| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `QIdentityProxyModel(QObject *parent = nullptr)` | 构造函数 | 创建透明代理模型 | 不设置源模型时按空模型工作；代理通常不拥有源模型 |
| `~QIdentityProxyModel()` | 析构函数 | 销毁代理并断开源模型连接 | 不等于删除源模型；所有代理索引随之失效 |
| `setSourceModel(QAbstractItemModel *newSourceModel)` | 公共函数 | 设置要包装的源模型 | 更换源模型会使旧索引和选择失效；派生重写要正确 reset |
| `handleSourceDataChanges() const` | Qt 6.8，公共函数 | 查询是否自动处理源 `dataChanged()` | 只反映配置；连接策略在 `setSourceModel()` 时建立 |
| `handleSourceLayoutChanges() const` | Qt 6.8，公共函数 | 查询是否自动处理源布局变化 | 关闭后派生类必须维护布局和持久索引 |
| `setHandleSourceDataChanges(bool b)` | Qt 6.8，protected | 配置源数据变化是否由内置逻辑处理 | 应在 `setSourceModel()` 前调用；不会自动重连当前源模型 |
| `setHandleSourceLayoutChanges(bool b)` | Qt 6.8，protected | 配置源布局变化是否由内置逻辑处理 | 关闭后要自行处理 `layoutAboutToBeChanged()` / `layoutChanged()` |

### 结构、索引与映射

| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `columnCount(const QModelIndex &parent = {}) const` | 重实现 | 查询代理父项的列数 | 父索引必须属于当前代理；结构默认与源相同 |
| `rowCount(const QModelIndex &parent = {}) const` | 重实现 | 查询代理父项的行数 | 不会自动 `fetchMore()`；树模型要使用代理父索引 |
| `index(int row, int column, const QModelIndex &parent = {}) const` | 重实现 | 创建代理索引 | 不能用源索引代替；返回索引属于代理 |
| `parent(const QModelIndex &child) const` | 重实现 | 查询代理索引的父项 | 顶层项返回无效索引；输入必须属于当前代理 |
| `sibling(int row, int column, const QModelIndex &idx) const` | 重实现 | 查询同父项下的兄弟索引 | 返回代理索引；复杂拓扑代理可能需自定义 |
| `mapFromSource(const QModelIndex &sourceIndex) const` | 重实现 | 源索引转代理索引 | 源索引必须属于当前源模型；无效输入返回无效索引 |
| `mapToSource(const QModelIndex &proxyIndex) const` | 重实现 | 代理索引转源索引 | 代理索引必须属于当前代理；用于读取、编辑和拖放 |
| `mapSelectionFromSource(const QItemSelection &selection) const` | 重实现 | 源选择转代理选择 | identity 结构下通常一一对应；复杂派生代理可能需重写 |
| `mapSelectionToSource(const QItemSelection &selection) const` | 重实现 | 代理选择转源选择 | 交给源模型处理业务选择时使用 |

### 数据、表头与搜索

| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const` | 重实现 | 返回代理表头数据 | section 默认与源相同；重排列时要重写 |
| `match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith \| Qt::MatchWrap)) const` | 重实现 | 搜索匹配的代理索引 | `hits == -1` 搜索全部；结果属于代理模型 |

### 行列修改与拖放

| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `insertRows(int row, int count, const QModelIndex &parent = {})` | 重实现 | 请求源模型插入行 | 代理不保存新行；成功依赖源模型 |
| `removeRows(int row, int count, const QModelIndex &parent = {})` | 重实现 | 请求源模型删除行 | 被删除索引失效；源模型负责通知 |
| `moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)` | 重实现 | 请求源模型移动行 | 两个父索引都要映射；不是删除加插入 |
| `insertColumns(int column, int count, const QModelIndex &parent = {})` | 重实现 | 请求源模型插入列 | 位置和数量由源模型判断 |
| `removeColumns(int column, int count, const QModelIndex &parent = {})` | 重实现 | 请求源模型删除列 | 删除范围内的索引失效 |
| `moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)` | 重实现 | 请求源模型移动列 | 依赖源模型支持正确的移动协议 |
| `dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)` | 重实现 | 在代理位置处理拖放 | parent 映射到源；特殊 -1 位置仍由源模型解释 |

## 19. 一句话总结

`QIdentityProxyModel` 是“结构透明、表现可改”的模型适配层：它不复制源数据，不改变行列拓扑，而是用可靠的双向索引映射把源模型交给视图使用。最重要的实践规则是始终区分代理索引与源索引，并在重写数据或关闭自动变化处理时同步维护角色、选择、信号和持久索引语义。
