# QPainter::PixmapFragment

> Qt 6.11.1 · Qt GUI · 来自 `QPainter::PixmapFragment`

## 1. 先建立直觉

`QPainter::PixmapFragment` 是给 `QPainter::drawPixmapFragments()` 用的小结构体：它描述“从一张 pixmap 的哪个源矩形切一块，放到目标坐标的哪里，按多少比例缩放、旋转，并以多少透明度绘制”。

它的典型用途不是画一张普通图片，而是批量画很多来自同一张图集的碎片：精灵动画、粒子、图标 atlas、地图瓦片、重复纹理片段。一次调用提交多个 fragment，通常比循环里反复 `drawPixmap()` 更利于绘制后端优化。

## 2. 类说明

- 头文件：`#include <QPainter>`
- 所属类：`QPainter`
- 类型性质：公开数据结构，主要由字段组成
- 使用入口：`QPainter::drawPixmapFragments(...)`
- 源图像：所有 fragment 共用同一个 `QPixmap`

`PixmapFragment` 的目标位置字段 `x` / `y` 表示目标矩形的中心点，不是左上角。目标矩形大小来自源矩形宽高再乘以 `scaleX` / `scaleY`，随后按 `rotation` 旋转。

## 3. API 速查

| API / 字段 | 作用 |
| --- | --- |
| `create(pos, sourceRect, scaleX, scaleY, rotation, opacity)` | 便利构造函数，把位置、源矩形、缩放、旋转和透明度一次填入结构体。 |
| `x` / `y` | 目标片段中心点坐标。 |
| `sourceLeft` / `sourceTop` | 源 pixmap 中要截取的矩形左上角。 |
| `width` / `height` | 源矩形尺寸，同时也是未缩放目标尺寸的基础。 |
| `scaleX` / `scaleY` | 目标绘制时的水平/垂直缩放比例。 |
| `rotation` | 旋转角度，单位为度；缩放后围绕中心点旋转。 |
| `opacity` | 单个片段透明度，`0.0` 完全透明，`1.0` 完全不透明。 |
| `QPainter::OpaqueHint` | 告诉绘制系统这些片段是不透明的，可减少不必要的混合成本。 |

## 4. 关键用法

### 从图集批量绘制精灵

```cpp
QVector<QPainter::PixmapFragment> fragments;
fragments.reserve(items.size());

for (const Sprite &sprite : items) {
    fragments.push_back(QPainter::PixmapFragment::create(
        sprite.center,
        sprite.sourceRect,
        sprite.scale,
        sprite.scale,
        sprite.angle,
        sprite.opacity));
}

painter.drawPixmapFragments(fragments.constData(),
                            fragments.size(),
                            atlasPixmap);
```

所有片段来自同一张 `atlasPixmap`。如果你的素材分散在多张 pixmap 中，需要按 pixmap 分组后分别调用。

### 目标坐标是中心点

```cpp
auto fragment = QPainter::PixmapFragment::create(
    QPointF(100, 80),      // 目标中心
    QRectF(32, 0, 16, 16), // 图集里的源块
    2.0, 2.0);            // 画成 32 x 32
```

这段代码最终把源块放到以 `(100, 80)` 为中心的位置，而不是从 `(100, 80)` 开始画。做碰撞框或鼠标命中时要把中心语义换算回来。

## 5. 使用场景

- 2D 游戏或动画：大量角色、特效、子弹、粒子来自同一张图集。
- 地图和棋盘：重复绘制许多小图片块。
- 图标面板：一张 icon atlas 中切出不同状态。
- 数据可视化：大量点标记共享一套纹理素材。
- 自定义控件：对同一 pixmap 做大量缩放、旋转、透明度变化。

## 6. 常见坑与经验

- **坐标是中心点。** 这和 `drawPixmap(point, pixmap)` 的左上角语义不同，是最容易错的地方。
- **源矩形在 pixmap 坐标中。** 高 DPI pixmap 可能带有 `devicePixelRatio`，切图前要确认源坐标和素材实际像素是否一致。
- **透明度是逐片段的。** 它会和 painter 当前的 `opacity()`、合成模式一起作用，最终结果可能比单独看 fragment 更透明。
- **`OpaqueHint` 只能在真的不透明时使用。** 如果源图或片段带 alpha，却声明不透明，可能得到错误混合结果。
- **不要为每个片段切一张 pixmap。** 这样会抵消批绘制的意义；fragment 的设计就是共用源 pixmap。
- **旋转和缩放会影响边界。** 如果目标区域需要裁剪或重绘脏区，不能只用未旋转矩形估算。

## 7. 知识点覆盖

- 图集、源矩形、目标中心点之间的坐标关系
- 批量绘制与循环 `drawPixmap()` 的性能差异
- 缩放、旋转、透明度、合成模式的叠加
- 高 DPI pixmap 与源坐标的匹配
- `QPainter::PixmapFragmentHints` 的优化边界
- 粒子、精灵和图标 atlas 的实际组织方式
