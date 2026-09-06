# QColor

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 颜色值和颜色空间转换类型。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QColor`：颜色值和颜色空间转换类型。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QColor>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum NameFormat { HexRgb, HexArgb }`
- `enum Spec { Rgb, Hsv, Cmyk, Hsl, ExtendedRgb, Invalid }`

### 公有函数

- `QColor()`
- `QColor(QRgb color)`
- `QColor(QRgba64 rgba64)`
- `QColor(const QString &name)`
- `QColor(int r, int g, int b, int a = 255)`
- `QColor(QLatin1StringView name)`
- `QColor(Qt::GlobalColor color)`
- `QColor(const char *name)`
- `int alpha() const`
- `float alphaF() const`
- `int black() const`
- `float blackF() const`
- `int blue() const`
- `float blueF() const`
- `QColor convertTo(QColor::Spec colorSpec) const`
- `int cyan() const`
- `float cyanF() const`
- `QColor darker(int factor = 200) const`
- `void getCmyk(int *c, int *m, int *y, int *k, int *a = nullptr) const`
- `void getCmykF(float *c, float *m, float *y, float *k, float *a = nullptr) const`
- `void getHsl(int *h, int *s, int *l, int *a = nullptr) const`
- `void getHslF(float *h, float *s, float *l, float *a = nullptr) const`
- `void getHsv(int *h, int *s, int *v, int *a = nullptr) const`
- `void getHsvF(float *h, float *s, float *v, float *a = nullptr) const`
- `void getRgb(int *r, int *g, int *b, int *a = nullptr) const`
- `void getRgbF(float *r, float *g, float *b, float *a = nullptr) const`
- `int green() const`
- `float greenF() const`
- `int hslHue() const`
- `float hslHueF() const`
- `int hslSaturation() const`
- `float hslSaturationF() const`
- `int hsvHue() const`
- `float hsvHueF() const`
- `int hsvSaturation() const`
- `float hsvSaturationF() const`
- `int hue() const`
- `float hueF() const`
- `bool isValid() const`
- `QColor lighter(int factor = 150) const`
- `int lightness() const`
- `float lightnessF() const`
- `int magenta() const`
- `float magentaF() const`
- `QString name(QColor::NameFormat format = HexRgb) const`
- `int red() const`
- `float redF() const`
- `QRgb rgb() const`
- `QRgba64 rgba64() const`
- `QRgb rgba() const`
- `int saturation() const`
- `float saturationF() const`
- `void setAlpha(int alpha)`
- `void setAlphaF(float alpha)`
- `void setBlue(int blue)`
- `void setBlueF(float blue)`
- `void setCmyk(int c, int m, int y, int k, int a = 255)`
- `void setCmykF(float c, float m, float y, float k, float a = 1.0)`
- `void setGreen(int green)`
- `void setGreenF(float green)`
- `void setHsl(int h, int s, int l, int a = 255)`
- `void setHslF(float h, float s, float l, float a = 1.0)`
- `void setHsv(int h, int s, int v, int a = 255)`
- `void setHsvF(float h, float s, float v, float a = 1.0)`
- `void setRed(int red)`
- `void setRedF(float red)`
- `void setRgb(int r, int g, int b, int a = 255)`
- `void setRgb(QRgb rgb)`
- `void setRgba64(QRgba64 rgba)`
- `void setRgbF(float r, float g, float b, float a = 1.0)`
- `void setRgba(QRgb rgba)`
- `QColor::Spec spec() const`
- `QColor toCmyk() const`
- `QColor toExtendedRgb() const`
- `QColor toHsl() const`
- `QColor toHsv() const`
- `QColor toRgb() const`
- `int value() const`
- `float valueF() const`
- `int yellow() const`
- `float yellowF() const`
- `operator QVariant() const`
- `bool operator!=(const QColor &color) const`
- `QColor & operator=(Qt::GlobalColor color)`
- `bool operator==(const QColor &color) const`

### 静态公有成员

