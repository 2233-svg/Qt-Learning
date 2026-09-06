# QFont

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 字体描述类型，包含家族、大小、粗体、斜体等属性。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QFont`：字体描述类型，包含家族、大小、粗体、斜体等属性。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QFont>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.7) struct Tag`
- `enum Capitalization { MixedCase, AllUppercase, AllLowercase, SmallCaps, Capitalize }`
- `enum HintingPreference { PreferDefaultHinting, PreferNoHinting, PreferVerticalHinting, PreferFullHinting }`
- `enum SpacingType { PercentageSpacing, AbsoluteSpacing }`
- `enum Stretch { AnyStretch, UltraCondensed, ExtraCondensed, Condensed, SemiCondensed, …, UltraExpanded }`
- `enum Style { StyleNormal, StyleItalic, StyleOblique }`
- `enum StyleHint { AnyStyle, SansSerif, Helvetica, Serif, Times, …, System }`
- `enum StyleStrategy { PreferDefault, PreferBitmap, PreferDevice, PreferOutline, ForceOutline, …, PreferQuality }`
- `enum Weight { Thin, ExtraLight, Light, Normal, Medium, …, Black }`

### 公有函数

- `QFont()`
- `QFont(const QFont &font, const QPaintDevice *pd)`
- `QFont(const QString &family, int pointSize = -1, int weight = -1, bool italic = false)`
- `QFont(const QStringList &families, int pointSize = -1, int weight = -1, bool italic = false)`
- `QFont(const QFont &font)`
- `~QFont()`
- `bool bold() const`
- `QFont::Capitalization capitalization() const`
- `(since 6.7) void clearFeatures()`
- `(since 6.7) void clearVariableAxes()`
- `QString defaultFamily() const`
- `bool exactMatch() const`
- `QStringList families() const`
- `QString family() const`
- `(since 6.7) QList<QFont::Tag> featureTags() const`
- `(since 6.7) quint32 featureValue(QFont::Tag tag) const`
- `bool fixedPitch() const`
- `bool fromString(const QString &descrip)`
- `QFont::HintingPreference hintingPreference() const`
- `bool isCopyOf(const QFont &f) const`
- `(since 6.7) bool isFeatureSet(QFont::Tag tag) const`
- `(since 6.7) bool isVariableAxisSet(QFont::Tag tag) const`
- `bool italic() const`
- `bool kerning() const`
- `QString key() const`
- `qreal letterSpacing() const`
- `QFont::SpacingType letterSpacingType() const`
- `bool overline() const`
- `int pixelSize() const`
- `int pointSize() const`
- `qreal pointSizeF() const`
- `QFont resolve(const QFont &other) const`
- `void setBold(bool enable)`
- `void setCapitalization(QFont::Capitalization caps)`
- `void setFamilies(const QStringList &families)`
- `void setFamily(const QString &family)`
- `(since 6.7) void setFeature(QFont::Tag tag, quint32 value)`
- `void setFixedPitch(bool enable)`
- `void setHintingPreference(QFont::HintingPreference hintingPreference)`
- `void setItalic(bool enable)`
- `void setKerning(bool enable)`
- `void setLetterSpacing(QFont::SpacingType type, qreal spacing)`
- `void setOverline(bool enable)`
- `void setPixelSize(int pixelSize)`
- `void setPointSize(int pointSize)`
- `void setPointSizeF(qreal pointSize)`
- `void setStretch(int factor)`
- `void setStrikeOut(bool enable)`
- `void setStyle(QFont::Style style)`
- `void setStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = PreferDefault)`
- `void setStyleName(const QString &styleName)`
- `void setStyleStrategy(QFont::StyleStrategy s)`
- `void setUnderline(bool enable)`
- `(since 6.7) void setVariableAxis(QFont::Tag tag, float value)`
- `void setWeight(QFont::Weight weight)`
- `void setWordSpacing(qreal spacing)`
- `int stretch() const`
- `bool strikeOut() const`
- `QFont::Style style() const`
- `QFont::StyleHint styleHint() const`
- `QString styleName() const`
- `QFont::StyleStrategy styleStrategy() const`
- `void swap(QFont &other)`
- `QString toString() const`
- `bool underline() const`
- `(since 6.7) void unsetFeature(QFont::Tag tag)`
- `(since 6.7) void unsetVariableAxis(QFont::Tag tag)`
- `(since 6.7) QList<QFont::Tag> variableAxisTags() const`
- `(since 6.7) float variableAxisValue(QFont::Tag tag) const`
- `QFont::Weight weight() const`
- `qreal wordSpacing() const`
- `operator QVariant() const`
- `bool operator!=(const QFont &f) const`
- `bool operator<(const QFont &f) const`
- `QFont & operator=(QFont &&other)`
- `QFont & operator=(const QFont &font)`
- `bool operator==(const QFont &f) const`

### 静态公有成员

