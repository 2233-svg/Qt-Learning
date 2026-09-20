# QAbstractVideoBuffer::MapData：一次视频映射的非拥有型平面描述

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractVideoBuffer>`  
> 所属模块：`Qt6::Multimedia`  
> 所属类型：`QAbstractVideoBuffer::MapData`  
> 类型性质：公开结构体，随 `QAbstractVideoBuffer::map()` 返回

## 它解决什么问题

`QAbstractVideoBuffer::MapData` 用一组固定大小的数组描述映射后的视频数据：

- 有多少个有效平面；
- 每个平面的起始地址；
- 每行跨过多少字节；
- 每个平面一共有多少字节。

它只是 `QAbstractVideoBuffer` 与 `QVideoFrame` 之间传递映射结果的“视图描述”，不分配、不复制，也不拥有这些地址指向的内存。应用通常不会单独创建它来存数据，而是在自定义 `QAbstractVideoBuffer::map()` 实现中填充后返回。

## 实际使用场景

对于 RGB 图像，常见情况是一个平面：

```cpp
QAbstractVideoBuffer::MapData data;
data.planeCount = 1;
data.data[0] = pixels;
data.bytesPerLine[0] = stride;
data.dataSize[0] = stride * height;
```

对于 NV12 等多平面格式，可以填充两个平面。`data[0]` 通常指向亮度平面，`data[1]` 指向交错的色度平面，两个平面的行跨度和大小可以不同。

## 生命周期与所有权

结构体本身按值返回，复制它只会复制计数、整数和指针值，不会复制像素数据。`data[]` 指针的所有权仍属于 `QAbstractVideoBuffer` 的实现。

派生缓冲必须保证指针至少在对应的 `unmap()` 调用返回前有效。调用方在 `unmap()` 之后继续读写这些指针属于未定义的使用方式，即使某些 CPU 缓冲地址碰巧仍未改变。

默认构造或值初始化的 `MapData` 表示“没有映射数据”：`planeCount` 和所有数组元素为零，所有 `data[]` 指针为 `nullptr`。因此它可以作为映射失败的统一返回值。

## 平面布局如何解释

`planeCount` 是有效平面的数量，数组最多提供四个平面槽位。只有下标 `0` 到 `planeCount - 1` 的元素有意义。

`bytesPerLine[i]` 是第 `i` 个平面的行跨度。它描述从一行起始地址跳到下一行起始地址需要跨过的字节数，可能大于紧密像素数据的理论宽度，因为底层缓冲可能有对齐填充。

`dataSize[i]` 是第 `i` 个平面的总字节数。它不是“每行大小”，也不是像素数量。使用它做指针运算前，应确认格式、行数和对齐规则都与实现一致。

对于多平面格式，如果 `planeCount == 1`，`QVideoFrame` 在某些情况下会依据第一平面的行跨度、帧高度和数据大小推导额外平面。想避免推导歧义，应由 `map()` 直接返回完整的平面布局。

## 与 `QVideoFrame::map()` 的关系

自定义 `QAbstractVideoBuffer::map()` 返回 `MapData` 后，`QVideoFrame::map()` 会把它暴露给调用方。应用应先检查映射是否成功，再根据 `QVideoFrame::planeCount()`、`bytesPerLine(plane)`、`bits(plane)` 等帧接口访问数据。

不要假定 `planeCount` 与“颜色通道数”相同。一个平面可以交错存放多个通道；平面是存储布局概念，通道是像素格式概念。

## 逐项 API 说明

### `int planeCount`

保存映射视频数据的有效平面数量，默认值为 `0`。

当值为 `0` 时表示没有映射结果。正常成功映射至少应使它表示一个有效平面，并同时填好对应的 `data[]`、`bytesPerLine[]` 和 `dataSize[]`。

如果多平面格式只返回 `1`，Qt 可能根据第一平面的信息推导剩余平面；这要求第一平面的跨度和总大小准确，否则得到的后续平面地址会错误。

### `uchar *data[4]`

保存每个平面的起始地址，默认全部为 `nullptr`。下标范围是 `0` 到 `planeCount - 1`。

这些指针是非拥有型指针。实现必须让对应内存保持有效，至少直到 `QAbstractVideoBuffer::unmap()` 返回。应用不应释放、调整或保存它们到映射生命周期之外。

### `int bytesPerLine[4]`

保存每个平面的行跨度，默认全部为 `0`。它用于处理行尾填充和非紧密排列的图像数据。

遍历像素时不能把它简单当作 `width * bytesPerPixel`。应使用视频格式和正确的行跨度计算每一行的起始位置。

### `int dataSize[4]`

保存每个平面占用的总字节数，默认全部为 `0`。它用于描述可访问范围，并参与某些多平面布局推导。

该值应与实际分配的平面内存匹配。填得过小会导致合法像素被截断，填得过大则可能让调用方越过分配边界。

## 常见误区与边界

- `MapData` 不拥有内存，离开作用域不会释放像素数据。
- `planeCount` 不是声道数、颜色通道数或图像层数。
- `bytesPerLine` 不是整个平面大小。
- `dataSize` 不是每行字节数。
- 未使用的数组元素应保持默认值，不要填入其他无效地址。
- `data[i] != nullptr` 不能单独证明映射成功，至少还要检查 `planeCount` 和布局是否合理。
- 复制 `MapData` 不会让底层数据延长生命周期，也不会形成独立快照。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 平面数量 | `int planeCount` | 表示有效视频平面的数量。 | `0` 表示未映射；只读下标 `0` 到 `planeCount - 1`。 |
| 平面地址 | `uchar *data[4]` | 保存每个平面的起始地址。 | 非拥有型；至少保持到 `unmap()` 返回。 |
| 行跨度 | `int bytesPerLine[4]` | 保存每个平面的每行字节跨度。 | 可能包含对齐填充，不等于紧密行大小。 |
| 平面大小 | `int dataSize[4]` | 保存每个平面的总字节数。 | 必须与实际分配范围一致。 |
| 默认状态 | `MapData{}` | 表示没有映射数据。 | 所有整数为 `0`，所有指针为 `nullptr`。 |

---

### 一句话总结

`MapData` 是一次视频缓冲映射的非拥有型布局描述；正确填写平面数量、地址、行跨度和大小，才能让 `QVideoFrame` 安全访问外部像素内存。
