# QAudioRoom

> Qt 6.11.1 · Qt Spatial Audio

## 1. 先建立直觉

**一句话定位：** `QAudioRoom` 是 Qt Multimedia 的“音频Room”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** 这是 Qt Spatial Audio 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QAudioRoom` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioRoom>`
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

- `enum Material { Transparent, AcousticCeilingTiles, BrickBare, BrickPainted, ConcreteBlockCoarse, …, UniformMaterial }`
- `enum Wall { LeftWall, RightWall, Floor, Ceiling, FrontWall, BackWall }`

### 属性

- `dimensions : QVector3D`
- `position : QVector3D`
- `reflectionGain : float`
- `reverbBrightness : float`
- `reverbGain : float`
- `reverbTime : float`
- `rotation : QQuaternion`

### 公有函数

- `QAudioRoom(QAudioEngine *engine)`
- `virtual ~QAudioRoom() override`
- `QVector3D dimensions() const`
- `QVector3D position() const`
- `float reflectionGain() const`
- `float reverbBrightness() const`
- `float reverbGain() const`
- `float reverbTime() const`
- `QQuaternion rotation() const`
- `void setDimensions(QVector3D dim)`
- `void setPosition(QVector3D pos)`
- `void setReflectionGain(float factor)`
- `void setReverbBrightness(float factor)`
- `void setReverbGain(float factor)`
- `void setReverbTime(float factor)`
- `void setRotation(const QQuaternion &q)`
- `void setWallMaterial(QAudioRoom::Wall wall, QAudioRoom::Material material)`
- `QAudioRoom::Material wallMaterial(QAudioRoom::Wall wall) const`

### 信号

- `void dimensionsChanged()`
- `void positionChanged()`
- `void reflectionGainChanged()`
- `void reverbBrightnessChanged()`
- `void reverbGainChanged()`
- `void reverbTimeChanged()`
- `void rotationChanged()`
- `void wallsChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAudioRoom::Material`

**作用与语义：**

定义了可以应用于房间不同墙面的不同材料。
- `QAudioRoom::Transparent`：`0`;房间一侧是开放的，不会产生反射或混响。
- `QAudioRoom::AcousticCeilingTiles`：`1`;抑制大部分反射和混响的声学磁砖。
- `QAudioRoom::BrickBare`：`2`;裸露的砖墙。
- `QAudioRoom::BrickPainted`：`3`;彩绘砖墙。
- `QAudioRoom::ConcreteBlockCoarse`：`4`;生混凝土墙
- `QAudioRoom::ConcreteBlockPainted`：`5`;彩绘混凝土墙
- `QAudioRoom::CurtainHeavy`：`6`;厚重的幕布。主要反射低频
- `QAudioRoom::FiberGlassInsulation`：43：`7`;玻璃纤维绝缘材料。仅反射极低频率
- `QAudioRoom::GlassThin`：`8`;薄玻璃墙
- `QAudioRoom::GlassThick`：`9`;厚玻璃墙
- `QAudioRoom::Grass`：`10`;草地
- `QAudioRoom::LinoleumOnConcrete`：`11`;油毡地板
- `QAudioRoom::Marble`：`12`;大理石地板
- `QAudioRoom::Metal`：`13`;金属
- `QAudioRoom::ParquetOnConcrete`：`14`;混凝土木地板拼花
- `QAudioRoom::PlasterRough`：`15`;粗糙石膏
- `QAudioRoom::PlasterSmooth`：`16`;光滑石膏
- `QAudioRoom::PlywoodPanel`：`17`;胶合板板
- `QAudioRoom::PolishedConcreteOrTile`：`18`;抛光混凝土或瓷砖
- `QAudioRoom::Sheetrock`：`19`;摇滚
- `QAudioRoom::WaterOrIceSurface`：`20`;水或冰
- `QAudioRoom::WoodCeiling`：`21`;木质天花板
- `QAudioRoom::WoodPanel`：`22`;木板
- `QAudioRoom::UniformMaterial`：`23`;人工材料在所有频率上产生均匀反射

### `enum QAudioRoom::Wall`

