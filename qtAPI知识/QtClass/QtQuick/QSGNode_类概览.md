# QSGNode：场景图节点树的结构与失效通知

> Qt 6.11.1 · `#include <QSGNode>` · 模块：`Qt6::Quick`

`QSGNode` 是 Qt Quick 场景图的基础节点。自定义 `QQuickItem::updatePaintNode()` 时，真正交给渲染器的不是 `QPainter` 命令，而是一棵由它及其派生类组成的节点树：变换、裁剪、透明度和几何节点都附着在这棵树上。

## 它解决的问题

节点树把“要画什么”和“怎样把状态传递给子项”拆开。一个普通 `QSGNode` 本身不绘制内容，却能组织子节点；子节点的顺序同时是渲染顺序。因此它适合做稳定的容器根节点，让每一帧只更新发生变化的叶子节点，而不是重建整棵树。

典型场景是一个自定义曲线控件：根节点下放背景、曲线和标记三个几何节点。背景先加入、曲线随后、标记最后，因而标记显示在最上层。插入到已有节点前后时，同样需要把顺序当作视觉层级，而不是无关紧要的列表位置。

## 使用方式与线程边界

所有以 `QSG` 开头的类都只能在场景图渲染线程中使用。通常这意味着仅在 `updatePaintNode()`、`QQuickWindow` 的场景图同步/渲染相关信号所规定的阶段，或由这些阶段调用的代码中读写节点；不要从 GUI 线程保存一个节点指针后直接修改它。

`updatePaintNode()` 返回的旧节点可作为下一帧输入。推荐保留结构、就地更新：

```cpp
auto *root = static_cast<QSGNode *>(oldNode);
if (!root) {
    root = new QSGNode;
    auto *background = new QSGGeometryNode;
    background->setFlag(QSGNode::OwnedByParent);
    root->appendChildNode(background);
}
// 更新 background 的几何或材质，而不是每帧重新安排整棵树。
return root;
```

父子关系不等于自动内存管理。只有子节点设置了 `OwnedByParent`，父节点析构时才会删除它。节点被 `removeChildNode()` 或 `removeAllChildNodes()` 脱离树后也不会自动释放；若应用仍拥有它，应明确决定复用还是销毁。

## 脏状态与预处理

大多数高层 setter 会自行通知渲染器。例如 `appendChildNode()` 会标记层次结构改变，`QSGGeometryNode::setGeometry()` 会处理相应状态。但如果直接写入顶点缓冲或自定义节点内部数据，必须调用与变更匹配的 `markDirty()`：改顶点用 `DirtyGeometry`，改材质参数或替换材质用 `DirtyMaterial`，改变换用 `DirtyMatrix`，改透明度用 `DirtyOpacity`。错误的位掩码会让渲染器复用过期缓存。

逐帧演算可覆写 `preprocess()`，但先在节点进入场景图前设置 `UsePreprocess`。它会在每个实际渲染的帧开始前调用。不要在一个节点的 `preprocess()` 中删除含有其他预处理节点的子树，Qt 文档明确指出这可能导致崩溃。

`isSubtreeBlocked()` 为 `true` 的节点树既不渲染也不执行预处理。它更适合作为派生节点的渲染优化契约，不应用它替代业务层的可见性状态管理。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSGNode()` / `~QSGNode()` | 创建空容器；析构时仅删除带 `OwnedByParent` 的直接子节点。 |
| `appendChildNode(node)` / `prependChildNode(node)` | 追加或前插子节点；几何节点按树中顺序绘制。 |
| `insertChildNodeBefore(node, before)` / `insertChildNodeAfter(node, after)` | 在指定兄弟节点相邻位置插入；用于精确控制层级。 |
| `removeChildNode(node)` / `removeAllChildNodes()` | 只解除父子关系，不承诺删除子节点。 |
| `reparentChildNodesTo(newParent)` | 将全部子节点转交给新父节点；转移后原节点不再拥有结构。 |
| `parent()` | 返回父节点；根节点返回空指针。 |
| `firstChild()` / `lastChild()` | 取得首尾子节点，适合链式遍历。 |
| `nextSibling()` / `previousSibling()` | 取得相邻兄弟节点；节点未挂到父节点时为空。 |
| `childCount()` | 返回直接子节点数。 |
| `childAtIndex(i)` | 返回第 `i` 个子节点；内部是链表，循环按索引访问会产生不必要的遍历成本。 |
| `flags()` | 读取当前节点标志。 |
| `setFlag(flag, enabled)` | 设置单个标志；常用 `OwnedByParent`、`UsePreprocess`。 |
| `setFlags(flags, enabled)` | 批量设置或清除标志。`OwnsGeometry`、`OwnsMaterial`、`OwnsOpaqueMaterial` 只适用于相应几何节点。 |
| `markDirty(bits)` | 通知已连接的渲染器状态变更；直接修改底层数据后必须选择正确的 `DirtyState`。 |
| `preprocess()` | 渲染前每帧回调；需在入树前开启 `UsePreprocess`。 |
| `isSubtreeBlocked()` | 返回子树是否应跳过更新与渲染；可由派生类覆写。 |
| `type()` | 返回 `NodeType`，可用于检查后安全转换为对应 Qt 预定义节点类型。 |
| `DirtyMatrix` / `DirtyGeometry` / `DirtyMaterial` / `DirtyOpacity` | 分别表示矩阵、几何、材质、透明度发生变化。 |
| `DirtyNodeAdded` / `DirtyNodeRemoved` | 层次结构修改标记，通常由节点插入/移除 API 自动产生。 |
| `OwnedByParent` | 让父节点在析构时删除子节点。 |
| `UsePreprocess` | 请求渲染器在每帧绘制前调用 `preprocess()`。必须在节点入树前设置。 |
