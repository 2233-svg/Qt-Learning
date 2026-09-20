# QFocusFrame

> Qt 6.11.1 · Qt Widgets · 来自 `QFocusFrame`

## 1. 先建立直觉

`QFocusFrame` 是一个跟随目标控件显示的焦点外框。它不让控件获得焦点，也不改变 Tab 顺序；它只是把“当前焦点在哪个控件上”用平台风格额外画出来。

多数控件会自己绘制焦点状态，所以应用代码很少直接使用 `QFocusFrame`。它更适合自定义控件、复杂容器或特殊主题：当目标控件本身不方便画焦点框时，用一个独立的小 widget 覆盖在外侧。

## 2. 类说明

`QFocusFrame` 继承自 `QWidget`。调用 `setWidget()` 后，它会关联到目标控件，跟随目标控件移动、调整大小、显示和隐藏，并按当前 `QStyle` 绘制焦点外观。

它设置了特殊属性以减少对子对象事件的干扰，所以可以放在一些会监控子控件变化的容器里。真正的焦点逻辑仍由目标控件的 `focusPolicy`、事件和窗口激活状态决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFocusFrame(QWidget *)` | 创建焦点框。父对象通常是目标控件所在的容器或顶层窗口。 |
| `setWidget(QWidget *)` | 指定要跟随和框住的目标控件。传入新控件会切换跟随对象。 |
| `widget()` | 返回当前关联的目标控件。 |
| `initStyleOption(QStyleOption *)` | 为自定义绘制准备样式参数，子类化时使用。 |
| `event(QEvent *)` | 处理自身事件，例如样式、显示、布局变化。 |
| `eventFilter(QObject *, QEvent *)` | 观察目标控件事件，用来同步几何与可见状态。 |
| `paintEvent(QPaintEvent *)` | 按平台样式绘制焦点框。 |

## 4. 关键用法

典型用法是给一个自绘控件加外部焦点框：

```cpp
auto *focusFrame = new QFocusFrame(parentWidget);
focusFrame->setWidget(customEditor);
```

目标控件获得焦点后，焦点框的显示由 Qt 内部事件同步。你通常不需要手动移动它；如果目标控件外面还有复杂变换、滚动或代理层，就要确认坐标关系是否符合预期。

子类化时，不建议完全绕过 style 自己画。可以先初始化样式选项，再交给 `QStyle`：

```cpp
void MyFocusFrame::paintEvent(QPaintEvent *)
{
    QStyleOption option;
    initStyleOption(&option);

    QPainter painter(this);
    style()->drawControl(QStyle::CE_FocusFrame, &option, &painter, this);
}
```

## 5. 使用场景

适合自定义编辑器、嵌入式属性面板、可视化设计器里的选中控件、高可访问性主题、需要统一焦点外观的复杂控件组合。

如果控件已经能清楚显示焦点，额外套一层 `QFocusFrame` 可能造成视觉重复。焦点反馈要明确，但不应该吵。

## 6. 常见坑与经验

`QFocusFrame` 不会让目标控件可聚焦。目标控件仍然需要合适的 `setFocusPolicy()`。

不要把它当成选中框。焦点表示键盘输入位置，选择表示业务状态，两者可以重合，但语义不同。

滚动区域中使用时要注意父对象选择。焦点框如果放在 viewport 外层，坐标映射错误时会漂；通常让它和目标控件处在容易同步的同一坐标体系里。
