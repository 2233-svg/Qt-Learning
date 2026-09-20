# QFontDatabase

> Qt 6.11.1 · Qt GUI · 来自 `QFontDatabase`

## 1. 先建立直觉

`QFontDatabase` 是应用看到的字体目录和临时字体注册器。它能枚举系统字族、样式与书写系统，加载随应用附带的 TTF/OTF，也能为特定文字脚本或 emoji 指定应用级回退优先级。

它不负责绘制，也不保证某个 `QFont` 请求最终一定选到哪张字体；查询实际匹配结果请用 `QFontInfo`。把它想成“字体可用性与策略层”，而非“设置控件字体”的日常 API。

## 2. 类说明

- 头文件：`#include <QFontDatabase>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- API 基本为静态成员；调用前应已创建 `QGuiApplication` 或其子类。
- 应用注册字体只对当前进程有效，退出后消失；其 ID 可用于查询和卸载。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `families([writingSystem])` | 枚举系统可用字族，可按书写系统过滤 |
| `styles(family)` / `pointSizes()` / `smoothSizes()` | 查询字族样式与推荐字号 |
| `font(family, style, pointSize)` | 从数据库条目创建一个字体请求 |
| `isScalable()` / `isSmoothlyScalable()` / `isBitmapScalable()` | 判断样式的缩放能力 |
| `isFixedPitch()` / `italic()` / `bold()` / `weight()` | 查询字族样式的关键属性 |
| `isPrivateFamily()` | 判断字族是否应隐藏在用户字体选择器中 |
| `systemFont(type)` | 获得系统推荐的常规、等宽、标题或最小可读字体 |
| `styleString(font)` | 把字体/字体匹配结果显示为用户可读样式名 |
| `writingSystems()` / `writingSystemName()` / `writingSystemSample()` | 查询系统或字族覆盖的书写系统 |
| `addApplicationFont(file)` | 从文件注册临时应用字体，失败返回 `-1` |
| `addApplicationFontFromData(data)` | 从内存字体数据注册字体 |
| `applicationFontFamilies(id)` | 获得一次注册实际提供的字族名 |
| `removeApplicationFont(id)` / `removeAllApplicationFonts()` | 卸载应用注册字体 |
| `setApplicationFallbackFontFamilies(script, families)` | Qt 6.8 起指定某脚本的应用级回退顺序 |
| `add/removeApplicationFallbackFontFamily()` | 在某脚本的回退列表中增删一个字族 |
| `setApplicationEmojiFontFamilies()` | Qt 6.9 起设置 emoji 字体优先列表 |
| `add/removeApplicationEmojiFontFamily()` | 管理单个应用级 emoji 字体 |
| `standardSizes()` | 获取传统字号选择器可用的标准列表 |

## 4. 关键用法

### 安全加载资源中的应用字体

```cpp
const int id = QFontDatabase::addApplicationFont(":/fonts/Inter-Variable.ttf");
if (id < 0)
    qWarning() << "Cannot load bundled font";

const QStringList loadedFamilies = QFontDatabase::applicationFontFamilies(id);
if (!loadedFamilies.isEmpty()) {
    QFont uiFont(loadedFamilies.first());
    uiFont.setPointSizeF(10.5);
    QApplication::setFont(uiFont);
}
```

不要假设文件名就是字族名。一个字体文件可能含多个 family，TTC 尤其如此；始终从 `applicationFontFamilies(id)` 取实际名称。注册失败用 `id < 0` 判断，不能继续传给查询或移除函数。

### 构建合格的字体选择器

```cpp
for (const QString &family : QFontDatabase::families()) {
    if (QFontDatabase::isPrivateFamily(family))
        continue;
    addFamilyToChooser(family);
}
```

用户可选字体列表不要简单展示所有 `families()`。某些平台会暴露私有系统 UI 字体，`isPrivateFamily()` 是专门为字体选择器提供的过滤条件。选中 family 后再列 `styles(family)`，而不是自己猜测 “Bold Italic” 是否存在。

### 固定多语言回退的优先级

```cpp
QFontDatabase::setApplicationFallbackFontFamilies(
    QChar::Script_Han,
    { "Noto Sans CJK SC", "Noto Sans CJK JP" });
```

这会影响**整个应用**中该文字脚本缺字时的候选顺序，适合将随程序发布的 CJK 字体放在系统回退之前。它不替代 `QFont::setFamilies()`：前者是按脚本的缺字回退策略，后者是某个字体请求的主候选列表。

### 为图标或消息选择 emoji 字体

```cpp
QFontDatabase::setApplicationEmojiFontFamilies(
    { "Noto Color Emoji", "Segoe UI Emoji" });
```

该 API 自 Qt 6.9 起可用。它面向 emoji 及序列渲染，不应滥用为通用符号字体回退；在不支持这些字族的平台上，Qt 仍会继续匹配其他可用字体。

## 5. 重要枚举

| 枚举 | 说明 |
| --- | --- |
| `SystemFont::GeneralFont` | 系统常规 UI 字体 |
| `SystemFont::FixedFont` | 系统推荐等宽字体 |
| `SystemFont::TitleFont` | 系统标题用字体 |
| `SystemFont::SmallestReadableFont` | 系统定义的最小可读字体 |
| `WritingSystem` | 粗粒度的文字系统分类，如 Latin、Arabic、SimplifiedChinese、Japanese、Symbol |

`WritingSystem` 适合给字体列表分组或筛选，但不是字符覆盖的严格证明。一个字体声明支持 Simplified Chinese，也未必含有某个罕见汉字；要检查具体码点，用 `QRawFont::supportsCharacter()` 或实际塑形测试。

## 6. 使用场景

- 应用启动时注册内置品牌字体或离线字体包。
- 做字体选择器、样式选择器和字号选择器。
- 为中文、阿拉伯文、天城文等脚本设置一致的跨平台回退。
- 选择符合系统外观的标题/等宽字体，而不是硬编码某个操作系统的字体名。
- 检查某个字体是否可平滑缩放，决定是否展示任意字号输入框。

## 7. 常见坑与经验

- **注册字体不等于嵌入字体。** 这是运行时进程注册；你仍须处理资源路径、许可证和平台部署。
- **移除字体会影响仍在使用它的 UI。** 仅在相关 `QFont` 和缓存不再使用时卸载；长期全局 UI 字体一般无需提前 remove。
- **`isScalable()` 不等于任意字号都好看。** 位图可缩放字体可能只能在 `smoothSizes()` 给出的点大小上保持质量。
- **字体数据库的“支持脚本”是元数据。** 它不能替代对具体字符、连字和 emoji ZWJ 序列的验证。
- **应用级回退是全局状态。** 库代码不应擅自调用 `setApplicationFallbackFontFamilies()` 覆盖宿主应用的策略。
- **枚举成本与缓存。** 系统字体库很大时，不要在每次 `paintEvent()` 或搜索按键中重新枚举所有字体。

## 8. 知识点覆盖

系统字体枚举、应用字体加载、字体选择器、字体缩放能力、书写系统、CJK/emoji 回退、进程级全局状态、字体文件与字族名差异、部署与许可证。
