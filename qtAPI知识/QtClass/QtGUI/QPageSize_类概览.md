# QPageSize：纸张规格、单位换算与标准尺寸识别

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPageSize>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 相关类型：`QPageLayout`、`QPagedPaintDevice`、`QPrinter`、`QPdfWriter`

`QPageSize` 是一个值类型，用来描述一张纸的**尺寸、标准纸型标识、内部键和显示名称**。它不负责打印，也不保存页面方向和页边距；这些工作分别由 `QPagedPaintDevice` / `QPrinter` / `QPdfWriter` 与 `QPageLayout` 承担。

它实现了 Adobe PostScript PPD 4.3 的标准纸张集合，例如 `A4`、`Letter`、信封和工程图纸，并且也能保存任意自定义尺寸。纸张的定义顺序始终是“宽 x 高”，不隐含横向或纵向的页面方向。

## 它解决的问题

打印、导出 PDF 和排版经常要在几种表示间转换：

- 用户选中了 “A4” 或 “Letter”；
- 打印机驱动给出了一个 Windows `DMPAPER` 值；
- 业务系统保存的是毫米；
- 绘制设备需要点（point）或某个 DPI 下的像素尺寸；
- 自定义标签纸没有标准纸型。

若项目自己保存一组宽高数字，容易在单位、舍入、标准纸型匹配和显示名称上出现不一致。`QPageSize` 把这些规则集中起来：既可用标准 `PageSizeId` 创建，也可从任意单位的自定义尺寸创建，并可查询标准纸型的点、毫米、英寸和像素尺寸。

## 实际使用场景

### 1. 导出 A4 PDF

```cpp
#include <QPageLayout>
#include <QPageSize>
#include <QPdfWriter>

QPdfWriter writer("report.pdf");
QPageLayout layout(
    QPageSize(QPageSize::A4),
    QPageLayout::Portrait,
    QMarginsF(12, 12, 12, 12),
    QPageLayout::Millimeter);

writer.setPageLayout(layout);
```

`QPageSize(A4)` 只指定纸张规格；`QPageLayout::Portrait` 才指定纵向。需要横向时不要交换 `A4` 的宽高，而是把布局方向改为 `Landscape`。

### 2. 创建标签纸或热敏纸

```cpp
const QPageSize labelSize(
    QSizeF(100.0, 150.0),
    QPageSize::Millimeter,
    QStringLiteral("100 x 150 mm label"),
    QPageSize::ExactMatch);

if (!labelSize.isValid())
    return;
```

这里使用 `ExactMatch`，确保 100 x 150 mm 不会因为接近某个标准尺寸而被识别成标准纸型。自定义名称会成为 `name()` 的显示名称。

### 3. 按打印分辨率分配光栅画布

```cpp
const QPageSize page(QPageSize::Letter);
const int dpi = 300;
const QSize rasterSize = page.sizePixels(dpi);
```

`rasterSize` 可用于估算位图或离屏绘制所需像素数。它是按 DPI 换算后的整数尺寸，不能把它再当成精确物理尺寸反向保存。

## 核心模型与边界

### 标准尺寸、自定义尺寸与有效性

标准尺寸通过 `PageSizeId` 表示，例如 `A4`、`Letter`、`EnvelopeDL`。以这些枚举构造的对象带有 Qt 已知的定义尺寸和 PPD 键。

自定义尺寸应使用带 `QSize` 或 `QSizeF` 的构造函数。`QPageSize(QPageSize::Custom)` 本身不是一个可用的自定义纸张定义；它只是“没有对应标准纸型”这一分类值。无效枚举、负尺寸、无效 `QSize` / `QSizeF`，以及默认构造的对象都可能使 `isValid()` 返回 `false`。

### 纸张没有方向

`QPageSize` 的宽高按定义顺序保存，不能用 `width() < height()` 推断页面方向。`Ledger` 等标准纸张的定义本来就可能宽大于高。方向由 `QPageLayout` 的 `Orientation` 管理。

### 单位和舍入

- `Point` 是 PostScript point，即 `1/72` 英寸。
- 标准纸张内部保证点尺寸为整数；换算到毫米、英寸、pica、didot 或 cicero 时可能出现小数。
- `size(Unit)` 和 `rect(Unit)` 返回 `QSizeF` / `QRectF`，适合保留物理尺寸。
- `sizePoints()`、`sizePixels(dpi)` 及对应 `rect...()` 返回整数，涉及换算和舍入。
- 像素尺寸只在给定 DPI 后才有意义。不同打印机或导出分辨率会得到不同的 `sizePixels()`。

