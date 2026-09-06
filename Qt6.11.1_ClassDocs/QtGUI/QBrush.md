# QBrush

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 填充绘制属性，负责纯色、纹理或渐变填充。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QBrush`：填充绘制属性，负责纯色、纹理或渐变填充。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QBrush>`
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

- `QBrush()`
- `QBrush(Qt::BrushStyle style)`
- `QBrush(const QGradient &gradient)`
- `QBrush(const QImage &image)`
- `QBrush(const QPixmap &pixmap)`
- `QBrush(Qt::GlobalColor color, Qt::BrushStyle style = Qt::SolidPattern)`
- `QBrush(Qt::GlobalColor color, const QPixmap &pixmap)`
- `QBrush(const QColor &color, Qt::BrushStyle style = Qt::SolidPattern)`
- `QBrush(const QColor &color, const QPixmap &pixmap)`
- `QBrush(const QBrush &other)`
- `~QBrush()`
- `const QColor & color() const`
- `const QGradient * gradient() const`
- `bool isOpaque() const`
- `void setColor(const QColor &color)`
- `void setColor(Qt::GlobalColor color)`
- `void setStyle(Qt::BrushStyle style)`
- `void setTexture(const QPixmap &pixmap)`
- `void setTextureImage(const QImage &image)`
- `void setTransform(const QTransform &matrix)`
- `Qt::BrushStyle style() const`
- `void swap(QBrush &other)`
- `QPixmap texture() const`
- `QImage textureImage() const`
- `QTransform transform() const`
- `operator QVariant() const`
- `bool operator!=(const QBrush &brush) const`
- `QBrush & operator=(QBrush &&other)`
- `QBrush & operator=(const QBrush &brush)`
- `(since 6.9) QBrush & operator=(QColor color)`
- `(since 6.9) QBrush & operator=(Qt::BrushStyle style)`
- `(since 6.9) QBrush & operator=(Qt::GlobalColor color)`
- `bool operator==(const QBrush &brush) const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QBrush &brush)`
- `QDataStream & operator>>(QDataStream &stream, QBrush &brush)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QBrush::QBrush()`

**作用与语义：**

构建一个默认的黑色画笔，带有样式`Qt::NoBrush`（即该画笔不会填充形状）。

### `QBrush::QBrush(Qt::BrushStyle style)`

**作用与语义：**

用给定的`style`构造黑色画笔。

### `QBrush::QBrush(const QGradient &gradient)`

**作用与语义：**

根据给定的画笔`gradient`构建。
画笔样式设置为相应的渐变风格（`Qt::LinearGradientPattern`、`Qt::RadialGradientPattern`或`Qt::ConicalGradientPattern`）。

### `QBrush::QBrush(const QImage &image)`

**作用与语义：**

构建一个黑色画笔，纹理设置为指定`image`。样式设置为`Qt::TexturePattern`。

### `QBrush::QBrush(const QPixmap &pixmap)`

**作用与语义：**

构建一个黑色画笔，纹理设置为给定`pixmap`。样式设置为`Qt::TexturePattern`。

### `QBrush::QBrush(Qt::GlobalColor color, Qt::BrushStyle style = Qt::SolidPattern)`

**作用与语义：**

构造与给定`color`和`style`的画刷。

### `QBrush::QBrush(Qt::GlobalColor color, const QPixmap &pixmap)`

**作用与语义：**

用给定的`color`和存储在`pixmap`中的自定义图案构建画笔。
样式设置为`Qt::TexturePattern`。颜色只会对QBitmaps产生影响。

### `QBrush::QBrush(const QColor &color, Qt::BrushStyle style = Qt::SolidPattern)`

**作用与语义：**

构造与给定`color`和`style`的画刷。

### `QBrush::QBrush(const QColor &color, const QPixmap &pixmap)`

**作用与语义：**

用给定的`color`和存储在`pixmap`中的自定义图案构建画笔。
样式设置为`Qt::TexturePattern`。颜色只会对QBitmaps产生影响。

### `QBrush::QBrush(const QBrush &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QBrush::~QBrush()`

**作用与语义：**

毁掉画刷。

### `const QColor &QBrush::color() const`

**作用与语义：**

还原画笔颜色。

### `const QGradient *QBrush::gradient() const`

**作用与语义：**

返回描述该画笔的梯度。

### `bool QBrush::isOpaque() const`

**作用与语义：**

