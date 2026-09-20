# Qt QScreen：屏幕拓扑、DPI 与方向信息

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScreen>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject -> QScreen`  
> 类型定位：屏幕信息与屏幕坐标查询对象

## 1. 它解决什么问题

`QScreen` 描述一个已经被 Qt GUI 平台发现的显示屏。它把应用在多屏、高 DPI、旋转显示器和窗口截图场景中经常需要的事实集中起来：

- 这个屏幕在虚拟桌面中的位置和大小；
- 避开任务栏、系统菜单等保留区域后的可用区域；
- 物理尺寸、物理 DPI、逻辑 DPI 和设备像素比；
- 当前方向、硬件原生方向、主方向以及方向之间的坐标变换；
- 刷新率、颜色深度和平台提供的显示器标识；
- 从屏幕或窗口系统表面抓取 `QPixmap`。

它不是“显示器配置器”，也不是应用窗口。`QScreen` 主要回答“屏幕现在是什么状态”，不负责创建显示器、改变系统分辨率、移动窗口或替应用决定布局。

屏幕对象不能由应用公开构造。应从 `QGuiApplication::primaryScreen()` 或 `QGuiApplication::screens()` 获取；热插拔时则通过 `QGuiApplication::screenAdded()` 和 `QGuiApplication::screenRemoved()` 跟踪对象集合。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QGuiApplication>
#include <QScreen>
```

qmake 工程使用：

```qmake
QT += gui
```

如果还要使用窗口或控件，应分别包含 `QWindow` 或 `QWidget`，并链接相应模块。`QScreen` 本身属于 `Gui`，不需要 `Widgets`。

## 3. 最小可用代码

```cpp
#include <QGuiApplication>
#include <QScreen>
#include <QDebug>

static void printScreen(QScreen *screen)
{
    if (!screen)
        return;

    qDebug() << screen->name()
             << "geometry =" << screen->geometry()
             << "available =" << screen->availableGeometry()
             << "dpr =" << screen->devicePixelRatio()
             << "logicalDpi =" << screen->logicalDotsPerInch()
             << "refreshRate =" << screen->refreshRate();
}

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);

    printScreen(app.primaryScreen());
    for (QScreen *screen : app.screens())
        printScreen(screen);

    return app.exec();
}
```

这段代码有三个重要前提：

1. 必须先创建 `QGuiApplication`，再查询屏幕集合。
2. `QScreen *` 是 Qt 管理的对象指针，不要 `new QScreen`，也不要手动 `delete`。
3. 如果窗口已经确定，应优先从窗口获取屏幕和设备像素比，而不是长期使用全局主屏幕：

```cpp
QScreen *screen = window->screen();
qreal dpr = window->devicePixelRatio();
```

## 4. 核心使用模型

### 4.1 屏幕对象来自应用的屏幕集合

`QScreen` 的构造函数是私有的，由 Qt 平台集成层创建。常用入口是：

- `QGuiApplication::primaryScreen()`：当前主屏幕；
- `QGuiApplication::screens()`：当前所有屏幕；
- `QGuiApplication::screenAdded(QScreen *)`：新增屏幕；
- `QGuiApplication::screenRemoved(QScreen *)`：屏幕即将从集合中移除。

屏幕移除后，之前保存的裸指针不能继续用于查询或截图。需要在移除信号中清理缓存、断开连接或改为使用新的屏幕对象。

### 4.2 `QScreen` 的坐标是屏幕级逻辑坐标

`geometry()`、`availableGeometry()` 和方向变换使用 Qt 的屏幕坐标系。高 DPI 环境下，应用层尺寸通常是设备无关像素；它们不能直接当作显卡 framebuffer 的物理像素尺寸。

同一虚拟桌面中的屏幕可以拥有负的 `x()` 或 `y()`。例如，位于主屏幕左侧的副屏可能从 `(-1920, 0)` 开始。不要假设所有屏幕都从 `(0, 0)` 开始，也不要仅根据 `size()` 推断屏幕位置。

### 4.3 单屏几何、可用几何和虚拟几何

可以按下面的层次区分：

| 查询 | 含义 |
| --- | --- |
| `geometry()` | 当前屏幕在虚拟桌面中的矩形，包含屏幕位置和尺寸 |
| `size()` | `geometry().size()` 对应的屏幕分辨率尺寸 |
| `availableGeometry()` | 排除任务栏、系统菜单等窗口管理器保留区域后的矩形 |
| `availableSize()` | 当前屏幕的可用尺寸 |
| `virtualSiblings()` | 与当前屏幕共享同一虚拟桌面坐标系的屏幕集合 |
| `virtualGeometry()` | 同组屏幕的 `geometry()` 并集形成的虚拟桌面包围矩形 |
| `virtualSize()` | 虚拟桌面的尺寸 |
| `availableVirtualGeometry()` | 同组屏幕的 `availableGeometry()` 并集 |
| `availableVirtualSize()` | 同组屏幕可用几何组合后的尺寸 |

虚拟桌面可能存在屏幕之间的空洞、错位或不同尺寸。`virtualGeometry()` 是并集得到的包围矩形，不代表矩形内每个点都落在某个真实屏幕上；用 `virtualSiblingAt()` 判断具体点是否落在屏幕上。

### 4.4 物理 DPI、逻辑 DPI 与设备像素比

三类值用途不同：

