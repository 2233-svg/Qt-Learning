# QGradient

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QGradient` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QGradient>`
- 继承自：未在类页中列出
- 直接派生类：QConicalGradient、QLinearGradient,、QRadialGradient

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum CoordinateMode { LogicalMode, ObjectMode, StretchToDeviceMode, ObjectBoundingMode }`
- `enum Preset { WarmFlame, NightFade, SpringWarmth, JuicyPeach, YoungPassion, …, PerfectBlue }`
- `enum Spread { PadSpread, RepeatSpread, ReflectSpread }`
- `enum Type { LinearGradient, RadialGradient, ConicalGradient, NoGradient }`

### 公有函数

- `QGradient(QGradient::Preset preset)`
- `QGradient::CoordinateMode coordinateMode() const`
- `void setColorAt(qreal position, const QColor &color)`
- `void setCoordinateMode(QGradient::CoordinateMode mode)`
- `void setSpread(QGradient::Spread method)`
- `void setStops(const QGradientStops &stopPoints)`
- `QGradient::Spread spread() const`
- `QGradientStops stops() const`
- `QGradient::Type type() const`
- `bool operator!=(const QGradient &gradient) const`
- `bool operator==(const QGradient &gradient) const`

### 相关非成员函数

- `QGradientStop`
- `QGradientStops`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGradient::CoordinateMode`

**作用与语义：**

该枚举规定了梯度坐标如何映射到使用梯度的绘画装置。
- `QGradient::LogicalMode`：`0`;这是默认模式。梯度坐标与对象坐标一样指定在逻辑空间中。
- `QGradient::ObjectMode`：`3`;在此模式下，梯度坐标相对于被绘制物体的边界矩形，左上角为（0,0），右下角为（1,1）。该值在Qt 5.12中加入。
- `QGradient::StretchToDeviceMode`：`1`;在此模式下，梯度坐标相对于绘画装置的边界矩形，左上角为（0,0），右下角为（1,1）。
- `QGradient::ObjectBoundingMode`：`2`;该模式与ObjectMode相同，不同之处在于{`QBrush::transform()`} {brush transform}（如有）相对于逻辑空间而非对象空间应用。该枚举值已废弃，不应在新代码中使用。

### `enum QGradient::Preset`

**作用与语义：**

