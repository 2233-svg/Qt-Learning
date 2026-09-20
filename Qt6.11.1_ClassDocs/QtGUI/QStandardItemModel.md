# QStandardItemModel
> Qt 6.11.1 · Qt GUI · 来自 `QStandardItemModel`

## 1. 先建立直觉

`QStandardItemModel` 是基于 `QStandardItem` 的通用模型实现。它让你不用从零实现 `QAbstractItemModel`，就能向 `QListView`、`QTableView`、`QTreeView` 提供列表、表格或树形数据。

它的优势是快、直观、功能全；代价是每个单元格都是 item 对象，超大数据集会比较重。

## 2. 类说明

- 头文件：`#include <QStandardItemModel>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAbstractItemModel`
- 节点类型：`QStandardItem`
- 协作类：`QItemSelectionModel`、`QSortFilterProxyModel`、各类 item view

模型拥有其中的 item。`setItem()`、`appendRow()` 等函数会接管传入指针；`takeItem()`、`takeRow()`、`takeColumn()` 会把所有权交还给调用者。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 构造函数 | 创建空模型或指定初始行列 |
| `setRowCount()` / `setColumnCount()` | 调整根层级表格尺寸 |
| `setItem()` / `item()` | 设置或读取指定单元格 item |
| `appendRow()` / `appendColumn()` | 追加行或列 |
| `insertRow()` / `insertColumn()` | 插入行或列 |
| `takeItem()` / `takeRow()` / `takeColumn()` | 移除 item 且调用者接管所有权 |
| `clear()` | 清空所有 item 和表头 |
| `invisibleRootItem()` | 获取不可见根 item，便于树形操作 |
| `indexFromItem()` / `itemFromIndex()` | 在 item 与 `QModelIndex` 之间转换 |
| `setHorizontalHeaderLabels()` / `setVerticalHeaderLabels()` | 设置表头文本 |
| `setHorizontalHeaderItem()` / `setVerticalHeaderItem()` | 设置表头 item |
| `findItems()` | 按文本和匹配规则查找 item |
| `setSortRole()` / `sortRole()` | 指定排序读取哪个 role |
| `sort()` | 按列排序 |
| `setItemRoleNames()` / `roleNames()` | 设置 role 名称，常用于 QML 或调试 |
| `itemChanged` | item 数据变化信号 |

## 4. 关键用法

表格：

```cpp
auto *model = new QStandardItemModel(0, 3, this);
model->setHorizontalHeaderLabels({"Name", "Type", "Size"});
model->appendRow({
    new QStandardItem("main.cpp"),
    new QStandardItem("C++"),
    new QStandardItem("12 KB")
});
view->setModel(model);
```

树：

```cpp
auto *root = model->invisibleRootItem();
auto *project = new QStandardItem("App");
project->appendRow(new QStandardItem("Sources"));
root->appendRow(project);
```

排序用业务 role：

```cpp
item->setData(fileSizeBytes, Qt::UserRole);
model->setSortRole(Qt::UserRole);
model->sort(2);
```

## 5. 使用场景

- 小型表格、树、列表 UI。
- 需要内置拖放、编辑、勾选、图标、表头的快速模型。
- 配合 `QSortFilterProxyModel` 做过滤排序。
- 原型阶段先跑通模型/视图，后续再替换为自定义模型。
- 工具类应用中的配置树、资源列表、日志分类。

## 6. 常见坑与经验

- `clear()` 会删除所有 item 和表头，也会让旧 `QModelIndex` 失效。
- `itemChanged` 对任何 role 变化都可能触发，槽里修改同一 item 时注意递归。
- 对树结构，用 `invisibleRootItem()` 和 item 的 `appendRow()` 更自然；对表结构，用 model 的行列 API 更直接。
- `findItems()` 默认只查一列，且是基于文本匹配，不适合大数据全文搜索。
- 超大模型、懒加载、实时刷新列表，应自定义 `QAbstractItemModel`，不要硬塞 `QStandardItemModel`。

## 7. 知识点覆盖

本页覆盖：标准 item 模型、列表/表格/树、item 所有权、表头、索引转换、排序 role、拖放 MIME、模型/视图通知。
