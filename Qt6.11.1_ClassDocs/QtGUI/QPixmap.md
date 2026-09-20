# QPixmap

> Qt 6.11.1 · Qt GUI · 来自 `QPixmap`

## 1. 先建立直觉

`QPixmap` 是为屏幕/窗口系统绘制准备的图像资源。它常能以平台更合适的方式保存，适合作为控件图标、背景、缓存图层和 `QPainter` 的绘制源，但不适合逐像素算法。

简单规则很实用：**处理像素、后台解码用 `QImage`；在 GUI 线程把结果转成 `QPixmap` 显示。** 这种分工既清楚又避开了不同平台上 pixmap 对窗口系统资源的依赖。

## 2. 类说明

- 头文件：`#include <QPixmap>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：隐式共享值类型，内容改变时自动 detach。
- 线程：把创建、加载、修改和使用 `QPixmap` 限在 GUI 线程。后台线程传 `QImage` 回来后再转换。
- 它是 `QPaintDevice`，可以用 `QPainter` 直接绘制到 pixmap，但此时不要同时 `fill()`、`scroll()` 或修改同一 pixmap。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QPixmap(size)` / `QPixmap(fileName)` | 分配未初始化 pixmap 或从资源/文件加载 |
| `load()` / `loadFromData()` | 解码并载入图像数据；成功后才可使用 |
| `fromImage()` / `convertFromImage()` | 把 CPU 图像转换为显示资源 |
| `fromImageReader()` | 可直接由 reader 读取为 pixmap，某些平台省内存 |
| `toImage()` | 转回 `QImage` 以做像素处理 |
| `isNull()` / `size()` / `rect()` / `depth()` | 检查内容和物理尺寸 |
| `fill()` | 填充 pixmap；不能在活跃 painter 期间调用 |
| `copy()` | 深复制全图或区域 |
| `scaled()` / `scaledToWidth()` / `scaledToHeight()` | 返回缩放后的 pixmap |
| `transformed()` / `trueMatrix()` | 返回几何变换后的 pixmap和实际补偿矩阵 |
| `scroll()` | 原地移动区域，并可获知裸露区域 |
| `devicePixelRatio()` / `deviceIndependentSize()` | 读取高 DPI 的显示解释和逻辑尺寸 |
| `setDevicePixelRatio()` | 给已有像素赋予 DPR 语义，不重采样 |
| `hasAlphaChannel()` / `hasAlpha()` | 查询原生 alpha 或 alpha/mask 的可见透明性 |
| `mask()` / `setMask()` | 获取或设置 1-bit 遮罩，通常较昂贵 |
| `createHeuristicMask()` / `createMaskFromColor()` | 从像素内容猜测/创建旧式遮罩 |
| `cacheKey()` | 识别共享内容版本，内容变化会变 |
| `detach()` | 显式断开共享；仅在原生句柄修改等罕见情况需要 |
| `save()` | 编码到文件或 `QIODevice` |
| `defaultDepth()` | 获取主屏默认 pixmap 深度，须已有 `QGuiApplication` |
| `operator QVariant()` / 数据流运算符 | 同 QVariant、QDataStream 互操作 |

## 4. 关键用法

### 从后台处理结果安全显示

```cpp
// Worker: 只创建和处理 QImage
QImage processed = decodeAndFilter(bytes);

// GUI thread:
if (!processed.isNull())
    label->setPixmap(QPixmap::fromImage(processed));
```

不要把 `QPixmap` 放进 worker 做缩放、读取或缓存，即便在某些机器上看起来可用。它可能依赖 GUI/窗口系统资源；`QImage` 才是后台工作对象。

### 创建高 DPI 图标资源

```cpp
QPixmap icon(":/icons/save@2x.png");
icon.setDevicePixelRatio(2.0);

button->setIcon(QIcon(icon));
const QSizeF logical = icon.deviceIndependentSize(); // 例如 16 x 16
```

物理 `size()` 可能是 `32 x 32`，但 DPR 为 2 时逻辑显示尺寸是 `16 x 16`。布局里不要把物理尺寸当 UI 尺寸；Qt 6.2 起直接用 `deviceIndependentSize()`。

### 使用 pixmap 做局部滚动缓存

```cpp
QRegion exposed;
backBuffer.scroll(0, -scrollDelta, backBuffer.rect(), &exposed);

QPainter p(&backBuffer);
for (const QRect &r : exposed)
    paintNewRows(p, r);
```

`scroll()` 移动已有像素，不会重画新暴露的区域；`exposed` 才是你需要补画的范围。调用它之前必须结束任何仍在该 pixmap 上活动的 painter。

### 依据内容版本缓存变换结果

```cpp
if (rotatedKey != source.cacheKey()) {
    rotated = source.transformed(transform, Qt::SmoothTransformation);
    rotatedKey = source.cacheKey();
}
```

`cacheKey()` 很适合判断 Qt pixmap 内容是否变更，不是跨程序、跨运行或永久持久化的 ID。

## 5. 使用场景

- `QLabel`、`QIcon`、工具栏、菜单与按钮的显示图像。
- GUI 线程中的背景缓存、滚动缓存、复杂自绘控件离屏层。
- 从 `QImageReader` 或 `QImage` 解码后立即显示的资源。
- 高 DPI 下的多倍率 icon/thumbnail 展示。

## 6. 常见坑与经验

- **新建 pixmap 未初始化。** `QPixmap(width, height)` 后先 `fill()`，否则会显示未定义内容。
- **不是像素算法容器。** `toImage()` 后再滤镜、取样、访问 alpha；改完再 `fromImage()`。
- **`setMask()` 是旧式且昂贵的路径。** 有 alpha 通道时优先使用 alpha，不要每帧提取 `mask()`。
- **`hasAlpha()` 与 `hasAlphaChannel()` 不同。** 前者也把 mask 视作透明性，后者只问像素格式是否有 alpha 通道。
- **缩略图不要每次重采样。** 连续 resize 过程可用 painter 缩放，稳定尺寸再生成 `scaled()` 缓存。
- **从文件加载会依赖运行时路径。** 资源路径写 `:/...`；相对磁盘路径相对于工作目录，容易在打包后失败。
- **转换不是免费的。** `QImage` 与 `QPixmap` 来回转换、启发式 mask、复杂 transform 都可能产生大副本；缓存稳定结果。

## 7. 知识点覆盖

窗口系统显示资源、GUI 线程约束、QImage/QPixmap 分工、隐式共享、高 DPI DPR、离屏缓存、区域滚动、alpha 与遮罩、图像转换成本、资源路径。