该枚举指定了一组预定义的`QGradient`预设预设，基于 https://webgradients.com/ 梯度。
- `QGradient::WarmFlame`：`1`
- `QGradient::NightFade`：`2`
- `QGradient::SpringWarmth`：`3`
- `QGradient::JuicyPeach`：`4`
- `QGradient::YoungPassion`：`5`
- `QGradient::LadyLips`：`6`
- `QGradient::SunnyMorning`：`7`
- `QGradient::RainyAshville`：`8`
- `QGradient::FrozenDreams`：`9`
- `QGradient::WinterNeva`：`10`
- `QGradient::DustyGrass`：`11`
- `QGradient::TemptingAzure`：`12`
- `QGradient::HeavyRain`：`13`
- `QGradient::AmyCrisp`：`14`
- `QGradient::MeanFruit`：`15`
- `QGradient::DeepBlue`：`16`
- `QGradient::RipeMalinka`：`17`
- `QGradient::CloudyKnoxville`：`18`
- `QGradient::MalibuBeach`：`19`
- `QGradient::NewLife`：`20`
- `QGradient::TrueSunset`：`21`
- `QGradient::MorpheusDen`：`22`
- `QGradient::RareWind`：`23`
- `QGradient::NearMoon`：`24`
- `QGradient::WildApple`：`25`
- `QGradient::SaintPetersburg`：`26`
- `QGradient::PlumPlate`：`28`
- `QGradient::EverlastingSky`：`29`
- `QGradient::HappyFisher`：`30`
- `QGradient::Blessing`：`31`
- `QGradient::SharpeyeEagle`：`32`
- `QGradient::LadogaBottom`：`33`
- `QGradient::LemonGate`：`34`
- `QGradient::ItmeoBranding`：`35`
- `QGradient::ZeusMiracle`：`36`
- `QGradient::OldHat`：`37`
- `QGradient::StarWine`：`38`
- `QGradient::HappyAcid`：`41`
- `QGradient::AwesomePine`：`42`
- `QGradient::NewYork`：`43`
- `QGradient::ShyRainbow`：`44`
- `QGradient::MixedHopes`：`46`
- `QGradient::FlyHigh`：`47`
- `QGradient::StrongBliss`：`48`
- `QGradient::FreshMilk`：`49`
- `QGradient::SnowAgain`：`50`
- `QGradient::FebruaryInk`：`51`
- `QGradient::KindSteel`：`52`
- `QGradient::SoftGrass`：`53`
- `QGradient::GrownEarly`：`54`
- `QGradient::SharpBlues`：`55`
- `QGradient::ShadyWater`：`56`
- `QGradient::DirtyBeauty`：`57`
- `QGradient::GreatWhale`：`58`
- `QGradient::TeenNotebook`：`59`
- `QGradient::PoliteRumors`：`60`
- `QGradient::SweetPeriod`：`61`
- `QGradient::WideMatrix`：`62`
- `QGradient::SoftCherish`：`63`
- `QGradient::RedSalvation`：`64`
- `QGradient::BurningSpring`：`65`
- `QGradient::NightParty`：`66`
- `QGradient::SkyGlider`：`67`
- `QGradient::HeavenPeach`：`68`
- `QGradient::PurpleDivision`：`69`
- `QGradient::AquaSplash`：`70`
- `QGradient::SpikyNaga`：`72`
- `QGradient::LoveKiss`：`73`
- `QGradient::CleanMirror`：`75`
- `QGradient::PremiumDark`：`76`
- `QGradient::ColdEvening`：`77`
- `QGradient::CochitiLake`：`78`
- `QGradient::SummerGames`：`79`
- `QGradient::PassionateBed`：`80`
- `QGradient::MountainRock`：`81`
- `QGradient::DesertHump`：`82`
- `QGradient::JungleDay`：`83`
- `QGradient::PhoenixStart`：`84`
- `QGradient::OctoberSilence`：`85`
- `QGradient::FarawayRiver`：`86`
- `QGradient::AlchemistLab`：`87`
- `QGradient::OverSun`：`88`
- `QGradient::PremiumWhite`：`89`
- `QGradient::MarsParty`：`90`
- `QGradient::EternalConstance`：`91`
- `QGradient::JapanBlush`：`92`
- `QGradient::SmilingRain`：`93`
- `QGradient::CloudyApple`：`94`
- `QGradient::BigMango`：`95`
- `QGradient::HealthyWater`：`96`
- `QGradient::AmourAmour`：`97`
- `QGradient::RiskyConcrete`：`98`
- `QGradient::StrongStick`：`99`
- `QGradient::ViciousStance`：`100`
- `QGradient::PaloAlto`：`101`
- `QGradient::HappyMemories`：`102`
- `QGradient::MidnightBloom`：`103`
- `QGradient::Crystalline`：`104`
- `QGradient::PartyBliss`：`106`
- `QGradient::ConfidentCloud`：`107`
- `QGradient::LeCocktail`：`108`
- `QGradient::RiverCity`：`109`
- `QGradient::FrozenBerry`：`110`
- `QGradient::ChildCare`：`112`
- `QGradient::FlyingLemon`：`113`
- `QGradient::NewRetrowave`：`114`
- `QGradient::HiddenJaguar`：`115`
- `QGradient::AboveTheSky`：`116`
- `QGradient::Nega`：`117`
- `QGradient::DenseWater`：`118`
- `QGradient::Seashore`：`120`
- `QGradient::MarbleWall`：`121`
- `QGradient::CheerfulCaramel`：`122`
- `QGradient::NightSky`：`123`
- `QGradient::MagicLake`：`124`
- `QGradient::YoungGrass`：`125`
- `QGradient::ColorfulPeach`：`126`
- `QGradient::GentleCare`：`127`
- `QGradient::PlumBath`：`128`
- `QGradient::HappyUnicorn`：`129`
- `QGradient::AfricanField`：`131`
- `QGradient::SolidStone`：`132`
- `QGradient::OrangeJuice`：`133`
- `QGradient::GlassWater`：`134`
- `QGradient::NorthMiracle`：`136`
- `QGradient::FruitBlend`：`137`
- `QGradient::MillenniumPine`：`138`
- `QGradient::HighFlight`：`139`
- `QGradient::MoleHall`：`140`
- `QGradient::SpaceShift`：`142`
- `QGradient::ForestInei`：`143`
- `QGradient::RoyalGarden`：`144`
- `QGradient::RichMetal`：`145`
- `QGradient::JuicyCake`：`146`
- `QGradient::SmartIndigo`：`147`
- `QGradient::SandStrike`：`148`
- `QGradient::NorseBeauty`：`149`
- `QGradient::AquaGuidance`：`150`
- `QGradient::SunVeggie`：`151`
- `QGradient::SeaLord`：`152`
- `QGradient::BlackSea`：`153`
- `QGradient::GrassShampoo`：`154`
- `QGradient::LandingAircraft`：`155`
- `QGradient::WitchDance`：`156`
- `QGradient::SleeplessNight`：`157`
- `QGradient::AngelCare`：`158`
- `QGradient::CrystalRiver`：`159`
- `QGradient::SoftLipstick`：`160`
- `QGradient::SaltMountain`：`161`
- `QGradient::PerfectWhite`：`162`
- `QGradient::FreshOasis`：`163`
- `QGradient::StrictNovember`：`164`
- `QGradient::MorningSalad`：`165`
- `QGradient::DeepRelief`：`166`
- `QGradient::SeaStrike`：`167`
- `QGradient::NightCall`：`168`
- `QGradient::SupremeSky`：`169`
- `QGradient::LightBlue`：`170`
- `QGradient::MindCrawl`：`171`
- `QGradient::LilyMeadow`：`172`
- `QGradient::SugarLollipop`：`173`
- `QGradient::SweetDessert`：`174`
- `QGradient::MagicRay`：`175`
- `QGradient::TeenParty`：`176`
- `QGradient::FrozenHeat`：`177`
- `QGradient::GagarinView`：`178`
- `QGradient::FabledSunset`：`179`
- `QGradient::PerfectBlue`：`180`

