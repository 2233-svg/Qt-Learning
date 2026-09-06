# QPageSize

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPageSize` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPageSize>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum PageSizeId { A0, A1, A2, A3, A4, …, LastPageSize }`
- `enum SizeMatchPolicy { FuzzyMatch, FuzzyOrientationMatch, ExactMatch }`
- `enum Unit { Millimeter, Point, Inch, Pica, Didot, Cicero }`

### 公有函数

- `QPageSize()`
- `QPageSize(QPageSize::PageSizeId pageSize)`
- `QPageSize(const QSize &pointSize, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QPageSize(const QSizeF &size, QPageSize::Unit units, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QPageSize(const QPageSize &other)`
- `~QPageSize()`
- `QSizeF definitionSize() const`
- `QPageSize::Unit definitionUnits() const`
- `QPageSize::PageSizeId id() const`
- `bool isEquivalentTo(const QPageSize &other) const`
- `bool isValid() const`
- `QString key() const`
- `QString name() const`
- `QRectF rect(QPageSize::Unit units) const`
- `QRect rectPixels(int resolution) const`
- `QRect rectPoints() const`
- `QSizeF size(QPageSize::Unit units) const`
- `QSize sizePixels(int resolution) const`
- `QSize sizePoints() const`
- `void swap(QPageSize &other)`
- `int windowsId() const`
- `QPageSize & operator=(QPageSize &&other)`
- `QPageSize & operator=(const QPageSize &other)`

### 静态公有成员

- `QSizeF definitionSize(QPageSize::PageSizeId pageSizeId)`
- `QPageSize::Unit definitionUnits(QPageSize::PageSizeId pageSizeId)`
- `QPageSize::PageSizeId id(int windowsId)`
- `QPageSize::PageSizeId id(const QSize &pointSize, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QPageSize::PageSizeId id(const QSizeF &size, QPageSize::Unit units, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QString key(QPageSize::PageSizeId pageSizeId)`
- `QString name(QPageSize::PageSizeId pageSizeId)`
- `QSizeF size(QPageSize::PageSizeId pageSizeId, QPageSize::Unit units)`
- `QSize sizePixels(QPageSize::PageSizeId pageSizeId, int resolution)`
- `QSize sizePoints(QPageSize::PageSizeId pageSizeId)`
- `int windowsId(QPageSize::PageSizeId pageSizeId)`

### 相关非成员函数

- `bool operator!=(const QPageSize &lhs, const QPageSize &rhs)`
- `bool operator==(const QPageSize &lhs, const QPageSize &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPageSize::PageSizeId`

**作用与语义：**