需要用于精确排版或数据保存时，优先保留 `definitionSize()` 和 `definitionUnits()`，而不是把一次换算得到的整数像素再换算回去。

### 尺寸匹配策略

用尺寸而非 `PageSizeId` 构造或调用静态 `id()` 时，Qt 可尝试识别标准纸张：

| 策略 | 语义 | 适用情况 |
| --- | --- | --- |
| `FuzzyMatch` | 默认策略；输入尺寸落在某标准纸张约 3 PostScript points 的容差内时，识别为该标准尺寸。方向也参与匹配。 | 用户输入、单位换算后的常规 A4/Letter。 |
| `FuzzyOrientationMatch` | 采用模糊匹配，但忽略宽高方向差异。 | 外部系统把横竖方向混在尺寸字段中，而业务只关心纸型。 |
| `ExactMatch` | 只有精确相等才识别标准尺寸。 | 自定义标签、固定票据，或必须避免“吸附”为标准尺寸的场景。 |

`FuzzyMatch` 的结果可能不等于传入的数值。得到 `PageSizeId` 后，若要参与后续计算，应重新调用 `size()` 或 `sizePoints()` 取得该标准纸张的实际尺寸。反过来，单位浮点换算常有微小误差，因此普通打印业务并不适合盲目使用 `ExactMatch`。

### 名称、键与平台映射

- `name()` 是面向用户的、本地化的显示名称。来自实际打印设备的纸张名称由驱动提供，可能不支持当前界面语言。
- `key()` 是 PPD `mediaOption` 或打印设备提供的内部键，适合设备协议或内部匹配，**不应直接显示给用户**。
- `windowsId()` 与 `id(int)` 用于 Windows `DMPAPER` 枚举映射。并非所有 PPD 纸型都有 Windows 对应项；无映射或对象无效时 `windowsId()` 返回 `0`，反向查找不到时 `id(int)` 返回 `Custom`。

### 比较语义

`operator==` / `operator!=` 比较当前全部属性，当前包括尺寸和名称。因此，同样是 210 x 297 mm、但自定义名称不同的两张纸可能不相等。

只关心实际尺寸是否相同，应使用 `isEquivalentTo()`；它忽略名称等其他属性。这一区别在“用户可改纸张名称”的配置系统里尤其重要。

### 生命周期与线程

`QPageSize` 是不依赖事件循环、窗口或打印作业的轻量值对象，可按值保存、传递和复制。它不拥有打印设备。

但若某个 `QPageSize` 是从 `QPrinter` 支持的纸张列表取得的，名称和键反映的是那台设备；不要把该设备专属键当成所有平台通用的持久化协议。与 `QPrinter`、窗口或绘制设备交互时，仍应遵守那些对象各自的线程亲和性与生命周期规则。

## 关键 API 语义

### 构造和标准识别

```cpp
QPageSize standard(QPageSize::A4);

QPageSize customPoints(
    QSize(595, 842), QStringLiteral("A4-like"), QPageSize::FuzzyMatch);

QPageSize customMillimeters(
    QSizeF(210.0, 297.0), QPageSize::Millimeter,
    QString(), QPageSize::FuzzyMatch);
```

后两个构造函数会根据匹配策略决定对象应保留为自定义尺寸，还是关联到某个标准 `PageSizeId`。若 `FuzzyMatch` 把输入识别为 A4，后续 `id()` 是 `A4`，而相关尺寸查询应以 Qt 的 A4 定义为准。

### 定义尺寸和请求单位的尺寸

```cpp
QPageSize page(QPageSize::Letter);

const QSizeF nativeDefinition = page.definitionSize();
const QPageSize::Unit nativeUnit = page.definitionUnits(); // Letter 通常为 Inch
const QSizeF millimeters = page.size(QPageSize::Millimeter);
const QSize points = page.sizePoints();
```

`definitionSize()` / `definitionUnits()` 回答“该纸张原本用什么单位定义”；`size(unit)` 回答“转换成请求单位后是多少”。对自定义尺寸，定义单位就是构造时传入的单位。

## 常见错误

### 把 `Custom` 当作“任意自定义纸张”

```cpp
QPageSize wrong(QPageSize::Custom); // 没有提供尺寸，通常是无效纸张
```

应改为带尺寸的构造函数，并在提交给打印或排版对象前检查 `isValid()`。

### 用 `key()` 填充纸张选择下拉框

`key()` 是机器键，既不保证本地化也不保证适合用户阅读。界面使用 `name()`，内部需要协议匹配时才保存 `key()`。

