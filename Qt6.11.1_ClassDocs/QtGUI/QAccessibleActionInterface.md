# QAccessibleActionInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleActionInterface`

## 1. 先建立直觉

`QAccessibleActionInterface` 让屏幕阅读器、语音控制或自动化工具能“操作”一个对象，而不仅是朗读它。它把点击、切换、增减、显示菜单、聚焦、翻页和滚动等用户可执行意图抽象为稳定的动作名称。

它通常作为 `QAccessibleInterface` 的可选子接口出现。不要把它理解成普通 Qt 槽函数列表：辅助技术调用 `doAction()` 后，行为必须等价于用户通过鼠标、键盘或触摸触发同一控件。

## 2. 类说明

- 头文件：`#include <QAccessibleActionInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：抽象接口；由自定义 `QAccessibleInterface::interface_cast()` 返回。
- 典型对象：按钮、复选框、滑块、可展开项目、分页视图、可滚动画布。

若控件只是显示信息，不应勉强实现动作接口。若动作当前不可用，则不要把它放进 `actionNames()`。

## 3. API 速查

| API | 用途 |
|---|---|
| `actionNames()` | 返回当前可执行的非本地化动作名，按重要性排序。 |
| `doAction(name)` | 执行指定动作。 |
| `keyBindingsForAction(name)` | 返回可触发动作的快捷键列表。 |
| `localizedActionName(name)` | 将动作名转为用户语言中的短名称。 |
| `localizedActionDescription(name)` | 返回更完整的本地化动作说明。 |
| `pressAction()` | 标准“按下/激活”动作。 |
| `toggleAction()` | 标准“切换开关状态”动作。 |
| `increaseAction()` / `decreaseAction()` | 标准增减值动作。 |
| `showMenuAction()` | 打开关联菜单。 |
| `setFocusAction()` | 将键盘焦点移到对象上。 |
| `nextPageAction()` / `previousPageAction()` | 翻页。 |
| `scrollUp/Down/Left/RightAction()` | 按方向滚动。 |

## 4. 关键用法

```cpp
QStringList AccessibleMeter::actionNames() const
{
    if (!meter()->isEnabled())
        return {};
    return { increaseAction(), decreaseAction(), setFocusAction() };
}

void AccessibleMeter::doAction(const QString &name)
{
    if (name == increaseAction())
        meter()->stepUp();       // 与真实 UI 的操作路径一致
    else if (name == decreaseAction())
        meter()->stepDown();
    else if (name == setFocusAction())
        meter()->setFocus();
}
```

不要自行拼接 `"increase"` 或把本地化文字作为协议值；始终使用本类提供的标准动作名称。`doAction()` 的参数来自 `actionNames()`，不是展示给终端用户的翻译文本。

## 5. 实现策略

| 控件语义 | 推荐动作 | 关键状态 |
|---|---|---|
| 普通按钮 | `pressAction()` | 禁用时不返回动作。 |
| 复选框、开关 | `toggleAction()` | 同步更新 `checked` / mixed 状态并发送事件。 |
| 滑块、步进器 | `increaseAction()`、`decreaseAction()` | 同时实现 `QAccessibleValueInterface`。 |
| 菜单按钮 | `pressAction()`、`showMenuAction()` | 菜单可见性变化要通知。 |
| 树节点 | `toggleAction()` | 语义应是展开/折叠，维护 `expanded`。 |
| 视图/页面容器 | 翻页或滚动动作 | 不要把每个视觉手势都暴露为动作。 |

## 6. 使用场景

这个接口适合那些“辅助技术需要替用户执行动作”的控件：自绘按钮、非 QWidget 的图形节点、可展开面板、虚拟列表项、画布上的缩放控件、没有原生控件语义的开关和步进器。若对象只是文本说明或状态展示，只实现名称、角色、状态和值接口即可，不要为了完整而暴露无意义动作。

## 7. 常见坑与经验

- `actionNames()` 是当前状态的快照。控件禁用、到达最小值或没有下一页时，应移除相应动作。
- `doAction()` 不能只改内部变量；必须走正常业务路径，以获得重绘、信号、验证、撤销栈和无障碍事件。
- 快捷键字符串应反映真实可用按键，不要为“方便读屏”虚构绑定。
- 动作名称非本地化，本地化只由 `localizedActionName()` / `localizedActionDescription()` 处理。
- 动作调用通常发生在 GUI 语义上下文，后台线程不得直接操纵 QWidget。

## 8. 知识点覆盖

- 可访问性动作协议与标准动作名称
- 自定义接口的动态能力暴露
- 可用性状态和动作列表同步
- 本地化展示与机器协议值分离
- 通过同一业务路径保持交互一致性
