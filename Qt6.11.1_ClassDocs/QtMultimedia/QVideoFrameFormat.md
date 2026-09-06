# QVideoFrameFormat

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QVideoFrameFormat` 是 Qt Multimedia 的“视频帧格式”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QVideoFrameFormat` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QVideoFrameFormat>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

### 状态、生命周期和线程

**生命周期：** 设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

**状态与结果：** 区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

**线程与事件循环：** 媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

## 3. 直接使用

先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ColorRange { ColorRange_Unknown, ColorRange_Video, ColorRange_Full }`
- `enum ColorSpace { ColorSpace_Undefined, ColorSpace_BT601, ColorSpace_BT709, ColorSpace_AdobeRgb, ColorSpace_BT2020 }`
- `enum ColorTransfer { ColorTransfer_Unknown, ColorTransfer_BT709, ColorTransfer_BT601, ColorTransfer_Linear, ColorTransfer_Gamma22, …, ColorTransfer_STD_B67 }`
- `enum Direction { TopToBottom, BottomToTop }`
- `enum PixelFormat { Format_Invalid, Format_ARGB8888, Format_ARGB8888_Premultiplied, Format_XRGB8888, Format_BGRA8888, …, Format_YUV420P10 }`

### 公有函数

- `QVideoFrameFormat()`
- `QVideoFrameFormat(const QSize &size, QVideoFrameFormat::PixelFormat format)`
- `QVideoFrameFormat(const QVideoFrameFormat &other)`
- `QVideoFrameFormat(QVideoFrameFormat &&other)`
- `~QVideoFrameFormat()`
- `QVideoFrameFormat::ColorRange colorRange() const`
- `QVideoFrameFormat::ColorSpace colorSpace() const`
- `QVideoFrameFormat::ColorTransfer colorTransfer() const`
- `int frameHeight() const`
- `qreal frameRate() const`
- `QSize frameSize() const`
- `int frameWidth() const`
- `bool isMirrored() const`
- `bool isValid() const`
- `QVideoFrameFormat::PixelFormat pixelFormat() const`
- `int planeCount() const`
- `QtVideo::Rotation rotation() const`
- `QVideoFrameFormat::Direction scanLineDirection() const`
- `void setColorRange(QVideoFrameFormat::ColorRange range)`
- `void setColorSpace(QVideoFrameFormat::ColorSpace colorSpace)`
- `void setColorTransfer(QVideoFrameFormat::ColorTransfer colorTransfer)`
- `void setFrameRate(qreal rate)`
- `void setFrameSize(const QSize &size)`
- `void setFrameSize(int width, int height)`
- `void setMaxLuminance(float lum)`
- `void setMirrored(bool mirrored)`
- `void setRotation(QtVideo::Rotation angle)`
- `void setScanLineDirection(QVideoFrameFormat::Direction direction)`
- `void setStreamFrameRate(qreal rate)`
- `void setViewport(const QRect &viewport)`
- `qreal streamFrameRate() const`
- `void swap(QVideoFrameFormat &other)`
- `QRect viewport() const`
- `bool operator!=(const QVideoFrameFormat &other) const`
- `QVideoFrameFormat & operator=(QVideoFrameFormat &&other)`
- `QVideoFrameFormat & operator=(const QVideoFrameFormat &other)`
- `bool operator==(const QVideoFrameFormat &other) const`

### 静态公有成员

- `QImage::Format imageFormatFromPixelFormat(QVideoFrameFormat::PixelFormat format)`
- `QVideoFrameFormat::PixelFormat pixelFormatFromImageFormat(QImage::Format format)`
- `QString pixelFormatToString(QVideoFrameFormat::PixelFormat pixelFormat)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QVideoFrameFormat::ColorRange`

**作用与语义：**

描述视频数据所使用的色彩范围。视频数据通常分为全色域，即所有数值均被使用，或为传统YUV视频格式中较有限的范围，使用所有数值的子集。
- `QVideoFrameFormat::ColorRange_Unknown`：`0`;视频的色彩范围未知。
- `QVideoFrameFormat::ColorRange_Video`：`1`
这是大多数YUV视频格式传统使用的色彩范围。对于8位格式，Y分量限制在16到235之间。U和V分量限制在16到240之间。
对于更高的位深，将这些数值乘以2^（depth-8）。
- `QVideoFrameFormat::ColorRange_Full`：`2`
全色域。所有从0到2^深度-1的值均有效。

### `enum QVideoFrameFormat::ColorSpace`

**作用与语义：**

枚举视频帧的颜色空间。
- `QVideoFrameFormat::ColorSpace_Undefined`: `0`; 未指定颜色空间。
- `QVideoFrameFormat::ColorSpace_BT601`: `1`; 由 ITU-R 推荐 BT.601 定义的颜色空间，Y 值范围从 16 到 235，Cb/Cr 范围从 16 到 240。主要用于针对 CRT 显示器的老视频。
- `QVideoFrameFormat::ColorSpace_BT709`: `2`; 由 ITU-R BT.709 定义的颜色空间，其值范围与 ColorSpace_BT601 相同。是目前最常用的颜色空间。
- `QVideoFrameFormat::ColorSpace_AdobeRgb`: `5`; 大多数 JPEG 文件使用的全范围 YUV 颜色空间。
- `QVideoFrameFormat::ColorSpace_BT2020`: `6`; 由 ITU-R BT.2020 定义的颜色空间。主要用于 HDR 视频。

### `enum QVideoFrameFormat::Direction`

**作用与语义：**

枚举视频扫描线的排列方向。
- `QVideoFrameFormat::TopToBottom`: `0`; 扫描线从帧的顶部到底部排列。
- `QVideoFrameFormat::BottomToTop`: `1`; 扫描线从帧的底部到顶部排列。

### `enum QVideoFrameFormat::PixelFormat`

**作用与语义：**

枚举视频数据类型。
- `QVideoFrameFormat::Format_Invalid`：`0`;该框架无效。
- `QVideoFrameFormat::Format_ARGB8888`：`1`;帧采用ARGB格式存储，每个分量为8位。
- `QVideoFrameFormat::Format_ARGB8888_Premultiplied`：`2`;采用预乘ARGB格式存储的帧，每个分量为8位。
- `QVideoFrameFormat::Format_XRGB8888`：`3`;采用每像素32位RGB格式（0xff、R、G、B）存储的帧。
- `QVideoFrameFormat::Format_BGRA8888`：`4`;帧使用32位BGRA格式（0xBBGGRRAA）存储。
- `QVideoFrameFormat::Format_BGRA8888_Premultiplied`：`5`;帧使用预乘法的32位BGRA格式存储。
- `QVideoFrameFormat::Format_ABGR8888`：`7`;帧采用32位ABGR格式（0xAABBGGRR）存储。
- `QVideoFrameFormat::Format_XBGR8888`：`8`;帧使用32位BGR格式（0xffBBGGRR）存储。
- `QVideoFrameFormat::Format_RGBA8888`：`9`;帧以字节 R、G、B、A/X 的形式存储在内存中，R 位于最低地址，A/X 位于最高地址。
- `QVideoFrameFormat::Format_BGRX8888`：`6`;帧以32位BGRx格式存储，[31：0] B：G：R：x 8：8：8：8：8小端序
- `QVideoFrameFormat::Format_RGBX8888`：`10`;帧存储在内存中，字节为 R、G、B、A/X，R 位于最低地址，A/X 位于最高地址。
- `QVideoFrameFormat::Format_AYUV`：`11`;帧使用打包的32位AYUV格式（0xAAYYUUVV）存储。
- `QVideoFrameFormat::Format_AYUV_Premultiplied`：`12`;帧使用打包预乘的32位AYUV格式（0xAAYYUUVV）存储。
- `QVideoFrameFormat::Format_YUV420P`：`13`;帧采用8位每组件平面YUV格式存储，U和V平面在水平和垂直上都被子采样，即U和V平面的高度和宽度均为Y平面的一半。
- `QVideoFrameFormat::Format_YUV422P`：`14`;帧采用8位每分量平面YUV格式存储，U和V平面水平子采样，即U和V平面宽度为Y平面的一半，U平面和V平面高度与Y相同。
- `QVideoFrameFormat::Format_YV12`：`15`;帧采用每组件8位平面YVU格式存储，V和U平面水平和垂直均有子采样，即V和U平面的高度和宽度为Y平面的一半。
- `QVideoFrameFormat::Format_UYVY`：`16`;帧采用8位每组件打包的YUV格式存储，U平面和V平面水平子采样（U-Y-V-Y），即两个水平相邻像素存储为32位宏像素，每个像素有Y值，且有常见的U和V值。
- `QVideoFrameFormat::Format_YUYV`：`17`;帧采用每组件8位打包的YUV格式存储，U平面和V平面水平子采样（Y-U-Y-V），即两个水平相邻像素存储为32位宏像素，每个像素有Y值，且有常见的U和V值。
- `QVideoFrameFormat::Format_NV12`：`18`;帧采用每组件8位半平面YUV格式存储，Y平面（Y），随后是水平和垂直采样的子采样、填充的UV平面（U-V）。
- `QVideoFrameFormat::Format_NV21`：`19`;帧采用每组件8位半平面YUV格式存储，Y平面（Y），随后是水平和垂直采样的打包VU平面（V-U）。
- `QVideoFrameFormat::Format_IMC1`：`20`;帧采用8位每组件平面YUV格式存储，U平面和V平面水平和垂直均被子采样。这与Format_YUV420P类型类似，但U和V平面每行字节填充至与Y平面相同的步幅。
- `QVideoFrameFormat::Format_IMC2`：`21`;帧采用每组件8位平面YUV格式存储，U和V平面水平和垂直均有子采样。这与Format_YUV420P类型类似，但U和V平面的线是交错的，即每行U数据后面跟一行V数据，形成与Y数据步幅相同的单行。
- `QVideoFrameFormat::Format_IMC3`：`22`;帧采用8位每分量平面YVU格式存储，V和U平面在水平和垂直上进行子采样。这与Format_YV12类型类似，但V和U平面每行字节的填充步幅与Y平面相同。
- `QVideoFrameFormat::Format_IMC4`：`23`;帧采用8位每分量平面YVU格式存储，V和U平面水平和垂直均有子采样。这与Format_YV12类型类似，但V和U平面的线是交错的，即每行V数据后面跟一行U数据，形成与Y数据步幅相同的单行。
- `QVideoFrameFormat::Format_P010`：`26`;帧采用每成分16位半平面YUV格式存储，Y平面（Y），后面是水平和垂直采样的子采样、填充的UV平面（U-V）。每个组件仅使用10位最高有效位。
- `QVideoFrameFormat::Format_P016`：`27`;帧采用每分量16位半平面YUV格式存储，Y平面（Y），后面是水平和垂直采样的打包UV平面（U-V）。
- `QVideoFrameFormat::Format_Y8`：`24`;帧采用8位灰度格式存储。
- `QVideoFrameFormat::Format_Y16`：`25`;帧采用16位线性灰度格式存储。小端序。
- `QVideoFrameFormat::Format_Jpeg`：`29`;帧以压缩后的Jpeg格式存储。
- `QVideoFrameFormat::Format_SamplerExternalOES`：`28`;帧以外部OES纹理格式存储。目前仅在Android上使用。
- `QVideoFrameFormat::Format_SamplerRect`：`30`;帧以矩形纹理格式（GL_TEXTURE_RECTANGLE）存储。该格式仅在macOS上使用基于OpenGL的渲染硬件接口。纹理中存储的底层像素格式为Format_BRGA8888。
- `QVideoFrameFormat::Format_YUV420P10`：`31`;类似于YUV420，但每个组件使用16位，其中10位为显著。

### `QVideoFrameFormat::QVideoFrameFormat()`

**作用与语义：**

构建一种零视频流格式。

### `QVideoFrameFormat::QVideoFrameFormat(const QSize &size, QVideoFrameFormat::PixelFormat format)`

**作用与语义：**

构建具有给定帧 `size` 和像素`format`的视频流。

### `QVideoFrameFormat::QVideoFrameFormat(const QVideoFrameFormat &other)`

**作用与语义：**

复制了`other`。

### `[constexpr noexcept] QVideoFrameFormat::QVideoFrameFormat(QVideoFrameFormat &&other)`

**作用与语义：**

通过从`other`移动构建QVideoFrameFormat。

### `[noexcept] QVideoFrameFormat::~QVideoFrameFormat()`

**作用与语义：**

会破坏视频流描述。

### `QVideoFrameFormat::ColorRange QVideoFrameFormat::colorRange() const`

**作用与语义：**

返回应用于渲染视频流的色彩范围。

### `QVideoFrameFormat::ColorSpace QVideoFrameFormat::colorSpace() const`

**作用与语义：**

返回视频流的色彩空间。

### `QVideoFrameFormat::ColorTransfer QVideoFrameFormat::colorTransfer() const`

**作用与语义：**

返回应用于渲染视频流的颜色传递函数。

### `int QVideoFrameFormat::frameHeight() const`

**作用与语义：**

返回视频流中的帧高度。

### `qreal QVideoFrameFormat::frameRate() const`

**作用与语义：**

返回视频流的帧率（帧每秒）。

### `QSize QVideoFrameFormat::frameSize() const`

**作用与语义：**

返回视频流中帧的尺寸。

### `int QVideoFrameFormat::frameWidth() const`

**作用与语义：**

返回视频流中的帧宽度。

### `[static] QImage::Format QVideoFrameFormat::imageFormatFromPixelFormat(QVideoFrameFormat::PixelFormat format)`

**作用与语义：**

返回的图像格式相当于视频帧像素`format`。如果没有等效格式，则返回`QImage::Format_Invalid`。
注意：一般来说`QImage`不处理YUV格式。

### `bool QVideoFrameFormat::isMirrored() const`

**作用与语义：**

如果曲面绕垂直轴镜像，返回`true`。
`QVideoFrameFormat`的变换，特别是旋转和镜像，可以通过摄像传感器的方向、摄像机设置或视频流的方向来确定。
镜像处理是在旋转后应用的。
注意：这里的镜像与`QImage::mirrored`不同，垂直镜像`QImage`会围绕其横轴进行镜像。

### `bool QVideoFrameFormat::isValid() const`

**作用与语义：**

识别视频表面格式是否具有有效的像素格式和帧大小。
如果格式有效，则返回 true;否则返回 false。

### `QVideoFrameFormat::PixelFormat QVideoFrameFormat::pixelFormat() const`

**作用与语义：**

返回视频流中帧的像素格式。

### `[static] QVideoFrameFormat::PixelFormat QVideoFrameFormat::pixelFormatFromImageFormat(QImage::Format format)`

**作用与语义：**

返回相当于图像`format`的视频像素格式。如果没有等效格式，则返回`QVideoFrameFormat::Format_Invalid`。
注意：一般来说`QImage`不处理YUV格式。

### `[static] QString QVideoFrameFormat::pixelFormatToString(QVideoFrameFormat::PixelFormat pixelFormat)`

**作用与语义：**

返回给定 `pixelFormat` 的字符串表示。

### `int QVideoFrameFormat::planeCount() const`

**作用与语义：**

返回使用的平面数。该数字取决于像素格式，基于RGB格式为1，基于YUV格式为1至3。

### `QtVideo::Rotation QVideoFrameFormat::rotation() const`

**作用与语义：**

返回顺时针旋转曲面的角度。
`QVideoFrameFormat`的变换，特别是旋转和镜像，可以通过摄像传感器的朝向、摄像机设置或视频流的朝向来确定。
旋转在镜像之前进行。

### `QVideoFrameFormat::Direction QVideoFrameFormat::scanLineDirection() const`

**作用与语义：**

返回扫描线的方向。

### `void QVideoFrameFormat::setColorRange(QVideoFrameFormat::ColorRange range)`

**作用与语义：**

将渲染视频流的颜色传输范围设置为`range`。

### `void QVideoFrameFormat::setColorSpace(QVideoFrameFormat::ColorSpace colorSpace)`

**作用与语义：**

设置视频流的 `colorSpace`。

### `void QVideoFrameFormat::setColorTransfer(QVideoFrameFormat::ColorTransfer colorTransfer)`

**作用与语义：**

将用于渲染视频流的颜色传递函数设置为`colorTransfer`。

### `void QVideoFrameFormat::setFrameRate(qreal rate)`

**作用与语义：**

将视频流的帧`rate`数设置为每秒帧数。

### `void QVideoFrameFormat::setFrameSize(const QSize &size)`

**作用与语义：**

将视频流中的帧大小设置为`size`。
这会重置`viewport()`，填满整个画面。

### `void QVideoFrameFormat::setFrameSize(int width, int height)`

**作用与语义：**

设置视频流中帧的帧数`width`和帧数`height`。
这会重置`viewport()`，填满整个画面。

### `void QVideoFrameFormat::setMaxLuminance(float lum)`

**作用与语义：**

将最大亮度设置为给定值`lum`。

### `void QVideoFrameFormat::setMirrored(bool mirrored)`

**作用与语义：**

如果曲面绕垂直轴`mirrored`，则集合。
`QVideoFrameFormat`的变换，特别是旋转和镜像，可以通过摄像传感器的朝向、摄像机设置或视频流的朝向来确定。
镜像处理是在旋转后应用的。
默认数值是`false`。
注意：这里的镜像与`QImage::mirrored`不同，垂直镜像`QImage`会围绕其横轴进行镜像。

### `void QVideoFrameFormat::setRotation(QtVideo::Rotation angle)`

**作用与语义：**

设定顺时针旋转表面的转`angle`。
`QVideoFrameFormat`的变换，特别是旋转和镜像，可以通过摄像传感器的方向、摄像机设置或视频流的方向来确定。
旋转在镜像之前进行。
默认值是`QtVideo::Rotation::None`。

### `void QVideoFrameFormat::setScanLineDirection(QVideoFrameFormat::Direction direction)`

**作用与语义：**

设置扫描线的 `direction`。

### `void QVideoFrameFormat::setStreamFrameRate(qreal rate)`

**作用与语义：**

将视频流的帧`rate`数设置为每秒帧数。

### `void QVideoFrameFormat::setViewport(const QRect &viewport)`

**作用与语义：**

将视频流的视口设置为`viewport`。

### `qreal QVideoFrameFormat::streamFrameRate() const`

**作用与语义：**

返回视频流的帧率（帧每秒）。

### `[noexcept] void QVideoFrameFormat::swap(QVideoFrameFormat &other)`

**作用与语义：**

将当前的视频帧格式与`other`交换。

### `QRect QVideoFrameFormat::viewport() const`

**作用与语义：**

返回视频流的视口。
视口是视频帧中实际显示的区域。
默认情况下，视口覆盖整帧。

### `bool QVideoFrameFormat::operator!=(const QVideoFrameFormat &other) const`

**作用与语义：**

如果`other`与该视频格式不同，则返回真;如果相同，则返回假。

### `[noexcept] QVideoFrameFormat &QVideoFrameFormat::operator=(QVideoFrameFormat &&other)`

**作用与语义：**

`other`进入这个`QVideoFrameFormat`。

### `QVideoFrameFormat &QVideoFrameFormat::operator=(const QVideoFrameFormat &other)`

**作用与语义：**

将`other`值赋予该对象。

### `bool QVideoFrameFormat::operator==(const QVideoFrameFormat &other) const`

**作用与语义：**

如果`other`与该视频格式相同，则返回true;如果不同，则返回false。

### `enum ColorTransfer { ColorTransfer_Unknown, ColorTransfer_BT709, ColorTransfer_BT601, ColorTransfer_Linear, ColorTransfer_Gamma22, …, ColorTransfer_STD_B67 }`

**作用与语义：**

- `QVideoFrameFormat::ColorTransfer_Unknown`：`0`;颜色传递函数未知。
- `QVideoFrameFormat::ColorTransfer_BT709`：`1`;颜色值按照BT709编码。另见 https://www.itu.int/rec/R-REC-BT.709/en。这接近但不完全相同的伽马曲线为2.2，且传输曲线与sRGB中使用相同。
- `QVideoFrameFormat::ColorTransfer_BT601`：`2`;颜色值按照BT601编码。参见 https://www.itu.int/rec/R-REC-BT.601/en。
- `QVideoFrameFormat::ColorTransfer_Linear`：`3`;颜色值为线性
- `QVideoFrameFormat::ColorTransfer_Gamma22`：`4`;颜色值编码为2.2的伽马
- `QVideoFrameFormat::ColorTransfer_Gamma28`：`5`;颜色值编码为2.8的伽马
- `QVideoFrameFormat::ColorTransfer_ST2084`：`6`;颜色值使用STME ST 2084编码。该传递函数是最常见的HDR传递函数，常被称为“感知量化器”。另见 https://www.itu.int/rec/R-REC-BT.2100 和 https://en.wikipedia.org/wiki/Perceptual_quantizer。
- `QVideoFrameFormat::ColorTransfer_STD_B67`：`7`;颜色值使用ARIB STD B67编码。该传递函数也常被称为“混合对数伽马”。另见 https://www.itu.int/rec/R-REC-BT.2100 和 https://en.wikipedia.org/wiki/Hybrid_log-伽马。

## 6. 深入实践与常见坑

### 生命周期和资源边界

设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

### 状态和错误边界

区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

### 线程边界

媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

### 最容易出现的错误

不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVideoFrameFormat` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
