# Qt QSvgRenderer 深入笔记：加载 SVG 并交给 QPainter 渲染

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSvgRenderer>`  
> 所属模块：`Qt6::Svg`  
> 继承：`QObject -> QSvgRenderer`  
> 线程说明：类成员可重入；不要把同一个 renderer 当作可并发读写的共享对象。

`QSvgRenderer` 把已经加载的 SVG 文档渲染到任意 `QPainter`。因此它不只用于屏幕控件：可以画到 `QWidget` 的 `paintEvent()`、`QImage`、`QPdfWriter`、`QPrinter` 或另一个绘图设备。

它解决的是“怎样解析一份 SVG，并在 Qt 的绘图管线里按需要绘制整张图或某个带 id 的元素”。它不是用于生成 SVG 的类；导出 QPainter 绘制结果应使用 `QSvgGenerator`。

```text
.svg 文件 / 内存字节 / QXmlStreamReader
                 |
                 v
           QSvgRenderer
                 |
                 v
          QPainter + 目标设备
```

## 1. 最常见的工作流

先创建 renderer，加载文档，检查 `isValid()` 或 `load()` 的返回值，最后在目标 painter 上调用 `render()`。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Svg)
target_link_libraries(mytarget PRIVATE Qt6::Svg)
```

```cpp
#include <QImage>
#include <QPainter>
#include <QSvgRenderer>

QSvgRenderer renderer;
if (!renderer.load(":/icons/company-mark.svg")) {
    return;
}

const QSize size = renderer.defaultSize();
if (!size.isValid()) {
    return;
}

QImage image(size, QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::transparent);

QPainter painter(&image);
renderer.render(&painter);
```

构造函数也能直接接收文件名、`QByteArray` 或 `QXmlStreamReader`，但它们会在构造期间立刻加载。需要在加载前设置解析选项时，先用无参构造，再 `setOptions()`，最后调用 `load()`。

## 2. 加载来源与失败处理

`load()` 有三种来源：

- `QString`：文件路径或资源路径，例如 `:/icons/a.svg`。
- `QByteArray`：已经读入内存的 SVG XML。
- `QXmlStreamReader *`：你希望把 SVG 解析嵌入自己现有的流式读取过程。

```cpp
QSvgRenderer renderer;
const QByteArray svg = reply->readAll();

if (!renderer.load(svg)) {
    qWarning() << "Invalid SVG";
    return;
}
```

`load()` 返回 `false` 时，不应继续假定 renderer 内有可绘制文档；用 `isValid()` 可以再次确认当前文档状态。与 `QUiLoader` 不同，`QSvgRenderer` 没有 `errorString()`，因此网络或文件 I/O 失败要在读取阶段自己保留上下文和错误信息。

## 3. 缩放：`viewBox`、`bounds` 与纵横比

### 3.1 先分清三个概念

- SVG 自己的 `viewBox`：文档原有的逻辑可见区域。
- `setViewBox()`：在 renderer 侧改写要显示的逻辑区域，类似裁切/选区。
- `render(painter, bounds)` 的 `bounds`：把输出放进目标画布的哪块矩形。

`aspectRatioMode` 的默认值是 `Qt::IgnoreAspectRatio`，意味着内容会拉伸填满目标范围；设为 `Qt::KeepAspectRatio` 时，Qt 会把内容居中并尽可能放大而不改变比例。

不过 Qt 6.11.1 的 `render(QPainter *, const QRectF &bounds)` 成员说明还特别写明：`bounds` 非空时输出会填满它而忽略 SVG 的纵横比。实际项目中，只要图标或 logo 不能变形，就不要仅凭某个属性设置赌行为；应自己先按源宽高算出居中的等比例目标矩形，再把该矩形传给 `render()`。

```cpp
const QSize source = renderer.defaultSize();
const QSize target(320, 160);
const QSize fitted = source.scaled(target, Qt::KeepAspectRatio);
const QRectF bounds(
    (target.width() - fitted.width()) / 2.0,
    (target.height() - fitted.height()) / 2.0,
    fitted.width(),
    fitted.height());

renderer.render(&painter, bounds);
```

### 3.2 只绘制 SVG 的一个元素

若 SVG 内有 `<g id="warning">` 或其他可渲染元素，可使用：

```cpp
renderer.render(&painter, "warning", QRectF(0, 0, 64, 64));
```

`elementExists("warning")` 只对可渲染元素返回 `true`。像渐变、填充样式一类即便带有 id，也不是可单独渲染的元素，查询会返回 `false`。

