# QRhiResourceUpdateBatch

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiResourceUpdateBatch`

## 1. 先建立直觉

`QRhiResourceUpdateBatch` 是一批资源搬运命令：上传 buffer、更新 dynamic buffer、上传 texture、复制 texture、生成 mipmap、发起异步回读。它把“CPU 侧准备的数据”整理成一批，随后在 `beginPass()`、`endPass()`、`resourceUpdate()` 或 compute pass 边界提交给 RHI。

它不是普通对象，不应该 `delete`。从 `QRhi::nextResourceUpdateBatch()` 取出后，要么交给 command buffer 提交，要么在不用时 `release()` 还回池。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 获取方式：`QRhi::nextResourceUpdateBatch()`
- 提交入口：`QRhiCommandBuffer::resourceUpdate()`、`beginPass()`、`endPass()`、`beginComputePass()`、`endComputePass()`
- 主要能力：buffer 上传/更新、texture 上传/复制、mipmap、异步回读

大多数上传函数会复制传入数据；Qt 6.10 起部分重载接受 `QByteArray` 并移动进 batch，适合避免额外复制。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `uploadStaticBuffer()` | 上传 `Immutable` 或 `Static` buffer，可全量或局部上传。 |
| `updateDynamicBuffer()` | 更新 `Dynamic` buffer 区域。 |
| `uploadTexture(QImage)` | 把 `QImage` 上传到未压缩纹理 level 0/layer 0。 |
| `uploadTexture(desc)` | 按 `QRhiTextureUploadDescription` 上传多层、多 mip、压缩或局部数据。 |
| `copyTexture(dst, src, desc)` | 在 GPU 侧从一个纹理复制到另一个纹理。 |
| `generateMips(tex)` | 为纹理生成 mipmap。 |
| `readBackTexture(desc, result)` | 发起纹理或 back buffer 异步回读。 |
| `readBackBuffer(buf, offset, size, result)` | 发起 buffer 异步回读。 |
| `merge(other)` | 合并另一个 batch 的操作，用于初始化更新延后提交。 |
| `hasOptimalCapacity()` | 判断当前批次是否仍在建议容量内。 |
| `release()` | 未提交时把 batch 还回池；提交给 command buffer 后不要再调用。 |

## 4. 关键用法

### 初始化资源上传

```cpp
QRhiResourceUpdateBatch *u = rhi->nextResourceUpdateBatch();
u->uploadStaticBuffer(vertexBuffer, vertexData.constData());
u->uploadTexture(diffuseTexture, image);

cb->beginPass(rt, clear, dsClear, u);
```

传给 `beginPass()` 后，batch 被 RHI 接管并释放。调用方不要再访问或 release 它。

### 延迟合并初始化 batch

```cpp
QRhiResourceUpdateBatch *initial = rhi->nextResourceUpdateBatch();
initial->uploadStaticBuffer(vb, vertexData.constData());

QRhiResourceUpdateBatch *frame = rhi->nextResourceUpdateBatch();
frame->merge(initial);
initial->release();
cb->resourceUpdate(frame);
```

`merge()` 后源 batch 不再可提交，但仍要 `release()`。

### 异步读回

```cpp
auto *result = new QRhiReadbackResult;
result->completed = [result] {
    process(result->data);
    delete result;
};
updates->readBackTexture(QRhiReadbackDescription(texture), result);
```

回读完成时机通常跨帧，不能在排队后立刻读取数据。

## 5. 使用场景

- 加载模型后上传 vertex/index buffer。
- 每帧更新 uniform buffer。
- 上传图片、压缩纹理、cubemap、texture array。
- 生成 mipmap，或在 GPU 侧复制纹理。
- 截图、测试、调试 readback。
- 把初始化阶段的资源更新合并进第一帧提交。

## 6. 常见坑与经验

- **不要手动 delete。** 未提交的 batch 用 `release()`；已提交的 batch 由 RHI 处理。
- **静态和动态 buffer 用不同函数。** `uploadStaticBuffer()` 对应 Immutable/Static，`updateDynamicBuffer()` 对应 Dynamic。
- **上传数据生命周期通常可以很短。** 指针重载会复制数据，函数返回后源数据可释放。
- **生成 mipmap 需要纹理 flag。** 纹理要有 `MipMapped` 和 `UsedWithGenerateMips`，格式也要支持过滤。
- **readback 是异步。** 用 callback 处理结果，并考虑 `MaxAsyncReadbackFrames`。
- **texture copy 不做格式转换。** 源/目标格式应一致，否则后端行为不可靠。
- **batch 太大时分批提交。** `hasOptimalCapacity()` 为 false 时可提交后重新取 batch。

## 7. 知识点覆盖

- RHI 资源更新批次模型
- static/dynamic buffer 更新差异
- texture 上传、复制、mipmap 和压缩/多层描述
- 异步 readback 结果处理
- batch merge、release 和提交所有权
- 数据复制、移动 QByteArray 与帧边界