**作用与语义：**

一个定义房间六面墙的枚举。
- `QAudioRoom::LeftWall`：`0`;左墙（负面x）
- `QAudioRoom::RightWall`：`1`;右壁（正x）
- `QAudioRoom::Floor`：`2`;底墙（负y）
- `QAudioRoom::Ceiling`：`3`;顶墙（正y）
- `QAudioRoom::FrontWall`：`4`;前墙（负z）
- `QAudioRoom::BackWall`：`5`;后墙（正z挡）

### `dimensions : QVector3D`

**作用与语义：**

定义了房间在三维空间中的尺寸。单位默认以厘米为单位。

**如何使用：** 调用 `dimensions()` 读取当前值；它不会修改应用状态。

### `position : QVector3D`

**作用与语义：**

定义了房间中心在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `reflectionGain : float`

**作用与语义：**

这是该房间内产生的反射的增益因子。0到1的值会抑制反射，而大于1的值则对反射产生增益，使其声音变大。
默认值为1，因子为0则禁用反射。负值映射为0。

**如何使用：** 调用 `reflectionGain()` 读取当前值；它不会修改应用状态。

### `reverbBrightness : float`

**作用与语义：**

一个亮度因子要应用于生成的混响。正值会在高频时增加混响，低频时会减弱，负值则相反。
默认值是0。

**如何使用：** 调用 `reverbBrightness()` 读取当前值；它不会修改应用状态。

### `reverbGain : float`

**作用与语义：**

混响在该房间内产生增益因子。0到1的值会抑制混响，而大于1的值则会给混响施加增益，使其更响。
默认值为1,0倍时会禁用混响。负值映射为0。

**如何使用：** 调用 `reverbGain()` 读取当前值；它不会修改应用状态。

### `reverbTime : float`

**作用与语义：**

该房间生成的所有混响时序都适用一个“是”因子。值越大，混响时序越长，房间听起来更大。
默认值为1。负值映射为0。

**如何使用：** 调用 `reverbTime()` 读取当前值；它不会修改应用状态。

### `rotation : QQuaternion`

**作用与语义：**

定义了房间在三维空间中的朝向。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `[explicit] QAudioRoom::QAudioRoom(QAudioEngine *engine)`

**作用与语义：**

为`engine`构建了一个QAudioRoom。
注意：必须带着有效的电话`QAudioEngine`。

### `[override virtual noexcept] QAudioRoom::~QAudioRoom()`

**作用与语义：**

毁了整个房间。

### `void QAudioRoom::setWallMaterial(QAudioRoom::Wall wall, QAudioRoom::Material material)`

**作用与语义：**

将`wall`设为`material`。
不同的墙体材料有不同的反射和混响特性，会影响房间的声音。

### `QAudioRoom::Material QAudioRoom::wallMaterial(QAudioRoom::Wall wall) const`

**作用与语义：**

归还用于`wall`的材料。

### `[signal] void QAudioRoom::wallsChanged()`

**作用与语义：**

墙体材料发生变化时会发出信号。

### `QVector3D dimensions() const`

**作用与语义：**

定义了房间在三维空间中的尺寸。单位默认以厘米为单位。

**如何使用：** 调用 `dimensions()` 读取当前值；它不会修改应用状态。

### `QVector3D position() const`

**作用与语义：**

定义了房间中心在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `float reflectionGain() const`

**作用与语义：**

这是该房间内产生的反射的增益因子。0到1的值会抑制反射，而大于1的值则对反射产生增益，使其声音变大。
默认值为1，因子为0则禁用反射。负值映射为0。

**如何使用：** 调用 `reflectionGain()` 读取当前值；它不会修改应用状态。

### `float reverbBrightness() const`

**作用与语义：**

一个亮度因子要应用于生成的混响。正值会在高频时增加混响，低频时会减弱，负值则相反。
默认值是0。

**如何使用：** 调用 `reverbBrightness()` 读取当前值；它不会修改应用状态。

### `float reverbGain() const`

**作用与语义：**

