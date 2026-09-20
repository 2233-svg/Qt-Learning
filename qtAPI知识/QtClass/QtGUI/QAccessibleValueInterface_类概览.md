# QAccessibleValueInterface：把数值控件作为一个“值”暴露给辅助技术

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleValueInterface>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 类型：抽象接口，通常与 `QAccessibleInterface` 一起实现

## 它解决什么问题

微调框、滑块、旋钮和滚动条在视觉上由轨道、按钮、刻度等部件组成，但用户的意图通常只是读取或调整一个值。`QAccessibleValueInterface` 让辅助技术以“当前值、最小值、最大值、最小步长”的简单模型访问它们，而不必逐个操作内部部件。

这是纯虚接口，常由同一个可访问对象与 `QAccessibleInterface` 一起实现。它尤其适合表示连续或离散的数值范围，而不是只用文字展示的状态标签。

## 哪些控件适合实现

- 有范围和值的微调框、滑块、旋钮和滚动条。
- 具有数值调节语义的自定义拨盘、时间轴缩放器、音量控制或进度显示。
- 可访问性树中应被视为一个整体的复合数值控件。

只读对象也可以实现本接口。进度条就是典型例子：辅助技术可以读取当前进度和范围，即使 `setCurrentValue()` 不执行更新。

## 实现契约

### 返回值必须来自同一数值体系

`currentValue()`、`minimumValue()`、`maximumValue()` 与 `minimumStepSize()` 都返回 `QVariant`，但应使用彼此可比较、可解释的同类数值，通常是 `int` 或 `double`。混用整数、字符串和不同单位会让平台后端无法稳定判断范围与增量。

正常情况下应保证：

```text
minimumValue() <= currentValue() <= maximumValue()
```

除非控件有明确、可访问后端能够理解的特殊语义。范围、步长和当前值应反映控件真实状态，不应是只为辅助技术临时拼出的另一套数值。

### `setCurrentValue()` 的边界

此函数是辅助技术请求改变真实值的入口。传入值超出允许范围时，应忽略请求，这是 Qt 文档规定的行为。实现者也应考虑值类型无法转换、控件只读、离散步长不匹配等情况，保持控件状态一致而不是强行接受无效请求。

成功改变后，应让 `currentValue()` 立即反映新状态，并按需发出 `QAccessibleValueChangeEvent`。不要只修改可访问性接口内部缓存。

### 最小步长不是装饰信息

`minimumStepSize()` 表示有意义的最小增量。自动化工具据此决定可调节粒度，程序化修改值时应使用它的整数倍。即便是只读进度条，也应提供有用值；Qt 文档建议此类控件返回范围除以 `100`。

## 设计和实现示意

```cpp
QVariant MyAccessibleDial::currentValue() const
{
    return dial()->value();
}

QVariant MyAccessibleDial::minimumStepSize() const
{
    return dial()->singleStep();
}

void MyAccessibleDial::setCurrentValue(const QVariant &value)
{
    bool ok = false;
    const int requested = value.toInt(&ok);
    if (!ok || requested < dial()->minimum() || requested > dial()->maximum())
        return;

    dial()->setValue(requested);
}
```

这只是三个接口的逻辑示意。完整实现还需覆盖最大值、最小值和虚析构语义，并在控件值真正改变时配合通知机制。

## 常见误区

- 把格式化文本如 `"50%"` 作为当前值。值接口应报告可计算的数值，文本标签由其他可访问性信息承担。
- 无视范围直接在 `setCurrentValue()` 中截断。Qt 对超范围请求的语义是忽略，调用方可据此重新读取当前值。
- 给只读进度条返回零步长。辅助技术仍需要了解合理的进度粒度。
- 只更新 `QVariant` 缓存而不更新实际控件，导致屏幕显示和辅助技术读到的数值不同。

## API 速查表

| API | 含义 | 实现重点 |
| --- | --- | --- |
| `virtual ~QAccessibleValueInterface()` | 虚析构函数。 | 经接口销毁派生对象必须安全；接口不定义控件所有权。 |
| `QVariant currentValue() const` | 返回当前实际值。 | 通常为 `int` 或 `double`，并与控件状态同步。 |
| `void setCurrentValue(const QVariant &value)` | 请求把控件设置为某个值。 | 超出允许范围必须忽略；成功后修改真实控件。 |
| `QVariant maximumValue() const` | 返回可接受的最大值。 | 与最小值、当前值使用同一类型和单位。 |
| `QVariant minimumValue() const` | 返回可接受的最小值。 | 应如实反映控件的有效范围。 |
| `QVariant minimumStepSize() const` | 返回有意义的最小调节增量。 | 程序化变更应是此值的倍数；只读进度条也要给合理粒度。 |
