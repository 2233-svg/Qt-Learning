# Qt QRgbaFloat：RGBA 浮点颜色值

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRgbaFloat>`  
> 所属模块：`Qt6::Gui`  
> 引入版本：Qt 6.2  
> 类型形式：`template <typename F> class QRgbaFloat`

## 1. 它解决什么问题

`QRgbaFloat<F>` 是一个只保存四个通道的 RGBA 浮点值类型。它把红、绿、蓝、透明度分别存放在 `r`、`g`、`b`、`a` 中，适合在需要浮点颜色数据的绘制、像素转换、颜色混合或图形后端适配代码中传递一个颜色。

它和 `QColor` 的职责不同：

- `QRgbaFloat` 只表示四个数值通道，不保存色彩空间、色温、颜色名称或转换上下文。
- 它允许通道暂时处在 `[0, 1]` 之外，适合中间计算；`QColor` 更偏向完整的颜色对象和颜色空间 API。
- 它不记录当前值是否已经预乘 alpha。`premultiplied()` 和 `unpremultiplied()` 返回转换后的副本，调用方需要自己维护当前数据的约定。
- 它不是 `QImage` 的像素格式，也不会自动和 `QColor`、`QRgba64` 或图像缓冲区互相转换。

模板参数 `F` 只有两种合法选择：

- `qfloat16`：对应 `QRgbaFloat16`，四个 16 位浮点通道，总大小为 64 bit。
- `float`：对应 `QRgbaFloat32`，四个 32 位浮点通道，总大小为 128 bit。

因此，`QRgbaFloat<double>` 不是受支持的实例化形式。日常代码优先使用两个别名，除非确实需要显式写出模板类型。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QRgbaFloat>
```

qmake 工程使用：

```qmake
QT += gui
```

这是头文件值类型，使用对象本身不需要创建 `QGuiApplication`。但如果后续把它交给窗口、图像或图形后端，仍要遵守那些 API 自身的初始化和线程要求。

## 3. 最小使用方式

```cpp
#include <QRgbaFloat>

QRgbaFloat32 makeColor()
{
    // 输入 8 位 RGBA，结果的通道约为 red / 255.0f 等。
    return QRgbaFloat32::fromRgba(32, 128, 224, 255);
}

uint packColor(QRgbaFloat32 color)
{
    // 导出时会把每个通道先钳制到 [0, 1]，再量化为 8 位。
    return color.toArgb32();
}
```

直接聚合初始化也可以：

```cpp
QRgbaFloat32 color{0.1f, 0.2f, 0.3f, 1.0f};
```

不要把下面这种未初始化的局部对象当作透明黑：

```cpp
QRgbaFloat32 color; // 局部对象的 r、g、b、a 没有被自动清零
```

需要零初始化时写成 `QRgbaFloat32{}`，或显式使用四个初值。值初始化得到的四个通道都是零。

## 4. 数值和表示语义

### 4.1 原始通道不是强制归一化值

`r`、`g`、`b`、`a` 是公开数据成员，构造聚合对象或调用 `setRed()` 等 setter 时都可以写入任意可转换为 `F` 的 `float` 值。Qt 不会在写入时自动把它们限制在 `[0, 1]`。

例如：

```cpp
QRgbaFloat32 color{1.4f, -0.1f, 0.5f, 0.75f};

float rawRed = color.red();           // 1.4f
float displayRed = color.redNormalized(); // 1.0f
```

`red()`、`green()`、`blue()`、`alpha()` 返回原始通道；`redNormalized()` 等函数通过钳制返回 `[0, 1]` 范围内的值。整数读取函数使用归一化值，因此也会钳制：

- 小于 `0` 的通道按 `0` 导出。
- 大于 `1` 的通道按 `1` 导出。
- 中间值按对应位深度四舍五入。

这意味着 `toArgb32()` 适合显示或打包，不适合保存 HDR 或超出范围的中间值。

### 4.2 8 位、16 位输入是归一化转换

`fromRgba()` 把四个 `quint8` 通道按 `255.0` 缩放；`fromRgba64()` 把四个 `quint16` 通道按 `65535.0` 缩放。两者都会得到未预乘的 RGBA 值：

```cpp
auto c8 = QRgbaFloat32::fromRgba(255, 128, 0, 64);
// red 约为 1.0，green 约为 128 / 255，alpha 约为 64 / 255

auto c16 = QRgbaFloat16::fromRgba64(65535, 32768, 0, 65535);
```

