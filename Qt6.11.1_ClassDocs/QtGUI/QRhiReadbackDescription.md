# QRhiReadbackDescription

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiReadbackDescription`

## 1. 先建立直觉

`QRhiReadbackDescription` 描述一次纹理/交换链回读的源位置：读哪张纹理、哪个 mip level、哪个 array layer，以及 Qt 6.10 起可以指定的矩形区域。它不保存结果，也不执行回读；真正排队执行的是 `QRhiResourceUpdateBatch::readBackTexture()`，结果通过 `QRhiReadbackResult` 异步返回。

如果 texture 为空，描述的是“当前 swapchain back buffer”。这适合截图当前帧，但只在基于 swapchain 的帧里有效，并且 swapchain 必须允许作为 transfer source。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- API 层级：Qt GUI 私有 API
- 使用入口：`QRhiResourceUpdateBatch::readBackTexture()`
- 读回对象：`QRhiTexture` 或当前 swapchain back buffer

读回是 GPU 到 CPU 的异步数据传输，通常跨若干帧完成。这个类只是源描述，不代表数据已经可用。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QRhiReadbackDescription()` | 创建空源描述；表示读取当前 swapchain back buffer。 |
| `QRhiReadbackDescription(QRhiTexture *texture)` | 指定读取 texture 的 level 0、layer 0。 |
| `setTexture()` / `texture()` | 设置/读取源纹理；`nullptr` 表示当前 back buffer。 |
| `setLevel()` / `level()` | 设置/读取 mip level。 |
| `setLayer()` / `layer()` | 设置/读取数组层、cubemap face 或 3D slice。 |
| `setRect()` / `rect()` | Qt 6.10 起设置/读取回读矩形；无效矩形表示全部读取。 |

## 4. 关键用法

```cpp
QRhiReadbackDescription rb(texture);
rb.setLevel(0);
rb.setLayer(0);
rb.setRect(QRect(0, 0, 256, 256));

auto *result = new QRhiReadbackResult;
result->completed = [result] {
    QByteArray bytes = result->data;
    delete result;
};

updates->readBackTexture(rb, result);
```

纹理必须以 `QRhiTexture::UsedAsTransferSource` 创建。多采样纹理不能直接读回；需要先 resolve 到普通纹理。

## 5. 使用场景

- 截取离屏渲染纹理。
- 从当前 swapchain back buffer 做截图。
- 读回某个 cubemap face、array layer 或 mip level。
- 只读回局部矩形，减少 GPU 到 CPU 数据量。
- 调试渲染结果、自动化测试像素结果。

## 6. 常见坑与经验

- **读回不是同步返回。** 数据在 `QRhiReadbackResult::completed` 后才可用。
- **源纹理要有 transfer source 标志。** 没有对应 flag，后端可能无法复制。
- **空 texture 只适合 swapchain 帧。** 离屏帧中没有当前 back buffer 可读。
- **多采样纹理不可直接读回。** 先 resolve。
- **返回是原始字节。** 你要按纹理格式、字节序、premultiplied alpha 自己解释。
- **局部 rect 是 Qt 6.10 起功能。** 兼容旧版本时要读整张。

## 7. 知识点覆盖

- GPU texture/back buffer 异步回读
- mip level、array layer、cubemap face 和局部 rect
- transfer source 标志、MSAA resolve、原始字节解释
- `QRhiReadbackDescription` 与 `QRhiReadbackResult` 的分工
