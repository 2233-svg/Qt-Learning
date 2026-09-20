# QHelpEvent

> Qt 6.11.1 · Qt GUI · 来自 `QHelpEvent`

## 1. 先建立直觉

`QHelpEvent` 是 Qt 帮助提示体系里的位置事件，主要用于工具提示 `ToolTip` 和“这是什么？”帮助 `WhatsThis`。它告诉接收对象：用户在某个局部坐标和全局坐标处请求帮助信息。

它不保存提示文本，文本由控件根据坐标和当前上下文决定。比如同一个表格控件，不同单元格可以显示不同 tooltip；同一个画布，不同图元可以显示不同说明。

## 2. 类说明

`QHelpEvent` 继承自 `QEvent`。常见类型是 `QEvent::ToolTip` 和 `QEvent::WhatsThis`。Widgets 中通常在 `event()` 里拦截它，因为 `QWidget` 没有专门的 `helpEvent()` 虚函数。

类说明只用于表明这些 API 来自 `QHelpEvent`：局部位置和全局位置属于帮助事件本身；实际显示可由 `QToolTip`、`QWhatsThis` 或自定义浮层完成。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QHelpEvent(type, pos, globalPos)` | 构造帮助事件，类型通常为 ToolTip 或 WhatsThis。 |
| `pos() const` | 返回相对于接收控件的局部位置，用于命中单元格、图元或区域。 |
| `globalPos() const` | 返回屏幕坐标，常作为 tooltip 或帮助浮层的弹出位置。 |
| `x()` / `y()` | 读取局部坐标分量。 |
| `globalX()` / `globalY()` | 读取全局坐标分量。 |
| `type()` | 区分 ToolTip 与 WhatsThis。 |

## 4. 关键用法

### 根据坐标显示不同工具提示

```cpp
bool ChartView::event(QEvent *event)
{
    if (event->type() == QEvent::ToolTip) {
        auto *help = static_cast<QHelpEvent *>(event);
        const auto point = dataPointAt(help->pos());

        if (point) {
            QToolTip::showText(help->globalPos(), formatPointTip(*point), this);
        } else {
            QToolTip::hideText();
            event->ignore();
        }
        return true;
    }

    return QWidget::event(event);
}
```

`pos()` 用来判断用户指向了什么，`globalPos()` 用来决定提示显示在哪里。

### What's This 和 tooltip 是不同语义

`ToolTip` 通常是短提示，解释按钮或数据点；`WhatsThis` 更像上下文帮助，可以写得更详细。控件可以根据 `type()` 提供不同内容。

```cpp
if (event->type() == QEvent::WhatsThis)
    QWhatsThis::showText(help->globalPos(), detailedHelpFor(help->pos()), this);
```

## 5. 使用场景

`QHelpEvent` 适合表格单元格提示、图表数据点提示、工具栏按钮说明、复杂画布图元说明、属性面板字段解释和教学式帮助。

它也适合让一个大控件内部拥有细粒度帮助。例如代码编辑器可以对错误波浪线、断点、折叠标记、行号区域显示完全不同的提示。

## 6. 常见坑与经验

不要把 tooltip 文本固定成控件级别的一个字符串。复杂控件应根据 `pos()` 做命中测试，返回真正相关的说明。

不要只显示不隐藏。没有命中内容时调用 `QToolTip::hideText()` 并忽略事件，可以避免旧提示残留。

不要在工具提示里做慢查询。tooltip 事件可能频繁出现，内容应缓存或快速计算。

不要混淆局部和全局坐标。命中测试用局部坐标，显示位置通常用全局坐标。

## 7. 知识点覆盖

学习 `QHelpEvent` 应覆盖 tooltip、What's This、局部/全局坐标、控件内部命中测试、动态提示、事件过滤器、帮助文本设计和性能缓存。