- `QStringList colorNames()`
- `QColor fromCmyk(int c, int m, int y, int k, int a = 255)`
- `QColor fromCmykF(float c, float m, float y, float k, float a = 1.0)`
- `QColor fromHsl(int h, int s, int l, int a = 255)`
- `QColor fromHslF(float h, float s, float l, float a = 1.0)`
- `QColor fromHsv(int h, int s, int v, int a = 255)`
- `QColor fromHsvF(float h, float s, float v, float a = 1.0)`
- `QColor fromRgb(QRgb rgb)`
- `QColor fromRgb(int r, int g, int b, int a = 255)`
- `QColor fromRgba64(QRgba64 rgba64)`
- `QColor fromRgba64(ushort r, ushort g, ushort b, ushort a = USHRT_MAX)`
- `QColor fromRgbF(float r, float g, float b, float a = 1.0)`
- `QColor fromRgba(QRgb rgba)`
- `(since 6.4) QColor fromString(QAnyStringView name)`
- `(since 6.4) bool isValidColorName(QAnyStringView name)`

### 相关非成员函数

- `QRgb`
- `int qAlpha(QRgb rgba)`
- `uint qAlpha(QRgba64 rgba64)`
- `int qBlue(QRgb rgb)`
- `uint qBlue(QRgba64 rgba64)`
- `int qGray(int r, int g, int b)`
- `int qGray(QRgb rgb)`
- `int qGreen(QRgb rgb)`
- `uint qGreen(QRgba64 rgba64)`
- `QRgb qPremultiply(QRgb rgb)`
- `QRgba64 qPremultiply(QRgba64 rgba64)`
- `int qRed(QRgb rgb)`
- `uint qRed(QRgba64 rgba64)`
- `QRgb qRgb(int r, int g, int b)`
- `QRgba64 qRgba64(quint64 c)`
- `QRgba64 qRgba64(quint16 r, quint16 g, quint16 b, quint16 a)`
- `QRgb qRgba(int r, int g, int b, int a)`
- `QRgb qUnpremultiply(QRgb rgb)`
- `QRgba64 qUnpremultiply(QRgba64 rgba64)`
- `QDataStream & operator<<(QDataStream &stream, const QColor &color)`
- `QDataStream & operator>>(QDataStream &stream, QColor &color)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QColor::NameFormat`

**作用与语义：**

如何格式化`name()`函数的输出。
- `QColor::HexRgb`：`0`;#RRGGBB 一个“#”字符后跟三个两位数十六进制数字（即`#RRGGBB`）。
- `QColor::HexArgb`：`1`;#AARRGGBB 一个“#”字符，后跟四个两位十六进制数字（即`#AARRGGBB`）。

### `enum QColor::Spec`

**作用与语义：**

指定颜色类型，包括RGB、扩展RGB、HSV、CMYK或HSL。
- `QColor::Rgb`：`1`
- `QColor::Hsv`：`2`
- `QColor::Cmyk`：`3`
- `QColor::Hsl`：`4`
- `QColor::ExtendedRgb`：`5`
- `QColor::Invalid`：`0`

### `[constexpr noexcept] QColor::QColor()`

**作用与语义：**

构造一个带有RGB值（0， 0， 0）的无效颜色。无效颜色是指未为底层窗口系统正确设置的颜色。
无效颜色的α值未被指定。

### `[noexcept] QColor::QColor(QRgb color)`

**作用与语义：**

构造一个颜色，取值为`color`。忽略alpha成分，设置为实心。

### `[noexcept] QColor::QColor(QRgba64 rgba64)`

**作用与语义：**

构造一个色彩，其值为 `rgba64`。

### `QColor::QColor(const QString &name)`

**作用与语义：**

以与`fromString()`相同的方式，使用给定的`name`构造命名颜色。
如果无法解析`name`，颜色则保持无效。

### `[constexpr noexcept] QColor::QColor(int r, int g, int b, int a = 255)`

**作用与语义：**

构造出RGB值为`r`、`g`、`b`和α通道（透明度）值为`a`的颜色。
如果任何参数无效，颜色就保持无效。

### `QColor::QColor(QLatin1StringView name)`

**作用与语义：**

以与`fromString()`相同的方式构造命名颜色，使用给定的`name`。

