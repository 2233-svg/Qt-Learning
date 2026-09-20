# QCameraDevice：描述一台可用摄像头

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCameraDevice>`  
> 所属模块：`Qt6::Multimedia`  
> 类型性质：隐式共享值类型  
> 相关类型：`QMediaDevices`、`QCamera`、`QCameraFormat`

## 1. 它解决什么问题

`QCameraDevice` 是“摄像头设备清单中的一项”。它保存某个物理摄像头的标识、显示名称、前后置位置、可用视频格式和照片分辨率等描述信息。

它不负责打开摄像头，也不输出视频帧。真正控制设备运行的是 `QCamera`：

```text
QMediaDevices::videoInputs()
        |
        v
QCameraDevice  --选择设备和能力-->  QCamera
                                      |
                                      v
                              QMediaCaptureSession
```

因此，枚举设备时使用 `QCameraDevice`，启动采集时把选中的设备传给 `QCamera`：

```cpp
const QList<QCameraDevice> devices = QMediaDevices::videoInputs();
if (!devices.isEmpty()) {
    QCamera camera(devices.first());
    // camera 仍需连接 QMediaCaptureSession，并处理权限后再 start()
}
```

## 2. 典型使用场景

### 2.1 让用户选择摄像头

`QMediaDevices::videoInputs()` 返回系统当前可见的摄像头列表。界面可以显示 `description()`，内部保存对应的 `QCameraDevice` 或 `id()`，用户确认后构造 `QCamera`。

`description()` 适合给人看，`id()` 更适合日志、配置和重新匹配设备。不要把显示名称当作唯一键，因为多个设备可能有相同名称。

### 2.2 选择采集规格

通过 `videoFormats()` 查看设备支持的分辨率、像素格式和帧率范围，再把选中的 `QCameraFormat` 传给 `QCamera::setCameraFormat()`。照片分辨率则由 `photoResolutions()` 提供。

列表为空并不一定表示 API 出错，也可能是设备无效、权限尚未就绪或平台后端没有提供对应能力。

### 2.3 判断前后置和旋转补偿

移动设备通常用 `position()` 区分前置和后置摄像头。视频显示或图像处理还可能需要使用 `correctionAngle()` 补偿摄像头在硬件上的安装方向。

`correctionAngle()` 是相对于设备原生方向的固定补偿角度，不会随着设备当前旋转方向改变。显示层仍需结合当前屏幕方向决定最终变换。

## 3. 构建与发现设备

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

```cpp
#include <QCameraDevice>
#include <QMediaDevices>

