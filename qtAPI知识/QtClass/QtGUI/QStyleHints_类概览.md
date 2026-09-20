# Qt QStyleHints：平台交互习惯与应用级输入参数

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleHints>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`  
> 类型定位：由 `QGuiApplication` 提供的平台风格提示对象

## 1. 它解决什么问题

`QStyleHints` 集中提供操作系统、窗口系统和 Qt 平台插件使用的交互参数，例如：

- 双击间隔、双击距离和长按间隔；
- 开始拖动所需的距离、时间和速度；
- 键盘自动重复速率与连续输入间隔；
- 光标闪烁时间；
- 触控获取焦点、单击激活和 hover 效果；
- 上下文菜单触发时机；
- Tab 焦点移动习惯；
- 系统颜色方案、密码遮罩字符；
- 是否在右到左环境中使用平台扩展。

它解决的是“应用如何遵循当前平台输入习惯”的问题。应用不应把 Windows、macOS、Linux 或触控平台的经验值硬编码到业务逻辑中，而应读取 `QStyleHints`。

## 2. 如何取得对象

`QStyleHints` 构造函数是 private，普通应用不直接 `new QStyleHints`。在 `QGuiApplication` 或 `QApplication` 创建后取得：

```cpp
#include <QGuiApplication>
#include <QStyleHints>

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    QStyleHints *hints = app.styleHints();
    qDebug() << hints->startDragDistance()
             << hints->mouseDoubleClickInterval();
    return app.exec();
}
```

Qt Widgets 应用通常使用 `QApplication`，它继承 `QGuiApplication`，同样可以访问 style hints。

## 3. 只读平台提示与可设置参数

属性可以分成三类：

### 3.1 平台只读/常量提示

例如：

- `fontSmoothingGamma`；
- `keyboardAutoRepeatRateF`；
- `passwordMaskCharacter`；
- `showIsFullScreen`；
- `singleClickActivation`；
- `startDragVelocity`；
- `useRtlExtensions`。

这些属性没有应用 setter，应用应读取并适配。

### 3.2 可由应用调整的参数

例如：

- `setMouseDoubleClickInterval()`；
- `setMousePressAndHoldInterval()`；
- `setStartDragDistance()`；
- `setStartDragTime()`；
- `setKeyboardInputInterval()`；
- `setCursorFlashTime()`；
- `setShowShortcutsInContextMenus()`；
- `setContextMenuTrigger()`；
- `setTabFocusBehavior()`；
- `setUseHoverEffects()`；
- `setWheelScrollLines()`；
- `setMouseQuickSelectionThreshold()`；
- `setColorScheme()`。

这些 setter 调整的是当前 Qt 应用看到的提示，不是修改操作系统的全局设置。除非产品确实需要统一交互策略，否则应优先尊重平台默认值。

### 3.3 Qt 版本相关项

- `colorScheme` 属性自 Qt 6.5 起提供，`setColorScheme()`/`unsetColorScheme()` 的公开使用按 Qt 6.8 语义核对；
- `keyboardAutoRepeatRateF` 自 Qt 6.5 起提供；
- `menuSelectionWraps` 和 `accessibility` 自 Qt 6.10 起提供；
- 整数形式 `keyboardAutoRepeatRate()` 自 Qt 6.5 起弃用，使用浮点形式替代。

## 4. 关键单位与实际含义

### 鼠标和拖动

| API | 含义 |
| --- | --- |
| `mouseDoubleClickInterval()` | 两次点击被视为双击的最大时间间隔，单位通常为毫秒 |
| `mouseDoubleClickDistance()` | 两次点击允许的最大移动距离，单位是平台逻辑像素 |
| `mousePressAndHoldInterval()` | 按住鼠标/触控多久触发长按，单位通常为毫秒 |
| `startDragDistance()` | 从按下位置移动多少才开始拖动 |
| `startDragTime()` | 按下后至少等待多久才允许开始拖动 |
| `startDragVelocity()` | 适用于平台拖动判断的速度提示 |

不要只用距离判断拖动；触控和高 DPI 平台还可能受时间、速度和设备类型影响。

### 键盘

| API | 含义 |
| --- | --- |
| `keyboardInputInterval()` | 连续键盘输入之间的时间间隔提示，常用于多键序列和输入节奏 |
| `keyboardAutoRepeatRateF()` | 键盘自动重复速率的浮点表示 |
| `keyboardAutoRepeatRate()` | 旧的整数速率 API，Qt 6.5 起弃用 |
| `cursorFlashTime()` | 文本光标闪烁时间提示，通常为毫秒 |

自动重复速率与“多久开始重复”不是同一个量，不要把速率当成延迟。

### 触控和选择

- `touchDoubleTapDistance()`：触控双击/双 tap 的距离阈值；
- `setFocusOnTouchRelease()`：只读平台提示，表示触控结束时是否设置焦点；
- `mouseQuickSelectionThreshold()`：快速选择相关阈值，可读写。

## 5. 属性语义

### 5.1 `accessibility : const QAccessibilityHints *`

Qt 6.10 起提供的只读辅助功能提示对象。返回指针由 Qt 管理，调用方不负责释放。它是平台/应用辅助功能状态的入口，不应缓存为跨 `QGuiApplication` 生命周期的裸指针。

### 5.2 `colorScheme : Qt::ColorScheme`

读取当前颜色方案，并可通过 `setColorScheme()` 覆盖或用 `unsetColorScheme()` 恢复 `Unknown`/平台默认策略。它是应用级颜色方案提示，不会自动替换所有 widget 的 palette 或应用样式。

### 5.3 `contextMenuTrigger : Qt::ContextMenuTrigger`

控制上下文菜单更偏向按下触发还是释放触发。Qt 6.8 起可设置。它影响 Qt 对上下文菜单手势的解释，但不替应用自动创建菜单。

### 5.4 `showShortcutsInContextMenus : bool`

控制上下文菜单中是否显示关联 action 的快捷键文本。它不改变 `QShortcut` 的匹配，也不影响 action 本身是否有 shortcut。

### 5.5 `tabFocusBehavior : Qt::TabFocusBehavior`

控制 Tab 键移动焦点时的平台习惯。可通过 getter、setter 和 changed 信号访问。自定义焦点链时，应尊重该 hint，避免强制覆盖平台用户习惯。

### 5.6 `useHoverEffects : bool`

控制平台是否使用 hover 效果。它是应用层提示和开关，不会替自定义控件自动绘制 hover 样式。

## 6. 属性和函数逐项语义

### 鼠标、触控和拖动

- `setMouseDoubleClickInterval(int)` / `mouseDoubleClickInterval()`：设置/读取双击时间阈值。
- `mouseDoubleClickDistance()`：读取双击距离阈值，只读。
- `setMousePressAndHoldInterval(int)` / `mousePressAndHoldInterval()`：设置/读取长按间隔。
- `setStartDragDistance(int)` / `startDragDistance()`：设置/读取拖动距离阈值。
- `setStartDragTime(int)` / `startDragTime()`：设置/读取拖动时间阈值。
- `startDragVelocity()`：读取拖动速度提示，只读。
- `touchDoubleTapDistance()`：读取触控双 tap 距离，只读。
- `setMouseQuickSelectionThreshold(int)` / `mouseQuickSelectionThreshold()`：设置/读取快速选择阈值。

负值、零值和极小阈值会使交互变得异常，设置应用级参数时应采用产品测试过的正值，并考虑平台单位。

### 键盘和光标

- `setKeyboardInputInterval(int)` / `keyboardInputInterval()`：设置/读取键盘连续输入间隔。
- `keyboardAutoRepeatRateF()`：读取浮点自动重复速率。
- `keyboardAutoRepeatRate()`：读取旧整数速率，Qt 6.5 起弃用。
- `setCursorFlashTime(int)` / `cursorFlashTime()`：设置/读取光标闪烁时间。

关闭光标闪烁可使用平台允许的值或由文本控件策略决定，不要让自定义控件仅靠自己的定时器与系统输入节奏脱节。

### 显示和平台习惯

- `showIsFullScreen()`：读取平台是否建议显示 full-screen 状态相关文案/行为提示。
- `showIsMaximized()`：读取平台是否建议显示 maximized 状态相关文案/行为提示。
- `singleClickActivation()`：读取平台是否偏好单击激活。
- `useRtlExtensions()`：读取平台是否使用 RTL 扩展行为。
- `setFocusOnTouchRelease()`：读取触控结束时设置焦点的提示。
- `fontSmoothingGamma()`：读取字体平滑 gamma 提示。
- `passwordMaskDelay()`：读取密码输入最后字符显示后转为遮罩的延迟。
- `passwordMaskCharacter()`：读取平台密码遮罩字符。
- `menuSelectionWraps()`：Qt 6.10 起读取菜单选择到末尾后是否循环。

这些只读提示的具体展示效果通常由 Qt 控件或 style 使用。自定义控件可参考它们，但不应把提示解释为强制平台行为。

### 上下文菜单、焦点和颜色

- `showShortcutsInContextMenus()` / `setShowShortcutsInContextMenus(bool)`：读取/设置上下文菜单是否展示快捷键。
- `contextMenuTrigger()` / `setContextMenuTrigger(Qt::ContextMenuTrigger)`：读取/设置上下文菜单触发时机。
- `tabFocusBehavior()` / `setTabFocusBehavior(Qt::TabFocusBehavior)`：读取/设置 Tab 焦点策略。
- `colorScheme()` / `setColorScheme(Qt::ColorScheme)`：读取/设置颜色方案。
- `unsetColorScheme()`：恢复未指定/平台默认颜色方案。
- `accessibility()`：Qt 6.10 起读取辅助功能提示指针。

## 7. changed 信号

`QStyleHints` 提供以下变化信号：

```cpp
void cursorFlashTimeChanged(int);
void keyboardInputIntervalChanged(int);
void mouseDoubleClickIntervalChanged(int);
void mousePressAndHoldIntervalChanged(int);
void startDragDistanceChanged(int);
void startDragTimeChanged(int);
void tabFocusBehaviorChanged(Qt::TabFocusBehavior);
void useHoverEffectsChanged(bool);
void showShortcutsInContextMenusChanged(bool);
void contextMenuTriggerChanged(Qt::ContextMenuTrigger);
void wheelScrollLinesChanged(int);
void mouseQuickSelectionThresholdChanged(int);
void colorSchemeChanged(Qt::ColorScheme);
```

自定义控件应连接这些信号更新自身行为，而不是在定时器中轮询：

```cpp
connect(app.styleHints(), &QStyleHints::startDragDistanceChanged,
        this, &Canvas::updateDragThreshold);
