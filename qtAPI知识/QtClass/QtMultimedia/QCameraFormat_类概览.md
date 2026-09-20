# QCameraFormat：描述一种视频采集规格

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCameraFormat>`  
> 所属模块：`Qt6::Multimedia`  
> 类型性质：隐式共享值类型  
> 相关类型：`QCameraDevice`、`QCamera`、`QVideoFrameFormat`

## 1. 它解决什么问题

`QCameraFormat` 把摄像头的一种视频采集规格组合成一个值。这个组合由三部分组成：

1. `resolution()`：视频分辨率；
2. `pixelFormat()`：视频帧像素格式；
3. `minFrameRate()` 和 `maxFrameRate()`：该规格支持的帧率范围。

它不是一个“任意填写参数的配置结构体”。公开 API 没有提供设置分辨率、像素格式或帧率的 setter，正常做法是从 `QCameraDevice::videoFormats()` 获取有效格式，然后把某一项传给 `QCamera::setCameraFormat()`。

```cpp
const QCameraDevice device = QMediaDevices::defaultVideoInput();
const QList<QCameraFormat> formats = device.videoFormats();
if (!formats.isEmpty()) {
    camera.setCameraFormat(formats.first());
}
```

## 2. 典型使用场景

### 2.1 在预览质量和性能之间选择

高分辨率通常带来更高的带宽、内存和处理成本；扫码、视觉检测等场景可能更关心稳定帧率和可处理的像素格式。遍历格式列表后，可以根据分辨率、帧率范围和像素格式筛选。

### 2.2 为视频处理选择像素格式

`pixelFormat()` 返回 `QVideoFrameFormat::PixelFormat`。它描述摄像头或后端提供的视频帧格式，不等于应用最终在屏幕上看到的颜色空间，也不保证不同平台对同一格式名称提供完全相同的底层布局。

接收 `QVideoFrame` 时应读取实际帧的 `pixelFormat()` 和平面信息，不能只根据请求过的 `QCameraFormat` 猜测内存布局。

### 2.3 选择设备支持的帧率范围

一个 `QCameraFormat` 通常表示一个帧率区间，而不是一个固定帧率。`minFrameRate()` 和 `maxFrameRate()` 是后端为该规格报告的边界。具体运行帧率还可能受到设备负载、曝光时间、平台协商和采集管线影响。

## 3. 构建与来源

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

```cpp
#include <QCameraFormat>
#include <QMediaDevices>

const QCameraDevice device = QMediaDevices::defaultVideoInput();
for (const QCameraFormat &format : device.videoFormats()) {
    qDebug() << format.resolution()
             << format.pixelFormat()
             << format.minFrameRate()
             << format.maxFrameRate();
}
```

`QCameraFormat` 的构造函数只有默认构造和拷贝构造，真正带有设备能力的格式由 Qt Multimedia 后端创建。应用不应尝试通过私有构造函数或手动拼接一个格式。

## 4. 生命周期和有效性

### 4.1 默认构造是空格式

`QCameraFormat()` 构造空格式，`isNull()` 返回 `true`。空格式没有可用的分辨率、像素格式或帧率范围，不能当作一个有效采集规格提交给 camera。

### 4.2 它不拥有设备和视频流

这是值类型，不继承 `QObject`，不拥有 `QCameraDevice`、摄像头硬件或视频帧。复制、赋值和把它放入容器不会启动采集，也不会改变设备状态。

格式对象可以安全地作为选择结果保存一段时间，但设备列表和后端能力可能发生变化。设备切换后应重新从新设备的 `videoFormats()` 取得格式，不要把旧设备格式直接套用到新设备。

### 4.3 最终格式可能需要确认

调用 `QCamera::setCameraFormat()` 是向后端提交选择。应用应监听 `cameraFormatChanged()`，并通过 `camera.cameraFormat()` 读取最终状态。设备不支持的格式或设备暂时无法打开时，不能只根据 setter 已调用就认为协商成功。

## 5. 关键 API 语义

### 5.1 `resolution()`

返回该视频规格的宽度和高度。它是采集规格中的原始尺寸，不等于预览控件的显示尺寸，也不等于后续处理时的裁剪或缩放尺寸。

宽高可能受摄像头传感器方向影响。视频帧到达后仍应结合 `QVideoFrameFormat::viewport()`、旋转信息和后端行为判断如何显示。

### 5.2 `pixelFormat()`

返回视频帧的像素格式。常见格式包括 JPEG、YUV 等，但具体可用值取决于设备和平台。

同一个逻辑格式在不同平台可能有不同的平面数量、步长和对齐方式。将帧映射到 CPU 内存时，应以 `QVideoFrame` 的实际 plane 信息为准；不要把所有 YUV 格式都当成同一种内存排列。

### 5.3 `minFrameRate()` 与 `maxFrameRate()`

返回该规格报告的最低和最高帧率，单位是每秒帧数。边界是 `float`，应用不应使用字符串比较或假定一定是整数。

这两个值表达支持范围，不保证 camera 在所有场景都能持续达到最高帧率。曝光时间、光线不足、处理阻塞和平台驱动都可能导致实际帧率变化。

### 5.4 `isNull()`

返回当前格式是否是默认构造的空格式。它只判断格式对象本身是否有后端数据，不表示对应物理摄像头当前是否在线。

### 5.5 `operator==` 与 `operator!=`

比较两个格式的值是否相同，适合判断用户选择是否改变、检查 camera 当前格式是否等于列表中的某项。比较格式不等于比较设备：不同摄像头可以报告完全相同的格式。

## 6. 选择格式的实用策略

下面的筛选逻辑只从设备报告的列表中选择，并把“优先满足条件”和“没有完全匹配时的回退”分开：

```cpp
QCameraFormat selected;
for (const QCameraFormat &candidate : device.videoFormats()) {
    if (candidate.resolution() == QSize(1920, 1080)
        && candidate.minFrameRate() <= 30.0f
        && candidate.maxFrameRate() >= 30.0f) {
        selected = candidate;
        break;
    }
}