### `[noexcept] QColor::QColor(Qt::GlobalColor color)`

**作用与语义：**

构造一个颜色值为`color`的新颜色。

### `QColor::QColor(const char *name)`

**作用与语义：**

以与`fromString()`相同的方式构造命名颜色，使用给定的`name`。

### `[noexcept] int QColor::alpha() const`

**作用与语义：**

返回该颜色的alpha色分量。

### `[noexcept] float QColor::alphaF() const`

**作用与语义：**

返回该颜色的alpha色分量。

### `[noexcept] int QColor::black() const`

**作用与语义：**

返回该颜色的黑色成分。

### `[noexcept] float QColor::blackF() const`

**作用与语义：**

返回该颜色的黑色成分。

### `[noexcept] int QColor::blue() const`

**作用与语义：**

返回该颜色的蓝色分量。

### `[noexcept] float QColor::blueF() const`

**作用与语义：**

返回该颜色的蓝色分量。

### `[static] QStringList QColor::colorNames()`

**作用与语义：**

返回包含Qt已知颜色名称的`QStringList`。

### `[noexcept] QColor QColor::convertTo(QColor::Spec colorSpec) const`

**作用与语义：**

以`colorSpec`指定格式创建该颜色的副本。

### `[noexcept] int QColor::cyan() const`

**作用与语义：**

返回该颜色的青色成分。

### `[noexcept] float QColor::cyanF() const`

**作用与语义：**

返回该颜色的青色成分。

### `[noexcept] QColor QColor::darker(int factor = 200) const`

**作用与语义：**

返回更深（或更浅）的颜色，但不会改变该对象。
如果`factor`大于100，该函数返回的颜色会变暗。将`factor`设为300，返回的颜色亮度只有三分之一。如果`factor`小于100，返回颜色较浅，但我们建议使用`lighter()`函数来实现此目的。如果`factor`为0或负数，返回值未指定。
该函数将当前颜色转换为HSV，将值（V）分量除以`factor`，并将颜色转换回其原始颜色规格。

### `[static] QColor QColor::fromCmyk(int c, int m, int y, int k, int a = 255)`

**作用与语义：**

静态便利函数，返回由给定的CMYK色彩值构成的`QColor`：`c`（青色）、`m`（品红色）、`y`（黄色）、`k`（黑色）和`a`（alpha通道，即透明）。
所有数值必须在0-255之间。

### `[static] QColor QColor::fromCmykF(float c, float m, float y, float k, float a = 1.0)`

**作用与语义：**

静态便利函数，返回由给定的CMYK色彩值构成的`QColor`：`c`（青）、`m`（品红）、`y`（黄色）、`k`（黑色）和`a`（α通道，即透明）。
所有值必须在0.0到1.0之间。

### `[static] QColor QColor::fromHsl(int h, int s, int l, int a = 255)`

**作用与语义：**

静态便利函数，返回由HSV色彩值构成的`QColor`，分别是`h`（色相）、`s`（饱和度）、`l`（明度）和`a`（α通道，即透明度）。
`s`、`l`和`a`的值都必须在0-255之间;`h`的值必须在0-359之间。

### `[static] QColor QColor::fromHslF(float h, float s, float l, float a = 1.0)`

**作用与语义：**

静态便利函数，返回由HSV色彩值构成的`QColor`，分别是`h`（色调）、`s`（饱和度）、`l`（明度）和`a`（α通道，即透明度）。
所有值必须在0.0到1.0之间。

### `[static] QColor QColor::fromHsv(int h, int s, int v, int a = 255)`

**作用与语义：**

静态便利函数，返回由HSV色彩值构成的`QColor`，分别是`h`（色调）、`s`（饱和度）、`v`（明度）和`a`（透明度）。
`s`、`v`和`a`的值都必须在0-255之间;`h`的值必须在0-359之间。

### `[static] QColor QColor::fromHsvF(float h, float s, float v, float a = 1.0)`

**作用与语义：**

