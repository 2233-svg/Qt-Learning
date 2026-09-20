<!-- 依据 Qt 6.11.1 头文件 qgraphicseffect.h 整理。 -->

# QGraphicsEffect 深入笔记

> 头文件：`#include <QGraphicsEffect>`  
> 模块：`Qt6::Widgets`  
> 继承：`QObject -> QGraphicsEffect`  
> 性质：抽象基类，不能直接创建

## 1. 它解决什么问题

`QGraphicsEffect` 把“先把目标内容画出来，再对结果做视觉处理”封装成一个统一机制。模糊、阴影、半透明、着色等效果不必修改目标控件或图元自己的 `paint()`，而是由效果对象在绘制管线中接管一次输出。

它能附着在两类目标上：

- `QWidget`：调用 `widget->setGraphicsEffect(effect)`，例如给一个面板、按钮或标签做阴影。
- `QGraphicsItem`：调用 `item->setGraphicsEffect(effect)`，例如给场景中的卡片、路径或图片做模糊。

`QGraphicsEffect` 自己是抽象类。日常项目直接选现成派生类：

```text
QGraphicsEffect
  ├─ QGraphicsBlurEffect        // 模糊
  ├─ QGraphicsDropShadowEffect  // 阴影
  ├─ QGraphicsOpacityEffect     // 透明度与遮罩
  └─ QGraphicsColorizeEffect    // 着色
```

只有当现成效果无法表达需求，例如灰阶、边缘描边、发光、像素化时，才从它派生并实现自己的 `draw()`。

## 2. 先理解绘制链，而不是先写 `draw()`

当目标安装了效果，绘制流程可粗略理解为：

```text
QWidget / QGraphicsItem 要绘制
        ↓
QGraphicsEffect::draw(painter)
        ↓
取得源内容：drawSource() 或 sourcePixmap()
        ↓
绘制原内容、处理后的内容，或两者叠加
```

效果对象并不替换目标对象，目标仍负责自己的内容、大小和事件；效果只介入“如何输出像素”。因此点击、焦点、布局这些行为仍属于原控件或图元，只是可见边界可能因阴影、模糊而扩大。

一个效果同一时间只能服务一个目标。`QWidget::setGraphicsEffect()` 和 `QGraphicsItem::setGraphicsEffect()` 都会接管传入效果的所有权；目标析构、替换效果或移除效果时，效果也会被处理。把同一个 `QGraphicsEffect *` 安装到第二个目标上，会让第一个目标失去它，不能共享。

## 3. 使用现成效果的正确姿势

```cpp
#include <QGraphicsDropShadowEffect>
#include <QWidget>

auto *shadow = new QGraphicsDropShadowEffect;
shadow->setBlurRadius(18.0);
shadow->setOffset(0.0, 4.0);
shadow->setColor(QColor(0, 0, 0, 90));

panel->setGraphicsEffect(shadow);
```

这里无需给 `shadow` 再设置 `parent`，因为 `panel` 在安装时会取得所有权。需要临时关闭效果时，不必删除对象：

```cpp
shadow->setEnabled(false);
```

禁用的效果会让源内容正常绘制，适合性能较敏感的滚动、拖动或过渡过程。频繁创建、销毁效果通常比复用一个效果并改属性更容易造成不必要的重绘。

## 4. 自定义效果时最关键的两条分支

`draw(QPainter *)` 是唯一必须实现的纯虚函数。它决定效果最终如何输出，但并不意味着必须先把源内容转成位图。

### 路径一：直接绘制源内容

当效果只是根据 painter 状态改变透明度、裁剪或混合方式时，可直接调用：

```cpp
void MyEffect::draw(QPainter *painter)
{
    painter->setOpacity(0.6);
    drawSource(painter);
}
```

这条路径避免额外位图缓存，适合不需要读取邻近像素的简单效果。

### 路径二：获取源内容快照

模糊、描边、像素化这类算法需要读取源图像像素，应调用 `sourcePixmap()`：

```cpp
void MyEffect::draw(QPainter *painter)
{
    QPoint offset;
    const QPixmap source = sourcePixmap(
        Qt::DeviceCoordinates, &offset,
        QGraphicsEffect::PadToEffectiveBoundingRect);

    // 对 source 做自己的图像处理，再绘制结果。
    painter->setWorldTransform(QTransform());
    painter->drawPixmap(offset, source);
}
```

