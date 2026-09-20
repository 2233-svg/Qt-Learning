# QPropertyAnimation：把时间变化写入 QObject 属性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPropertyAnimation>`  
> 模块：`Qt6::Core`  
> 继承：`QVariantAnimation`  
> 动画框架配置：需要 `QT_CONFIG(animation)`

## 它解决什么问题

`QPropertyAnimation` 将一个 `QObject` 的 Qt 属性从起点逐帧过渡到终点。它不负责绘制，也不认识“按钮移动”或“面板淡出”这些业务概念；它做的事情是：

1. 根据动画时间计算一个 `QVariant` 当前值；
2. 通过元对象系统把这个值写入目标对象的指定属性；
3. 由目标对象的 setter、属性通知和界面系统产生实际效果。

这使它可以复用在很多对象上：

- `QWidget::pos`、`geometry`、`windowOpacity` 等界面属性；
- 自定义对象的进度、半径、角度、颜色或数值属性；
- 配合 `QParallelAnimationGroup` / `QSequentialAnimationGroup` 编排多对象状态变化；
- 在状态切换、展开收起、拖拽回弹和页面转场中表达时间过程。

动画对象本身是 `QObject`，不可拷贝；它需要事件循环驱动，通常与目标对象属于同一线程。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 最小可用例子

```cpp
#include <QPropertyAnimation>
#include <QPushButton>

auto *button = new QPushButton("Move");
auto *animation = new QPropertyAnimation(button, "pos", button);

animation->setDuration(250);             // 默认也是 250 ms
animation->setStartValue(QPoint(0, 0));
animation->setEndValue(QPoint(200, 80));
animation->start();
```

这里把动画对象的父对象设为 `button`，只是让按钮销毁时自动销毁动画；它不改变动画所控制的目标属性，也不表示动画会拥有一个独立的目标生命周期。

## 属性必须满足什么条件

目标属性必须属于一个 `QObject`，并且提供可写 setter，动画才有地方写入每一帧的值：

```cpp
class Meter : public QObject
{
    Q_OBJECT
    Q_PROPERTY(qreal level READ level WRITE setLevel NOTIFY levelChanged)

public:
    qreal level() const { return m_level; }

public slots:
    void setLevel(qreal level)
    {
        if (qFuzzyCompare(m_level, level))
            return;
        m_level = level;
        emit levelChanged();
    }

signals:
    void levelChanged();

private:
    qreal m_level = 0.0;
};
```

```cpp
auto *animation = new QPropertyAnimation(&meter, "level", &meter);
animation->setStartValue(0.0);
animation->setEndValue(1.0);
animation->setDuration(500);
animation->start();
```

只读属性没有可调用的写入路径，不能作为动画目标。属性名是 `QByteArray`，必须与元对象系统中的属性名一致，例如 `"pos"`，而不是 C++ setter 名 `"setPos"`。

属性值还必须是 `QVariantAnimation` 支持插值的类型，或由项目提供相应的可插值能力。`QPoint`、`QPointF`、基本数值等是常见选择；任意自定义类型不能因为能放入 `QVariant` 就自动获得有意义的中间值。

## 起点、终点和采样时机

常用配置是 `setStartValue()` 与 `setEndValue()`。如果没有设置起点，Qt 会在动画从 `Stopped` 进入 `Running` 时读取目标属性当前值作为起点，而不是简单地使用构造动画对象那一刻的值。

```cpp
animation->setEndValue(QPoint(400, 100));

// start() 之前用户可能已经移动了窗口；
// 未设置 startValue 时，动画会从 start() 时的当前位置开始。
animation->start();
```

这适合“从当前状态过渡到目标状态”。如果需要可重复、确定的演示动画，显式设置起点；如果需要从当前状态反向播放，先读取当前属性再配置对应起点和终点。

只设置终点时，重启动画会重新采样当前属性作为起点。动画运行中更换 `targetObject`、`propertyName`、起点或终点，可能使当前过渡产生跳变；复杂交互通常先 `stop()`，重新配置，再 `start()`。