静态便利函数，返回由HSV色彩值构成的`QColor`，分别是`h`（色调）、`s`（饱和度）、`v`（明度）和`a`（α通道，即透明度）。
所有值必须在0.0到1.0之间。

### `[static noexcept] QColor QColor::fromRgb(QRgb rgb)`

**作用与语义：**

静态便利函数，返回由给定`QRgb`值构造的`QColor` `rgb`。
`rgb`的α成分被忽略（即自动设置为255），使用`fromRgba()`函数包含由给定`QRgb`值指定的α通道。

### `[static] QColor QColor::fromRgb(int r, int g, int b, int a = 255)`

**作用与语义：**

静态便利函数，返回由RGB颜色值构成的`QColor`，分别是`r`（红色）、`g`（绿色）、`b`（蓝色）和`a`（alpha通道，即透明）。
所有数值必须在0-255之间。

### `[static noexcept] QColor QColor::fromRgba64(QRgba64 rgba64)`

**作用与语义：**

静态便利函数，返回由给定`QRgba64`值构造的`QColor` `rgba64`。

### `[static noexcept] QColor QColor::fromRgba64(ushort r, ushort g, ushort b, ushort a = USHRT_MAX)`

**作用与语义：**

静态便利函数，返回由RGBA64颜色值构成的`QColor`，分别是`r`（红色）、`g`（绿色）、`b`（蓝色）和`a`（alpha通道，即透明度）。

### `[static] QColor QColor::fromRgbF(float r, float g, float b, float a = 1.0)`

**作用与语义：**

静态便利函数，返回由RGB颜色值构成的`QColor`，分别是`r`（红色）、`g`（绿色）、`b`（蓝色）和`a`（alpha通道，即透明）。
alpha值必须在0.0-1.0范围内。如果其他值超出0.0-1.0范围，颜色模型将设置为`ExtendedRgb`。

### `[static noexcept] QColor QColor::fromRgba(QRgb rgba)`

**作用与语义：**

静态便利函数，返回由给定`QRgb`值构造的`QColor` `rgba`。
与`fromRgb()`函数不同，包含由给定`QRgb`值指定的α通道。

### `[static noexcept, since 6.4] QColor QColor::fromString(QAnyStringView name)`

**作用与语义：**

返回从`name`解析的RGB信号`QColor`，格式如下：
- #RGB（R、G、B各为一个十六进制数字）
- #RRGGBB
- #AARRGGBB（自5.2版本起）
- #RRRGGGBBB
- #RRRRGGGGBBBB
- 来自万维网联盟提供的SVG颜色关键词列表中定义的颜色列表中的名称;例如，“steelblue”或“gainsboro”。这些颜色名称适用于所有平台。注意这些颜色名称与`Qt::GlobalColor`枚举定义不同，例如“green”和`Qt::green`不指同一颜色。
- `transparent` - 表示颜色的缺失。
如果无法解析，返回无效颜色`name`。

### `void QColor::getCmyk(int *c, int *m, int *y, int *k, int *a = nullptr) const`

**作用与语义：**

将`c`、`m`、`y`、`k`和`a`所指向的内容，设置为颜色CMYK值中的青色、品红色、黄色、黑色和α通道（透明度）成分。
这些组件可以通过`cyan()`、`magenta()`、`yellow()`、`black()`和`alpha()`函数单独检索。

### `void QColor::getCmykF(float *c, float *m, float *y, float *k, float *a = nullptr) const`

**作用与语义：**

将`c`、`m`、`y`、`k`和`a`所指向的内容，设置为颜色CMYK值中的青色、品红色、黄色、黑色和α通道（透明度）成分。
这些组件可以通过`cyanF()`、`magentaF()`、`yellowF()`、`blackF()`和`alphaF()`函数单独检索。

### `void QColor::getHsl(int *h, int *s, int *l, int *a = nullptr) const`

**作用与语义：**

将`h`、`s`、`l`和`a`所指向的内容，设置为颜色HSL值的色相、饱和度、明度和alpha通道（透明度）分量。
这些组件可以通过`hslHue()`、`hslSaturation()`、`lightness()`和`alpha()`函数单独检索。