- `physicalDotsPerInchX/Y()`：根据屏幕物理尺寸和像素信息估算的显示密度，适合打印预览、物理尺寸估算等场景，但平台提供的数据可能不准确。
- `logicalDotsPerInchX/Y()`：窗口系统用于把点大小、字体和 UI 尺寸换算为应用像素的逻辑密度，可能受系统设置影响。
- `devicePixelRatio()`：物理像素与设备无关像素的比例，用于理解图像或底层资源的像素密度。

`physicalDotsPerInch()` 和 `logicalDotsPerInch()` 分别是对应 X、Y 值的平均值。Qt 文档规定物理 DPI 和逻辑 DPI 都以设备无关点表示；需要设备相关密度时，乘以 `devicePixelRatio()`。

如果目标是一个已知的 `QWindow`，应使用 `QWindow::devicePixelRatio()`。在 Wayland 分数缩放、窗口表面分辨率属性等情况下，窗口的 DPR 可能不同于它所在屏幕的 `devicePixelRatio()`。

### 4.5 方向参数不是任意角度

方向 API 使用 `Qt::ScreenOrientation`，常见值是：

- `Qt::LandscapeOrientation`
- `Qt::PortraitOrientation`
- `Qt::InvertedLandscapeOrientation`
- `Qt::InvertedPortraitOrientation`
- `Qt::PrimaryOrientation`

`Qt::PrimaryOrientation` 在 `angleBetween()`、`mapBetween()`、`transformBetween()`、`isPortrait()` 和 `isLandscape()` 中会被解释为 `primaryOrientation()`，不是一个需要调用方自行展开的第五种物理方向。

### 4.6 状态变化通过信号观察

尺寸、DPI、方向、虚拟桌面和刷新率都可能在程序运行期间改变。不要只在启动时读取一次并永久缓存。对于屏幕加入和移除，监听 `QGuiApplication` 的拓扑信号；对于已有屏幕的属性变化，监听 `QScreen` 的九个信号。

## 5. 实际使用场景

### 5.1 把窗口放到合适的工作区域

窗口初始化或跨屏移动时，可以用 `availableGeometry()` 约束窗口位置，避免被任务栏遮挡。不要用 `geometry()` 代替可用几何，也不要假设可用区域一定从 `(0, 0)` 开始。

### 5.2 为窗口选择正确的高 DPI 资源

已知窗口时，以 `QWindow::devicePixelRatio()` 为准加载图标、创建 framebuffer 或计算图像尺寸。只有没有目标窗口、需要估计某个屏幕的一般密度时，才直接使用 `QScreen::devicePixelRatio()`。

### 5.3 多屏拖动和跨屏布局

用 `virtualSiblings()` 确认屏幕是否属于同一虚拟桌面，用 `geometry()` 保存屏幕在全局坐标中的位置。跨屏定位时保留完整的 `QRect` 坐标，不要只保存 `QSize`。

### 5.4 移动设备旋转

用 `orientationChanged()` 响应窗口系统报告的当前方向；用 `nativeOrientation()` 了解硬件原生方向，用 `primaryOrientation()` 判断当前主方向。方向变化不等于直接读取加速度传感器，传感器数据属于其他模块和另一种抽象。

### 5.5 计算旋转后的内容区域

要把一个矩形从方向 `a` 的坐标系转换到方向 `b`，使用 `transformBetween()` 获取 `QTransform`，或使用 `mapBetween()` 直接获得变换后的包围矩形。前者适合连续坐标、绘制和点变换；后者适合布局区域、裁剪矩形等整数几何。

### 5.6 诊断显示器环境

`name()`、`manufacturer()`、`model()`、`serialNumber()`、`depth()`、刷新率和 DPI 信息适合写入诊断日志。平台可能无法提供完整标识，字符串为空或在系统配置改变后发生变化时，不能把它们未经确认地当作跨机器永久 ID。

### 5.7 截取屏幕或窗口内容

`grabWindow()` 可以截取整个屏幕、应用窗口或由 `WId` 指定的外部窗口。它是窗口系统级抓屏，不等价于从某个 widget 的离屏绘制结果读取像素；遮挡关系、权限和平台限制都会影响结果。

## 6. 生命周期、所有权和线程

### 6.1 不要创建或释放 `QScreen`

没有公开构造函数。屏幕由 `QGuiApplication` 和平台集成层管理，应用只借用返回的指针：

```cpp
QScreen *screen = QGuiApplication::primaryScreen();
```

不要对这个指针调用 `delete`，也不要把它包装进会独立释放指针的所有权对象。需要观察对象是否仍存在时，可在合适的 QObject 上使用 `QPointer<QScreen>`，但屏幕拓扑本身仍应通过 `screenRemoved()` 处理。

### 6.2 屏幕移除会使缓存指针失效

显示器拔出、远程桌面会话变化、窗口系统重新配置等情况都可能触发屏幕移除。`screenRemoved(QScreen *)` 发出后，该屏幕不再属于应用的有效屏幕集合。不要在异步任务中继续使用旧指针，也不要在回调里默认原窗口仍然位于该屏幕。

窗口本身可能通过 `QWindow::screenChanged(QScreen *)` 换屏。与窗口相关的 DPR、可用区域和资源选择，应在窗口的 `screenChanged` 中重新读取。

### 6.3 GUI 线程约束

`QScreen` 是 GUI 对象，屏幕对象、窗口系统状态和本地平台接口应在 GUI 线程使用。工作线程如果只需要数值，可以在 GUI 线程复制 `QRect`、`QSizeF`、`qreal` 和字符串后再传递；不要跨线程保存并调用 `QScreen *` 或 `handle()` 返回的本地句柄。

