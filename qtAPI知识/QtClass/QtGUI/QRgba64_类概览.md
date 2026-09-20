# Qt QRgba64：64 位 RGBA 整数颜色

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRgba64>`  
> 所属模块：`Qt6::Gui`  
> 类型定位：64 位 RGBA 值类型

## 1. 它解决什么问题

`QRgba64` 是一个固定大小的颜色值类型，用四个 16 位无符号整数保存 red、green、blue、alpha。它可以在需要比 `QRgb` 更高精度时使用，尤其适合图像像素处理、颜色格式转换、预乘 alpha 计算和 16 位通道的缓存。

它和 `QColor` 的职责不同：

- `QRgba64` 只保存四个通道，不保存颜色空间、色域、白点或传递函数。
- 它是整数像素表示，不是浮点颜色工作空间；每个通道的合法数值范围就是 `0..65535`。
- 它不记录当前数据是否已经预乘 alpha。`premultiplied()` 和 `unpremultiplied()` 返回转换后的副本，调用方负责维护表示约定。
- 它的核心存储是一个 64 位打包值，适合紧凑保存和与底层像素数据衔接，但原始 `quint64` 形式不应未经约定就当作跨平台文件格式。

Qt 文档把它描述为 `QRgb` 的高精度替代类型。与 8 位 `QRgb` 相比，`QRgba64` 能在多次处理过程中减少量化损失；最后需要显示或兼容旧 API 时，再用 `toArgb32()` 降为 8 位。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QRgba64>
```

qmake 工程使用：

```qmake
QT += gui
```

这是一个值类型，不需要 `QGuiApplication` 才能构造或读取。但如果把它用于 `QImage`、窗口或图形资源，仍要遵守对应 API 的线程和初始化约束。

## 3. 最小使用方式

```cpp
#include <QRgba64>

QRgba64 makeColor()
{
    // 逐通道使用 16 位表示。
    return QRgba64::fromRgba64(50000, 30000, 10000, 65535);
}

uint toLegacyArgb(QRgba64 color)
{
    // 降为 0xAARRGGBB；每通道会按 16 位到 8 位规则量化。
    return color.toArgb32();
}
```

从 8 位颜色提升到 16 位时：

```cpp
QRgba64 color = QRgba64::fromArgb32(0x80402010u);
Q_ASSERT(color.red() == 0x4040);
Q_ASSERT(color.alpha() == 0x8080);
```

`fromRgba()` 使用 `x | (x << 8)` 展开 8 位通道，因此 `0x00 -> 0x0000`、`0xff -> 0xffff`，而不是简单地把 8 位数值放到 16 位低位。

## 4. 通道和打包语义

### 4.1 四个通道均为 `quint16`

`red()`、`green()`、`blue()`、`alpha()` 返回原始 16 位通道。它们不会做归一化，也不会返回浮点值：

```cpp
QRgba64 color = QRgba64::fromRgba64(65535, 32768, 0, 49152);

quint16 red = color.red();     // 65535
quint16 green = color.green(); // 32768
quint16 alpha = color.alpha(); // 49152
```

setter 只替换对应的 16 位字段，不会改变其他通道，也不会因为改变 alpha 而重新计算 RGB。

### 4.2 与 8 位通道互转会四舍五入

`red8()`、`green8()`、`blue8()`、`alpha8()` 使用 Qt 的 `div_257` 规则把 16 位通道降为 8 位。它不是简单的 `channel >> 8`，而是近似除以 `257` 的四舍五入转换：

```cpp
QRgba64 color = QRgba64::fromRgba64(0x8080, 0x0100, 0xfeff, 0xffff);
// color.red8() 约为 128，color.alpha8() 为 255
```

因此从 8 位通过 `fromRgba()` 提升，再通过 `red8()` 等函数降回时，通常能得到原始 8 位通道。

### 4.3 `ARGB32` 按数值位解释

`fromArgb32()` 和 `toArgb32()` 使用 `0xAARRGGBB` 的数值形式：

- bits 31..24：alpha
- bits 23..16：red
- bits 15..8：green
- bits 7..0：blue

