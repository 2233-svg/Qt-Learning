# QIcon：按尺寸、交互模式和开关状态选择图像

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QIcon>`

## 它解决什么问题

界面中的“一个图标”通常不只是一张图片。同一图标可能需要：

- 16、24、32、64 等不同尺寸；
- 普通、禁用、悬停或选中外观；
- 开关控件的 On 与 Off 两套图形；
- 1x、2x、3x 等不同设备像素密度；
- 位图、SVG、系统主题或自定义图标引擎。

`QIcon` 把这些候选资源包装成一个隐式共享值对象。控件或绘制代码只需提出目标尺寸、`Mode` 和 `State`，内部 `QIconEngine` 决定使用哪份资源以及是否生成缺失外观。

它不是一张确定尺寸的位图。需要操作像素时使用 `QImage` 或 `QPixmap`；需要让按钮、动作和窗口根据状态获得合适图像时使用 `QIcon`。

## 实际使用场景

- 给 `QAction`、按钮、菜单项、标签页或窗口设置图标。
- 为禁用、选中和可切换状态提供独立美术资源。
- 从桌面图标主题或系统原生图标库取得符合平台习惯的图标。
- 用 SVG 或多分辨率位图适配高 DPI 屏幕。
- 通过 `QIconEngine` 实现程序化、动画式或第三方格式图标。
- 在自绘控件中按当前状态调用 `paint()`。

## 最常用的创建方式

固定资源图标：

```cpp
QIcon saveIcon(":/icons/save.svg");
action->setIcon(saveIcon);
```

系统主题图标并提供可靠回退：

```cpp
QIcon saveIcon = QIcon::fromTheme(
    QIcon::ThemeIcon::DocumentSave,
    QIcon(":/icons/save.svg"));
