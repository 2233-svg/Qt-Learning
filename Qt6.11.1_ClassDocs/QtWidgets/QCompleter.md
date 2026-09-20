# QCompleter

> Qt 6.11.1 · Qt Widgets · 来自 `QCompleter`

## 1. 先建立直觉

`QCompleter` 给输入控件提供自动补全。它可以基于 `QStringList`，也可以基于任意 `QAbstractItemModel`，并通过弹窗、内联文本或未过滤弹窗把候选项展示给用户。

典型场景包括命令输入、路径输入、搜索框、联系人选择、标签输入、表单字段建议。它本身不保存业务数据，真正的候选来源是 model；它负责根据前缀、列、角色、大小写和匹配方式筛选候选。

## 2. 类说明

- 头文件：`#include <QCompleter>`
- 模块：`Qt6::Widgets`
- 继承自：`QObject`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

常与 `QLineEdit`、`QComboBox`、自定义输入控件配合。对 tree model 可通过重写 `splitPath()` 和 `pathFromIndex()` 定制层级补全。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QCompleter(parent)` | 创建空 completer，稍后设置模型。 |
| `QCompleter(model, parent)` | 基于模型创建 completer。 |
| `QCompleter(QStringList, parent)` | 基于字符串列表创建 completer。 |
| `setWidget()` / `widget()` | 绑定到输入控件。 |
| `setModel()` / `model()` | 设置候选数据模型。 |
| `completionModel()` | 获取经过当前前缀过滤后的候选模型。 |
| `setCompletionPrefix()` / `completionPrefix()` | 设置或读取当前补全前缀。 |
| `completionCount()` | 当前候选数量；大模型中避免高频调用。 |
| `setCurrentRow()` / `currentRow()` | 在候选中选择某一行。 |
| `currentCompletion()` / `currentIndex()` | 当前候选文本或模型索引。 |
| `setCompletionColumn()` / `completionColumn()` | 指定用于匹配和显示的列。 |
| `setCompletionRole()` / `completionRole()` | 指定用于匹配的 model role。 |
| `setCaseSensitivity()` / `caseSensitivity()` | 控制大小写敏感性。 |
| `setFilterMode()` / `filterMode()` | 控制 starts-with、contains、ends-with 匹配。 |
| `setCompletionMode()` / `completionMode()` | 弹窗、内联、未过滤弹窗三种呈现模式。 |
| `setModelSorting()` / `modelSorting()` | 告诉 completer 模型是否已排序，用于性能优化。 |
| `setMaxVisibleItems()` / `maxVisibleItems()` | 弹窗最多显示多少项。 |
| `setWrapAround()` / `wrapAround()` | 候选导航是否首尾循环。 |
| `setPopup()` / `popup()` | 设置自定义候选弹窗视图。 |
| `complete(rect)` | 主动显示补全弹窗，可指定矩形。 |
| `splitPath()` | 子类化拆分用户输入路径。 |
| `pathFromIndex()` | 子类化把模型索引转为插入文本。 |
| `activated(text/index)` | 用户确认某候选。 |
| `highlighted(text/index)` | 用户高亮某候选但未确认。 |

## 4. 关键用法

### 简单列表最快

`new QCompleter(QStringList{...}, parent)` 适合固定候选，如国家、命令、标签。绑定到 `QLineEdit` 后，输入框会自动使用它。候选会随前缀过滤，用户确认后文本写回控件。

候选来自业务数据时，不要每次输入都重建 completer。维护一个 model，更新 model 数据即可。

### 列和 role 决定匹配对象

模型有多列时，`completionColumn` 指定按哪列补全；同一 index 有多种 role 时，`completionRole` 指定使用哪种数据匹配。显示文本、编辑值和业务 id 可以分开保存，不必把所有内容拼成一列字符串。

### 模式影响输入体验

`PopupCompletion` 最常见，用户从列表选。`InlineCompletion` 更像浏览器地址栏，会在输入框内补齐剩余文本。`UnfilteredPopupCompletion` 会显示所有候选，只把最可能项设为当前项，适合用户需要浏览全集的场景。

### 大模型性能靠排序声明

如果模型按补全列和补全 role 升序排好，设置 `CaseSensitivelySortedModel` 或 `CaseInsensitivelySortedModel` 可让 completer 用更快的搜索。大小写敏感设置必须和排序声明匹配，否则优化不能成立。

`completionCount()` 可能迫使 completer 计算所有候选，大模型中不要每次按键都调用它更新状态栏。

### 层级补全

文件路径、命名空间、分类路径这类层级补全可重写 `splitPath()` 和 `pathFromIndex()`。前者把用户输入拆成层级片段，后者把选中的 index 拼回最终文本。

## 5. 常见坑与经验

- `filterMode` 只支持 starts-with、contains、ends-with 这类匹配；大小写用 `caseSensitivity` 控制。
- popup 是一个 `QAbstractItemView`，可以自定义成 `QTreeView`、`QTableView` 或调整 delegate。
- completer 不负责验证最终输入是否合法；用户仍可能输入候选以外的文本。
- 模型数据变化后，确认 completer 使用的列、role 和排序声明仍然正确。
- 对远程搜索建议，通常不要把网络请求塞进 completer 事件里阻塞 GUI。