该枚举类型列出了Postscript PPD标准中定义的可用页面大小。这些值在`QPagedPaintDevice`和 `QPrinter`中被复制。
定义的尺寸如下：
- `QPageSize::A0`：`3`;841 x 1189 毫米
- `QPageSize::A1`：`4`;594 x 841毫米
- `QPageSize::A2`：`5`;420 x 594 毫米
- `QPageSize::A3`：`6`;297 x 420毫米
- `QPageSize::A4`：`7`;210 x 297 毫米，8.26 x 11.69 英寸
- `QPageSize::A5`：`8`;148 x 210毫米
- `QPageSize::A6`：`9`;105 x 148毫米
- `QPageSize::A7`：`10`;74 x 105毫米
- `QPageSize::A8`：`11`;52 x 74毫米
- `QPageSize::A9`：`12`;37 x 52毫米
- `QPageSize::B0`：`14`;1000 x 1414毫米
- `QPageSize::B1`：`15`;707 x 1000毫米
- `QPageSize::B2`：`16`;500 x 707毫米
- `QPageSize::B3`：`17`;353 x 500 毫米
- `QPageSize::B4`：`18`;250 x 353毫米
- `QPageSize::B5`：`19`;176 x 250 毫米，6.93 x 9.84 英寸
- `QPageSize::B6`：`20`;125 x 176毫米
- `QPageSize::B7`：`21`;88 x 125毫米
- `QPageSize::B8`：`22`;62 x 88毫米
- `QPageSize::B9`：`23`;44 x 62毫米
- `QPageSize::B10`：`24`;31 x 44毫米
- `QPageSize::C5E`：`25`;163 x 229毫米
- `QPageSize::Comm10E`：`26`;105 x 241毫米，美国通用10毫米信封
- `QPageSize::DLE`：`27`;110 x 220毫米
- `QPageSize::Executive`：`2`;7.5 x 10英寸，190.5 x 254毫米
- `QPageSize::Folio`：`28`;210 x 330 毫米
- `QPageSize::Ledger`：`29`;431.8 x 279.4 毫米
- `QPageSize::Legal`：`1`;8.5 x 14英寸，215.9 x 355.6毫米
- `QPageSize::Letter`：`0`;8.5 x 11英寸，215.9 x 279.4毫米
- `QPageSize::Tabloid`：`30`;279.4 x 431.8 毫米
- `QPageSize::Custom`：`31`;未知，或用户自定义大小。
- `QPageSize::A10`：`13`
- `QPageSize::A3Extra`：`32`
- `QPageSize::A4Extra`：`33`
- `QPageSize::A4Plus`：`34`
- `QPageSize::A4Small`：`35`
- `QPageSize::A5Extra`：`36`
- `QPageSize::B5Extra`：`37`
- `QPageSize::JisB0`：`38`
- `QPageSize::JisB1`：`39`
- `QPageSize::JisB2`：`40`
- `QPageSize::JisB3`：`41`
- `QPageSize::JisB4`：`42`
- `QPageSize::JisB5`：`43`
- `QPageSize::JisB6`：`44`;,
- `QPageSize::JisB7`：`45`
- `QPageSize::JisB8`：`46`
- `QPageSize::JisB9`：`47`
- `QPageSize::JisB10`：`48`
- `QPageSize::AnsiA`：`Letter`;= 信件
- `QPageSize::AnsiB`：`Ledger`;= 账本
- `QPageSize::AnsiC`：`49`
- `QPageSize::AnsiD`：`50`
- `QPageSize::AnsiE`：`51`
- `QPageSize::LegalExtra`：`52`
- `QPageSize::LetterExtra`：`53`
- `QPageSize::LetterPlus`：`54`
- `QPageSize::LetterSmall`：`55`
- `QPageSize::TabloidExtra`：`56`
- `QPageSize::ArchA`：`57`
- `QPageSize::ArchB`：`58`
- `QPageSize::ArchC`：`59`
- `QPageSize::ArchD`：`60`
- `QPageSize::ArchE`：`61`
- `QPageSize::Imperial7x9`：`62`
- `QPageSize::Imperial8x10`：`63`
- `QPageSize::Imperial9x11`：`64`
- `QPageSize::Imperial9x12`：`65`
- `QPageSize::Imperial10x11`：`66`
- `QPageSize::Imperial10x13`：`67`
- `QPageSize::Imperial10x14`：`68`
- `QPageSize::Imperial12x11`：`69`
- `QPageSize::Imperial15x11`：`70`
- `QPageSize::ExecutiveStandard`：`71`
- `QPageSize::Note`：`72`
- `QPageSize::Quarto`：`73`
- `QPageSize::Statement`：`74`
- `QPageSize::SuperA`：`75`
- `QPageSize::SuperB`：`76`
- `QPageSize::Postcard`：`77`
- `QPageSize::DoublePostcard`：`78`
- `QPageSize::Prc16K`：`79`
- `QPageSize::Prc32K`：`80`
- `QPageSize::Prc32KBig`：`81`
- `QPageSize::FanFoldUS`：`82`
- `QPageSize::FanFoldGerman`：`83`
- `QPageSize::FanFoldGermanLegal`：`84`
- `QPageSize::EnvelopeB4`：`85`
- `QPageSize::EnvelopeB5`：`86`
- `QPageSize::EnvelopeB6`：`87`
- `QPageSize::EnvelopeC0`：`88`
- `QPageSize::EnvelopeC1`：`89`
- `QPageSize::EnvelopeC2`：`90`
- `QPageSize::EnvelopeC3`：`91`
- `QPageSize::EnvelopeC4`：`92`
- `QPageSize::EnvelopeC5`：`C5E`;= C5E
- `QPageSize::EnvelopeC6`：`93`
- `QPageSize::EnvelopeC65`：`94`
- `QPageSize::EnvelopeC7`：`95`
- `QPageSize::EnvelopeDL`：`DLE`;= DLE
- `QPageSize::Envelope9`：`96`
- `QPageSize::Envelope10`：`Comm10E`;= Comm10E
- `QPageSize::Envelope11`：`97`
- `QPageSize::Envelope12`：`98`
- `QPageSize::Envelope14`：`99`
- `QPageSize::EnvelopeMonarch`：`100`
- `QPageSize::EnvelopePersonal`：`101`
- `QPageSize::EnvelopeChou3`：`102`
- `QPageSize::EnvelopeChou4`：`103`
- `QPageSize::EnvelopeInvite`：`104`
- `QPageSize::EnvelopeItalian`：`105`
- `QPageSize::EnvelopeKaku2`：`106`
- `QPageSize::EnvelopeKaku3`：`107`
- `QPageSize::EnvelopePrc1`：`108`
- `QPageSize::EnvelopePrc2`：`109`
- `QPageSize::EnvelopePrc3`：`110`
- `QPageSize::EnvelopePrc4`：`111`
- `QPageSize::EnvelopePrc5`：`112`
- `QPageSize::EnvelopePrc6`：`113`
- `QPageSize::EnvelopePrc7`：`114`
- `QPageSize::EnvelopePrc8`：`115`
- `QPageSize::EnvelopePrc9`：`116`
- `QPageSize::EnvelopePrc10`：`117`
- `QPageSize::EnvelopeYou4`：`118`
- `QPageSize::LastPageSize`：`EnvelopeYou4`;= 信封You4
由于历史原因，QPageSize：：Executive 与标准的 Postscript 和 Windows 执行尺寸不同，请使用 QPageSize：：ExecutiveStandard 代替。
Postscript 标准大小 QPageSize：：Folio 与 Windows DMPAPER_FOLIO 大小不同，如有需要，使用 Postscript 标准大小的 QPageSize：：FanFoldGermanLegal。

