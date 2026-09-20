# Qt QColorSpace::PrimaryPoints 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QColorSpace>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 定位：RGB 色域的原色坐标值类型

## 1. 它解决什么问题

一个 RGB 色彩空间不能只用“红、绿、蓝三个颜色名称”描述。颜色管理需要知道三个原色在 CIE 1931 xy 色度图中的位置，以及哪个白点代表“中性白”。`QColorSpace::PrimaryPoints` 就是承载这四个二维坐标的轻量值类型：

- `whitePoint`：白点；
- `redPoint`：红原色；
- `greenPoint`：绿原色；
- `bluePoint`：蓝原色。

它描述的是**色域的几何边界和参考白点**，不是一个 `QColor`，也不是完整的颜色空间。伽马曲线、传递函数、颜色模型等信息仍然由 `QColorSpace` 负责。

实际使用中，它主要出现在三类场景：

1. 根据标准原色创建自定义 RGB `QColorSpace`；
2. 读取 ICC、显示器或相机资料后检查原色坐标是否合理；
3. 在颜色转换、色域分析或调试工具中展示某个 RGB 空间的色域参数。

## 2. 构建与包含

`PrimaryPoints` 是 `QColorSpace` 内的公开嵌套结构体，通常通过 `QColorSpace` 头文件使用：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QColorSpace>
```

它是普通值类型：可以直接创建、复制、返回和放入容器，不需要事件循环，也没有 QObject 父对象或手动释放要求。

## 3. 最小可用代码

下面示例取得 sRGB 的标准原色点，并在交给消费者前做合理性检查：

```cpp
#include <QColorSpace>
#include <QDebug>

void inspectSrgbPrimaries()
{
    const QColorSpace::PrimaryPoints points =
        QColorSpace::PrimaryPoints::fromPrimaries(QColorSpace::SRgb);

    if (!points.isValid()) {
        qWarning() << "Primary points are not usable";
        return;
    }

    qDebug() << "white =" << points.whitePoint
             << "red =" << points.redPoint
             << "green =" << points.greenPoint
             << "blue =" << points.bluePoint;
}
```

`fromPrimaries()` 的参数是 `QColorSpace::Primaries`，不是 `QColorSpace::NamedColorSpace`。两者都描述颜色空间相关概念，但枚举用途不同，不能因为都包含 `SRgb` 等名字就混用。

## 4. 数据模型与边界

### 4.1 四个点是 CIE xy 坐标

每个字段都是 `QPointF`，其 `x`、`y` 分量表示色度坐标，而不是像素坐标，也不是 XYZ 三刺激值。典型的 xy 坐标满足：

```text
x >= 0
y >= 0
x + y <= 1
```

但实际能否组成一个可用 RGB 色域，还要同时考虑四个点之间的几何关系和白点位置。因此不要只检查四个数是否落在 0 到 1 之间，就断定结构有效。

### 4.2 `isValid()` 是消费者使用的合理性检查

`isValid()` 返回的是 Qt 内部消费者所需的 sanity check 结果。它适合在把结构传给创建颜色空间或颜色转换相关 API 前调用，但它不是完整的色彩科学证明，也不会保证所有自定义数据都符合你的业务标准。

特别是：

- 默认构造的结构体字段是默认的 `QPointF`，通常不代表有效的 RGB 原色；
- `NaN`、无穷大、退化或明显越界的坐标不应继续传递；
- `isValid()` 为 `false` 时，不要假设后续 API 会抛异常；Qt 的许多值类型 API 使用无效对象或失败返回值表达错误；
- 即使结构有效，也只说明原色点通过该检查，不等于已经拥有完整的传递函数和颜色模型。

### 4.3 这是公开字段结构，不是封装属性

四个成员是公开的 `QPointF` 字段，可以直接读取和修改：

```cpp
QColorSpace::PrimaryPoints points =
    QColorSpace::PrimaryPoints::fromPrimaries(QColorSpace::DisplayP3);
points.greenPoint = QPointF(0.30, 0.60);

