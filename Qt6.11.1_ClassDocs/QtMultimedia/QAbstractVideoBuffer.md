# QAbstractVideoBuffer
> Qt 6.11.1 · Qt Multimedia · 来自 `QAbstractVideoBuffer`

## 作用定位

`QAbstractVideoBuffer` 是视频帧底层缓冲抽象。它隐藏一帧图像数据来自 CPU 内存、GPU 纹理、平台句柄还是自定义后端资源。大多数应用直接用 `QVideoFrame`，只有实现自定义视频缓冲时才需要理解它。

## 类说明

- 头文件：`#include <QAbstractVideoBuffer>`
- CMake：链接 `Qt6::Multimedia`
- 抽象基类

## API 速查

| API | 说明 |
| --- | --- |
| `MapMode` | 只读、只写、读写、未映射等映射模式。 |
| `map()` / `unmap()` | 派生类实现 CPU 访问映射。 |
| `format()` | 返回缓冲对应的视频帧格式。 |
| `mapMode()` | 当前映射状态。 |

## 使用场景
- 接入自定义解码器或采集后端。
- 把外部图像缓冲包装成 `QVideoFrame`。
- 控制零拷贝或平台纹理资源的生命周期。

## 常见坑与经验
- 自定义 buffer 的最大难点是生命周期和线程，而不是几个函数签名。
- map/unmap 必须严格配对，并正确报告 stride、平面和格式。
- GPU 资源不一定可映射到 CPU，必要时提供转换路径或限制用途。

## 知识点覆盖

- 视频帧底层缓冲
- 映射模式
- 自定义视频后端
- 零拷贝与资源生命周期
