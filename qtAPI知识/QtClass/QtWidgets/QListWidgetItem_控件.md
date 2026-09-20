# Qt QListWidgetItem 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QListWidgetItem>`
> 所属模块：`Qt6::Widgets`
> 继承：无
> 常见搭档：`QListWidget`、`Qt::ItemDataRole`、`QVariant`

## 1. QListWidgetItem 解决什么问题

`QListWidgetItem` 是 `QListWidget` 里的一个条目对象。它把一个列表项需要展示和参与交互的数据集中在一起：

- 标题文字；
- 图标；
- 字体和颜色；
- 勾选状态；
- 是否可选、可编辑、可拖放；
- 工具提示和状态提示；
- 自定义 `QVariant` 数据；
- 排序和序列化行为。

它不是 `QWidget`，不能给它设置布局，也不能把它当成真正的控件。它更像是“被 `QListWidget` 显示出来的一条数据记录”。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QListWidget>
#include <QListWidgetItem>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QListWidget list;
    auto *item = new QListWidgetItem(QIcon(":/icons/file.png"), "main.cpp");
    item->setData(Qt::UserRole, 42);
    item->setCheckState(Qt::Unchecked);
    list.addItem(item);

    list.show();
    return app.exec();
}
```

### 2.1 item 的所有权

把 item 加入 `QListWidget` 后，列表会管理它：

```cpp
auto *item = new QListWidgetItem("temporary");
list->addItem(item);