### `enum QPageSize::Unit`

**作用与语义：**

该枚举类型用于指定页面大小的测量单位。
- `QPageSize::Millimeter`：`0`
- `QPageSize::Point`：`1`;1/72英寸
- `QPageSize::Inch`：`2`
- `QPageSize::Pica`：`3`;1/72英尺，1/6英寸，12点
- `QPageSize::Didot`：`4`;1/72法式英寸，0.375毫米
- `QPageSize::Cicero`：`5`;1/6法式英寸，12迪多特，4.5毫米

### `QPageSize::QPageSize()`

**作用与语义：**

创建空 QPageSize。

### `QPageSize::QPageSize(QPageSize::PageSizeId pageSize)`

**作用与语义：**

创建标准`pageSize`的QPageSize。
如果`pageSize` `QPageSize::Custom`，那么生成的 QPageSize 就无效。请使用自定义大小构造器。

### `[explicit] QPageSize::QPageSize(const QSize &pointSize, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**作用与语义：**

利用匹配的 `matchPolicy` 创建给定`pointSize`的 QPageSize （点数）。
如果给定`pointSize`与标准`QPageSize::PageSizeId`相符，则使用该页面尺寸。注意，如果`matchPolicy` `FuzzyMatch`，可能会导致`pointSize`调整为标准尺寸。为避免这种情况，建议使用`ExactMatch` `matchPolicy`。
如果给定的`pointSize`不是标准`QPageSize::PageSizeId`，则会创建一个`QPageSize::Custom`尺寸。
如果`name`为空，则使用标准的本地化名称。如果是自定义页面大小，则会创建格式为“Custom （宽度 x 高度）”的自定义名称。
`matchPolicy`默认是`FuzzyMatch`。

### `[explicit] QPageSize::QPageSize(const QSizeF &size, QPageSize::Unit units, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**作用与语义：**

在`units`中创建该`size`的自定义页面。
如果给定的`size`与标准`QPageSize::PageSizeId`相符，则使用该页面大小。注意，如果`matchPolicy` `FuzzyMatch`，可能会导致`size`调整为标准尺寸。为防止这种情况，建议使用一个`ExactMatch`的`matchPolicy`。
如果给定的`size`不是标准`QPageSize::PageSizeId`，则会创建一个`QPageSize::Custom`尺寸。原始单位大小将被保留，并作为所有其他单位大小计算的基础。
如果`name`为空，则会创建一个自定义名称，格式为“Custom （宽度 x 高度）”，其中尺寸以单位表示。

### `QPageSize::QPageSize(const QPageSize &other)`

