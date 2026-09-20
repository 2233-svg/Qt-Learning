# QAbstractVideoBuffer：让 QVideoFrame 能引用自定义视频存储

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractVideoBuffer>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：抽象接口，通常由自定义视频缓冲实现类继承

## 它解决什么问题

`QVideoFrame` 需要一个对象来描述“视频像素实际存在哪里，以及如何访问它”。`QAbstractVideoBuffer` 就是这个桥梁：它把帧的格式信息和底层存储的映射操作交给具体实现。

Qt 自带的视频流水线通常会创建自己的缓冲对象。只有在以下情况，应用才需要直接实现这个抽象类：

- 视频帧来自相机、采集卡、共享内存或第三方解码器；
- 像素已经在一块预分配的 CPU 内存中，不希望再次复制；
- 像素在 GPU、DMA-BUF 或其他硬件资源中，需要在 CPU 访问时临时映射；
- 需要把外部视频缓冲包装成 `QVideoFrame`，再交给 Qt Multimedia 的后续组件。

它不是一个通用的“内存容器”，也不是可以直接创建的具体视频帧类。应用通常通过自定义派生类实例化，再把派生对象交给 `QVideoFrame`。

## 实际使用场景

例如，第三方解码器每次回调给应用一块 NV12 图像。可以让派生类保存这块内存及其行跨度，在 `format()` 返回 `QVideoFrameFormat`，在 `map()` 中填充 Y 平面和 UV 平面的指针，最后用这些信息构造 `QVideoFrame`。

如果底层是 CPU 内存，映射可以只是返回预先存在的地址；如果底层是硬件缓冲，`map()` 可以执行硬件到 CPU 地址空间的映射，而 `unmap()` 负责解除映射并按需写回。

## 生命周期、所有权与线程

`QAbstractVideoBuffer` 本身是抽象基类，不负责替派生类管理外部资源。派生类必须明确保存的数据、句柄或引用在 `QVideoFrame` 仍可能使用期间保持有效。

`map()` 返回的 `MapData` 只描述映射结果，不拥有 `data[]` 指向的内存。至少在对应的 `unmap()` 返回前，派生类必须继续持有这些地址所指向的数据。不要返回临时数组、局部变量地址或会立即失效的第三方对象内部指针。

同一个缓冲可能被多个值语义的 `QVideoFrame` 间接引用。不要假定 `map()` 一定发生在创建线程，也不要在没有确认线程约束的情况下让外部线程同时修改底层数据。若底层资源要求特定图形或采集线程访问，应在派生类内部同步，或把帧的使用限制在明确的线程中。

`QVideoFrame::map()` 与 `unmap()` 必须成对使用。应用完成 CPU 访问后应立即解除映射，避免硬件资源长期被锁定。映射失败时返回默认构造的 `MapData`，调用方应检查 `planeCount` 或数据指针，而不是继续解引用。

## 最小实现骨架

下面只展示接口关系，实际实现还需要保存外部缓冲的生命周期和格式：

```cpp
class ExternalVideoBuffer final : public QAbstractVideoBuffer
{
public:
    explicit ExternalVideoBuffer(const QVideoFrameFormat &format)
        : m_format(format)
    {
    }

    QVideoFrameFormat format() const override
    {
        return m_format;
    }

    MapData map(QVideoFrame::MapMode mode) override
    {
        Q_UNUSED(mode);
        MapData result;
        result.planeCount = 1;
        result.data[0] = m_data;
        result.bytesPerLine[0] = m_stride;
        result.dataSize[0] = m_size;
        return result;
    }

    void unmap() override
    {
        // 硬件缓冲在这里解除映射；CPU 缓冲可以什么也不做。
    }

private:
    QVideoFrameFormat m_format;
    uchar *m_data = nullptr;
    int m_stride = 0;
    int m_size = 0;
};
```

## `format()`、`map()` 与 `unmap()` 的协作

1. 构造派生缓冲时确定格式，使 `format()` 随时可用。
2. `QVideoFrame` 使用该格式创建自己的格式值副本；之后帧格式可以被分离并修改，因此缓冲实现不能依赖调用方永远不改格式对象。
3. 调用方请求 `QVideoFrame::ReadOnly` 时，`map()` 必须确保返回的数据已经包含当前帧内容。
4. 请求包含 `QVideoFrame::WriteOnly` 时，调用方可能修改映射内存；`unmap()` 必须按底层资源规则提交或写回这些修改。
5. 如果映射失败，返回默认 `MapData`。不要用“非空但不完整”的结构表示失败。

