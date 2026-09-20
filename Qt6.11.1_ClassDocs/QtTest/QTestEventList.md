# QTestEventList
> Qt 6.11.1 · Qt Test · 来自 `QTestEventList`

## 1. 先建立直觉

`QTestEventList` 是一串可复放的键盘和鼠标测试事件。你把“按下、释放、点击、输入文字、移动鼠标、等待”按顺序加进去，然后对某个 `QWidget` 调用 `simulate()`，Qt Test 会按列表重放这些输入。

它适合把一段用户操作流程写成可读的脚本，尤其是同一组输入要在多个控件或多组数据上重复执行时。

## 2. 类说明

保留类说明：这些 API 来自 `QTestEventList`，属于 Qt Test 模块，用于组织并模拟 QWidget 输入事件。

它继承自 `QList`，但业务上更应把它当“事件脚本”，而不是普通数据容器。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QTestEventList()` / copy ctor / dtor | 创建、复制、销毁事件列表。 |
| `addDelay(msecs)` | 在事件序列中插入等待。 |
| `addKeyClick(Qt::Key/char, modifiers, msecs)` | 添加一次按下+释放。 |
| `addKeyClicks(QString, modifiers, msecs)` | 添加一串文本输入。 |
| `addKeyPress(Qt::Key/char, modifiers, msecs)` | 只添加按下。 |
| `addKeyRelease(Qt::Key/char, modifiers, msecs)` | 只添加释放。 |
| `addMouseClick(button, modifiers, pos, delay)` | 添加鼠标单击。 |
| `addMouseDClick(button, modifiers, pos, delay)` | 添加鼠标双击。 |
| `addMousePress(button, modifiers, pos, delay)` | 添加鼠标按下。 |
| `addMouseRelease(button, modifiers, pos, delay)` | 添加鼠标释放。 |
| `addMouseMove(pos, delay)` | 添加鼠标移动。 |
| `simulate(QWidget *w)` | 在指定 widget 上按顺序模拟全部事件。 |
| `clear()` | 清空列表，重新录制脚本。 |

## 4. 典型流程

```cpp
QTestEventList events;
events.addMouseClick(Qt::LeftButton, {}, QPoint(10, 10));
events.addKeyClicks("hello");
events.addKeyClick(Qt::Key_Return);

events.simulate(lineEdit);
QCOMPARE(lineEdit->text(), "hello");
```

拖拽类流程可以显式 press/move/release：

```cpp
events.addMousePress(Qt::LeftButton, {}, start);
events.addMouseMove(end, 20);
events.addMouseRelease(Qt::LeftButton, {}, end);
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 表单输入流程 | 事件脚本比散落的 `QTest::keyClick` 更清楚。 |
| 多组数据复用同一输入 | 同一个列表对不同 widget 或状态重放。 |
| 鼠标拖拽/组合键 | 可以显式排列 press、move、release 和 delay。 |
| 回归测试用户操作顺序 | 流程变动时一处修改。 |

## 6. 常见坑与经验

默认鼠标位置是 widget 中心，不一定是你想点的控件内部有效区域。复杂 widget、delegate、树表视图里最好传明确坐标。

`addDelay()` 会让测试变慢，也可能掩盖异步问题。等待异步状态时优先用 `QSignalSpy::wait()` 或 `QTRY_VERIFY`，delay 只用于模拟真实输入节奏。

`simulate()` 针对 QWidget。Qt Quick 测试要使用 Quick 相关测试工具，不要强行拿 QWidget 输入事件覆盖 QML 场景。

## 7. 知识点覆盖

- 键盘、鼠标事件序列化与重放。
- QWidget 输入测试坐标、修饰键和延迟。
- 单击/双击/拖拽/文本输入流程。
- 事件脚本复用和异步等待策略。