**作用与语义：**

复制构造器，复制`other`到这里。

### `[noexcept] QPageSize::~QPageSize()`

**作用与语义：**

会毁掉页面。

### `QSizeF QPageSize::definitionSize() const`

**作用与语义：**

返回定义页面大小。
对于标准页面尺寸，这会按照相关标准定义，i.e. ISO A4 以毫米为单位，而 ANSI 字母则以英寸为单位。
对于自定义页面大小，这将是创建页面大小对象时使用的原始尺寸。
如果`QPageSize`无效，那么`QSizeF`也无效。

### `[static] QSizeF QPageSize::definitionSize(QPageSize::PageSizeId pageSizeId)`

**作用与语义：**

返回标准`pageSizeId`的定义大小。
要获得定义单位，请调用`QPageSize::definitionUnits()`。

### `QPageSize::Unit QPageSize::definitionUnits() const`

**作用与语义：**

返回页面大小的定义单位。
对于标准页面尺寸，这将是相关标准中定义的单位，i.e. ISO A4以毫米为单位，而ANSI字母则以英寸为单位。
对于自定义页面大小，这些将是创建页面大小对象时使用的原始单位。
如果`QPageSize`无效，那么`QPageSize::Unit`也无效。

### `[static] QPageSize::Unit QPageSize::definitionUnits(QPageSize::PageSizeId pageSizeId)`

**作用与语义：**

返回标准`pageSizeId`的定义单位。
要获得定义大小，请调用`QPageSize::definitionSize()`。

### `QPageSize::PageSizeId QPageSize::id() const`

**作用与语义：**

返回页面的标准`QPageSize::PageSizeId`，或`QPageSize::Custom`。
如果`QPageSize`无效，身份证将`QPageSize::Custom`。

### `[static] QPageSize::PageSizeId QPageSize::id(int windowsId)`

**作用与语义：**

返回给定 Windows DMPAPER 枚举值的`PageSizeId` `windowsId`。
如果没有匹配的`PageSizeId`，则返回`QPageSize::Custom`。

### `[static] QPageSize::PageSizeId QPageSize::id(const QSize &pointSize, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**作用与语义：**

使用给定`matchPolicy`返回给定`pointSize`的标准`QPageSize::PageSizeId`点。
如果用`FuzzyMatch`，返回的`PageSizeId`点大小可能和你传入的`pointSize`不完全一致。你应该用返回的`PageSizeId`调用`QPageSize::sizePoints()`，先确定`PageSizeId`的实际点大小，再考虑计算。

### `[static] QPageSize::PageSizeId QPageSize::id(const QSizeF &size, QPageSize::Unit units, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**作用与语义：**

使用给定`matchPolicy`返回给定`size`的标准`QPageSize::PageSizeId`，并`units`。
如果用`FuzzyMatch`，回`PageSizeId`的单位大小可能和你输入的`size`不完全一致。你应该用回来的 `PageSizeId`打电话给`QPageSize::size()`，确认`PageSizeId`的实际单位大小，再用它进行任何计算。

### `bool QPageSize::isEquivalentTo(const QPageSize &other) const`

**作用与语义：**

如果该页面与`other`页面等价，即页面大小相同，无论名称等其他属性如何，返回`true`。

### `bool QPageSize::isValid() const`

**作用与语义：**

如果页面大小有效，返回`true`。
如果页面大小是用无效的`PageSizeId`、负或无效的`QSize`或`QSizeF`，或者空构造函数创建的，页面大小可能无效。

### `QString QPageSize::key() const`

**作用与语义：**

返回页面大小的唯一键。
默认情况下，这是页面大小的 PPD 标准 mediaOption 关键字，或 PPD 自定义格式键。如果`QPageSize`实例来自打印设备，则该键将由打印设备提供，可能与标准键不同。
如果`QPageSize`无效，则密钥将是一个空字符串。
这个密钥绝不应向终端用户展示，它只是内部密钥。为了获得人类可读的名称，请使用`name()`。

### `[static] QString QPageSize::key(QPageSize::PageSizeId pageSizeId)`

**作用与语义：**

返回标准`pageSizeId`的PPD mediaOption关键字。
如果`QPageSize`无效，则密钥为空。

### `QString QPageSize::name() const`

**作用与语义：**