### 6.4 平台句柄不是稳定业务数据

`handle()` 返回 `QPlatformScreen *`，属于 Qt Platform Abstraction（QPA）层。QPA 接口可能造成源代码和二进制兼容性风险，不应让业务层、公共插件接口或跨模块数据模型依赖它。平台适配层可以读取它，再转换成应用自己的小型结果对象。

## 7. 属性之间的语义边界

### 7.1 `geometry()` 与 `availableGeometry()`

`geometry()` 表示屏幕的完整几何；`availableGeometry()` 排除了窗口管理器保留的任务栏、系统菜单等区域。窗口最大化、初始定位和工作区布局通常应使用后者。

X11 有明确限制：只有在单显示器系统且窗口管理器设置了 `_NET_WORKAREA` 时，`availableGeometry()` 才能返回真实可用区域；其他情况下它可能与 `geometry()` 相同。这是 X11 窗口管理器规范的限制，不是应用计算错误。

### 7.2 `virtualGeometry()` 与 `availableVirtualGeometry()`

前者并集的是每个虚拟 sibling 的完整 `geometry()`，后者并集的是每个 sibling 的 `availableGeometry()`。`availableVirtualGeometry()` 不是简单地从 `virtualGeometry()` 四周扣除一条统一的任务栏，因为不同屏幕的保留区域可以不同。

### 7.3 物理尺寸不等于逻辑窗口尺寸

`physicalSize()` 的单位是毫米，描述显示面板的实际物理尺寸估计；`size()` 是屏幕坐标中的像素尺寸。用 `physicalSize()` 计算真实英寸时，应意识到平台元数据可能不准确，且显示缩放不会把物理面板变大或变小。

### 7.4 `orientation()`、`primaryOrientation()` 与 `nativeOrientation()`

- `orientation()`：窗口系统当前报告的屏幕方向，移动设备自动旋转时可能改变。
- `primaryOrientation()`：根据当前主几何确定的主方向；宽度大于等于高度时是横向，否则是纵向，具体变化仍受平台和应用清单影响。
- `nativeOrientation()`：硬件铭牌或设备原生方向，是硬件属性，通常不会改变；平台不支持时可能返回 `Qt::PrimaryOrientation`。

### 7.5 刷新率不是动画时钟

`refreshRate()` 是近似的垂直刷新率，单位为 Hz。不要用它驱动 `QTimer` 或 `QChronoTimer` 来模拟绘制节拍；窗口动画或渲染应使用 `QWindow::requestUpdate()`，让窗口系统决定合适的更新时机。

## 8. 方向变换的具体规则

### 8.1 `angleBetween()`

`angleBetween(a, b)` 计算从方向 `a` 旋转到方向 `b` 所需的角度，返回值只可能是 `0`、`90`、`180` 或 `270`。方向是离散的屏幕方向，不要把返回值理解成任意角度传感器读数。

### 8.2 `transformBetween()`

`transformBetween(a, b, target)` 返回一个把方向 `a` 的坐标系映射到方向 `b` 的坐标系的 `QTransform`。`target` 提供目标矩形的尺寸和坐标范围。

文档中的典型例子是：`a` 为横向，`b` 为纵向，`target` 为 `QRect(0, 0, w, h)`。结果把横向坐标中的 `QRect(0, 0, h, w)` 旋转映射到纵向的 `QRect(0, 0, w, h)`；例如点 `(0, 0)` 映射到 `(0, w)`。

使用返回变换时，注意 `QTransform` 的坐标系方向和目标矩形原点，不要只根据 `angleBetween()` 手动交换宽高后忽略平移分量。

### 8.3 `mapBetween()`

`mapBetween(a, b, rect)` 直接返回矩形在两个方向之间的映射结果。当一个方向属于横向、另一个属于纵向时，矩形的 X/Y 尺寸会互换；横向到反向横向或纵向到反向纵向时，位置也会按照目标方向改变。

它适合矩形区域的布局或裁剪，不提供 `QTransform` 的连续点变换能力。若算法还要变换点、路径或绘制坐标，应使用 `transformBetween()`。

## 9. 截图 `grabWindow()` 的边界

`grabWindow(window, x, y, width, height)` 的语义是：

- `window == 0`：抓取整个屏幕；
- 非零 `window`：抓取由 `WId` 标识的窗口系统窗口；
- `x`、`y`：相对于目标窗口的偏移；
- `width < 0`：复制到窗口右边界；
- `height < 0`：复制到窗口下边界；
- 参数使用设备无关像素；
- 返回的 `QPixmap` 在高 DPI 屏幕上可能比请求的逻辑尺寸更大，应读取返回 pixmap 的 `devicePixelRatio()`。

它抓的是屏幕上的像素，不是窗口自己的离屏内容。因此另一个窗口覆盖在目标窗口上时，覆盖窗口的像素也可能被抓到；鼠标光标通常不会被抓取。

平台限制必须单独考虑：

- iOS 等沙箱平台通常不能抓取应用之外的窗口；
- X11 中，如果目标窗口与 root window 深度不同且被其他窗口遮挡，被遮挡区域可能是未初始化、未定义的像素；
- Windows Vista 及更高版本抓取设置了 `Qt::WA_TranslucentBackground` 的 layered window 可能失败，抓取 desktop widget 才可能有效；
- 抓取屏幕外区域通常不安全，行为取决于底层窗口系统。

## 10. 逐项 API 说明