`fromArgb32()` 的参数按 `0xAARRGGBB` 解释，而不是按内存中的字节顺序解释：

```cpp
auto color = QRgbaFloat32::fromArgb32(0x80402010u);
// alpha = 0x80 / 255，red = 0x40 / 255
// green = 0x20 / 255，blue = 0x10 / 255
```

### 4.3 alpha 判定是比较，不是“接近”判断

`isOpaque()` 实际判断 `a >= 1.0f`，`isTransparent()` 实际判断 `a <= 0.0f`：

- alpha 在 `(0, 1)` 内时，两个函数都返回 `false`，表示半透明。
- alpha 小于 `0` 时，`isTransparent()` 为 `true`，即使这个值不是通常意义上的合法 alpha。
- alpha 大于 `1` 时，`isOpaque()` 为 `true`。
- 如果 alpha 是 NaN，两个比较都不成立，两个函数都会返回 `false`。

如果业务需要“约等于不透明”或“非法值拒绝”，应在调用前自行定义容差和校验策略。

## 5. 预乘与非预乘

未预乘 RGBA 通常表示颜色通道独立于 alpha，例如：

```text
r = 1.0, g = 0.0, b = 0.0, a = 0.5
```

预乘形式则保存：

```text
r = r * a, g = g * a, b = b * a, a = a
```

调用 `premultiplied()` 会返回这样的副本，不改变原对象。它直接用原始 `r`、`g`、`b`、`a` 相乘，不会先把任何通道钳制到 `[0, 1]`。

调用 `unpremultiplied()` 时有两个重要边界：

- `a <= 0`：返回全通道为零的值，避免除以零；原来的 RGB 不会被保留。
- `a >= 1`：直接返回当前值的副本。
- `0 < a < 1`：用 `1 / a` 还原 RGB，alpha 保持不变。

这两个函数不会标记或追踪“已经转换过”。重复调用 `premultiplied()` 会再次乘 alpha；对已预乘数据调用 `unpremultiplied()` 才是有意义的还原。转换前必须明确数据的当前约定。

## 6. 实际使用场景

### 6.1 在 CPU 像素循环中保留浮点精度

需要多次做颜色叠加、滤波、曝光调整或透明度计算时，可以先把整数像素转成 `QRgbaFloat32`，在浮点域计算，最后一次性量化回 `QRgb` 或图像像素。

注意：`QRgbaFloat` 只负责四通道数值，颜色空间转换、gamma/线性空间转换和裁剪策略仍需由应用或其他 API 完成。

### 6.2 在渲染数据和 Qt 值类型之间传递颜色

图形代码常常需要在普通 C++ 结构、着色器参数准备阶段和 Qt 绘制辅助代码之间传递四个通道。`QRgbaFloat32` 适合作为明确的值对象，`QRgbaFloat16` 则适合带宽或存储大小更敏感的场景。

它不能替代图形 API 的格式声明。把 `QRgbaFloat16` 的内存直接当作某个 GPU 格式上传前，仍要确认目标 API 对浮点 16 位布局、对齐、通道顺序和端序的要求。

### 6.3 在整数颜色格式之间做明确的桥接

`fromArgb32()` / `toArgb32()` 适合与 `QRgb` 风格的打包整数衔接；`fromRgba()` / `fromRgba64()` 适合逐通道转换。不要把 `uint` 的内存字节序和 `ARGB32` 的数值表示混为一谈。

## 7. 生命周期、所有权和线程

`QRgbaFloat` 是无 QObject 父子关系的值类型：

- 不需要 `new`、`delete` 或事件循环。
- 不拥有外部内存，也不持有图像、窗口或 GPU 资源。
- 可以按值返回、复制、放入 Qt 容器或作为函数参数传递。
- 仅访问其自身数据时没有 QObject 线程归属问题。

但“值类型本身可跨线程”不等于使用它的整个算法自动线程安全。如果多个线程共享同一个实例并通过公开字段或 setter 写入，仍需同步；只读副本通常更简单。

## 8. 常见误区与排查顺序

### 8.1 把 `red()` 当成始终位于 `[0, 1]`

错误原因：原始通道允许超出范围。  
排查方式：需要显示、打包或传给要求归一化输入的 API 时使用 `redNormalized()` 或先自行验证；需要保留中间计算结果时才使用 `red()`。

### 8.2 误以为 setter 会自动修正非法值

