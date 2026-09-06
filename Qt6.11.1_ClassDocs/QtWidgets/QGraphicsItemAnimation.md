# QGraphicsItemAnimation

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsItemAnimation` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsItemAnimation` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsItemAnimation>`
- 继承自：QObject
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

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGraphicsItemAnimation(QObject *parent = nullptr)`
- `virtual ~QGraphicsItemAnimation()`
- `void clear()`
- `qreal horizontalScaleAt(qreal step) const`
- `qreal horizontalShearAt(qreal step) const`
- `QGraphicsItem * item() const`
- `QPointF posAt(qreal step) const`
- `QList<std::pair<qreal, QPointF>> posList() const`
- `qreal rotationAt(qreal step) const`
- `QList<std::pair<qreal, qreal>> rotationList() const`
- `QList<std::pair<qreal, QPointF>> scaleList() const`
- `void setItem(QGraphicsItem *item)`
- `void setPosAt(qreal step, const QPointF &point)`
- `void setRotationAt(qreal step, qreal angle)`
- `void setScaleAt(qreal step, qreal sx, qreal sy)`
- `void setShearAt(qreal step, qreal sh, qreal sv)`
- `void setTimeLine(QTimeLine *timeLine)`
- `void setTranslationAt(qreal step, qreal dx, qreal dy)`
- `QList<std::pair<qreal, QPointF>> shearList() const`
- `QTimeLine * timeLine() const`
- `QTransform transformAt(qreal step) const`
- `QList<std::pair<qreal, QPointF>> translationList() const`
- `qreal verticalScaleAt(qreal step) const`
- `qreal verticalShearAt(qreal step) const`
- `qreal xTranslationAt(qreal step) const`
- `qreal yTranslationAt(qreal step) const`

### 公有槽函数

- `void setStep(qreal step)`

### 保护函数

- `virtual void afterAnimationStep(qreal step)`
- `virtual void beforeAnimationStep(qreal step)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGraphicsItemAnimation::QGraphicsItemAnimation(QObject *parent = nullptr)`

**作用与语义：**

构造一个具有给定`parent`的动画对象。

### `[virtual noexcept] QGraphicsItemAnimation::~QGraphicsItemAnimation()`

**作用与语义：**

会破坏动画对象。

### `[virtual protected] void QGraphicsItemAnimation::afterAnimationStep(qreal step)`

**作用与语义：**

该方法旨在覆盖需要在新步骤后执行额外代码的子类中。动画`step`用于动作依赖于其值的情况。

### `[virtual protected] void QGraphicsItemAnimation::beforeAnimationStep(qreal step)`

**作用与语义：**

该方法旨在被需要执行额外代码的子类覆盖，然后才会进行新步骤。动画`step`提供用于动作依赖于其值的情况。

### `void QGraphicsItemAnimation::clear()`

**作用与语义：**

清除动画中计划的变形，但保留物品和时间线。

### `qreal QGraphicsItemAnimation::horizontalScaleAt(qreal step) const`

**作用与语义：**

返回指定`step`值下的水平刻度。

### `qreal QGraphicsItemAnimation::horizontalShearAt(qreal step) const`

**作用与语义：**

返回指定`step`值的水平剪切值。

### `QGraphicsItem *QGraphicsItemAnimation::item() const`

**作用与语义：**

返回动画对象所操作的项目。

### `QPointF QGraphicsItemAnimation::posAt(qreal step) const`

**作用与语义：**

返回该项在给定`step`值处的位置。

### `QList<std::pair<qreal, QPointF>> QGraphicsItemAnimation::posList() const`

**作用与语义：**

返回所有明确插入的位置。

### `qreal QGraphicsItemAnimation::rotationAt(qreal step) const`

**作用与语义：**

返回物品在指定`step`值下旋转的角度。

### `QList<std::pair<qreal, qreal>> QGraphicsItemAnimation::rotationList() const`

**作用与语义：**

返回所有显式插入的旋转。

### `QList<std::pair<qreal, QPointF>> QGraphicsItemAnimation::scaleList() const`

**作用与语义：**

返回所有明确插入的音阶。

### `void QGraphicsItemAnimation::setItem(QGraphicsItem *item)`

**作用与语义：**

设置指定`item`用于动画。

### `void QGraphicsItemAnimation::setPosAt(qreal step, const QPointF &point)`

**作用与语义：**

将该物品在给定`step`值下的位置设置为指定的`point`。

### `void QGraphicsItemAnimation::setRotationAt(qreal step, qreal angle)`

**作用与语义：**

将物品在给定`step`值上的旋转设置为指定的`angle`。

### `void QGraphicsItemAnimation::setScaleAt(qreal step, qreal sx, qreal sy)`

**作用与语义：**

利用`sx`和`sy`指定的水平和垂直比例因子，将物品的比例设定在给定的`step`值。

### `void QGraphicsItemAnimation::setShearAt(qreal step, qreal sh, qreal sv)`

**作用与语义：**

利用`sh`和`sv`指定的水平和垂直剪切因子，将物体的剪切值设定在给定的`step`值。

### `[slot] void QGraphicsItemAnimation::setStep(qreal step)`

**作用与语义：**

设置当前动画的`step`值，从而执行该步骤安排的变换。

### `void QGraphicsItemAnimation::setTimeLine(QTimeLine *timeLine)`

**作用与语义：**

将用于控制动画速度的时间线对象设置为指定的`timeLine`。

### `void QGraphicsItemAnimation::setTranslationAt(qreal step, qreal dx, qreal dy)`

**作用与语义：**

利用`dx`和`dy`指定的水平和垂直坐标，将项目在给定的`step`值处设置平移。

### `QList<std::pair<qreal, QPointF>> QGraphicsItemAnimation::shearList() const`

**作用与语义：**

返回所有明确插入的剪刀。

### `QTimeLine *QGraphicsItemAnimation::timeLine() const`

**作用与语义：**

返回用于控制动画发生速率的时间线对象。

### `QTransform QGraphicsItemAnimation::transformAt(qreal step) const`

**作用与语义：**

返回指定`step`值下用于该项的变换。

### `QList<std::pair<qreal, QPointF>> QGraphicsItemAnimation::translationList() const`

**作用与语义：**

返回所有明确插入的翻译。

### `qreal QGraphicsItemAnimation::verticalScaleAt(qreal step) const`

**作用与语义：**

返回该物品在指定`step`值下的垂直刻度。

### `qreal QGraphicsItemAnimation::verticalShearAt(qreal step) const`

**作用与语义：**

返回该物品在指定`step`值处的垂直剪切值。

### `qreal QGraphicsItemAnimation::xTranslationAt(qreal step) const`

**作用与语义：**

返回指定`step`值下的水平平移。

### `qreal QGraphicsItemAnimation::yTranslationAt(qreal step) const`

**作用与语义：**

返回指定`step`值处的垂直平移。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsItemAnimation` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
