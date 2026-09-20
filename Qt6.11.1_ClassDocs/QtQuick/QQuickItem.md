# QQuickItem
> Qt 6.11.1 · Qt Quick · 来自 `QQuickItem`

## 作用定位
`QQuickItem` 是 Qt Quick 里绝大多数可见对象的 C++ 基类。它不等于一个“控件”：它定义的是视觉树中的一个节点，负责几何、可见性、焦点、输入和与 Scene Graph 节点的衔接。QML 的 `Item`、自定义 QML 可视类型，以及 `Rectangle` 等视觉项最终都建立在这套模型上。

## 类说明
继承 `QQuickItem` 时，通常让 QML 负责组合和绑定，让 C++ 只承载确实需要原生实现的交互、数据桥接或高性能绘制。仅仅为了写几个属性而继承它，往往不如组合现有 QML 类型清晰。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(app PRIVATE Qt6::Quick)
```

## API 速查
| API | 是做什么的 |
|---|---|
| `setX()` / `setY()` / `setWidth()` / `setHeight()` | 设置项在父项坐标系中的位置和大小。|
| `setImplicitWidth()` / `setImplicitHeight()` | 提供布局的理想尺寸；不直接强制实际尺寸。|
| `setParentItem()` / `childItems()` | 建立或检查视觉父子关系；不同于 QObject 的所有权父子关系。|
| `setVisible()` / `setEnabled()` / `setOpacity()` | 控制显示、交互资格和整体透明度。|
| `setFocus()` / `forceActiveFocus()` | 请求键盘焦点；后者会沿焦点域强制激活。|
| `setClip(true)` | 裁剪超出自身边界的子项，代价是额外渲染状态。|
| `contains()` / `childAt()` | 命中测试；可重写 `contains()` 改变交互形状。|
| `grabToImage()` | 异步抓取当前项为图像，结果由 `QQuickItemGrabResult` 返回。|
| `update()` | 请求下一帧更新 Scene Graph，不是立即绘制。|
| `updatePaintNode()` | 在渲染同步阶段创建或更新 `QSGNode` 树。|
| `geometryChange()` / `itemChange()` | 监听尺寸、父项、场景等结构性变化。|
| `setAcceptHoverEvents()` / `setAcceptedMouseButtons()` | 声明希望接收哪些鼠标输入。|

## 使用场景
### 自定义可视项
实现一个数据可视化、仪表盘指针或特殊命中区域时，继承 `QQuickItem` 并在 `updatePaintNode()` 中维护节点。应复用传入的旧节点，避免每帧重新分配整个节点树。

```cpp
QSGNode *GaugeItem::updatePaintNode(QSGNode *oldNode,
                                    UpdatePaintNodeData *)
{
    auto *node = static_cast<QSGSimpleRectNode *>(oldNode);
    if (!node)
        node = new QSGSimpleRectNode;
    node->setRect(boundingRect());
    node->setColor(m_color);
    return node;
}
```

### 和 QML 布局协作
`implicitWidth`、`implicitHeight` 是“建议大小”。在 `RowLayout`、`ColumnLayout` 中，用它们表达内容自然尺寸；直接改 `width`/`height` 则可能与布局管理产生竞争。

## 常见坑与经验
- `parentItem` 管的是画面坐标和裁剪层级，`QObject::parent()` 管生命周期；两者经常一致，但不应把它们当成同一件事。
- `updatePaintNode()` 可能运行在渲染线程。不要在那里读取普通 GUI 对象、创建 `QPixmap`，或修改 QML 属性；把所需状态在 GUI 线程提前保存为可安全读取的数据。
- 对宽高存在 QML 绑定时，C++ 直接 `setWidth()` 会移除该绑定。更适合暴露业务属性，再由 QML 绑定宽高。
- `visible: false` 会影响自身和子树的渲染；`opacity: 0` 仍可能保留输入和渲染工作。需要禁用交互时应同时考虑 `enabled`。

## 知识点覆盖
视觉树与 QObject 树、坐标系统和隐式尺寸、焦点域、鼠标/触摸命中、QML 属性绑定、Scene Graph 同步阶段、GUI 线程与渲染线程边界。