if (points.isValid()) {
    // 交给需要原色点的 QColorSpace API。
}
```

修改字段后要重新调用 `isValid()`。结构体不会在每次字段赋值时自动通知，也不会自动更新某个已经创建好的 `QColorSpace`；如果颜色空间对象已经建立，修改这个独立副本不会反向修改原对象。

## 5. 真实使用场景

### 5.1 创建自定义 RGB 颜色空间

当设备资料给出白点、RGB 原色和传递函数时，可以把原色部分组织成 `PrimaryPoints`，再交给 `QColorSpace` 的相应构造函数或设置接口。这里要把职责拆开：

- `PrimaryPoints`：回答“色域顶点和白点在哪里”；
- `QColorSpace`：保存颜色模型、原色、传递函数和颜色空间身份；
- `QColorTransform`：把一个具体颜色或像素从源空间映射到目标空间。

不要把 `PrimaryPoints` 当作一个可以直接给 `QImage` 设置的颜色空间对象。

### 5.2 显示器、相机和图片元数据检查

读取 EDID、ICC 或相机配置时，可以先将外部数据转成四个 `QPointF`，再调用 `isValid()`。这一步应当位于“解析外部输入”和“创建 Qt 颜色空间”之间，避免异常坐标污染后续转换。

外部文件是非可信输入。除了 `isValid()`，还应按业务需要检查：

- 坐标是否在允许的精度和范围内；
- 原色三角形是否退化；
- 白点是否位于合理位置；
- 传递函数参数是否与原色点来自同一份配置。

### 5.3 颜色管理调试工具

调试界面可以将四个点绘制在 xy 色度图上，或者打印它们与 sRGB、Display P3 等预置空间的差异。绘图坐标需要做自己的坐标变换；`PrimaryPoints` 中的 `QPointF` 不是窗口像素坐标，不能直接当作 `QPainter` 的屏幕位置使用。

## 6. 线程、生命周期与性能

`PrimaryPoints` 只包含四个 `QPointF` 值，没有 QObject 线程归属，也不依赖 GUI 线程。只要不同线程不同时修改同一个共享对象，它可以像普通值一样在线程间传递。

常见做法是在线程中解析或计算原色点，在线程边界传递一个值副本；真正涉及 GUI、屏幕或平台色彩配置的操作，仍需遵守相关类自己的线程约束。

它本身非常轻量，通常不需要缓存策略。需要缓存的是由这些参数进一步生成的 `QColorSpace` 或 `QColorTransform`，尤其是会被大量像素重复使用的颜色转换对象。

## 7. 常见误区

### 7.1 把 xy 坐标当成 RGB 分量

`QPointF(0.64, 0.33)` 表示色度图中的位置，不表示红色通道值为 0.64、绿色通道值为 0.33。它不能直接传给 `QColor::fromRgbF()`。

### 7.2 混淆 `Primaries` 和命名颜色空间

`fromPrimaries()` 接受的是 `QColorSpace::Primaries`。如果手头只有 `QColorSpace::SRgb` 这样的命名颜色空间枚举，应先确认目标 API 要的是命名空间还是原色枚举，必要时使用对应的 `QColorSpace` 对象取得信息。

### 7.3 只检查一个点

四个点共同定义 RGB 色域。单独检查白点或红点没有意义；应把整个结构交给 `isValid()`，并在外部数据场景补充业务级校验。

### 7.4 以为修改结构会更新颜色空间

`PrimaryPoints` 是独立值。修改它只改变这个结构本身，不会改变从它之前创建出来的 `QColorSpace` 或 `QColorTransform`。

## 8. 与相关类型的协作

- `QColorSpace::Primaries`：描述可由 `fromPrimaries()` 查找的标准原色集合。
- `QColorSpace`：把原色点与颜色模型、传递函数等组合成完整颜色空间。
- `QColorTransform`：由源 `QColorSpace` 和目标 `QColorSpace` 生成，用于实际颜色转换。
- `QPointF`：承载每个 CIE xy 坐标。
- `QImage`：保存带颜色空间信息的图像，并可使用 `QColorTransform` 做整图转换。

## 9. 逐项 API 说明

### `QColorSpace::PrimaryPoints::fromPrimaries()`

```cpp
static QColorSpace::PrimaryPoints
QColorSpace::PrimaryPoints::fromPrimaries(QColorSpace::Primaries primaries)
```

**作用：** 根据一个预定义的 `QColorSpace::Primaries` 枚举值返回对应的四个原色点。

**参数语义：**

- `primaries` 必须是 Qt 支持的原色枚举值；
- 它选择的是原色集合，不是传递函数，也不是完整颜色空间；
- 不应把 `NamedColorSpace` 枚举直接传入此 API。

**返回值与边界：**

- 返回一个按值传递的 `PrimaryPoints`；
- 对受支持的枚举值，返回对应标准的白点、红点、绿点和蓝点；
- 对未识别或不适合表示原色的值，不要假设结果有效，使用前调用 `isValid()`；
- 该函数不修改任何已有的 `QColorSpace` 对象。

### `QColorSpace::PrimaryPoints::isValid()`

```cpp
bool QColorSpace::PrimaryPoints::isValid() const noexcept
```

**作用：** 检查四个点是否通过 Qt 消费 `PrimaryPoints` 时使用的基本合理性检查。

**返回值：**

- `true`：结构满足该检查，可以继续交给需要原色点的 API；
- `false`：结构不应被当作有效 RGB 原色集合使用。

**边界：**

- 只做检查，不修复字段，也不抛异常；
- 不会验证完整颜色空间的传递函数、色度学来源或业务约束；
- 函数是 `noexcept`，适合在输入校验路径中直接调用。

### 公开数据成员

| 数据成员 | 类型 | 含义 |
| --- | --- | --- |
| `whitePoint` | `QPointF` | RGB 颜色空间的参考白点 CIE xy 坐标。 |
| `redPoint` | `QPointF` | 红原色 CIE xy 坐标。 |
| `greenPoint` | `QPointF` | 绿原色 CIE xy 坐标。 |
| `bluePoint` | `QPointF` | 蓝原色 CIE xy 坐标。 |

这些字段没有单独的 setter，也没有变更信号。修改后由调用者负责再次校验。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 静态函数 | `static QColorSpace::PrimaryPoints fromPrimaries(QColorSpace::Primaries primaries)` | 从 Qt 预置原色枚举取得四个 CIE xy 点。 | 参数是 `Primaries`，不是 `NamedColorSpace`；返回值仍应调用 `isValid()`。 |
| 查询函数 | `bool isValid() const noexcept` | 判断原色结构是否通过 Qt 的基本合理性检查。 | 不等于完整色彩科学验证，也不会修复无效坐标。 |
| 数据成员 | `QPointF whitePoint` | 保存参考白点。 | 是 CIE xy 色度坐标，不是屏幕像素位置。 |
| 数据成员 | `QPointF redPoint` | 保存红原色坐标。 | 与另外三个点共同定义 RGB 色域。 |
| 数据成员 | `QPointF greenPoint` | 保存绿原色坐标。 | 修改后要重新检查整个结构。 |
| 数据成员 | `QPointF bluePoint` | 保存蓝原色坐标。 | 不要把它当作蓝色通道的数值。 |

---

### 一句话总结

`QColorSpace::PrimaryPoints` 是描述 RGB 色域的四个 CIE xy 坐标的值类型；它负责原色几何信息，不负责完整颜色空间和像素转换。
