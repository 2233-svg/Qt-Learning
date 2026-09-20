# Qt QFontComboBox 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QFontComboBox>`
> 所属模块：`Qt6::Widgets`
> 继承：`QComboBox`

## 它解决什么问题

`QFontComboBox` 是一个专门用于选择字体族的下拉框。它把系统字体枚举、字体过滤、当前字体同步、字体预览文本等细节封装在 `QComboBox` 之上，让富文本编辑器、绘图软件、报表工具和设置面板不用自己维护一份字体列表。

它解决的是“选择字体族”而不是“完整编辑字体”。如果用户还需要字号、字重、斜体、下划线、脚本等完整配置，通常要配合其他控件或使用 `QFontDialog`。

## 实际使用场景

- 文本编辑器工具栏里选择正文或标题字体。
- 图形/流程图软件中给文本节点选择字体。
- 报表设计器里为单元格、标签、图例选择字体族。
- 多语言应用中只展示支持某种书写系统的字体。
- 只允许等宽字体的代码编辑器设置项。

## 核心状态

`currentFont` 是当前选中的字体。用户选择新字体，或代码调用 `setCurrentFont()` 后，会通过 `currentFontChanged(const QFont &)` 通知外部。

`writingSystem` 用来限制字体列表到某个书写系统，例如拉丁、中文、日文、阿拉伯文等。这样可以避免展示对当前文本脚本没有意义的字体。

`fontFilters` 用标志位过滤字体类型：

| 过滤项 | 含义 |
| --- | --- |
| `AllFonts` | 不按字体类型过滤。 |
| `ScalableFonts` | 只显示可缩放字体。 |
| `NonScalableFonts` | 只显示非可缩放字体。 |
| `MonospacedFonts` | 只显示等宽字体。 |
| `ProportionalFonts` | 只显示比例字体。 |

这些过滤项可以组合，但组合后是否有结果取决于系统实际安装字体。列表为空时，应从产品层面给出兜底行为。

## 字体预览与显示字体

Qt 6.3 起，`QFontComboBox` 可以按书写系统或字体族设置示例文本，也可以指定某个字体族在下拉列表中的显示字体。这对多语言字体选择很有用：中文字体可以显示中文样例，日文字体显示假名，代码字体显示短代码片段。

`displayFont(fontFamily)` 返回 `std::optional<QFont>`。没有单独设置显示字体时返回空 optional，而不是构造一个默认值冒充用户设置。

## 使用边界

`QFontComboBox` 继承 `QComboBox`，因此仍遵守 QWidget 线程和生命周期规则：只在 GUI 线程创建和访问。系统字体很多时，弹出列表和 size hint 计算可能受到字体数量影响，不要在高频路径反复创建销毁。

`setCurrentFont()` 的重点是选中字体族；传入的 `QFont` 可能包含字号、字重等信息，但下拉框本身主要表达 family 选择。完整字体属性应由其他控件保存。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFontComboBox(QWidget *parent = nullptr)` | 创建字体选择下拉框。 | 作为 QWidget 使用，遵守父子对象和 GUI 线程规则。 |
| 析构 | `~QFontComboBox()` | 销毁控件。 | 不拥有系统字体，只销毁下拉框自身资源。 |
| 当前字体 | `QFont currentFont() const` | 返回当前选中的字体。 | 主要关注字体族；其他字体属性不一定代表完整字体选择结果。 |
| 当前字体 | `void setCurrentFont(const QFont &font)` | 将下拉框切换到指定字体。 | 如果字体族不在过滤后的列表中，实际选择可能无法按预期命中。 |
| 当前字体 | `void currentFontChanged(const QFont &font)` | 当前字体变化信号。 | 响应用户选择时优先连接这个信号。 |
| 书写系统 | `void setWritingSystem(QFontDatabase::WritingSystem writingSystem)` | 限制显示支持指定书写系统的字体。 | 多语言界面可用它减少无关字体。 |
| 书写系统 | `QFontDatabase::WritingSystem writingSystem() const` | 返回当前书写系统过滤条件。 | 和 `fontFilters` 共同决定列表内容。 |
| 字体过滤 | `void setFontFilters(FontFilters filters)` | 设置字体类型过滤标志。 | 等宽、比例、可缩放等条件可以组合，但可能筛出空列表。 |
| 字体过滤 | `FontFilters fontFilters() const` | 返回当前过滤标志。 | 用于同步设置面板状态。 |
| 枚举 | `enum FontFilter` | 描述字体过滤条件。 | `AllFonts` 为 0；其他值是可组合标志。 |
| 布局 | `QSize sizeHint() const` | 返回控件推荐尺寸。 | 受字体列表、样例文本和当前 style 影响。 |
| 预览文本 | `void setSampleTextForSystem(QFontDatabase::WritingSystem, const QString &sampleText)` | 为某个书写系统设置列表样例文本。 | Qt 6.3 起可用；适合多语言字体预览。 |
| 预览文本 | `QString sampleTextForSystem(QFontDatabase::WritingSystem) const` | 查询某书写系统的样例文本。 | 未设置时返回默认策略下的文本。 |
| 预览文本 | `void setSampleTextForFont(const QString &fontFamily, const QString &sampleText)` | 为指定字体族设置样例文本。 | 适合少数字体需要特殊展示的场景。 |
| 预览文本 | `QString sampleTextForFont(const QString &fontFamily) const` | 查询指定字体族样例文本。 | Qt 6.3 起可用。 |
| 显示字体 | `void setDisplayFont(const QString &fontFamily, const QFont &font)` | 指定某字体族在列表中的显示字体。 | 只影响列表展示，不等于改变实际字体库。 |
| 显示字体 | `std::optional<QFont> displayFont(const QString &fontFamily) const` | 查询指定字体族的显示字体覆盖。 | 返回空 optional 表示没有单独设置。 |
| 事件 | `bool event(QEvent *event)` | 处理内部事件。 | 派生类重写时要保持 `QComboBox` 的基本交互。 |

## 一句话总结

`QFontComboBox` 是字体族选择控件：它负责列出、过滤和预览系统字体，但完整字体属性仍应由应用自己的字体设置流程管理。
