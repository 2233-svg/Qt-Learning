# Qt QProgressBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QProgressBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QProgressBar`  
> 定位：展示已知或未知工作进度的只读反馈控件

## 1. QProgressBar 解决什么问题

`QProgressBar` 不负责执行任务，它负责让用户知道任务还在运行、已完成多少，以及大致还要等多久。

```text
导出文件： [████████░░░░░░░░░░] 42%
```

它适合文件复制、批量导入、离线计算、下载、数据库迁移、安装或渲染等耗时操作。核心输入是一个闭区间 `[minimum, maximum]` 和当前 `value`，默认范围为 `0..100`。

它不适合：

- 用一个假进度条掩盖完全未知且无法估计的工作；
- 在 GUI 线程执行长循环后才调用 `setValue()`，因为界面不会有机会重绘；
- 把 `value == maximum` 当作任务成功的唯一证明，实际任务仍可能在收尾、写盘或失败处理。

## 2. 最小可用示例：批量处理 200 个对象

```cpp
auto *progress = new QProgressBar(this);
progress->setRange(0, 200);
progress->setValue(0);
progress->setFormat("正在处理：%v / %m（%p%）");

for (int i = 0; i < 200; ++i) {
    processItem(i);
    progress->setValue(i + 1);
}
```

`%v` 是当前值，`%m` 是总步数，`%p` 是完成百分比。任务应放进工作线程或分批交还事件循环；否则即使不断 `setValue()`，主线程被阻塞时用户仍看不到变化。

跨线程时，不要让工作线程直接操作控件。工作对象发出进度信号，在 GUI 线程中通过带 context 的连接更新：

```cpp
connect(worker, &Worker::progressChanged, progress,
        &QProgressBar::setValue);
```

## 3. 确定进度与忙碌状态

### 3.1 已知总量：设置正常范围

```cpp
progress->setRange(0, totalBytes);
progress->setValue(doneBytes);
```

百分比按下面的概念计算：

```text
(value - minimum) / (maximum - minimum)
```

范围不一定从 0 开始，例如进度来自某个分段任务时可用 `100..500`。业务上最易理解的做法仍是将可见进度归一为 `0..100` 或 `0..任务总数`。

### 3.2 未知总量：使用不确定进度

```cpp
progress->setRange(0, 0);
```

当最小值和最大值都为 0 时，Qt 显示忙碌动画，而不是百分比。它表示“任务仍在进行，但总量未知”，例如尚未取得 `Content-Length` 的下载。

一旦得到总量，应切回确定范围并设置当前值：

```cpp
progress->setRange(0, totalBytes);
progress->setValue(receivedBytes);
```

不要把忙碌状态理解为 0%。它没有“已完成比例”，也不应显示虚构的剩余时间。

## 4. 范围改变与 `reset()` 的边界

`setMinimum()`、`setMaximum()` 和 `setRange()` 会维护一个合法范围：

- 设置最大值时若小于 minimum，Qt 会调整 minimum；
- 设置最小值时若大于 maximum，Qt 会调整 maximum；
- `setRange(min, max)` 中若 `max < min`，`min` 成为唯一合法值；
- 若改变范围后当前 value 落在新范围外，控件会 `reset()`。

```cpp
progress->setRange(10, 5); // 退化为只允许值 10 的范围，不是倒退进度
```

`reset()` 的语义是“回到尚未开始显示进度的状态”，而不是简单 `setValue(minimum)`。在 reset 状态，`text()` 可能为空，显示进度也可能小于 minimum。重新开始一个任务时，先设新范围，再显式设 `setValue(0)` 或对应的起点，避免旧任务的视觉状态残留。

```cpp
progress->setRange(0, fileCount);
progress->reset();      // 显示尚未开始
progress->setValue(0);  // 现在明确显示起点
```

`setValue()` 传入范围外数值不会改变当前值。因此业务层应在源头保证已完成数量与总数量一致，而不是期待进度条自动截断。

## 5. 文本、方向与样式并非总能完全控制

### 格式与文本

```cpp
progress->setFormat("%p%（%v / %m）");
```

| 占位符 | 含义 |
| --- | --- |
| `%p` | 已完成百分比。 |
| `%v` | 当前 value。 |
| `%m` | 总步数，通常是 `maximum - minimum` 的数量概念。 |

默认格式为 `%p%`。`text()` 返回根据当前 format 生成的描述文本；`resetFormat()` 恢复默认格式。`textVisible` 控制是否请求显示文字，但某些平台样式可能忽略它，例如某些 macOS 风格不会绘制进度文字。

### 外观方向

`invertedAppearance` 只改变填充增长方向，例如水平条从右向左增长；它不改变进度数值的大小关系。右到左界面、反向时间轴或特定仪表语义可使用它，但普通“完成越多填得越满”的进度条不应随意反向。

垂直进度条可设置 `textDirection`：

| 枚举 | 含义 |
| --- | --- |
| `TopToBottom` | 文字顺时针旋转 90 度。 |
| `BottomToTop` | 文字逆时针旋转 90 度。 |

它对水平进度条没有影响，而且是否真的绘制文字仍由样式决定。需要稳定可访问的进度说明时，在旁边放一个 `QLabel`，不要只依赖进度条内部文字。

## 6. `valueChanged` 不是“任务完成”信号

