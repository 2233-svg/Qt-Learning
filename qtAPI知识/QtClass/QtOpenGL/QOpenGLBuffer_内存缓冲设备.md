# QOpenGLBuffer 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLBuffer>`  
> 所属模块：`Qt6::OpenGL`  
> 类型：OpenGL buffer object 包装

## 它解决什么问题

OpenGL buffer object 把顶点、索引、像素和其他数据保存在 OpenGL server 一侧，避免每次绘制都从 CPU 上传。`QOpenGLBuffer` 将这类 GPU 资源包装为 Qt 值类型，提供创建、绑定、分配、局部读写、映射和销毁接口。

它不是 CPU 内存容器。`allocate()`、`write()`、`read()`、`map()` 等操作最终都走当前 OpenGL context，是否可用还取决于实际 OpenGL/OpenGL ES 实现。

## 实际使用场景

### 顶点与索引数据

`VertexBuffer` 保存顶点属性，`IndexBuffer` 保存 `glDrawElements()` 使用的索引。它们是最常见的用途。

### 像素传输

桌面 OpenGL 的 `PixelPackBuffer` 可帮助从 OpenGL server 读回像素，`PixelUnpackBuffer` 可用于向纹理上传像素。这两个 target 在 OpenGL ES 中不支持。

### 动态几何

动态网格、粒子数据、流式 UI 图元可使用 `DynamicDraw`，再用 `write()` 或 `mapRange()` 改写指定范围。usage pattern 只是交给驱动的使用提示，不保证具体内存布局或性能结果。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL)
target_link_libraries(mytarget PRIVATE Qt6::OpenGL)
```

```cpp
#include <QOpenGLBuffer>

QOpenGLBuffer vertexBuffer(QOpenGLBuffer::VertexBuffer);

