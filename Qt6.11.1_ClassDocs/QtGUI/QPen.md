# QPen

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 轮廓绘制属性，负责线宽、颜色、线型、端点和连接样式。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPen`：轮廓绘制属性，负责线宽、颜色、线型、端点和连接样式。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPen>`
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

### 公有函数

- `QPen()`
- `QPen(Qt::PenStyle style)`
- `QPen(const QColor &color)`
- `QPen(const QBrush &brush, qreal width, Qt::PenStyle style = Qt::SolidLine, Qt::PenCapStyle cap = Qt::SquareCap, Qt::PenJoinStyle join = Qt::BevelJoin)`
- `QPen(const QPen &pen)`
- `QPen(QPen &&pen)`
- `~QPen()`
- `QBrush brush() const`
- `Qt::PenCapStyle capStyle() const`
- `QColor color() const`
- `qreal dashOffset() const`
- `QList<qreal> dashPattern() const`
- `bool isCosmetic() const`
- `bool isSolid() const`
- `Qt::PenJoinStyle joinStyle() const`
- `qreal miterLimit() const`
- `void setBrush(const QBrush &brush)`
- `void setCapStyle(Qt::PenCapStyle style)`
- `void setColor(const QColor &color)`
- `void setCosmetic(bool cosmetic)`
- `void setDashOffset(qreal offset)`
- `void setDashPattern(const QList<qreal> &pattern)`
- `void setJoinStyle(Qt::PenJoinStyle style)`
- `void setMiterLimit(qreal limit)`
- `void setStyle(Qt::PenStyle style)`
- `void setWidth(int width)`
- `void setWidthF(qreal width)`
- `Qt::PenStyle style() const`
- `void swap(QPen &other)`
- `int width() const`
- `qreal widthF() const`
- `operator QVariant() const`
- `bool operator!=(const QPen &pen) const`
- `QPen & operator=(QPen &&other)`
- `QPen & operator=(const QPen &pen)`
- `(since 6.9) QPen & operator=(QColor color)`
- `(since 6.9) QPen & operator=(Qt::PenStyle style)`
- `bool operator==(const QPen &pen) const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QPen &pen)`
- `QDataStream & operator>>(QDataStream &stream, QPen &pen)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPen::QPen()`

**作用与语义：**

构建一个默认的黑色实心线笔，宽度为1。

### `QPen::QPen(Qt::PenStyle style)`

**作用与语义：**

构造一支宽度为1、`style`为的黑色笔。

### `QPen::QPen(const QColor &color)`

**作用与语义：**

构建一个宽度为1、`color`为的实心线笔。

### `QPen::QPen(const QBrush &brush, qreal width, Qt::PenStyle style = Qt::SolidLine, Qt::PenCapStyle cap = Qt::SquareCap, Qt::PenJoinStyle join = Qt::BevelJoin)`

**作用与语义：**

构建具备指定`brush`、`width`、笔型`style`、`cap`样式和 `join` 样式的笔。

### `[noexcept] QPen::QPen(const QPen &pen)`

**作用与语义：**

构建一支复制给定`pen`的笔。

### `[constexpr noexcept] QPen::QPen(QPen &&pen)`

**作用与语义：**

构造一个从给定`pen`移动的笔。
移出笔只能被分配、复制或销毁。在分配之前的任何操作都会导致行为不明确。

### `[noexcept] QPen::~QPen()`

**作用与语义：**

毁了笔。

### `QBrush QPen::brush() const`

**作用与语义：**

返回用来填充这支笔生成笔画的画笔。

### `Qt::PenCapStyle QPen::capStyle() const`

**作用与语义：**

笔帽样式还原了。

### `QColor QPen::color() const`

**作用与语义：**

还原这支笔笔的颜色。

### `qreal QPen::dashOffset() const`

**作用与语义：**

还原了笔的破折号偏移。

### `QList<qreal> QPen::dashPattern() const`

**作用与语义：**

返回这支笔的破折号图案。

### `bool QPen::isCosmetic() const`

**作用与语义：**

如果笔是美观的，返回`true`;否则返回`false`。
美观钢笔用于绘制无论对所用的`QPainter`施加任何变换，笔廓宽度均为恒定。用美观笔绘制形状可以确保其轮廓在不同比例尺下厚度相同。
零宽度的笔默认是外观问题。

### `bool QPen::isSolid() const`

**作用与语义：**

如果笔有实心填充，则返回`true`，否则为假。

### `Qt::PenJoinStyle QPen::joinStyle() const`

**作用与语义：**

恢复笔的连接方式。

### `qreal QPen::miterLimit() const`

**作用与语义：**

返回笔的斜口限值。斜口限值仅在连接样式设置为`Qt::MiterJoin`时才相关。

### `void QPen::setBrush(const QBrush &brush)`

**作用与语义：**

将用来填充笔触的笔刷设置为给定的`brush`。

### `void QPen::setCapStyle(Qt::PenCapStyle style)`

**作用与语义：**

将笔的笔帽样式设置为给定的 `style`。默认值是 `Qt::SquareCap`。

### `void QPen::setColor(const QColor &color)`

**作用与语义：**

将这支笔笔的颜色设置为给定的`color`。

### `void QPen::setCosmetic(bool cosmetic)`

**作用与语义：**

根据`cosmetic`值，将笔设置为外观或非装饰。

