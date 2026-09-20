# Qt QAccessibleActionInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleActionInterface>`  
> 所属模块：`Qt6::Gui`  
> 定位：向辅助技术公开可发现、可调用动作的纯虚接口

## 1. 它解决什么问题

`QAccessibleActionInterface` 让屏幕阅读器、语音控制或自动化辅助工具知道一个可访问对象可以执行哪些用户动作，并能以稳定的动作名调用它们。它通常与 `QAccessibleInterface` 由同一个 accessible object 实现。

它解决的不是快捷键系统，也不是业务命令总线：

- `actionNames()` 用于发现当前真正可调用的动作；
- `doAction()` 用非本地化动作名触发与正常用户交互等价的行为；
- `keyBindingsForAction()` 用于告诉辅助技术有哪些键盘方式；
- 本地化 API 只负责显示名字和说明，不改变机器协议动作名。

## 2. 实际使用场景

自定义无障碍对象为一个可勾选的控件提供标准 toggle 操作：

```cpp
QStringList ToggleAccessible::actionNames() const
{
    if (!control()->isEnabled())
        return {};
    return { QAccessibleActionInterface::toggleAction() };
}

void ToggleAccessible::doAction(const QString &actionName)
{
    if (actionName == QAccessibleActionInterface::toggleAction())
        control()->toggle(); // 使用与正常交互相同的业务入口
}

QStringList ToggleAccessible::keyBindingsForAction(
    const QString &actionName) const
{
    if (actionName == QAccessibleActionInterface::toggleAction())
        return { QStringLiteral("Space") };
    return {};
}
```

要点是复用控件的真实交互路径，而不是只改一个视觉状态。动作执行后若状态改变，还应由控件发出相应的无障碍状态或值变化事件。

## 3. 动作名是机器协议，不是显示文本

`actionNames()` 返回的名称永远不应本地化。调用方把这些名字再传回 `doAction()`，因此动作名必须在同一对象生命周期内保持可识别。

优先使用本类的标准动作名：

| 静态函数 | 语义 |
| --- | --- |
| `pressAction()` | 点击、按下或激活对象。 |
| `toggleAction()` | 切换复选框、单选按钮、开关等。 |
| `increaseAction()` | 增加值，如 spin box 或 slider。 |
| `decreaseAction()` | 减少值。 |
| `setFocusAction()` | 把键盘焦点设到对象。 |
| `showMenuAction()` | 显示上下文菜单，通常对应右键。 |
| `scrollLeftAction()` / `scrollRightAction()` | 水平滚动。 |
| `scrollUpAction()` / `scrollDownAction()` | 垂直滚动。 |
| `nextPageAction()` / `previousPageAction()` | 前后翻页。 |

只有标准名确实不能表达动作时才定义自定义名称。自定义名同样应稳定、非本地化，并必须自行实现本地化名称和说明。

## 4. 可发现性、启用状态与线程边界

`actionNames()` 只能列出当前可调用的动作。禁用控件、不可达菜单项、没有下一页的翻页器或已到滚动边界的滚动操作，不应继续公开为可调用动作。

`doAction()` 通常由辅助技术在 GUI 对象所属线程触发。实现中不要直接从其他线程修改控件；跨线程请求必须排队到 GUI 线程。动作应该具有与鼠标点击、按键激活或菜单触发一致的前置条件、验证和副作用。

不要用 action interface 绕过权限、禁用状态、确认对话框或业务校验。它的目标是让辅助技术拥有相同能力，不是更高权限。

## 5. 逐项 API 说明

### `virtual ~QAccessibleActionInterface()`

虚析构函数。接口本身不规定所有权；通常由实现它的 accessible interface 对象拥有或共同构成。不要通过辅助技术获取的接口指针擅自删除对象。

### `virtual QStringList actionNames() const = 0`

返回当前对象支持且可以立即调用的动作名列表。列表可以为空，且应按偏好顺序排列：用户最可能触发的动作放在前面。

返回的名称是非本地化机器名。禁用动作不能出现在列表里。若对象状态改变导致动作集合变化，应让辅助技术可观察到对应状态/结构更新。

### `virtual void doAction(const QString &actionName) = 0`

调用 `actionName` 指定的动作。参数必须是 `actionNames()` 返回的非本地化名称，而不是 `localizedActionName()` 的结果。

未知名称、过期名称或当前不可用的名称应安全地忽略或按实现记录诊断，不能导致控件崩溃。成功路径应复用普通用户交互的业务入口，以保持信号、状态、撤销逻辑和权限检查一致。

### `virtual QStringList keyBindingsForAction(const QString &actionName) const = 0`