QListWidgetItem *taken = list->takeItem(0);
delete taken;
```

`takeItem()` 把 item 从列表中取出，后续释放责任回到调用方。

## 3. 先理解 role 数据

### 3.1 可见属性其实都是 role 数据

很多便捷函数最终都落到 `data(role)` / `setData(role, value)`：

```cpp
item->setText("Report");
item->setData(Qt::UserRole, reportId);
```

可以把它理解成：

```text
DisplayRole     -> 显示文字
DecorationRole  -> 图标
FontRole        -> 字体
ForegroundRole  -> 前景画刷
BackgroundRole  -> 背景画刷
CheckStateRole  -> 勾选状态
UserRole        -> 业务自定义数据
```

### 3.2 `UserRole` 不要只存显示文本

推荐把稳定业务 ID、数据库主键或轻量状态放到 `Qt::UserRole`：

```cpp
item->setData(Qt::UserRole, documentId);
```

这样即使列表排序、插入或删除，业务对象仍能通过 ID 找到，不会因为行号变化而错位。

## 4. 自定义 item 类型

`ItemType::UserType` 的最小值是 `1000`。如果你派生 `QListWidgetItem`，可以传入大于等于 `UserType` 的类型值：

```cpp
class FileItem : public QListWidgetItem
{
public:
    enum { Type = QListWidgetItem::UserType + 1 };
    FileItem() : QListWidgetItem(Type) {}
    FileItem *clone() const override { return new FileItem(*this); }
};
```

类型值适合让代码区分标准 item 和自定义 item。小于 `UserType` 的值由 Qt 保留，不应拿来定义业务类型。

## 5. 排序、复制和序列化

### 5.1 排序

`operator<()` 决定 item 参与排序时的比较规则。默认通常依据显示数据比较；如果你要按隐藏的业务字段排序，就可以重写它。

### 5.2 clone 和赋值

`clone()` 适合在拖放、复制或模型操作中创建 item 的副本。赋值运算符复制的是数据和 flags，但不会复制 `type()` 和所属的 `QListWidget`。

### 5.3 QDataStream

`read()` / `write()` 以及 `operator<<` / `operator>>` 用来做二进制序列化。自定义 item 如果需要保存到文件或拖放数据中，应让读写格式保持对称。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `ItemType::Type` | 标准列表 item 的默认类型。 | 值为 `0`。 |
| 枚举 | `ItemType::UserType` | 自定义 item 类型的起始值。 | 值为 `1000`，更小的值由 Qt 保留。 |
| 构造 | `QListWidgetItem(QListWidget *listview = nullptr, int type = Type)` | 创建 item，可选地直接插入列表。 | 排序列表中不建议在构造阶段直接传 parent。 |
| 构造 | `QListWidgetItem(const QString &text, QListWidget *listview = nullptr, int type = Type)` | 创建带标题的 item。 | 需要控制插入位置时，先不传列表，再调用 `insertItem()`。 |
| 构造 | `QListWidgetItem(const QIcon &icon, const QString &text, QListWidget *listview = nullptr, int type = Type)` | 创建带图标和标题的 item。 | 同样注意排序列表里的插入时机。 |
| 构造 | `QListWidgetItem(const QListWidgetItem &other)` | 复制 item 数据。 | 不复制所属列表和类型归属关系。 |
| 析构 | `~QListWidgetItem()` | 销毁 item。 | 已在列表中的 item 通常由列表负责销毁。 |
| 工厂 | `clone() const` | 创建当前 item 的副本。 | 自定义派生 item 时应重写并返回派生类型。 |
| 查询 | `listWidget() const` | 返回 item 所属的列表。 | item 未加入列表时为空。 |
| 修改 | `setSelected(bool select)` | 设置选中状态。 | 需要 item 已被列表管理才有完整视觉效果。 |
| 查询 | `isSelected() const` | 查询是否选中。 | 只反映当前选择状态。 |
| 修改 | `setHidden(bool hide)` | 隐藏或显示 item。 | 隐藏不等于从列表删除。 |
| 查询 | `isHidden() const` | 查询是否隐藏。 | 与 `QListWidget::setItemWidget()` 无关。 |
| 查询 | `flags() const` | 获取 item 的交互标志。 | 决定可选、可编辑、可拖放等能力。 |
| 修改 | `setFlags(Qt::ItemFlags flags)` | 设置 item 交互标志。 | 常用于定制条目是否可编辑或勾选。 |
| 查询 | `text() const` | 获取显示文字。 | 实际对应 `Qt::DisplayRole`。 |
| 修改 | `setText(const QString &text)` | 设置显示文字。 | 会触发列表刷新。 |
| 查询 | `icon() const` | 获取显示图标。 | 实际对应 `Qt::DecorationRole`。 |
| 修改 | `setIcon(const QIcon &icon)` | 设置显示图标。 | 图标大小由视图和样式共同影响。 |
| 查询 | `statusTip() const` | 获取状态提示。 | 通常显示在状态栏。 |
| 修改 | `setStatusTip(const QString &statusTip)` | 设置状态提示。 | 需要外层界面显示状态栏才明显。 |
| 查询 | `toolTip() const` | 获取鼠标悬停提示。 | 依赖 tooltip 功能。 |
| 修改 | `setToolTip(const QString &toolTip)` | 设置鼠标悬停提示。 | 适合补充被截断的标题。 |
| 查询 | `whatsThis() const` | 获取 What's This 帮助文本。 | 用于上下文帮助。 |
| 修改 | `setWhatsThis(const QString &whatsThis)` | 设置 What's This 帮助文本。 | 依赖 What's This 功能。 |
| 查询 | `font() const` | 获取 item 字体。 | 对单条目设置显示样式。 |
| 修改 | `setFont(const QFont &font)` | 设置 item 字体。 | 不建议用来替代统一样式系统。 |
| 查询 | `textAlignment() const` | 获取文字对齐方式。 | Qt 6.4 以后推荐使用 `Qt::Alignment` 语义。 |
| 修改 | `setTextAlignment(Qt::Alignment alignment)` | 设置文字对齐方式。 | 旧的整数重载已弃用。 |
| 查询 | `background() const` | 获取背景画刷。 | 适合标记状态或分组。 |
| 修改 | `setBackground(const QBrush &brush)` | 设置背景画刷。 | `NoBrush` 可用于清除自定义背景。 |
| 查询 | `foreground() const` | 获取前景画刷。 | 通常影响文字颜色。 |
| 修改 | `setForeground(const QBrush &brush)` | 设置前景画刷。 | 状态表达最好同时考虑无障碍。 |
| 查询 | `checkState() const` | 获取勾选状态。 | 需要 flags 包含可勾选能力。 |
| 修改 | `setCheckState(Qt::CheckState state)` | 设置勾选状态。 | 常见值有 Unchecked、PartiallyChecked、Checked。 |
| 查询 | `sizeHint() const` | 获取 item 尺寸提示。 | 无效时由 delegate 计算。 |
| 修改 | `setSizeHint(const QSize &size)` | 设置 item 尺寸提示。 | 可用于让某一行变高。 |
| 查询 | `data(int role) const` | 按 role 读取数据。 | 自定义 item 逻辑的核心入口。 |
| 修改 | `setData(int role, const QVariant &value)` | 按 role 写入数据。 | 默认实现把 DisplayRole 和 EditRole 视为同一数据。 |
| 比较 | `operator<(const QListWidgetItem &other) const` | 定义 item 排序规则。 | `QListWidget::sortItems()` 会用到。 |
| 序列化 | `read(QDataStream &in)` | 从数据流读取 item。 | 自定义 read/write 必须保持格式一致。 |
| 序列化 | `write(QDataStream &out) const` | 把 item 写入数据流。 | 适合持久化和拖放。 |
| 赋值 | `operator=(const QListWidgetItem &other)` | 复制对方的数据和 flags。 | 不复制 type 和所属 `QListWidget`。 |
| 查询 | `type() const` | 返回 item 类型值。 | 自定义类型应使用 `UserType` 以上的值。 |
| 非成员 | `operator<<(QDataStream &, const QListWidgetItem &)` | 把 item 写入数据流。 | 内部调用 `write()`。 |
| 非成员 | `operator>>(QDataStream &, QListWidgetItem &)` | 从数据流读出 item。 | 内部调用 `read()`。 |

### 一句话总结

`QListWidgetItem` 是列表中的数据条目，不是 QWidget；把显示信息放进标准 role，把稳定业务标识放进 `UserRole`，再用 flags、排序和自定义类型扩展它。