### 10.1 屏幕标识与基础属性

#### `[read-only, constant] QString QScreen::name() const`

返回屏幕名称。它是平台提供的描述性字符串，不保证跨平台格式或永久稳定。适合显示和诊断，不应在没有平台保证时作为唯一持久化 ID。

#### `[read-only, constant] QString QScreen::manufacturer() const`

返回屏幕制造商字符串。平台没有提供时可能为空；不要假设它一定是标准化品牌名。

#### `[read-only, constant] QString QScreen::model() const`

返回屏幕型号字符串。它是平台元数据，可能为空或包含驱动程序提供的型号文本。

#### `[read-only, constant] QString QScreen::serialNumber() const`

返回屏幕序列号。平台或权限不提供时可能为空。即使非空，也应在使用前确认目标平台对其稳定性和隐私要求。

#### `[read-only, constant] int QScreen::depth() const`

返回屏幕的颜色深度。它描述屏幕或窗口系统报告的显示深度，不等于某一个 `QImage`、纹理或截图的通道位数。

### 10.2 屏幕几何

#### `[read-only] QSize QScreen::size() const`

返回屏幕的像素尺寸，对应 `geometry()` 的尺寸部分。它不包含屏幕在虚拟桌面中的位置。高 DPI 应用中不要把它无条件当作物理 framebuffer 的宽高；目标窗口的底层资源尺寸还要结合窗口 DPR。

#### `[read-only] QRect QScreen::geometry() const`

返回屏幕在虚拟桌面中的几何矩形，包含位置和尺寸。多屏布局中可能出现负坐标，不能假设 `topLeft()` 是 `(0, 0)`。

#### `[read-only] QSize QScreen::availableSize() const`

返回排除了任务栏、系统菜单等窗口管理器保留区域后的可用尺寸。需要窗口位置时使用 `availableGeometry()`，因为单独的 `QSize` 不携带原点。

#### `[read-only] QRect QScreen::availableGeometry() const`

返回当前屏幕的可用几何。适合限制窗口初始位置、最大化区域和工作区布局。X11 上可能由于 `_NET_WORKAREA` 不可用而退化为与 `geometry()` 相同。

#### `[read-only] QSize QScreen::virtualSize() const`

返回当前屏幕所属虚拟桌面的尺寸。它描述同组 virtual siblings 的联合桌面，不是当前单个屏幕的尺寸。

#### `[read-only] QRect QScreen::virtualGeometry() const`

返回同组 virtual siblings 的完整几何并集。结果是覆盖这些屏幕的虚拟桌面矩形，可能包含真实屏幕之间的空白区域。

#### `[read-only] QSize QScreen::availableVirtualSize() const`

返回同组屏幕可用几何组合后的尺寸。不同屏幕保留区域不一致时，它不应被理解为从完整虚拟桌面统一裁剪得到的简单尺寸。

#### `[read-only] QRect QScreen::availableVirtualGeometry() const`

返回同组 virtual siblings 的 `availableGeometry()` 并集。它表示可用于工作区布局的虚拟桌面范围，但内部仍可能存在屏幕布局空洞。

### 10.3 DPI 与高 DPI

#### `[read-only] QSizeF QScreen::physicalSize() const`

返回屏幕物理尺寸，单位为毫米。值来自平台提供的显示器信息，可能不完全准确；它适合物理尺寸估算，不是窗口布局的逻辑尺寸。

#### `[read-only] qreal QScreen::physicalDotsPerInchX() const`

返回水平方向物理 DPI。物理 DPI 以设备无关点表示，若要得到设备相关密度，按 Qt 文档乘以 `devicePixelRatio()`。

#### `[read-only] qreal QScreen::physicalDotsPerInchY() const`

返回垂直方向物理 DPI。它可能与 X 方向不同，不能总是用一个值替代两个方向。

#### `[read-only] qreal QScreen::physicalDotsPerInch() const`

返回 X、Y 物理 DPI 的平均值。它是方便属性，不会提供比两个方向值更高的测量精度。

#### `[read-only] qreal QScreen::logicalDotsPerInchX() const`

返回水平方向逻辑 DPI。它用于将点大小、字体和 UI 尺寸转换为应用像素，并可能受桌面环境的用户设置影响。

#### `[read-only] qreal QScreen::logicalDotsPerInchY() const`

返回垂直方向逻辑 DPI。需要精确处理非方形像素或方向性尺寸时，应分别读取 X、Y 值。

#### `[read-only] qreal QScreen::logicalDotsPerInch() const`

返回 X、Y 逻辑 DPI 的平均值。它适合一般 UI 尺寸估算；已知窗口的实际缩放仍应结合窗口本身的 DPR。

#### `[read-only] qreal QScreen::devicePixelRatio() const`

返回屏幕物理像素与设备无关像素的比例。它适合在没有明确目标窗口时做屏幕级估算；如果知道目标 `QWindow`，优先使用 `QWindow::devicePixelRatio()`，因为两者在分数缩放等场景可能不同。

### 10.4 方向与刷新率

#### `[read-only] Qt::ScreenOrientation QScreen::primaryOrientation() const`

返回主屏幕方向。通常屏幕几何宽度大于等于高度时为横向，否则为纵向；旋转显示器后它可能改变，最终行为受平台和应用清单影响。

#### `[read-only] Qt::ScreenOrientation QScreen::orientation() const`

返回窗口系统当前报告的屏幕方向。移动设备可能依据自动旋转改变该值；它不是直接的传感器读数。