`boundsOnElement(id)` 得到的边界不包含父元素变换；要获得逻辑坐标中的边界，应将 `transformForElement(id)` 返回的父级变换应用到这个矩形上。

## 4. 动画 SVG：谁负责刷新

`animated()` 只判断当前文档是否含动画元素，不表示动画已经在跑。对于动画 SVG：

- `framesPerSecond` 控制播放帧率。
- `animationEnabled` 为 `false` 时会停止动画计时器。
- `repaintNeeded()` 表示当前图像该重新画了，通常在这里安排控件更新。

```cpp
connect(&renderer, &QSvgRenderer::repaintNeeded,
        this, QOverload<>::of(&QWidget::update));
```

在 `QWidget::paintEvent()` 中调用 `render()`，而不是在 `repaintNeeded()` 信号里直接临时构造一个 painter。后者很容易破坏 QWidget 正常的绘制时机。

`currentFrame()`、`setCurrentFrame()` 和 `animationDuration()` 也由当前 Qt 6.11.1 头文件声明，适合需要手动检查或定位动画时间线的场景。它们只对动画 SVG 有意义；静态 SVG 不应依赖这些值驱动业务状态。

## 5. 解析选项必须早于加载

`QtSvg::Options` 从 Qt 6.7 起作为 `options` 属性提供，用于开启或关闭 SVG 的部分解析、渲染能力。它的生效时点很严格：

```cpp
QSvgRenderer renderer;
renderer.setOptions(options);
renderer.load(svgBytes);
```

一旦调用 `load()`，再修改 `options` 不会改变已经解析的文档。直接传入文件名或字节数组的构造函数也会立即加载，因此不适合“先配 options 再加载”的流程。

`setDefaultOptions()` 是全局默认值，影响之后创建的 renderer；Qt 6.8 起可用，运行时还可能被 `QT_SVG_DEFAULT_OPTIONS` 环境变量覆盖。库代码一般应避免随意修改全局默认值，以免影响宿主程序的其他 SVG。

## 6. 对象、线程与使用边界

`QSvgRenderer` 是 `QObject`，可以传入 parent 交给对象树销毁；但 `QPainter` 和目标设备的生命周期依然由调用者控制。要在界面控件中长期使用，通常把 renderer 作为该控件的成员或 child，而不是每次 `paintEvent()` 都重复解析文件。

