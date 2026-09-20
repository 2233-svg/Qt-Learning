# Qt QTabletEvent：读取数位笔输入状态的事件对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTabletEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QSinglePointEvent` -> `QPointerEvent` -> `QInputEvent` -> `QEvent`  
> 类型定位：描述数位笔、绘图笔或其他 tablet pointing device 单点输入的事件

## 1. 它解决什么问题

鼠标事件通常只能表达位置、按键和按键组合；绘图笔还需要表达压感、笔身倾斜、笔身旋转、侧向压力以及与感应面的距离。`QTabletEvent` 把这些设备特有的输入值和普通单点事件的坐标、按钮、修饰键放在同一个事件中，适合实现：

- 绘画、书法、签名和批注工具；
- 根据压力改变笔刷粗细、透明度或不透明度；
- 根据 `xTilt()`、`yTilt()` 模拟喷笔、铅笔或斜锋笔效果；
- 读取橡皮擦、压感笔和专业绘图板的设备能力；
- 在自定义 `QWidget`、`QWindow` 或画布控件中建立平滑的笔迹输入。

它描述的是一次输入通知，不是设备配置对象。设备名称、唯一标识、能力和指针类型应通过继承体系中的 `pointingDevice()` 与设备对象查询；笔刷、采样、平滑和笔迹模型则由应用负责。

## 2. 事件处理的最小用法

```cpp
void Canvas::tabletEvent(QTabletEvent *event)
{
    const QPointF point = event->position();
    const qreal pressure = event->pressure();

    switch (event->type()) {
    case QEvent::TabletPress:
        beginStroke(point, pressure);
        event->accept();
        break;
    case QEvent::TabletMove:
        continueStroke(point, pressure, event->xTilt(), event->yTilt());
        event->accept();
        break;
    case QEvent::TabletRelease:
        endStroke(point, pressure);
        event->accept();
        break;
    default:
        event->ignore();
        break;
    }
}
```

实际项目中通常还要读取 `pointingDevice()->pointerType()`，区分笔尖、橡皮擦或其他指针；仅凭 `button()` 并不能完整识别“笔尖还是橡皮擦”。

## 3. 继承来的单点事件语义

### 坐标

- `position()`：事件接收对象局部坐标中的浮点位置；
- `scenePosition()`：场景或窗口坐标中的浮点位置；
- `globalPosition()`：全局屏幕坐标中的浮点位置。

对于 QWidget 处理函数，通常使用 `position()`；需要跨窗口、屏幕或记录设备轨迹时再使用全局坐标。浮点坐标保留了高分辨率采样信息，Qt 6 中不应主动退回整数坐标。

### 按钮和修饰键

- `button()`：本次事件触发或释放的按钮；
- `buttons()`：事件发生时仍处于按下状态的按钮集合；
- `modifiers()`：事件发生时的键盘修饰键；
- `device()` / `pointingDevice()`：输入设备对象；
- `pointerType()`：设备报告的指针类型。

按下事件应重点看 `button()`；移动事件中 `button()` 可能是 `Qt::NoButton`，此时应看 `buttons()` 判断是否仍在拖动。不要把 `button()` 和 `buttons()` 当成同一个概念。

## 4. 平板专有数值

### `pressure()`

返回笔尖压力，通常是归一化的 `qreal`，常见逻辑范围接近 `0.0` 到 `1.0`。但具体范围、分辨率、零点和平台转换方式受设备驱动与平台能力影响，应用不应假定所有硬件都具有相同有效位数。

压力可能用于映射笔刷宽度：

```cpp
const qreal normalized = qBound<qreal>(0.0, event->pressure(), 1.0);
const qreal width = minWidth + normalized * (maxWidth - minWidth);
```

如果设备不提供压力，值可能长期为固定值或不具备可用变化。不要把压力直接当作物理牛顿值，也不要在未确认设备能力时把 `0` 自动解释成“用户没有接触”。

### `xTilt()` 和 `yTilt()`

返回笔相对感应面在两个轴上的倾角，单位是角度；它们不是位置坐标，也不是向量长度。正负方向和最大角度由平台与设备约定决定，应用若要跨平台保持一致，应通过实机校准或以效果而非绝对方向为依据。

倾角适合影响笔刷纹理、椭圆形笔尖和阴影方向。只使用一个轴时要明确另一轴仍然可能变化，不能把二者当作互斥模式。

### `rotation()`

返回笔身围绕笔轴的旋转量。它通过事件点的 `QEventPoint` 数据提供，可能因设备不支持旋转而固定、无效或不具有业务意义。旋转范围和零度方向也可能因设备而不同，使用前应确认 `pointingDevice()` 的能力。

