# QSize
> Qt 6.11.1 · Qt Core · 来自 `QSize`

## 作用定位
`QSize` 表示整数宽高，常用于控件尺寸、图像像素尺寸、布局约束和 `QRect` 的 size 部分。它不带位置，只回答“多大”。

## API 速查
| API | 是做什么的 |
|---|---|
| `QSize(w, h)` | 创建整数尺寸。 |
| `width()` / `height()` | 读取宽高。 |
| `setWidth()` / `setHeight()` | 修改单个维度。 |
| `isNull()` | 宽高都为 0。 |
| `isEmpty()` | 任一维度小于等于 0。 |
| `isValid()` | 宽高都大于等于 0。 |
| `expandedTo()` / `boundedTo()` | 与另一个尺寸取逐维最大或最小。 |
| `scaled()` / `scale()` | 按比例适配目标尺寸。 |
| `transposed()` | 交换宽高。 |
| `toSizeF()` | 转为浮点尺寸。 |

## 使用场景
```cpp
QSize preview = image.size().scaled(QSize(320, 240), Qt::KeepAspectRatio);
label->setFixedSize(preview);
```

## 常见坑与经验
- `isEmpty()` 比 `isNull()` 更适合判断能否绘制，因为宽或高为 0 都没有面积。
- 布局计算可能产生负尺寸，传给绘制或数组分配前先验证。
- 高 DPI 或动画插值使用 `QSizeF`，最后落到像素时再转换。

## 知识点覆盖
尺寸约束、布局、图像缩放、空尺寸与无效尺寸、纵横比、高 DPI。