#### `[read-only] Qt::ScreenOrientation QScreen::nativeOrientation() const`

返回硬件原生方向，即设备标识或硬件通常认为的正向。它是硬件属性，通常不变；平台不支持时可能返回 `Qt::PrimaryOrientation`。

#### `[read-only] qreal QScreen::refreshRate() const`

返回近似垂直刷新率，单位是 Hz。它适合诊断和显示信息，不应拿来驱动定时器动画；使用 `QWindow::requestUpdate()` 请求窗口更新。

### 10.5 虚拟桌面成员

#### `QList<QScreen *> QScreen::virtualSiblings() const`

返回与当前屏幕共享同一个虚拟桌面坐标系的屏幕集合。它们之间可以移动和定位窗口，而无需重新创建窗口。列表中的指针仍由 Qt 管理，屏幕移除后需要重新获取集合。

#### `QScreen *QScreen::virtualSiblingAt(QPoint point)`

返回包含 `point` 的 virtual sibling；如果点不在任何真实屏幕内，返回 `nullptr`。`point` 是相对于这组 virtual siblings 的虚拟桌面坐标，不是相对于当前屏幕左上角的局部坐标。

### 10.6 方向计算

#### `int QScreen::angleBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b) const`

计算从方向 `a` 到方向 `b` 的旋转角度，返回 `0`、`90`、`180` 或 `270`。`Qt::PrimaryOrientation` 会解析为 `primaryOrientation()`。

#### `QTransform QScreen::transformBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &target) const`

返回把方向 `a` 的坐标系映射到方向 `b` 的坐标系的变换。`target` 决定目标坐标的矩形范围。旋转时除了交换宽高，还需要处理平移，因此不要只根据角度自行调用 `rotate()`。

#### `QRect QScreen::mapBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &rect) const`

把矩形从方向 `a` 映射到方向 `b`。横向和纵向之间转换时 X/Y 尺寸会交换；`Qt::PrimaryOrientation` 按当前主方向解释。该函数返回矩形结果，不替代对任意点或路径使用 `QTransform`。

#### `bool QScreen::isPortrait(Qt::ScreenOrientation o) const`

当方向是纵向或反向纵向时返回 `true`，否则返回 `false`。`Qt::PrimaryOrientation` 按 `primaryOrientation()` 解释。

#### `bool QScreen::isLandscape(Qt::ScreenOrientation o) const`

当方向是横向或反向横向时返回 `true`，否则返回 `false`。`Qt::PrimaryOrientation` 按 `primaryOrientation()` 解释。

### 10.7 屏幕截图

#### `QPixmap QScreen::grabWindow(WId window = 0, int x = 0, int y = 0, int width = -1, int height = -1)`

抓取窗口系统中的像素并返回 `QPixmap`。`window == 0` 时抓取整个屏幕；否则按 `WId` 指定目标窗口。偏移和尺寸使用设备无关像素，负的宽度或高度表示复制到目标窗口相应边界。

该函数抓取屏幕内容，所以遮挡窗口可能出现在结果中，鼠标光标通常不会出现。高 DPI 下返回 pixmap 可能比逻辑请求尺寸更大，应读取其 `devicePixelRatio()`。外部窗口、X11 深度差异、Windows layered window、屏幕外区域和沙箱权限都会造成平台相关限制。

### 10.8 QPA 与原生接口

#### `QPlatformScreen *QScreen::handle() const`

返回 QPA 平台屏幕句柄。它是平台集成层的内部边界，可能带来源代码和二进制兼容性风险。除非正在编写明确隔离的平台适配代码，否则应使用 `nativeInterface<T>()` 或更高层的 Qt API。

#### `template <typename QNativeInterface> QNativeInterface *QScreen::nativeInterface() const`

请求指定平台的屏幕原生接口；接口不存在或当前平台不支持时返回 `nullptr`。Qt 6.11.1 文档列出的接口包括：

- `QNativeInterface::QAndroidScreen`
- `QNativeInterface::QCocoaScreen`
- `QNativeInterface::QWaylandScreen`
- `QNativeInterface::QWindowsScreen`

接口类型本身也受平台宏约束。跨平台源码应把对应类型和调用放入平台条件编译，并始终检查返回值：

```cpp
#if defined(Q_OS_WIN)
if (auto *native = screen->nativeInterface<QNativeInterface::QWindowsScreen>()) {
    HMONITOR monitor = native->handle();
    // 只在 Windows 平台适配层使用 monitor。
}
#endif
```

原生接口返回的指针或句柄由平台和 Qt 管理，应用不应释放它们，也不应跨线程长期保存。

### 10.9 属性通知信号

#### `[signal] void QScreen::geometryChanged(const QRect &geometry)`

屏幕完整几何变化时发出。`size` 属性也使用该通知信号；槽函数中需要同时读取位置和尺寸时应重新调用 `geometry()`。

#### `[signal] void QScreen::availableGeometryChanged(const QRect &geometry)`

可用工作区变化时发出，例如任务栏或窗口管理器保留区域变化。`availableSize` 属性也使用该通知信号。

#### `[signal] void QScreen::physicalSizeChanged(const QSizeF &size)`

平台报告的物理尺寸变化时发出。该值的单位是毫米，可能受显示器重新识别或平台信息更新影响。

#### `[signal] void QScreen::physicalDotsPerInchChanged(qreal dpi)`

物理 DPI 变化时发出。`physicalDotsPerInchX`、`physicalDotsPerInchY`、`physicalDotsPerInch` 以及 `devicePixelRatio` 属性使用这一通知信号。

