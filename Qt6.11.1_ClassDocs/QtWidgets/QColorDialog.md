# QColorDialog

> Qt 6.11.1 · Qt Widgets · 来自 `QColorDialog`

## 1. 先建立直觉

`QColorDialog` 是标准颜色选择对话框。它既可以一次性弹出并返回颜色，也可以作为实时颜色选择面板使用，让用户拖动时立即预览效果。

典型场景包括选择文字颜色、背景色、图表色、主题色、画笔颜色。它返回 `QColor`，不是样式表；如何把颜色应用到控件、文档或绘图逻辑，需要调用方自己决定。

## 2. 类说明

- 头文件：`#include <QColorDialog>`
- 模块：`Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

颜色对话框可能使用原生实现。某些选项，如隐藏按钮、透明度通道或滴管按钮，受平台支持影响。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `getColor(initial, parent, title, options)` | 快速弹出模态颜色对话框，返回用户确认的颜色。 |
| `QColorDialog(parent)` / `QColorDialog(initial, parent)` | 创建可配置实例。 |
| `setCurrentColor()` / `currentColor()` | 设置或读取当前正在预览的颜色。 |
| `selectedColor()` | 读取用户最终确认的颜色。 |
| `currentColorChanged(color)` | 当前颜色变化，适合实时预览。 |
| `colorSelected(color)` | 用户点击确定后发出，适合最终应用。 |
| `setOption()` / `setOptions()` / `testOption()` | 设置透明度、无按钮、非原生等选项。 |
| `open(receiver, member)` | 异步打开并连接最终选择信号。 |
| `customColor(index)` / `setCustomColor()` | 读取或设置共享自定义颜色槽。 |
| `customCount()` | 自定义颜色槽数量。 |
| `standardColor(index)` / `setStandardColor()` | 读取或设置标准颜色槽。 |

## 4. 关键用法

### `currentColor` 和 `selectedColor` 不同

`currentColor` 表示用户正在对话框里移动到的颜色，会频繁变化；`selectedColor` 表示用户最终接受的颜色。实时预览连接 `currentColorChanged()`，但要在取消时恢复原颜色；只想在确认后应用则用 `colorSelected()` 或静态 `getColor()` 返回值。

### 静态函数要检查有效性

用户取消 `getColor()` 时返回无效 `QColor`。使用前调用 `isValid()`，不要把无效颜色直接写进配置或样式。

### 透明度通道要明确开启

需要 RGBA 时设置 `ShowAlphaChannel`。如果应用内部不支持透明色，就不要开启，否则用户以为选择了半透明，最终显示却被当成不透明。

### `NoButtons` 适合实时面板

`NoButtons` 会隐藏确定/取消按钮，适合颜色变化立即生效的工具面板。它要求你自己设计关闭和撤销逻辑，否则用户很难理解“取消”在哪里。

## 5. 常见坑与经验

- 选项应在显示对话框前设置，显示后不保证各平台都能立即生效。
- 自定义颜色是所有颜色对话框共享的静态槽，不是某个实例私有状态。
- 原生对话框在不同平台上可用功能和外观不同。
- 滴管按钮在 Qt 6.6 起可用 `NoEyeDropperButton` 隐藏。
- 实时预览时要保存旧颜色，以便用户取消后恢复。
