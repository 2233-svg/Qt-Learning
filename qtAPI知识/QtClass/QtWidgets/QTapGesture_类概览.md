# QTapGesture：轻触手势的位置载体

> Qt 6.11.1 · `#include <QTapGesture>` · 模块：`Qt6::Widgets` · 继承：`QGesture`

`QTapGesture` 表示一次轻触。它比普通鼠标点击更偏向触摸输入语义：由手势系统识别，随 `QGestureEvent` 投递，位置保存在 `position()` 中。

## 使用场景

适合触摸优先的 widget：点击选中图元、在触摸界面触发按钮外的自定义动作、与 pan/pinch 同时纳入手势仲裁。传统桌面按钮点击仍应优先使用普通鼠标/按钮事件或控件信号。

当同一个目标同时启用 tap 和 tap-and-hold 时，要根据手势状态和接受策略避免短按、长按重复触发。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTapGesture(QObject *parent = nullptr)` | 构造 tap 手势；通常由 Qt 创建。 |
| `position() const` | 返回轻触位置。 |
| `setPosition(const QPointF &)` | 设置轻触位置，主要供 recognizer 使用。 |
| `state() const` | 继承自 `QGesture`；通常在触发/完成时执行离散动作。 |
| 与鼠标点击 | 不等同于 `QMouseEvent`；是否产生取决于 grab 的手势和平台输入。 |
