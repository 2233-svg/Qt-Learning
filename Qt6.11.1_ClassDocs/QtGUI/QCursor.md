# QCursor

> Qt 6.11.1 · Qt GUI · 来自 `QCursor`

## 1. 先建立直觉

`QCursor` 是鼠标指针外观与位置的值类型。它既可以表示标准系统光标，例如箭头、文本选择、拖拽、缩放，也可以表示带热点的自定义 pixmap 或单色 bitmap 光标。

使用时要区分两件事：

- 控件“希望显示什么形状”：通常用 `QWidget::setCursor()`、`unsetCursor()`，传入一个 `QCursor`。
- 系统光标“此刻在哪里”：用静态 `QCursor::pos()` 查询；用 `setPos()` 移动。

前者是界面反馈，后者会影响真实系统输入，副作用完全不同。

## 2. 类说明

`QCursor` 不继承 `QObject`，可复制、可移动、可放入容器。标准光标由 Qt 与平台窗口系统实现；自定义光标封装 pixmap 或 bitmap、mask 与 hotspot。

类说明只用于表明这些 API 来自 `QCursor`。控件级 cursor override 由 `QWidget` / `QWindow` 管理，应用级临时覆盖通常用 `QGuiApplication::setOverrideCursor()`，不要靠全局移动光标解决控件交互问题。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QCursor()` | 构造默认箭头光标。 |
| `QCursor(Qt::CursorShape)` | 用标准形状构造光标。 |
| `QCursor(pixmap, hotX, hotY)` | 用彩色 pixmap 构造自定义光标。 |
| `QCursor(bitmap, mask, hotX, hotY)` | 用 1-bit bitmap 与 mask 构造单色光标。 |
| `shape() const` | 返回标准光标形状标识。 |
| `setShape(shape)` | 切换为标准光标形状。 |
| `pixmap()` | 返回 pixmap 光标图像；非 pixmap 光标时可能无效。 |
| `bitmap()` / `mask()` | 返回 bitmap 光标图像与掩码；标准光标时通常为空。 |
| `hotSpot()` | 返回点击命中的热点坐标。 |
| `pos()` / `pos(screen)` | 查询系统光标在全局坐标中的当前位置。 |
| `setPos(...)` | 将系统光标移动到指定全局位置。 |
| `swap(other)` | 高效交换两个光标值。 |
| `operator==` / `operator!=` | 比较两个光标配置是否相同。 |
| 流运算符 | 用 `QDataStream` 序列化与反序列化光标。 |

## 4. 关键用法

### 用标准形状表达可交互语义

```cpp
ResizeHandle::ResizeHandle(QWidget *parent)
    : QWidget(parent)
{
    setCursor(Qt::SizeHorCursor);
}
```

标准光标比自定义图片更符合平台习惯，也能随系统主题、缩放和无障碍设置变化。只有确有品牌或工具语义需求时再使用自定义图像。

### 自定义光标必须设置合理热点

```cpp
QPixmap brushCursor(":/cursors/brush.png");
QCursor cursor(brushCursor, 3, 28);
canvas->setCursor(cursor);
```

hotspot 是用户真正点击位置，不一定是图片中心。画笔尖端、十字准星中心、拖拽手柄尖端都应对准实际命中点；热点设错会让绘图和选取产生明显偏移。

### 事件处理优先使用事件位置

```cpp
void Canvas::mouseMoveEvent(QMouseEvent *event)
{
    updatePreview(event->position());
}
```

不要在事件处理中用 `QCursor::pos()` 替代 `event->globalPosition()` 或 `event->position()`。事件坐标表示事件发生时的位置；全局查询返回当前系统位置，高频输入和异步窗口系统下两者可能不同。

### 谨慎使用 `setPos()`

```cpp
QCursor::setPos(mapToGlobal(targetPoint));
```

它会真的移动操作系统光标，并可能触发新的鼠标事件。适合无障碍辅助、受控演示或特定原生集成，不适合普通拖拽、吸附或单元测试模拟。

## 5. 使用场景

`QCursor` 适合调整大小手柄、文本选择、拖拽目标、画布工具、链接区域、忙碌状态、取色器、图形编辑器和自定义输入工具。

它也适合高精度工具反馈。绘图应用可以根据当前工具在笔刷、橡皮擦、吸管、移动画布之间切换 cursor；但应保证图像分辨率与 device pixel ratio 匹配，避免高 DPI 下模糊。

## 6. 常见坑与经验

不要对每个 `mouseMoveEvent()` 调用 `setCursor()`。只有光标语义真的切换时才更新，否则会产生无意义的系统调用。

不要在普通交互中调用 `setPos()`。移动系统光标会干扰用户控制，也会让测试环境中事件状态与真实窗口系统状态不一致。

不要忘记清除临时覆盖光标。若使用 `QGuiApplication::setOverrideCursor()`，必须成对调用 `restoreOverrideCursor()`。

不要假设自定义光标尺寸在所有平台都被完整支持。过大图片可能被缩放、裁剪或由平台替换；32x32 一类常见尺寸兼容性更好。

不要只比较 `shape()` 判断自定义光标是否相同。自定义 pixmap、bitmap、mask 和 hotspot 都可能不同。

## 7. 知识点覆盖

学习 `QCursor` 应覆盖标准光标形状、控件 cursor、应用 override cursor、全局坐标、事件快照坐标、自定义 pixmap/bitmap 光标、热点、高 DPI、系统光标移动、跨平台限制和交互反馈设计。
