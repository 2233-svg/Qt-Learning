# QSGNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGNode`

## 作用定位
`QSGNode` 是 Scene Graph 的树节点基类。`QQuickItem::updatePaintNode()` 返回的不是像素，而是由它组织的可渲染节点树。

## API 速查
| API | 是做什么的 |
|---|---|
| `appendChildNode()` / `insertChildNodeBefore()` | 改变子节点顺序。|
| `removeChildNode()` / `removeAllChildNodes()` | 从树中移除节点。|
| `firstChild()` / `nextSibling()` | 遍历节点树。|
| `markDirty()` | 告知渲染器节点的矩阵、材质或几何已改变。|
| `setFlag(OwnedByParent)` | 让父节点负责删除子节点。|

## 使用场景
在自定义 item 中创建稳定的节点树，更新时只替换确实变动的属性或局部节点。

## 常见坑与经验
- 节点只应在 Scene Graph 同步/渲染边界使用，不能缓存给任意 GUI 线程代码操作。
- `OwnedByParent` 决定释放责任；手动删除仍挂在树里的节点会产生悬空指针。
- 节点顺序就是绘制顺序的一部分，透明内容尤其不能随意重排。

## 知识点覆盖
保留模式渲染、节点所有权、脏标记、树遍历、渲染顺序。
