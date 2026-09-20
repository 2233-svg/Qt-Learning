# QStandardItem
> Qt 6.11.1 · Qt GUI · 来自 `QStandardItem`

## 1. 先建立直觉

`QStandardItem` 是 `QStandardItemModel` 里的一个节点。它既可以表示表格中的一个单元格，也可以表示树上的一个节点；它保存 role 数据、图标、文字、字体、颜色、勾选状态、可编辑/可拖放等 item flags，还能拥有子 item。

它适合中小规模模型快速开发。数据量巨大、需要懒加载或强业务结构时，自定义 `QAbstractItemModel` 往往更合适。

## 2. 类说明

- 头文件：`#include <QStandardItem>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：普通 C++ 类，不是 `QObject`
- 所属模型：`QStandardItemModel`
- 所有权：放入 item/model 后，模型或父 item 负责销毁；`take*()` 会取回所有权

`QStandardItem` 的核心是 role 数据。`setText()` 只是 `Qt::DisplayRole`/`Qt::EditRole` 的便利 API；`setData(value, role)` 才是通用入口。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 构造函数 | 创建空 item、文本 item、图标文本 item、预留子表尺寸 |
| `setText()` / `text()` | 设置或读取显示文本 |
| `setIcon()` / `icon()` | 设置或读取图标 |
| `setData()` / `data()` / `clearData()` | 按 role 存取通用数据 |
| `setFlags()` / `flags()` | 一次性设置 item 能力 |
| `setEditable()` / `isEditable()` | 控制是否可编辑 |
| `setCheckable()` / `setCheckState()` | 控制复选框和状态 |
| `setSelectable()` / `setEnabled()` | 控制选择与启用 |
| `setDragEnabled()` / `setDropEnabled()` | 控制拖放能力 |
| `appendRow()` / `appendColumn()` / `appendRows()` | 添加子 item |
| `insertRow(s)` / `insertColumn(s)` | 插入子结构 |
| `removeRow(s)` / `removeColumn(s)` | 删除子结构并销毁 |
| `takeRow()` / `takeColumn()` / `takeChild()` | 移除但不销毁，调用者接管 |
| `child()` / `parent()` / `row()` / `column()` | 查询树关系和位置 |
| `model()` / `index()` | 回到模型和 `QModelIndex` |
| `clone()` / `type()` / `operator<()` | 子类化、原型和排序定制 |
| `read()` / `write()` | 数据流序列化 |

## 4. 角色与便利属性

| 便利 API | 常见对应 role 或视图行为 |
| --- | --- |
| `setText` | `DisplayRole` / `EditRole` |
| `setToolTip` | `ToolTipRole` |
| `setStatusTip` | `StatusTipRole` |
| `setWhatsThis` | `WhatsThisRole` |
| `setFont` | `FontRole` |
| `setForeground` / `setBackground` | `ForegroundRole` / `BackgroundRole` |
| `setTextAlignment` | `TextAlignmentRole` |
| `setSizeHint` | `SizeHintRole` |
| `setAccessibleText` / `setAccessibleDescription` | 无障碍辅助信息 |

自定义业务数据建议从 `Qt::UserRole` 或更高 role 开始，避免覆盖 Qt 视图约定的内置 role。

## 5. 关键用法

构建树：

```cpp
auto *root = model->invisibleRootItem();
auto *group = new QStandardItem("Images");
group->appendRow(new QStandardItem("logo.png"));
root->appendRow(group);
```

存业务 id：

```cpp
item->setData(fileId, Qt::UserRole);
item->setData(filePath, Qt::UserRole + 1);
```

取回 item 所有权：

```cpp
QStandardItem *detached = parent->takeChild(row);
// detached 现在由调用者负责 delete 或重新插入
```

子类化排序：

```cpp
class NumberItem : public QStandardItem {
public:
    bool operator<(const QStandardItem &other) const override {
        return data(Qt::UserRole).toInt() < other.data(Qt::UserRole).toInt();
    }
};
```

## 6. 使用场景

- 快速搭建 `QListView`、`QTableView`、`QTreeView` 数据。
- 设置图标、颜色、字体、勾选框等常见显示状态。
- 简单树形配置、文件列表、属性表。
- 教学和原型阶段，不想立即实现自定义模型。
- 通过 item prototype 支持自定义 item 克隆。

## 7. 常见坑与经验

- 一个 `QStandardItem` 不能同时属于两个位置；插入模型后所有权转移。
- `removeRow()` 会删除 item；想保留对象必须用 `takeRow()`。
- `setData()` 后子类如果自己管理数据，应调用 `emitDataChanged()` 通知模型。
- 大量 item 会有明显内存开销；几十万行数据应考虑自定义模型。
- `index()` 只有 item 已在模型中时才有意义。

## 8. 知识点覆盖

本页覆盖：item role 数据、模型所有权、树/表结构、flags、勾选状态、拖放、排序、子类化、序列化、无障碍文本。