这里说的是整数值的位布局，不是把 `uint` 强转为字节指针后观察到的内存顺序。Qt 内部会根据主机字节序安排 16 位通道，使通道的逻辑顺序保持一致。

### 4.4 `quint64` 是表示层接口

`fromRgba64(quint64)`、`operator quint64()` 和 `operator=(quint64)` 处理的是 `QRgba64` 的 64 位内部表示。它们适合与已经遵守同一表示约定的底层代码衔接。

如果把这个 `quint64` 写入文件、网络协议或跨架构共享内存，应自行定义字节序和通道顺序。不要把它等同于 `ARGB64` 的通用外部编码。

## 5. 预乘与非预乘

未预乘颜色的 RGB 与 alpha 独立保存。预乘颜色则把 RGB 按 alpha 缩放：

```text
R' = R * A / 65535
G' = G * A / 65535
B' = B * A / 65535
A' = A
```

`premultiplied()` 返回预乘副本，不改变当前对象。对于完全不透明值直接返回自身；对于完全透明值返回全零表示；部分透明值使用整数计算并进行适当舍入。

`unpremultiplied()` 返回非预乘副本：

- alpha 为 `65535` 时直接返回自身。
- alpha 为 `0` 时也直接返回自身，因为无法从零 alpha 恢复原来的 RGB。
- 介于两者之间时按 alpha 还原 RGB，并进行整数舍入。

这意味着对规范的透明预乘像素，alpha 为零时通常 RGB 本来就是零；但对任意手工构造的透明 `QRgba64`，`unpremultiplied()` 不会替你把 RGB 清零。

不要重复执行同一种转换。对已经预乘的值再次调用 `premultiplied()` 会再次缩放 RGB；对未预乘值调用 `unpremultiplied()` 会错误放大通道。

## 6. 实际使用场景

### 6.1 高精度 CPU 像素处理

图像缩放、卷积、颜色叠加、透明合成等操作若在 8 位通道上反复进行，容易积累量化误差。使用 `QRgba64` 作为中间像素可以把每个通道的整数精度提高到 16 位，最后再输出到目标图像格式。

### 6.2 预乘 alpha 管线

Qt 图像格式中常见预乘和非预乘的区别。进行自定义像素计算时，应在算法入口统一成一种表示，计算完成后再转回目标格式。`premultiplied()` 和 `unpremultiplied()` 适合做这个边界转换。

### 6.3 与 8 位像素 API 兼容

旧代码常使用 `QRgb` 或 `uint` 的 `0xAARRGGBB` 形式。`fromArgb32()` 可以把它提升为 16 位通道，`toArgb32()` 可以在最终输出时降回去。这样可以把高精度处理限制在需要的阶段。

### 6.4 RGB565 输出

`toRgb16()` 把颜色压缩为 16 位 RGB565：

- red 使用 5 位。
- green 使用 6 位。
- blue 使用 5 位。
- alpha 被丢弃。

它适合与只支持 RGB565 的显示或协议接口衔接，不适合保存透明颜色。

## 7. 生命周期、所有权和线程

`QRgba64` 是轻量值类型：

- 不继承 `QObject`，没有父对象和事件循环要求。
- 不拥有外部内存或图形资源。
- 可以按值返回、复制、放入 Qt 容器或作为信号参数。
- 只读访问一个独立副本不涉及对象线程归属。

如果多个线程共享同一个实例并通过 setter 或赋值运算写入，仍然需要外部同步。把 `QRgba64` 作为消息值复制到工作线程，通常比跨线程共享可变实例更清晰。

它的大小和位布局适合底层像素工作，但不要仅凭 `sizeof(QRgba64) == 8` 就假定外部 ABI、文件格式或 GPU 格式完全相同。跨边界传递时要明确端序、对齐和通道约定。

## 8. 常见误区与排查顺序

### 8.1 把 `toRgb16()` 当成 RGBA16

它返回的是 RGB565，只有 5/6/5 位 RGB，alpha 完全丢失。需要保留四个 16 位通道时，应使用 `operator quint64()` 或按通道调用 `red()` 等函数。

