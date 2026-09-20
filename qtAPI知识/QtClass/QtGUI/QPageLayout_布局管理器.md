# QPageLayout：页面尺寸、方向、边距与可绘制区域

> 适用版本：Qt 6.11.1
> 头文件：`#include <QPageLayout>`
> 所属模块：`Qt6::Gui`
> 继承：无，隐式共享值类型

## 它解决什么问题

`QPageLayout` 描述一页纸的几何规则：纸张尺寸、纵横向、边距、最小可打印边距、单位以及“是否按整页绘制”。`QPdfWriter`、`QPrinter` 和分页排版代码会用它把 A4、Letter、横向、15 mm 边距这类业务设定转换成可供 `QPainter` 使用的页面矩形。

它不是窗口布局管理器，也不会摆放 QWidget。它服务的是打印、PDF、报表、文档导出、标签纸和分页预览这些“纸面布局”场景。

## 实际使用场景

- 生成 PDF 前统一设置 A4/Letter、Portrait/Landscape 和页边距。
- 打印前把内容限制在打印机可打印区域内。
- 报表引擎按 `paintRect()` 计算正文区域，按 `fullRect()` 绘制出血背景。
- 在不同单位、DPI 和设备之间换算点、毫米、英寸和像素矩形。
- 比较两份页面设置是否实际等价，而不纠结内部 ID 或单位细节。

## 核心使用模型

先用 `QPageSize` 表示纸张，再给 `QPageLayout` 设置方向和边距。`QPageSize` 自身总是以 Portrait 语义描述纸张尺寸；方向变化不会改写 `pageSize()` 的定义，而是体现在 `fullRect()`、`paintRect()` 等结果中。

`fullRect()` 是整张纸的外框；`paintRect()` 是扣除边距后的内容区域。大多数文档正文应排进 `paintRect()`。只有背景、裁切线、出血或自行控制边距的场景，才直接使用 `fullRect()`。

单位是布局对象状态的一部分。`margins()`、`fullRect()`、`paintRect()` 默认返回当前单位；`*Points()` 固定返回 1/72 英寸点；`*Pixels(resolution)` 按给定 DPI 换算为整数像素。缓存像素矩形时必须同时缓存 DPI。

## 模式与边距策略

`StandardMode` 是普通打印/PDF 模式：`paintRect()` 会扣除边距，边距还要满足 `minimumMargins()` 和 `maximumMargins()`。最小边距通常来自物理打印机的不可打印区域；把它强行设成 0 不会让实体打印机突破硬件限制，只可能导致内容被裁掉。

`FullPageMode` 表示由调用方自行处理边距：`paintRect()` 等于 `fullRect()`。它适合整页背景、出血、裁切线或专业排版流程，但也意味着你不能再指望 `QPageLayout` 帮你避开打印机不可打印边缘。

Qt 6.8 起，`setMargins()` 和四个单边 setter 支持 `OutOfBoundsPolicy`：

- `Reject`：边距越界时拒绝修改并返回 `false`。
- `Clamp`：把边距夹到合法范围内，并返回修改结果。

当页面尺寸或最小边距变化时，`StandardMode` 会让现有边距服从新的合法范围；`FullPageMode` 下边距仍保留，是否使用由调用方决定。

## 等价与严格相等

`operator==` 比较对象内部状态，适合判断“设置是否完全相同”。如果只关心最终排版效果，比如纸张实际尺寸、方向和边距是否一致，用 `isEquivalentTo()` 更符合业务语义。