if (!selected.isNull())
    camera.setCameraFormat(selected);
```

真实项目中通常还要：

- 根据处理模块是否支持该像素格式做筛选；
- 对列表为空和没有匹配项提供回退；
- 设置后读取 `camera.cameraFormat()`；
- 在设备改变时重新筛选；
- 预览、录像和图像处理分别评估内存和带宽成本。

## 7. 线程、异步和平台边界

`QCameraFormat` getter 是值查询，不会触发设备 I/O，也没有自己的信号或事件循环。异步行为属于 `QCamera` 和 `QMediaCaptureSession`。

格式对象可以跨线程按值传递，但把它传给 `QCamera::setCameraFormat()` 仍应遵守 `QCamera` 所在线程和 QObject 连接规则。不要因为格式是值类型，就在任意线程直接操作 camera。

## 8. 常见误区

- 自己构造一个分辨率和像素格式就认为 camera 支持：有效格式应来自 `videoFormats()`。
- 把 `maxFrameRate()` 当成实际恒定帧率：它只是能力上界。
- 根据格式名猜 `QVideoFrame` 内存布局：应检查实际帧的 plane 和 stride。
- 把格式对象当成设备句柄：它不拥有硬件。
- 忘记空格式：默认构造格式必须先用 `isNull()` 排除。
- 切换摄像头后继续使用旧格式：设备能力可能完全不同。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCameraFormat()` | 构造空的视频格式。 | `isNull()` 为 `true`，不能作为有效规格使用。 |
| 构造 | `QCameraFormat(const QCameraFormat &other)` | 复制视频格式。 | 复制的是值，不会启动采集。 |
| 析构 | `~QCameraFormat()` | 销毁格式值。 | 不影响摄像头或视频流。 |
| 赋值 | `QCameraFormat &operator=(const QCameraFormat &other)` | 替换当前格式值。 | 赋值不会自动提交给 `QCamera`。 |
| 查询 | `QVideoFrameFormat::PixelFormat pixelFormat() const` | 返回视频帧像素格式。 | 以实际 `QVideoFrame` 平面布局为准。 |
| 查询 | `QSize resolution() const` | 返回视频采集分辨率。 | 不是预览控件尺寸。 |
| 查询 | `float minFrameRate() const` | 返回规格支持的最低帧率。 | 单位 fps；是能力边界。 |
| 查询 | `float maxFrameRate() const` | 返回规格支持的最高帧率。 | 不保证运行中持续达到。 |
| 查询 | `bool isNull() const noexcept` | 判断格式是否为空。 | 设备格式列表为空时要有回退路径。 |
| 比较 | `bool operator==(const QCameraFormat &other) const` | 比较两个格式值是否相同。 | 相同格式不代表来自同一设备。 |
| 比较 | `bool operator!=(const QCameraFormat &other) const` | 判断两个格式值是否不同。 | 适合检测用户选择变化。 |

## 10. 一句话总结

`QCameraFormat` 是摄像头视频能力的一个“已验证规格项”，负责描述分辨率、像素格式和帧率范围；它应从 `QCameraDevice` 的格式列表中取得，再交给 `QCamera` 协商。
