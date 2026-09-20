# QListWidgetItem

> Qt 6.11.1 · Qt Widgets · 来自 `QListWidgetItem`

## 1. 先建立直觉

`QListWidgetItem` 是 `QListWidget` 中的一行数据项。它不是 QWidget，也没有 QObject 父子关系；它保存文本、图标、勾选状态、字体、颜色、提示文本、尺寸建议和自定义数据，然后由 `QListWidget` 的内部模型显示出来。

它适合承载轻量显示数据和业务 id。真正复杂的业务对象不建议直接继承或塞满 item；更稳的做法是在 `Qt::UserRole` 中保存 id，再通过业务层查询完整对象。

## 2. 类说明

- 头文件：`#include <QListWidgetItem>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

item 加入 `QListWidget` 后由列表管理生命周期；从列表 `takeItem()` 后由调用者管理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QListWidgetItem(parent, type)` | 创建 item 并可直接插入列表。排序开启时更建议先构造再插入。 |
| `QListWidgetItem(text, parent, type)` | 创建带文本的 item。 |
| `QListWidgetItem(icon, text, parent, type)` | 创建带图标和文本的 item。 |
| `QListWidgetItem(other)` / `operator=()` | 复制 item 数据；不会复制所属列表。 |
| `clone()` | 创建副本，子类需要保留自定义类型时应重写。 |
| `type()` | 返回 item 类型；自定义类型从 `UserType` 起。 |
| `listWidget()` | 返回当前所属 `QListWidget`，未插入时为空。 |
| `text()` / `setText()` | 主显示文本。 |
| `icon()` / `setIcon()` | 显示图标。 |
| `data(role)` / `setData(role, value)` | 按 Qt item role 读取和写入数据。 |
| `checkState()` / `setCheckState()` | 勾选状态；还需要 flags 允许 user check。 |
| `flags()` / `setFlags()` | 控制是否可选、可编辑、可拖拽、可勾选等。 |
| `font()` / `setFont()` | 文本字体。 |
| `foreground()` / `setForeground()` | 前景画刷，通常控制文字颜色。 |
| `background()` / `setBackground()` | 背景画刷。 |
| `sizeHint()` / `setSizeHint()` | 项目推荐尺寸。 |
| `toolTip()` / `setToolTip()` | 鼠标提示。 |
| `statusTip()` / `setStatusTip()` | 状态栏提示。 |
| `whatsThis()` / `setWhatsThis()` | What's This 帮助文本。 |
| `textAlignment()` / `setTextAlignment()` | 文本对齐；`setTextAlignment` 自 Qt 6.4 起可用。 |
| `isHidden()` / `setHidden()` | 视图中隐藏或显示该项。 |
| `isSelected()` / `setSelected()` | 查询或设置选中状态。 |
| `read()` / `write()` | 用 `QDataStream` 序列化 item 数据。 |
| `operator<()` | 排序比较逻辑，子类可重写。 |
| `operator<<` / `operator>>` | 非成员流操作符。 |

## 4. 关键用法

### 数据角色比堆字段更好用

显示文本走 `Qt::DisplayRole`，图标走 `Qt::DecorationRole`，勾选走 `Qt::CheckStateRole`。业务 id、原始路径、数据库主键这类附加值放在 `Qt::UserRole` 及之后的角色中，比把信息拼进文本再解析可靠得多。

### 勾选项需要 flags 配合

只设置 `setCheckState()` 通常能显示状态，但真正的用户交互要看 `flags()` 是否包含 `Qt::ItemIsUserCheckable`。同理，可编辑需要 `Qt::ItemIsEditable`，可拖拽/可放置也要对应 flag。

### 排序：重写 `operator<()`

`QListWidget::sortItems()` 会调用 item 的比较逻辑。默认比较通常基于文本；如果文本是版本号、数字、日期或带前缀编号，建议继承 `QListWidgetItem` 并重写 `operator<()`，或把排序交给模型视图体系。

### 插入时避免“半构造排序”

构造函数允许传 `QListWidget *parent` 并直接插入列表。但如果列表已经开启排序，插入时可能需要比较 item，而 item 还在构造过程中。更稳的写法是先 `new QListWidgetItem(...)`，设置完数据后再 `addItem()` 或 `insertItem()`。

## 5. 常见坑与经验

- `QListWidgetItem` 不是 QWidget，不能安装布局，也没有信号槽。
- item 被列表接管后不要手动 delete；除非先用 `takeItem()` 取出。
- 复制 item 不会复制它属于哪个列表。
- 隐藏 item 是视图层操作；复杂过滤更适合 `QListView` + proxy model。
- 批量修改 item 会触发 `itemChanged()`，需要时用列表的信号阻断器包住更新过程。