返回页面大小的本地化且可读的名称。
如果该`QPageSize`实例是从打印设备获得的，则使用的名称即打印设备提供的名称。请注意，打印设备可能不支持当前默认的本地语言。
如果`QPageSize`无效，则名称将是空字符串。

### `[static] QString QPageSize::name(QPageSize::PageSizeId pageSizeId)`

**作用与语义：**

返回标准`pageSizeId`的本地名称。
如果`QPageSize`无效，则名称为空。

### `QRectF QPageSize::rect(QPageSize::Unit units) const`

**作用与语义：**

返回页面矩形，按要求`units`返回。
如果`QPageSize`无效，那么`QRect`也无效。

### `QRect QPageSize::rectPixels(int resolution) const`

**作用与语义：**

在给定`resolution`返回设备像素中的页面矩形。
如果`QPageSize`无效，那么`QRect`也无效。

### `QRect QPageSize::rectPoints() const`

**作用与语义：**

返回页面矩形（Postscript Points，1/72英寸）。
如果`QPageSize`无效，那么`QRect`也无效。

### `QSizeF QPageSize::size(QPageSize::Unit units) const`

**作用与语义：**

返回页面大小并按要求`units`。
如果`QPageSize`无效，那么`QSizeF`也无效。

### `[static] QSizeF QPageSize::size(QPageSize::PageSizeId pageSizeId, QPageSize::Unit units)`

**作用与语义：**

返回请求`units`中标准`pageSizeId`的大小。

### `QSize QPageSize::sizePixels(int resolution) const`

**作用与语义：**

返回给定`resolution`时的页面大小（设备像素）。
如果`QPageSize`无效，那么`QSize`也无效。

### `[static] QSize QPageSize::sizePixels(QPageSize::PageSizeId pageSizeId, int resolution)`

**作用与语义：**

返回给定`resolution`的标准 `pageSizeId` 尺寸（设备像素数）。

### `QSize QPageSize::sizePoints() const`

**作用与语义：**

返回页面的Postscript Points尺寸（1/72英寸）。
如果`QPageSize`无效，那么`QSize`也无效。

### `[static] QSize QPageSize::sizePoints(QPageSize::PageSizeId pageSizeId)`

**作用与语义：**

返回标准`pageSizeId`的点数大小。

### `[noexcept] void QPageSize::swap(QPageSize &other)`

**作用与语义：**

将`QPageSize`与`other`交换。这个操作非常快，从未出错。

### `int QPageSize::windowsId() const`

**作用与语义：**

返回 Windows DMPAPER 枚举值的页面大小。
并非所有有效的PPD页面大小都有Windows对应的，这种情况下返回为0。
如果`QPageSize`无效，Windows ID将为0。

### `[static] int QPageSize::windowsId(QPageSize::PageSizeId pageSizeId)`

**作用与语义：**

返回 Windows DMPAPER 枚举值的标准`pageSizeId`。
并非所有有效的PPD页面大小都有Windows对应的，这种情况下返回为0。

### `[noexcept] QPageSize &QPageSize::operator=(QPageSize &&other)`

**作用与语义：**

Move将`other`分配到该`QPageSize`实例，将管理指针的所有权转移到该实例。

### `QPageSize &QPageSize::operator=(const QPageSize &other)`

**作用与语义：**

赋值操作员，将`other`分配到这里。

### `bool operator!=(const QPageSize &lhs, const QPageSize &rhs)`

**作用与语义：**

如果页面大小`lhs`与页面大小`rhs`不等，即页面大小有不同属性，返回`true`。当前属性为大小和名称。

### `bool operator==(const QPageSize &lhs, const QPageSize &rhs)`

**作用与语义：**

如果页面大小`lhs`等于页面大小`rhs`，即页面大小具有相同属性，返回 `true`。当前属性为大小和名称。

### `enum SizeMatchPolicy { FuzzyMatch, FuzzyOrientationMatch, ExactMatch }`

**作用与语义：**

- `QPageSize::FuzzyMatch`：`0`;如果在容差范围内，则与标准页面尺寸匹配。
- `QPageSize::FuzzyOrientationMatch`：`1`;无论朝向如何，只要在容差范围内，则与标准页面尺寸相匹配。
- `QPageSize::ExactMatch`：`2`;只有当页面大小完全匹配时，才匹配到标准页面大小。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPageSize` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
