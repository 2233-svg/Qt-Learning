# QHelpContentItem：帮助目录树节点

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpContentItem>`
> 所属模块：`Qt6::Help`
> 类型：帮助目录树节点

## 它解决什么问题

`QHelpContentItem` 表示帮助系统目录树中的一个节点。节点有标题、目标 URL、父节点和子节点，`QHelpContentModel` 再把这棵树转换成 Qt Model/View 可以展示的 `QModelIndex`。

它解决的是“文档目录不是平面列表，而是需要保留章节层级和展开关系”的问题。应用一般通过模型取得节点，不直接维护节点树。

## 实际使用场景

- 从 `QHelpContentModel::contentItemAt()` 取得当前索引对应的节点。
- 在调试帮助目录时遍历父子关系，检查标题和 URL。
- 根据节点 URL 同步帮助浏览器的当前页面。
- 在自定义目录视图中读取标题、链接和层级信息。

## 所有权与构造限制

公开头文件没有提供可供应用调用的构造函数，节点由 Qt Help 内部创建并由目录模型管理。应用只能读取节点，不应 `delete` 返回的指针，也不应保存它跨越目录重建。

当 `QHelpContentModel` 重新创建目录、切换 filter 或销毁时，旧节点指针可能失效。需要长期保存目录位置时，保存 URL 或模型索引相关信息，而不是保存 `QHelpContentItem *`。

`row()` 是节点在父节点子列表中的位置；根节点没有普通父节点。`childPosition()` 只对当前节点的直接子节点有意义，传入其他分支的节点应按无效位置处理。

## 关键边界

- `child(row)` 的合法范围是 `0` 到 `childCount() - 1`，越界返回空指针。
- 叶子节点的 `childCount()` 为 0，继续访问子节点没有意义。
- `url()` 是帮助系统 URL，通常需要交给 `QHelpEngineCore::fileData()` 或帮助浏览器解析，不应当直接当作本地文件路径。
- 节点 API 是只读视图；修改目录内容应通过文档包和帮助引擎重新生成。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `~QHelpContentItem()` | 销毁目录节点。 | 节点通常由 Qt 内部管理；应用不应主动删除从模型取得的指针。 |
| `QHelpContentItem *child(int row) const` | 返回指定行的直接子节点。 | 先检查 `row` 范围；目录重建后旧指针可能失效。 |
| `int childCount() const` | 返回直接子节点数量。 | 叶子节点返回 0。 |
| `QString title() const` | 返回节点显示标题。 | 标题是目录文本，不一定等于目标页面的 HTML 标题。 |
| `QUrl url() const` | 返回节点对应的帮助 URL。 | 通常是 qthelp URL，不能盲目交给普通文件 API。 |
| `int row() const` | 返回节点在父节点子列表中的行号。 | 根节点或脱离树的节点不要假设有普通行号。 |
| `QHelpContentItem *parent() const` | 返回父节点。 | 根节点没有父节点；返回指针不转移所有权。 |
| `int childPosition(QHelpContentItem *child) const` | 查找直接子节点在当前节点下的行号。 | 只对直接子节点进行匹配；未找到时按无效位置处理。 |

## 一句话总结

`QHelpContentItem` 是由 Qt 管理的只读目录节点；用它读取标题、URL 和父子关系，不要自行构造、删除或长期缓存指针。
