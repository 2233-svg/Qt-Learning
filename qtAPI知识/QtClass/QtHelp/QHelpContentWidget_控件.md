# QHelpContentWidget：帮助目录树控件

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpContentWidget>`
> 所属模块：`Qt6::Help`
> 继承：`QTreeView`

## 它解决什么问题

`QHelpContentWidget` 是 Qt Help 提供的目录树视图。它把 `QHelpContentModel` 的章节层级显示成可展开树，并在用户激活某个目录项时发出链接信号。应用只需把信号接到帮助浏览器或文档查看器，就能完成“左侧目录、右侧页面”的常见帮助界面。

## 实际使用场景

- 直接使用 `QHelpEngine::contentWidget()` 作为帮助窗口的目录栏。
- 将 `linkActivated` 连接到 `QTextBrowser::setSource()` 或自定义文档导航函数。
- 通过 `indexOf()` 根据当前页面 URL 定位并选中目录项。
- 继承 `QTreeView` 的展开、选择、键盘导航和样式能力调整目录体验。

## 所有权与模型关系

构造函数是私有的，控件由 `QHelpEngine` 创建。返回的控件由引擎管理，应用应把它作为普通 QWidget 放入布局，但不要手动删除或重复设置不匹配的目录模型。

控件会与引擎内部的 `QHelpContentModel` 协作。目录异步重建时，URL 到索引的对应关系可能短暂变化；在 `contentsCreated()` 之后再调用 `indexOf()` 更可靠。

## `indexOf()` 与链接激活

`indexOf(link)` 用帮助 URL 在目录中查找对应索引。找不到时返回无效 `QModelIndex`。同一个页面可能没有目录项，或者一个页面有多个目录节点，因此不能把“找不到”解释为文档不存在。

用户激活目录项后，`linkActivated` 提供目标 URL。该信号只负责通知，不会自动打开页面；应用需要检查 URL、处理内部 qthelp 地址，并决定是否允许外部 scheme。

## 常见误区

- 将 `QHelpContentWidget` 当作独立可构造控件使用。
- 把 `linkActivated` 当成已经完成导航；实际页面切换仍需应用实现。
- 在目录生成过程中保存旧索引，切换 filter 后继续使用。
- 不检查 URL scheme 就把帮助链接交给外部浏览器。
- 跨线程更新控件或在没有 GUI 事件循环时等待目录完成。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QModelIndex indexOf(const QUrl &link)` | 查找与帮助 URL 对应的目录索引。 | 找不到时返回无效索引；目录重建完成后再查询更可靠。 |
| `[signal] void linkActivated(const QUrl &link)` | 用户激活目录项时发出目标 URL。 | 不会自动导航；应用应自行处理 qthelp、file 和外部 URL。 |
| `QTreeView::setModel(QAbstractItemModel *)` | 设置目录模型。 | 通常使用引擎提供的 `contentModel()`，不要混用不对应的模型。 |
| `QAbstractItemView::currentIndex()` | 读取当前选中的目录项。 | 目录重建后索引可能失效，必要时根据 URL 重新定位。 |
| `QAbstractItemView::setCurrentIndex(const QModelIndex &)` | 选中指定目录索引。 | 传入的索引必须属于当前控件使用的模型。 |
| `QTreeView::expand(const QModelIndex &)` | 展开某个目录节点。 | 只对当前模型中的有效父节点有意义。 |
| `QTreeView::collapse(const QModelIndex &)` | 折叠某个目录节点。 | 不会改变帮助数据，只改变视图状态。 |

## 一句话总结

`QHelpContentWidget` 负责展示和发出目录链接；模型由 `QHelpEngine` 提供，页面真正打开与 URL 安全策略由应用决定。