### `void QColor::getHslF(float *h, float *s, float *l, float *a = nullptr) const`

**作用与语义：**

将`h`、`s`、`l`和`a`所指向的内容，设置为颜色HSL值的色相、饱和度、明度和α通道（透明度）分量。
这些组件可以通过`hslHueF()`、`hslSaturationF()`、`lightnessF()`和`alphaF()`函数单独检索。

### `void QColor::getHsv(int *h, int *s, int *v, int *a = nullptr) const`

**作用与语义：**

将`h`、`s`、`v`和`a`所指向的内容设置为颜色的HSV值中的色调、饱和度、明暗和透明度（alpha通道）分量。
这些组件可以通过`hue()`、`saturation()`、`value()`和`alpha()`函数单独检索。

### `void QColor::getHsvF(float *h, float *s, float *v, float *a = nullptr) const`

**作用与语义：**

将`h`、`s`、`v`和`a`所指向的内容，设置为颜色HSV值中的色相、饱和度、明暗和透明度（alpha通道）分量。
这些组件可以通过`hueF()`、`saturationF()`、`valueF()`和`alphaF()`函数单独检索。

### `void QColor::getRgb(int *r, int *g, int *b, int *a = nullptr) const`

**作用与语义：**

将`r`、`g`、`b`和`a`所指向的内容设置为颜色RGB值中的红、绿、蓝和α通道（透明）分量。
这些组件可以通过`red()`、`green()`、`blue()`和`alpha()`函数单独检索。

### `void QColor::getRgbF(float *r, float *g, float *b, float *a = nullptr) const`

**作用与语义：**

将`r`、`g`、`b`和`a`所指向的内容设置为颜色RGB值中的红、绿、蓝和alpha通道（透明度）分量。
这些组件可以通过`redF()`、`greenF()`、`blueF()`和`alphaF()`函数单独检索。

### `[noexcept] int QColor::green() const`

**作用与语义：**

返回该颜色的绿色分量。

### `[noexcept] float QColor::greenF() const`

**作用与语义：**

返回该颜色的绿色分量。

### `[noexcept] int QColor::hslHue() const`

**作用与语义：**

返回该颜色的HSL色相分量。

### `[noexcept] float QColor::hslHueF() const`

**作用与语义：**

返回该颜色的HSL色相分量。

### `[noexcept] int QColor::hslSaturation() const`

**作用与语义：**

返回该颜色的HSL饱和色彩分量。

### `[noexcept] float QColor::hslSaturationF() const`

**作用与语义：**

返回该颜色的HSL饱和色彩分量。

### `[noexcept] int QColor::hsvHue() const`

**作用与语义：**

返回该颜色的HSV色相成分。

### `[noexcept] float QColor::hsvHueF() const`

**作用与语义：**

返回该颜色的色相成分。

### `[noexcept] int QColor::hsvSaturation() const`

**作用与语义：**

返回该颜色的HSV饱和色彩分量。

### `[noexcept] float QColor::hsvSaturationF() const`

**作用与语义：**

返回该颜色的HSV饱和色彩分量。

### `[noexcept] int QColor::hue() const`

**作用与语义：**

返回该颜色的HSV色相成分。
颜色隐含地转化为HSV。

### `[noexcept] float QColor::hueF() const`

**作用与语义：**

返回该颜色的HSV色相成分。
颜色隐含地转化为HSV。

### `[noexcept] bool QColor::isValid() const`

**作用与语义：**

如果颜色有效，返回`true`;否则返回`false`。

### `[static noexcept, since 6.4] bool QColor::isValidColorName(QAnyStringView name)`

**作用与语义：**

如果`name`是有效的颜色名称并且可以用来构造有效的`QColor`对象，则返回`true`，否则返回false。
它使用了`fromString()`中使用的相同算法。

### `[noexcept] QColor QColor::lighter(int factor = 150) const`

**作用与语义：**

返回较浅（或更暗）的颜色，但不会改变该对象。
如果`factor`大于100，该函数返回的颜色会变浅。将`factor`设为150，返回颜色亮度提升50%。如果`factor`小于100，返回颜色较暗，但我们建议使用`darker()`函数来实现此目的。如果`factor`为0或负数，返回值未指定。
该函数将当前颜色转换为HSV，将值（V）分量乘以`factor`，并将颜色转换回其原始颜色规格。