### 8.2 把 `quint64` 原始值当作可移植编码

`fromRgba64(quint64)` 和转换运算符服务于 QRgba64 内部表示。写入网络或文件前必须定义自己的字节序和字段顺序。

### 8.3 把 `fromRgba()` 误写成简单左移

8 位到 16 位的展开是复制高 8 位到低 8 位，即 `x * 257` 的等价形式。`0x80` 应变成 `0x8080`，不是 `0x8000`。

### 8.4 认为 `red8()` 只是取高字节

Qt 会进行近似除以 257 的四舍五入。需要与 Qt 的 8 位颜色转换保持一致时，调用 `red8()` 等 API，不要用自定义的 `>> 8` 代替。

### 8.5 忽略预乘状态

同一个四通道数值在预乘和非预乘管线中含义不同。出现边缘变暗、透明区域颜色异常或重复合成问题时，先确认每个阶段的 alpha 表示。

### 8.6 以为透明值一定会清空 RGB

`unpremultiplied()` 对 alpha 为零时直接返回原值。只有 `premultiplied()` 的透明特殊分支明确返回全零表示；手工构造的透明对象可能仍然带有非零 RGB。

### 8.7 默认构造对象一定是零

头文件中的默认构造函数是 `= default`，普通局部变量的默认初始化不应依赖它自动清零：

```cpp
QRgba64 uninitialized; // 不要读取其中的通道
QRgba64 transparent{}; // 值初始化为全零
```

需要确定值时使用 `QRgba64{}` 或工厂函数。

## 9. 相关辅助函数

头文件还提供几个与类成员配套的非成员函数：

- `qRgba64(r, g, b, a)`：调用四通道版 `fromRgba64()`。
- `qRgba64(quint64 c)`：把已有的 64 位表示包装成 `QRgba64`。
- `qPremultiply(c)`：调用 `c.premultiplied()`。
- `qUnpremultiply(c)`：调用 `c.unpremultiplied()`。
- `qRed(c)`、`qGreen(c)`、`qBlue(c)`、`qAlpha(c)`：返回对应的 8 位通道值。

Qt 6.11.1 还提供 `qHash(QRgba64, size_t)`，因此可以直接把 `QRgba64` 用作 `QHash` 或 `QSet` 的键。该显式 hash 重载自 Qt 6.11.1 引入；较早版本主要依靠到 `quint64` 的隐式转换参与哈希。

## 10. 逐项 API 说明

### 构造和原始表示

#### `QRgba64::QRgba64()`

默认构造 `QRgba64`。像 `QRgba64 value;` 这样的普通默认初始化不应当被当作全零值；需要零值时使用 `QRgba64{}`。实际读取前应确保对象已经通过工厂、赋值或值初始化设置。

#### `[static constexpr] QRgba64 QRgba64::fromRgba64(quint64 c)`

把已有的 `quint64` 内部表示包装成 `QRgba64`。它不重新排列通道、不执行端序转换、不做范围校验。

#### `[static constexpr] QRgba64 QRgba64::fromRgba64(quint16 r, quint16 g, quint16 b, quint16 a)`

从四个 16 位通道创建 `QRgba64`，通道顺序为 red、green、blue、alpha。所有输入都已经处于完整的 `0..65535` 取值范围，不需要额外钳制。

#### `[static constexpr] QRgba64 QRgba64::fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)`

从四个 8 位 RGBA 通道创建 16 位颜色。每个通道通过 `x | (x << 8)` 展开到 16 位，alpha 也按相同规则处理。

#### `[static constexpr] QRgba64 QRgba64::fromArgb32(uint rgb)`

从 `0xAARRGGBB` 数值构造 16 位颜色。它先提取 8 位 alpha、red、green、blue，再使用 8 位到 16 位的精确展开。

#### `[constexpr] QRgba64::operator quint64() const`

返回 QRgba64 的 64 位内部表示。它适合底层代码或同一约定下的快速传递；跨平台序列化时应自行处理字节序。

#### `[noexcept] QRgba64 &QRgba64::operator=(quint64 rgba)`

