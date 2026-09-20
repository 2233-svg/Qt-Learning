# QQuickTextDocument
> Qt 6.11.1 · Qt Quick · 来自 `QQuickTextDocument`

## 作用定位
`QQuickTextDocument` 是 QML 文本编辑组件与 C++ `QTextDocument` 之间的桥梁。它让 C++ 能访问 `TextEdit` 等项背后的富文本文档。

## 类说明
主要从 QML 的 `TextDocument` 属性取得它，再调用 `textDocument()`。它不会替代 QML 文本项的选择、光标和输入法状态管理。

## API 速查
| API | 是做什么的 |
|---|---|
| `textDocument()` | 返回底层 `QTextDocument`。|
| `setTextDocument()` | 绑定另一个文档对象。|
| `modified()` | 查询文档是否存在未保存编辑。|
| `modifiedChanged()` | 文档修改状态变化通知。|

## 使用场景
用 C++ 实现统一的富文本导出、语法高亮或撤销栈管理，再把同一个 `QTextDocument` 交给 QML 编辑器显示。

## 常见坑与经验
- `QTextDocument` 的生存期必须长于正在使用它的文本项。
- 操作文档会触发 QML 文本更新；批量编辑时可暂时屏蔽高亮或合并撤销命令。
- 不要把 QML `text` 属性和外部文档内容同时当作单一事实来源。

## 知识点覆盖
富文本、文档模型、QML/C++ 桥接、修改状态、撤销与高亮。
