# QAbstractItemDelegate

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractItemDelegate`

## 1. 先建立直觉

`QAbstractItemDelegate` 是模型/视图体系中“单元格如何显示、如何编辑”的抽象协议。view 负责滚动和选择，model 负责数据，delegate 负责把某个 `QModelIndex` 画出来，并在需要时创建编辑器把用户输入写回 model。

你通常不会直接使用它，而是继承 `QStyledItemDelegate`。只有在需要完全自定义绘制与编辑协议，或构建自己的 delegate 基类时，才直接面对 `QAbstractItemDelegate`。

## 2. 类说明

- 头文件：`#include <QAbstractItemDelegate>`
- 模块：`Qt6::Widgets`
- 继承自：`QObject`
- 直接派生类：`QItemDelegate`、`QStyledItemDelegate`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

delegate 是 QObject，可由 view 或其他对象管理生命周期。它不是 item，也不保存每个单元格的数据。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QAbstractItemDelegate(parent)` | 创建 delegate 基对象。 |
| `paint()` | 纯虚函数；绘制指定 index 的可视内容。 |
| `sizeHint()` | 纯虚函数；返回指定 index 的推荐尺寸。 |
| `createEditor()` | 创建编辑器 QWidget；默认不创建。 |
| `setEditorData()` | 把 model 数据填入编辑器。 |
| `setModelData()` | 把编辑器数据写回 model。 |
| `updateEditorGeometry()` | 根据 item 区域调整编辑器位置。 |
| `destroyEditor()` | 销毁编辑器，默认 `deleteLater()`。 |
| `editorEvent()` | 处理发生在 item 上的鼠标/键盘事件，如勾选框点击。 |
| `helpEvent()` | 处理 tooltip、What's This 等帮助事件。 |
| `handleEditorEvent()` | Qt 6.10 起用于编辑器内 Tab/Enter/Esc 等标准提交关闭逻辑。 |
| `commitData(editor)` | delegate 发出，要求 view 把编辑器数据提交到 model。 |
| `closeEditor(editor, hint)` | delegate 发出，要求 view 关闭编辑器，并可提示下一步编辑行为。 |
| `sizeHintChanged(index)` | 尺寸建议变化时发出，要求 view 重新布局。 |
| `EndEditHint` | 关闭编辑器后的提示：编辑下一项、上一项、提交/回滚模型缓存等。 |

## 4. 关键用法

### 绘制和编辑是两条路径

`paint()` 负责非编辑状态下的显示；`createEditor()`、`setEditorData()`、`setModelData()` 负责进入编辑后的 QWidget。很多自定义 delegate 只需要重写绘制，不需要创建编辑器；反过来，如果只是想换一个编辑控件，通常不用完全重写绘制。

### 提交数据靠信号协作

编辑器里的值改变后，delegate 通常发出 `commitData(editor)`，再发出 `closeEditor(editor, hint)`。view 收到后调用 `setModelData()` 写回模型。直接在 editor 的槽里改 model 也能做，但会绕过标准编辑生命周期，容易破坏 Tab 到下一格、Esc 取消等行为。

### `EndEditHint` 是体验细节

表格录入中按 Enter 跳到下一行、按 Shift+Tab 回上一格、编辑完成后提交缓存，都可以通过 `closeEditor()` 的 hint 表达。自定义 view 可以忽略这些 hint，但标准 item view 会尽量配合。

### `editorEvent()` 适合无编辑器交互

复选框点击、星级评分、按钮式图标这类交互不一定要创建 QWidget 编辑器。可以在 `editorEvent()` 中根据事件位置修改 model 数据，再返回 `true`。这样比给每个单元格塞真实控件更轻。

## 5. 常见坑与经验

- `paint()` 中不要修改 model；绘制函数可能被频繁调用。
- 自定义绘制时要考虑 `option.state` 中的选中、禁用、焦点、悬停状态。
- 创建的 editor 应该以传入的 `parent` 为父对象，并具备合适焦点策略。
- 尺寸变化后必须发 `sizeHintChanged()`，否则 view 不一定重新计算布局。
- `QModelIndex` 可能失效，不要在 delegate 里长期保存普通 index。