把指定的 64 位内部表示直接写入对象并返回 `*this`。它不做通道重排或合法性检查。

### 通道读取

#### `[constexpr] quint16 QRgba64::red() const`

返回 16 位 red 通道的原始值。

#### `[constexpr] quint16 QRgba64::green() const`

返回 16 位 green 通道的原始值。

#### `[constexpr] quint16 QRgba64::blue() const`

返回 16 位 blue 通道的原始值。

#### `[constexpr] quint16 QRgba64::alpha() const`

返回 16 位 alpha 通道的原始值。

#### `[constexpr] quint8 QRgba64::red8() const`

将 red 从 16 位按 Qt 的除以 257 舍入规则降为 8 位，不是简单取高字节。

#### `[constexpr] quint8 QRgba64::green8() const`

将 green 从 16 位降为 8 位，使用与 `red8()` 相同的舍入规则。

#### `[constexpr] quint8 QRgba64::blue8() const`

将 blue 从 16 位降为 8 位，使用与 `red8()` 相同的舍入规则。

#### `[constexpr] quint8 QRgba64::alpha8() const`

将 alpha 从 16 位降为 8 位，使用与 `red8()` 相同的舍入规则。

### alpha 状态

#### `[constexpr] bool QRgba64::isOpaque() const`

当 alpha 等于 `0xffff` 时返回 `true`。这是精确的满 alpha 判断，不是近似判断。

#### `[constexpr] bool QRgba64::isTransparent() const`

当 alpha 等于 `0` 时返回 `true`。alpha 位于两者之间时表示部分透明。

### 通道写入

#### `void QRgba64::setRed(quint16 red)`

只替换 red 通道，保留 green、blue、alpha。输入已经是 `quint16`，不存在浮点钳制；修改 red 也不会改变预乘约定。

#### `void QRgba64::setGreen(quint16 green)`

只替换 green 通道，保留其他三个通道。

#### `void QRgba64::setBlue(quint16 blue)`

只替换 blue 通道，保留其他三个通道。

#### `void QRgba64::setAlpha(quint16 alpha)`

只替换 alpha 通道，不会自动按新 alpha 重新预乘或还原 RGB。若对象代表预乘颜色，修改 alpha 后需要由调用方重新建立一致的 RGB。

### 预乘转换

#### `[constexpr] QRgba64 QRgba64::premultiplied() const`

返回 alpha 预乘后的副本。满 alpha 直接返回当前值；零 alpha 返回全零；部分 alpha 对 RGB 做 16 位整数预乘和舍入，alpha 保持不变。

#### `[constexpr] QRgba64 QRgba64::unpremultiplied() const`

返回非预乘副本。满 alpha 或零 alpha 时直接返回当前值；部分 alpha 按 alpha 还原 RGB。零 alpha 无法恢复原 RGB，因此该函数不会凭空生成原始颜色。

### 打包输出

#### `[constexpr] uint QRgba64::toArgb32() const`

把四个 16 位通道按舍入规则降为 8 位并打包成 `0xAARRGGBB`。结果仍只是通道打包，不会自动改变预乘状态。

#### `[constexpr] ushort QRgba64::toRgb16() const`

把颜色打包成 RGB565：red 5 位、green 6 位、blue 5 位。alpha 被忽略，通道采用位截取，不适合需要精确舍入或透明度的场景。

### 相关非成员

#### `[constexpr] QRgba64 qRgba64(quint16 r, quint16 g, quint16 b, quint16 a)`

四通道版便捷工厂，等价于 `QRgba64::fromRgba64(r, g, b, a)`。

#### `[constexpr] QRgba64 qRgba64(quint64 c)`

原始 64 位表示版便捷工厂，等价于 `QRgba64::fromRgba64(c)`。

#### `[constexpr] QRgba64 qPremultiply(QRgba64 c)`

调用 `c.premultiplied()` 并返回结果。

#### `[constexpr] QRgba64 qUnpremultiply(QRgba64 c)`

调用 `c.unpremultiplied()` 并返回结果。

