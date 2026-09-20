# QFontComboBox

> Qt 6.11.1 · Qt Widgets · 来自 `QFontComboBox`

## 1. 先建立直觉

`QFontComboBox` 是专门列出系统字体的组合框。它适合放在富文本工具栏、代码编辑器设置页、图表样式面板里，让用户快速选择字体族。

它和 `QFontDialog` 的定位不同：`QFontDialog` 处理完整字体选择体验，`QFontComboBox` 只负责字体族下拉；字号、粗细、斜体通常由其他控件配合。

## 2. 类说明

- 头文件：`#include <QFontComboBox>`
- 模块：`Qt6::Widgets`
- 继承自：`QComboBox`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 `QComboBox` 的下拉选择能力，并自动使用字体数据库填充候选。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFontComboBox(parent)` | 创建字体下拉框。 |
| `setCurrentFont()` / `currentFont()` | 设置或读取当前字体。 |
| `currentFontChanged(font)` | 当前字体变化信号。 |
| `setFontFilters()` / `fontFilters()` | 只显示可缩放、等宽、比例等字体类别。 |
| `setWritingSystem()` / `writingSystem()` | 按书写系统过滤字体。 |
| `setDisplayFont(fontFamily, font)` | Qt 6.3 起指定某字体族在下拉中用什么字体展示。 |
| `displayFont(fontFamily)` | 读取某字体族的展示字体设置。 |
| `setSampleTextForFont(fontFamily, text)` | Qt 6.3 起给特定字体族设置示例文本。 |
| `sampleTextForFont(fontFamily)` | 读取特定字体族示例文本。 |
| `setSampleTextForSystem(writingSystem, text)` | 为某书写系统设置示例文本。 |
| `sampleTextForSystem(writingSystem)` | 读取某书写系统示例文本。 |
| `sizeHint()` | 返回推荐尺寸。 |

## 4. 关键用法

### 过滤字体能减少噪声

代码编辑器通常设置 `MonospacedFonts`，设计工具可能保留所有字体，嵌入式或打印场景可能关注可缩放字体。过滤不是校验；用户配置里的旧字体仍可能在目标系统上不存在。

### 书写系统影响候选质量

`setWritingSystem()` 可以只显示支持某类文字的字体。做中文、日文、阿拉伯文等文本编辑时，比让用户从全量字体里碰运气更友好。

### 示例文本帮助用户判断字体

Qt 6.3 起可以给字体族或书写系统设置 sample text。多语言应用里，给中文字体显示中文样例、给拉丁字体显示拉丁样例，用户判断会快很多。

### 只选择字体族，不管理完整样式

`currentFont()` 返回 `QFont`，但下拉的核心是字体族。字号、粗体、斜体、字距通常要由独立控件或当前编辑上下文决定，避免用户换字体时意外重置其他格式。

## 5. 常见坑与经验

- 系统字体列表可能很长，不要把它放进过窄工具栏而不测试布局。
- 字体在不同系统上差异很大，保存配置时要能 fallback。
- `currentFontChanged()` 对程序设置也会触发。
- 等宽过滤对代码编辑有用，但仍建议预留“使用系统默认等宽字体”的选项。
- 完整字体选择需求用 `QFontDialog`，不要在一个 combo 里硬塞所有字体属性。
