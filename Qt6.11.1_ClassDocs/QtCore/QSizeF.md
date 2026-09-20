# QSizeF
> Qt 6.11.1 · Qt Core · 来自 `QSizeF`

## 作用定位
`QSizeF` 是浮点宽高，适合布局中间值、缩放比例、打印/绘图坐标和动画尺寸。它避免整数过早舍入造成的累积误差。

## API 速查
| API | 是做什么的 |
|---|---|
| `QSizeF(w, h)` | 创建浮点尺寸。 |
| `width()` / `height()` | 读取宽高。 |
| `isNull()` / `isEmpty()` / `isValid()` | 判断零尺寸、无面积和合法尺寸。 |
| `scaled()` / `scale()` | 按模式缩放到目标范围。 |
| `expandedTo()` / `boundedTo()` | 逐维放大或限制。 |
| `toSize()` | 四舍五入到整数尺寸。 |
| `transposed()` | 交换宽高。 |

## 使用场景
动画和绘制先保持浮点尺寸：
```cpp
QSizeF logical = QSizeF(image.size()) / devicePixelRatio;
```

## 常见坑与经验
- `toSize()` 会舍入，不等于向下取整；像素边界敏感时手动控制舍入策略。
- 浮点尺寸比较使用容差，别把计算结果直接与字面值做严格相等。
- 宽高为负通常表示上游计算错误，先规范或拒绝。

## 知识点覆盖
浮点布局、缩放、打印坐标、高 DPI、舍入策略、尺寸有效性。
