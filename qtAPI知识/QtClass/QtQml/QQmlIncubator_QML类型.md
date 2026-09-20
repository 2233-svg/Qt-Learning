# QQmlIncubator：异步创建 QML 对象的状态与回调容器

> Qt 6.11.1 · `#include <QQmlIncubator>` · 模块：`Qt6::Qml`

`QQmlIncubator` 允许 `QQmlComponent` 创建对象时不一次性占满 UI 线程。它适合列表离屏委托、复杂页面预热和资源受限设备上的动态对象创建。

它不是 QObject，也没有信号；需派生并覆写 `statusChanged()`，或在自己的调度点检查状态。它也不是后台线程构造器：没有 `QQmlIncubationController` 的 engine 会让所有模式同步完成。

## 基本路径

```cpp
class PanelIncubator final : public QQmlIncubator
{
protected:
    void statusChanged(Status status) override
    {
        if (status == Ready)
            usePanel(object());
        else if (status == Error)
            qWarning() << errors();
    }
};

PanelIncubator incubator(QQmlIncubator::Asynchronous);
incubator.setInitialProperties({{u"title"_s, u"Settings"_s}});
component.create(incubator);
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。`setInitialProperties()` 要在 `component.create(incubator, ...)` 之前设置。

## 三种创建模式

| 模式 | 行为 | 适用边界 |
| --- | --- | --- |
| `Asynchronous` | 在有 controller 时异步创建 | 对象不需要立刻可用时使用。 |
| `AsynchronousIfNested` | 外层异步时加入其任务，否则同步 | 需要“正常单独创建立即可见、嵌套异步不破坏帧预算”时的常用选择。 |
| `Synchronous` | 调用返回时已 Ready 或 Error | 主要用于统一 API；通常不如直接 `component.create()`。 |

缺少 `QQmlIncubationController` 时，上述三种都会同步创建。`QQuickWindow` / `QQuickView` / `QQuickWidget` 一般已安装 controller，裸 `QQmlEngine` 默认没有。

## 状态、对象和清理

`Null` 表示尚未开始或已清理；`Loading` 表示正在创建；`Ready` 后才能通过 `object()` 取得对象；`Error` 时从 `errors()` 读取诊断。

`forceCompletion()` 会把进行中的创建同步完成，调用后不再是 Loading。它可处理“原本预加载、现在用户立刻需要”的情况，但会把延后的卡顿集中到当前调用点。

`clear()` 中止进行中的孵化；若当前已 Ready，创建出的对象**不会被删除**。这意味着对象所有权要在 Ready 时明确交接，不能误以为销毁 incubator 或调用 clear 会自动回收对象。

## 高级钩子

`setInitialState(object)` 在对象首次创建后、复杂绑定与 `componentComplete()` 前调用，适合设置初始顶层属性。不要依赖任何具体 binding 一定在它前后执行：Qt 可把某些常量表达式提前折叠，也可在不同版本、qmlcachegen 配置下改变执行时机。

`statusChanged(status)` 用于派生类接收进度。回调中只有 `Ready` 才能安全取 `object()`；`Error` 应处理 `errors()`，而不是继续假设创建成功。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlIncubator(mode)` | 创建孵化器 | 默认 `Asynchronous`，但无 controller 时仍同步。 |
| `IncubationMode::Asynchronous` | 请求异步创建 | 需 engine controller 才实际异步。 |
| `IncubationMode::AsynchronousIfNested` | 条件异步创建 | 通常适合组件内部委托。 |
| `IncubationMode::Synchronous` | 同步创建 | 多数场景直接用 `QQmlComponent::create()` 更直观。 |
| `status()` / `isNull()` / `isLoading()` / `isReady()` / `isError()` | 查询状态机 | `object()` 仅在 Ready 时非空。 |
| `object()` | 取得创建对象 | 仅 Ready 可取；随后由调用方管理使用与所有权。 |
| `errors()` | 读取创建错误 | 仅 Error 时作为失败诊断。 |
| `setInitialProperties(map)` | 设置创建初始顶层属性 | 在开始 incubation 前设置。 |
| `clear()` | 终止/复位 incubator | 中止 Loading；不删除 Ready 状态的对象。 |
| `forceCompletion()` | 强制同步完成 | 可能引入当前帧卡顿。 |
| `setInitialState(object)` | 高级初始状态钩子 | binding 时机不稳定，勿依赖固定求值顺序。 |
| `statusChanged(status)` | 高级状态回调 | Ready 取对象，Error 读 errors。 |

孵化机制真正的收益来自“对象尚未被需要时就开始创建”。若每次都会立刻 `forceCompletion()`，它只是在用更复杂的 API 恢复同步卡顿。