如果画笔完全不透明，返回`true`，否则为假。如果有以下条件，则认为画笔是不透明的：
- `color()`的α分量为255。
- 其`texture()`没有α通道，也不是`QBitmap`。
- `gradient()`中的颜色都有一个α分量为255。
- 它是扩展的径向梯度。

### `void QBrush::setColor(const QColor &color)`

**作用与语义：**

将画笔颜色设置为给定的`color`。
注意，如果样式是渐变，调用 setColor() 不会有影响。如果样式是 `Qt::TexturePattern`样式，情况也是如此，除非当前纹理是`QBitmap`。

### `void QBrush::setColor(Qt::GlobalColor color)`

**作用与语义：**

将画笔颜色设置为给定的`color`。

### `void QBrush::setStyle(Qt::BrushStyle style)`

**作用与语义：**

把画笔样式设置为`style`。

### `void QBrush::setTexture(const QPixmap &pixmap)`

**作用与语义：**

将画笔像素贴图设置为`pixmap`。样式设置为`Qt::TexturePattern`。
当前的画笔颜色仅对单色像素贴图有影响，即对`QPixmap::depth()` == 1 （`QBitmaps`）。

### `void QBrush::setTextureImage(const QImage &image)`

**作用与语义：**

将画笔图像设置为`image`。样式设置为`Qt::TexturePattern`。
注意当前画笔颜色对单色图像没有影响，不同于用`QBitmap`调用`setTexture()`。如果你想更改单色画笔的颜色，要么用`QBitmap::fromImage()`将图像转换为`QBitmap`，并将生成的 `QBitmap` 设置为纹理，要么更改该图像在颜色表中的条目。

### `void QBrush::setTransform(const QTransform &matrix)`

**作用与语义：**

将`matrix`设为当前画刷上的显式变换矩阵。画笔变换矩阵与`QPainter`变换矩阵合并以生成最终结果。

### `Qt::BrushStyle QBrush::style() const`

**作用与语义：**

还原了画笔风格。

### `[noexcept] void QBrush::swap(QBrush &other)`

**作用与语义：**

把画刷换成`other`。这个操作非常快，从不失败。

### `QPixmap QBrush::texture() const`

**作用与语义：**

返回自定义画笔图案，或者如果没有设置自定义画笔图，则返回空画图。

### `QImage QBrush::textureImage() const`

**作用与语义：**

返回自定义画笔图案，或者如果没有设置自定义画笔图，则返回空图。
如果纹理被设置为`QPixmap`，它会被转换成`QImage`。

### `QTransform QBrush::transform() const`

**作用与语义：**

返回画刷的电流变换矩阵。

### `QBrush::operator QVariant() const`

**作用与语义：**

把画刷当作`QVariant`。

### `bool QBrush::operator!=(const QBrush &brush) const`

**作用与语义：**

如果画笔与给定`brush`不同，返回`true`;否则返回 `false`。
如果两个画笔的样式、颜色、变换方式不同，或者根据风格的不同，像素贴图和渐变不同，那它们就是不同的。

### `[noexcept] QBrush &QBrush::operator=(QBrush &&other)`

**作用与语义：**

Move-assign `other`到该`QBrush`实例。

### `QBrush &QBrush::operator=(const QBrush &brush)`

**作用与语义：**

将给定的 `brush` 分配给该画刷，并返回对该画刷的引用。

### `[since 6.9] QBrush &QBrush::operator=(Qt::GlobalColor color)`

**作用与语义：**

使该画笔成为给定`color`的实心图案刷，并返回该画笔的参考。

### `[since 6.9] QBrush &QBrush::operator=(Qt::BrushStyle style)`

**作用与语义：**

使该画笔成为给定`color`的实心图案刷，并返回该画笔的参考。

### `bool QBrush::operator==(const QBrush &brush) const`

**作用与语义：**

如果画刷等于给定`brush`，则返回`true`;否则返回`false`。
如果两个画笔的样式、颜色、变换以及相等的像素贴图或渐变，则它们是相等的，这取决于样式。

### `QDataStream &operator<<(QDataStream &stream, const QBrush &brush)`

**作用与语义：**

将给定的`brush`写入给定的`stream`，并返回对`stream`的引用。

### `QDataStream &operator>>(QDataStream &stream, QBrush &brush)`

**作用与语义：**

从给定`stream`读取给定`brush`，并返回对`stream`的引用。

### `(since 6.9) QBrush & operator=(QColor color)`

**作用与语义：**

将该画笔设置为给定`style`的黑色画笔，并返回对该画笔的引用。

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

`QBrush` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
