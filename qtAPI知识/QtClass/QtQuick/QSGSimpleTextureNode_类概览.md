# QSGSimpleTextureNode：默认后端中的单纹理四边形

> Qt 6.11.1 · `#include <QSGSimpleTextureNode>` · 模块：`Qt6::Quick` · 继承：`QSGGeometryNode`

`QSGSimpleTextureNode` 将一张 `QSGTexture` 映射到一个矩形，并提供源区域、滤波和纹理坐标翻转控制。它适合快速展示一整张或一块纹理，但后端适配能力有限。

## 实际场景

一个自定义预览 Item 想显示 `QQuickWindow::createTextureFromImage()` 创建的纹理时，可以保留节点并只调整目标尺寸、裁剪源区或采样模式。`rect` 是 Item 本地坐标里的目标区域，`sourceRect` 是纹理坐标中的取样区域。

`TextureCoordinatesTransform` 尤其用于接入第三方 OpenGL 渲染到纹理的结果：OpenGL 的 Y 轴方向与 Qt Quick 常见纹理方向不同，选择相应翻转模式才能避免画面上下颠倒。

## 必须注意的边界

该便利类只保证在默认或软件场景图后端可用。可移植实现应使用 `QQuickWindow::createImageNode()` 获得 `QSGImageNode`。

默认不拥有传入的纹理。若调用 `setOwnsTexture(true)`，节点析构或替换纹理时会删除该纹理；不要同时由其他对象持有并释放它。纹理以及节点都属于场景图资源，必须在渲染线程生命周期内使用。

## API 速查表

| API | 语义与边界 |
|---|---|
| `setTexture(QSGTexture *texture)` / `texture()` | 绑定或取得纹理；默认不转移所有权。 |
| `setOwnsTexture(bool owns)` / `ownsTexture()` | 控制节点是否销毁纹理；启用后不得重复释放同一纹理。 |
| `setRect(const QRectF &rect)` / `rect()` | 设置或取得屏幕目标区域。 |
| `setRect(x, y, width, height)` | 设置目标区域的便捷重载。 |
| `setSourceRect(const QRectF &rect)` / `sourceRect()` | 设置或取得纹理采样区域。 |
| `setSourceRect(x, y, width, height)` | 设置源区域的便捷重载。 |
| `setFiltering(QSGTexture::Filtering)` / `filtering()` | 设置或取得纹理放大缩小时的采样方式。 |
| `setTextureCoordinatesTransform(mode)` / `textureCoordinatesTransform()` | 设置或取得纹理坐标变换，常用于纠正上下翻转。 |
| `QQuickWindow::createImageNode()` | 需要跨后端支持时优先使用的替代入口。 |
