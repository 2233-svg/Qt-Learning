# QInputEvent

> Qt 6.11.1 · Qt GUI · 来自 `QInputEvent`

## 1. 先建立直觉

`QInputEvent` 是所有 GUI 输入事件的共同基类之一。它不负责描述“按下了哪个键”“鼠标在哪个坐标”“触点有几个”，这些细节交给 `QKeyEvent`、`QMouseEvent`、`QTouchEvent` 等子类；它保存的是输入事件都会关心的公共上下文：事件来自哪个输入设备、发生时有哪些键盘修饰键、窗口系统给出的时间戳。

把它理解成输入事件的“来源标签”会更准确：当同一个手势可能来自鼠标、触摸板、触摸屏、手写笔或由系统合成出来的事件时，`QInputEvent` 让你先判断事件的来源，再决定是否把它当作鼠标、触控、笔输入或快捷操作处理。

## 2. 类说明

`QInputEvent` 继承自 `QEvent`，常见派生类包括 `QKeyEvent`、`QPointerEvent` 和 `QContextMenuEvent`。业务代码通常不会直接创建或处理裸的 `QInputEvent`，而是在重写 `QWidget`、`QWindow` 的输入事件函数，或在 `event()` / `eventFilter()` 中拿到一个更具体的事件对象后，通过基类 API 读取公共信息。

使用它时要记住三件事：

- 事件对象通常只在当前事件处理调用期间有效，不要长期保存事件指针。
- `modifiers()` 表示事件发生时的修饰键状态，不等同于你处理到事件这一刻键盘的最新状态。
- `device()` 在 Qt 6 里比旧式 `source()` 更有价值，尤其适合区分真实鼠标事件和触摸合成鼠标事件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `device() const` | 取得产生该事件的输入设备对象，可进一步判断名称、类型、能力和 seat。 |
| `deviceType() const` | 快速取得设备类型，例如鼠标、触摸屏、触摸板、键盘等。 |
| `modifiers() const` | 读取事件发生时的 `Shift`、`Ctrl`、`Alt`、`Meta` 等键盘修饰符组合。 |
| `timestamp() const` | 读取窗口系统给事件标记的时间戳，常用于节流、双击/长按逻辑或事件排序。 |

## 4. 关键用法

### 判断事件是不是由触摸合成

Qt 6 更推荐从设备角度理解输入来源。比如某些平台会把触摸屏点击合成为鼠标事件，让老代码也能工作；但绘图板、地图、手势编辑器这类程序往往需要区分真实鼠标和触摸输入。

```cpp
void MyWidget::mousePressEvent(QMouseEvent *event)
{
    if (event->deviceType() == QInputDevice::DeviceType::TouchScreen) {
        event->ignore();
        return;
    }

    beginMouseSelection(event->position());
    event->accept();
}
```

这里不要只看事件类型是 `QEvent::MouseButtonPress`。事件类型说明 Qt 分发了鼠标事件，`deviceType()` 才更接近“它最初来自哪里”。

### 读取修饰键要以事件为准

`modifiers()` 是事件快照。处理快捷拖拽、框选、复制拖动时，应以事件里的修饰键判断，而不是临时调用全局键盘状态。

```cpp
void Canvas::mouseMoveEvent(QMouseEvent *event)
{
    const bool additive = event->modifiers().testFlag(Qt::ShiftModifier);
    updateRubberBand(event->position(), additive);
}
```

这样做能避免事件队列延迟带来的问题：用户可能已经松开 `Shift`，但当前这次移动事件发生时它仍然是按下的。

### 时间戳适合做输入节流

`timestamp()` 通常来自窗口系统，单位一般是毫秒，但起点不是 Unix 时间。它适合计算两个事件之间的相对间隔，不适合显示成真实日期。

```cpp
bool StrokeFilter::shouldSample(const QInputEvent *event)
{
    if (event->timestamp() - m_lastSampleTime < 8)
        return false;

    m_lastSampleTime = event->timestamp();
    return true;
}
```

## 5. 使用场景

`QInputEvent` 最常见于“跨输入类型的公共判断”。例如绘图软件里，鼠标、触控笔和触摸输入都可能进入同一套工具逻辑，此时可以把设备类型、修饰键、时间戳先抽出来，作为统一的上下文。

它也适合事件过滤器。过滤器经常先拿到 `QEvent *`，通过 `event->type()` 判断是否是输入事件，再转为具体子类。公共字段越早判断，分支越清楚。

另一个高频场景是兼容平台差异。不同窗口系统对触摸板、触摸屏、鼠标合成事件的行为并不完全一致，直接依赖“鼠标事件就是鼠标硬件”容易出错；基于 `device()` 和 `deviceType()` 做策略会稳得多。

## 6. 常见坑与经验

不要缓存 `device()` 返回值并假设它永远代表同一个物理设备的完整生命周期。通常可以在事件处理期间读取它的属性；如果要长期记录设备，保存设备类型、名称、系统 ID 等更明确的数据会更安全。

不要把 `timestamp()` 当作墙上时钟。它的价值是比较相邻事件的时间差，例如“上一次输入到这一次输入间隔多久”。

不要在基类层面吞掉所有输入事件。`QInputEvent` 只告诉你公共上下文，真正的按钮、坐标、按键文本、触点状态都在派生类里；如果判断不充分就 `accept()`，很容易让控件默认行为失效。

## 7. 知识点覆盖

学习 `QInputEvent` 时，重点覆盖 Qt 事件系统、输入设备抽象、键盘修饰符、事件时间戳、事件接受与忽略、合成输入事件、事件过滤器和平台输入差异。掌握它之后，再看 `QKeyEvent`、`QPointerEvent`、`QMouseEvent`、`QTouchEvent` 会更容易形成一套统一的输入处理模型。