```

需要多个状态时：

```cpp
QIcon icon;
icon.addFile(":/icons/sync.svg", {}, QIcon::Normal, QIcon::Off);
icon.addFile(":/icons/sync-active.svg", {}, QIcon::Active, QIcon::Off);
icon.addFile(":/icons/sync-paused.svg", {}, QIcon::Normal, QIcon::On);
```

`Mode` 与 `State` 是两个维度。`Disabled` 不是 `Off`，`Active` 也不是 `On`。

## Mode 与 State

| 维度 | 取值 | 语义 |
| --- | --- | --- |
| `Mode` | `Normal` | 功能可用但用户没有正在交互 |
| `Mode` | `Disabled` | 功能当前不可用 |
| `Mode` | `Active` | 用户正在悬停、按压或以其他方式交互 |
| `Mode` | `Selected` | 图标代表的项目处于选中状态 |
| `State` | `On` | 可切换控件处于开启或选中状态 |
| `State` | `Off` | 可切换控件处于关闭状态，默认值 |

未提供精确组合时，图标引擎会尝试选择替代资源或生成效果。例如默认 pixmap 引擎可借助当前样式生成禁用外观。若品牌设计要求精确，显式提供对应模式的图片更可靠。

原生图标库和图标字体通常对 On 与 Off 使用同一个 glyph。需要明显的开关图形时，应由应用根据状态切换图标，或添加两套自有资源。

## 图标引擎由第一个来源决定

每个 `QIcon` 内部由一个 `QIconEngine` 处理资源。引擎类型由第一个加入的文件、pixmap、主题图标或自定义引擎决定，后续资源仍交给同一个引擎。

这会产生一个重要顺序规则：如果要使用 SVG 引擎，应先加入 SVG，再加入位图。

```cpp
QIcon icon;
icon.addFile(":/icons/tool.svg");
icon.addFile(":/icons/tool-32.png", QSize(32, 32));
```

反过来先加入 PNG，可能先选中默认 pixmap 引擎，使后来的 SVG 得不到可缩放引擎的处理。主题图标引擎和自定义引擎还可以忽略后续 `addFile()` 或 `addPixmap()`，所以不能假定任意来源都能混合。

构造 `QIcon(QIconEngine *engine)` 时，`QIcon` 接管该指针的所有权，调用方不得再删除或复用为另一个独立所有者。

## 位图、SVG 与尺寸选择

默认 pixmap 引擎会选择最合适的固定尺寸资源，必要时缩小，但不会把低分辨率图像放大。因此只提供 16x16 PNG 后请求 64x64，返回结果可能仍小于请求尺寸。

`actualSize(requested)` 返回引擎能提供的实际逻辑尺寸，结果不会大于请求值。`availableSizes()` 适合检查固定图像资源，但可缩放或主题引擎不一定能用一张有限列表表达能力，不能把空列表简单解释为图标不可绘制。

SVG 引擎可以按目标尺寸重新渲染矢量图，前提是 Qt SVG 支持可用且 SVG 是决定引擎的首个来源。

`addFile()` 延迟加载文件。相对路径按进程运行时工作目录解释，部署中更适合使用 Qt 资源路径或稳定的绝对数据目录。

## 高 DPI

自有位图可以使用 Qt 的 `@nx` 命名：

```text
open.png
open@2x.png
open@3x.png
```

`addFile("open.png")` 可自动发现高分辨率版本并设置对应 DPR。使用 `pixmap(size, devicePixelRatio, mode, state)` 时，`size` 是设备无关尺寸；从 Qt 6.8 起，传给图标引擎缩放接口的也是设备无关尺寸。

返回 pixmap 的 DPR 可能与请求值不同，这是允许的。判断屏幕上的逻辑大小应结合 `QPixmap::deviceIndependentSize()` 或 `size() / devicePixelRatio()`，不要把物理像素尺寸直接当布局尺寸。

## 主题图标查找链

`fromTheme()` 按以下顺序查找：

1. 当前主题 `themeName()`；
2. 回退主题 `fallbackThemeName()`；
3. `fallbackSearchPaths()` 中的独立图标文件；
4. 平台原生图标库；
5. 若调用了带 fallback 的重载，最后返回显式 fallback。

无显式主题时使用平台定义主题。Freedesktop 主题目录应位于 `themeSearchPaths()` 下，并包含 `index.theme`。所有平台还会把资源目录 `:/icons` 作为后备主题位置。

Qt 6.7 起，`ThemeIcon` 用强类型枚举表示常见语义图标，例如 `DocumentOpen`、`EditUndo`、`MediaPlaybackStart` 和 `DialogWarning`。它避免手写 Freedesktop 名称，但不保证每个平台库都提供每一项，应继续提供 fallback。

Qt 6.9 起，主题名也可以是已安装的图标字体 family，随后可按命名 glyph 调用字符串版 `fromTheme()`。Android 使用 Material 图标时需要系统存在相应字体，或把规定的字体资源打包进应用。

回退主题最好在构造 `QGuiApplication` 前设置，以保证平台初始化使用正确配置。主题和搜索路径是进程级全局状态，库代码不宜在不告知宿主应用的情况下随意修改。

## 空图标、坏文件与比较

`isNull()` 只判断图标是否没有 pixmap 和文件名。向图标加入一个非空文件名后，即使文件不存在或损坏，图标也会变成非空；它仍可能无法生成有效 pixmap。

因此资源校验不能只看 `isNull()`。对外部文件可先检查文件和解码结果，或取得目标 `pixmap()` 后检查其 `isNull()`。

`QIcon` 的 `operator==` 和 `operator!=` 被删除。图标资源、引擎与延迟生成规则使“视觉相等”没有简单定义。`cacheKey()` 用于缓存身份：共享相同内容的不同对象可以有相同 key，修改图标后 key 会变化，但它不是持久化 ID 或跨进程稳定标识。

## 复制、分离与线程

`QIcon` 隐式共享，复制构造和复制赋值通常很轻量。`detach()` 强制当前对象拥有独立数据，`isDetached()` 查询是否已独占；一般业务代码无需主动调用，修改操作会按需分离。

状态值可以方便地复制传递，但生成 `QPixmap`、调用 `paint()`、访问平台主题或原生图标库会触及 GUI 资源。应在已创建 `QGuiApplication` 的 GUI 线程完成这些操作，不要把 `QIcon` 当作工作线程中的通用像素渲染器。

## Mask 标志

`setIsMask(true)` 告诉平台该图标可作为遮罩处理。某些平台会按当前上下文重新着色，例如 macOS 菜单图标。它不是把彩色图片实际转换成二值 mask，也不保证所有平台都改变显示效果。

## 常见错误

- 把 `Mode::Disabled` 和 `State::Off` 当成同一个状态。
- 先加入 PNG 再加入 SVG，导致选择了不支持矢量重渲染的引擎。
- 只提供小位图，却期待默认引擎无损放大。
- 用 `isNull()` 验证文件是否真实存在和可解码。
- 在不同工作目录启动程序时仍依赖相对图片路径。
- 忽略返回 pixmap 的 DPR，把物理像素大小直接用于布局。
- 认为 `availableSizes()` 为空就不能绘制 SVG 或主题图标。
- 依赖主题图标一定存在，没有提供资源回退。
- 使用 `cacheKey()` 做跨进程数据库主键或视觉相等判断。
- 把同一个 `QIconEngine *` 同时交给多个所有者。
- 在工作线程调用需要 `QPixmap` 或平台主题的图标操作。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `Mode` | 交互可用性维度：`Normal`、`Disabled`、`Active`、`Selected`。 |
| 类型 | `State` | 开关维度：`On`、`Off`。 |
| 类型 | `ThemeIcon` | Qt 6.7 起的语义主题图标枚举；`NThemeIcons` 是计数哨兵，不是图标。 |
| 构造 | `QIcon() noexcept` | 构造空图标。 |
| 构造 | `QIcon(const QPixmap &pixmap)` | 以 pixmap 建立默认引擎和 Normal/Off 资源。 |
| 构造 | `explicit QIcon(const QString &fileName)` | 延迟加载文件或资源；相对路径基于运行时工作目录。 |
| 构造 | `explicit QIcon(QIconEngine *engine)` | 使用自定义引擎并接管指针所有权。 |
| 构造 | `QIcon(const QIcon &other)` | 隐式共享复制，开销小。 |
| 构造 | `QIcon(QIcon &&other) noexcept` | 移动内部数据，源对象保持可析构但内容不再保证。 |
| 析构 | `~QIcon()` | 释放共享状态；最后一个所有者会释放所拥有的图标引擎。 |
| 赋值 | `operator=(const QIcon &other)` | 隐式共享复制赋值。 |
| 赋值 | `operator=(QIcon &&other) noexcept` | 移动赋值。 |
| 交换 | `swap(QIcon &other) noexcept` | 常量时间交换内部状态。 |
| QVariant | `operator QVariant() const` | 将图标包装为 `QVariant`。 |
| 取图 | `pixmap(const QSize &size, Mode mode, State state) const` | 取得或生成目标逻辑尺寸的 pixmap；可能小于请求尺寸。 |
| 取图 | `pixmap(int w, int h, Mode mode, State state) const` | `QSize(w, h)` 便捷重载。 |
| 取图 | `pixmap(int extent, Mode mode, State state) const` | 请求正方形 pixmap。 |
| 取图 | `pixmap(const QSize &size, qreal dpr, Mode mode, State state) const` | Qt 6.0 起。按逻辑尺寸和目标 DPR 请求；返回 DPR 可以不同。 |
| 取图 | `pixmap(QWindow *, const QSize &, Mode, State) const` | Qt 6.0 已弃用；改用显式 DPR 重载。 |
| 尺寸 | `actualSize(const QSize &size, Mode mode, State state) const` | 返回可提供的设备无关尺寸，不大于请求值。 |
| 尺寸 | `actualSize(QWindow *, const QSize &, Mode, State) const` | Qt 6.0 已弃用；使用无窗口参数的重载。 |
| 绘制 | `paint(QPainter *painter, const QRect &rect, Qt::Alignment alignment, Mode mode, State state) const` | 在矩形内按对齐、模式和状态绘制；painter 必须有效且已激活。 |
| 绘制 | `paint(QPainter *, int x, int y, int w, int h, ...) const` | `QRect(x,y,w,h)` 的便捷重载。 |
| 添加 | `addPixmap(const QPixmap &pixmap, Mode mode, State state)` | 添加指定模式和状态资源；自定义或主题引擎可以忽略它。 |
| 添加 | `addFile(const QString &fileName, const QSize &size, Mode mode, State state)` | 延迟加入文件；首个来源决定引擎，非空坏路径也会使图标非空。 |
| 查询 | `availableSizes(Mode mode, State state) const` | 返回引擎报告的固定尺寸；空列表不必然表示不可缩放或不可绘制。 |
| 查询 | `isNull() const` | 是否没有 pixmap 和文件名；不验证资源能否成功加载。 |
| 查询 | `name() const` | 返回可用的创建名称，主题图标通常有值，普通文件图标未必有。 |
| 缓存 | `cacheKey() const` | 当前内容的缓存身份；修改后变化，不保证跨进程稳定。 |
| 共享 | `isDetached() const` | 是否独占内部共享数据；属于低层优化查询。 |
| 共享 | `detach()` | 强制分离共享数据；通常由修改操作自动完成。 |
| Mask | `setIsMask(bool isMask)` | 标记可由平台按上下文处理的遮罩图标，不执行格式转换。 |
| Mask | `isMask() const` | 返回 mask 标志。 |
| 主题 | `static fromTheme(const QString &name)` | 按主题、回退主题、独立路径和原生库查找；失败可返回空图标。 |
| 主题 | `static fromTheme(const QString &name, const QIcon &fallback)` | 查找失败时返回显式 fallback。 |
| 主题 | `static fromTheme(ThemeIcon icon)` | Qt 6.7 起，按语义枚举查找主题图标。 |
| 主题 | `static fromTheme(ThemeIcon icon, const QIcon &fallback)` | Qt 6.7 起，语义查找并提供显式回退。 |
| 主题 | `static hasThemeIcon(const QString &name)` | 是否能通过完整主题回退链找到名称。 |
| 主题 | `static hasThemeIcon(ThemeIcon icon)` | Qt 6.7 起，检查语义图标是否可用。 |
| 主题 | `static themeName()` | 返回当前主题名；未设置时由平台决定。 |
| 主题 | `static setThemeName(const QString &name)` | 设置全局主题；Qt 6.9 起也可指定提供命名 glyph 的字体 family。 |
| 路径 | `static themeSearchPaths()` | 返回主题目录列表，平台默认还包含资源后备位置。 |
| 路径 | `static setThemeSearchPaths(const QStringList &paths)` | 替换全局主题搜索路径；目录内容须遵守支持的主题格式。 |
| 回退 | `static fallbackThemeName()` | 返回回退主题名；未设置时可能由平台决定。 |
| 回退 | `static setFallbackThemeName(const QString &name)` | 设置回退主题，最好在构造 `QGuiApplication` 前调用。 |
| 回退 | `static fallbackSearchPaths()` | 返回独立图标文件搜索目录。 |
| 回退 | `static setFallbackSearchPaths(const QStringList &paths)` | 替换独立文件回退路径。 |
| 比较 | `operator==` / `operator!=` | 已删除，`QIcon` 不提供相等比较。 |
| 序列化 | `operator<<(QDataStream &, const QIcon &)` | 写入数据流；持久化时固定流版本，并确认自定义引擎支持。 |
| 序列化 | `operator>>(QDataStream &, QIcon &)` | 从数据流恢复图标。 |
| 调试 | `operator<<(QDebug, const QIcon &)` | 输出调试描述，不是稳定序列化格式。 |
| 内部接口 | `DataPtr` / `data_ptr()` | 暴露内部数据指针的兼容接口；普通应用代码不应依赖其布局或所有权。 |

## 相关类

- `QPixmap`：适合屏幕显示的固定像素图。
- `QImage`：适合像素处理、文件解码和跨线程图像数据。
- `QIconEngine`：尺寸和状态选择、生成与绘制的后端。
- `QIconEnginePlugin`：按文件后缀注册第三方图标引擎。
- `QAction`：菜单、工具栏等常用的图标消费者。

`QIcon` 的核心价值是延迟选择。应用提供候选资源和语义状态，真正的尺寸、DPR 与平台外观在使用时才由图标引擎决定。
