# QFontDatabase

`QFontDatabase` 是进程内字体目录的静态查询与注册入口。它用于枚举系统和应用临时加载的字体、查询字体家族能提供的样式/尺寸/书写系统，并配置应用级的脚本回退和 emoji 回退。

- 头文件：`#include <QFontDatabase>`
- 模块：`Qt6::Gui`
- 设计：Qt 6 中没有可实例化数据库对象，API 都是静态函数
- 前提：已有 `QGuiApplication`，因为字体数据库来自窗口系统与字体后端

## 它解决的问题

`QFont` 描述“希望用什么”，但不负责列举机器上有什么，也不负责加载随应用分发的 `.ttf` / `.otf`。`QFontDatabase` 填补这部分：字体选择器可列出家族、样式和字号；编辑器可判断等宽字体；应用可注册私有字体并按语言脚本指定回退优先级。

它返回的家族和样式是可用资源的目录信息，不是“对某段具体文本最终用了哪些字形”。确认实际匹配看 `QFontInfo`，计算显示尺寸看 `QFontMetricsF`。

## 实际场景

**加载随应用发布的字体。**

```cpp
const int id = QFontDatabase::addApplicationFont(":/fonts/Inter-Regular.ttf");
if (id < 0)
    return;

const QStringList families = QFontDatabase::applicationFontFamilies(id);
if (!families.isEmpty())
    QApplication::setFont(QFont(families.first()));

// 只有确保当前没有 QFont/QRawFont 继续依赖该字体时才考虑 removeApplicationFont(id)。
```

支持 TrueType、TrueType Collection 与 OpenType；`addApplicationFont()` / `addApplicationFontFromData()` 返回 `-1` 表示加载失败。ID 仅对当前进程和这次注册有效，不能持久化。

**构建字体选择器。** 使用 `families()`、`styles()`、`pointSizes()` / `smoothSizes()` 填充 UI；家族出现在多个 foundry 时，返回名会采用 `Family [Foundry]` 格式。

**混合语言与 emoji。** Qt 默认会针对缺字形搜索回退字体。Qt 6.8 起可通过 `setApplicationFallbackFontFamilies(script, list)` 为特定 `QChar::Script` 指定优先级；Qt 6.9 起可用 `setApplicationEmojiFontFamilies()` 指定 emoji 族。二者是应用级全局设置，应在创建大多数文本对象之前集中配置。

## 查询和匹配的边界

- `families()` 已排序，可按 `WritingSystem` 过滤；它适合构建列表，也比深度匹配检测更快，但别把它当成所有别名的完整集合。
- `hasFamily()` 用于家族存在性检查。存在不代表每个样式、字号或字形均可用。
- `font(family, style, pointSize)` 找不到精确组合时会返回应用默认字体，而不是空 `QFont`；必要时配合 `QFontInfo` 验证。
- `isScalable()` 只说明可缩放；`isSmoothlyScalable()` 更接近“可在连续尺寸下质量良好”；位图可缩放字体在任意大小上往往难看，应考虑 `smoothSizes()`。
- `isPrivateFamily()` 为真表示不应在普通字体选择 UI 中展示该家族。

应用字体的可见范围仅是本应用。卸载已注册字体的同时若仍有文本布局、`QFont`、`QRawFont` 或图形缓存引用它，会造成难以诊断的行为；实际项目通常让应用字体存活到进程结束。

## 回退策略

脚本回退与 `QFont::families()` 是不同层次：

| 机制 | 范围 | 适合的需求 |
| --- | --- | --- |
| `QFont::setFamilies()` | 单个字体请求 | 主 UI 字体在不同系统的候选顺序 |
| `setApplicationFallbackFontFamilies()` | 全应用、某 `QChar::Script` | CJK、阿拉伯文、符号等缺字的统一视觉 |
| `setApplicationEmojiFontFamilies()` | 全应用 emoji | 统一彩色 emoji 样式或补足系统 emoji |
| `QFont::NoFontMerging` | 单个字体请求 | 禁止回退以暴露缺字；普通 UI 通常不应使用 |

## API 速查表

### 目录查询与构造字体

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `standardSizes()` | 返回常用的标准点大小列表。 | 用于字体选择器建议值，不等于某字体真正支持的全部尺寸。 |
| `writingSystems()` | 返回系统中所有可用书写系统。 | 是全局能力集合。 |
| `writingSystems(family)` | 返回一个家族支持的书写系统。 | 不保证覆盖该书写系统的每个 Unicode 字符。 |
| `families(writingSystem = Any)` | 返回支持指定书写系统的排序家族列表。 | foundry 名会附在方括号中；列表不一定包含所有别名。 |
| `hasFamily(family)` | 判断数据库是否含该家族。 | 仅检查家族，不检查样式和字形覆盖。 |
| `styles(family)` | 返回家族提供的样式名。 | 这些名字可传给 `font()`，不同平台表述不同。 |
| `pointSizes(family, style)` | 返回给定组合的可用点大小。 | 对可平滑缩放字体不应把此列表误作唯一合法大小。 |
| `smoothSizes(family, style)` | 返回视觉上适合的点大小。 | 位图字体缩放时优先使用这些值。 |
| `font(family, style, pointSize)` | 按目录条目构造 `QFont`。 | 失败时返回应用默认字体，不能只检查对象是否存在。 |
| `styleString(QFont)` | 返回请求字体对应的样式文本。 | 多用于显示，未必是实际匹配样式。 |
| `styleString(QFontInfo)` | 返回实际匹配字体的样式文本。 | 诊断和显示实际结果时优先这一重载。 |
| `systemFont(SystemFont type)` | 返回系统 UI、固定宽度等预定义字体。 | 使用平台语义字体比硬编码家族名更可移植。 |

