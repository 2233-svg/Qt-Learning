# QSpatialSound

> Qt 6.11.1 · Qt Spatial Audio

## 1. 先建立直觉

**一句话定位：** `QSpatialSound` 是 Qt Multimedia 的“Spatial声音”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** 这是 Qt Spatial Audio 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QSpatialSound` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QSpatialSound>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS SpatialAudio)
target_link_libraries(mytarget PRIVATE Qt6::SpatialAudio)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `enum class DistanceModel { Logarithmic, Linear, ManualAttenuation }`
- `enum Loops { Infinite, Once }`

### 属性

- `autoPlay : bool`
- `directivity : float`
- `directivityOrder : float`
- `distanceCutoff : float`
- `distanceModel : DistanceModel`
- `loops : int`
- `manualAttenuation : float`
- `nearFieldGain : float`
- `occlusionIntensity : float`
- `position : QVector3D`
- `rotation : QQuaternion`
- `size : float`
- `source : QUrl`
- `volume : float`

### 公有函数

- `QSpatialSound(QAudioEngine *engine)`
- `virtual ~QSpatialSound() override`
- `bool autoPlay() const`
- `float directivity() const`
- `float directivityOrder() const`
- `float distanceCutoff() const`
- `QSpatialSound::DistanceModel distanceModel() const`
- `QAudioEngine * engine() const`
- `int loops() const`
- `float manualAttenuation() const`
- `float nearFieldGain() const`
- `float occlusionIntensity() const`
- `QVector3D position() const`
- `QQuaternion rotation() const`
- `void setAutoPlay(bool autoPlay)`
- `void setDirectivity(float alpha)`
- `void setDirectivityOrder(float alpha)`
- `void setDistanceCutoff(float cutoff)`
- `void setDistanceModel(QSpatialSound::DistanceModel model)`
- `void setLoops(int loops)`
- `void setManualAttenuation(float attenuation)`
- `void setNearFieldGain(float gain)`
- `void setOcclusionIntensity(float occlusion)`
- `void setPosition(QVector3D pos)`
- `void setRotation(const QQuaternion &q)`
- `void setSize(float size)`
- `void setSource(const QUrl &url)`
- `void setVolume(float volume)`
- `float size() const`
- `QUrl source() const`
- `float volume() const`

### 公有槽函数

- `void pause()`
- `void play()`
- `void stop()`

### 信号

- `void autoPlayChanged()`
- `void directivityChanged()`
- `void directivityOrderChanged()`
- `void distanceCutoffChanged()`
- `void distanceModelChanged()`
- `void loopsChanged()`
- `void manualAttenuationChanged()`
- `void nearFieldGainChanged()`
- `void occlusionIntensityChanged()`
- `void positionChanged()`
- `void rotationChanged()`
- `void sizeChanged()`
- `void sourceChanged()`
- `void volumeChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QSpatialSound::DistanceModel`

**作用与语义：**

定义了声音音量随听者距离的增长。
- `QSpatialSound::DistanceModel::Logarithmic`：`0`;体积随距离对数递减。
- `QSpatialSound::DistanceModel::Linear`：`1`;体积随距离线性递减。
- `QSpatialSound::DistanceModel::ManualAttenuation`：`2`;衰减是利用`manualAttenuation`属性手动定义的。

### `enum QSpatialSound::Loops`

**作用与语义：**

你可以用以下数值控制声音回放循环：
- `QSpatialSound::Infinite`：`-1`;无限回放
- `QSpatialSound::Once`：`1`;回放一次

### `autoPlay : bool`

**作用与语义：**

决定当指定音源时声音是否应该自动开始播放。
默认值是`true`。

**如何使用：** 调用 `autoPlay()` 读取当前值；它不会修改应用状态。

### `directivity : float`

**作用与语义：**

定义了声源的指向性。0表示声音在所有方向均匀发出，而1表示声音主要向正向发出。
有效值在0到1之间，默认值为0。

**如何使用：** 调用 `directivity()` 读取当前值；它不会修改应用状态。

### `directivityOrder : float`

**作用与语义：**

定义声源指向性的阶数。阶数越高，声音锥的定位越为清晰。
该房产的最低价值和违约值为1。

**如何使用：** 调用 `directivityOrder()` 读取当前值；它不会修改应用状态。

### `distanceCutoff : float`

**作用与语义：**

定义了声音来源超过该距离会被截止的距离。如果听者距离声音物体比截止距离更远，声音就不再可听见了。

**如何使用：** 调用 `distanceCutoff()` 读取当前值；它不会修改应用状态。

### `distanceModel : DistanceModel`

**作用与语义：**

定义该声源的距离模型。音量从`size`缩放到`distanceCutoff`。音量在距离小于尺寸时保持恒定，距离大于截止距离时为零。

**如何使用：** 调用 `distanceModel()` 读取当前值；它不会修改应用状态。

### `loops : int`

**作用与语义：**

决定该声音播放多少次后玩家停止。设置为`QSpatialSound::Infinite`，将当前声音循环播放。
默认值是`1`。

**如何使用：** 调用 `loops()` 读取当前值；它不会修改应用状态。

### `manualAttenuation : float`

**作用与语义：**

如果`distanceModel`设置为`QSpatialSound::DistanceModel::ManualAttenuation`，则定义一个手动衰减因子。

**如何使用：** 调用 `manualAttenuation()` 读取当前值；它不会修改应用状态。

### `nearFieldGain : float`

**作用与语义：**

定义声源的近场增益。有效值在0到1之间。近场增益为1时，声音信号音量在距离听者非常近时大约增加20 dB。

**如何使用：** 调用 `nearFieldGain()` 读取当前值；它不会修改应用状态。

### `occlusionIntensity : float`

**作用与语义：**

定义物体被遮挡的程度。0表示该物体根本没有被遮挡，1表示声音源被另一个物体完全遮挡。
完全遮挡的物体仍然可以听到声音，但尤其是高频会被抑制。此外，物体仍会参与在房间内产生混响和反射。
大于1的数值可以进一步抑制来自声源的直接声音。
默认值是0。

**如何使用：** 调用 `occlusionIntensity()` 读取当前值；它不会修改应用状态。

### `position : QVector3D`

**作用与语义：**

定义声源在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `rotation : QQuaternion`

**作用与语义：**

定义声源在三维空间中的方向。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `size : float`

**作用与语义：**

定义声源的大小。如果听者距离声音物体比大小更近，音量将保持不变。尺寸也用于遮挡计算，即大声源可能被墙部分遮挡。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

要播放的声音的源文件。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `volume : float`

**作用与语义：**

定义声音的音量。
0到1之间的数值会削弱声音，而大于1的数值则提供额外的增益提升。

**如何使用：** 调用 `volume()` 读取当前值；它不会修改应用状态。

### `[explicit] QSpatialSound::QSpatialSound(QAudioEngine *engine)`

**作用与语义：**

为`engine`创建一个空间声源。物体可以放置在三维空间中，离听者越近，声音越大。
注意：必须有有效电话联系`QAudioEngine`。

### `[override virtual noexcept] QSpatialSound::~QSpatialSound()`

**作用与语义：**

破坏了声音源。

### `QAudioEngine *QSpatialSound::engine() const`

**作用与语义：**

返回与该监听器关联的引擎。

### `[slot] void QSpatialSound::pause()`

**作用与语义：**

暂停声音播放。调用`play()`将继续播放。

### `[slot] void QSpatialSound::play()`

**作用与语义：**

它开始播放声音。如果声音已经在播放，它就没用。

### `[slot] void QSpatialSound::stop()`

**作用与语义：**

停止声音播放，并将当前位置和当前循环计数重置为0。调用`play()`会从声音文件开头开始播放。

### `bool autoPlay() const`

**作用与语义：**

决定当指定音源时声音是否应该自动开始播放。
默认值是`true`。

**如何使用：** 调用 `autoPlay()` 读取当前值；它不会修改应用状态。

### `float directivity() const`

**作用与语义：**

定义了声源的指向性。0表示声音在所有方向均匀发出，而1表示声音主要向正向发出。
有效值在0到1之间，默认值为0。

**如何使用：** 调用 `directivity()` 读取当前值；它不会修改应用状态。

### `float directivityOrder() const`

**作用与语义：**

定义声源指向性的阶数。阶数越高，声音锥的定位越为清晰。
该房产的最低价值和违约值为1。

**如何使用：** 调用 `directivityOrder()` 读取当前值；它不会修改应用状态。

### `float distanceCutoff() const`

**作用与语义：**

定义了声音来源超过该距离会被截止的距离。如果听者距离声音物体比截止距离更远，声音就不再可听见了。

**如何使用：** 调用 `distanceCutoff()` 读取当前值；它不会修改应用状态。

### `QSpatialSound::DistanceModel distanceModel() const`

**作用与语义：**

定义该声源的距离模型。音量从`size`缩放到`distanceCutoff`。音量在距离小于尺寸时保持恒定，距离大于截止距离时为零。

**如何使用：** 调用 `distanceModel()` 读取当前值；它不会修改应用状态。

### `int loops() const`

**作用与语义：**

决定该声音播放多少次后玩家停止。设置为`QSpatialSound::Infinite`，将当前声音循环播放。
默认值是`1`。

**如何使用：** 调用 `loops()` 读取当前值；它不会修改应用状态。

### `float manualAttenuation() const`

**作用与语义：**

如果`distanceModel`设置为`QSpatialSound::DistanceModel::ManualAttenuation`，则定义一个手动衰减因子。

**如何使用：** 调用 `manualAttenuation()` 读取当前值；它不会修改应用状态。

### `float nearFieldGain() const`

**作用与语义：**

定义声源的近场增益。有效值在0到1之间。近场增益为1时，声音信号音量在距离听者非常近时大约增加20 dB。

**如何使用：** 调用 `nearFieldGain()` 读取当前值；它不会修改应用状态。

### `float occlusionIntensity() const`

**作用与语义：**

定义物体被遮挡的程度。0表示该物体根本没有被遮挡，1表示声音源被另一个物体完全遮挡。
完全遮挡的物体仍然可以听到声音，但尤其是高频会被抑制。此外，物体仍会参与在房间内产生混响和反射。
大于1的数值可以进一步抑制来自声源的直接声音。
默认值是0。

**如何使用：** 调用 `occlusionIntensity()` 读取当前值；它不会修改应用状态。

### `QVector3D position() const`

**作用与语义：**

定义声源在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `QQuaternion rotation() const`

**作用与语义：**

定义声源在三维空间中的方向。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `void setAutoPlay(bool autoPlay)`

**作用与语义：**

决定当指定音源时声音是否应该自动开始播放。
默认值是`true`。

**如何使用：** 调用 `setAutoPlay(...)` 修改 `autoPlay`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDirectivity(float alpha)`