### `void QPen::setDashOffset(qreal offset)`

**作用与语义：**

将该笔的破折号偏移量（破折号图案的起点）设置为指定的`offset`。偏移量以指定破折号图案的单位来衡量。
- “'：例如，画成线条时，每笔画长四个单位，后面有两个单位的间隙，画成线条时会以画笔开始。但如果划线偏移设置为4.0，任何画线都会以空隙开头。偏移值在4.0以内时，划线部分会先画;偏移值介于4.0到6.0之间时，线条会以部分空隙开始。
注意：这隐含地将笔的风格转变为`Qt::CustomDashLine`。

### `void QPen::setDashPattern(const QList<qreal> &pattern)`

**作用与语义：**

将该笔的破折号图案设置为给定的`pattern`。这隐含地将笔的样式转换为`Qt::CustomDashLine`。
该模式必须指定为偶数个正元素，其中1、3、5......是划号，2、4、6......是空格。例如：
- '`: `QPen' 笔;
`QList`<`qreal`>破折号;
`qreal`空间 = 4;
破折号<<1<<空格<<3<<空格<<9<<空格。
<<27个<<空间<<9个<<空间;
pen.setDashPattern（破折号）;
破折号图案以笔宽度为单位表示;例如，长度为5、宽度为10的破折号长度为50像素。注意，宽度为0的笔等同于宽度为1像素的装饰笔。
每个破折号也受大写样式影响，比如1的破折号设置为方形大写，会向每个方向延伸0.5像素，总宽度为2。
注意默认的顶端样式是`Qt::SquareCap`，意味着方形线端覆盖端点，并且延伸到线宽的一半。

### `void QPen::setJoinStyle(Qt::PenJoinStyle style)`

**作用与语义：**

将笔的连接样式设置为给定的`style`。默认值为`Qt::BevelJoin`。

### `void QPen::setMiterLimit(qreal limit)`

**作用与语义：**

将该笔的斜切极限设定为给定的`limit`。
斜口极限描述了斜口连接从连接点延伸的距离。这用于减少线连接间接近平行线条之间的伪影。
该数值仅在笔型设置为`Qt::MiterJoin`时生效。该数值以笔宽为单位表示，例如宽度为5的斜切限制10为50像素。默认斜切限制为2，即笔宽的两倍像素数。

### `void QPen::setStyle(Qt::PenStyle style)`

**作用与语义：**

将笔式设置为给定的 `style`。
请参阅 `Qt::PenStyle` 文档，查看可用样式列表。自 Qt 4.1 起，还可以使用 `setDashPattern()` 函数指定自定义破折号图案，该函数隐式将笔的样式转换为 `Qt::CustomDashLine`。
注意：该功能会将仪表盘偏移重置为零。

### `void QPen::setWidth(int width)`

**作用与语义：**

以整数精度将笔宽设置为像素`width`。
线宽为零表示为美观钢笔。这意味着笔宽始终绘制为一个像素宽，与画家的 `transformation` 设置无关。
不支持将笔宽设置为负值。

### `void QPen::setWidthF(qreal width)`

**作用与语义：**

以浮点精度将笔宽设置为像素`width`。
线宽为零表示是美观笔。这意味着笔宽总是画成一个像素宽，与画家的 `transformation` 无关。
不支持将笔宽设置为负值。

### `Qt::PenStyle QPen::style() const`

**作用与语义：**

还原了笔式。

### `[noexcept] void QPen::swap(QPen &other)`

**作用与语义：**

把这支笔和`other`互换。这个操作非常快，而且从未失败过。

### `int QPen::width() const`

**作用与语义：**

以整数精度返回笔宽。

### `qreal QPen::widthF() const`

**作用与语义：**

以浮点精度返回笔宽。

### `QPen::operator QVariant() const`

**作用与语义：**

把笔当作`QVariant`还回来。

### `bool QPen::operator!=(const QPen &pen) const`

**作用与语义：**

如果笔与给定`pen`不同，则返回`true`;否则为假。如果两支笔的样式、宽度或颜色不同，则它们是不同的。

### `[noexcept] QPen &QPen::operator=(QPen &&other)`

**作用与语义：**

Move-Assign `other`到这个`QPen`实例。

### `[noexcept] QPen &QPen::operator=(const QPen &pen)`

**作用与语义：**

将给定的`pen`分配给这支笔，并返回对该笔的引用。

### `[since 6.9] QPen &QPen::operator=(QColor color)`

**作用与语义：**

让这支笔变成一支实心笔，颜色相同，默认的顶部和连接样式，并返回对这支笔的引用。

### `[since 6.9] QPen &QPen::operator=(Qt::PenStyle style)`

**作用与语义：**

让这支笔变成一本实心黑色的笔，默认采用封顶和连接样式，并返回对这支笔的引用。

### `bool QPen::operator==(const QPen &pen) const`

**作用与语义：**

如果笔等于给定`pen`，则返回`true`;否则为假。如果两支笔的样式、宽度和颜色相等，则它们相等。

### `QDataStream &operator<<(QDataStream &stream, const QPen &pen)`

**作用与语义：**

将给定`pen`写入给定`stream`，并返回对`stream`的引用。

### `QDataStream &operator>>(QDataStream &stream, QPen &pen)`

**作用与语义：**

将给定`stream`中的笔读入给定`pen`，并返回对`stream`的引用。

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

`QPen` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
