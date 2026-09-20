# QColumnView

> Qt 6.11.1 · Qt Widgets · 来自 `QColumnView`

## 1. 先建立直觉

`QColumnView` 用多列并排方式浏览层级模型：左列选中父节点，右列显示它的子节点，再右边继续显示下一层。它很像 macOS Finder 的 column view，适合文件夹、分类、层级资源库、对象树的横向导航。

它继承 `QAbstractItemView`，但内部会为每一层创建一个列视图。你关心的不是表格列，而是“层级路径上的每一级”。选中某项后，下一列展示该项的 children，预览列可展示当前项详情。

## 2. 类说明

- 头文件：`#include <QColumnView>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemView`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它适用于层级 model。平面列表用 `QListView` 更直接，多列属性表用 `QTreeView` 或 `QTableView`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QColumnView(parent)` | 创建列视图。 |
| `setModel()` | 绑定层级模型。 |
| `setRootIndex()` | 设置浏览起点。 |
| `columnWidths()` / `setColumnWidths()` | 读取或设置各级列宽。 |
| `setResizeGripsVisible()` / `resizeGripsVisible()` | 是否显示列宽拖拽柄。 |
| `setPreviewWidget()` / `previewWidget()` | 设置或读取预览区域 widget。 |
| `setPreviewColumnVisible()` / `isPreviewColumnVisible()` | Qt 6.11 起控制预览列是否可见。 |
| `updatePreviewWidget(index)` | 当前项变化时请求更新预览内容。 |
| `createColumn(index)` | 子类化创建某一级使用的 item view。 |
| `initializeColumn(column)` | 把当前视图的通用行为复制到新列。 |
| `indexAt()` / `visualRect()` | 坐标和模型索引互转。 |
| `scrollTo()` | 滚动到指定索引对应的层级路径。 |
| `selectAll()` | 选择当前列中的项目。 |
| `sizeHint()` | 返回推荐尺寸。 |

## 4. 关键用法

### 它浏览的是层级，不是字段列

`QColumnView` 的每一列代表树的一层，而不是模型的某个 column 字段。模型仍然可以有多列数据，但导航的核心是 parent/child。若你想显示“名称、大小、日期”这种字段列，`QTreeView` 更合适。

### 预览列用于详情，而不是下一层数据

`setPreviewWidget()` 可以在最右侧显示当前项详情，如文件预览、属性摘要、说明面板。监听 `updatePreviewWidget(index)`，根据 index 更新预览 widget。Qt 6.11 的 `previewColumnVisible` 可以在不销毁预览 widget 的情况下隐藏显示预览列。

### 自定义每一级视图

重写 `createColumn()` 可以返回自定义 `QAbstractItemView`，例如使用特定 delegate、图标尺寸或选择行为。创建后调用 `initializeColumn()` 能继承主视图的常用设置，避免每列行为不一致。

### 列宽是用户体验的一部分

`columnWidths()` 适合保存用户调整后的列宽，下次用 `setColumnWidths()` 恢复。层级导航里列宽太窄会让路径判断困难，太宽又浪费横向空间；通常给名称列留够文本宽度，预览列单独控制。

## 5. 常见坑与经验

- 不适合平面数据，也不适合传统多字段表格。
- 预览 widget 由 column view 接管显示关系，但内容更新仍需你响应信号。
- 自定义 column view 时要保持 selection model 和 root index 协作，否则层级联动会断。
- 大型层级模型仍应靠 model 的懒加载，而不是一次性展开所有数据。
- 视图坐标依然是 viewport 坐标，命中测试不要用全局坐标。
