# QRangeModelAdapter
> Qt 6.11.1 · Qt Core · 来自 `QRangeModelAdapter<Range, Protocol, Model>`

## 作用定位
`QRangeModelAdapter` 是 `QRangeModel` 的安全编辑门面。它既持有/引用原始 C++ range，又负责在插入、删除、移动和改值时发出正确的模型通知，因此视图、代理模型和持久索引不会因为“容器悄悄变了”而失去一致性。

它适合应用代码修改数据；`QRangeModel` 更像给视图调用的模型本体。拿到原始 `std::vector` 后直接 `push_back()` 是绕过协议，应该避免。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 以 range 和可选树协议创建 adapter 及其模型。 |
| `model()` | 取得供 view/QML 使用的 `QRangeModel` 指针。 |
| `range()` | 只读访问被适配的原始范围。 |
| `assign(...)` | 以新范围整体替换内容，并保持模型状态一致。 |
| `data(...)` / `at(...)` / `operator[]` | 用列表、表或树的位置读取项目。 |
| `setData(...)` | 用角色数据修改一个项目，成功返回 `true`。 |
| `insertRow(s)` / `insertColumn(s)` | 在指定位置安全插入行或列。 |
| `removeRow(s)` / `removeColumn(s)` | 安全移除结构元素。 |
| `moveRow(s)` / `moveColumn(s)` | 改变顺序并发送 move 通知。 |
| `rowCount()` / `columnCount()` / `hasChildren()` | 查询 range 映射出的模型结构。 |
| 迭代器与 `DataReference` | 用 STL 风格遍历或赋值，但结构修改会使引用失效。 |

## 使用场景

### 编辑向量并立即刷新视图
```cpp
std::vector<QString> names = {"Ada", "Linus"};
QRangeModelAdapter adapter(names);
view->setModel(adapter.model());

adapter.insertRow(1, QString("Grace"));
adapter.setData(0, QString("Ada Lovelace"));
```
让 adapter 完成操作，视图会看到与 `beginInsertRows/endInsertRows` 等价的完整通知。不要在这之后直接对 `names` 调用 `insert`、`erase` 或排序。

### 将模型当作范围读取
adapter 的迭代器和 `at()` 方便把模型交给算法，但其返回的 `DataReference` 是模型访问代理，不是稳定的普通 C++ 引用。结构变化之后立即重新定位，别缓存它。

## 常见坑与经验
- 能否插入、删除、移动取决于 `Range` 的能力；模板重载会在不满足条件时根本不参与编译，而不是运行时失败。
- 表和树的位置语义不同：树通常使用 `QSpan<const int>` 路径，列表使用单一行号；不要把二者混淆。
- 数据角色转换失败时 `setData()` 会返回 `false`；不要假定任意 `QVariant` 都能写进底层元素。
- 适配器析构后，其 `model()` 指针失效。视图使用模型的生命周期必须被 adapter 覆盖。
- 直接修改 range 是最危险的错误：表面上数据变了，模型却没有对应信号，后续可能出现错行、悬空索引或崩溃。

## 知识点覆盖
模型一致性、结构通知、C++ ranges、模板约束、列表/表/树、数据角色、`QVariant` 转换、迭代器失效、视图缓存与所有权。