`setRed()`、`setGreen()`、`setBlue()`、`setAlpha()` 只是把 `float` 转换为模板参数 `F` 后写入。它们不会钳制、不会检查 NaN，也不会因为修改 alpha 而自动重新预乘 RGB。

### 8.3 把 alpha 的存储形式和预乘状态混为一谈

预乘只改变 RGB 的数值，alpha 仍然独立保存。`a == 0` 时，预乘结果的 RGB 必然为零；非预乘数据即使 alpha 为零，也可能暂时带有 RGB，但 `unpremultiplied()` 会按 Qt 实现返回全零值。

### 8.4 直接把 `QRgbaFloat` 当成完整颜色模型

本类不含色彩空间、传递函数、白点、HDR 元数据或透明度合成规则。进入显示管线前，应明确是否需要线性化、色域转换、预乘和最终量化。

### 8.5 忽略量化损失和 `qfloat16` 精度

从浮点转 8 位或 16 位整数会发生量化；使用 `QRgbaFloat16` 还会发生半精度存储。若算法对微小差异敏感，计算阶段可使用 `QRgbaFloat32`，最后再转成较低精度格式。

### 8.6 使用未初始化对象

聚合类型没有把普通局部变量自动清零。出现颜色随机变化时，先检查是否写成了 `QRgbaFloat32 color;`，以及是否所有四个通道都已赋值。

## 9. 相关类型如何选择

- `QRgbaFloat16`：四个 `qfloat16` 通道，适合存储体积较小、可以接受半精度的中间值或交换数据。
- `QRgbaFloat32`：四个 `float` 通道，适合计算和需要更宽数值范围的场景。
- `QRgba64`：整数 16 位 RGBA 表示；当数据本来就是固定精度整数像素时，不必绕道浮点。
- `QRgb`：32 位打包的 `0xAARRGGBB` 数值；适合传统 8 位通道像素。
- `QColor`：需要颜色空间、颜色模型和更高层颜色操作时使用。

这些类型之间没有隐式的“全部自动转换”契约。选择转换函数时，应同时确认通道顺序、位深、是否预乘以及是否允许超出 `[0, 1]`。

## 10. 逐项 API 说明

### 模板参数与公开数据成员

#### `template <typename F> class QRgbaFloat`

`F` 必须是 `qfloat16` 或 `float`。模板类按 `r`、`g`、`b`、`a` 的顺序保存四个通道，并按 `sizeof(F) * 4` 对齐。

#### `using QRgbaFloat::Type = F`

公开别名，表示实际通道存储类型。`QRgbaFloat16::Type` 是 `qfloat16`，`QRgbaFloat32::Type` 是 `float`。

#### `using QRgbaFloat::FastType`

用于实现乘法等运算的辅助类型。Qt 6.11.1 文档将它描述为 `float`；特定支持原生半精度乘法的编译配置可能采用模板参数本身。应用代码不应依赖它作为稳定的存储格式。

#### `F QRgbaFloat::r`

红色通道的公开存储成员。它是原始值，不保证位于 `[0, 1]`。

#### `F QRgbaFloat::g`

绿色通道的公开存储成员。它是原始值，不保证位于 `[0, 1]`。

#### `F QRgbaFloat::b`

蓝色通道的公开存储成员。它是原始值，不保证位于 `[0, 1]`。

#### `F QRgbaFloat::a`

alpha 通道的公开存储成员。它是原始值；`isOpaque()` 和 `isTransparent()` 会直接用它与 `1.0`、`0.0` 比较。

### 静态成员

#### `[static constexpr] QRgbaFloat<T> QRgbaFloat::fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)`

从四个 8 位 RGBA 通道构造浮点颜色。每个输入通道除以 `255`，结果为未预乘值。alpha 参数也按相同规则转换。

#### `[static constexpr] QRgbaFloat<T> QRgbaFloat::fromRgba64(quint16 red, quint16 green, quint16 blue, quint16 alpha)`

从四个 16 位 RGBA 通道构造浮点颜色。每个输入通道除以 `65535`，适合从 `QRgba64` 风格的逐通道数据转换。

#### `[static constexpr] QRgbaFloat<T> QRgbaFloat::fromArgb32(uint rgb)`

从数值形式的 `0xAARRGGBB` 构造颜色。高 8 位是 alpha，接着是 red、green、blue；返回值仍是未预乘的浮点颜色。

### 通道读取