**作用与语义：**

定义了声源的指向性。0表示声音在所有方向均匀发出，而1表示声音主要向正向发出。
有效值在0到1之间，默认值为0。

**如何使用：** 调用 `setDirectivity(...)` 修改 `directivity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDirectivityOrder(float alpha)`

**作用与语义：**

定义声源指向性的阶数。阶数越高，声音锥的定位越为清晰。
该房产的最低价值和违约值为1。

**如何使用：** 调用 `setDirectivityOrder(...)` 修改 `directivityOrder`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDistanceCutoff(float cutoff)`

**作用与语义：**

定义了声音来源超过该距离会被截止的距离。如果听者距离声音物体比截止距离更远，声音就不再可听见了。

**如何使用：** 调用 `setDistanceCutoff(...)` 修改 `distanceCutoff`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDistanceModel(QSpatialSound::DistanceModel model)`

**作用与语义：**

定义该声源的距离模型。音量从`size`缩放到`distanceCutoff`。音量在距离小于尺寸时保持恒定，距离大于截止距离时为零。

**如何使用：** 调用 `setDistanceModel(...)` 修改 `distanceModel`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLoops(int loops)`

**作用与语义：**

决定该声音播放多少次后玩家停止。设置为`QSpatialSound::Infinite`，将当前声音循环播放。
默认值是`1`。

**如何使用：** 调用 `setLoops(...)` 修改 `loops`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setManualAttenuation(float attenuation)`

