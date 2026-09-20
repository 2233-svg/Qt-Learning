# QIconEngine：为 QIcon 提供渲染后端

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QIconEngine>`

## 它解决什么问题

`QIcon` 是面向使用者的图标值类型，`QIconEngine` 则是它的后端。每个 `QIcon` 都由一个引擎负责在指定的尺寸、`QIcon::Mode` 与 `QIcon::State` 下选择、生成和绘制图像。

Qt 自带的引擎能处理普通位图、SVG 和主题图标；当图标来自自定义文件格式、远程资源、程序化绘制或企业资源库时，才需要实现自己的 `QIconEngine`。

这个类是抽象接口，最少必须实现：

- `paint()`：真正把图标画到 `QPainter`；
- `clone()`：返回语义等价但独立的引擎副本。

它不是给普通应用层调用的“图标编辑器”。大多数程序只使用 `QIcon`；只有实现图标格式或绘制策略时才继承本类。

## 实际使用场景

- 为专有后缀实现矢量、动画或参数化图标引擎。
- 根据外部资源 ID、颜色主题和尺寸实时生成图标。
- 将图标存储在数据库、压缩包或受控资源服务中。
- 让自定义图标资源通过 `QIcon`、`QAction` 和各类控件透明使用。
- 配合 `QIconEnginePlugin` 按文件后缀动态加载引擎。

不适合用它做简单的“加载 PNG 后再显示”。那是 `QIcon`、`QPixmap`、`QImageReader` 已经覆盖的工作。

## 最小实现骨架

```cpp
#include <QIconEngine>
#include <QPainter>

class DotIconEngine final : public QIconEngine
{
public:
    QIconEngine *clone() const override
    {
        return new DotIconEngine(*this);
    }

    void paint(QPainter *painter, const QRect &rect,
               QIcon::Mode mode, QIcon::State state) override
    {
        Q_UNUSED(mode);
        const QColor color = state == QIcon::On ? Qt::green : Qt::gray;
        painter->setBrush(color);
        painter->setPen(Qt::NoPen);
        painter->drawEllipse(rect.adjusted(2, 2, -2, -2));
    }
};