#### `[constexpr] uint qRed(QRgba64 c)`、`qGreen(QRgba64 c)`、`qBlue(QRgba64 c)`、`qAlpha(QRgba64 c)`

返回相应通道的 8 位值，分别等价于 `c.red8()`、`c.green8()`、`c.blue8()`、`c.alpha8()`。

#### `[constexpr noexcept, since 6.11.1] size_t qHash(QRgba64 key, size_t seed = 0)`

返回用于哈希容器的哈希值。`seed` 用于随机化或组合哈希计算；该重载从 Qt 6.11.1 起公开提供。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QRgba64()` | 默认构造一个值对象 | `QRgba64 value;` 不应假定为零；需要零值用 `QRgba64{}` |
| 静态工厂 | `fromRgba64(quint64 c)` | 包装现有 64 位表示 | 不做端序转换；原始值不是通用序列化格式 |
| 静态工厂 | `fromRgba64(quint16 r, quint16 g, quint16 b, quint16 a)` | 创建四个 16 位通道颜色 | 顺序是 RGBA，通道范围为 `0..65535` |
| 静态工厂 | `fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)` | 从 8 位 RGBA 提升到 16 位 | 使用 `x * 257` 等价展开，不是 `x << 8` |
| 静态工厂 | `fromArgb32(uint rgb)` | 从 `0xAARRGGBB` 创建颜色 | 按数值位解释，不按内存字节顺序解释 |
| 原始表示 | `operator quint64() const` | 取得内部 64 位表示 | 适合同一约定下的底层互操作；跨平台传输需自定义端序 |
| 原始表示 | `operator=(quint64 rgba)` | 写入内部 64 位表示 | 直接赋值，不重排、不校验 |
| 16 位读取 | `red()` / `green()` / `blue()` / `alpha()` | 读取原始 16 位通道 | 返回 `quint16`，不会归一化 |
| 8 位读取 | `red8()` / `green8()` / `blue8()` / `alpha8()` | 将通道量化为 8 位 | 使用除以 257 的舍入规则，不是简单取高字节 |
| 状态 | `isOpaque()` | 判断 alpha 是否为 `0xffff` | 精确满 alpha 判断 |
| 状态 | `isTransparent()` | 判断 alpha 是否为 `0` | 零 alpha 不代表可以恢复原 RGB |
| 写入 | `setRed(quint16)` / `setGreen(quint16)` | 修改 red 或 green | 不影响其他通道，不自动维护预乘关系 |
| 写入 | `setBlue(quint16)` / `setAlpha(quint16)` | 修改 blue 或 alpha | 改 alpha 不会重新计算 RGB |
| 转换 | `premultiplied()` | 返回预乘 alpha 的副本 | 零 alpha 返回全零；重复调用会重复预乘 |
| 转换 | `unpremultiplied()` | 返回非预乘副本 | alpha 为零时原样返回，无法恢复 RGB |
| 打包 | `toArgb32()` | 降为 `0xAARRGGBB` | 16 位到 8 位会舍入，仍不改变预乘状态 |
| 打包 | `toRgb16()` | 输出 RGB565 | 只保留 5/6/5 位 RGB，alpha 丢失 |
| 辅助工厂 | `qRgba64(...)` | `fromRgba64()` 的便捷形式 | 同样区分四通道参数和原始 `quint64` |
| 辅助转换 | `qPremultiply()` / `qUnpremultiply()` | 调用对应成员转换 | 不会记录转换状态 |
| 辅助读取 | `qRed()` / `qGreen()` / `qBlue()` / `qAlpha()` | 读取 8 位通道 | 等价于对应的 `*8()` 成员函数 |
| 哈希 | `qHash(QRgba64, size_t seed = 0)` | 为 `QHash`/`QSet` 提供哈希 | Qt 6.11.1 新增显式重载 |

---

### 一句话总结

`QRgba64` 是四个 16 位通道组成的紧凑 RGBA 值：适合高精度整数像素处理和预乘 alpha 管线；使用时要分清原始 64 位表示、`ARGB32` 数值打包、RGB565 输出以及当前的预乘状态。