#### `[constexpr] float QRgbaFloat::red() const`

返回原始红色通道。对 `QRgbaFloat16` 会把半精度存储值转换为 `float`；不执行钳制。

#### `[constexpr] float QRgbaFloat::green() const`

返回原始绿色通道，不执行钳制。

#### `[constexpr] float QRgbaFloat::blue() const`

返回原始蓝色通道，不执行钳制。

#### `[constexpr] float QRgbaFloat::alpha() const`

返回原始 alpha 通道，不执行钳制。

#### `[constexpr] float QRgbaFloat::redNormalized() const`

把红色通道钳制到 `[0, 1]` 后返回。整数导出函数使用同样的归一化规则。

#### `[constexpr] float QRgbaFloat::greenNormalized() const`

把绿色通道钳制到 `[0, 1]` 后返回。

#### `[constexpr] float QRgbaFloat::blueNormalized() const`

把蓝色通道钳制到 `[0, 1]` 后返回。

#### `[constexpr] float QRgbaFloat::alphaNormalized() const`

把 alpha 通道钳制到 `[0, 1]` 后返回。它只改变读取结果，不修改对象中的 `a`。

### 整数读取与打包

#### `[constexpr] quint8 QRgbaFloat::red8() const`

读取归一化红色并乘以 `255` 后四舍五入为 `quint8`。

#### `[constexpr] quint8 QRgbaFloat::green8() const`

读取归一化绿色并量化为 8 位。

#### `[constexpr] quint8 QRgbaFloat::blue8() const`

读取归一化蓝色并量化为 8 位。

#### `[constexpr] quint8 QRgbaFloat::alpha8() const`

读取归一化 alpha 并量化为 8 位。

#### `[constexpr] quint16 QRgbaFloat::red16() const`

读取归一化红色并乘以 `65535` 后四舍五入为 `quint16`。

#### `[constexpr] quint16 QRgbaFloat::green16() const`

读取归一化绿色并量化为 16 位。

#### `[constexpr] quint16 QRgbaFloat::blue16() const`

读取归一化蓝色并量化为 16 位。

#### `[constexpr] quint16 QRgbaFloat::alpha16() const`

读取归一化 alpha 并量化为 16 位。

#### `[constexpr] uint QRgbaFloat::toArgb32() const`

将四个归一化通道量化后打包成 `0xAARRGGBB`。它不会保留超出 `[0, 1]` 的浮点范围，也不会把结果解释为预乘像素。

### alpha 状态

#### `[constexpr] bool QRgbaFloat::isOpaque() const`

当原始 alpha `a >= 1.0` 时返回 `true`。它不是基于 `alphaNormalized()` 的近似判断。

#### `[constexpr] bool QRgbaFloat::isTransparent() const`

当原始 alpha `a <= 0.0` 时返回 `true`。alpha 位于 `(0, 1)` 时返回 `false`。

### 通道写入

#### `void QRgbaFloat::setRed(float red)`

把 `red` 转换为 `F` 后写入红色通道。不钳制、不改变其他通道，也不会自动处理预乘关系。

#### `void QRgbaFloat::setGreen(float green)`

把 `green` 转换为 `F` 后写入绿色通道。不钳制。

#### `void QRgbaFloat::setBlue(float blue)`

把 `blue` 转换为 `F` 后写入蓝色通道。不钳制。

#### `void QRgbaFloat::setAlpha(float alpha)`

把 `alpha` 转换为 `F` 后写入 alpha 通道。不钳制，也不会按新 alpha 重新计算 RGB。

### 预乘转换

#### `[constexpr] QRgbaFloat<T> QRgbaFloat::premultiplied() const`

返回 `{r * a, g * a, b * a, a}` 的副本。乘法使用原始通道，因此调用方应先确定数据范围和当前预乘状态。

#### `[constexpr] QRgbaFloat<T> QRgbaFloat::unpremultiplied() const`

当 `a <= 0` 时返回全零值；当 `a >= 1` 时返回当前值副本；其余情况用 alpha 的倒数恢复 RGB，alpha 原样保留。它不会恢复因半精度或量化已经丢失的信息。

### 比较运算

#### `[constexpr] bool QRgbaFloat::operator==(QRgbaFloat other) const`

逐一比较 `r`、`g`、`b`、`a`，使用的是精确的 `==`。这是数值逐字段相等，不是带容差的颜色相似判断；含 NaN 的通道不会与自身相等。