### `enum QGradient::Spread`

**作用与语义：**

指定梯度区外的区域应如何填充。
- `QGradient::PadSpread`：`0`;该区域填充最近的止音色。这是默认颜色。
- `QGradient::RepeatSpread`：`2`;梯度在梯度区域外重复。
- `QGradient::ReflectSpread`：`1`;梯度反射在梯度区之外。

### `enum QGradient::Type`

**作用与语义：**

指定梯度类型。
- `QGradient::LinearGradient`：`0`;在起点和终点之间插值颜色（`QLinearGradient`）。
- `QGradient::RadialGradient`：`1`;在焦点和环绕其周围的圆（`QRadialGradient`）的端点之间插值颜色。
- `QGradient::ConicalGradient`：`2`;围绕中心点（`QConicalGradient`）插值颜色。
- `QGradient::NoGradient`：`3`;不使用梯度。

### `QGradient::QGradient(QGradient::Preset preset)`

**作用与语义：**

基于预定义的`preset`构造梯度。
所得梯度的坐标模态`QGradient::ObjectMode`，允许将预设应用于任意对象大小。

### `QGradient::CoordinateMode QGradient::coordinateMode() const`

**作用与语义：**

返回该梯度的坐标模态。默认模式为`LogicalMode`。

### `void QGradient::setColorAt(qreal position, const QColor &color)`

**作用与语义：**

在给定`position`和给定`color`处建立一个停止点。给定`position`必须在0到1之间。

### `void QGradient::setCoordinateMode(QGradient::CoordinateMode mode)`

**作用与语义：**

将该梯度的坐标模式设置为`mode`。默认模式为`LogicalMode`。

### `void QGradient::setSpread(QGradient::Spread method)`

**作用与语义：**

指定该梯度应使用何种扩散`method`。
注意，该函数仅对线性梯度和径向梯度有效。

### `void QGradient::setStops(const QGradientStops &stopPoints)`

**作用与语义：**

用给定的`stopPoints`替换当前的停止点集合。点的位置必须在0到1之间，并且必须先从最低点排序。

### `QGradient::Spread QGradient::spread() const`

**作用与语义：**

返回该梯度所使用的扩散方法。默认为`PadSpread`。

### `QGradientStops QGradient::stops() const`

**作用与语义：**

返回该梯度的停止点。
如果没有指定停止点，则使用从0处的黑色到1处的白色渐变。

### `QGradient::Type QGradient::type() const`

**作用与语义：**

返回梯度类型。

### `bool QGradient::operator!=(const QGradient &gradient) const`

**作用与语义：**

如果梯度与指定的其他`gradient`相同，返回`true`;否则返回`false`。

### `bool QGradient::operator==(const QGradient &gradient) const`

**作用与语义：**

如果梯度与指定的其他`gradient`相同，返回`true`;否则返回`false`。

### `QGradientStop`

**作用与语义：**

类型def用于性病：:p air<`qreal`，`QColor`>。

### `QGradientStops`

**作用与语义：**

渐变停止点列表类型，等价于 `QList<QGradientStop>`；每项由 0 到 1 的位置和该位置的颜色组成。用 `setStops()` 一次设置多个色标时通常按位置升序排列，超出有效范围的位置不应使用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGradient` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
