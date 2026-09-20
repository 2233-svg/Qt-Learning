# QToolTip

> Qt 6.11.1 · Qt Widgets · 来自 `QToolTip`

## 1. 先建立直觉

`QToolTip` 是显示工具提示的静态工具类。大多数时候你只需要给控件或 action 设置 `toolTip` 属性；只有在自定义视图、绘图区域、复杂命中测试中，才直接调用 `QToolTip::showText()`。

它不是 QWidget 子类，不创建你能加入布局的对象。它管理当前全局可见的 tooltip 文本、字体和调色板。

## 2. 类说明

- 头文件：`#include <QToolTip>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

工具提示显示位置使用全局屏幕坐标；关联 widget 和 rect 用来决定屏幕以及鼠标离开区域时何时隐藏。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `showText(pos, text, w, rect, msecDisplayTime)` | 在全局位置显示提示；空文本会隐藏提示。 |
| `hideText()` | 隐藏当前提示。 |
| `isVisible()` | 当前是否显示 tooltip。 |
| `text()` | 返回当前 tooltip 文本，不可见时为空。 |
| `setFont()` / `font()` | 设置或读取 tooltip 字体。 |
| `setPalette()` / `palette()` | 设置或读取 tooltip 调色板。 |

## 4. 关键用法

### 普通控件优先用属性

按钮、输入框、菜单 action 的说明，优先 `setToolTip()`。Qt 会根据平台规则处理延迟、位置和隐藏。只有自绘 canvas、表格单元格、图形项等没有天然 tooltip 区域时，才手动 `showText()`。

### 坐标和区域要配对

`pos` 是全局坐标。`rect` 是相对于参数 `w` 的局部区域；如果传了非空 rect，就必须传对应 widget。鼠标移出该区域后 tooltip 会隐藏。这个机制适合 item view 中单元格级提示。

### 不要滥用工具提示

tooltip 应解释控件作用、显示被截断内容、补充短信息。它不适合放错误详情、复杂说明、可交互内容或必须阅读的警告，因为用户可能永远不会悬停到它。

### 全局外观会影响整个应用

`setFont()` 和 `setPalette()` 改的是工具提示全局样式。除非应用有统一设计要求，不要在局部功能里随意改，避免其他界面提示突然变样。

## 5. 常见坑与经验

- 文本相同且 tooltip 已显示时，再次 `showText()` 不一定移动位置；可先隐藏再显示。
- `msecDisplayTime = -1` 表示由 Qt 根据文本长度决定显示时长。
- tooltip 使用非活动调色板颜色组，因为它不是活动窗口。
- 重要信息不要只放 tooltip，键盘和触屏用户可能看不到。
- 自定义视图里要在鼠标移动或 help event 中及时更新/隐藏提示。
