# QRangeModel
> Qt 6.11.1 · Qt Core · 来自 `QRangeModel`

## 作用定位
`QRangeModel` 是 Qt 6.10 起提供的范围到模型/视图协议的桥梁。它把满足顺序范围要求的 C++ 数据组织成 `QAbstractItemModel`，从而能被 Widgets 视图、代理模型和 QML 模型消费者使用，而不必为常见的列表、表和树手写大量样板模型代码。

模型是底层 range 的“受控入口”。一旦 range 已交给模型和视图使用，就不能绕过模型直接修改它；否则 `QModelIndex`、选择状态及视图缓存将不同步。

## API 速查
| API | 是做什么的 |
|---|---|
| `QRangeModel(range, parent)` | 将列表或表式范围包装为模型；按值传入时模型拥有范围。 |
| `QRangeModel(range, protocol, parent)` | 以协议描述树形范围的父子遍历方式。 |
| `data()` / `multiData()` | 以角色读取单元格或项目数据。 |
| `rowCount()` / `columnCount()` / `index()` / `parent()` | 向视图提供模型结构。 |
| `setData()` / `setItemData()` | 在底层范围允许写入时编辑数据。 |
| `insert*` / `remove*` / `move*` | 通过模型通知协议安全改变结构。 |
| `setRoleNames()` / `resetRoleNames()` | 定义 QML 和代理读取的角色名称。 |
| `setAutoConnectPolicy()` | 控制 QObject 行项目的属性变化是否自动映射为 `dataChanged`。 |
| `AutoConnectPolicy::None` | 默认值；不自动建立属性信号连接。 |
| `AutoConnectPolicy::Full` | 为所有有关 QObject 属性建立连接，更新及时但内存成本高。 |
| `AutoConnectPolicy::OnRead` | 某角色首次被读取时才连接，节约初始成本但连接集合会随浏览增长。 |

## 使用场景

### 用普通容器快速提供只读列表
```cpp
std::vector<QString> cities = {"Beijing", "Shanghai"};
QRangeModel model(cities);
view->setModel(&model);
```
如果把容器以值移入模型，模型拥有它，外部不再维护同一份数据；如果传引用或指针，外部仍拥有数据，但所有后续结构修改必须通过配套的 `QRangeModelAdapter` 完成。

### QObject 项目自动更新
当列表元素是 `QObject` 并以属性向角色暴露数据时，可考虑 `OnRead`：
```cpp
model.setAutoConnectPolicy(QRangeModel::AutoConnectPolicy::OnRead);
```
适合长列表只显示少量可见行的情况。频繁滚动海量不同项目时，已连接属性会积累，需评估内存与连接数。

## 常见坑与经验
- `QRangeModel` 是新接口：页中标有 6.10/6.11 的功能应以实际 Qt 版本为准。
- 不要在 `data()` 的读取路径改变底层数据；读取可能被视图高频调用。
- `roleNames` 是 QML 接口契约。修改角色名会影响 QML 绑定和代理代码，应保持稳定。
- Full 自动连接易于使用，但对于成千上万的 QObject 项可能有显著连接开销；默认 `None` 不是漏功能，而是明确的性能选择。
- 后台线程不能直接改正在 GUI 线程显示的模型；将结果投递到模型所在线程，再通过模型或 adapter 修改。

## 知识点覆盖
C++ ranges、模型/视图、`QModelIndex` 生命周期、角色数据、QML 模型角色、QObject 属性通知、结构变更协议、所有权、GUI 线程约束。
