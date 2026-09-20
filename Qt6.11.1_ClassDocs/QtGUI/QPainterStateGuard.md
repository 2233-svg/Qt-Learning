# QPainterStateGuard

> Qt 6.11.1 · Qt GUI · 来自 `QPainterStateGuard`

## 1. 先建立直觉

`QPainterStateGuard` 是 `QPainter::save()` / `restore()` 的 RAII 包装。构造时保存 painter 状态，析构时自动恢复，适合在绘制函数里有多个提前返回、复杂分支或异常边界的地方使用。

手写 `save()` / `restore()` 没错，但一旦中间出现 `return`、`continue`、错误分支或多层 helper 函数，就很容易把 painter 留在错误状态。这个类的价值就是把“状态一定会还原”交给对象生命周期。

## 2. 类说明

- 头文件：`#include <QPainterStateGuard>`
- CMake：`Qt6::Gui`
- 类型性质：移动类型，不用于复制
- 作用对象：一个已经存在的 `QPainter`
- 管理内容：`QPainter` 的状态栈，不拥有 painter 本身

`QPainterStateGuard` 不负责开始或结束绘制，也不检查你的 painter 是否绑定了合法设备。它只管理状态保存/恢复计数：构造、`save()` 会增加计数，`restore()` 或析构会按计数恢复。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPainterStateGuard(QPainter *painter, InitialState state = Save)` | 绑定 painter；默认立即调用一次 `save()`。 |
| `~QPainterStateGuard()` | 析构时把内部保存过的状态全部恢复。 |
| `save()` | 再调用一次 `QPainter::save()`，内部计数加一。 |
| `restore()` | 恢复一层保存的状态，内部计数减一；调试构建下计数为零会断言。 |
| `swap()` | 与另一个 guard 交换绑定状态和计数。 |
| 移动构造 / 移动赋值 | 转移恢复责任，适合从 helper 返回 guard 或放入局部控制流。 |

## 4. 关键用法

### 包住局部绘制状态

```cpp
void drawBadge(QPainter *p, const QRectF &rect)
{
    QPainterStateGuard guard(p);

    p->setPen(Qt::NoPen);
    p->setBrush(QColor("#2f80ed"));
    p->drawRoundedRect(rect, 6, 6);
}
```

函数结束时，不管中间是否提前返回，pen、brush、transform、clip、opacity 等 painter 状态都会恢复到进入函数前。

### 多层保存也能统一恢复

```cpp
QPainterStateGuard guard(&p);
p.translate(origin);

guard.save();
p.setClipPath(mask);
drawMaskedContent(&p);
guard.restore(); // 只恢复 clip 那一层

drawUnmaskedContent(&p);
```

`QPainterStateGuard` 不是只能保存一次；它可以显式 `save()` 多层，并在析构时把未恢复的层全部补齐。

### 不立即保存的场景

```cpp
QPainterStateGuard guard(&p, QPainterStateGuard::InitialState::NoSave);

if (needIsolation) {
    guard.save();
    p.setOpacity(0.5);
}
```

当是否需要隔离状态取决于运行条件时，可以延迟调用 `save()`。但要注意：没有 save 就没有 restore，调试构建会帮你抓多余恢复。

## 5. 使用场景

- 自定义控件中拆分多个绘制 helper，每个 helper 独立改 painter 状态。
- 绘制代码存在提前返回，例如数据为空、资源缺失、区域不可见。
- 临时设置 transform、clip、opacity、composition mode，结束后必须恢复。
- 在复杂路径绘制中局部改变 pen/brush/font，避免污染后续层。
- 需要把 painter 状态管理写成“作用域语义”的团队代码规范。

## 6. 常见坑与经验

- **它不拥有 `QPainter`。** painter 必须比 guard 活得更久。
- **它不负责 `begin()` / `end()`。** 如果 painter 还没激活，guard 也不能让它变成可绘制。
- **不要和手写 restore 混乱交叉。** guard 内部有自己的计数；如果同时在外面随意调 `painter.restore()`，状态栈会变得难以推理。
- **移动后原对象不再负责恢复。** 这符合移动语义，但调试时要确认恢复责任在哪个对象上。
- **计数为零时调用 `restore()` 是错误。** 调试构建会断言，发布构建也不应依赖未定义的状态栈行为。
- **它恢复的是 painter 状态，不是业务状态。** 你修改的数据模型、缓存、成员变量不会自动回滚。

## 7. 知识点覆盖

- `QPainter` 状态栈与 RAII 的结合
- 作用域式绘制状态隔离
- 提前返回和异常边界下的状态恢复
- 多层 `save()` / `restore()` 计数
- painter 生命周期与状态生命周期的区别
- 与手写 `QPainter::save()` / `restore()` 的取舍