```cpp
connect(progress, &QProgressBar::valueChanged, this,
        [this, progress](int value) {
            statusLabel->setText(
                QString("已完成 %1 / %2").arg(value).arg(progress->maximum()));
        });
```

`valueChanged(int)` 只表示控件显示值改变。`value == maximum()` 常被用作 UI 收尾条件，但任务是否真正成功应由工作对象的 `finished`、`failed` 或结果信号决定：

```cpp
connect(worker, &Worker::finished, this, [progress] {
    progress->setValue(progress->maximum());
});

connect(worker, &Worker::failed, this, [progress](const QString &error) {
    progress->reset();
    progress->setFormat("失败：" + error);
});
```

这样错误路径不会错误地显示 100%。

## 7. 自定义绘制的边界

继承 `QProgressBar` 时，`initStyleOption(QStyleOptionProgressBar *)` 会把当前控件状态填入样式选项；自定义 `paintEvent()` 前应优先调用它，再使用 `QStyle` 绘制，避免丢失禁用、忙碌、方向和平台主题状态。

仅仅为了改变颜色、圆角或字体，优先使用样式表或 `QProxyStyle`。只有需要叠加阶段标记、双层进度或领域专用图形时，才重写 `paintEvent()`。

## API 速查表
### 8.1 类型与核心状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Direction` | 定义垂直进度条内部文字的阅读方向 | 只影响垂直进度条；是否绘制文字仍由样式决定 |
| 枚举值 | `TopToBottom` | 让垂直文字按从上到下方向阅读 | 常作为默认方向使用 |
| 枚举值 | `BottomToTop` | 让垂直文字按从下到上方向阅读 | 适合特定仪表或平台习惯，水平进度条不受影响 |
| 范围 | `minimum() const` / `setMinimum(int)` | 读取或设置进度下界 | 改变后可能调整 `maximum()`；当前 value 出界时控件会 reset |
| 范围 | `maximum() const` / `setMaximum(int)` | 读取或设置进度上界 | 改变后可能调整 `minimum()`；不要把 maximum 当作任务成功信号 |
| 范围 | `setRange(int minimum, int maximum)` | 一次设置完整进度范围 | `0, 0` 表示未知总量的忙碌状态；`maximum < minimum` 会退化成单值范围 |
| 进度值 | `value() const` / `setValue(int value)` | 读取或设置当前显示进度 | 范围外 value 不生效；`value == maximum()` 不能单独证明任务成功 |
| 状态 | `reset()` | 回到尚未显示进度的 reset 状态 | 新任务开始或失败回退时使用，不等同于 `setValue(minimum())` |

### 8.2 文字与外观 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 文本 | `format() const` / `setFormat(const QString &format)` | 读取或设置进度文字模板 | `%p`、`%v`、`%m` 分别表示百分比、当前值和总步数概念 |
| 文本 | `resetFormat()` | 恢复默认 `%p%` 文本格式 | 临时显示任务描述后可用它回到默认百分比显示 |
| 文本 | `text() const` | 返回按当前 format 生成的描述文本 | reset 状态可能为空；它是虚函数，子类可定制 |
| 文本 | `isTextVisible() const` / `setTextVisible(bool visible)` | 查询或请求在进度条内显示文字 | 部分平台样式会忽略此请求；可访问说明更稳妥的做法是旁边放 `QLabel` |
| 文本 | `alignment() const` / `setAlignment(Qt::Alignment)` | 读取或设置文字对齐方式 | 只有样式实际绘制文字时才可见 |
| 方向 | `orientation() const` / `setOrientation(Qt::Orientation)` | 查询或设置水平/垂直进度条 | 默认水平；垂直进度条才需要考虑 `textDirection` |
| 方向 | `invertedAppearance() const` / `setInvertedAppearance(bool invert)` | 查询或反转填充增长方向 | 只改变视觉方向，不改变 `minimum`、`maximum` 和 `value` 的数值语义 |
| 方向 | `textDirection() const` / `setTextDirection(Direction direction)` | 查询或设置垂直文字旋转方向 | 水平条无影响，且部分样式不绘制内部文字 |

### 8.3 构造、信号与扩展 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QProgressBar(QWidget *parent = nullptr)` | 创建进度条控件 | 默认范围 `0..100`；传 `parent` 后纳入 Qt 对象生命周期 |
| 生命周期 | `~QProgressBar()` | 销毁进度条 | 通常由父对象销毁，业务代码很少直接调用 |
| 信号 | `valueChanged(int value)` | 当前显示进度值改变时发出 | 可同步旁边标签或测试观察，不要用它替代 worker 的完成/失败信号 |
| 尺寸 | `minimumSizeHint() const` / `sizeHint() const` | 返回布局建议尺寸 | 交给布局系统使用；文字、方向和样式会影响结果 |
| 样式 | `initStyleOption(QStyleOptionProgressBar *option) const` | 用当前控件状态初始化进度条样式选项 | 派生类自定义绘制时调用，避免丢失忙碌、禁用、反向等状态 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 执行进度条绘制 | 只有需要阶段标记、双层进度等专用表现时才重写 |
| 事件 | `event(QEvent *event)` | 处理通用事件入口 | 普通使用不调用；派生控件重写时要保留父类行为 |

---

### 一句话总结

`QProgressBar` 负责可信地展示进度：总量未知时用 `setRange(0, 0)`，总量已知时设置真实范围，任务完成与失败仍以工作对象的结果信号为准。
