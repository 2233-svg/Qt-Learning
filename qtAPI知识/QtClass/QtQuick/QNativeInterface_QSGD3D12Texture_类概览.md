# QNativeInterface::QSGD3D12Texture：带资源状态的 Direct3D 12 纹理桥接

> Qt 6.11.1 | `#include <QSGTexture>` | CMake: `Qt6::Quick` | Windows / D3D12 后端

`QNativeInterface::QSGD3D12Texture` 让 Qt Quick 包装既有的 D3D12 纹理，或者从 `QSGTexture` 取回底层 `ID3D12Resource`。它和 D3D11 版本最大的不同是：D3D12 没有隐式资源状态，包装和查询必须同时处理当前 `D3D12_RESOURCE_STATES`。

这适用于视频帧、计算着色器输出或自定义 D3D12 渲染结果直接作为 QML 图元纹理的场景。

## resourceState 是正确性条件

```cpp
QSGTexture *texture = QNativeInterface::QSGD3D12Texture::fromNative(
    resource,
    int(D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE),
    window,
    size);
```

`resourceState` 必须如实表示调用时该资源的**当前**状态。Qt Quick 需要据此安排它后续的使用；把“希望它将要处于的状态”或一个过时状态传进去，会得到验证错误、错误采样或 GPU 同步问题。

该函数从 Qt 6.6 起提供，且必须在 scene graph 的渲染线程调用。scene graph 尚未初始化仍会返回 `nullptr`。

## 反向访问与所有权

```cpp
auto *native = texture->nativeInterface<
    QNativeInterface::QSGD3D12Texture>();
if (native) {
    void *resource = native->nativeTexture(); // ID3D12Resource *
    const int state = native->nativeResourceState();
    Q_UNUSED(resource);
    Q_UNUSED(state);
}
```

`nativeTexture()` 返回 `ID3D12Resource *` 的 opaque 表示，`nativeResourceState()` 返回其当前 D3D12 state。接口只让你观察和对接；不要借此改变资源状态却不和 Qt Quick 的渲染节奏同步。

与其它 `fromNative()` 一样，返回的 `QSGTexture` 由调用方销毁，底层 resource 仍由调用方拥有。当前仅支持二维 RGBA 纹理；创建选项中仅 alpha 与 mipmap 标志会被考虑。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `fromNative(texture, resourceState, window, size, options)` | 包装一个 `ID3D12Resource` | Qt 6.6 起；必须在 scene graph 渲染线程调用 |
| `resourceState` 参数 | 声明原生资源的当前 D3D12 状态 | 传错状态会破坏资源转换和同步 |
| `nativeTexture()` | 取得 `ID3D12Resource *` | 不增加所有权，也不授权任意改变资源状态 |
| `nativeResourceState()` | 查询 texture 当前 D3D12 state | 仅用于与外部命令列表协调，不能代替同步 |
| `QSGTexture::nativeInterface<QSGD3D12Texture>()` | 查询 D3D12 特定接口 | 非 D3D12 后端或不支持时返回空 |

## 使用边界

- `fromNative()` 返回空通常意味着 scene graph 尚未初始化，不是资源自动被接管。
- wrapper 和底层纹理生命周期独立；资源不能先于 Qt 使用结束释放。
- 不要假定它可包装任意 dimension、格式或 multi-plane D3D12 资源。
