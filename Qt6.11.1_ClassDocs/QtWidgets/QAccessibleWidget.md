# QAccessibleWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QAccessibleWidget`

## 1. 先建立直觉

`QAccessibleWidget` 是 QWidget 的无障碍接口基类。它把一个可见控件转换成辅助技术能理解的对象：名字是什么、角色是什么、在哪里、是否可用、有哪些动作、子对象是谁。

屏幕阅读器、自动化测试、系统辅助功能都依赖这些信息。自定义控件如果只画得漂亮但没有无障碍语义，对很多用户来说就是不可用的。

## 2. 类说明

`QAccessibleWidget` 继承自 `QAccessibleObject` 并实现 `QAccessibleActionInterface`。它包装一个 `QWidget`，默认从 widget 的属性、geometry、palette、focus、enabled/visible 状态中推导无障碍信息。

自定义 widget 无法被 Qt 默认准确描述时，可以继承它，覆盖 `role()`、`text()`、`state()`、`child()`、`childCount()`、`doAction()` 等函数。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QAccessibleWidget(QWidget *, Role)` | 为 widget 创建无障碍对象并指定角色。 |
| `QAccessibleWidget(QWidget *, Role, QString)` | 创建时指定角色和名称。 |
| `widget()` | 返回被包装的 QWidget。 |
| `parentObject()` | 返回父对象。 |
| `role()` | 返回控件角色，如 Button、Client、Slider。 |
| `text(QAccessible::Text)` | 返回名称、描述、值等文本。 |
| `state()` | 返回可见、可用、焦点、选中等状态。 |
| `rect()` | 返回屏幕坐标中的可访问区域。 |
| `childCount()` / `child()` | 暴露可访问子对象。 |
| `parent()` / `indexOfChild()` | 描述可访问树关系。 |
| `focusChild()` | 返回当前焦点子对象。 |
| `actionNames()` | 返回支持的动作，如 press。 |
| `doAction()` | 执行无障碍动作。 |
| `keyBindingsForAction()` | 返回动作快捷键。 |
| `addControllingSignal()` | 声明某信号会影响被控制对象。 |

## 4. 关键用法

自定义控件工厂通常返回派生接口：

```cpp
class AccessibleKnob : public QAccessibleWidget {
public:
    AccessibleKnob(QWidget *w)
        : QAccessibleWidget(w, QAccessible::Slider) {}

    QString text(QAccessible::Text t) const override
    {
        if (t == QAccessible::Name)
            return "Gain";
        return QAccessibleWidget::text(t);
    }
};
```

然后通过 Qt 无障碍工厂机制注册，让辅助技术能获取它。

## 5. 使用场景

适合自定义 widget、复杂绘制控件、非标准按钮/滑块/图表交互、需要屏幕阅读器正确读出的专业软件。

普通 Qt 标准控件通常已有无障碍实现；重点检查自绘控件和图形化控件。

## 6. 常见坑与经验

无障碍名称不是 tooltip。名称要短而稳定，描述可以补充更多语义。

角色要准确。把滑块报成普通 Client，辅助技术就不知道它有值、范围和可调动作。

控件状态变化时要发送合适的无障碍事件，否则屏幕阅读器不会知道内容变了。
