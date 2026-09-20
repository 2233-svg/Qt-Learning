# QItemDelegate

> Qt 6.11.1 · Qt Widgets · 来自 `QItemDelegate`

## 1. 先建立直觉

`QItemDelegate` 是较早的 item delegate 实现，负责在模型/视图中绘制和编辑单元格。现代 Qt Widgets 项目通常优先使用 `QStyledItemDelegate`，因为后者更完整地走当前平台 `QStyle`。

你仍会在旧代码、需要继承其 `drawDisplay()` / `drawCheck()` / `drawDecoration()` 分段绘制逻辑、或维护历史 delegate 时遇到它。新代码如果没有明确理由，选 `QStyledItemDelegate` 更自然。

## 2. 类说明

- 头文件：`#include <QItemDelegate>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemDelegate`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它是 QObject，并被安装到 `QAbstractItemView` 派生视图上使用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QItemDelegate(parent)` | 创建 item delegate。 |
| `setClipping()` / `hasClipping()` | 控制绘制是否裁剪到 item 区域。 |
| `paint()` | 绘制 item。 |
| `sizeHint()` | 返回 item 推荐尺寸。 |
| `createEditor()` | 创建编辑器。 |
| `setEditorData()` | 把 model 数据填入编辑器。 |
| `setModelData()` | 把编辑器数据写回 model。 |
| `updateEditorGeometry()` | 更新编辑器几何。 |
| `itemEditorFactory()` / `setItemEditorFactory()` | 设置编辑器工厂。 |
| `drawBackground()` | 绘制背景。 |
| `drawCheck()` | 绘制复选框状态。 |
| `drawDecoration()` | 绘制图标或装饰 pixmap。 |
| `drawDisplay()` | 绘制文本。 |
| `drawFocus()` | 绘制焦点框。 |
| `editorEvent()` | 处理 item 上的交互事件。 |
| `eventFilter()` | 处理编辑器事件。 |

## 4. 关键用法

### 和 `QStyledItemDelegate` 的选择

`QStyledItemDelegate` 更适合新项目，因为它通过 style option 走平台样式；`QItemDelegate` 更适合已有代码中依赖分段绘制函数的场景。若你只是想格式化显示文本或换编辑器，不必退回 `QItemDelegate`。

### 分段绘制的价值

`drawBackground()`、`drawCheck()`、`drawDecoration()`、`drawDisplay()`、`drawFocus()` 让你能只替换某一部分绘制。例如保留默认背景和焦点，只改文本绘制；或保留文本，只改复选框外观。这是维护旧 delegate 时的主要价值。

### clipping 防止绘制越界

`setClipping(true)` 会把 painter 限制在 item 区域内，避免大图标或自定义绘制覆盖邻近单元格。关闭 clipping 只适合非常明确的视觉效果，例如跨格阴影或特殊标记；普通表格应保持开启。

### 编辑器逻辑与抽象 delegate 一致

创建编辑器、填数据、提交数据、调整几何的生命周期与 `QAbstractItemDelegate` 相同。若自定义 editor，仍应发出标准提交/关闭信号，保持 Tab、Enter、Esc 等编辑体验。

## 5. 常见坑与经验

- 新代码默认考虑 `QStyledItemDelegate`，除非你确实需要 `QItemDelegate` 的绘制分段。
- 绘制时尊重 `option.state`，否则选中和禁用状态会失真。
- 关闭 clipping 后要非常小心，不要污染相邻 item。
- 编辑器工厂只解决“类型到控件”的映射，不解决每个 index 的业务校验。
- delegate 不拥有数据；任何编辑结果都应写回 model。
