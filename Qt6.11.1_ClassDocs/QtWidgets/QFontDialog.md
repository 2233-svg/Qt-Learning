# QFontDialog

> Qt 6.11.1 · Qt Widgets · 来自 `QFontDialog`

## 1. 先建立直觉

`QFontDialog` 是标准字体选择对话框。它让用户选择字体族、字号、粗细、斜体等字体属性，并返回 `QFont`。

常见场景包括编辑器字体设置、富文本工具栏、打印模板字体、图表标签字体。它只负责选字体，不负责把字体应用到哪些控件或文档范围。

## 2. 类说明

- 头文件：`#include <QFontDialog>`
- 模块：`Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

字体对话框可能使用平台原生实现；某些字体过滤选项在不同平台支持程度不同。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `getFont(ok, initial, parent, title, options)` | 弹出模态字体对话框，返回选择结果，并用 `ok` 表示是否确认。 |
| `getFont(ok, parent)` | 使用默认字体作为初始值的便捷重载。 |
| `QFontDialog(parent)` / `QFontDialog(initial, parent)` | 创建可配置字体对话框。 |
| `setCurrentFont()` / `currentFont()` | 设置或读取当前正在预览的字体。 |
| `selectedFont()` | 用户最终接受后选择的字体。 |
| `currentFontChanged(font)` | 当前字体变化，适合实时预览。 |
| `fontSelected(font)` | 用户确认选择后发出。 |
| `setOption()` / `setOptions()` / `testOption()` | 设置无按钮、非原生、只显示等宽/可缩放字体等选项。 |
| `open(receiver, member)` | 异步打开并连接最终选择信号。 |

## 4. 关键用法

### 用 `ok` 判断用户是否确认

静态 `getFont()` 在用户取消时也会返回一个 `QFont`，通常是初始字体或默认字体。因此必须检查 `ok`，不要只看返回字体是否为空。

### 当前字体和最终字体分开

`currentFontChanged()` 会随着用户在对话框里选择而持续发出，适合实时预览。`fontSelected()` 只在用户最终确认后发出。若做实时预览，要保留原字体，在取消时恢复。

### 字体过滤不是跨平台铁律

`MonospacedFonts`、`ProportionalFonts`、`ScalableFonts`、`NonScalableFonts` 能帮助缩小候选范围，但原生字体面板可能不完全支持。需要严格控制候选字体时，非原生对话框或自定义选择 UI 更可控。

### `NoButtons` 适合设置面板

`NoButtons` 让字体变化立即生效，适合偏好设置页里的实时预览。但它改变了确认/取消语义，应用需要自己提供恢复或撤销路径。

## 5. 常见坑与经验

- 用户取消时返回字体不代表用户接受了它，必须看 `ok` 或最终信号。
- 选项应在显示前设置。
- 字体名、字号在不同系统上可用性不同，保存配置后下次启动要能处理字体不存在。
- 修改全局应用字体会影响布局尺寸，可能需要重新布局。
- 对代码编辑器优先筛选等宽字体，并保留用户手动选择其他字体的可能。
