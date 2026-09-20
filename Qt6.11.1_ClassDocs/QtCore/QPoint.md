# QPoint
> Qt 6.11.1 · Qt Core · 来自 `QPoint`

## 作用定位
`QPoint` 是整数二维坐标或位移值，广泛用于鼠标位置、控件坐标、像素偏移和 `QRect` 角点。

## API 速查
| API | 是做什么的 |
|---|---|
| `(x, y)` / `setX/setY` | 创建或修改坐标。 |
| `x/y` | 读取分量。 |
| `manhattanLength()` | 返回 `abs(x)+abs(y)`，适合拖拽阈值。 |
| `transposed()` | 交换 x、y。 |
| `toPointF()` | 转为浮点坐标。 |
| `+ - * /` | 做位移和整数缩放。 |

## 使用场景
```cpp
if ((event->pos() - pressPos).manhattanLength()
    >= QApplication::startDragDistance())
    beginDrag();
```
## 常见坑与经验
- 坐标系统取决于对象：`QMouseEvent::pos()` 是局部坐标，`globalPosition()` 是屏幕坐标。
- 整数除法会截断；布局和缩放计算先用 `QPointF`。
- 这不是向量库，不提供归一化与浮点长度。
## 知识点覆盖
坐标系、局部/全局位置、像素精度、拖拽阈值、整数算术。
