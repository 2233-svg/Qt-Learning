# QtVideo：视频呈现方向的枚举命名空间

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtVideo>`  
> 所属模块：`Qt6::Multimedia`  
> 类型性质：命名空间，包含视频方向枚举
> 引入版本：Qt 6.7

## 它解决什么问题

视频帧的像素内存可能没有按照最终显示方向存储。例如手机横竖屏切换后，原始像素仍是同一块宽高数据，但显示端需要旋转 90 度或 270 度。

`QtVideo::Rotation` 用类型安全的枚举表达显示前的顺时针旋转角度。`QVideoFrame` 和 `QVideoFrameFormat` 使用它保存呈现元数据，因此旋转不会要求应用先复制并改写底层像素。

它不是矩阵、图像变换器或视频帧对象。真正的旋转由视频输出、渲染器或应用自己的绘制代码执行。

## 实际使用场景

- 摄像头输出带有设备方向信息，需要在预览中保持人像方向。
- 读取视频帧元数据并在自定义 `QVideoSink` 渲染时应用旋转。
- 在 `QVideoFrameFormat` 中设置一组自定义帧的显示方向。
- 用统一的枚举替代旧式整数旋转角度。

## 方向语义

旋转在视频坐标中定义，坐标的 Y 轴向下，因此方向与 `QTransform::rotate()` 的顺时针显示效果一致。

| 枚举 | 数值 | 含义 |
| --- | ---: | --- |
| `QtVideo::Rotation::None` | `0` | 不旋转，帧方向已经正确 |
| `QtVideo::Rotation::Clockwise90` | `90` | 顺时针旋转 90 度 |
| `QtVideo::Rotation::Clockwise180` | `180` | 顺时针旋转 180 度 |
| `QtVideo::Rotation::Clockwise270` | `270` | 顺时针旋转 270 度 |

`Clockwise270` 等价于逆时针 90 度，但使用哪个枚举应以视频显示坐标为准，不要把图像坐标系和数学坐标系混在一起。

## 与 `QVideoFrameFormat` 的关系

```cpp
QVideoFrameFormat format(QSize(1280, 720), QVideoFrameFormat::Format_BGRA8888);
format.setRotation(QtVideo::Rotation::Clockwise90);

QVideoFrame frame(image);
frame.setRotation(QtVideo::Rotation::Clockwise90);
```

格式和帧都可以携带旋转信息。具体管线中应明确由哪一层负责最终显示，避免同时在上游元数据和下游绘制代码中重复旋转。

旋转只描述呈现方式：

- 不交换 `frameSize()` 的底层像素宽高；
- 不改变 `pixelFormat()`；
- 不重新排列平面数据；
- 不保证任意输出都自动应用。

如果应用调用 `QVideoFrame::toImage()` 后自行绘制，应读取旋转元数据并决定是否执行变换；不要假设 `toImage()` 已经替你完成显示方向修正。

## 与镜像、裁剪的边界

旋转和镜像是不同的元数据。旋转表示绕显示方向转动，镜像表示沿显示轴翻转。摄像头预览常常同时需要旋转和水平镜像，应用应确认输出对象的应用顺序。

旋转也不改变 viewport。视频帧可能同时带有有效显示矩形和旋转信息，裁剪、缩放与旋转的处理顺序应由渲染层统一规定。

## 版本和兼容性

`QtVideo::Rotation` 从 Qt 6.7 引入。旧代码可能使用 `QVideoFrameFormat::RotationAngle` 或整数角度；新代码应改用强类型枚举，并在跨 Qt 版本的代码中用版本宏隔离兼容层。

## 常见误区

- 把 `QtVideo::Rotation` 当成会立即旋转 `QImage` 的函数。
- 以为设置旋转会改变底层 `frameSize()` 或像素平面。
- 把顺时针方向按数学坐标的 Y 轴向上理解。
- 在摄像头元数据和自定义渲染器中重复应用同一旋转。
- 忘记旧版整数角度和 Qt 6.7+ 强类型枚举之间的 API 差异。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 命名空间 | `QtVideo` | 放置视频呈现相关枚举。 | 不能实例化。 |
| 枚举 | `QtVideo::Rotation` | 表示显示前的顺时针旋转角度。 | Qt 6.7 引入。 |
| 枚举值 | `Rotation::None` | 不旋转。 | 角度为 0。 |
| 枚举值 | `Rotation::Clockwise90` | 顺时针旋转 90 度。 | 只描述呈现元数据。 |
| 枚举值 | `Rotation::Clockwise180` | 顺时针旋转 180 度。 | 不改写像素。 |
| 枚举值 | `Rotation::Clockwise270` | 顺时针旋转 270 度。 | 等价于逆时针 90 度的显示方向。 |

### 一句话总结

`QtVideo::Rotation` 只表达“显示时应如何转”，不负责真正执行图像变换。
