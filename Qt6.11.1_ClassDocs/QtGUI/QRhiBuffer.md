# QRhiBuffer

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiBuffer`

## 1. 先建立直觉

`QRhiBuffer` 是 GPU 缓冲区资源，用来存顶点、索引、uniform/constant 数据或 storage buffer 数据。它解决的问题不是“C++ 里放一段字节”，而是“这段字节如何放到图形后端可访问的位置，并以什么用途暴露给 shader 或 draw call”。

理解它要同时看两个维度：`Type` 描述数据更新频率和存储策略，`UsageFlags` 描述 GPU 如何使用它。一个经常改的 uniform buffer 应该偏 `Dynamic`；一个初始化后长期不变的顶点缓冲适合 `Immutable` 或 `Static`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newBuffer(type, usage, size)`
- 必需步骤：设置类型/用途/大小后调用 `create()`

buffer 的底层实现会随后端变化：有的后端可能为动态 uniform buffer 准备多份 backing storage，有的资源可能没有可直接暴露的 native buffer。不要把 native handle 当成跨后端稳定契约。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `Type::Immutable` | 初始上传后基本不变；通常适合长期顶点/索引数据。 |
| `Type::Static` | 偶尔更新；比 Immutable 更适合低频变更。 |
| `Type::Dynamic` | 高频更新；uniform buffer 常用类型，后端可多缓冲避免阻塞。 |
| `UsageFlag::VertexBuffer` | 作为顶点输入绑定。 |
| `UsageFlag::IndexBuffer` | 作为索引缓冲绑定。 |
| `UsageFlag::UniformBuffer` | 作为 uniform/constant buffer 暴露给 shader。 |
| `UsageFlag::StorageBuffer` | 作为读写或只读/只写 storage buffer，通常需要 compute 能力。 |
| `create()` | 创建底层 native 资源；失败返回 `false`。 |
| `setSize()` / `size()` | 设置/读取字节大小。 |
| `setType()` / `type()` | 设置/读取存储类型。 |
| `setUsage()` / `usage()` | 设置/读取用途标志。 |
| `beginFullDynamicBufferUpdateForCurrentFrame()` | 帧内直接获取动态 buffer 当前帧的可写内存。 |
| `endFullDynamicBufferUpdateForCurrentFrame()` | 完成上面的直接写入。 |
| `nativeBuffer()` | 返回后端 native buffer 信息；可能为空或包含多个 frame slot。 |
| `resourceType()` | 返回 `QRhiResource::Buffer`。 |

## 4. 关键用法

### 创建静态顶点缓冲

```cpp
QRhiBuffer *vb = rhi->newBuffer(QRhiBuffer::Immutable,
                                QRhiBuffer::VertexBuffer,
                                vertexData.size());
vb->create();

QRhiResourceUpdateBatch *u = rhi->nextResourceUpdateBatch();
u->uploadStaticBuffer(vb, vertexData.constData());
```

`Immutable` 不是绝对不可更新，而是表达“我不希望频繁更新”。频繁改它会让后端走更重的上传路径。

### 创建动态 uniform buffer

```cpp
QRhiBuffer *ubuf = rhi->newBuffer(QRhiBuffer::Dynamic,
                                  QRhiBuffer::UniformBuffer,
                                  rhi->ubufAligned(sizeof(Uniforms)));
ubuf->create();
```

uniform buffer 要考虑 `ubufAlignment()` / `ubufAligned()`，特别是一个大 uniform buffer 内放多组对象参数时。

### 动态 buffer 全量写入

```cpp
char *p = ubuf->beginFullDynamicBufferUpdateForCurrentFrame();
memcpy(p, &uniforms, sizeof uniforms);
ubuf->endFullDynamicBufferUpdateForCurrentFrame();
```

这适合每帧全量更新中大型 dynamic buffer。它不能和同一 buffer 的 `QRhiResourceUpdateBatch` 更新/回读混用，也不能只更新一小段后假设旧内容保留。

## 5. 使用场景

- 网格顶点和索引数据。
- per-frame、per-object uniform/constant 数据。
- compute shader 的 storage buffer。
- 实例化绘制的实例数据。
- 临时 staging 或 scratch GPU 数据，配合 `deleteLater()` 管理帧内生命周期。

## 6. 常见坑与经验

- **类型和用途是两个维度。** `Dynamic` 不等于 uniform，`UniformBuffer` 也不一定能用非 dynamic 类型，取决于后端功能。
- **创建后改设置需要重新 `create()`。** `setSize()`、`setType()`、`setUsage()` 对已创建 native 资源不会魔法生效。
- **uniform buffer 注意对齐。** 不按 `ubufAlignment()` 排布，跨后端很容易读错。
- **不要混用两套更新路径。** full dynamic update 与 resource update batch/readback 混用会有未定义或后端相关行为。
- **dynamic buffer 每帧都要写需要的区域。** 后端可能丢弃旧内容或使用多帧 backing storage。
- **native buffer 不一定存在或只有一个。** `nativeBuffer()` 结果要按 slotCount 和当前 frame slot 理解。

## 7. 知识点覆盖

- GPU buffer 的用途：顶点、索引、uniform、storage
- Immutable、Static、Dynamic 三种存储/更新策略
- Resource update batch 与 direct dynamic update 的边界
- uniform buffer 对齐、多帧飞行和 frame slot
- native buffer 互操作的限制
- buffer 创建、重建、销毁与 RHI 生命周期