“可重入”表示不同线程中使用不同 renderer 实例是允许的。一个实例有可变的已加载文档、动画定时器和属性，不应在多个线程同时 `load()`、改属性或 `render()`；GUI 目标也只能在 GUI 线程绘制。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSvgRenderer(QObject *parent = nullptr)` | 创建尚未加载文档的 renderer | 需要先设置 `options` 时使用它，再调用 `load()` |
| 构造 | `QSvgRenderer(const QString &filename, QObject *parent = nullptr)` | 创建并立即加载文件或资源路径 | 加载失败后检查 `isValid()`；无法在加载前设置实例 options |
| 构造 | `QSvgRenderer(const QByteArray &contents, QObject *parent = nullptr)` | 创建并立即解析内存中的 SVG | 字节内容必须在构造时就是完整 SVG；options 的设置时机同样太晚 |
| 构造 | `QSvgRenderer(QXmlStreamReader *contents, QObject *parent = nullptr)` | 创建并从流式 XML 读取器立即解析 SVG | 调用方负责 reader 的生命周期和当前位置正确 |
| 析构 | `~QSvgRenderer()` | 销毁已加载的 SVG 文档和动画状态 | 由 QObject parent 管理时不要再手动重复释放 |
| 有效性 | `isValid() const` | 判断当前是否有有效 SVG 文档 | `load()` 失败后不要继续渲染，先检查它 |
| 文档尺寸 | `defaultSize() const` | 返回 SVG 文档声明或推导出的默认尺寸 | 可作为 `QImage` 初始尺寸；先确认返回值有效 |
| 可见区域 | `viewBox() const` | 以整数矩形读取当前逻辑可见区域 | 小数坐标会被转换；需要精度时用 `viewBoxF()` |
| 可见区域 | `viewBoxF() const` | 以浮点矩形读取当前逻辑可见区域 | 用于精确裁切和坐标映射 |
| 可见区域 | `setViewBox(const QRect &viewBox)` | 以整数矩形设置要显示的 SVG 逻辑区域 | 会改变之后的渲染范围，不是设置目标像素大小 |
| 可见区域 | `setViewBox(const QRectF &viewBox)` | 以浮点矩形设置要显示的 SVG 逻辑区域 | 适合小数坐标；与 `render()` 的目标 bounds 是两层概念 |
| 纵横比 | `aspectRatioMode() const` | 读取当前纵横比策略 | 默认是 `Qt::IgnoreAspectRatio` |
| 纵横比 | `setAspectRatioMode(Qt::AspectRatioMode mode)` | 设置 SVG 映射到目标范围时的纵横比策略 | logo 这类内容优先考虑 `Qt::KeepAspectRatio`；`render(bounds)` 的细节仍要实测或自行计算等比矩形 |
| 解析选项 | `options() const` | 读取本实例的 SVG 解析与渲染选项 | Qt 6.7 起可用 |
| 解析选项 | `setOptions(QtSvg::Options flags)` | 设置本实例在下次加载时采用的选项 | 必须在 `load()` 之前调用；构造即加载的重载无法满足这个顺序 |
| 动画判断 | `animated() const` | 判断当前 SVG 是否含动画元素 | `true` 不等于动画已经启动或界面已经刷新 |
| 动画帧率 | `framesPerSecond() const` | 读取动画播放帧率 | 仅对动画 SVG 有实际意义 |
| 动画帧率 | `setFramesPerSecond(int num)` | 设置动画播放帧率 | 改动会影响刷新频率和 CPU 消耗 |
| 当前帧 | `currentFrame() const` | 读取动画当前帧 | 当前安装头文件声明该接口；静态 SVG 上不要依赖其值 |
| 当前帧 | `setCurrentFrame(int frame)` | 将动画定位到指定帧 | 只用于可动画文档；传入范围应和实际动画帧数匹配 |
| 动画时长 | `animationDuration() const` | 读取当前动画的总时长 | 只在动画 SVG 上有意义；用作时间线逻辑前先验证文档确实可动画 |
| 动画开关 | `isAnimationEnabled() const` | 查询动画计时器是否启用 | Qt 6.7 起可用；与 `animated()` 一起判断才完整 |
| 动画开关 | `setAnimationEnabled(bool enable)` | 启动或停止动画计时器 | 静态 SVG 上没有效果；停止后仍可手动渲染当前帧 |
| 元素查询 | `boundsOnElement(const QString &id) const` | 返回指定元素的局部边界 | 不包含父元素变换；配合 `transformForElement()` 使用 |
| 元素查询 | `elementExists(const QString &id) const` | 判断指定 id 是否对应可渲染元素 | 渐变等样式节点即使有 id 也会返回 `false` |
| 元素查询 | `transformForElement(const QString &id) const` | 返回指定元素父级变换的乘积矩阵 | 不含元素自身 transform；用于把局部边界映射到逻辑坐标 |
| 加载槽 | `load(const QString &filename)` | 从路径加载 SVG | 返回 `false` 时停止渲染流程；重载连接信号时用 `qOverload` 明确签名 |
| 加载槽 | `load(const QByteArray &contents)` | 从内存字节加载 SVG | 适合网络下载或资源解包后的内容；同样会覆盖当前文档 |
| 加载槽 | `load(QXmlStreamReader *contents)` | 从流式 XML reader 加载 SVG | reader 的读取位置和生命周期由调用方负责 |
| 渲染槽 | `render(QPainter *painter)` | 用默认尺寸和当前视图渲染整张 SVG | painter 必须已有效地绑定到目标设备 |
| 渲染槽 | `render(QPainter *painter, const QRectF &bounds)` | 把整张 SVG 绘制到给定目标矩形 | Qt 6.11.1 详细说明指出非空 bounds 会填满区域并忽略比例；重要图形请手动算等比 bounds |
| 渲染槽 | `render(QPainter *painter, const QString &elementId, const QRectF &bounds = QRectF())` | 只渲染指定 id 的元素 | 先用 `elementExists()` 过滤；同名重载连信号时要显式选择签名 |
| 刷新信号 | `repaintNeeded()` | 当前渲染内容需要更新时发出，通常由动画触发 | 连接到 `QWidget::update()` 等调度接口，不要在信号回调里越过正常绘制周期 |
| 全局默认项 | `setDefaultOptions(QtSvg::Options flags)` | 设置后续创建 renderer 的全局默认选项 | Qt 6.8 起可用；会影响进程内其他实例，并可能被环境变量覆盖 |

---

### 一句话总结

`QSvgRenderer` 负责“加载一份 SVG，然后交给 QPainter 画出来”。核心不是记住三种 `load()`，而是先处理加载失败、理清逻辑 `viewBox` 与目标 `bounds`，并让动画通过 `repaintNeeded()` 回到正常的界面刷新流程。