### `[noexcept] int QColor::lightness() const`

**作用与语义：**

返回该颜色的明度颜色分量。

### `[noexcept] float QColor::lightnessF() const`

**作用与语义：**

返回该颜色的明度颜色分量。

### `[noexcept] int QColor::magenta() const`

**作用与语义：**

返回该颜色的品红色成分。

### `[noexcept] float QColor::magentaF() const`

**作用与语义：**

返回该颜色的品红色成分。

### `QString QColor::name(QColor::NameFormat format = HexRgb) const`

**作用与语义：**

返回指定`format`中颜色的名称。

### `[noexcept] int QColor::red() const`

**作用与语义：**

返回该颜色的红色分量。

### `[noexcept] float QColor::redF() const`

**作用与语义：**

返回该颜色的红色分量。

### `[noexcept] QRgb QColor::rgb() const`

**作用与语义：**

返回颜色的RGB值。alpha值是不透明的。

### `[noexcept] QRgba64 QColor::rgba64() const`

**作用与语义：**

返回颜色的RGB64值，包括其alpha值。
对于无效颜色，返回颜色的α值未指定。

### `[noexcept] QRgb QColor::rgba() const`

**作用与语义：**

返回颜色的RGB值，包括其alpha。
对于无效颜色，返回颜色的α值未指定。

### `[noexcept] int QColor::saturation() const`

**作用与语义：**

返回该颜色的HSV饱和色彩分量。
颜色隐含地转化为HSV。

### `[noexcept] float QColor::saturationF() const`

**作用与语义：**

返回该颜色的HSV饱和色彩分量。
颜色隐含地转化为HSV。

### `void QColor::setAlpha(int alpha)`

**作用与语义：**

将该颜色的α设为`alpha`。整数α定义在0-255范围内。

### `void QColor::setAlphaF(float alpha)`

**作用与语义：**

将该颜色的α设为`alpha`。浮子α定义在0.0-1.0的范围内。

### `void QColor::setBlue(int blue)`

**作用与语义：**

将该颜色的蓝色分量设置为`blue`。整数分量指定在0-255之间。

### `void QColor::setBlueF(float blue)`

**作用与语义：**

将该颜色的蓝色分量设置为`blue`。如果`blue`在0.0-1.0范围内，颜色模型将被更改为`ExtendedRgb`。

### `void QColor::setCmyk(int c, int m, int y, int k, int a = 255)`

**作用与语义：**

将颜色设置为CMYK值，分别是`c`（青色）、`m`（品红色）、`y`（黄色）、`k`（黑色）和`a`（透明度）。
所有数值必须在0-255之间。

### `void QColor::setCmykF(float c, float m, float y, float k, float a = 1.0)`

**作用与语义：**

将颜色设置为CMYK值，分别是`c`（青色）、`m`（品红色）、`y`（黄色）、`k`（黑色）和`a`（透明度）。
所有值必须在0.0到1.0之间。

### `void QColor::setGreen(int green)`

**作用与语义：**

将该颜色的绿色分量设置为`green`。整数分量指定在0-255之间。

### `void QColor::setGreenF(float green)`

**作用与语义：**

将该颜色的绿色分量设置为`green`。如果`green`超出0.0-1.0范围，颜色模型将改为`ExtendedRgb`。

### `void QColor::setHsl(int h, int s, int l, int a = 255)`

**作用与语义：**

设定HSL色彩值;`h`为色相，`s`为饱和度，`l`为亮度，`a`为HSL颜色的α成分。
饱和度、明度和α通道值必须在0-255之间，色相值必须大于-1。

### `void QColor::setHslF(float h, float s, float l, float a = 1.0)`

**作用与语义：**

设定HSL颜色的浅度;`h`是色相，`s`是饱和度，`l`是亮度，`a`是HSL颜色的α成分。
所有值必须在0.0到1.0之间。

