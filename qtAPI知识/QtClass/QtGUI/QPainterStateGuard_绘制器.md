# QPainterStateGuard：用 RAII 自动平衡 QPainter 状态栈

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.9  
> 头文件：`#include <QPainterStateGuard>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 相关类型：`QPainter`

`QPainterStateGuard` 是一个 RAII（资源获取即初始化）辅助类型，用来自动平衡 `QPainter::save()` 与 `QPainter::restore()`。构造 guard 时，它默认调用一次 `save()`；离开作用域时，析构函数会调用对应次数的 `restore()`，使画笔状态回到进入该作用域前。

它特别适合 `paintEvent()`、复杂绘制帮助函数和含多个提前返回分支的代码。与手写 `save()` / `restore()` 相比，它把“恢复状态”绑定到 C++ 作用域，不会因 `return`、异常路径或后续重构漏掉 `restore()`。

## 它解决的问题

`QPainter` 的 pen、brush、font、transform、clip、opacity、composition mode 等都是可变状态。局部绘制需要临时改变其中若干项，结束后必须恢复，否则状态会泄漏给后续绘制：

```cpp
painter.setPen(Qt::red);

painter.save();
painter.setPen(Qt::blue);
painter.setFont(QFont("Arial", 30));
painter.drawText(rect, Qt::AlignCenter, QStringLiteral("Qt"));
painter.restore();

painter.drawLine(line); // 期望仍使用 red
```

在实际代码中，条件分支、早返回和错误处理很容易使最后一个 `restore()` 被遗漏。`QPainterStateGuard` 把这对调用变为一个作用域对象。

## 实际使用场景

### 1. `paintEvent()` 中的临时样式

```cpp
void ChartWidget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.setPen(Qt::darkGray);

    {
        QPainterStateGuard guard(&painter);
        painter.setPen(QPen(Qt::blue, 2));
        painter.setOpacity(0.55);
        painter.rotate(-12.0);
        drawHighlightedSeries(painter);
    } // 自动 restore()

    painter.drawLine(axisLine); // 使用进入块前的状态
}
```

把 guard 放在最小需要隔离状态的块中，状态恢复范围最直观。

### 2. 含早返回的绘制帮助函数

```cpp
void drawBadge(QPainter &painter, const QRectF &rect, bool enabled)
{
    QPainterStateGuard guard(&painter);
    painter.setRenderHint(QPainter::Antialiasing);

    if (!enabled)
        return; // guard 析构，仍会 restore()

    painter.setBrush(Qt::yellow);
    painter.drawRoundedRect(rect, 6, 6);
}
```

无论函数从哪个分支退出，画笔状态都会回滚到调用前。

### 3. 手动管理 guard 的多层保存

```cpp
QPainterStateGuard guard(&painter, QPainterStateGuard::InitialState::NoSave);

guard.save();
painter.setClipRect(viewport);

guard.save();
painter.scale(scale, scale);
drawScene(painter);

guard.restore(); // 只恢复 scale 那层
// 仍保留 viewport clip
```

析构时 guard 还会恢复它自己尚未恢复的层数。`NoSave` 适合你需要延后第一次保存的情况。

## 核心语义与边界

### 默认构造行为

```cpp
QPainterStateGuard guard(&painter);
```

默认 `InitialState::Save`，构造时立即调用 `painter.save()`，并将内部计数加一。析构时会调用一次 `painter.restore()`。

`InitialState::NoSave` 不会在构造时保存状态；只有之后调用 `guard.save()` 才会累加需要在析构时恢复的层数。

| `InitialState` | 构造时行为 | 析构时行为 |
| --- | --- | --- |
| `InitialState::Save` | 立即调用一次 `QPainter::save()`。 | 恢复构造保存的这一层，以及之后经 guard 新增的层。 |
| `InitialState::NoSave` | 不调用 `save()`。 | 只恢复之后通过该 guard 调用 `save()` 所建立的层。 |

### guard 只跟踪自己的保存层数

guard 内部维护独立计数。它只知道：

- 构造时是否由自身执行过 `save()`；
- 之后是否调用过 `guard.save()`；
- 是否调用过匹配次数的 `guard.restore()`。

不要在 guard 存活期间混入不配对的手工调用：

```cpp
QPainterStateGuard guard(&painter);
painter.restore(); // 错误：guard 的计数不知道这次 restore
```

这会让 `QPainter` 自身状态栈和 guard 计数失同步，之后析构再恢复时可能触发断言或恢复到错误层级。要么完全使用 guard 的 `save()` / `restore()`，要么在同一小段代码中完全手工管理 painter 状态栈。

### `restore()` 不能超过 guard 保存次数

`guard.restore()` 仅在内部计数大于 0 时可调用。若计数已经为 0，Qt 的 debug 构建会断言：

```cpp
QPainterStateGuard guard(&painter);
guard.restore();
guard.restore(); // debug 下断言
```

需要提前恢复一层时可以调用一次 `restore()`；析构函数只会恢复剩余层数，不会重复恢复已手动恢复的那一层。

### QPainter 必须有效且活得更久

构造函数接收裸指针并在 debug 构建检查非空，但不拥有 painter。正确的局部变量顺序是：

```cpp
QPainter painter(device);
QPainterStateGuard guard(&painter);
```

guard 析构时会访问 painter，因此 painter 必须在 guard 析构后才销毁。不要传入空指针、未激活的 painter，或在 guard 存活期间结束 / 销毁其 painter。

### 作用域对象必须有名字

构造函数带有 nodiscard 属性。下面写法会创建并立刻销毁临时 guard，几乎没有作用：

```cpp
QPainterStateGuard(&painter); // 错误的使用方式
```

应使用具名局部变量：

```cpp
QPainterStateGuard stateGuard(&painter);
```

### 移动语义

guard 不可复制，但可以移动。移动构造、移动赋值和 `swap()` 会转移 painter 指针及尚未恢复的层数。移动后的源 guard 不再负责恢复原有层数。

这主要服务于需要把 guard 放入移动型控制流的底层代码；普通绘制函数中应把 guard 固定为局部变量，避免不必要地转移作用域恢复责任。

### 可重入与线程

Qt 文档将本类所有函数标为可重入。它仍然操作传入的 `QPainter`，所以线程规则由 painter 和其目标 `QPaintDevice` 决定：同一个活动 painter 不可在多个线程中并发使用。

## 关键 API 语义

### 典型使用模式

```cpp
void drawOverlay(QPainter &painter)
{
    QPainterStateGuard guard(&painter);
    painter.setCompositionMode(QPainter::CompositionMode_SourceOver);
    painter.setOpacity(0.4);
    painter.translate(8, 8);
    drawOverlayContent(painter);
} // 恢复 pen、brush、font、clip、transform、opacity 等 painter 状态
```

guard 恢复的是 `QPainter::save()` 保存的完整 painter 状态，不只是最后一次设置的一个属性。

### `NoSave` 加手动 `save()`

```cpp
QPainterStateGuard guard(&painter, QPainterStateGuard::InitialState::NoSave);