bool uploadVertices(const float *vertices, int byteCount)
{
    if (!vertexBuffer.create())
        return false;

    vertexBuffer.setUsagePattern(QOpenGLBuffer::StaticDraw);
    if (!vertexBuffer.bind())
        return false;

    vertexBuffer.allocate(vertices, byteCount);
    vertexBuffer.release();
    return true;
}
```

调用 `create()`、`bind()` 和数据操作前，必须已有正确的 current `QOpenGLContext`。

## 核心使用模型

典型生命周期如下：

1. 在 context current 后构造 wrapper；
2. `create()` 在 OpenGL server 创建底层对象；
3. `setUsagePattern()` 设置数据使用提示；
4. `bind()` 绑定到该 buffer 的 target；
5. `allocate()` 分配/上传，或 `write()` 更新；
6. 必要时 `map()`/`mapRange()`，之后 `unmap()`；
7. `release()` 解除绑定；
8. 在资源不再需要且 context 生命周期允许时 `destroy()` 或析构。

## context、资源共享与拷贝语义

### 创建与绑定的 context 要求

`create()` 必须在有 current context 时调用。底层 buffer 只能在创建它的 context，或与其共享资源的 context 中使用。

`bind()` 失败通常意味着当前 context 不正确，或当前 OpenGL 实现不支持所选 target。必须检查其返回值。

### 浅拷贝，不复制 GPU 存储

拷贝 `QOpenGLBuffer` 会共享同一个底层 OpenGL buffer，并且没有 copy-on-write。对任一副本执行 `write()`、`allocate()` 或 `destroy()`，都会影响其他副本。

要获得独立 GPU 数据，必须创建另一个 `QOpenGLBuffer` 并分别创建、上传资源。

Qt 6.5 引入移动构造、移动赋值和 `swap()`。移动后的源对象只保证可以析构或重新赋值，不能继续正常使用。

### 绑定是 OpenGL context 状态

`bind()` 改变 current context 内指定 target 的绑定状态。`release()` 解绑本对象；静态 `QOpenGLBuffer::release(type)` 相当于让这个 target 绑定 0，适用于调用方不知道当前绑定的是哪一个 wrapper 的场景。

## 枚举语义

### `Type`

| 取值 | 用途 | 边界 |
| --- | --- | --- |
| `VertexBuffer` | 顶点数组数据。 | 最常用于顶点属性。 |
| `IndexBuffer` | 索引数据。 | 供 `glDrawElements()` 使用。 |
| `PixelPackBuffer` | 从 OpenGL server 读像素。 | OpenGL ES 不支持。 |
| `PixelUnpackBuffer` | 向 OpenGL server 上传像素。 | OpenGL ES 不支持。 |

### `UsagePattern`

- `Stream*`：设置一次，使用少量次数；
- `Static*`：设置一次，使用很多次；
- `Dynamic*`：会重复修改并重复使用。

后缀 `Draw`、`Read`、`Copy` 分别描述主要用于绘制、从 OpenGL server 读回、或供后续 server 复制/绘制。默认值为 `StaticDraw`。

必须在 `allocate()` 或 `write()` 之前调用 `setUsagePattern()`。

### `Access` 和 `RangeAccessFlags`

`map()` 使用单一访问模式：

- `ReadOnly`：只读；
- `WriteOnly`：只写；
- `ReadWrite`：读写。

`mapRange()` 使用可组合 flags：

- `RangeRead`、`RangeWrite`：访问方向；
- `RangeInvalidate`：丢弃指定范围旧内容；
- `RangeInvalidateBuffer`：丢弃整个 buffer 旧内容；
- `RangeFlushExplicit`：修改后由调用方显式 flush；
- `RangeUnsynchronized`：不等待未完成操作，换取性能但由调用方负责同步安全。

## 关键 API 语义与边界

### `allocate()` 会替换全部旧内容

`allocate(data, count)` 重新分配 buffer 的 `count` 字节，原内容被移除。仅需改写一段时用 `write()`，不要误用 `allocate()`。

### offset 和 count 都是字节数

`read()`、`write()`、`mapRange()` 的 offset/count 都不是元素数量。调用方必须保证范围非负且不越界；Qt 不会替你把 `float` 数量转换成字节数。

### 映射指针只能短期使用

`map()` 或 `mapRange()` 成功后返回临时 CPU 可访问地址。必须在正确的 current context 和绑定状态下 `unmap()`；`unmap()` 后、buffer 销毁后或 context 状态变化后都不能继续解引用该指针。

映射失败返回 `nullptr`。

### OpenGL ES 支持差异

- `mapRange()` 在 OpenGL ES 2.0 及更早版本不可用；
- `map()` 在 OpenGL ES 2.0 及更早版本要求 `GL_OES_mapbuffer`；
- `read()` 在 OpenGL ES 中不支持；
- `PixelPackBuffer` 和 `PixelUnpackBuffer` 在 OpenGL ES 中不支持。

### 查询失败的哨兵值

`bufferId()` 在未创建时返回 `0`。`size()` 在未创建或实现不支持读取尺寸时返回 `-1`，不能把该值当作空 buffer 的长度。

## 常见误区

### 忽略 `bind()` 返回值

buffer 已创建不代表它一定能在当前 context 中绑定。共享 context 配置、OpenGL ES target 差异和线程切换都会导致失败。

### 认为拷贝产生独立副本

`QOpenGLBuffer a = b;` 共享同一 GPU buffer。若 `a.destroy()`，`b` 也不再代表可用的底层资源。

### 映射后忘记 `unmap()`

映射未解除时继续使用或重建 buffer，容易造成未定义行为或驱动错误。映射范围应尽量小，并把 `unmap()` 放在清晰的控制流中。

## 逐项 API 说明

### 成员类型

#### `enum Type`

选择底层 buffer target：`VertexBuffer`、`IndexBuffer`、`PixelPackBuffer`、`PixelUnpackBuffer`。

#### `enum UsagePattern`

选择 `StreamDraw` 到 `DynamicCopy` 之间的使用提示，默认 `StaticDraw`。

#### `enum Access`

指定 `map()` 的读写方式：`ReadOnly`、`WriteOnly`、`ReadWrite`。

#### `enum RangeAccessFlag` 与 `RangeAccessFlags`

指定 `mapRange()` 的范围访问策略。`RangeAccessFlags` 是这些标志的 `QFlags` 组合。

### 构造、赋值与生命周期

#### `QOpenGLBuffer::QOpenGLBuffer()`

创建默认 `VertexBuffer` wrapper；尚未创建 GPU buffer。

#### `explicit QOpenGLBuffer::QOpenGLBuffer(Type type)`

创建指定 target 的 wrapper；仍需 `create()` 才会创建 OpenGL server 资源。

#### `QOpenGLBuffer::QOpenGLBuffer(const QOpenGLBuffer &other)`

创建 `other` 的浅拷贝，两个对象共享底层 buffer。

#### `QOpenGLBuffer::QOpenGLBuffer(QOpenGLBuffer &&other) noexcept`（Qt 6.5）

移动构造 wrapper。源对象进入部分形成状态，只应析构或重新赋值。

#### `QOpenGLBuffer::~QOpenGLBuffer() noexcept`

销毁 wrapper 和相应的 OpenGL server 存储；其他共享同一底层资源的副本会失效。

#### `QOpenGLBuffer &operator=(const QOpenGLBuffer &other)`

浅拷贝赋值，共享 `other` 的底层资源。

#### `QOpenGLBuffer &operator=(QOpenGLBuffer &&other) noexcept`（Qt 6.5）

移动赋值。源对象后续仅可析构或重新赋值。

#### `void swap(QOpenGLBuffer &other) noexcept`（Qt 6.5）

快速交换两个 wrapper，不复制 GPU 内容。

### 创建、绑定与查询

#### `Type type() const`

返回此对象的 buffer target。

#### `UsagePattern usagePattern() const`

返回使用提示，默认 `StaticDraw`。

#### `void setUsagePattern(UsagePattern value)`

设置使用提示。必须早于 `allocate()` 或 `write()`。

#### `bool create()`

在 current context 创建底层 buffer。没有 current context、实现不支持 buffer 或创建失败时返回 `false`。

#### `bool isCreated() const`

返回底层 OpenGL buffer 是否已创建。

#### `void destroy()`

销毁底层 buffer，使所有共享引用失效。

#### `bool bind()`

绑定到 current context 的相应 target。context 必须是创建 context 或共享 context；失败返回 `false`。

#### `void release()`

解除该对象在 current context 中的绑定。通常需要与 `bind()` 相同的 context。

#### `static void release(Type type)`

对 current context 中的 target 直接解除绑定，效果类似 `glBindBuffer(type, 0)`。

#### `GLuint bufferId() const`

返回 OpenGL buffer ID；未创建时为 `0`。

### 数据和映射

#### `void allocate(const void *data, int count)`

分配 `count` 字节并复制 data，旧内容全部丢弃。要求 buffer 已创建并绑定。

#### `void allocate(int count)`

分配未初始化的 `count` 字节，等价于 `allocate(nullptr, count)`。要求已创建并绑定。

#### `void write(int offset, const void *data, int count)`

替换从 offset 开始的 `count` 字节，其他范围保持不变。要求已创建、绑定且范围有效。

#### `bool read(int offset, void *data, int count)`

把数据读回应用内存。成功返回 `true`；OpenGL ES 不支持时返回 `false`。要求已绑定。

#### `void *map(Access access)`

映射整个 buffer，失败返回 `nullptr`。要求已创建并绑定，成功后必须 `unmap()`。

#### `void *mapRange(int offset, int count, RangeAccessFlags access)`

映射指定字节范围，失败返回 `nullptr`。要求已创建并绑定；OpenGL ES 2.0 及更早版本不可用。

#### `bool unmap()`

解除此前映射。成功返回 `true`；要求当前 buffer 已绑定且确实仍处于映射状态。

#### `int size() const`

返回字节大小。未创建或实现不支持查询时返回 `-1`；查询前通常应绑定。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Type` | 选择顶点、索引或像素传输 target。 | Pixel pack/unpack 不支持 OpenGL ES。 |
| 类型 | `UsagePattern` | 向驱动提示数据更新频率和用途。 | 只是提示；需在 `allocate()`/`write()` 前设置。 |
| 类型 | `Access` | 指定整块映射的读写方式。 | 传给 `map()`；失败会返回空指针。 |
| 类型 | `RangeAccessFlag(s)` | 指定范围映射的访问和同步策略。 | `RangeUnsynchronized` 的同步风险由调用方承担。 |
| 构造 | `QOpenGLBuffer()` | 创建默认顶点 buffer wrapper。 | 还没有 GPU 资源。 |
| 构造 | `QOpenGLBuffer(Type)` | 创建指定 target wrapper。 | 仍需 `create()`。 |
| 拷贝 | `QOpenGLBuffer(const QOpenGLBuffer &)` | 浅拷贝底层资源引用。 | 无 copy-on-write，修改会彼此可见。 |
| 移动 | 移动构造、移动赋值、`swap()` | 转移或交换 wrapper。 | Qt 6.5 起；移动源只可析构/重赋值。 |
| 生命周期 | `create()` | 在 current context 创建 GPU buffer。 | 失败必须处理；资源只可用于创建/共享 context。 |
| 生命周期 | `isCreated()` / `destroy()` | 查询或销毁底层 buffer。 | `destroy()` 会使全部浅拷贝失效。 |
| 绑定 | `bind()` / `release()` | 绑定或解绑该 target。 | 绑定是 context 状态；检查 `bind()` 返回值。 |
| 绑定 | `static release(Type)` | 直接清空 current context 的 target。 | 需要 current context。 |
| 查询 | `bufferId()` / `size()` | 查询 ID 或字节数。 | 未创建 ID 为 `0`；不支持 size 查询时为 `-1`。 |
| 配置 | `setUsagePattern()` / `usagePattern()` | 设置或读取使用提示。 | 默认 `StaticDraw`。 |
| 数据 | `allocate()` 两个重载 | 重新分配整个 buffer。 | 会丢弃旧数据；长度为字节数。 |
| 数据 | `write()` | 局部改写 buffer。 | 要求已创建、绑定且范围不越界。 |
| 数据 | `read()` | 从 GPU buffer 读数据。 | OpenGL ES 不支持；检查返回值。 |
| 映射 | `map()` / `mapRange()` | 获得临时 CPU 访问地址。 | 失败为空；使用后必须 `unmap()`。 |
| 映射 | `unmap()` | 结束映射。 | 指针之后立即失效。 |

### 一句话总结

`QOpenGLBuffer` 管理 OpenGL server 侧 buffer：创建和数据操作离不开正确的 current context，拷贝共享资源，映射和读写则必须严格遵守绑定、平台支持和字节范围边界。