### `tangentialPressure()`

表示侧向压力或 barrel wheel 一类的附加压力。许多普通绘图笔不提供该轴，因此常见结果为 `0` 或固定值。它不等于笔尖压力；如果设备没有该能力，应用应回退到默认工具行为。

### `z()`

表示设备报告的距离或高度值，只有部分平台和设备会提供。Qt 不保证所有驱动都把它映射为相同单位、范围或方向，因此不能无条件把它当作毫米，也不能依靠它判断“离开屏幕”的精确时刻。离屏生命周期应以事件类型和设备报告为准。

## 5. 事件生命周期、抓取和传播

平板输入通常经历 `TabletPress`、多个 `TabletMove`、`TabletRelease`。应用开始绘制时应记录当前设备、指针类型和按钮状态；移动过程中要处理没有按钮变化但压力或倾角变化的采样；释放时结束笔划并清理临时状态。

事件接收对象可以抓取指针，使后续事件即使笔移出控件仍继续送到当前交互对象。使用抓取时要在释放、取消或窗口失活路径中清理笔划状态，否则应用可能一直处于“正在绘制”状态。

如果平板事件未被接受并继续传播，Qt 在适用平台和配置下可能把它转换或伴随生成鼠标事件。一个绘画控件同时处理平板和鼠标会导致一次笔划被画两遍。能够处理该笔事件时应明确 `accept()`；若确实希望上层或鼠标兼容路径接收，再调用 `ignore()`。

事件指针只在事件处理期间有效。不要把 `QTabletEvent *` 保存到异步任务或队列中；需要延迟处理时应立即复制坐标、压力、倾角、按钮和设备标识等必要数据。

## 6. 设备能力与跨平台边界

`QTabletEvent` 的字段是事件中报告出来的值，不是能力探测 API。使用压感、旋转或距离前，应查看 `pointingDevice()` 的设备信息和 `QInputDevice` / `QPointingDevice` 能力，或对输入进行运行时校准。

可能出现的情况包括：

- 压感笔被系统识别为普通指针，收到的压力没有变化；
- 驱动没有提供旋转或侧向压力；
- 高 DPI、窗口缩放和设备坐标转换导致位置需要使用浮点值；
- 不同操作系统对橡皮擦、按钮和指针类型的映射不同；
- 同一设备在平板模式、鼠标模式或驱动软件启用后报告不同数据。

因此，跨平台代码应为缺失轴提供退化行为：固定宽度、默认纹理或忽略旋转，而不是因为一个可选字段不可用就拒绝整次输入。

## 7. 构造函数的用途

```cpp
QTabletEvent(Type type, const QPointingDevice *device,
             const QPointF &pos, const QPointF &globalPos,
             qreal pressure, float xTilt, float yTilt,
             float tangentialPressure, qreal rotation, float z,
             Qt::KeyboardModifiers keyState,
             Qt::MouseButton button, Qt::MouseButtons buttons);
```

构造函数允许测试代码或集成层构造一个带有设备数据的事件。它不会连接真实硬件，也不会自动把事件投递给窗口；要让对象参与事件系统仍需使用 `QCoreApplication::sendEvent()`、`postEvent()` 或窗口系统的正常输入路径。

手工构造事件时，`device`、坐标体系、按钮集合和事件类型必须彼此一致。构造一个 `TabletMove` 却把按钮集合、压力和设备指针类型设置成不相容的组合，只能测试应用对异常输入的容错，不能模拟真实驱动行为。

## 8. Qt 6 迁移提示

Qt 6 保留了一些整数坐标访问器作为弃用兼容接口，例如 `pos()`、`globalPos()`、`x()`、`y()`、`globalX()` 和 `globalY()`；应改用 `position()` 与 `globalPosition()`，需要整数时在业务边界显式调用 `toPoint()` 或进行合适的取整。

`uniqueId()` 也属于弃用迁移路径，Qt 6 推荐通过 `pointingDevice()->uniqueId()` 获取设备唯一标识。设备指针可能为空，因此读取前应检查。

## 9. 常见误区

### 9.1 把压力范围写死成设备物理规格

事件通常提供逻辑归一化值。先进行边界裁剪和设备校准，不要把它直接解释为牛顿或固定硬件级别。

### 9.2 把倾角当坐标

`xTilt()`、`yTilt()` 是角度；笔尖位置仍应从 `position()` 获取。

### 9.3 只看 `button()`

移动事件常以 `Qt::NoButton` 表示“没有新按钮动作”。拖动或绘制期间要结合 `buttons()` 和应用自己的笔划状态。

### 9.4 同时处理平板和合成鼠标事件