### 把 `FuzzyMatch` 返回的尺寸继续当作原尺寸

模糊匹配可能把 `209.5 x 297.2 mm` 识别为 A4。若后续要算绘制范围，应从返回的 ID 或对象重新读取 `size()`，而不是混用输入浮点数。

### 用 `operator==` 判断“是否同纸张大小”

比较尺寸时用 `isEquivalentTo()`；比较配置是否完全一致时才用 `==`。

## API 速查表

### 枚举与常量

| API | 说明 | 重点 |
| --- | --- | --- |
| `enum PageSizeId` | PPD 标准纸型标识，含 ISO A/B、ANSI、信封、工程纸和中国纸张等。 | 常用 `A4`、`Letter`、`Legal`、`Ledger`、`Tabloid`；`Custom` 表示不对应标准纸型，不是可直接使用的尺寸。 |
| `A0` 至 `A10` | ISO A 系列纸张。 | `A4` 是常用办公纸，定义为 210 x 297 mm。 |
| `B0` 至 `B10`、`JisB0` 至 `JisB10` | ISO B 与 JIS B 系列。 | 不同 B 系列不是同一标准，不能仅按名称推断尺寸。 |
| `Letter`、`Legal`、`Executive`、`Ledger`、`Tabloid` | 北美常用标准纸。 | `Ledger` 的定义可为横向宽高，不能据此推断 `QPageLayout` 的方向。 |
| `Envelope...`、`C5E`、`Comm10E`、`DLE` | 信封纸型；同时保留部分兼容别名。 | `EnvelopeC5 == C5E`、`EnvelopeDL == DLE`、`Envelope10 == Comm10E`。 |
| `AnsiA`、`AnsiB` | 一致性别名。 | 分别等于 `Letter`、`Ledger`。 |
| `LastPageSize` | 最后一个标准纸型枚举值。 | 适合枚举遍历的上界提示；不要把枚举连续性当作外部数据格式。 |
| `enum Unit` | 尺寸单位：`Millimeter`、`Point`、`Inch`、`Pica`、`Didot`、`Cicero`。 | `Point` 为 1/72 英寸；跨单位计算应保留浮点 `QSizeF`。 |
| `enum SizeMatchPolicy` | 从尺寸识别标准纸型的策略。 | 默认 `FuzzyMatch`；固定自定义纸用 `ExactMatch`；忽略宽高方向用 `FuzzyOrientationMatch`。 |

### 创建、复制和交换

| API | 说明 | 重点 |
| --- | --- | --- |
| `QPageSize()` | 创建无效纸张对象。 | 作为稍后赋值的占位可以；实际使用前检查 `isValid()`。 |
| `QPageSize(PageSizeId pageSizeId)` | 以标准纸型创建对象。 | 不要传 `Custom` 来创建自定义纸；传入无效 ID 时对象无效。 |
| `QPageSize(const QSize &pointSize, const QString &name = {}, SizeMatchPolicy policy = FuzzyMatch)` | 以整数 point 尺寸创建或识别纸型。 | `QSize` 的单位固定是 PostScript point。 |
| `QPageSize(const QSizeF &size, Unit units, const QString &name = {}, SizeMatchPolicy policy = FuzzyMatch)` | 以任意支持单位的浮点尺寸创建或识别纸型。 | 标签纸等固定规格通常选 `ExactMatch`。 |
| `QPageSize(const QPageSize &other)` | 复制值对象。 | 副本可独立作为配置值传递。 |
| `operator=(const QPageSize &other)` | 复制赋值。 | 用于替换当前纸张配置。 |
| `operator=(QPageSize &&other)` | 移动赋值。 | `noexcept`；普通业务代码通常无需显式调用。 |
| `swap(QPageSize &other)` | 快速交换两个纸张对象。 | `noexcept`；适合实现交换或高效调整容器中的值。 |
| `~QPageSize()` | 销毁值对象。 | 不关闭打印机，也不管理页面设备。 |

### 状态、身份和名称

