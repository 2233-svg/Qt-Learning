# QStyleHints
> Qt 6.11.1 · Qt GUI · 来自 `QStyleHints`

## 1. 先建立直觉

`QStyleHints` 提供平台交互习惯和用户偏好：双击间隔、拖拽阈值、光标闪烁、滚轮行数、是否单击激活、系统浅色/深色方案、触摸焦点行为等。它让应用跟随系统体验，而不是把交互参数写死。

通过 `QGuiApplication::styleHints()` 获取全局对象。

## 2. 类说明

- 头文件：`#include <QStyleHints>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 获取方式：`QGuiApplication::styleHints()`
- 协作类：`QGuiApplication`、事件处理、控件或自绘 UI

多数属性是平台只读提示；少数如 `colorScheme`、`showShortcutsInContextMenus`、`useHoverEffects`、`contextMenuTrigger` 可以设置或覆盖。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `colorScheme()` / `setColorScheme()` / `unsetColorScheme()` | 读取或覆盖浅色/深色方案 |
| `accessibility()` | Qt 6.10 起读取无障碍提示，如高对比度需求 |
| `contextMenuTrigger()` / `setContextMenuTrigger()` | 设置右键菜单由 press 还是 release 触发 |
| `mouseDoubleClickInterval()` / `mouseDoubleClickDistance()` | 双击时间和移动距离阈值 |
| `mousePressAndHoldInterval()` | 长按触发阈值 |
| `startDragDistance()` / `startDragTime()` / `startDragVelocity()` | 拖拽判定阈值 |
| `keyboardInputInterval()` / `keyboardAutoRepeatRateF()` | 键盘连续输入与自动重复 |
| `cursorFlashTime()` | 文本光标闪烁周期 |
| `wheelScrollLines()` | 滚轮每步建议滚动行数 |
| `tabFocusBehavior()` | Tab 键焦点策略 |
| `singleClickActivation()` | 平台是否倾向单击激活 |
| `useHoverEffects()` / `setUseHoverEffects()` | 是否启用 hover 效果 |
| `showShortcutsInContextMenus()` | 上下文菜单是否显示快捷键 |
| `passwordMaskCharacter()` / `passwordMaskDelay()` | 密码输入显示策略 |

## 4. 关键用法

自定义拖拽判定：

```cpp
const int threshold = qApp->styleHints()->startDragDistance();
if ((event->position().toPoint() - pressPos).manhattanLength() >= threshold)
    startDrag();
```

跟随系统配色：

```cpp
auto *hints = qGuiApp->styleHints();
connect(hints, &QStyleHints::colorSchemeChanged, this, &ThemeController::reload);
```

`colorSchemeChanged` 发出时，旧 palette 可能仍有效；应用自定义颜色更可靠的刷新点通常还包括 `PaletteChange` 或 `ApplicationPaletteChange` 事件。

## 5. 使用场景

- 自绘控件实现双击、拖拽、长按时遵循平台阈值。
- 主题系统响应浅色/深色变化。
- 菜单和快捷键显示与平台习惯一致。
- 触摸设备上处理焦点、长按和双击距离。
- 无障碍模式下调整对比度、动画和 hover 策略。

## 6. 常见坑与经验

- 不要随意覆盖 `contextMenuTrigger`，这会改变用户在平台上的肌肉记忆。
- `setColorScheme()` 是提示，不保证所有平台都能强制切换。
- 拖拽距离要用平台阈值，不要写死 5 或 10 像素；高 DPI 和触摸设备差异很大。
- `wheelScrollLines()` 可能为特殊值或平台策略变化，自绘滚动要允许用户设置影响。
- `QStyleHints` 是全局提示，不代表某个控件一定采用同样策略；Widgets style 仍可能做自己的适配。

## 7. 知识点覆盖

本页覆盖：平台交互阈值、系统颜色方案、无障碍提示、拖拽/双击/长按、键盘重复、滚轮策略、上下文菜单触发。
