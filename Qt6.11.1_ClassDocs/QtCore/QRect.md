# QRect
> Qt 6.11.1 · Qt Core · 来自 `QRect`

## 作用定位
`QRect` 表示整数坐标系中的轴对齐矩形，常用于像素区域、控件几何、裁剪区和命中测试。它存的是位置与尺寸，不是绘制命令。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `(x, y, width, height)` | 以左上角和尺寸创建区域。 |
| `x/y/width/height/size` | 读取位置与尺寸。 |
| `left/top/right/bottom` | 读取边界坐标；整数 `right/bottom` 是包含式边界。 |
| `contains()` | 判断点或矩形是否在区域内。 |
| `intersects()` / `intersected()` | 判断或取得交集。 |
| `united()` | 取得能包住两个矩形的最小边界矩形。 |
| `adjusted()` / `marginsAdded()` | 扩大或缩小区域。 |
| `normalized()` | 修正负宽高导致的反向边界。 |
| `translated()` / `moveTo()` | 平移区域而不改变尺寸。 |

## 使用场景
```cpp
QRect content = widget->rect().marginsRemoved(QMargins(12, 8, 12, 8));
if (content.contains(mouseEvent->pos()))
    handleContentClick();
```

## 常见坑与经验
- `QRect` 的 `right() == left() + width() - 1`，而 `QRectF` 的右边界是几何边缘；混用转换时先理解包含式与连续坐标差异。
- 拖拽反向得到的矩形应先 `normalized()`，再进行绘制或命中测试。
- `isNull()`、`isEmpty()`、`isValid()` 含义不同；零尺寸不等于可用的绘制区域。
- 高 DPI 及浮点布局计算中使用 `QRectF`，最后落到像素栅格时再转换为 `QRect`。

## 知识点覆盖
像素几何、包含式边界、命中测试、裁剪、边距、整数舍入、DPI 与 `QRectF` 转换。
