<!-- 依据 Qt 6.11.1 头文件 qgraphicseffect.h 整理。 -->

# QGraphicsBlurEffect 深入笔记

> 头文件：`#include <QGraphicsBlurEffect>`  
> 模块：`Qt6::Widgets`  
> 继承：`QObject -> QGraphicsEffect -> QGraphicsBlurEffect`

## 1. 它解决什么问题

`QGraphicsBlurEffect` 用于把一个 `QWidget` 或 `QGraphicsItem` 的最终绘制结果做模糊处理。它适合“背景退焦”“内容不可操作时弱化”“弹窗出现时压低背景存在感”等视觉层级需求，而不是用来处理原始图片数据。

它处理的是目标的**整体输出**，所以文字、子控件、边框和自定义绘制都会一起被模糊：

```cpp
auto *blur = new QGraphicsBlurEffect;
blur->setBlurRadius(12.0);
backgroundPanel->setGraphicsEffect(blur);
```

如果只想模糊一张 `QImage`、保存模糊后的文件，或者对视频帧做离线处理，应使用图像处理算法，而不是 GUI 绘制效果。`QGraphicsBlurEffect` 的输出依赖屏幕绘制和事件循环，它不是通用图像滤镜 API。

## 2. 它如何挂到目标上

```cpp
#include <QGraphicsBlurEffect>
#include <QWidget>

auto *blur = new QGraphicsBlurEffect;
blur->setBlurRadius(10.0);
blur->setBlurHints(QGraphicsBlurEffect::PerformanceHint);

contentWidget->setGraphicsEffect(blur);
```

`setGraphicsEffect()` 会接管 `blur` 的所有权。一个控件或图元同时只能安装一个 `QGraphicsEffect`，因此再装阴影、透明度或自定义效果会替换当前模糊效果，而不是把它们自动叠加。

要同时实现“模糊 + 透明度”之类的复合效果，通常有三种选择：

1. 编写一个自定义 `QGraphicsEffect`，在一次 `draw()` 中完成多步处理。
2. 调整界面层级，把不同效果装到不同的父子对象上。
3. 根据交互阶段切换效果，而不是永久叠加。

## 3. `blurRadius`：模糊范围，而不是透明度

`blurRadius` 表示模糊半径，数值越大，单个像素会受越大范围的邻近像素影响，边缘越柔和、细节越少。默认半径为 `5`。

```cpp
blur->setBlurRadius(0.0);   // 基本不产生模糊
blur->setBlurRadius(8.0);   // 轻度退焦
blur->setBlurRadius(24.0);  // 明显模糊
```

半径使用设备坐标。不要把它当成与控件逻辑宽高完全同一套单位：高 DPI、缩放和视图变换都会影响最终像素成本与视觉密度。

半径变大还会使有效绘制区域扩到源对象边界外。`QGraphicsBlurEffect::boundingRectFor()` 已经处理这一点，因此正常使用不必手工算裁剪区域；自定义效果才需要自己解决类似问题。

性能上，半径和目标面积相乘才是关键。给 `80 x 30` 的标签做 `20` 半径模糊，和给全屏页面做同样半径，成本完全不是一个量级。弹窗背景效果应优先模糊小范围容器，避免每次滚动或动画都处理大面积内容。

## 4. `BlurHint` 不是“开关”，而是策略提示

`blurHints` 是 `BlurHints` 标志集合，告诉 Qt 应更偏向哪种策略：

| 取值 | 用途 | 适合场景 |
| --- | --- | --- |
| `PerformanceHint` | 优先减少处理开销。 | 静态或轻量模糊；这是默认选择。 |
| `QualityHint` | 更偏向视觉质量。 | 大尺寸图片、细节需要更平滑的静态画面。 |
| `AnimationHint` | 为半径持续变化的动画做优化，可能用额外内存缓存不同半径的结果。 | 源内容基本稳定的弹窗进出、焦点切换、悬停退焦动画。 |

提示不等于强制保证，部分绘制后端也可能不采用它。实际收益取决于平台、后端、目标大小和变化频率。`AnimationHint` 的核心交易是“占更多内存，减少动画过程反复计算的压力”；源内容本身频繁变化时不应使用它，也不应该给每个静态模糊对象都打开。

设置多个提示时使用按位或：

```cpp
blur->setBlurHints(
    QGraphicsBlurEffect::QualityHint
    | QGraphicsBlurEffect::AnimationHint);
```

先在实际目标尺寸和目标设备上测量，再决定是否需要质量或动画提示。肉眼上不明显的质量升级，往往不值得让列表滚动和窗口缩放变慢。

## 5. 模糊动画的正确方式

`blurRadius` 是 Qt 属性，可直接交给 `QPropertyAnimation`：