未接受的平板事件可能触发鼠标兼容输入。绘画控件应明确接受已处理的平板事件，并避免重复响应。

### 9.5 保存事件指针

事件对象的有效期很短。异步处理必须复制数据，而不是保存裸指针。

### 9.6 认为构造函数能模拟完整硬件

手工事件只是一条事件记录，不会产生驱动采样、设备能力协商、指针抓取或系统级光标行为。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QTabletEvent(Type, const QPointingDevice *, const QPointF &, const QPointF &, qreal, float, float, float, qreal, float, Qt::KeyboardModifiers, Qt::MouseButton, Qt::MouseButtons)` | 构造一条平板事件 | 主要用于测试和集成；不会模拟真实硬件 |
| 继承 | `position() const` | 获取局部浮点坐标 | Qt 6 推荐接口；坐标属于接收对象 |
| 继承 | `scenePosition() const` | 获取场景/窗口浮点坐标 | 不要与局部坐标混用 |
| 继承 | `globalPosition() const` | 获取全局浮点坐标 | 适合跨窗口记录和屏幕定位 |
| 继承 | `button() const` | 获取本次按钮动作 | 移动事件可能为 `Qt::NoButton` |
| 继承 | `buttons() const` | 获取当前按下按钮集合 | 适合判断拖动/绘制是否持续 |
| 继承 | `modifiers() const` | 获取键盘修饰键 | 是事件发生时的快照 |
| 继承 | `device() const` | 获取输入设备 | 可能为空 |
| 继承 | `pointingDevice() const` | 获取指针设备 | 可继续查询指针类型和设备能力 |
| 继承 | `pointerType() const` | 获取指针类型 | 橡皮擦等识别应结合设备报告 |
| 生命周期 | `isBeginEvent() const` | 判断是否为开始阶段 | 继承自 `QPointerEvent`；也可按事件类型判断 |
| 生命周期 | `isUpdateEvent() const` | 判断是否为更新阶段 | 适合处理连续移动采样 |
| 生命周期 | `isEndEvent() const` | 判断是否为结束阶段 | 结束时清理笔划状态 |
| 抓取 | `exclusivePointGrabber() const` | 查询单点独占抓取对象 | 需要处理窗口失活和释放路径 |
| 抓取 | `setExclusivePointGrabber(QObject *)` | 设置单点独占抓取对象 | 不是普通业务状态替代品 |
| 专有数据 | `pressure() const` | 获取笔尖压力 | 通常近似归一化；设备能力可能缺失 |
| 专有数据 | `xTilt() const` | 获取 X 轴倾角 | 角度，不是坐标；方向由设备/平台决定 |
| 专有数据 | `yTilt() const` | 获取 Y 轴倾角 | 角度，不是坐标；方向由设备/平台决定 |
| 专有数据 | `rotation() const` | 获取笔身旋转 | 设备可能不支持或返回固定值 |
| 专有数据 | `tangentialPressure() const` | 获取侧向压力 | 常见为不支持或零 |
| 专有数据 | `z() const` | 获取设备距离/高度 | 单位和可用性不统一 |
| 兼容 | `pos() const` | 获取整数局部坐标 | Qt 6 弃用；改用 `position()` |
| 兼容 | `globalPos() const` | 获取整数全局坐标 | Qt 6 弃用；改用 `globalPosition()` |
| 兼容 | `posF() const` | 获取浮点局部坐标 | Qt 6 弃用；改用 `position()` |
| 兼容 | `globalPosF() const` | 获取浮点全局坐标 | Qt 6 弃用；改用 `globalPosition()` |
| 兼容 | `x() const` / `y() const` | 获取整数局部坐标分量 | Qt 6 弃用；改用 `position().x()/y()` |
| 兼容 | `globalX() const` / `globalY() const` | 获取整数全局坐标分量 | Qt 6 弃用；改用 `globalPosition().x()/y()` |
| 兼容 | `hiResGlobalX() const` / `hiResGlobalY() const` | 获取浮点全局坐标分量 | Qt 6 弃用；改用 `globalPosition()` |
| 兼容 | `uniqueId() const` | 获取旧式数位笔标识 | Qt 6 弃用；改用 `pointingDevice()->uniqueId()` |

---

### 一句话总结

`QTabletEvent` 是绘图笔单点输入的事件快照：用继承来的浮点坐标、按钮和设备信息处理生命周期，用 `pressure()`、`xTilt()`、`yTilt()`、`rotation()`、`tangentialPressure()` 和 `z()`表达笔的附加维度。可选能力、平台映射和事件传播都不能想当然，已处理的事件应明确接受，延迟处理时应复制数据。