## 生命周期和所有权

`QPropertyAnimation` 的父对象由构造函数的 `parent` 参数决定。也可以使用 `start(QAbstractAnimation::DeleteWhenStopped)` 让动画停止后由动画框架删除：

```cpp
auto *animation = new QPropertyAnimation(button, "geometry", button);
animation->setStartValue(button->geometry());
animation->setEndValue(QRect(20, 20, 240, 50));
animation->setDuration(180);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

二选一地设计所有权即可。不要让一个已经由 QObject 父对象管理的动画再以不清晰的方式交给多个外部所有者；也不要在动画仍运行时手动 `delete`，除非明确了解动画框架和对象线程的生命周期。

目标对象不是由 `QPropertyAnimation` 自动拥有的。动画销毁不会销毁目标，目标销毁也不应被当作动画的“正常完成”信号。目标的生命周期由其父对象或业务代码负责；目标可能销毁时，应停止动画或让它与目标共享明确的生命周期管理。

## 运行线程和事件循环

动画由 Qt 的动画计时器推进。启动动画的线程需要有可用的事件循环，GUI 动画通常在 GUI 线程运行。不要在工作线程里直接动画 QWidget；也不要从其他线程直接修改动画或目标对象。

目标对象、动画对象和属性 setter 的线程亲和性应保持一致。需要后台计算时，把计算结果通过 queued signal/slot 发送到目标线程，再在那里配置或启动动画。

同步等待、在 GUI 线程里长时间阻塞或频繁调用 `processEvents()` 都会破坏动画平滑性。动画是异步状态机，应使用 `finished()`、`stateChanged()` 等信号观察过程。

## 真实场景：可中断的展开/收起

```cpp
void Panel::setExpanded(bool expanded)
{
    if (!m_animation) {
        m_animation = new QPropertyAnimation(this, "maximumHeight", this);
        m_animation->setDuration(180);
        m_animation->setEasingCurve(QEasingCurve::OutCubic);
    }

    m_animation->stop();
    m_animation->setStartValue(maximumHeight());
    m_animation->setEndValue(expanded ? 240 : 0);
    m_animation->start();
}
```

先停止、从当前值重新设置起点，是可中断动画常用的写法。否则用户在过渡中再次点击时，旧动画的时间位置和新目标状态可能叠加出跳变。

## 属性绑定与 bindable API

`propertyName` 和 `targetObject` 都声明为支持 `QProperty` binding：

- `propertyName()` / `targetObject()` 读取当前配置；
- `setPropertyName()` / `setTargetObject()` 修改配置；
- `bindablePropertyName()` / `bindableTargetObject()` 返回 `QBindable`，用于接入 Qt Property Binding 系统。

绑定适合“动画目标由响应式状态决定”的场景，但要注意：动画运行过程中改变绑定产生的目标或属性名，本质上是在改变动画写入的位置。应设计清楚由谁拥有最终写入权，避免 binding 与动画每帧写值互相争夺。

## protected 重写点

普通使用者不需要调用 `event()`、`updateCurrentValue()` 或 `updateState()`。它们是 `QVariantAnimation` 驱动 `QPropertyAnimation` 的扩展点：

- `updateCurrentValue(value)`：当前插值值变化时，将值写入目标属性；动画停止时不再更新目标；
- `updateState(newState, oldState)`：状态变化时处理动画行为；若没有显式起点，从 `Stopped` 到 `Running` 的切换会在这里确定当前属性值；
- `event(event)`：重写基类的事件处理，用于框架内部事件分发。

若要实现自定义值如何写入，优先考虑自定义 `QVariantAnimation` 或属性 setter，而不是在业务代码中直接调用这些 protected 函数。

## 常见错误

### 属性名写错或属性没有 setter

`"setPos"`、`"position"` 和 `"pos"` 不是同一个属性名。使用 `QMetaObject::indexOfProperty()` 或 `QObject::metaObject()` 在调试阶段验证属性是否存在、是否可写。

### QVariant 能保存类型就以为能插值

可存储不代表可插值。自定义类型需要明确动画的中间值语义；否则动画可能无法按预期更新。

### 忘记设置起点导致每次重启行为变化

未设置 `startValue` 时起点是运行开始时的当前属性值。对于用户可打断的动画这是优点，对于需要严格复现的动画则应显式设置起点。

### 动画被局部变量销毁

```cpp
// 错误：函数返回后动画对象被销毁，动画不会继续运行。
void Panel::animate()
{
    QPropertyAnimation animation(this, "windowOpacity");
    animation.start();
}
```

把动画作为成员、设置合适的 QObject 父对象，或使用堆对象加 `DeleteWhenStopped`。

### 动画与手写赋值同时争夺同一属性

动画运行期间手动调用同一属性 setter，下一帧可能又被动画值覆盖。停止动画后再修改，或明确规定手动修改只是新的动画起点。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QPropertyAnimation(QObject *parent = nullptr)` | 构造空动画 | 只设置父对象；之后再设置目标和属性。默认时长 250 ms 来自带目标构造的语义/动画默认值。 |
| `QPropertyAnimation(QObject *target, const QByteArray &propertyName, QObject *parent = nullptr)` | 直接绑定目标属性 | 目标必须是 `QObject`；属性名必须是可写、可插值的 Qt 属性。 |
| `~QPropertyAnimation()` | 销毁动画对象 | 不拥有目标对象；销毁运行中动画会停止其更新。 |
| `targetObject() const` | 读取目标对象 | 返回非拥有指针；目标生命周期由其他代码管理。 |
| `setTargetObject(QObject *target)` | 设置/替换目标 | 运行中替换可能造成跳变；通常先停止再更换。 |
| `bindableTargetObject()` | 获取目标对象绑定接口 | 返回 `QBindable<QObject *>`；绑定变化会改变动画写入目标。 |
| `propertyName() const` | 读取目标属性名 | 返回 `QByteArray`，是元对象属性名，不是 setter 名。 |
| `setPropertyName(const QByteArray &propertyName)` | 设置/替换属性名 | 必须对应目标的可写属性；运行中改变需谨慎。 |
| `bindablePropertyName()` | 获取属性名绑定接口 | 返回 `QBindable<QByteArray>`；适合 Property Binding 场景。 |
| `event(QEvent *)` | 处理动画事件 | protected，重写基类；普通调用者不直接使用。 |
| `updateCurrentValue(const QVariant &value)` | 把当前插值值写入属性 | protected；由基类在值变化时调用，动画停止后不再更新目标。 |
| `updateState(newState, oldState)` | 响应动画状态切换 | protected；未设置起点时从 Stopped 到 Running 会采样目标当前值。 |
| 继承的 `setDuration()` | 设置时长 | 毫秒；时长越短越快，不改变属性类型要求。 |
| 继承的 `setStartValue()` / `setEndValue()` | 设置端点 | 必须是目标属性可接受且可插值的 `QVariant` 类型。 |
| 继承的 `setEasingCurve()` | 设置缓动曲线 | 改变时间到进度的映射，不改变属性值插值类型。 |
| 继承的 `start()` / `stop()` | 启停动画 | 依赖事件循环；可用 `DeleteWhenStopped` 管理临时动画。 |
| 继承的 `finished()` / `stateChanged()` | 观察生命周期 | 用信号协调后续动作，不要在 GUI 线程同步阻塞等待。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 将时间变化写入 QObject 属性 | `QPropertyAnimation` |
| 只计算 QVariant 值，自己决定如何应用 | `QVariantAnimation` |
| 多个动画并行或串行 | `QParallelAnimationGroup` / `QSequentialAnimationGroup` |
| 复杂状态切换或可逆转场 | 状态机配合动画组 |
| 非 QObject、无 setter 的数据 | 先设计可写 Qt 属性，或使用 `QVariantAnimation` 自己消费值 |

一句话记忆：`QPropertyAnimation` 每帧通过可写 Qt 属性驱动目标对象；目标、属性名、可插值类型和对象生命周期，四者缺一不可。
