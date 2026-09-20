# QGraphicsColorizeEffect

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsColorizeEffect`

## 1. 先建立直觉

`QGraphicsColorizeEffect` 给目标绘制结果叠加一种颜色倾向。它不会改变原控件或 item 的调色板、图片数据或文本内容，只是在最终显示时把结果染向某个颜色。

它适合表达状态：选中高亮、警告染色、禁用弱化、搜索命中、拖拽目标提示。比直接改每个子元素颜色更省事，但也更像“后处理滤镜”。

## 2. 类说明

`QGraphicsColorizeEffect` 继承自 `QGraphicsEffect`。核心属性是 `color` 和 `strength`。`strength` 越高，目标越接近指定颜色；越低，越保留原本颜色。

这个效果对复杂内容很方便，例如一整个图标、面板或图元组统一染色。但如果你需要语义化主题配色，改 palette、样式表或 item 自身绘制更可维护。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsColorizeEffect(QObject *)` | 创建染色效果。 |
| `setColor(const QColor &)` / `color()` | 设置或读取目标染色颜色。 |
| `setStrength(qreal)` / `strength()` | 设置或读取染色强度，通常在 0 到 1 之间使用。 |
| `colorChanged(QColor)` | 染色颜色变化时发出。 |
| `strengthChanged(qreal)` | 强度变化时发出。 |
| `setEnabled(bool)` | 继承自 `QGraphicsEffect`，快速开关效果。 |

## 4. 关键用法

```cpp
auto *effect = new QGraphicsColorizeEffect(item);
effect->setColor(QColor("#2f80ed"));
effect->setStrength(0.45);
item->setGraphicsEffect(effect);
```

用动画做搜索命中闪烁：

```cpp
auto *anim = new QPropertyAnimation(effect, "strength", effect);
anim->setStartValue(0.0);
anim->setEndValue(0.8);
anim->setLoopCount(2);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

## 5. 使用场景

适合状态高亮、临时警告、拖放目标提示、选中对象强调、图标统一染色、禁用态快速处理。

不适合应用级主题系统。长期颜色规则应该进入样式、调色板、delegate 或 item 绘制逻辑。

## 6. 常见坑与经验

染色会影响目标整体，包括图标、文字、边框和子内容。只想改文字颜色时，用文本颜色 API。

`strength` 过高会损失原内容层次。图标细节、图片明暗可能被压平。

效果和源对象绘制分离。源内容改变时效果会重新作用，但业务数据本身没有被修改。
