# QNativeInterface::QSGOpenGLTexture：复用 OpenGL 与外部 OES 纹理

> Qt 6.11.1 | `#include <QSGTexture>` | CMake: `Qt6::Quick` | OpenGL / OpenGL ES 后端

`QNativeInterface::QSGOpenGLTexture` 把一个已有 OpenGL texture name 包装为 `QSGTexture`，或从 Quick 纹理读回它的 `GLuint`。它最常见于共享 OpenGL 上下文中的离屏渲染、解码器输出，以及 Android 相机提供的 `GL_TEXTURE_EXTERNAL_OES` 纹理。

## 普通 2D 纹理与 External OES 不可混用

```cpp
QSGTexture *texture = QNativeInterface::QSGOpenGLTexture::fromNative(
    glTextureId, window, size);
```

这适用于常规二维 RGBA texture。相机等设备写入的 external texture 必须使用专门入口：

```cpp
QSGTexture *cameraTexture =
    QNativeInterface::QSGOpenGLTexture::fromNativeExternalOES(
        oesTextureId, window, size);
```

`fromNativeExternalOES()` 只适用于目标为 `GL_TEXTURE_EXTERNAL_OES` 的 OpenGL ES 纹理；把普通 `GL_TEXTURE_2D` 传给它或反过来包装，采样器和纹理目标不会匹配。

## 生命周期与 scene graph 时机

两个工厂函数都只包装 texture ID，不拥有 GL 原生对象。调用方负责删除返回的 `QSGTexture`，也继续负责在合适的 GL context 中删除原始 texture name。

若 scene graph 尚未初始化，函数会返回 `nullptr`。此外，调用方要保证 `GLuint` 所属的 context/share group 能被 Quick 当前 OpenGL 后端访问，并自行保证在 Quick 使用期间不重用或删除该名字。

```cpp
auto *native = texture->nativeInterface<
    QNativeInterface::QSGOpenGLTexture>();
if (native)
    const GLuint textureId = native->nativeTexture();
```

`nativeTexture()` 不会绑定纹理、改变 active unit 或提供 OpenGL state 隔离；在 scene graph 的渲染路径接入自有 GL 命令时，应完整保存和恢复应用需要的状态。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `fromNative(GLuint, window, size, options)` | 包装常规 OpenGL 2D RGBA 纹理 | scene graph 未初始化返回空；不取得 GL 对象所有权 |
| `fromNativeExternalOES(GLuint, ...)` | 包装 `GL_TEXTURE_EXTERNAL_OES` 纹理 | Qt 6.1 起；只用于 external OES，常见于相机帧 |
| `nativeTexture()` | 返回底层 OpenGL texture ID | 不绑定 texture，也不延长其 GL 生命周期 |
| `QSGTexture::nativeInterface<QSGOpenGLTexture>()` | 查询 OpenGL 专用接口 | Quick 不在 OpenGL 后端时可能没有该接口 |
| `TextureHasAlphaChannel` / `TextureHasMipmaps` | 可识别的创建选项 | 不会替换原始 texture 的实际 storage 或 target |

## 使用边界

- `fromNative()` 当前仅适用二维 RGBA；多平面视频纹理需要专门渲染路径。
- 外部纹理产生者与 Qt Quick 的 GPU 访问必须同步，不能只依赖 QML 帧刷新。
- texture ID 是 context 相关资源，跨不共享的 context 不可直接使用。