### `void QColor::setHsv(int h, int s, int v, int a = 255)`

**作用与语义：**

设置HSV颜色值;`h`为色相，`s`为饱和度，`v`为数值，`a`为HSV颜色的α成分。
饱和度、明度和α通道值必须在0-255之间，色相值必须大于-1。

### `void QColor::setHsvF(float h, float s, float v, float a = 1.0)`

**作用与语义：**

设置HSV颜色值;`h`为色相，`s`为饱和度，`v`为数值，`a`为HSV颜色的α成分。
所有值必须在0.0到1.0之间。

### `void QColor::setRed(int red)`

**作用与语义：**

将该颜色的红色分量设置为`red`。整数分量指定在0-255范围内。

### `void QColor::setRedF(float red)`

**作用与语义：**

将该颜色的红色分量设置为`red`。如果`red`位于0.0-1.0范围之外，颜色模型将被更改为`ExtendedRgb`。

### `void QColor::setRgb(int r, int g, int b, int a = 255)`

**作用与语义：**

将RGB值设置为`r`、`g`、`b`，alpha值设为`a`。
所有数值必须在0-255之间。

### `[noexcept] void QColor::setRgb(QRgb rgb)`

**作用与语义：**

将RGB值设置为`rgb`。alpha值设置为不透明。

### `[noexcept] void QColor::setRgba64(QRgba64 rgba)`

**作用与语义：**

将RGB64值设置为`rgba`，包括其alpha值。

### `void QColor::setRgbF(float r, float g, float b, float a = 1.0)`

**作用与语义：**

将该颜色的色彩通道设置为`r`（红色）、`g`（绿色）、`b`（蓝色）和`a`（透明度）。
alpha值必须在0.0-1.0范围内。如果其他值超出0.0-1.0范围，颜色模型将设置为`ExtendedRgb`。

### `[noexcept] void QColor::setRgba(QRgb rgba)`

**作用与语义：**

将RGB值设置为`rgba`，包括其alpha值。

### `[noexcept] QColor::Spec QColor::spec() const`

**作用与语义：**

返回颜色的指定方式。

### `[noexcept] QColor QColor::toCmyk() const`

**作用与语义：**

基于该颜色创建并返回CMYK的CMYK信号`QColor`。

### `[noexcept] QColor QColor::toExtendedRgb() const`

**作用与语义：**

基于该颜色创建并返回扩展RGB的RGB `QColor`。

### `[noexcept] QColor QColor::toHsl() const`

**作用与语义：**

基于该颜色创建并返回HSL的`QColor`。

### `[noexcept] QColor QColor::toHsv() const`

**作用与语义：**

基于该颜色创建并返回HSV的`QColor`。

### `[noexcept] QColor QColor::toRgb() const`

**作用与语义：**

创建并返回基于该颜色的RGB信号`QColor`。

### `[noexcept] int QColor::value() const`

**作用与语义：**

返回该颜色的值颜色分量。

### `[noexcept] float QColor::valueF() const`

**作用与语义：**

返回该颜色的值颜色分量。

### `[noexcept] int QColor::yellow() const`

**作用与语义：**

返回该颜色的黄色分量。

### `[noexcept] float QColor::yellowF() const`

**作用与语义：**

返回该颜色的黄色分量。

### `QColor::operator QVariant() const`

**作用与语义：**

返回颜色作为 `QVariant`。

### `[noexcept] bool QColor::operator!=(const QColor &color) const`

**作用与语义：**

如果该颜色与`color`颜色规格或组件值不同，返回`true`;否则返回`false`。
在此语境下，`ExtendedRgb`和RGB规范被视为匹配。

### `[noexcept] QColor &QColor::operator=(Qt::GlobalColor color)`

**作用与语义：**

分配一份 `color` 并返回该颜色的引用。

### `[noexcept] bool QColor::operator==(const QColor &color) const`

**作用与语义：**

如果该颜色的颜色规格和分量值与`color`相同，则返回`true`;否则返回`false`。
在此语境下，`ExtendedRgb`和RGB规范被视为匹配。

### `QRgb`

**作用与语义：**

