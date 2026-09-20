# QSGDynamicTexture：由 scene graph 阶段显式刷新的纹理基类

> Qt 6.11.1 | `#include <QSGDynamicTexture>` | CMake: `Qt6::Quick`

`QSGDynamicTexture` 是内容会变化的 `QSGTexture` 抽象基类，例如持续更新的离屏渲染结果、视频帧或外部生产者写入的图像。它解决的问题不是“通知 QML 刷新”，而是让 texture 在 scene graph 正确阶段把最新像素同步到 GPU 可采样资源。

派生类实现 `updateTexture()`，再由使用者在 `QQuickItem::updatePaintNode()` 或 node 的 `preprocess()` 中显式触发。它不是定时器：Qt Quick 不会因为类型名称含 dynamic 而自动刷新内容。

## 更新应发生在 scene graph 生命周期内

```cpp
QSGNode *VideoItem::updatePaintNode(QSGNode *oldNode, UpdatePaintNodeData *)
{
    auto *node = static_cast<MyTextureNode *>(oldNode);
    node->dynamicTexture()->updateTexture();
    return node;
}
```

`updateTexture()` 返回 true 表示纹理内容确实变了，false 表示不需要进一步更新。调用时机通常是同步阶段的 `updatePaintNode()`，或启用 `QSGNode::UsePreprocess` 后的 `preprocess()`；在任意 GUI 回调、工作线程或渲染循环之外强行调用会破坏 scene graph 同步假设，官方明确不建议这么做。

外部生产线程可以准备 CPU 数据或发布帧序号，但 GPU 上传和 Qt Quick texture 状态变化仍应在渲染线程完成。使用单独的锁、队列或无锁交换把“新帧可用”传到 node，再在上述阶段消费。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGDynamicTexture` | 动态内容纹理的抽象基类 | 继承 `QSGTexture`；所有 QSG 操作限 scene graph 渲染线程 |
| `updateTexture()` | 把最新内容更新到此纹理，返回是否变化 | 纯虚；通常只在 `updatePaintNode()` 或 `preprocess()` 调用 |
| 返回 `true` | 本次更新改变了纹理内容 | 调用方可据此进行后续依赖更新 |
| 返回 `false` | 没有新内容或无需上传 | 不是错误码，表示维持现有纹理内容 |
| `QSGNode::preprocess()` | 可放置连续动态更新的节点预处理点 | 需启用 `UsePreprocess`；仍运行在 scene graph 线程 |
