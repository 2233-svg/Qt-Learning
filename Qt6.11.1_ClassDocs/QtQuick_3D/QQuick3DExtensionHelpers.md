# QQuick3DExtensionHelpers
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DExtensionHelpers`

## 1. 先建立直觉

`QQuick3DExtensionHelpers` 是 QML/Quick 3D 对象侧扩展的辅助函数集合。它位于 `QQuick3DObject` 和底层渲染对象之间，帮助扩展把 QML 属性同步到渲染图对象。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DExtensionHelpers`，属于 Qt Quick 3D 模块，用于辅助实现 Quick 3D C++ 扩展对象。

它与 `QSSGRenderExtensionHelpers` 的区别在于：一个偏 QML/对象同步侧，一个偏渲染执行侧。

## 3. API 速查

| API 类别 | 用来做什么 |
| --- | --- |
| spatial node 同步辅助 | 创建/更新底层 render graph object。 |
| 属性同步辅助 | 把 QML 对象状态传给渲染对象。 |
| 扩展对象桥接 | 连接 QQuick3DObject 与 QSSG* 渲染对象。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 写 QQuick3DRenderExtension 派生类 | 简化 updateSpatialNode。 |
| 暴露 C++ 扩展到 QML | 让 QML 属性进入渲染线程对象。 |
| 维护自定义 Quick 3D 对象 | 处理对象/渲染节点生命周期。 |

## 5. 常见坑与经验

同步 helper 不等于线程安全万能胶。GUI 线程对象和渲染线程对象仍要遵守 Quick scene graph 的同步阶段规则。

不要在同步阶段做大规模资源创建或阻塞 IO。同步阶段拖慢会直接影响帧率。

## 6. 知识点覆盖

- QML 对象侧扩展 helper。
- spatial node 同步。
- QQuick3DObject 到 QSSG 渲染对象的桥接。