```cpp
auto *animation = new QPropertyAnimation(blur, "blurRadius", blur);
animation->setStartValue(0.0);
animation->setEndValue(16.0);
animation->setDuration(180);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

动画期间每个半径变化都意味着新的视觉输出。为了避免把昂贵工作放在高频交互上：

- 给动画设定短而稳定的时长，避免同时叠加多个大面积模糊动画。
- 动画结束后不再频繁改半径。
- 对快速滚动、拖动过程可暂时 `setEnabled(false)`，结束后再恢复。
- 只在确实连续改变半径时考虑 `AnimationHint`。

`blurRadiusChanged(qreal)` 和 `blurHintsChanged(BlurHints)` 可用于同步属性面板或诊断状态，但不应用信号里再立即改回同一属性，否则容易产生无意义的更新循环。

## 6. 与其它效果如何分工

| 需求 | 更合适的类 |
| --- | --- |
| 目标整体模糊 | `QGraphicsBlurEffect` |
| 给目标投射偏移阴影 | `QGraphicsDropShadowEffect` |
| 调低整体可见度或使用遮罩 | `QGraphicsOpacityEffect` |
| 统一染色 | `QGraphicsColorizeEffect` |
| 同时做多个像素级效果 | 自定义 `QGraphicsEffect` 或拆分到不同对象层级 |

一个目标不能直接叠加多个 `QGraphicsEffect`。这是使用此类时最容易被忽略的边界。

## 7. API 逐项说明

### 构造、属性与槽

- `QGraphicsBlurEffect(QObject *parent = nullptr)`：创建模糊效果。安装给控件/图元后由目标接管。
- `blurRadius()` / `setBlurRadius(qreal)`：读取或设置模糊半径。
- `blurHints()` / `setBlurHints(BlurHints)`：读取或设置质量、性能、动画策略提示。

### 框架调用和通知

- `boundingRectFor(const QRectF &rect) const`：计算包含扩散模糊边缘的有效边界；框架在布局绘制判断时调用。
- `draw(QPainter *)`：实际进行模糊输出的受保护实现。现成类已实现，业务代码不调用也不重写。
- `blurRadiusChanged(qreal)`、`blurHintsChanged(BlurHints)`：属性变化通知。

从 `QGraphicsEffect` 继承的 `setEnabled()`、`update()` 和 `enabledChanged()` 仍然可用；它们的用途见 [QGraphicsEffect_类概览.md](QGraphicsEffect_类概览.md)。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsBlurEffect(QObject *parent = nullptr)` | 创建一个可安装到控件或图元的模糊效果。 | 安装后由目标接管；一个目标只能有一个效果。 |
| 析构 | `~QGraphicsBlurEffect()` | 销毁模糊效果。 | 已安装时通常不手动删除。 |
| 属性 | `blurRadius : qreal` | 保存模糊半径。 | 默认 `5`；半径和目标面积都会影响性能。 |
| 读取 | `qreal blurRadius() const` | 读取当前模糊半径。 | 用于检查动画或设置是否生效。 |
| 设置/槽 | `void setBlurRadius(qreal blurRadius)` | 设置模糊半径。 | 会触发重绘，并扩大或缩小有效绘制边界。 |
| 属性 | `blurHints : BlurHints` | 保存模糊算法的策略提示。 | 是标志组合，不是互斥枚举。 |
| 读取 | `BlurHints blurHints() const` | 读取当前策略提示。 | 用按位与检查是否包含某个提示。 |
| 设置/槽 | `void setBlurHints(BlurHints hints)` | 设置性能、质量或动画提示。 | `AnimationHint` 可能用更多内存换取动画表现。 |
| 枚举 | `PerformanceHint` | 请求偏向性能的模糊策略。 | 默认选择，适合普通静态效果。 |
| 枚举 | `QualityHint` | 请求偏向画质的模糊策略。 | 先在目标设备上确认成本是否可接受。 |
| 枚举 | `AnimationHint` | 请求为持续半径变化优化。 | 仅在确有模糊动画且源内容基本不变时使用。 |
| 框架接口 | `QRectF boundingRectFor(const QRectF &rect) const` | 返回包含模糊扩散边缘的矩形。 | 框架调用，业务代码通常不直接调用。 |
| 信号 | `void blurRadiusChanged(qreal radius)` | 通知模糊半径已改变。 | 动画时会高频发射，槽函数应轻量。 |
| 信号 | `void blurHintsChanged(BlurHints hints)` | 通知策略提示已改变。 | 用于同步设置界面或日志。 |
| 受保护函数 | `void draw(QPainter *painter)` | 执行实际模糊绘制。 | 现成类已实现；不要把它当普通调用 API。 |

## 9. 排查清单

1. 设置了效果却没有变化：确认效果安装在正确目标上，且没有被后续 `setGraphicsEffect()` 替换。
2. 模糊太重或界面变慢：先减小半径和作用面积，再判断是否真的需要 `QualityHint`。
3. 动画卡顿：减少同时动画的目标，尝试 `AnimationHint`，并避免模糊整个大窗口。
4. 想叠加阴影却失效：同一个目标只能有一个效果，应拆分对象层级或写自定义效果。

### 一句话总结

`QGraphicsBlurEffect` 是界面绘制阶段的整体退焦工具；半径决定视觉和成本，`BlurHint` 决定取舍，而“一个目标只能安装一个效果”决定了复杂效果要如何组织。
