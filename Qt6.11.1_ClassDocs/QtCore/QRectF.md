# QRectF
> Qt 6.11.1 · Qt Core · 来自 `QRectF`

## 作用定位
`QRectF` 是连续坐标系的浮点矩形，适合布局计算、动画、缩放、图形视图和高 DPI 几何。右、下边界是几何边缘，不采用 `QRect` 的“减一像素”包含式规则。

## API 速查
| API | 是做什么的 |
|---|---|
| `(x, y, width, height)` / 点加尺寸构造 | 创建浮点矩形。 |
| `contains()` / `intersects()` | 命中或重叠判断。 |
| `intersected()` / `united()` | 计算交集或包围并集。 |
| `normalized()` | 将负宽高规范为正向区域。 |
| `adjust()` / `adjusted()` | 按四边偏移修改区域。 |
| `move*` / `set*` | 保持尺寸移动，或固定对边改变尺寸。 |
| `toRect()` | 四舍五入成整数矩形。 |
| `toAlignedRect()` | 得到完整覆盖原区域的最小整数矩形。 |
| `qFuzzyCompare()` | 以浮点容差比较矩形。 |

## 使用场景
```cpp
QRectF target = source.adjusted(-0.5, -0.5, 0.5, 0.5);
painter.drawRect(target);
```
绘制和布局链路中保持 `QRectF`，只在调用只接受像素整数的 API 时转化。需要确保不裁掉边缘内容时使用 `toAlignedRect()`。

## 常见坑与经验
- 浮点坐标不要直接用 `==` 判断计算结果；需要近似判断时使用 `qFuzzyCompare()`。
- `toRect()` 与 `toAlignedRect()` 的意图不同：前者取近似值，后者保证覆盖。
- `isValid()` 要求宽高大于零；反向拖拽先规范化。
- 向 `QRectF` 传 NaN 或无穷数没有正常几何意义，应在外部数值计算层拦截。

## 知识点覆盖
浮点几何、DPI、布局与绘制、舍入策略、包围盒、容差比较、命中测试。
