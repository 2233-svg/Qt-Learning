# QMediaTimeRange：表示可用的多个媒体时间区间

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaTimeRange>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：显式共享值类型

## 它解决什么问题

`QMediaTimeRange` 表示一组零个或多个互不相交的时间区间。它解决的是“某些时间点或时间段目前可用吗”这类问题，而不是保存媒体内容本身。

典型例子是网络媒体的缓冲情况：一个视频可能已经缓冲了 `0 ms - 5000 ms` 和 `12000 ms - 18000 ms`，中间仍然缺一段。用单个 `qint64` 无法表达这种状态，`QMediaTimeRange` 可以把这些区间作为一个集合保存。

区间端点的单位由调用方约定。Qt Multimedia 中通常使用毫秒，但这个类本身只处理带符号 64 位整数，不强制单位。

## 实际使用场景

- 读取 `QMediaPlayer::bufferedTimeRange()`，绘制缓冲条上的多个已缓冲片段；
- 判断某个时间点能否立即播放；
- 对下载进度、缓存片段或媒体章节范围做并集和差集；
- 从可用范围中移除已经失效的片段；
- 在测试代码中构造一组离散的可播放时间范围。

## 区间模型

`QMediaTimeRange` 使用包含两端的闭区间：

```text
[start, end]
```

例如 `[1000, 3000]` 包含 `1000`、`2000` 和 `3000`。区间集合会保持为不相交的规范形式：

```cpp
QMediaTimeRange range;
range.addInterval(0, 1000);
range.addInterval(1000, 2000);
range.addInterval(4000, 5000);

// 前两个区间会合并；结果相当于：
// [0, 2000] 和 [4000, 5000]
```

添加重叠或相邻区间会合并。添加反向区间，例如 `(3000, 1000)`，是无效操作，会被忽略；需要接受任意端点顺序时，先使用 `QMediaTimeRange::Interval::normalized()`。

删除不是简单地删除一个“元素”。它会根据目标区间裁剪、拆分或删除已有区间：

```cpp
QMediaTimeRange range(0, 10000);
range.removeInterval(4000, 6000);

// 结果为 [0, 4000] 和 [6000, 10000]
```

## 查询边界

- 空范围的 `earliestTime()` 和 `latestTime()` 都返回 `0`，不能把 `0` 当成“有效的第一个时间”；
- `isEmpty()` 才是判断有没有区间的可靠方法；
- `isContinuous()` 在区间数量为零或一时返回 `true`，所以空范围也被视为连续；
- `contains(time)` 对闭区间端点返回 `true`；
- `intervals()` 返回当前区间列表的值副本，修改返回的列表不会修改原对象；
- 添加和删除区间的操作复杂度为线性时间，适合中等数量的片段，不适合把它当高频大规模区间树。

## 值语义、共享和修改

这个类使用显式共享数据。复制对象成本较低，但复制后修改其中一个对象时会分离数据，因此修改通常不会影响另一个对象：

```cpp
QMediaTimeRange original(0, 5000);
QMediaTimeRange copy = original;
copy.addInterval(10000, 12000);

// original 仍然只有 [0, 5000]
```

`detach()` 可以显式确保当前对象拥有自己的数据副本。一般业务代码不需要主动调用它，只有在需要控制分离时机或编写底层性能敏感代码时才有意义。

值语义不等于线程安全。不同线程使用各自的副本通常没有问题；多个线程同时读写同一个对象时，仍需要应用层同步。

## 加法、减法和赋值的语义

`operator+` 表示并集，`operator-` 表示从左侧范围中扣除右侧范围：

```cpp
QMediaTimeRange a(0, 10000);
QMediaTimeRange b(4000, 6000);

QMediaTimeRange unionRange = a + b;      // [0, 10000]
QMediaTimeRange remaining = a - b;       // [0, 4000]、[6000, 10000]
```

`operator+=` 和 `operator-=` 会修改左侧对象。它们和 `addTimeRange()`、`removeTimeRange()` 的行为对应。

注意：

```cpp
range = QMediaTimeRange::Interval(1000, 2000);
```

这里是把 `range` 替换成单个区间，不是向已有范围追加区间。追加应使用 `addInterval()` 或 `operator+=`。

## 与 QMediaPlayer 缓冲的关系

`QMediaPlayer::bufferedTimeRange()` 返回的是当前媒体中“已经缓冲、可以立即播放”的时间片段集合。它不是整个文件的下载进度，也不是播放器未来一定会保持不变的承诺。

网络媒体的缓冲范围可能随着播放、网络速度和后端策略变化。界面应在 `bufferedTimeRangeChanged()` 后重新读取整个对象，不要只保存一个起点和终点，也不要长期缓存旧范围。

## 线程和生命周期

`QMediaTimeRange` 本身不是 `QObject`，没有事件循环和异步行为。它可以作为信号参数、容器元素或配置值传递。

如果范围来自 `QMediaPlayer`，读取播放器属性仍应在播放器所属线程完成。复制出 `QMediaTimeRange` 后，可以把这个值交给其它线程处理，但不要因此跨线程操作播放器。

## 常见误区

