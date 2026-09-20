# QStyledItemDelegate

> Qt 6.11.1 · Qt Widgets · 来自 `QStyledItemDelegate`

## 1. 先建立直觉

`QStyledItemDelegate` 是现代 Qt Widgets 中最推荐的 item delegate。它使用当前 `QStyle` 绘制列表、表格、树中的项目，因此能跟随平台主题、调色板、选中态、禁用态和高 DPI 行为。

你需要自定义单元格显示、格式化文本、换编辑器、处理勾选/按钮点击时，优先从它继承。除非维护旧代码或刻意使用非 style 绘制，否则通常不选 `QItemDelegate`。

## 2. 类说明

- 头文件：`#include <QStyledItemDelegate>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemDelegate`
- 直接派生类：`QSqlRelationalDelegate`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它以 `QStyleOptionViewItem` 为中心，把 model role 转换成 style option，再交给当前 style 绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStyledItemDelegate(parent)` | 创建 style-aware delegate。 |
| `paint()` | 绘制 item，默认使用当前 `QStyle`。 |
| `sizeHint()` | 返回项目尺寸，默认参考 style 和数据 role。 |
| `displayText(value, locale)` | 把 `DisplayRole` 的 QVariant 转成显示文本。 |
| `initStyleOption()` | 按指定 index 初始化 `QStyleOptionViewItem`，自定义绘制时非常常用。 |
| `createEditor()` | 根据数据类型和 editor factory 创建编辑器。 |
| `setEditorData()` | 把 model 数据写入编辑器用户属性。 |
| `setModelData()` | 从编辑器用户属性取值写回 model。 |
| `updateEditorGeometry()` | 把编辑器放到 item 的编辑区域。 |
| `itemEditorFactory()` / `setItemEditorFactory()` | 设置按 QVariant 类型创建编辑器的工厂。 |
| `editorEvent()` | 处理 item 上的事件，如复选框点击。 |
| `eventFilter()` | 处理编辑器内提交、取消、导航等事件。 |

## 4. 关键用法

### 只改显示文本：重写 `displayText()`

数字、日期、枚举、人类可读单位这些格式化，优先重写 `displayText()`。这样能保留默认绘制、选中态、图标、勾选框、焦点框和编辑逻辑，只改变文本转换。

如果你在 model 里直接把数字转成字符串，排序、过滤、编辑和本地化都会更麻烦。让 model 保持真实类型，让 delegate 负责展示，是更干净的分工。

### 自定义绘制：先 `initStyleOption()`

重写 `paint()` 时，通常先复制 option，再调用 `initStyleOption(&opt, index)`，然后在 opt 的基础上改文本、图标、颜色或子矩形。完全手写所有状态很容易漏掉选中、禁用、RTL、hover、焦点和平台主题。

如果只是附加一点视觉元素，可以先调用基类 `paint()`，再在同一个 rect 内追加绘制。记得 `painter->save()` / `restore()`，不要污染后续项的 painter 状态。

### 自定义编辑器：四个函数成套

换编辑器通常要一起处理 `createEditor()`、`setEditorData()`、`setModelData()`、`updateEditorGeometry()`。例如用 `QComboBox` 编辑枚举：创建 combo，把当前值选中，提交时写回模型，再把 combo 放到 `option.rect`。

如果只是想让某种 QVariant 类型自动使用某种编辑器，`QItemEditorFactory` 更省力。

### editor factory 适合类型到控件的映射

`setItemEditorFactory()` 可以把 `int`、`double`、`QDate` 或自定义 user type 映射到特定编辑器。它适合全局一致的编辑体验，不适合每个 index 都有完全不同的业务规则；后者更适合在 `createEditor()` 里看 index 决定。

## 5. 常见坑与经验

- 优先继承 `QStyledItemDelegate`，它比 `QItemDelegate` 更尊重当前 style。
- `paint()` 里不要创建 QWidget；delegate 绘制应该轻量。
- 用 `option.rect` 绘制，不要假设单元格从 `(0, 0)` 开始。
- 自定义编辑器提交时要确保 model 的 flags 包含可编辑，且 `setData()` 返回成功。
- `displayText()` 不会处理无效 QVariant 的 index；别把它当成所有显示逻辑入口。
