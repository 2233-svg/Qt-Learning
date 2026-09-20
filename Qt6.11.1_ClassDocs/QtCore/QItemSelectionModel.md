# QItemSelectionModel
> Qt 6.11.1 · Qt Core · 来自 `QItemSelectionModel`

## 作用定位
`QItemSelectionModel` 保存一个模型当前的选中项与 current index，并通过信号通知 view、工具栏和业务控制器。

## API 速查
| API | 是做什么的 |
|---|---|
| `setCurrentIndex()` | 设置键盘/焦点意义上的当前索引。|
| `select()` | 按 `SelectionFlag` 添加、替换或移除选区。|
| `clearSelection()` | 清除选中项但保留 current。|
| `clearCurrentIndex()` | 清除 current。|
| `selectedIndexes()` | 返回选中索引列表。|
| `selectedRows()` / `selectedColumns()` | 按行或列取得选择。|
| `currentChanged()` | current 发生变化时通知。|
| `selectionChanged()` | 选区发生变化时通知。|

## 使用场景
让多个 view 共享同一模型的选择状态，或让操作面板根据当前选中行启用删除、导出和编辑按钮。

## 常见坑与经验
- current 不等于 selected；键盘移动可以只改变 current。
- 模型 reset、行删除后旧索引可能失效，应响应模型变更并重新定位业务键。
- 选择行为应明确使用 `Clear|Select|Current` 等标志，避免只调用默认行为造成旧选择残留。

## 知识点覆盖
Model/View、current、selection flags、共享选择、索引生命周期、视图交互。