const QList<QCameraDevice> cameras = QMediaDevices::videoInputs();
for (const QCameraDevice &camera : cameras) {
    qDebug() << camera.description()
             << camera.id()
             << camera.videoFormats();
}
```

设备列表属于 `QMediaDevices` 的职责。应用应监听 `QMediaDevices::videoInputsChanged()`，因为 USB 摄像头插拔、系统权限变化和浏览器设备授权都可能让列表发生变化。

## 4. 生命周期、所有权和有效性

### 4.1 它是值类型，不拥有硬件

`QCameraDevice` 是 `Q_GADGET` 值类型，不继承 `QObject`，没有 parent，也不能通过它直接释放或锁定摄像头。复制它只复制设备描述，不会复制一个正在运行的摄像头实例。

它采用隐式共享，放进 `QList`、作为函数返回值或按值传递通常成本较低。设备信息仍可能在系统层发生变化，所以长时间缓存后应重新从 `QMediaDevices` 获取列表并用 `id()` 重新匹配。

### 4.2 默认构造代表空设备

`QCameraDevice()` 构造的是空、无效的设备描述。用 `isNull()` 判断它是否无效。不要把空设备当成一个可以直接打开的摄像头。

如果需要系统默认摄像头，优先使用 `QMediaDevices::defaultVideoInput()`；如果是给 `QCamera` 设置设备，Qt 也支持用默认构造的 `QCameraDevice` 请求默认设备，但仍应检查 camera 的可用性和错误。

### 4.3 描述信息不是实时控制状态

`videoFormats()`、`photoResolutions()` 和其它属性描述的是枚举时后端报告的能力。它们不会因为 `QCamera` 当前是否 active 而自动变成实时状态，也不保证每一次启动都能成功使用某个格式。

最终能否打开还受权限、设备占用、平台后端和当前采集链路影响。选择设备之后，仍要处理 `QCamera::errorOccurred()`。

## 5. 关键 API 语义

### 5.1 `id()`

返回设备标识 `QByteArray`。它用于区分设备和持久化选择结果，通常不适合作为用户界面文字。

设备标识的具体格式由平台后端决定，应用不应解析其中的私有结构。设备重新插拔后，某些平台可能改变标识，因此持久化配置应准备好“原设备不存在”的分支。

### 5.2 `description()`

返回人类可读的摄像头名称，例如厂商名或系统显示名。它适合放入设备选择框，但不保证唯一，也不保证跨系统语言和版本稳定。

### 5.3 `isDefault()`

表示该描述是否对应系统当前默认摄像头。默认设备可能因系统设置、设备插拔或权限状态变化而改变。它不是“硬件永远是默认设备”的永久标记。

### 5.4 `position()`

返回摄像头在硬件上的物理位置：

- `UnspecifiedPosition`：位置未知或平台没有提供信息；
- `BackFace`：设备背面摄像头；
- `FrontFace`：设备正面摄像头。

桌面 USB 摄像头通常可能返回 `UnspecifiedPosition`，不能因为不是前置或后置就认为设备无效。

### 5.5 `videoFormats()`

返回摄像头支持的 `QCameraFormat` 列表。每个格式包含：

- `resolution()`：视频分辨率；
- `pixelFormat()`：视频帧像素格式；
- `minFrameRate()` 和 `maxFrameRate()`：该格式允许的帧率范围。

实际选择时应从这个列表中挑选，而不是自行构造 `QCameraFormat`，因为它的有效构造函数是私有的。设置格式后，仍应读取 `QCamera::cameraFormat()` 确认后端最终采用的值。

### 5.6 `photoResolutions()`

返回设备可以用于静态图像捕获的分辨率列表。它和 `videoFormats()` 是两套能力描述：视频能支持某个尺寸，不代表拍照一定支持同一尺寸，反之亦然。

列表中的分辨率是能力信息，不是对 `QImageCapture` 的强制设置接口。具体拍照结果还会受图像格式、裁剪和平台实现影响。

### 5.7 `correctionAngle()`

Qt 6.7 引入。返回补偿物理摄像头安装方向所需的 `QtVideo::Rotation`。它通常用于把摄像头原始画面转成设备原生方向下更自然的显示方向。

该值相对于设备的 native orientation，因此不应在每次屏幕旋转时修改或累加。应把摄像头补偿角与当前窗口或屏幕方向分别计算。

### 5.8 `isNull()` 与比较运算

`isNull()` 在描述为空或无效时返回 `true`。`operator==`、`operator!=` 比较两个设备描述是否相同，适合比较当前选择与列表中的设备。

不要用 `description()` 比较设备，也不要只用列表下标持久化选择。更可靠的流程是优先按 `id()` 匹配，匹配失败后再让用户重新选择。

## 6. 线程、异步和平台边界

`QCameraDevice` 本身是轻量值对象，调用 getter 不会打开设备，也不会启动异步采集。设备枚举和设备变化由 `QMediaDevices` 管理，应用需要按平台处理权限和异步通知。

在 WebAssembly 等环境中，设备列表可能在权限请求或浏览器授权后才完整。不要在应用刚创建时把一次 `videoInputs()` 结果当作永久清单。

如果设备描述来自 GUI 或媒体对象所在的线程，建议在该线程完成枚举和对象连接；跨线程传递值类型本身通常没有所有权问题，但不要把它误认为跨线程使用同一个摄像头资源。

## 7. 常见误区

- 把 `QCameraDevice` 当成已经打开的摄像头：它只是描述信息。
- 只保存 `description()`：名称不唯一且可能变化。
- 把 `videoFormats()` 当成拍照分辨率列表：拍照能力应看 `photoResolutions()`。
- 看到 `UnspecifiedPosition` 就判定设备坏了：很多桌面设备没有前后置语义。
- 设置了一个旧列表中的格式后不重新确认：设备切换或后端协商可能使最终格式不同。
- 忽略 `isNull()`：默认构造对象和无设备场景必须单独处理。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCameraDevice()` | 构造空的摄像头设备描述。 | 用 `isNull()` 判断有效性；它不打开硬件。 |
| 构造 | `QCameraDevice(const QCameraDevice &other)` | 复制设备描述。 | 复制的是值，不是运行中的 camera。 |
| 析构 | `~QCameraDevice()` | 销毁设备描述值。 | 不负责释放摄像头硬件。 |
| 赋值 | `QCameraDevice &operator=(const QCameraDevice &other)` | 替换当前设备描述。 | 赋值后应重新读取所有能力属性。 |
| 比较 | `operator==(const QCameraDevice &, const QCameraDevice &)` | 判断两个设备描述是否相同。 | 不要用显示名称替代设备比较。 |
| 比较 | `operator!=(const QCameraDevice &, const QCameraDevice &)` | 判断两个设备描述是否不同。 | 适合检测选择是否变化。 |
| 查询 | `bool isNull() const` | 判断描述是否为空或无效。 | 空对象不能直接作为可用设备使用。 |
| 查询 | `QByteArray id() const` | 返回平台设备标识。 | 适合保存和匹配；不要解析私有格式。 |
| 查询 | `QString description() const` | 返回人类可读名称。 | 适合显示；不保证唯一和稳定。 |
| 查询 | `bool isDefault() const` | 判断是否为系统默认摄像头。 | 默认设备会随系统状态变化。 |
| 类型 | `enum Position` | 表示未知、后置或前置位置。 | 桌面摄像头常为 `UnspecifiedPosition`。 |
| 查询 | `Position position() const` | 返回硬件位置。 | 这是物理位置，不是视频画面方向。 |
| 查询 | `QList<QSize> photoResolutions() const` | 返回静态图像捕获分辨率。 | 与视频格式列表分开理解。 |
| 查询 | `QList<QCameraFormat> videoFormats() const` | 返回支持的视频采集格式。 | 从列表选择后交给 `QCamera`。 |
| 查询 | `QtVideo::Rotation correctionAngle() const` | 返回物理安装方向补偿角。 | Qt 6.7 起提供；相对于 native orientation。 |

## 9. 一句话总结

`QCameraDevice` 是摄像头的“能力和身份描述”，负责发现、展示和选择；打开设备、处理权限和运行状态应交给 `QCamera`。
