# QGraphicsOpacityEffect

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsOpacityEffect` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsOpacityEffect` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsOpacityEffect>`
- 继承自：QGraphicsEffect
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `opacity : qreal`
- `opacityMask : QBrush`

### 公有函数

- `QGraphicsOpacityEffect(QObject *parent = nullptr)`
- `virtual ~QGraphicsOpacityEffect()`
- `qreal opacity() const`
- `QBrush opacityMask() const`

### 公有槽函数

- `void setOpacity(qreal opacity)`
- `void setOpacityMask(const QBrush &mask)`

### 信号

- `void opacityChanged(qreal opacity)`
- `void opacityMaskChanged(const QBrush &mask)`

### 重实现的保护函数

- `virtual void draw(QPainter *painter) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `opacity : qreal`

**作用与语义：**

该属性表示了效应的不透明度。
值应在0.0到1.0之间，0.0表示完全透明，1.0表示完全不透明。
默认情况下，不透明度为0.7。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `opacityMask : QBrush`

**作用与语义：**

该属性表示了该效应的不透明度掩膜。
不透明度遮罩允许你对元素的某些部分施加不透明度。
默认情况下没有不透明度遮罩。

**如何使用：** 调用 `opacityMask()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 ...
 QLinearGradient alphaGradient(rect.topLeft(), rect.bottomLeft());
 alphaGradient.setColorAt(0.0, Qt::transparent);
 alphaGradient.setColorAt(0.5, Qt::black);
 alphaGradient.setColorAt(1.0, Qt::transparent);
 QGraphicsOpacityEffect *effect = new QGraphicsOpacityEffect;
 effect->setOpacityMask(alphaGradient);
 ...
```

### `QGraphicsOpacityEffect::QGraphicsOpacityEffect(QObject *parent = nullptr)`

**作用与语义：**

构造一个新的 QGraphicsOpacityEffect 实例。`parent`参数传递给 `QGraphicsEffect` 的构造器。

### `[virtual noexcept] QGraphicsOpacityEffect::~QGraphicsOpacityEffect()`

**作用与语义：**

破坏效果。

### `[override virtual protected] void QGraphicsOpacityEffect::draw(QPainter *painter)`

**作用与语义：**

重实现自：`QGraphicsEffect::draw`（QPainter *画师）。
这个纯虚拟函数绘制该效应，并在需要绘制源时调用。
在`QGraphicsEffect`子类中重新实现该函数，以提供该效果的绘制实现，使用`painter`。
用户不应明确调用该函数，因为它仅用于重实现。

### `[signal] void QGraphicsOpacityEffect::opacityChanged(qreal opacity)`

**作用与语义：**

该属性表示了效应的不透明度。
值应在0.0到1.0之间，0.0表示完全透明，1.0表示完全不透明。
默认情况下，不透明度为0.7。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `opacity` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsOpacityEffect::opacityMaskChanged(const QBrush &mask)`

**作用与语义：**

该属性表示了该效应的不透明度掩膜。
不透明度遮罩允许你对元素的某些部分施加不透明度。
默认情况下没有不透明度遮罩。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `opacityMask` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 ...
 QLinearGradient alphaGradient(rect.topLeft(), rect.bottomLeft());
 alphaGradient.setColorAt(0.0, Qt::transparent);
 alphaGradient.setColorAt(0.5, Qt::black);
 alphaGradient.setColorAt(1.0, Qt::transparent);
 QGraphicsOpacityEffect *effect = new QGraphicsOpacityEffect;
 effect->setOpacityMask(alphaGradient);
 ...
```

### `qreal opacity() const`

**作用与语义：**

该属性表示了效应的不透明度。
值应在0.0到1.0之间，0.0表示完全透明，1.0表示完全不透明。
默认情况下，不透明度为0.7。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `QBrush opacityMask() const`

**作用与语义：**

该属性表示了该效应的不透明度掩膜。
不透明度遮罩允许你对元素的某些部分施加不透明度。
默认情况下没有不透明度遮罩。

**如何使用：** 调用 `opacityMask()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 ...
 QLinearGradient alphaGradient(rect.topLeft(), rect.bottomLeft());
 alphaGradient.setColorAt(0.0, Qt::transparent);
 alphaGradient.setColorAt(0.5, Qt::black);
 alphaGradient.setColorAt(1.0, Qt::transparent);
 QGraphicsOpacityEffect *effect = new QGraphicsOpacityEffect;
 effect->setOpacityMask(alphaGradient);
 ...
```

### `void setOpacity(qreal opacity)`

**作用与语义：**

该属性表示了效应的不透明度。
值应在0.0到1.0之间，0.0表示完全透明，1.0表示完全不透明。
默认情况下，不透明度为0.7。

**如何使用：** 调用 `setOpacity(...)` 修改 `opacity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpacityMask(const QBrush &mask)`

**作用与语义：**

该属性表示了该效应的不透明度掩膜。
不透明度遮罩允许你对元素的某些部分施加不透明度。
默认情况下没有不透明度遮罩。

**如何使用：** 调用 `setOpacityMask(...)` 修改 `opacityMask`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 ...
 QLinearGradient alphaGradient(rect.topLeft(), rect.bottomLeft());
 alphaGradient.setColorAt(0.0, Qt::transparent);
 alphaGradient.setColorAt(0.5, Qt::black);
 alphaGradient.setColorAt(1.0, Qt::transparent);
 QGraphicsOpacityEffect *effect = new QGraphicsOpacityEffect;
 effect->setOpacityMask(alphaGradient);
 ...
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsOpacityEffect` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
