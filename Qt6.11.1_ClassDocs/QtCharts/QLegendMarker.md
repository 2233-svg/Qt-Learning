# QLegendMarker
> Qt 6.11.1 · Qt Charts · 来自 `QLegendMarker`

## 作用定位
`QLegendMarker` 是图例中的单个条目，连接视觉标签与对应的数据序列、bar set 或 pie slice。

## API 速查
| API | 是做什么的 |
|---|---|
| `label()` / `setLabel()` | 读取或改写显示文字。|
| `setVisible()` | 单独隐藏该条图例。|
| `setLabelBrush()` / `setBrush()` | 设置文字或图标画刷。|
| `setPen()` | 设置标记边框。|
| `setShape()` | 设置图例图标形状。|
| `clicked()` / `hovered()` | 响应图例交互。|

## 使用场景
点击 marker 后隐藏相应序列，并降低 marker 透明度表示当前关闭状态。

## 常见坑与经验
- 该类是抽象基类，应通过 `QLegend::markers()` 获得具体 marker。
- 切换 marker 可见性不等于隐藏数据本身；通常操作关联对象的 `setVisible()`。

## 知识点覆盖
图例条目、信号交互、关联数据对象、样式同步。
