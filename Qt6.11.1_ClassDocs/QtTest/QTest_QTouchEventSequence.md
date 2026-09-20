# QTest::QTouchEventSequence
> Qt 6.11.1 · Qt Test · 来自 `QTest::QTouchEventSequence`

## 1. 先建立直觉

`QTouchEventSequence` 用来在测试里构造一帧或一组触摸点状态：某根手指按下、移动、保持不动、释放，然后 `commit()` 发出去。它面向 `QWindow`/窗口级触摸输入，是测试手势、触控控件和多点触摸逻辑的基础工具。

## 2. 类说明

保留类说明：这些 API 来自 `QTest::QTouchEventSequence`，属于 Qt Test 模块，用于模拟触摸事件序列。

它使用链式 API。每个 `touchId` 表示一根手指；同一帧中没动但仍按住的手指，需要用 `stationary()` 明确保留。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `press(touchId, pt, window)` | 添加某触点按下。 |
| `move(touchId, pt, window)` | 添加某触点移动。 |
| `stationary(touchId)` | 标记某触点保持不动但仍参与当前事件。 |
| `release(touchId, pt, window)` | 添加某触点释放。 |
| `commit(processEvents = true)` | 提交当前序列；可选择是否处理事件循环。 |
| `~QTouchEventSequence()` | 销毁序列对象。 |

## 4. 典型流程

```cpp
QTest::touchEvent(window, device)
    .press(0, QPoint(20, 20), window)
    .commit();

QTest::touchEvent(window, device)
    .move(0, QPoint(80, 20), window)
    .commit();

QTest::touchEvent(window, device)
    .release(0, QPoint(80, 20), window)
    .commit();
```

多点缩放时，两根手指要在每帧都表达状态：

```cpp
seq.move(0, p0).move(1, p1).commit();
seq.stationary(0).move(1, p2).commit();
```

## 5. 使用场景

| 场景 | 检查重点 |
| --- | --- |
| 自定义触控控件 | press/move/release 后状态是否正确。 |
| 多点手势 | 每个 touchId 的生命周期和坐标变化。 |
| 触摸取消/边界移动 | 移出窗口、释放顺序、stationary 点处理。 |
| Window 级输入 | 适合 QWindow 或 Quick 底层窗口相关测试。 |

## 6. 常见坑与经验

触点 ID 要稳定：同一根手指从 press 到 release 都用同一个 id。复用已释放 id 可以，但不要在同一活动手势里混乱切换。

多点触摸中，没移动的手指也常常要 `stationary()`。否则被测对象可能以为那根手指消失或没有参与当前帧，手势识别结果会偏。

`commit(true)` 会处理事件，方便多数同步测试；如果你要精细控制事件循环，才考虑传 `false` 并自己推进。

## 7. 知识点覆盖

- 触点 ID、触摸生命周期和多点状态帧。
- press/move/stationary/release 的组合。
- `QWindow` 目标和事件循环提交。
- 手势测试的稳定性和坐标设计。