这个区别在配置迁移、打印机默认值和单位换算中很重要：两个布局可能内部来源不同，但最终画出来的页面区域一致。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPageLayout()` | 创建无效或未完整配置的页面布局。 | 使用前通常要设置 page size、orientation 和 margins，并检查 `isValid()`。 |
| 构造 | `QPageLayout(const QPageSize &, Orientation, const QMarginsF &, Unit, const QMarginsF &minMargins)` | 一次性指定纸张、方向、边距、单位和最小边距。 | `pageSize` 按 Portrait 定义；横向效果体现在矩形查询中。 |
| 拷贝 | `QPageLayout(const QPageLayout &)` / `operator=` / `swap()` | 拷贝或交换值类型状态。 | 隐式共享，适合作为配置值传递。 |
| 有效性 | `bool isValid() const` | 判断页面尺寸和布局状态是否可用。 | 交给 PDF/打印设备前先检查，避免空页面几何。 |
| 模式 | `void setMode(Mode)` / `Mode mode() const` | 设置或查询 `StandardMode`、`FullPageMode`。 | `StandardMode` 扣边距；`FullPageMode` 让 `paintRect()` 等于整页。 |
| 纸张 | `void setPageSize(const QPageSize &, const QMarginsF &minMargins = {})` | 更换纸张并可同时更新最小边距。 | `StandardMode` 下既有边距可能被裁剪到新合法范围。 |
| 纸张 | `QPageSize pageSize() const` | 返回纸张定义。 | 它本身不随 Landscape 变成横向尺寸。 |
| 方向 | `void setOrientation(Orientation)` / `Orientation orientation() const` | 设置或读取纵横向。 | 不改写 `QPageSize`，但影响 `fullRect()` 和 `paintRect()`。 |
| 单位 | `void setUnits(Unit)` / `Unit units() const` | 设置默认几何单位。 | 影响无单位参数的矩形和边距查询结果。 |
| 边距 | `bool setMargins(const QMarginsF &, OutOfBoundsPolicy = Reject)` | 设置四边页边距。 | 返回 false 表示 Reject 策略下越界未改。 |
| 边距 | `setLeftMargin()` / `setRightMargin()` / `setTopMargin()` / `setBottomMargin()` | 单独设置某一边边距。 | Qt 6.8 起同样支持 Reject/Clamp 策略。 |
| 边距 | `QMarginsF margins() const` / `margins(Unit) const` | 查询当前边距。 | 无参数版本使用布局当前单位。 |
| 边距像素 | `QMargins marginsPoints() const` | 以 point 返回整数边距。 | 适合 PDF/PostScript 传统 72 DPI 坐标。 |
| 边距像素 | `QMargins marginsPixels(int resolution) const` | 按 DPI 转为像素边距。 | DPI 是调用方输入；换设备时必须重新计算。 |
| 最小边距 | `void setMinimumMargins(const QMarginsF &)` | 设置设备或业务要求的最小边距。 | 对实体打印机通常来自不可打印区域。 |
| 最小边距 | `QMarginsF minimumMargins() const` | 查询最小允许边距。 | 用于设置面板显示下限。 |
| 最大边距 | `QMarginsF maximumMargins() const` | 查询最大允许边距。 | 由纸张尺寸和最小可用区域推导。 |
| 整页矩形 | `QRectF fullRect() const` / `fullRect(Unit) const` | 返回整张纸外框。 | 考虑方向，不扣边距。 |
| 整页矩形 | `QRect fullRectPoints() const` | 返回 point 单位整页矩形。 | 结果是整数，存在取整。 |
| 整页矩形 | `QRect fullRectPixels(int resolution) const` | 返回指定 DPI 下整页像素矩形。 | 适合光栅预览和打印位图排版。 |
| 可绘制矩形 | `QRectF paintRect() const` / `paintRect(Unit) const` | 返回正文可绘制区域。 | `StandardMode` 扣边距；`FullPageMode` 等于整页。 |
| 可绘制矩形 | `QRect paintRectPoints() const` | 返回 point 单位正文区域。 | PDF 排版常用。 |
| 可绘制矩形 | `QRect paintRectPixels(int resolution) const` | 返回指定 DPI 下正文像素区域。 | 高 DPI 输出要传入目标设备 DPI。 |
| 等价比较 | `bool isEquivalentTo(const QPageLayout &other) const` | 判断最终页面几何是否等价。 | 比 `operator==` 更适合业务比较。 |
| 严格比较 | `operator==` / `operator!=` | 比较布局状态是否完全相同。 | 单位、页面定义来源等差异也可能影响结果。 |
| 调试 | `operator<<(QDebug, const QPageLayout &)` | 输出布局调试信息。 | 只用于诊断，不是持久化格式。 |
| 枚举 | `Unit` | 表示 `Millimeter`、`Point`、`Inch`、`Pica`、`Didot`、`Cicero`。 | 与 `QPageSize::Unit`、`QPrinter::Unit` 保持同步语义。 |
| 枚举 | `Orientation` | 表示 `Portrait` 或 `Landscape`。 | 影响矩形方向，不改变 `QPageSize` 的定义方式。 |
| 枚举 | `Mode` | 表示 `StandardMode` 或 `FullPageMode`。 | 决定 `paintRect()` 是否扣除边距。 |
| 枚举 | `OutOfBoundsPolicy` | 表示越界边距的处理方式。 | `Reject` 保守，`Clamp` 适合设置面板即时校正。 |

## 一句话总结

`QPageLayout` 是纸面几何配置：先决定纸张和方向，再决定边距和模式，最后用 `paintRect()` 而不是想当然的整页尺寸去排版内容。