**作用与语义：**

如果`distanceModel`设置为`QSpatialSound::DistanceModel::ManualAttenuation`，则定义一个手动衰减因子。

**如何使用：** 调用 `setManualAttenuation(...)` 修改 `manualAttenuation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNearFieldGain(float gain)`

**作用与语义：**

定义声源的近场增益。有效值在0到1之间。近场增益为1时，声音信号音量在距离听者非常近时大约增加20 dB。

**如何使用：** 调用 `setNearFieldGain(...)` 修改 `nearFieldGain`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOcclusionIntensity(float occlusion)`

**作用与语义：**

定义物体被遮挡的程度。0表示该物体根本没有被遮挡，1表示声音源被另一个物体完全遮挡。
完全遮挡的物体仍然可以听到声音，但尤其是高频会被抑制。此外，物体仍会参与在房间内产生混响和反射。
大于1的数值可以进一步抑制来自声源的直接声音。
默认值是0。

**如何使用：** 调用 `setOcclusionIntensity(...)` 修改 `occlusionIntensity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPosition(QVector3D pos)`

**作用与语义：**

定义声源在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 调用 `setPosition(...)` 修改 `position`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRotation(const QQuaternion &q)`

**作用与语义：**

定义声源在三维空间中的方向。

**如何使用：** 调用 `setRotation(...)` 修改 `rotation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSize(float size)`