- `void insertSubstitution(const QString &familyName, const QString &substituteName)`
- `void insertSubstitutions(const QString &familyName, const QStringList &substituteNames)`
- `void removeSubstitutions(const QString &familyName)`
- `QString substitute(const QString &familyName)`
- `QStringList substitutes(const QString &familyName)`
- `QStringList substitutions()`

### 相关非成员函数

- `size_t qHash(const QFont &key, size_t seed = 0)`
- `QDataStream & operator<<(QDataStream &s, const QFont &font)`
- `QDataStream & operator>>(QDataStream &s, QFont &font)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 95 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QFont::Capitalization`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Capitalization`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Capitalization`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFont::HintingPreference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Hinting、Preference`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:HintingPreference`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFont::Stretch`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Stretch`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Stretch`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFont::Style`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Style`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Style`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFont::StyleHint`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Style、Hint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StyleHint`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFont::StyleStrategy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Style、Strategy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StyleStrategy`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFont::Weight`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFont` 暴露的类型声明 `Weight`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Weight`。
- 属性名：`QFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::QFont()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::QFont(const QFont &font, const QPaintDevice *pd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pd`：类型为 `const QPaintDevice *`。没有默认值，调用时必须提供。传入 `const QPaintDevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::QFont(const QString &family, int pointSize = -1, int weight = -1, bool italic = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `family`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pointSize`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `weight`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `italic`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFont::QFont(const QStringList &families, int pointSize = -1, int weight = -1, bool italic = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `families`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pointSize`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `weight`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `italic`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::QFont(const QFont &font)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QFont::~QFont()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::bold() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::bold` 用于计算、查询或取得与“bold”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::Capitalization QFont::capitalization() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::capitalization` 用于计算、查询或取得与“capitalization”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::Capitalization`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::Capitalization`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QFont::clearFeatures()`

**API 类别：** 成员函数说明

**中文解读：** `QFont::clearFeatures` 用于执行与“清空、Features”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QFont::clearVariableAxes()`

**API 类别：** 成员函数说明

**中文解读：** `QFont::clearVariableAxes` 用于执行与“清空、Variable、Axes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFont::defaultFamily() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::defaultFamily` 用于计算、查询或取得与“default、Family”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::exactMatch() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::exactMatch` 用于计算、查询或取得与“exact、匹配”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QFont::families() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::families` 用于计算、查询或取得与“families”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFont::family() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::family` 用于计算、查询或取得与“family”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QList<QFont::Tag> QFont::featureTags() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::featureTags` 用于计算、查询或取得与“feature、Tags”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QFont::Tag>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QFont::Tag>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] quint32 QFont::featureValue(QFont::Tag tag) const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::featureValue` 用于计算、查询或取得与“feature、值访问”相关的操作。调用时要先确认当前状态和 `tag` 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::fixedPitch() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::fixedPitch` 用于计算、查询或取得与“fixed、Pitch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::fromString(const QString &descrip)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `fromString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`bool`。
- 参数 `descrip`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::HintingPreference QFont::hintingPreference() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::hintingPreference` 用于计算、查询或取得与“hinting、Preference”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::HintingPreference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::HintingPreference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QFont::insertSubstitution(const QString &familyName, const QString &substituteName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `insertSubstitution`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `familyName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `substituteName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QFont::insertSubstitutions(const QString &familyName, const QStringList &substituteNames)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `insertSubstitutions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `familyName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `substituteNames`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::isCopyOf(const QFont &f) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCopyOf`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `f`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] bool QFont::isFeatureSet(QFont::Tag tag) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFeatureSet`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] bool QFont::isVariableAxisSet(QFont::Tag tag) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isVariableAxisSet`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::italic() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::italic` 用于计算、查询或取得与“italic”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::kerning() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::kerning` 用于计算、查询或取得与“kerning”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFont::key() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QFont::letterSpacing() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::letterSpacing` 用于计算、查询或取得与“letter、Spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::SpacingType QFont::letterSpacingType() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::letterSpacingType` 用于计算、查询或取得与“letter、Spacing、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::SpacingType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::SpacingType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::overline() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::overline` 用于计算、查询或取得与“overline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFont::pixelSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::pixelSize` 用于计算、查询或取得与“pixel、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFont::pointSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::pointSize` 用于计算、查询或取得与“point、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QFont::pointSizeF() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::pointSizeF` 用于计算、查询或取得与“point、尺寸或数量、F”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QFont::removeSubstitutions(const QString &familyName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `removeSubstitutions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `familyName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont QFont::resolve(const QFont &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::resolve` 用于计算、查询或取得与“resolve”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数 `other`：类型为 `const QFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setBold(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBold`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setCapitalization(QFont::Capitalization caps)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCapitalization`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `caps`：类型为 `QFont::Capitalization`。没有默认值，调用时必须提供。传入 `QFont::Capitalization` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setFamilies(const QStringList &families)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFamilies`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `families`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setFamily(const QString &family)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFamily`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `family`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QFont::setFeature(QFont::Tag tag, quint32 value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFeature`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `quint32`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setFixedPitch(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFixedPitch`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setHintingPreference(QFont::HintingPreference hintingPreference)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHintingPreference`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hintingPreference`：类型为 `QFont::HintingPreference`。没有默认值，调用时必须提供。传入 `QFont::HintingPreference` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setItalic(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItalic`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setKerning(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKerning`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setLetterSpacing(QFont::SpacingType type, qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLetterSpacing`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `type`：类型为 `QFont::SpacingType`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setOverline(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOverline`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setPixelSize(int pixelSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPixelSize`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pixelSize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setPointSize(int pointSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPointSize`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointSize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setPointSizeF(qreal pointSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPointSizeF`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setStretch(int factor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStretch`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `factor`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setStrikeOut(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStrikeOut`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setStyle(QFont::Style style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyle`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `QFont::Style`。没有默认值，调用时必须提供。传入 `QFont::Style` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = PreferDefault)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyleHint`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hint`：类型为 `QFont::StyleHint`。没有默认值，调用时必须提供。传入 `QFont::StyleHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `strategy`：类型为 `QFont::StyleStrategy`。默认值为 `PreferDefault`。传入 `QFont::StyleStrategy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setStyleName(const QString &styleName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyleName`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `styleName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setStyleStrategy(QFont::StyleStrategy s)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyleStrategy`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `s`：类型为 `QFont::StyleStrategy`。没有默认值，调用时必须提供。传入 `QFont::StyleStrategy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setUnderline(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnderline`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QFont::setVariableAxis(QFont::Tag tag, float value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVariableAxis`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `float`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setWeight(QFont::Weight weight)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWeight`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `weight`：类型为 `QFont::Weight`。没有默认值，调用时必须提供。传入 `QFont::Weight` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFont::setWordSpacing(qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWordSpacing`。调用它会改变 `QFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFont::stretch() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::stretch` 用于计算、查询或取得与“stretch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::strikeOut() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::strikeOut` 用于计算、查询或取得与“strike、Out”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::Style QFont::style() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::style` 用于计算、查询或取得与“style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::Style`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::Style`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::StyleHint QFont::styleHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::styleHint` 用于计算、查询或取得与“style、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::StyleHint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::StyleHint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFont::styleName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::styleName` 用于计算、查询或取得与“style、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::StyleStrategy QFont::styleStrategy() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::styleStrategy` 用于计算、查询或取得与“style、Strategy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::StyleStrategy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::StyleStrategy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFont::substitute(const QString &familyName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `substitute`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `familyName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QFont::substitutes(const QString &familyName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `substitutes`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `familyName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QFont::substitutions()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `substitutions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QFont::swap(QFont &other)`

**API 类别：** 成员函数说明

**中文解读：** `QFont::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFont::toString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::underline() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::underline` 用于计算、查询或取得与“underline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QFont::unsetFeature(QFont::Tag tag)`

**API 类别：** 成员函数说明

**中文解读：** `QFont::unsetFeature` 用于执行与“unset、Feature”相关的操作。调用时要先确认当前状态和 `tag` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QFont::unsetVariableAxis(QFont::Tag tag)`

**API 类别：** 成员函数说明

**中文解读：** `QFont::unsetVariableAxis` 用于执行与“unset、Variable、Axis”相关的操作。调用时要先确认当前状态和 `tag` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QList<QFont::Tag> QFont::variableAxisTags() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::variableAxisTags` 用于计算、查询或取得与“variable、Axis、Tags”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QFont::Tag>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QFont::Tag>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] float QFont::variableAxisValue(QFont::Tag tag) const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::variableAxisValue` 用于计算、查询或取得与“variable、Axis、值访问”相关的操作。调用时要先确认当前状态和 `tag` 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::Weight QFont::weight() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::weight` 用于计算、查询或取得与“weight”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::Weight`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::Weight`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QFont::wordSpacing() const`

**API 类别：** 成员函数说明

**中文解读：** `QFont::wordSpacing` 用于计算、查询或取得与“word、Spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::operator!=(const QFont &f) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `f`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::operator<(const QFont &f) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `f`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QFont &QFont::operator=(QFont &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QFont &`。
- 参数 `other`：类型为 `QFont &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont &QFont::operator=(const QFont &font)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QFont &`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFont::operator==(const QFont &f) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `f`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QFont &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QFont::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QFont &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &s, const QFont &font)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `s`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &s, QFont &font)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `s`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `font`：类型为 `QFont &`。没有默认值，调用时必须提供。传入 `QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.7) struct Tag`

**API 类别：** 公有类型

**中文解读：** 这是 `QFont` 的 `Tag` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SpacingType { PercentageSpacing, AbsoluteSpacing }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFont` 暴露的类型声明 `Spacing、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFont` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
