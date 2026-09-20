# QTabletEvent

> Qt 6.11.1 · Qt GUI · 来自 `QTabletEvent`

## 1. 先建立直觉

`QTabletEvent` 描述绘图板、手写笔、艺术笔、喷笔、4D 鼠标等专业指针设备产生的事件。它继承自 `QSinglePointEvent`，所以具备位置、按钮和修饰键信息；它自身额外提供压力、倾斜、旋转、切向压力和 Z 轴位置。

如果 `QMouseEvent` 只够表达“在哪里按下”，`QTabletEvent` 表达的是“用什么工具、以什么姿态、施加多大压力在这个位置输入”。绘图、批注、签名、建模和专业创作软件都应该优先利用这些维度。

## 2. 类说明

`QTabletEvent` 继承自 `QSinglePointEvent`。它通常由 `QWidget::tabletEvent()` 或 `QObject::event()` 中的 `QEvent::TabletPress`、`TabletMove`、`TabletRelease`、`TabletEnterProximity`、`TabletLeaveProximity` 分支接收。

类说明只用于表明这些 API 来自 `QTabletEvent`：压力、倾斜、旋转、切向压力和 Z 轴是平板事件特有数据；坐标、按钮和设备信息来自父类输入模型。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTabletEvent(type, dev, pos, globalPos, pressure, xTilt, yTilt, tangentialPressure, rotation, z, keyState, button, buttons)` | 构造平板事件，常用于平台层、测试或事件转发。 |
| `pressure() const` | 返回笔压，通常 0.0 到 1.0；绘制笔触粗细和透明度时最常用。 |
| `xTilt() const` | 返回设备相对 X 轴方向的倾斜角度。 |
| `yTilt() const` | 返回设备相对 Y 轴方向的倾斜角度。 |
| `rotation() const` | 返回设备绕自身轴线的旋转角度，艺术笔、Apple Pencil 等设备可能支持。 |
| `tangentialPressure() const` | 返回喷笔指轮等切向压力，范围通常为 -1.0 到 1.0。 |
| `z() const` | 返回 Z 轴位置，常见于 4D 鼠标或特殊设备；不是笔压。 |
| `pointerType() const` | 来自父类，可区分笔尖、橡皮擦等指针类型。 |
| `pointingDevice() const` | 来自父类，可检查设备能力和类型。 |

## 4. 关键用法

### 用压力驱动笔刷

笔压最常见的用途是影响笔触半径、透明度或纹理强度。

```cpp
void PaintArea::tabletEvent(QTabletEvent *event)
{
    if (event->type() == QEvent::TabletMove && event->pressure() > 0.0) {
        const qreal radius = m_minRadius + event->pressure() * (m_maxRadius - m_minRadius);
        drawDab(event->position(), radius, event->pressure());
        event->accept();
        return;
    }

    QWidget::tabletEvent(event);
}
```

不要把压力简单当成鼠标左键。很多设备在接近但未接触绘板时也会产生移动或邻近事件，此时压力可能为 0。

### 倾斜和旋转适合表现真实笔触

书法笔、马克笔、铅笔侧锋都可以从倾斜和旋转中得到更自然的形状。

```cpp
BrushShape shape;
shape.angle = std::atan2(event->yTilt(), event->xTilt());
shape.flatness = qMin<qreal>(1.0, std::hypot(event->xTilt(), event->yTilt()) / 60.0);
shape.rotation = event->rotation();
```

不是所有设备都支持这些能力。使用前可以结合 `pointingDevice()->capabilities()` 判断，或把 0 值作为默认姿态处理。

### 区分笔尖和橡皮擦端

许多压感笔有橡皮擦端。用 `pointerType()` 切换工具比让用户手动切换更自然。

```cpp
void PaintArea::tabletEvent(QTabletEvent *event)
{
    if (event->pointerType() == QPointingDevice::PointerType::Eraser)
        eraseAt(event->position(), event->pressure());
    else
        paintAt(event->position(), event->pressure());

    event->accept();
}
```

## 5. 使用场景

`QTabletEvent` 用于绘画软件、签名板、PDF 批注、电子白板、医学影像标注、3D 建模、动画分镜、工业手写输入等场景。只要输入质量依赖“力度和姿态”，它就比 `QMouseEvent` 更合适。

它也适合做设备诊断。专业设备在不同平台和驱动下能力差异明显，读取压力、倾斜、旋转、切向压力和设备 capability 能快速判断问题出在应用逻辑还是设备后端。

在混合输入应用中，平板事件可能伴随合成鼠标事件。专业绘图控件通常会接受平板事件并抑制重复鼠标路径，避免一笔被绘制两次。

## 6. 常见坑与经验

不要假设所有数值都有效。设备不支持旋转、Z 轴、切向压力时通常返回 0；这不是用户一定垂直握笔，而是能力不存在。

不要把 `z()` 和 `pressure()` 混为一谈。压力表示接触力度，Z 轴表示设备额外的空间位置或轮值。

不要忽略邻近事件。`TabletEnterProximity` 和 `TabletLeaveProximity` 可以用于显示笔刷预览、切换当前工具、更新光标，但它们不一定表示真正接触绘板。

不要过早把浮点坐标和压力量化成整数。压感设备的价值就在连续输入，量化会让线条抖动或阶梯化。

## 7. 知识点覆盖

学习 `QTabletEvent` 应覆盖平板事件类型、笔压、倾斜角、旋转、切向压力、Z 轴、设备 capability、笔尖与橡皮擦、邻近事件、合成鼠标事件、浮点坐标、高 DPI、笔刷建模和跨平台驱动差异。