关键是坐标系：

- `Qt::LogicalCoordinates`：遵循目标当前的逻辑坐标和 painter 变换，适合直接按目标几何关系绘制。
- `Qt::DeviceCoordinates`：得到设备坐标中的快照。像素级算法常用它，避免在高 DPI 或缩放后反复把处理结果再缩放一次；切换到它后通常需要清空 painter 的 world transform，再按 `offset` 绘制。

## 5. 为什么效果会被裁掉

模糊和阴影会把像素扩散到源矩形外。若效果仍报告原始边界，视图或控件系统会把外侧像素裁掉，表现为阴影只剩一半或模糊边缘被切平。

自定义效果要重写 `boundingRectFor()`，返回足以容纳输出的矩形：

```cpp
QRectF MyGlowEffect::boundingRectFor(const QRectF &sourceRect) const
{
    return sourceRect.adjusted(-m_radius, -m_radius, m_radius, m_radius);
}
```

当影响边界的参数变化时，例如模糊半径、阴影偏移或描边宽度发生变化，还必须调用 `updateBoundingRect()`。它通知框架重新计算有效边界；只调用 `update()` 只能要求重绘，不能修复裁剪范围。

## 6. `ChangeFlag` 和源内容变化

框架通过 `sourceChanged(ChangeFlags)` 告诉自定义效果源发生了什么变化。通常只在效果维护缓存、纹理或预计算数据时才需要重写它。

| 标志 | 表示什么 | 自定义效果通常要做什么 |
| --- | --- | --- |
| `SourceAttached` | 效果刚安装到一个源对象。 | 初始化与目标相关的缓存。 |
| `SourceDetached` | 效果已从源对象脱离。 | 释放不再可用的缓存或引用。 |
| `SourceBoundingRectChanged` | 源内容的边界改变。 | 丢弃尺寸相关缓存，并考虑 `updateBoundingRect()`。 |
| `SourceInvalidated` | 源内容需要重新取得。 | 作废像素缓存并安排重绘。 |

不要保存 `source()` 返回的内部对象指针并在其它地方长期使用。头文件虽公开了该函数，但标记为 internal；自定义效果应该通过 `sourcePixmap()`、`sourceBoundingRect()`、`drawSource()` 等受保护接口与源交互。

## 7. `PixmapPadMode` 如何选

`sourcePixmap()` 的第三个参数决定快照是否预留边缘：

| 枚举值 | 用途 |
| --- | --- |
| `NoPad` | 不留额外边缘。输出不会越过源矩形时使用。 |
| `PadToTransparentBorder` | 为透明边缘预留空间，适合会向四周扩散像素的滤镜。 |
| `PadToEffectiveBoundingRect` | 预留到效果的有效边界，通常是自定义模糊、阴影和发光效果的稳妥选择。 |

边缘留得越大，临时位图也越大。动画中给大面积控件做大半径模糊会很贵，尤其在高 DPI 屏幕或滚动区域中；这类效果应限制面积、半径和更新频率。

## 8. API 逐项说明

### 公开状态和命令

- `isEnabled()` / `setEnabled(bool)`：读取或开关效果。禁用时源按正常方式绘制。
- `boundingRect()`：取得当前源内容经过效果后的有效边界。
- `boundingRectFor(const QRectF &sourceRect)`：根据给定源矩形计算效果边界。派生类用于将边缘扩大。
- `update()`：请求效果重新绘制。改变只影响像素的自定义参数后调用。
- `enabledChanged(bool)`：启用状态切换时发出。

### 派生类绘制接口

- `draw(QPainter *)`：必须实现；输出处理后的效果。
- `drawSource(QPainter *)`：不缓存图像，直接让源对象绘制。
- `sourcePixmap(...)`：取得源的 `QPixmap` 快照及其绘制偏移。
- `sourceBoundingRect(...)`：取得源内容的逻辑或设备坐标边界。
- `sourceIsPixmap()`：判断源内容是否可视为 pixmap，帮助决定是否值得走位图处理路径。
- `sourceChanged(ChangeFlags)`：接收源安装、卸载、边界变化或失效通知。
- `updateBoundingRect()`：通知框架效果的有效边界改变。

### 内部接口

