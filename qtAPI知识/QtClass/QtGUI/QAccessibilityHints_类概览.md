# Qt QAccessibilityHints 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibilityHints>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`  
> 自 Qt 6.10 引入  
> 定位：读取操作系统无障碍显示偏好的只读 QObject

## 1. 它解决什么问题

`QAccessibilityHints` 把平台提供的无障碍偏好暴露给 Qt 应用。当前公开的偏好是系统的对比度模式：应用和 Qt 样式可据此调整调色板颜色、轮廓或其他视觉提示，让界面更符合用户在操作系统层面选择的可访问性设置。

它不是“开启无障碍功能”的全局开关，也不是保存应用自定义设置的配置类：

- 不负责屏幕阅读器事件或可访问对象树；
- 不替代 `QPalette`、主题系统或控件样式；
- 不直接修改控件颜色；
- 不提供 setter，因为值来自平台；
- 不保证所有平台都能报告比默认状态更细的偏好。

通常不直接构造它，而是通过 `QGuiApplication::styleHints()->accessibility()` 取得 Qt 管理的实例。

## 2. 实际使用场景

### 2.1 根据系统对比度偏好调整自绘控件

```cpp
auto *hints = QGuiApplication::styleHints()->accessibility();

connect(hints, &QAccessibilityHints::contrastPreferenceChanged,
        this, [this](Qt::ContrastPreference preference) {
    updateVisualMetrics(preference);
    update();
});

updateVisualMetrics(hints->contrastPreference());
```

自绘控件可以在高对比度偏好下加粗焦点环、提高边框和背景差异，或为图标增加轮廓。应优先从 `QPalette` 的颜色角色取色，不要把“高对比度”简单实现成全局硬编码黑白。

### 2.2 让非 QWidget UI 与系统偏好保持一致

Qt Quick 自定义 item、基于 `QWindow` 的界面或导出预览工具没有现成控件样式可以依赖时，可以监听该对象的变化，在应用运行中更新自己的渲染参数。

## 3. 获取、所有权与线程

典型获取方式：

```cpp
QAccessibilityHints *hints =
    QGuiApplication::styleHints()->accessibility();
```

该指针由 Qt 管理，调用方不应删除、重新设 parent 或长期跨应用对象生命周期保存它。应用关闭过程中 `QGuiApplication` 和 `QStyleHints` 会销毁，晚于它们使用该指针是不安全的。

作为 `QObject`，它通常属于 GUI 线程。平台设置变化会通过事件循环进入对象并发射信号；不要从后台线程直接读取或连接后修改 GUI。后台任务需要响应时，用 queued signal/slot 把结果传回自己的线程。

## 4. 对比度偏好的正确理解

`contrastPreference` 的类型是 `Qt::ContrastPreference`。它表示系统表达的偏好，而不是对当前每个屏幕像素对比度的测量结果。

因此：

- 不能据此推断当前窗口一定使用某套特定色值；
- 不能替代对 `QGuiApplication::palette()` 或控件 palette 的读取；
- 平台切换主题、调色板或显示器时，仍可能需要处理相关 palette 更新；
- 应把它理解成样式决策的一个输入，而不是唯一输入；
- 不支持该信息的平台可能只能给出默认/无偏好的值，代码要有普通显示回退。

Qt 自带样式会利用该偏好调整 palette 和轮廓；应用若又强制覆盖颜色，可能反而破坏高对比度效果。

## 5. 逐项 API 说明

### `explicit QAccessibilityHints(QObject *parent = nullptr)`

构造一个无障碍提示对象，可选地交给 `parent` 管理。公开构造函数主要服务于 Qt 的对象模型和实现扩展；正常应用代码优先使用 `QStyleHints::accessibility()` 的共享实例。

自行构造时不应假设对象马上具备与 Qt 全局样式提示实例相同的更新来源或生命周期语义。若只是读取平台设置，直接取得共享对象更可靠。

### `~QAccessibilityHints() override`

销毁对象。由父对象拥有时会随父对象析构。通过 `QStyleHints::accessibility()` 得到的对象由 Qt 所有，调用方不能手动销毁。

### `Qt::ContrastPreference contrastPreference() const`

返回系统当前的对比度偏好。该函数是只读查询，不会触发主题刷新，也不会修改 palette。

返回值应与信号参数一起使用：首次创建 UI 时调用它取得初值，运行期间连接 `contrastPreferenceChanged()` 处理变化。不要用高频轮询代替信号。

### `void contrastPreferenceChanged(Qt::ContrastPreference contrastPreference)`

当系统报告的对比度偏好改变时发射。槽函数应把参数视为新的完整偏好状态，而不是增量变化。

收到信号后通常只需要更新样式依赖的缓存、请求控件重绘或重新计算自己的颜色选择。不要在槽中同步执行耗时 IO，也不要直接假设所有控件的 palette 已经在该调用栈中完成更新。

### `bool event(QEvent *event)`（保护重写）

重写 `QObject::event()`，用于处理平台/Qt 事件并维护提示状态。应用层不应主动调用它；如果为了测试或扩展而继承该类，必须先交给基类处理不认识的事件，并避免破坏属性变化和信号发射链路。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `QAccessibilityHints(QObject *)` | 构造提示对象。 | 常规代码优先使用 `QStyleHints::accessibility()` 返回的 Qt 管理实例。 |
| 生命周期 | `~QAccessibilityHints()` | 销毁对象。 | 不要删除 Qt 管理的共享实例。 |
| 属性/查询 | `contrastPreference()` | 返回系统对比度偏好。 | 是偏好，不是实际 palette 或像素对比度测量。 |
| 信号 | `contrastPreferenceChanged(Qt::ContrastPreference)` | 通知系统偏好变化。 | 用于刷新视觉决策，不要高频轮询。 |
| 保护 | `event(QEvent *)` | 处理内部平台事件。 | 框架调用；应用层不要直接调用。 |

### 一句话总结

`QAccessibilityHints` 是系统无障碍显示偏好的只读入口。通常从 `QStyleHints::accessibility()` 取得它，用初始查询加变化信号同步自绘 UI，同时让 `QPalette` 和 Qt 样式继续承担实际取色工作。