返回可触发该动作的键盘绑定列表。结果用于辅助技术提示用户替代操作方式，可以为空。

绑定字符串应反映应用当前可用的真实键盘操作，不能虚构；当快捷键受平台、焦点上下文或用户设置影响时，返回能够确定的可用集合。未知动作返回空列表。

### `virtual QString localizedActionName(const QString &actionName) const`

返回动作的本地化显示名称。对标准动作名，基类实现可提供 Qt 的本地化结果；自定义动作应在派生类中覆盖。

返回值只用于向人展示，绝不能作为 `doAction()` 的参数。没有对应显示名时可以返回空字符串，但更好的实现是对所有自定义公开动作提供清晰名称。

### `virtual QString localizedActionDescription(const QString &actionName) const`

返回动作的本地化说明。对标准名可以使用基类实现；自定义动作应返回能说明效果的本地化文字。

说明应描述实际结果，如“显示选项菜单”，而不要把内部命令名暴露给用户。它不应包含快捷键本身，快捷键由 `keyBindingsForAction()` 报告。

### `static const QString &pressAction()`

返回标准“按下/点击/激活”动作名。适合按钮、链接、普通可激活条目和大多数 widget 激活行为。

### `static const QString &increaseAction()`

返回标准“增加值”动作名。适合值可上调的可访问对象；边界值已达到最大值时不应仍在 `actionNames()` 中公开。

### `static const QString &decreaseAction()`

返回标准“减少值”动作名。适合值可下调的对象；到最小值时应按真实可用性处理。

### `static const QString &showMenuAction()`

返回标准“显示菜单”动作名，通常对应对象的上下文菜单。只有确实有可展示菜单时才应公开。

### `static const QString &setFocusAction()`

返回标准“设置焦点”动作名。对象必须真的可接受焦点且所在窗口允许获得焦点。

### `static const QString &toggleAction()`

返回标准“切换”动作名，适合 checkbox、radio button、switch 等状态切换对象。三态控件应让执行结果符合真实的状态循环。

### `static QString scrollLeftAction()`、`scrollRightAction()`、`scrollUpAction()`、`scrollDownAction()`

返回四个标准滚动动作名。它们以值返回 `QString`，调用方可直接保存。仅在对应方向实际可滚动时公开；RTL、倒置外观或内容方向不应改变动作名的语义约定。

### `static QString nextPageAction()`、`previousPageAction()`

返回前页、后页的标准动作名。适合分页文档、向导、轮播或页表控件。没有相邻页时不要提供不可执行的动作。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `~QAccessibleActionInterface()` | 虚析构接口。 | 所有权由具体 accessible object 决定。 |
| 发现 | `actionNames()` | 返回当前可调用动作的非本地化名称列表。 | 可为空；按偏好排序；不包含禁用动作。 |
| 执行 | `doAction(const QString &)` | 执行指定动作。 | 参数来自 `actionNames()`，复用正常用户交互路径。 |
| 键盘 | `keyBindingsForAction(const QString &)` | 返回动作的键盘绑定。 | 只能报告真实可用绑定；未知动作返回空。 |
| 显示 | `localizedActionName(const QString &)` | 返回本地化动作名称。 | 不能作为机器动作名传回。 |
| 显示 | `localizedActionDescription(const QString &)` | 返回本地化动作说明。 | 自定义动作应覆盖实现。 |
| 标准名 | `pressAction()` | 点击/激活。 | 多数可激活控件的首选动作。 |
| 标准名 | `increaseAction()` / `decreaseAction()` | 调整数值。 | 到上/下界时不应暴露不可执行动作。 |
| 标准名 | `toggleAction()` | 切换状态。 | 用于勾选和开关，不替代 press 的一般激活语义。 |
| 标准名 | `setFocusAction()` | 设置键盘焦点。 | 对象必须真实可聚焦。 |
| 标准名 | `showMenuAction()` | 显示上下文菜单。 | 必须真的有可展示菜单。 |
| 标准名 | `scrollLeftAction()` / `scrollRightAction()` | 水平滚动。 | 仅在对应方向可滚动时公开。 |
| 标准名 | `scrollUpAction()` / `scrollDownAction()` | 垂直滚动。 | 仅在对应方向可滚动时公开。 |
| 标准名 | `nextPageAction()` / `previousPageAction()` | 翻页。 | 没有相邻页时不公开。 |

### 一句话总结

`QAccessibleActionInterface` 是辅助技术的动作协议：公开当前可执行的稳定非本地化动作名，用同一套真实业务路径执行它们，再分别提供面向用户的本地化名称、说明和键盘绑定。