格式 #AARRGGBB 上的 ARGB 四元音，相当于无符号的 int。
该类型还包含 alpha 通道的值。默认的 alpha 通道是`ff`，即不透明的。更多信息请参见 Alpha 混合绘图部分。
以下是一些QRgb值的创建示例：

**官方示例：**

```cpp
 const QRgb rgb1 = 0x88112233;
 const QRgb rgb2 = QColor("red").rgb();
 const QRgb rgb3 = qRgb(qRed(rgb1), qGreen(rgb2), qBlue(rgb2));
 const QRgb rgb4 = qRgba(qRed(rgb1), qGreen(rgb2), qBlue(rgb2), qAlpha(rgb1));
```

### `[constexpr] int qAlpha(QRgb rgba)`

**作用与语义：**

返回ARGB四联组的α部分`rgba`。

### `[constexpr] uint qAlpha(QRgba64 rgba64)`

**作用与语义：**

返回`rgba64`的alpha分量为8位值。

### `[constexpr] int qBlue(QRgb rgb)`

**作用与语义：**

返回ARGB四联组的蓝色分量`rgb`。

### `[constexpr] uint qBlue(QRgba64 rgba64)`

**作用与语义：**

返回`rgba64`的蓝色分量为8位值。

### `[constexpr] int qGray(int r, int g, int b)`

**作用与语义：**

返回从（`r`， `g`， `b`）三元组中返回一个灰色值（0到255）。
灰度的数值采用公式（`r` * 11 `g` * 16 `b` * 5）/32 计算。

### `[constexpr] int qGray(QRgb rgb)`

**作用与语义：**

返回给定ARGB四元组`rgb`的灰色值（0到255）。
灰色值使用公式（R * 11 G * 16 B * 5）/32计算;忽略了阿尔法通道。

### `[constexpr] int qGreen(QRgb rgb)`

**作用与语义：**

返回ARGB四联组的绿色分量`rgb`。

### `[constexpr] uint qGreen(QRgba64 rgba64)`

**作用与语义：**

返回`rgba64`的绿色分量为8位值。

### `[constexpr] QRgb qPremultiply(QRgb rgb)`

**作用与语义：**

将未预乘的ARGB四联组`rgb`转换为预乘ARGB四联。

### `[constexpr] QRgba64 qPremultiply(QRgba64 rgba64)`

**作用与语义：**

将未预乘的`QRgba64`四重态`rgba64`转换为预乘的`QRgba64`四重态。

### `[constexpr] int qRed(QRgb rgb)`

**作用与语义：**

返回ARGB四联组的红色分量`rgb`。

### `[constexpr] uint qRed(QRgba64 rgba64)`

**作用与语义：**

返回`rgba64`的红色分量为8位值。

### `[constexpr] QRgb qRgb(int r, int g, int b)`

**作用与语义：**

回归ARGB四联组（255、`r`、`g`、`b`）。

### `[constexpr] QRgba64 qRgba64(quint64 c)`

**作用与语义：**

`c`以`QRgba64`结构体的形式返回。

### `[constexpr] QRgba64 qRgba64(quint16 r, quint16 g, quint16 b, quint16 a)`

**作用与语义：**

返回`QRgba64`四胞胎（`r`、`g`、`b`、`a`）。

### `[constexpr] QRgb qRgba(int r, int g, int b, int a)`

**作用与语义：**

返回ARGB四连体（`a`、`r`、`g`、`b`）。

### `QRgb qUnpremultiply(QRgb rgb)`

**作用与语义：**

将预乘的ARGB四联组`rgb`转换为未预乘的ARGB四联组。

### `[constexpr] QRgba64 qUnpremultiply(QRgba64 rgba64)`

**作用与语义：**

将预乘的`QRgba64`四连`rgba64`转换成未预乘的`QRgba64`四连态。

### `QDataStream &operator<<(QDataStream &stream, const QColor &color)`

**作用与语义：**

写`color`给`stream`。

### `QDataStream &operator>>(QDataStream &stream, QColor &color)`

**作用与语义：**

从`stream`上读`color`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QColor` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