### 字体属性和书写系统辅助

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `isBitmapScalable(family, style)` | 判断是否为可缩放位图字体。 | 任意倍率缩放常不清晰。 |
| `isSmoothlyScalable(family, style)` | 判断是否适合连续缩放。 | 不代表所有平台的输出完全一致。 |
| `isScalable(family, style)` | 判断字体是否能缩放。 | 不等于平滑缩放。 |
| `isFixedPitch(family, style)` | 判断该组合是否等宽。 | 用于代码编辑器过滤，但仍应在实际字体上测量/验证。 |
| `italic(family, style)` | 判断样式是否为斜体。 | 样式名和属性由字体后端定义。 |
| `bold(family, style)` | 判断样式是否为粗体。 | 不等于任意 weight 都存在独立 face。 |
| `weight(family, style)` | 返回样式字重。 | 使用 `QFont::Weight` 标尺理解。 |
| `isPrivateFamily(family)` | 判断家族是否私有。 | 私有家族不适合作为面向用户的选择项。 |
| `writingSystemName(system)` | 返回书写系统的显示名称。 | 用于 UI 标签。 |
| `writingSystemSample(system)` | 返回该书写系统的示例字符。 | 用于字体预览，不是完整覆盖验证。 |

### 应用字体的注册与移除

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `addApplicationFont(fileName)` | 从文件加载字体并返回注册 ID。 | 失败为 `-1`；仅支持 Qt 文档列出的 TTF/TTC/OTF。 |
| `addApplicationFontFromData(fontData)` | 从二进制数据加载字体。 | 适合资源/网络已验证字节；失败为 `-1`。 |
| `applicationFontFamilies(id)` | 返回注册字体包含的家族名。 | 先检查加载 ID；一个文件可含多个家族。 |
| `removeApplicationFont(id)` | 卸载一个应用字体。 | 成功返回 `true`；不要在仍使用字体时卸载。 |
| `removeAllApplicationFonts()` | 卸载全部应用字体。 | 影响范围大，测试/退出清理以外应避免。 |

### 脚本与 emoji 回退

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `addApplicationFallbackFontFamily(script, family)` | 向某脚本的应用回退列表追加家族。 | Qt 6.8；顺序影响优先级。 |
| `removeApplicationFallbackFontFamily(script, family)` | 删除某条脚本回退项。 | 找到并删除时返回 `true`。 |
| `setApplicationFallbackFontFamilies(script, families)` | 整体替换某脚本的回退列表。 | 会覆盖此前追加的列表；应使用已确认存在的家族。 |
| `applicationFallbackFontFamilies(script)` | 获取应用配置的脚本回退列表。 | 只返回应用定义项，不等于平台完整回退链。 |
| `addApplicationEmojiFontFamily(family)` | 追加应用优先的 emoji 家族。 | Qt 6.9；适合覆盖系统默认 emoji。 |
| `removeApplicationEmojiFontFamily(family)` | 删除一个 emoji 家族。 | 结果表示是否实际移除了条目。 |
| `setApplicationEmojiFontFamilies(families)` | 整体替换 emoji 回退列表。 | 会覆盖此前追加值。 |
| `applicationEmojiFontFamilies()` | 获取应用定义的 emoji 家族列表。 | 不包含平台默认 fallback 链。 |

### 枚举速览

| 枚举 | 含义 |
| --- | --- |
| `WritingSystem` | `Any` 以及 Latin、Greek、Cyrillic、Arabic、Han、Japanese、Korean 等书写系统，用于目录过滤和预览。 |
| `SystemFont` | `GeneralFont`、`FixedFont`、`TitleFont`、`SmallestReadableFont` 等平台语义字体类别。 |

## 易错点

1. 加载成功后直接用文件名作为 `QFont` 家族名。应取 `applicationFontFamilies(id)` 返回的真实家族。
2. 认为 `font()` 失败会返回无效对象。它会退回应用默认字体，必须用 `QFontInfo` 检查结果。
3. 在每个控件创建时反复枚举 `families()`。将选择器数据缓存到合适层级，避免启动期和交互期反复扫描。
4. 在普通应用运行中随意 `removeAllApplicationFonts()`。它会改变全局字体可用性，已创建文本对象不应依赖这种动态变化。
5. 只因 `families()` 不包含别名就判断字体不存在。需要更彻底匹配时让 `QFont` / `QFontInfo` 参与验证。
