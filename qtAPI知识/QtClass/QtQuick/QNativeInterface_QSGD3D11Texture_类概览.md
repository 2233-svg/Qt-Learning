# QNativeInterface::QSGD3D11Texture：在 Qt Quick 与 Direct3D 11 纹理之间互操作

> Qt 6.11.1 | `#include <QSGTexture>` | CMake: `Qt6::Quick` | Windows / D3D11 后端

`QNativeInterface::QSGD3D11Texture` 是 `QSGTexture` 的后端专用原生接口。它解决的场景是：应用已经有 `ID3D11Texture2D`，例如视频解码器、采集卡或自有 D3D 渲染器产出的纹理，怎样让 Qt Quick 直接采样它，而不先拷贝回 CPU 内存再重新上传。

## 两个方向的互操作

已有原生纹理时，用 `fromNative()` 生成供 scene graph 使用的 `QSGTexture`：

```cpp
QSGTexture *texture = QNativeInterface::QSGD3D11Texture::fromNative(
    d3dTexture, window, pixelSize,
    QQuickWindow::TextureHasAlphaChannel);
if (!texture)
    return; // scene graph 尚未初始化
```

反向取得一个 Qt Quick 纹理的 D3D 对象时，在渲染阶段查询原生接口：

```cpp
auto *native = texture->nativeInterface<
    QNativeInterface::QSGD3D11Texture>();
if (native)
    void *handle = native->nativeTexture(); // ID3D11Texture2D *
```

`void *` 只是为了不在公共 Qt 头中暴露 D3D 头文件；实际对象是 `ID3D11Texture2D *`。

## 所有权和时序

`fromNative()` 只包装原生对象，不接管它。调用方删除返回的 `QSGTexture`，但这不会释放 `ID3D11Texture2D`；原生纹理必须至少存活到 Qt Quick 不再采样它为止。

函数要求 scene graph 已初始化，过早调用会返回 `nullptr`。实践中应在场景图渲染相关回调或确认 `QQuickWindow` 完成初始化的时机创建，而不是窗口刚构造时。

当前包装只适用于二维 RGBA 纹理。`CreateTextureOptions` 中只有 `TextureHasAlphaChannel` 和 `TextureHasMipmaps` 会生效，其他选项不应被当成 D3D11 资源创建参数。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `fromNative(void *, QQuickWindow *, QSize, options)` | 将 `ID3D11Texture2D *` 包装成 `QSGTexture` | scene graph 未初始化时返回空；只支持 2D RGBA |
| `nativeTexture()` | 取得底层 `ID3D11Texture2D` 的 opaque 指针 | 不转移引用计数或所有权 |
| `QSGTexture::nativeInterface<QSGD3D11Texture>()` | 从 Qt 纹理查询 D3D11 接口 | 当前渲染后端不匹配时可能返回空 |
| `TextureHasAlphaChannel` | 标注包装纹理含 alpha | 仅是创建选项之一，不会改变源纹理格式 |
| `TextureHasMipmaps` | 标注纹理带 mipmap | 源资源实际必须满足相应采样需求 |

## 使用边界

- 确保 Qt Quick 和原生渲染代码使用兼容的 D3D11 device / 资源同步策略。
- 不要在 GUI 线程任意时刻改写正在被 scene graph 采样的纹理；同步由应用负责。
- 只在 Windows 可用，且项目实际选择 D3D11 scene graph 后端时才有意义。
