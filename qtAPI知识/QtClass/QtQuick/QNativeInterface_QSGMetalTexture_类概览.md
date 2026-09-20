# QNativeInterface::QSGMetalTexture：把 MTLTexture 交给 Qt Quick 采样

> Qt 6.11.1 | `#include <QSGTexture>` | CMake: `Qt6::Quick` | Apple 平台 / Metal 后端

`QNativeInterface::QSGMetalTexture` 是 Metal 纹理和 `QSGTexture` 之间的轻量适配层。它面向已经从 AVFoundation、Metal 渲染管线或平台 API 获得 `MTLTexture` 的应用，避免为了在 QML 中显示它而经过 CPU 图像中转。

## 包装平台纹理

在 Objective-C++ 编译单元中，`nativeTexture()` 和 `fromNative()` 使用 `id<MTLTexture>`；纯 C++ 公共头会把该类型表示为 opaque `id`。

```objective-c++
id<MTLTexture> sourceTexture = frame.texture;
QSGTexture *texture = QNativeInterface::QSGMetalTexture::fromNative(
    sourceTexture, window, sourceTextureSize,
    QQuickWindow::TextureHasAlphaChannel);
```

结果纹理只包装原生 Metal 对象。删除 `QSGTexture` 不会释放 `MTLTexture`；调用方必须保持原生纹理在 Quick 采样完成前有效，并按 ARC 或自己的 Metal 所有权规则管理它。

`fromNative()` 当前只支持二维 RGBA 纹理，并在 scene graph 尚未初始化时返回空。不要把窗口构造完毕误认为已经具备 scene graph 资源。

## 从 Qt 纹理取回 Metal 对象

```objective-c++
auto *native = texture->nativeInterface<
    QNativeInterface::QSGMetalTexture>();
if (native) {
    id<MTLTexture> metalTexture = native->nativeTexture();
    useInMetalEncoder(metalTexture);
}
```

查询出的对象仍由 Qt/原始提供者管理。该接口用于同一渲染系统内协作，不是把 scene graph 内部资源转移给其它线程或 command queue 的许可。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `fromNative(MTLTexture, window, size, options)` | 用既有 `MTLTexture` 创建包装 `QSGTexture` | 原生对象不转移所有权；只支持 2D RGBA |
| `nativeTexture()` | 返回底层 Metal texture 对象 | 使用者不应提前释放或跨上下文滥用它 |
| `QSGTexture::nativeInterface<QSGMetalTexture>()` | 查询 Metal 专用接口 | 仅当 Quick 使用 Metal 后端且纹理支持接口时有效 |
| `TextureHasAlphaChannel` | 告知 Quick 纹理的 alpha 特性 | 不会自动转换像素格式 |
| `TextureHasMipmaps` | 告知 mipmap 可用 | 源 `MTLTexture` 必须确实具备相应级别 |

## 使用边界

- 依赖 Metal 的平台和渲染后端；跨平台代码应先做后端分支。
- 资源同步与 command encoder 的使用顺序由应用和底层渲染系统协调。
- scene graph 未初始化时先处理空返回，不要继续把空 texture 交给节点。