- `source()`：返回框架内部的 `QGraphicsEffectSource`。它是公开但标注为 internal 的接口，普通应用和自定义效果都不应以它建立业务依赖。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsEffect(QObject *parent = nullptr)` | 构造效果基类。 | 抽象类，实际应创建派生类。 |
| 析构 | `virtual ~QGraphicsEffect()` | 销毁效果并解除与源的关联。 | 安装到目标后通常由目标接管并销毁。 |
| 属性 | `enabled : bool` | 保存效果是否参与绘制。 | 关闭可临时绕过效果，不等于删除对象。 |
| 读取 | `bool isEnabled() const` | 读取效果是否启用。 | 可用于性能降级或动画状态判断。 |
| 设置/槽 | `void setEnabled(bool enable)` | 启用或禁用效果。 | 状态变化会触发重绘并发出 `enabledChanged()`。 |
| 查询 | `QRectF boundingRect() const` | 返回当前效果的有效输出边界。 | 阴影、模糊通常比源对象边界更大。 |
| 可重写查询 | `virtual QRectF boundingRectFor(const QRectF &sourceRect) const` | 由源矩形推导效果输出边界。 | 自定义扩散类效果必须扩大结果，避免裁剪。 |
| 命令/槽 | `void update()` | 请求重新绘制效果。 | 只影响像素时使用；边界变化还要调用 `updateBoundingRect()`。 |
| 信号 | `void enabledChanged(bool enabled)` | 通知启用状态改变。 | 连接时提供 context，避免对象销毁后的回调。 |
| 受保护纯虚函数 | `virtual void draw(QPainter *painter) = 0` | 绘制处理后的最终内容。 | 自定义效果必须实现；不要直接调用目标的 `paint()`。 |
| 受保护函数 | `void drawSource(QPainter *painter)` | 直接绘制未处理的源内容。 | 简单透明度等效果可避免生成 pixmap。 |
| 受保护函数 | `QRectF sourceBoundingRect(Qt::CoordinateSystem system = Qt::LogicalCoordinates) const` | 查询源内容边界。 | 明确选择逻辑坐标还是设备坐标。 |
| 受保护函数 | `bool sourceIsPixmap() const` | 判断源是否可按 pixmap 路径处理。 | 只用作绘制策略判断，不要据此假设所有源都可共享缓存。 |
| 受保护函数 | `QPixmap sourcePixmap(Qt::CoordinateSystem system = Qt::LogicalCoordinates, QPoint *offset = nullptr, PixmapPadMode mode = PadToEffectiveBoundingRect) const` | 抓取源内容快照。 | 像素处理要处理 `offset`；大快照会带来性能成本。 |
| 受保护可重写函数 | `virtual void sourceChanged(ChangeFlags flags)` | 接收源对象状态变化。 | 有缓存时重写，并按标志作废相应缓存。 |
| 受保护函数 | `void updateBoundingRect()` | 通知框架重新计算效果边界。 | 改变模糊半径、描边宽度、偏移等几何参数后调用。 |
| 内部接口 | `QGraphicsEffectSource *source() const` | 返回 Qt 内部源包装对象。 | 标记 internal；不要作为应用层 API 使用。 |
| 枚举 | `ChangeFlag` / `ChangeFlags` | 描述源的安装、卸载、边界变化和失效。 | 在 `sourceChanged()` 中按标志管理缓存。 |
| 枚举 | `PixmapPadMode` | 选择源快照的边缘留白策略。 | 过滤会扩散像素时不能盲用 `NoPad`。 |

## 10. 常见问题

1. 阴影或模糊被裁边：检查派生类的 `boundingRectFor()`，以及参数改变时是否调用 `updateBoundingRect()`。
2. 自定义效果画面位置错：使用 `sourcePixmap()` 后按返回的 `offset` 绘制，并确认逻辑/设备坐标选择。
3. 目标没有效果：确认效果仍在目标上，且 `isEnabled()` 为 `true`。
4. 界面卡顿：缩小受效果影响的区域，降低模糊半径，避免每次鼠标移动都更新大尺寸快照。

### 一句话总结

`QGraphicsEffect` 是目标内容与像素处理之间的绘制钩子：现成效果直接安装使用；自定义效果的关键是正确取得源内容、报告扩大的输出边界，并在参数变化时区分重绘和边界更新。