#### `[constexpr] bool QRgbaFloat::operator!=(QRgbaFloat other) const`

等价于 `!(*this == other)`。需要误差容忍时应自行比较四个通道。

### 相关别名

#### `using QRgbaFloat16 = QRgbaFloat<qfloat16>`

四个 16 位浮点通道组成的 64 位值类型。存储更紧凑，但通道精度和中间计算稳定性低于 `QRgbaFloat32`。

#### `using QRgbaFloat32 = QRgbaFloat<float>`

四个 32 位浮点通道组成的 128 位值类型。适合通常的浮点颜色计算和交换。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 类型 | `template <typename F> class QRgbaFloat` | 保存四个 RGBA 浮点通道 | `F` 只支持 `qfloat16` 或 `float` |
| 类型别名 | `QRgbaFloat::Type` | 暴露实际存储类型 | 不等于读取函数的返回类型；读取统一返回 `float` |
| 类型别名 | `QRgbaFloat::FastType` | 为内部乘法提供辅助浮点类型 | 不要把它当作稳定的存储或 ABI 契约 |
| 数据成员 | `F r` | 红色原始通道 | 可超出 `[0, 1]`，普通局部对象可能未初始化 |
| 数据成员 | `F g` | 绿色原始通道 | setter 不钳制 |
| 数据成员 | `F b` | 蓝色原始通道 | setter 不钳制 |
| 数据成员 | `F a` | alpha 原始通道 | `isOpaque()`/`isTransparent()` 直接比较原始值 |
| 静态构造 | `fromRgba(quint8, quint8, quint8, quint8)` | 从 8 位 RGBA 生成未预乘浮点值 | 每通道除以 `255` |
| 静态构造 | `fromRgba64(quint16, quint16, quint16, quint16)` | 从 16 位 RGBA 生成未预乘浮点值 | 每通道除以 `65535` |
| 静态构造 | `fromArgb32(uint)` | 从 `0xAARRGGBB` 生成未预乘浮点值 | 按数值位解释，不是按内存字节序解释 |
| 读取 | `red()` / `green()` / `blue()` / `alpha()` | 读取原始通道 | 不钳制，可能得到负数、超范围或 NaN |
| 读取 | `redNormalized()` / `greenNormalized()` / `blueNormalized()` / `alphaNormalized()` | 读取 `[0, 1]` 范围通道 | 不修改对象；超范围值会被钳制 |
| 8 位读取 | `red8()` / `green8()` / `blue8()` / `alpha8()` | 归一化后量化为 8 位 | 先钳制，再四舍五入 |
| 16 位读取 | `red16()` / `green16()` / `blue16()` / `alpha16()` | 归一化后量化为 16 位 | 先钳制，再四舍五入 |
| 打包 | `toArgb32()` | 导出 `0xAARRGGBB` | 不保留 HDR/超范围值，不改变预乘状态 |
| 状态 | `isOpaque()` | 判断 `a >= 1.0` | 不是近似比较；NaN 返回 `false` |
| 状态 | `isTransparent()` | 判断 `a <= 0.0` | alpha 在 `(0, 1)` 时返回 `false` |
| 写入 | `setRed(float)` / `setGreen(float)` | 写入 RGB 通道 | 转换为 `F`，不钳制、不自动预乘 |
| 写入 | `setBlue(float)` / `setAlpha(float)` | 写入蓝色或 alpha 通道 | 修改 alpha 不会重新计算 RGB |
| 转换 | `premultiplied()` | 返回 RGB 乘 alpha 的副本 | 直接使用原始值；重复调用会再次乘 alpha |
| 转换 | `unpremultiplied()` | 返回非预乘副本 | `a <= 0` 返回全零；`a >= 1` 原样返回 |
| 比较 | `operator==` / `operator!=` | 四个通道精确逐字段比较 | 无容差；NaN 不与自身相等 |
| 别名 | `QRgbaFloat16` | `QRgbaFloat<qfloat16>` | 64 bit，紧凑但精度较低 |
| 别名 | `QRgbaFloat32` | `QRgbaFloat<float>` | 128 bit，适合通常浮点计算 |

---

### 一句话总结

`QRgbaFloat` 是一个轻量的 RGBA 浮点值容器：写入时不替你约束数值，读取和整数导出时才提供归一化路径；使用它时最重要的是明确通道范围、预乘状态、位深和颜色空间，而不是把它当作带完整色彩管理的 `QColor`。