QIcon icon(new DotIconEngine);
```

`QIcon` 接管传入引擎指针的所有权。调用 `new DotIconEngine` 后，调用方不得自行 `delete` 该对象，也不应把同一指针交给另一个 `QIcon`。

## `paint()` 是主契约

`paint(QPainter *, QRect, Mode, State)` 是纯虚函数。它应在给定矩形内绘制所请求状态的图标，并尊重传入的 painter 状态和坐标变换。

实现时通常遵守以下规则：

- 不结束由调用方开始的 `QPainter`；
- 保存并恢复自己修改的 pen、brush、transform、clip 等状态；
- 不假定目标一定是窗口，可能是 `QPixmap`、`QImage`、打印设备或其他 paint device；
- 依据 `mode`、`state` 选择资源或生成外观；
- 不缓存依赖当前 painter 的裸指针；
- 对空资源安全返回，不崩溃。

`pixmap()` 的默认实现会创建 pixmap 并调用 `paint()`。如果生成 pixmap 很昂贵，或可直接取得预渲染资源，可重写 `pixmap()` 以避免重复绘制。

## 克隆决定 QIcon 的复制是否可靠

`clone()` 是纯虚函数。它必须返回一个新的堆对象，表现与当前引擎一致，且后续对其中一个副本的修改不应意外影响另一个副本。

原因是 `QIcon` 是可复制、隐式共享的值类型；当图标需要分离时，Qt 依赖引擎克隆。只复制原指针、返回 `this`、或让多个可变引擎对象共享同一未管理状态，都会造成双重释放、跨图标串状态或悬空引用。

若内部持有共享缓存，缓存可以使用明确的共享所有权；但“图标配置状态”应能被 `clone()` 正确复制。受保护的复制构造函数可帮助派生类实现复制，赋值运算符被禁用。

## 尺寸、模式与状态

`actualSize()` 接收目标**设备无关尺寸**、Mode 和 State，返回该引擎能提供的实际设备无关尺寸。基类默认直接返回请求尺寸；固定位图引擎应重写它以报告真实可用尺寸。

`availableSizes()` 应返回指定 Mode/State 下引擎拥有的固定图像尺寸。可无限缩放的矢量引擎可以返回空列表，这不表示绘制失败，只表示没有有限离散尺寸集合。

`addPixmap()` 和 `addFile()` 是 `QIcon` 将附加资源交给引擎的入口。引擎必须明确自己是否支持它们：

- 位图引擎通常保存 pixmap 或文件名，并在需要时加载；
- 矢量、主题或程序化引擎可以忽略附加资源；
- 忽略时应保持一致、可预测，不能部分接受却在后续绘制时使用已失效引用。

`addFile()` 的 `size`、Mode、State 是资源的专门化标签；不表示 Qt 已经加载并验证文件。

## 高 DPI：`scaledPixmap()` 与 hook

`scaledPixmap(size, mode, state, scale)` 处理按缩放因子请求的 pixmap。`size` 是设备无关像素，`scale` 通常是目标设备 DPR。返回 pixmap 应具有与实际像素资源相符的 DPR，避免交给绘制阶段再做不必要缩放。

部分引擎会把 `scale` 转成整数，因此 1.25x、1.5x 等分数缩放必须在真实平台上测试。不能只在 1x 和 2x 屏幕验证。

为了不破坏二进制兼容性，Qt 还通过 `virtual_hook()` 提供两个标准扩展请求：

| Hook | `data` 指向 | 用途 |
| --- | --- | --- |
| `IsNullHook` | `bool *` | 引擎可将其设为 `true`，表明它代表空图标 |
| `ScaledPixmapHook` | `ScaledPixmapArgument *` | 输入目标 size/mode/state/scale，输出匹配的 `pixmap` |

不要把 `virtual_hook()` 当成通用 `void *` 回调。只解析自己明确支持的标准 `id`，并严格使用对应数据布局。未知 id 应安全忽略。

## `ScaledPixmapArgument`

这个结构体是 `ScaledPixmapHook` 的输入输出载体：

- `size`：请求的设备无关尺寸；
- `mode`：请求的 `QIcon::Mode`；
- `state`：请求的 `QIcon::State`；
- `scale`：请求缩放因子，通常等于 DPR；
- `pixmap`：由引擎写回的最佳匹配结果。

它尤其服务于 `QIcon::fromTheme()` 创建的主题图标：Freedesktop 主题可通过 `index.theme` 的目录 `Scale` 信息提供针对当前 DPR 的资源。其他来源通常仍按普通 `pixmap()` 路径工作，并受 `@nx` 高 DPI 文件支持。

## 名称、空状态与序列化

`key()` 返回标识引擎类型的字符串。它应稳定、可区分，尤其当引擎参与插件发现或数据流恢复时，不能依赖地址、随机数或当前语言。

`iconName()` 返回创建引擎时使用的名称（若有），用于让 `QIcon::name()` 报告主题或资源标识。它不是显示文字，也不保证所有引擎都能提供。

`isNull()` 判断该引擎是否代表空图标。若不重写，Qt 会经由 `virtual_hook(IsNullHook, ...)` 尝试查询，因而旧引擎或未实现 hook 的引擎可能无法提供准确结果。

`read()` 与 `write()` 用于 `QDataStream` 序列化引擎状态。基类默认都返回 `false`。实现它们时：

- 为自己的数据格式设置版本号；
- 验证长度、范围和流状态，不信任外部输入；
- 序列化可恢复的配置或资源引用，而不是无效的 GUI 句柄；
- 让 `read()` 失败后保持对象处于可析构且可识别的状态。

## 生命周期与线程边界

`QIconEngine` 通常由 `QIcon` 管理，插件创建的引擎最终也会由 `QIcon` 接管。引擎不要把 `QObject` 父子所有权和 `QIcon` 的裸指针所有权混在一起。

接口涉及 `QPixmap` 和 `QPainter`，因此渲染、pixmap 缓存和平台主题访问应视为 GUI 线程工作。若后台线程要准备资源，优先使用纯数据或 `QImage`，再把最终 `QPixmap` 创建、引擎更新和绘制安排到 GUI 线程。

## 常见错误

- 只实现 `paint()`，忘记实现纯虚的 `clone()`。
- `clone()` 返回 `this` 或浅复制独占资源。
- 在 `paint()` 中破坏调用方 painter 的状态。
- 将请求的逻辑尺寸误当作物理像素尺寸。
- 对分数 DPR 只做整数缩放。
- 让 `addFile()` 保存指向临时字符串、临时设备或已关闭资源的引用。
- 把 `availableSizes()` 空列表误作“不可渲染”，或为 SVG 虚构离散尺寸。
- 误用 `virtual_hook()` 的 `void *` 数据结构。
- 使用默认 `read()` / `write()`，却期待自定义引擎能随 `QIcon` 流化恢复。
- 在工作线程直接创建 `QPixmap` 或调用引擎绘制。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `IconEngineHook` | `virtual_hook()` 的标准扩展请求：`IsNullHook` 与 `ScaledPixmapHook`。 |
| 类型 | `ScaledPixmapArgument` | `ScaledPixmapHook` 的输入输出结构，保存 size、mode、state、scale 与输出 pixmap。 |
| 构造 | `QIconEngine()` | 构造引擎基类状态；派生类仍必须实现 `paint()` 与 `clone()`。 |
| 构造 | `QIconEngine(const QIconEngine &other)` | 受保护复制构造，供派生类在 `clone()` 中复制基类状态。 |
| 析构 | `virtual ~QIconEngine()` | 虚析构；通常由拥有它的 `QIcon` 删除。 |
| 绘制 | `virtual void paint(QPainter *, const QRect &, QIcon::Mode, QIcon::State) = 0` | 必须实现的主渲染契约；在给定矩形中按状态绘制。 |
| 图像 | `virtual QPixmap pixmap(const QSize &, QIcon::Mode, QIcon::State)` | 返回目标 pixmap；默认通过 `paint()` 生成。 |
| 尺寸 | `virtual QSize actualSize(const QSize &, QIcon::Mode, QIcon::State)` | 返回实际设备无关尺寸；默认返回请求尺寸。 |
| 资源 | `virtual void addPixmap(const QPixmap &, QIcon::Mode, QIcon::State)` | 接收 `QIcon::addPixmap()` 的附加资源；可重写，某些引擎可选择忽略。 |
| 资源 | `virtual void addFile(const QString &, const QSize &, QIcon::Mode, QIcon::State)` | 接收 `QIcon::addFile()` 的文件资源；可延迟加载，或由不适用的引擎忽略。 |
| 查询 | `virtual QList<QSize> availableSizes(QIcon::Mode, QIcon::State)` | 返回该状态下已包含的离散尺寸；矢量引擎可为空。 |
| 复制 | `virtual QIconEngine *clone() const = 0` | 必须返回独立、堆分配且语义等价的副本；所有权交给调用方。 |
| 标识 | `virtual QString key() const` | 返回稳定的引擎类型标识。 |
| 标识 | `virtual QString iconName()` | 返回创建名称（若有），供 `QIcon::name()` 使用。 |
| 空状态 | `virtual bool isNull()` | 是否表示空图标；未重写时依赖 hook 查询，兼容性可能不足。 |
| 缩放 | `virtual QPixmap scaledPixmap(const QSize &, QIcon::Mode, QIcon::State, qreal scale)` | 按目标 DPR 返回 pixmap；size 为设备无关尺寸。 |
| ABI 扩展 | `virtual void virtual_hook(int id, void *data)` | 处理标准 hook，必须依据 id 使用准确数据结构并忽略未知 id。 |
| 序列化 | `virtual bool read(QDataStream &in)` | 从流恢复引擎；基类默认 `false`。 |
| 序列化 | `virtual bool write(QDataStream &out) const` | 写入引擎状态；基类默认 `false`。 |
| 赋值 | `operator=(const QIconEngine &)` | 被删除；不支持基类赋值。 |

## 相关类

- `QIcon`：拥有并调用图标引擎。
- `QIconEnginePlugin`：将自定义引擎注册为可动态加载的插件。
- `QIconEngine::ScaledPixmapArgument`：高 DPI hook 的参数结构。
- `QPainter`、`QPixmap`：引擎绘制和返回图像所依赖的 GUI 类型。

实现 `QIconEngine` 的本质，是把“图标资源”变成遵守 Qt 值语义、状态选择和高 DPI 规则的渲染服务，而不只是写一个能画图的函数。
