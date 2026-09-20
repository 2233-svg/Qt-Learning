# QListWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QListWidget`

## 1. 先建立直觉

`QListWidget` 是 `QListView` 的便捷版本：它内置了一个 item-based 模型，让你直接创建 `QListWidgetItem`，不用先写 `QAbstractListModel`。它适合设置页选项、短列表、工具列表、最近文件、标签候选、简单拖拽排序等中小规模场景。

它的代价也很明确：数据被包在 item 里，业务层和视图容易耦合。列表很大、数据来自数据库/网络、需要复用模型或做复杂排序过滤时，应转向 `QListView` + model。

最需要记住的是所有权：把 `QListWidgetItem` 加入列表后，列表负责销毁它；`takeItem()` 会把所有权取回来，调用者要自己删除或重新插入。

## 2. 类说明

- 头文件：`#include <QListWidget>`
- 模块：`Qt6::Widgets`
- 继承自：`QListView`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 `QListView` 的选择、滚动、拖放、编辑和布局能力，同时把 model/index 操作包装成 item/row 操作。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QListWidget(parent)` | 创建空列表控件。 |
| `addItem(item)` / `addItem(text)` | 在末尾添加一个 item 或文本项。 |
| `addItems(labels)` | 批量添加文本项。 |
| `insertItem(row, item/text)` / `insertItems()` | 在指定行插入。 |
| `takeItem(row)` | 移除并返回 item，调用者获得所有权。 |
| `clear()` | 清空并删除所有 item。 |
| `count()` | item 数量，包括隐藏项。 |
| `item(row)` / `row(item)` | 行号与 item 互查。 |
| `itemAt(point)` | 根据视口坐标找 item。 |
| `visualItemRect(item)` | 获取 item 的可视矩形。 |
| `currentItem()` / `setCurrentItem()` | 读取或设置当前 item。 |
| `currentRow()` / `setCurrentRow()` | 读取或设置当前行。 |
| `selectedItems()` | 获取所有选中 item。 |
| `findItems(text, flags)` | 按文本和匹配规则查找。 |
| `editItem(item)` | 进入 item 编辑状态。 |
| `openPersistentEditor()` / `closePersistentEditor()` | 长期开启或关闭 item 编辑器。 |
| `setItemWidget()` / `itemWidget()` | 给 item 放置真实 QWidget；仅适合少量静态控件。 |
| `removeItemWidget()` | 移除 item 上的控件。 |
| `setSortingEnabled()` / `sortItems()` | 启用自动排序或立即排序。 |
| `indexFromItem()` / `itemFromIndex()` | 与模型索引互转，连接 model/view API 时使用。 |
| `scrollToItem()` | 滚动到指定 item。 |
| `setSupportedDragActions()` / `supportedDragActions()` | Qt 6.10 起设置列表可发起的拖拽动作。 |
| `items(mimeData)` | 从 MIME 数据中解析列表 item。 |
| `mimeData()` / `mimeTypes()` | 子类化自定义拖拽导出的数据。 |
| `dropMimeData()` / `supportedDropActions()` | 子类化自定义 drop 接收和支持动作。 |
| `currentItemChanged()` / `currentRowChanged()` / `currentTextChanged()` | 当前项变化信号。 |
| `itemClicked()` / `itemDoubleClicked()` / `itemActivated()` | 常用用户操作信号。 |
| `itemChanged()` | item 数据变化信号。 |
| `itemSelectionChanged()` | 选择集合变化。 |

## 4. 关键用法

### 适合“小而直接”的列表

`QListWidget` 的优势是快：`addItem("Open")` 就能显示，item 可设置图标、文本、勾选状态、用户数据和 flags。设置页、工具箱、颜色列表、最近文件这类数据通常不值得单独写 model。

但它不适合把业务数据库完整塞进 UI。item 不是领域对象，最多保存轻量 id 或指针标识；真正的数据仍应在业务层。否则一旦需要搜索、分页、权限过滤、多视图共享，就会难以迁移。

### 排序时机要小心

开启 `setSortingEnabled(true)` 后，插入 item 可能立刻改变行号。若你正在按 row 批量填充并保存行号映射，排序会让映射失效。常见做法是先关闭排序，填充完成后再 `sortItems()` 或重新开启排序。

自定义排序通常通过继承 `QListWidgetItem` 并重写比较逻辑完成。不要在排序后继续假设“插入的第 n 个就是第 n 行”。

### item widget 不是列表项渲染的万能方案

`setItemWidget()` 适合少量静态展示，例如某个 item 上放一个进度条或状态标签。若每一行都要复杂外观，推荐使用 delegate；若每一行都有按钮且数量很多，也应考虑 delegate 加点击命中，而不是创建大量 QWidget。

### 拖放和 MIME

便捷控件也支持拖放。`mimeData()` 决定拖出去带什么数据，`dropMimeData()` 决定放进来怎么创建 item。跨应用拖放时，不要只依赖 Qt 内部格式，最好同时提供文本、URL 或自定义 MIME 类型。

## 5. 常见坑与经验

- 同一个 `QListWidgetItem` 只能加入一个列表一次，重复加入行为不可靠。
- `takeItem()` 不删除 item；如果不用它，记得释放。
- `itemChanged()` 对程序修改也会触发。批量更新时可临时阻断信号或用状态位避免递归。
- `currentItem` 不等于 selected items；多选场景要用 `selectedItems()`。
- 大量数据、复杂过滤和共享数据源时，尽早切换到 `QListView` + model。