对于多平面格式，`map()` 可以返回实际的多个平面，也可以只返回一个包含全部像素数据的平面。后一种情况下，`QVideoFrame` 会依据第一平面的行跨度、帧高度和数据大小推导额外平面。若格式和布局不匹配，推导出的平面地址就不可靠，因此自定义实现必须准确填写跨度与大小。

## 常见误区与边界

- 不能直接 `new QAbstractVideoBuffer`，因为 `format()` 和 `map()` 是纯虚函数。
- `MapData` 不拥有内存。析构 `MapData` 不会释放任何数据。
- `planeCount` 表示有效平面数量，最多使用固定数组支持的平面槽位；没有填充的槽位应保持默认值。
- `bytesPerLine` 是每一行占用的字节数，不是像素宽度，也不一定等于紧密打包的行大小。
- `dataSize` 是该平面的总字节数，不能随意填成帧的像素数。
- `ReadOnly` 和 `WriteOnly` 是访问意图，不应被忽略；写映射结束后的提交时机是 `unmap()`。
- CPU 内存缓冲可使用默认 `unmap()`，但硬件或暂时映射的缓冲通常必须重写它。
- 不要在 `unmap()` 后继续使用 `map()` 返回的指针，除非实现明确保证其仍然有效；从接口契约看，安全做法是视为已失效。

## 逐项 API 说明

### `[virtual noexcept] QAbstractVideoBuffer::~QAbstractVideoBuffer()`

销毁视频缓冲基类对象。派生类析构函数应负责释放自己拥有的 CPU 内存、解除仍存在的硬件映射并关闭相关句柄。析构时不要再依赖调用方会补做一次 `unmap()`。

### `[pure virtual] QVideoFrameFormat QAbstractVideoBuffer::format() const`

返回底层视频缓冲的格式。格式必须在 `QVideoFrame` 使用该缓冲时可查询，通常在构造缓冲时就确定。返回值是格式对象的值拷贝；它不改变底层缓冲，也不负责动态通知格式变化。

如果外部资源在运行中切换分辨率、像素格式或颜色空间，应创建与新格式匹配的新缓冲/新帧，而不是让已有缓冲的 `format()` 在使用中悄悄改变。

### `[pure virtual] QAbstractVideoBuffer::MapData QAbstractVideoBuffer::map(QVideoFrame::MapMode mode)`

把视频缓冲的平面映射到 CPU 可访问的地址，并返回平面布局。`mode` 指出调用方是要读、写，还是读写；包含 `ReadOnly` 时，初始映射内容必须可读，包含 `WriteOnly` 时，修改结果要在 `unmap()` 时按底层资源规则写回。

映射失败必须返回默认构造的 `MapData`。对于已经位于 CPU 内存中的缓冲，可以把数据视为已映射，直接返回预分配内存的布局。

映射并不表示复制。返回的 `data[]` 地址可能是原始地址，也可能是硬件映射后的临时地址。调用方只应在映射有效期间访问它。

### `[virtual] void QAbstractVideoBuffer::unmap()`

释放 `map()` 建立的映射，并在写映射场景中提交修改。CPU 内存缓冲通常可以依赖默认实现，因为它没有临时映射需要释放；硬件缓冲、共享资源或需要显式同步的实现必须重写它。

调用方应保证每次成功映射都与一次解除映射配对。不要把 `unmap()` 当成清空视频数据的操作，它的职责是结束访问并完成必要的资源同步。

### `struct QAbstractVideoBuffer::MapData`

描述一次映射后的平面数量、每个平面的地址、行跨度和字节数。该结构只是一组非拥有型视图，具体字段见下一篇 `QAbstractVideoBuffer::MapData` 笔记。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual noexcept ~QAbstractVideoBuffer()` | 销毁视频缓冲对象。 | 派生类负责释放外部资源；不要依赖调用方再补 `unmap()`。 |
| 纯虚查询 | `QVideoFrameFormat format() const` | 返回底层缓冲格式。 | 构造后应稳定可用；格式变化通常应创建新缓冲。 |
| 纯虚映射 | `MapData map(QVideoFrame::MapMode mode)` | 将视频平面映射到 CPU 地址空间。 | 失败返回默认 `MapData`；按读写模式准备和提交数据。 |
| 解除映射 | `void unmap()` | 结束映射并按需写回数据。 | 与成功的 `map()` 配对；硬件缓冲通常必须重写。 |
| 公开类型 | `struct MapData` | 描述平面地址、跨度和大小。 | 不拥有数据；地址至少保持到 `unmap()` 返回。 |

---

### 一句话总结

`QAbstractVideoBuffer` 是把外部或硬件视频存储接入 `QVideoFrame` 的抽象契约：实现时最重要的是稳定的格式、正确的平面布局，以及严格配对的 `map()`/`unmap()` 生命周期。
