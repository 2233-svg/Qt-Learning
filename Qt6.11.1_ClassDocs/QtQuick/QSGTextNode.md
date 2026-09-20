# QSGTextNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGTextNode`

## 作用定位
`QSGTextNode` 是 Qt Quick 内部和高级自定义项使用的文本节点接口，用于把布局后的文字片段放入 Scene Graph。

## API 速查
| API | 是做什么的 |
|---|---|
| `addTextLayout()` | 将 `QTextLayout` 的内容加入节点。|
| `setColor()` | 设置文字颜色。|
| `setStyle()` / `setStyleColor()` | 设置描边、阴影等样式。|
| `clear()` | 清空已有文字片段。|

## 使用场景
只有当 `Text`/`TextEdit` 或现有 QML 文字组件无法满足定制绘制时才考虑直接使用，例如特殊图表坐标标签。

## 常见坑与经验
- 字体 shaping、复杂脚本和高 DPI 都很细，能让 QML 文本项处理就不要重写。
- 文本内容或字体改变后要重新布局，而不仅仅更新颜色。

## 知识点覆盖
文本布局、glyph 渲染、文字样式、国际化脚本、高 DPI。