#### `[signal] void QScreen::logicalDotsPerInchChanged(qreal dpi)`

逻辑 DPI 变化时发出。用户调整桌面缩放或字体 DPI 后，应重新计算依赖逻辑密度的 UI。

#### `[signal] void QScreen::virtualGeometryChanged(const QRect &rect)`

虚拟桌面几何变化时发出。`virtualGeometry`、`virtualSize`、`availableVirtualGeometry` 和 `availableVirtualSize` 都应在该信号后重新读取。

#### `[signal] void QScreen::primaryOrientationChanged(Qt::ScreenOrientation orientation)`

主方向变化时发出。需要按照设备主方向调整布局时连接该信号。

#### `[signal] void QScreen::orientationChanged(Qt::ScreenOrientation orientation)`

窗口系统当前方向变化时发出。它是 `orientation` 属性的通知信号。

#### `[signal] void QScreen::refreshRateChanged(qreal refreshRate)`

近似刷新率变化时发出。它适合更新诊断或显示信息，不改变使用 `QWindow::requestUpdate()` 驱动更新的原则。

## 11. 常见误区与排查顺序

### 11.1 自己构造 `QScreen`

`QScreen` 没有公开构造函数。若需要测试屏幕信息，应在业务层抽象出屏幕信息接口，或使用真实 `QGuiApplication` 下的屏幕对象；不要伪造 Qt 平台屏幕对象。

### 11.2 永久缓存 `primaryScreen()`

主屏幕可能改变，屏幕也可能被移除。启动时保存的 `QScreen *` 不能代表整个进程生命周期中的主屏幕。监听 `QGuiApplication` 的拓扑信号，并在需要时重新调用 `primaryScreen()`。

### 11.3 把 `size()` 当成全局位置

`size()` 只有宽高，屏幕在多屏布局中的位置由 `geometry()` 给出。需要放置窗口时必须使用完整的 `QRect`。

### 11.4 把 `availableGeometry()` 视为绝对可靠

X11 窗口管理器可能无法报告每个屏幕的真实可用区域。遇到窗口仍被任务栏遮挡时，先确认平台限制、窗口管理器配置和实际返回值。

### 11.5 把屏幕 DPR 用于已知窗口

同一屏幕上的窗口可能因为分数缩放或窗口属性拥有不同的设备像素比。已知目标窗口时读取 `QWindow::devicePixelRatio()`；屏幕 DPR 只用于没有窗口上下文的屏幕级估算。

### 11.6 把物理 DPI 当作 UI 缩放值

物理 DPI 反映显示器密度估计，逻辑 DPI 才是窗口系统用于 UI 和字体缩放的主要值。两者可能不同，也都可能受平台数据质量影响。

### 11.7 把 `virtualGeometry()` 的包围矩形当作全都可见

多个屏幕错位时，虚拟几何包围矩形中可能存在没有真实屏幕的空洞。需要判断一个点能否显示时调用 `virtualSiblingAt()`，不要只检查点是否在 `virtualGeometry()` 内。

### 11.8 用刷新率驱动定时器动画

刷新率是近似值，且显示系统可能采用可变刷新率。用定时器按这个数值循环容易产生抖动或额外功耗；窗口绘制应使用窗口系统的更新请求机制。

### 11.9 把 `grabWindow()` 当成离屏渲染

它抓取屏幕上的最终像素，可能包含覆盖窗口，不保证得到目标窗口自己的完整内容。若需要可控的窗口内容，应使用自己的绘制目标、`QImage` 或图形 API 的离屏资源。

### 11.10 无条件使用原生接口

`nativeInterface<T>()` 可能返回 `nullptr`，接口类型还可能只在特定平台上声明。应使用平台条件编译、空指针检查和适配层隔离，不要让业务逻辑依赖 `QPlatformScreen *`。

### 11.11 忽略信号中的重新读取

屏幕变化可能连续发生，例如拖动窗口、改变系统缩放或重新排列显示器。信号槽中应重新读取当前属性并更新缓存，不要只保存信号参数而假设其他相关属性同步完成且永远不再变化。

## 12. 相关类型的协作边界