混响在该房间内产生增益因子。0到1的值会抑制混响，而大于1的值则会给混响施加增益，使其更响。
默认值为1,0倍时会禁用混响。负值映射为0。

**如何使用：** 调用 `reverbGain()` 读取当前值；它不会修改应用状态。

### `float reverbTime() const`

**作用与语义：**

该房间生成的所有混响时序都适用一个“是”因子。值越大，混响时序越长，房间听起来更大。
默认值为1。负值映射为0。

**如何使用：** 调用 `reverbTime()` 读取当前值；它不会修改应用状态。

### `QQuaternion rotation() const`

**作用与语义：**

定义了房间在三维空间中的朝向。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `void setDimensions(QVector3D dim)`

**作用与语义：**

定义了房间在三维空间中的尺寸。单位默认以厘米为单位。

**如何使用：** 调用 `setDimensions(...)` 修改 `dimensions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPosition(QVector3D pos)`

**作用与语义：**

定义了房间中心在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 调用 `setPosition(...)` 修改 `position`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReflectionGain(float factor)`

**作用与语义：**

这是该房间内产生的反射的增益因子。0到1的值会抑制反射，而大于1的值则对反射产生增益，使其声音变大。
默认值为1，因子为0则禁用反射。负值映射为0。

**如何使用：** 调用 `setReflectionGain(...)` 修改 `reflectionGain`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReverbBrightness(float factor)`

**作用与语义：**

一个亮度因子要应用于生成的混响。正值会在高频时增加混响，低频时会减弱，负值则相反。
默认值是0。

**如何使用：** 调用 `setReverbBrightness(...)` 修改 `reverbBrightness`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReverbGain(float factor)`

**作用与语义：**

混响在该房间内产生增益因子。0到1的值会抑制混响，而大于1的值则会给混响施加增益，使其更响。
默认值为1,0倍时会禁用混响。负值映射为0。

**如何使用：** 调用 `setReverbGain(...)` 修改 `reverbGain`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReverbTime(float factor)`

**作用与语义：**

该房间生成的所有混响时序都适用一个“是”因子。值越大，混响时序越长，房间听起来更大。
默认值为1。负值映射为0。

**如何使用：** 调用 `setReverbTime(...)` 修改 `reverbTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRotation(const QQuaternion &q)`

**作用与语义：**

定义了房间在三维空间中的朝向。

**如何使用：** 调用 `setRotation(...)` 修改 `rotation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void dimensionsChanged()`

**作用与语义：**

定义了房间在三维空间中的尺寸。单位默认以厘米为单位。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `dimensions` 的变化，不要把它当作普通函数主动调用。

### `void positionChanged()`

**作用与语义：**

定义了房间中心在三维空间中的位置。单位默认以厘米为单位。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `position` 的变化，不要把它当作普通函数主动调用。

### `void reflectionGainChanged()`

**作用与语义：**

这是该房间内产生的反射的增益因子。0到1的值会抑制反射，而大于1的值则对反射产生增益，使其声音变大。
默认值为1，因子为0则禁用反射。负值映射为0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reflectionGain` 的变化，不要把它当作普通函数主动调用。

### `void reverbBrightnessChanged()`

**作用与语义：**

一个亮度因子要应用于生成的混响。正值会在高频时增加混响，低频时会减弱，负值则相反。
默认值是0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reverbBrightness` 的变化，不要把它当作普通函数主动调用。

### `void reverbGainChanged()`

**作用与语义：**

混响在该房间内产生增益因子。0到1的值会抑制混响，而大于1的值则会给混响施加增益，使其更响。
默认值为1,0倍时会禁用混响。负值映射为0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reverbGain` 的变化，不要把它当作普通函数主动调用。

### `void reverbTimeChanged()`

**作用与语义：**

该房间生成的所有混响时序都适用一个“是”因子。值越大，混响时序越长，房间听起来更大。
默认值为1。负值映射为0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reverbTime` 的变化，不要把它当作普通函数主动调用。

### `void rotationChanged()`

**作用与语义：**

定义了房间在三维空间中的朝向。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `rotation` 的变化，不要把它当作普通函数主动调用。

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

`QAudioRoom` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