| API | 说明 | 重点 |
| --- | --- | --- |
| `isValid() const` | 判断对象是否含有有效纸张定义。 | 默认构造、负尺寸、无效 ID 都可能返回 `false`。 |
| `id() const` | 返回标准 `PageSizeId`，自定义或无效时为 `Custom`。 | `Custom` 不能区分“有效自定义”与“无效对象”；先结合 `isValid()`。 |
| `key() const` | 返回对象的内部纸型键。 | 空对象返回空字符串；不可用于终端用户界面。 |
| `name() const` | 返回本地化的可读名称。 | 设备提供的名称可能不随当前 locale 翻译。 |
| `key(PageSizeId)` | 返回标准纸型的 PPD `mediaOption` 键。 | 适用于设备协议或内部匹配；无效 ID 返回空字符串。 |
| `name(PageSizeId)` | 返回标准纸型的本地化名称。 | 用于静态纸张选择列表的显示文本。 |
| `windowsId() const` | 返回此纸张对应的 Windows `DMPAPER` 值。 | 没有映射或对象无效时返回 `0`。 |
| `windowsId(PageSizeId)` | 返回标准纸型对应的 Windows `DMPAPER` 值。 | `0` 不代表某个可用纸型，应按“无映射”处理。 |
| `id(int windowsId)` | 从 Windows `DMPAPER` 值反查 `PageSizeId`。 | 无匹配时返回 `Custom`。 |

### 尺寸和矩形查询

| API | 说明 | 重点 |
| --- | --- | --- |
| `definitionSize() const` | 返回该对象的原始定义尺寸。 | 标准纸和自定义纸都保留自己的定义单位。 |
| `definitionUnits() const` | 返回该对象的原始定义单位。 | A4 通常是毫米，Letter 通常是英寸；无效对象返回无效单位。 |
| `definitionSize(PageSizeId)` | 查询标准纸型的原始定义尺寸。 | 与静态 `definitionUnits()` 配对使用。 |
| `definitionUnits(PageSizeId)` | 查询标准纸型的原始定义单位。 | 不能假设所有标准纸都由毫米定义。 |
| `size(Unit) const` | 把当前纸张换算为指定单位的 `QSizeF`。 | 适合物理尺寸计算；可能有浮点误差。 |
| `size(PageSizeId, Unit)` | 查询标准纸型在指定单位下的尺寸。 | 无需先构造对象。 |
| `sizePoints() const` | 返回当前纸张的整数 point 尺寸。 | point 是 1/72 英寸；换算结果是整数。 |
| `sizePoints(PageSizeId)` | 返回标准纸型的整数 point 尺寸。 | 适合 PDF/PostScript 坐标相关计算。 |
| `sizePixels(int dpi) const` | 返回指定分辨率下的整数设备像素尺寸。 | `dpi` 必须来自目标设备或导出设置；结果带舍入。 |
| `sizePixels(PageSizeId, int dpi)` | 返回标准纸型在指定 DPI 下的像素尺寸。 | 用于预分配光栅缓冲区或预估内存。 |
| `rect(Unit) const` | 返回原点为 `(0, 0)`、大小为 `size(unit)` 的 `QRectF`。 | 只描述整张纸，不扣除页边距。 |
| `rectPoints() const` | 返回 point 单位的整张纸矩形。 | 无效对象返回无效矩形。 |
| `rectPixels(int dpi) const` | 返回设备像素单位的整张纸矩形。 | 与 `sizePixels(dpi)` 使用同一 DPI。 |

### 识别、比较与辅助

| API | 说明 | 重点 |
| --- | --- | --- |
| `id(const QSize &pointSize, SizeMatchPolicy policy = FuzzyMatch)` | 从 point 尺寸识别标准纸型。 | 模糊匹配返回的标准实际尺寸可能与输入略不同。 |
| `id(const QSizeF &size, Unit units, SizeMatchPolicy policy = FuzzyMatch)` | 从任意单位的尺寸识别标准纸型。 | 得到 ID 后，重新取 `size()` 再做精确计算。 |
| `isEquivalentTo(const QPageSize &other) const` | 只比较实际尺寸是否相同。 | 忽略名称等属性；用来判断“物理纸张是否等价”。 |
| `operator==(lhs, rhs)` | 比较两个对象的完整属性。 | 当前包括尺寸与名称；不能替代 `isEquivalentTo()`。 |
| `operator!=(lhs, rhs)` | `operator==` 的否定。 | 用于配置变更检测。 |

## 与 QPageLayout 的分工

| 需求 | 应使用的类型 |
| --- | --- |
| 纸张的原始宽高、单位和标准纸型 | `QPageSize` |
| 纵向/横向、页边距、完整页面与可绘制页面矩形 | `QPageLayout` |
| 开始新页和设置页面布局 | `QPagedPaintDevice`、`QPrinter` 或 `QPdfWriter` |
| 设备实际支持的纸型集合 | 具体打印设备 / `QPrinter` 的能力查询 |

一句话记忆：`QPageSize` 管“这张纸是什么尺寸”，`QPageLayout` 管“如何在这张纸上排版”。