**作用与语义：**

定义声源的大小。如果听者距离声音物体比大小更近，音量将保持不变。尺寸也用于遮挡计算，即大声源可能被墙部分遮挡。

**如何使用：** 调用 `setSize(...)` 修改 `size`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSource(const QUrl &url)`

**作用与语义：**

要播放的声音的源文件。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVolume(float volume)`

**作用与语义：**

定义声音的音量。
0到1之间的数值会削弱声音，而大于1的数值则提供额外的增益提升。

**如何使用：** 调用 `setVolume(...)` 修改 `volume`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `float size() const`

**作用与语义：**

定义声源的大小。如果听者距离声音物体比大小更近，音量将保持不变。尺寸也用于遮挡计算，即大声源可能被墙部分遮挡。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `QUrl source() const`

**作用与语义：**

要播放的声音的源文件。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `float volume() const`

**作用与语义：**

定义声音的音量。
0到1之间的数值会削弱声音，而大于1的数值则提供额外的增益提升。

**如何使用：** 调用 `volume()` 读取当前值；它不会修改应用状态。

### `void autoPlayChanged()`

**作用与语义：**

决定当指定音源时声音是否应该自动开始播放。
默认值是`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `autoPlay` 的变化，不要把它当作普通函数主动调用。

### `void directivityChanged()`

**作用与语义：**

定义了声源的指向性。0表示声音在所有方向均匀发出，而1表示声音主要向正向发出。
有效值在0到1之间，默认值为0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `directivity` 的变化，不要把它当作普通函数主动调用。

### `void directivityOrderChanged()`

**作用与语义：**

定义声源指向性的阶数。阶数越高，声音锥的定位越为清晰。
该房产的最低价值和违约值为1。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `directivityOrder` 的变化，不要把它当作普通函数主动调用。

### `void distanceCutoffChanged()`

**作用与语义：**

定义了声音来源超过该距离会被截止的距离。如果听者距离声音物体比截止距离更远，声音就不再可听见了。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `distanceCutoff` 的变化，不要把它当作普通函数主动调用。

### `void distanceModelChanged()`

**作用与语义：**

定义该声源的距离模型。音量从`size`缩放到`distanceCutoff`。音量在距离小于尺寸时保持恒定，距离大于截止距离时为零。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `distanceModel` 的变化，不要把它当作普通函数主动调用。

### `void loopsChanged()`

**作用与语义：**

决定该声音播放多少次后玩家停止。设置为`QSpatialSound::Infinite`，将当前声音循环播放。
默认值是`1`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `loops` 的变化，不要把它当作普通函数主动调用。

### `void manualAttenuationChanged()`

**作用与语义：**

如果`distanceModel`设置为`QSpatialSound::DistanceModel::ManualAttenuation`，则定义一个手动衰减因子。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `manualAttenuation` 的变化，不要把它当作普通函数主动调用。

### `void nearFieldGainChanged()`

**作用与语义：**

定义声源的近场增益。有效值在0到1之间。近场增益为1时，声音信号音量在距离听者非常近时大约增加20 dB。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `nearFieldGain` 的变化，不要把它当作普通函数主动调用。

### `void occlusionIntensityChanged()`

**作用与语义：**

定义物体被遮挡的程度。0表示该物体根本没有被遮挡，1表示声音源被另一个物体完全遮挡。
完全遮挡的物体仍然可以听到声音，但尤其是高频会被抑制。此外，物体仍会参与在房间内产生混响和反射。
大于1的数值可以进一步抑制来自声源的直接声音。
默认值是0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `occlusionIntensity` 的变化，不要把它当作普通函数主动调用。

### `void positionChanged()`

**作用与语义：**

定义声源在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `position` 的变化，不要把它当作普通函数主动调用。

### `void rotationChanged()`

**作用与语义：**

定义声源在三维空间中的方向。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `rotation` 的变化，不要把它当作普通函数主动调用。

### `void sizeChanged()`

**作用与语义：**

定义声源的大小。如果听者距离声音物体比大小更近，音量将保持不变。尺寸也用于遮挡计算，即大声源可能被墙部分遮挡。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `size` 的变化，不要把它当作普通函数主动调用。

### `void sourceChanged()`

**作用与语义：**

要播放的声音的源文件。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `source` 的变化，不要把它当作普通函数主动调用。

### `void volumeChanged()`

**作用与语义：**

定义声音的音量。
0到1之间的数值会削弱声音，而大于1的数值则提供额外的增益提升。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `volume` 的变化，不要把它当作普通函数主动调用。

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

`QSpatialSound` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
