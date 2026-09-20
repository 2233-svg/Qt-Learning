# QAccessibilityHints

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibilityHints`

## 1. 先建立直觉

`QAccessibilityHints` 将操作系统的无障碍偏好暴露给 Qt 应用。Qt 6.11.1 中它目前提供的是用户对**对比度**的偏好，使应用能在高对比需求下调整自绘控件、图表、画布或非标准配色。

这不是一个“开启无障碍模式”的开关，也不是对调色板的强制修改。它提供的是系统意图；应用仍要决定如何让文本、焦点框、图标边缘和状态提示真正可辨识。

## 2. 类说明

- 头文件：`#include <QAccessibilityHints>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`；实例由 `QGuiApplication::styleHints()` 关联提供，不应自行创建或删除。
- 版本：`contrastPreference` 在 Qt 6.10 引入。

典型入口：

```cpp
QAccessibilityHints *hints = QGuiApplication::styleHints()
    ->accessibilityHints();
```

对象随应用存活，系统设置改变时会发送信号。读取它不要求屏幕阅读器正在运行。

## 3. API 速查

| API | 用途 |
|---|---|
| `contrastPreference()` | 读取系统当前的 `Qt::ContrastPreference`。 |
| `contrastPreferenceChanged(preference)` | 系统对比度偏好改变时通知 UI 更新。 |
| `contrastPreference` 属性 | 上述 getter 和通知的属性形式，Qt 6.10 起可用。 |
| `event()` | Qt 内部接收平台设置变化；一般不需重写。 |

`Qt::ContrastPreference` 应被理解为偏好提示：例如无特别偏好、偏好更高对比度或偏好降低对比度。应用不能把它简单等同于某个平台的“深色模式”，深浅色外观仍应通过调色板、样式或其他平台提示处理。

## 4. 关键用法

```cpp
auto *hints = QGuiApplication::styleHints()->accessibilityHints();

auto applyContrastPolicy = [this](Qt::ContrastPreference preference) {
    highContrastMode = preference == Qt::ContrastPreference::HighContrast;
    update();
};

applyContrastPolicy(hints->contrastPreference());
connect(hints, &QAccessibilityHints::contrastPreferenceChanged,
        this, applyContrastPolicy);
```

正确顺序是“先读当前值，再订阅变化”。只连接信号会遗漏程序启动时已经存在的系统偏好。

应用对 `HighContrast` 的实际响应通常包括：

- 让文字与背景达到足够对比，而不是只提高饱和度。
- 为键盘焦点提供清晰、不仅依赖颜色的轮廓。
- 让禁用、选中、错误、悬停等状态可从形状、文字或图标区分。
- 避免在自绘画布中用相近灰度表达重要边界。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 自绘 `QWidget`、`QQuickPaintedItem` 或图表 | 根据偏好选择边框、网格、标记线和焦点指示的对比策略。 |
| 设计系统/主题管理器 | 将偏好映射到一组语义色，不要在各控件散落硬编码颜色。 |
| 带状态的图标按钮 | 让禁用、选中与焦点状态具有额外的形状或轮廓提示。 |
| 纯 Qt Widgets 标准控件 | Qt 样式通常已处理一部分；自定义 stylesheet 仍需自行验证。 |

## 6. 常见坑与经验

- 不要缓存一次查询结果后永久使用；系统设置可以在应用运行中改变。
- 不要为了“高对比”把所有背景强制改成黑白，这可能破坏品牌色、图像和用户选择的主题；应以可读性为目标。
- 这不是屏幕阅读器 API。可访问名称、角色、值和事件仍由 `QAccessible` 体系负责。
- `QAccessibilityHints` 是应用级对象，勿跨线程直接操作 UI；收到变化信号后在 GUI 线程刷新视图。
- 针对高对比的界面应该同时用键盘焦点、缩放和读屏测试验证，不能只凭肉眼看一张截图。

## 7. 知识点覆盖

- 平台无障碍偏好与应用主题策略
- 初始状态读取与运行时设置变化
- 高对比设计：文字、焦点、状态与非颜色线索
- Qt 标准控件与自绘界面的责任边界
- `QAccessibilityHints` 和 `QAccessible` 的分工