```

只读常量提示通常没有 changed 信号，因为它们在当前应用生命周期内不通过公开 setter 改变。

## 8. 生命周期、线程和所有权

`QStyleHints` 由 `QGuiApplication` 管理，不应手动删除。它是 GUI 全局对象，通常只在 GUI 线程访问和修改。

不要在 `QGuiApplication` 构造前缓存 `styleHints()`。应用退出后也不要继续使用该指针。若后台线程需要阈值，应在 GUI 线程读取后复制纯数值，再传给后台逻辑。

## 9. 常见误区与排查顺序

### 9.1 直接构造 QStyleHints

构造函数是 private。使用 `QGuiApplication::styleHints()`。

### 9.2 把平台 hint 当成硬性保证

只读属性描述平台偏好，实际 widget/style 是否使用由 Qt 和应用实现决定。

### 9.3 把 setter 当成修改系统设置

setter 只影响当前 Qt 应用的 style hints，不会修改操作系统鼠标或键盘设置。

### 9.4 混淆距离、时间和速度

开始拖动需要综合 distance/time/velocity。只使用某一个阈值会导致触控或慢速鼠标体验异常。

### 9.5 把自动重复速率当成重复延迟

`keyboardAutoRepeatRateF()` 是速率，`keyboardInputInterval()` 是输入间隔，二者不是同一单位和语义。

### 9.6 忽略信号

用户可能在系统设置中改变双击间隔、拖动距离或颜色方案。应用若缓存值，应连接对应 changed 信号。

### 9.7 在非 GUI 线程写全局 hint

这会造成竞态或违反 GUI 对象线程约定。跨线程只传递复制后的数值。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 获取 | `QGuiApplication::styleHints()` | 获取全局 style hints | 需先创建 QGuiApplication |
| 鼠标 | `setMouseDoubleClickInterval()` / `mouseDoubleClickInterval()` | 双击时间阈值 | 通常为毫秒；setter 是应用级 |
| 鼠标 | `mouseDoubleClickDistance()` | 双击距离阈值 | 只读，通常是逻辑像素 |
| 鼠标 | `setMousePressAndHoldInterval()` / `mousePressAndHoldInterval()` | 长按间隔 | 不要和双击间隔混用 |
| 拖动 | `setStartDragDistance()` / `startDragDistance()` | 拖动距离阈值 | 需结合时间和设备 |
| 拖动 | `setStartDragTime()` / `startDragTime()` | 拖动时间阈值 | 通常为毫秒 |
| 拖动 | `startDragVelocity()` | 拖动速度提示 | 只读平台 hint |
| 键盘 | `setKeyboardInputInterval()` / `keyboardInputInterval()` | 键盘输入间隔 | 不是自动重复速率 |
| 键盘 | `keyboardAutoRepeatRateF()` | 浮点自动重复速率 | Qt 6.5 起提供，只读 |
| 键盘 | `keyboardAutoRepeatRate()` | 整数自动重复速率 | Qt 6.5 起弃用 |
| 光标 | `setCursorFlashTime()` / `cursorFlashTime()` | 光标闪烁时间 | 影响应用控件的节奏 |
| 触控 | `touchDoubleTapDistance()` | 触控双 tap 距离 | 只读平台 hint |
| 选择 | `setMouseQuickSelectionThreshold()` / `mouseQuickSelectionThreshold()` | 快速选择阈值 | 依赖控件交互实现 |
| 显示 | `showIsFullScreen()` / `showIsMaximized()` | 读取平台显示习惯 hint | 不是窗口状态 setter |
| 密码 | `passwordMaskDelay()` / `passwordMaskCharacter()` | 密码遮罩策略 | 只读 |
| 平台 | `fontSmoothingGamma()` | 字体平滑 gamma | 只读 |
| 平台 | `useRtlExtensions()` | RTL 扩展提示 | 只读 |
| 平台 | `singleClickActivation()` | 单击激活提示 | 只读 |
| 平台 | `setFocusOnTouchRelease()` | 触控结束焦点提示 | 只读 getter |
| 菜单 | `showShortcutsInContextMenus()` / `setShowShortcutsInContextMenus()` | 上下文菜单显示快捷键 | 不改变 shortcut 匹配 |
| 菜单 | `contextMenuTrigger()` / `setContextMenuTrigger()` | 设置菜单触发时机 | Qt 6.8 起可设置 |
| 菜单 | `menuSelectionWraps()` | 菜单选择是否循环 | Qt 6.10 起，只读 |
| 焦点 | `tabFocusBehavior()` / `setTabFocusBehavior()` | Tab 焦点行为 | 应尊重平台习惯 |
| 视觉 | `useHoverEffects()` / `setUseHoverEffects()` | hover 效果提示/开关 | 不自动绘制样式 |
| 颜色 | `colorScheme()` / `setColorScheme()` | 读取/设置颜色方案 | 应用级，不自动替换 palette |
| 颜色 | `unsetColorScheme()` | 恢复平台默认方案 | 相当于设置 Unknown |
| 辅助功能 | `accessibility()` | 获取辅助功能提示 | Qt 6.10 起；不负责释放 |
| 信号 | `*Changed(...)` 信号族 | 响应可变 hint 更新 | 优先响应而非轮询 |

---

### 一句话总结

`QStyleHints` 是 Qt 对平台交互习惯的统一入口：先通过 `QGuiApplication::styleHints()` 获取，再区分只读提示与应用可覆盖参数，按正确单位使用距离/时间/速度/速率，并通过 changed 信号保持自定义控件与平台设置同步。