if (needsOverlay) {
    guard.save();
    painter.setOpacity(0.5);
    drawOverlay(painter);
}
```

这避免在条件不成立时压入不需要的 painter 状态层。条件成立时，析构会补回该层。

## 常见错误

### 让 guard 比 QPainter 活得更久

```cpp
QPainterStateGuard *guard = nullptr;
{
    QPainter painter(device);
    guard = new QPainterStateGuard(&painter);
}
delete guard; // painter 已销毁，错误
```

不需要动态分配 guard。用局部变量能自然保证析构顺序。

### guard 存活期间手工 `restore()`

这会破坏计数。若必须提前恢复，调用 `guard.restore()`，而不是 `painter.restore()`。

### 把 guard 当作 QPainter 的所有权对象

guard 只管理状态栈，不会调用 `QPainter::begin()`、`end()`，不负责设备和 painter 生命周期，也不保存绘制结果。

### 在 Qt 6.9 之前的项目中使用

`QPainterStateGuard` 从 Qt 6.9 开始提供。需要兼容 Qt 6.8 或更早版本时，使用明确的 `painter.save()` / `painter.restore()`，或在项目内部实现等价的局部 RAII 封装。

## API 速查表

### 类型

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `enum class InitialState { Save, NoSave }` | 控制构造函数是否立即保存 painter 状态。 | 默认 `Save`；需要延后或条件化保存时使用 `NoSave`。 |

### 构造、移动与析构

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `QPainterStateGuard(QPainter *painter, InitialState state = InitialState::Save)` | 绑定非拥有的 painter；默认立即 `save()`。 | painter 必须有效、活动并比 guard 活得久；对象要有名字。 |
| `QPainterStateGuard(QPainterStateGuard &&other)` | 移动构造，接管 painter 指针与未恢复层数。 | 源对象不再负责 restore。 |
| `operator=(QPainterStateGuard &&other)` | 移动赋值，转移 guard 的恢复责任。 | 高级用法；普通绘制中保持局部变量更清晰。 |
| `~QPainterStateGuard()` | 对内部计数的每一层调用 `QPainter::restore()`。 | 不抛异常；会访问绑定 painter。 |
| `swap(QPainterStateGuard &other)` | 交换两个 guard 的 painter 和剩余层数。 | `noexcept`；用于移动实现或容器算法。 |

### 状态栈操作

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `save()` | 调用 `QPainter::save()`，并让内部恢复计数加一。 | 与 `guard.restore()` 成对；析构会补回未恢复的层。 |
| `restore()` | 若内部计数大于零，调用 `QPainter::restore()` 并减一。 | 计数为零时 debug 构建断言；不要绕过 guard 改 painter 栈。 |

## 与手工 save/restore 的选择

| 情况 | 推荐方式 |
| --- | --- |
| 一个局部绘制块临时改状态 | `QPainterStateGuard guard(&painter)` |
| 多个早返回或复杂分支 | `QPainterStateGuard` |
| 需要按条件才压入状态层 | `InitialState::NoSave` + `guard.save()` |
| 需兼容 Qt 6.8 或更早 | 手工 `save()` / `restore()` 或项目内 RAII 封装 |
| 需要长期、跨作用域管理画笔 | 重新设计绘制边界；guard 应保持短生命周期 |

一句话记忆：`QPainterStateGuard` 让一次 `save()` 的恢复责任跟着 C++ 作用域走，前提是 painter 活得更久，并且 save/restore 不与手工调用混用。