- `QGuiApplication`：提供 `primaryScreen()`、`screens()` 以及屏幕加入和移除信号，是屏幕拓扑的入口。
- `QWindow`：提供窗口当前所在屏幕、窗口级 DPR、`screenChanged()` 和 `requestUpdate()`。窗口已知时优先使用窗口上下文。
- `QRect`、`QSize`、`QSizeF`：承载几何、尺寸和毫米物理尺寸，注意整数逻辑坐标与浮点物理尺寸的区别。
- `QTransform`：承载方向之间的连续坐标变换。
- `QPixmap`：接收 `grabWindow()` 的抓屏结果，并通过 `devicePixelRatio()` 表示高 DPI 像素密度。
- `QNativeInterface`：以较窄的模板接口暴露平台原生屏幕能力，但只应在平台适配边界使用。
- `QPlatformScreen`：QPA 层平台句柄，适合 Qt 平台插件或明确隔离的适配代码，不适合作为普通应用 API。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 生命周期 | `QScreen` 构造 | 由 Qt 平台集成层创建屏幕对象 | 构造函数私有，不能由应用自行创建 |
| 生命周期 | `~QScreen()` | 销毁屏幕对象 | 由 Qt 管理；不要对 `QGuiApplication` 返回的屏幕指针手动 `delete` |
| 属性 | `name : const QString` | 屏幕名称 | 描述性平台字符串，不保证是永久稳定 ID |
| 属性 | `manufacturer : const QString` | 制造商信息 | 可能为空，格式由平台决定 |
| 属性 | `model : const QString` | 型号信息 | 可能为空，不保证跨平台一致 |
| 属性 | `serialNumber : const QString` | 序列号 | 可能为空；使用前确认平台稳定性和隐私要求 |
| 属性 | `depth : const int` | 屏幕颜色深度 | 不是某个图像或纹理的通道位数 |
| 属性 | `size : QSize` | 屏幕尺寸 | 不包含虚拟桌面位置；通知信号是 `geometryChanged` |
| 属性 | `geometry : QRect` | 屏幕在虚拟桌面中的位置和尺寸 | 多屏时可能有负坐标 |
| 属性 | `availableSize : QSize` | 排除保留区后的可用尺寸 | 需要原点时用 `availableGeometry()`；通知信号是 `availableGeometryChanged` |
| 属性 | `availableGeometry : QRect` | 屏幕可用工作区 | X11 可能退化为完整几何 |
| 属性 | `virtualSize : QSize` | 同组屏幕虚拟桌面尺寸 | 不等于当前屏幕尺寸 |
| 属性 | `virtualGeometry : QRect` | 同组屏幕完整几何并集 | 包围矩形内可能有空洞 |
| 属性 | `availableVirtualSize : QSize` | 同组屏幕可用几何组合尺寸 | 不是统一扣除任务栏的简单结果 |
| 属性 | `availableVirtualGeometry : QRect` | 同组屏幕可用几何并集 | 使用 `virtualGeometryChanged` 通知 |
| 属性 | `physicalSize : QSizeF` | 屏幕物理尺寸，单位毫米 | 平台数据可能不准确 |
| 属性 | `physicalDotsPerInchX : qreal` | 水平物理 DPI | 设备无关点；需要设备密度时结合 DPR |
| 属性 | `physicalDotsPerInchY : qreal` | 垂直物理 DPI | 可能与 X 方向不同 |
| 属性 | `physicalDotsPerInch : qreal` | X/Y 物理 DPI 平均值 | 方便值，不提供额外测量精度 |
| 属性 | `logicalDotsPerInchX : qreal` | 水平逻辑 DPI | 可能受桌面设置影响 |
| 属性 | `logicalDotsPerInchY : qreal` | 垂直逻辑 DPI | 需要方向性尺寸时不要只取平均值 |
| 属性 | `logicalDotsPerInch : qreal` | X/Y 逻辑 DPI 平均值 | 用于一般 UI 和字体尺寸估算 |
| 属性 | `devicePixelRatio : qreal` | 屏幕物理像素与设备无关像素比例 | 已知窗口时优先用 `QWindow::devicePixelRatio()` |
| 属性 | `primaryOrientation : Qt::ScreenOrientation` | 当前主方向 | 平台和应用清单可能影响变化行为 |
| 属性 | `orientation : Qt::ScreenOrientation` | 窗口系统当前方向 | 移动设备自动旋转时可能改变 |
| 属性 | `nativeOrientation : Qt::ScreenOrientation` | 硬件原生方向 | 通常不变；不支持时可能是 `PrimaryOrientation` |
| 属性 | `refreshRate : qreal` | 近似垂直刷新率，单位 Hz | 不要用定时器按它驱动动画 |
| 成员函数 | `QString name() const` | 获取屏幕名称 | 可能是空或平台特定文本 |
| 成员函数 | `QString manufacturer() const` | 获取制造商 | 可能无法由平台提供 |
| 成员函数 | `QString model() const` | 获取型号 | 不应未经确认作为稳定 ID |
| 成员函数 | `QString serialNumber() const` | 获取序列号 | 可能为空或受平台权限限制 |
| 成员函数 | `int depth() const` | 获取颜色深度 | 不代表所有图像资源的位深 |
| 成员函数 | `QSize size() const` | 获取屏幕尺寸 | 只含尺寸，不含虚拟桌面位置 |
| 成员函数 | `QRect geometry() const` | 获取完整屏幕几何 | 多屏布局可能有负坐标 |
| 成员函数 | `QSize availableSize() const` | 获取可用尺寸 | 需要位置时使用可用几何 |
| 成员函数 | `QRect availableGeometry() const` | 获取可用工作区 | X11 上可能与完整几何相同 |
| 成员函数 | `QSize virtualSize() const` | 获取虚拟桌面尺寸 | 由 virtual siblings 共同决定 |
| 成员函数 | `QRect virtualGeometry() const` | 获取虚拟桌面几何 | 是并集包围矩形，不保证无空洞 |
| 成员函数 | `QSize availableVirtualSize() const` | 获取可用虚拟桌面尺寸 | 不等于简单缩小的完整虚拟桌面 |
| 成员函数 | `QRect availableVirtualGeometry() const` | 获取可用虚拟桌面几何 | 使用 `virtualGeometryChanged` 通知 |
| 成员函数 | `QList<QScreen *> virtualSiblings() const` | 获取同一虚拟桌面的屏幕 | 指针由 Qt 管理；屏幕移除后重新获取 |
| 成员函数 | `QScreen *virtualSiblingAt(QPoint point)` | 根据虚拟坐标查找屏幕 | 空洞或屏幕外返回 `nullptr` |
| 成员函数 | `QSizeF physicalSize() const` | 获取毫米物理尺寸 | 平台估计值可能不准确 |
| 成员函数 | `qreal physicalDotsPerInchX() const` | 获取水平物理 DPI | 与 DPR 和物理尺寸语义不同 |
| 成员函数 | `qreal physicalDotsPerInchY() const` | 获取垂直物理 DPI | 不要默认 X/Y 完全相同 |
| 成员函数 | `qreal physicalDotsPerInch() const` | 获取平均物理 DPI | 只是 X/Y 平均值 |
| 成员函数 | `qreal logicalDotsPerInchX() const` | 获取水平逻辑 DPI | 受窗口系统 UI 缩放设置影响 |
| 成员函数 | `qreal logicalDotsPerInchY() const` | 获取垂直逻辑 DPI | 方向性布局可分别使用 |
| 成员函数 | `qreal logicalDotsPerInch() const` | 获取平均逻辑 DPI | 一般 UI 估算值 |
| 成员函数 | `qreal devicePixelRatio() const` | 获取屏幕级 DPR | 已知目标窗口时应使用窗口 DPR |
| 成员函数 | `Qt::ScreenOrientation primaryOrientation() const` | 获取主方向 | 方向变化行为平台相关 |
| 成员函数 | `Qt::ScreenOrientation orientation() const` | 获取当前方向 | 是窗口系统视角，不是传感器读数 |
| 成员函数 | `Qt::ScreenOrientation nativeOrientation() const` | 获取硬件原生方向 | 硬件属性，通常固定 |
| 成员函数 | `qreal refreshRate() const` | 获取近似刷新率 | 诊断用途优先；动画用 `requestUpdate()` |
| 成员函数 | `int angleBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b) const` | 计算两个方向间旋转角 | 只返回 `0/90/180/270`；Primary 会解析 |
| 成员函数 | `QTransform transformBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &target) const` | 获取方向坐标变换 | 目标矩形决定平移和尺寸；不要只手动旋转 |
| 成员函数 | `QRect mapBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &rect) const` | 映射矩形方向 | 横纵方向转换时可能交换宽高 |
| 成员函数 | `bool isPortrait(Qt::ScreenOrientation o) const` | 判断是否纵向或反向纵向 | Primary 解析为主方向 |
| 成员函数 | `bool isLandscape(Qt::ScreenOrientation o) const` | 判断是否横向或反向横向 | Primary 解析为主方向 |
| 成员函数 | `QPixmap grabWindow(WId window = 0, int x = 0, int y = 0, int width = -1, int height = -1)` | 抓取屏幕或窗口像素 | 抓最终屏幕内容；高 DPI、权限和平台限制明显 |
| 成员函数 | `QPlatformScreen *handle() const` | 获取 QPA 平台句柄 | 可能破坏源/二进制兼容性，应隔离在平台适配层 |
| 成员函数 | `nativeInterface<T>() const` | 获取指定平台原生屏幕接口 | 不支持时返回 `nullptr`，类型需平台条件编译 |
| 信号 | `geometryChanged(const QRect &geometry)` | 通知完整几何变化 | `size` 属性也使用该通知 |
| 信号 | `availableGeometryChanged(const QRect &geometry)` | 通知可用工作区变化 | `availableSize` 属性也使用该通知 |
| 信号 | `physicalSizeChanged(const QSizeF &size)` | 通知物理尺寸变化 | 单位是毫米，平台数据可能更新 |
| 信号 | `physicalDotsPerInchChanged(qreal dpi)` | 通知物理 DPI 或 DPR 相关变化 | 物理 X/Y/平均值和屏幕 DPR 使用该通知 |
| 信号 | `logicalDotsPerInchChanged(qreal dpi)` | 通知逻辑 DPI 变化 | 系统缩放变化后重新计算 UI |
| 信号 | `virtualGeometryChanged(const QRect &rect)` | 通知虚拟桌面变化 | 四个 virtual/available virtual 属性都应重读 |
| 信号 | `primaryOrientationChanged(Qt::ScreenOrientation orientation)` | 通知主方向变化 | 适合重新布局方向相关内容 |
| 信号 | `orientationChanged(Qt::ScreenOrientation orientation)` | 通知当前方向变化 | `orientation` 属性的通知信号 |
| 信号 | `refreshRateChanged(qreal refreshRate)` | 通知近似刷新率变化 | 不改变窗口更新机制 |
| 应用拓扑 | `QGuiApplication::primaryScreen()` | 获取当前主屏幕 | 主屏幕可改变，不能永久缓存假设 |
| 应用拓扑 | `QGuiApplication::screens()` | 获取当前所有屏幕 | 屏幕集合变化后重新获取 |
| 应用拓扑 | `QGuiApplication::screenAdded(QScreen *)` | 通知新屏幕加入 | 在 GUI 线程更新屏幕模型 |
| 应用拓扑 | `QGuiApplication::screenRemoved(QScreen *)` | 通知屏幕移除 | 清理旧指针和依赖该屏幕的资源 |
| 相关非成员 | `operator<<(QDebug, const QScreen *)` | 将屏幕指针写入调试输出 | 输出格式不是稳定的数据交换格式；受调试流配置影响 |

---

### 一句话总结

`QScreen` 是 Qt 对已发现显示屏的运行时描述：用它查询屏幕几何、虚拟桌面、DPI、方向和刷新率，用 `QGuiApplication` 管理屏幕拓扑，用窗口级 DPR 处理具体窗口，并把 QPA 句柄、抓屏权限和平台差异隔离在适配边界内。