- 把空范围的 `earliestTime() == 0` 当作范围包含零时刻；
- 把 `isContinuous()` 的空范围结果误解为“存在一段连续媒体”；
- 认为删除区间只会移除完整匹配的区间；
- 用 `operator=` 添加区间，结果覆盖了原范围；
- 把重叠或相邻区间当作两个独立区间保存；
- 忽略 `qint64` 的单位约定，混用毫秒、微秒和纳秒；
- 把值类型的隐式优化理解成多线程同步。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMediaTimeRange()` | 创建空时间范围。 | 空范围的最早、最晚时间都为 `0`。 |
| 构造 | `explicit QMediaTimeRange(qint64 start, qint64 end)` | 用一个区间创建范围。 | 反向区间无效，不能依赖它被自动交换。 |
| 构造 | `QMediaTimeRange(const Interval &interval)` | 用一个 `Interval` 创建范围。 | 非 normal 区间会被忽略。 |
| 构造 | `QMediaTimeRange(const QMediaTimeRange &range)` | 复制时间范围。 | 值语义；修改副本时会按需分离。 |
| 构造 | `QMediaTimeRange(QMediaTimeRange &&other)` | 移动时间范围。 | 移动后的源对象只保留有效但未指定的状态。 |
| 析构 | `~QMediaTimeRange()` | 销毁时间范围。 | 不涉及媒体设备或播放器资源。 |
| 赋值 | `operator=(const QMediaTimeRange &other)` | 复制另一个范围。 | 会替换当前内容。 |
| 赋值 | `operator=(QMediaTimeRange &&other)` | 移动另一个范围。 | 适合临时值和容器操作。 |
| 赋值 | `operator=(const Interval &interval)` | 替换为单个区间。 | 不是追加操作。 |
| 共享 | `void swap(QMediaTimeRange &other)` | 交换两个范围。 | `noexcept`，只交换范围数据。 |
| 共享 | `void detach()` | 强制当前对象与共享数据分离。 | 通常不需要手动调用。 |
| 查询 | `qint64 earliestTime() const` | 返回范围内最早时间。 | 空范围返回 `0`。 |
| 查询 | `qint64 latestTime() const` | 返回范围内最晚时间。 | 空范围返回 `0`。 |
| 查询 | `QList<Interval> intervals() const` | 返回所有不相交区间。 | 返回值是列表副本；区间已按集合规则合并。 |
| 查询 | `bool isEmpty() const` | 判断是否没有区间。 | 比检查 `earliestTime()` 更可靠。 |
| 查询 | `bool isContinuous() const` | 判断是否有一个或更少的不相交区间。 | 空范围也返回 `true`。 |
| 查询 | `bool contains(qint64 time) const` | 判断时间点是否落在任一区间内。 | 两端都包含。 |
| 添加 | `void addInterval(qint64 start, qint64 end)` | 添加一个区间。 | 反向区间忽略；重叠或相邻区间合并。 |
| 添加 | `void addInterval(const Interval &interval)` | 添加一个 `Interval`。 | 非 normal 区间忽略；线性时间。 |
| 添加 | `void addTimeRange(const QMediaTimeRange &range)` | 添加另一个范围的全部区间。 | 等价于逐个调用 `addInterval()`。 |
| 删除 | `void removeInterval(qint64 start, qint64 end)` | 删除指定区间覆盖的时间。 | 可能裁剪、拆分或删除已有区间。 |
| 删除 | `void removeInterval(const Interval &interval)` | 删除一个 `Interval`。 | 非 normal 区间忽略；线性时间。 |
| 删除 | `void removeTimeRange(const QMediaTimeRange &range)` | 删除另一个范围的全部区间。 | 等价于逐个调用 `removeInterval()`。 |
| 运算 | `QMediaTimeRange &operator+=(const QMediaTimeRange &other)` | 把另一个范围并入当前对象。 | 修改当前对象并合并区间。 |
| 运算 | `QMediaTimeRange &operator+=(const Interval &interval)` | 把一个区间并入当前对象。 | 非 normal 区间不产生效果。 |
| 运算 | `QMediaTimeRange &operator-=(const QMediaTimeRange &other)` | 从当前对象扣除另一个范围。 | 可能产生多个剩余区间。 |
| 运算 | `QMediaTimeRange &operator-=(const Interval &interval)` | 从当前对象扣除一个区间。 | 闭区间边界参与删除。 |
| 修改 | `void clear()` | 清空所有区间。 | 清空后 `isEmpty()` 为 `true`。 |
| 比较 | `operator==(lhs, rhs)` | 比较两个范围是否包含相同区间集合。 | 比较的是规范化后的范围语义。 |
| 比较 | `operator!=(lhs, rhs)` | 判断两个范围是否不同。 | 与 `operator==` 相反。 |
| 运算 | `operator+(r1, r2)` | 返回两个范围的并集。 | 不修改输入对象。 |
| 运算 | `operator-(r1, r2)` | 返回从 `r1` 扣除 `r2` 的结果。 | 不修改输入对象。 |
| 调试 | `operator<<(QDebug, const Interval &)` | 将区间写入 Qt 调试流。 | 仅在未禁用 debug stream 时提供。 |
| 调试 | `operator<<(QDebug, const QMediaTimeRange &)` | 将时间范围写入 Qt 调试流。 | 适合日志，不是持久化格式。 |

## 一句话总结

`QMediaTimeRange` 是媒体时间轴上的区间集合：添加做并集合并，删除做区间差集，空范围和连续性的边界需要单独判断；它非常适合表达缓冲片段，而不是表达媒体数据本身。
