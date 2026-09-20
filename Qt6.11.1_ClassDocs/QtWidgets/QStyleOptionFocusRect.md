# QStyleOptionFocusRect

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionFocusRect`

## 1. 先建立直觉

`QStyleOptionFocusRect` 是焦点框绘制参数包。键盘焦点需要清晰可见，但不同平台的焦点框样式不一样，style 通过这个 option 统一处理。

它通常用于绘制 `QStyle::PE_FrameFocusRect`。

## 2. 类说明

`QStyleOptionFocusRect` 继承自 `QStyleOption`。它主要增加 `backgroundColor`，让 style 能根据背景选择合适的焦点框显示方式。

焦点框表达“键盘输入当前会作用到哪里”，不要和选中、高亮混为一谈。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `backgroundColor` | 焦点框所在背景色，帮助 style 选择对比。 |
| `state` | 是否有焦点、是否启用等通用状态。 |
| `rect` | 焦点框绘制区域。 |
| `QStyle::PE_FrameFocusRect` | 绘制焦点框的 primitive。 |

## 4. 关键用法

```cpp
QStyleOptionFocusRect opt;
opt.initFrom(this);
opt.rect = focusRect;
opt.backgroundColor = palette().color(QPalette::Window);

QPainter p(this);
style()->drawPrimitive(QStyle::PE_FrameFocusRect, &opt, &p, this);
```

## 5. 使用场景

适合自定义控件、可键盘导航的画布 item、列表/表格 delegate 中补充焦点显示。

普通控件通常已经由 Qt 绘制焦点，不需要手动处理。

## 6. 常见坑与经验

不要为了美观去掉焦点框。键盘用户和辅助技术用户需要它。

焦点区域应围绕可操作对象，而不是随便画在整个 widget 上。

背景色要准确，尤其在深色主题和选中背景上，否则焦点框可能看不见。
