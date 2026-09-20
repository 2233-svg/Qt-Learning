# QMediaTimeRange::Interval：不可变的整数时间区间值对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaTimeRange>`  
> 所属模块：`Qt6::Multimedia`  
> 所属类：`QMediaTimeRange::Interval`  
> 类型性质：嵌套值类型

## 它解决什么问题

`QMediaTimeRange::Interval` 描述一个带整数精度的时间区间。它只保存两个 `qint64` 端点，不保存媒体、不连接播放器，也不负责区间集合的合并。

它适合把一个明确的时间段作为值传递：

```cpp
QMediaTimeRange::Interval intro(0, 15000);
QMediaTimeRange::Interval adBreak(60000, 75000);
```

`QMediaTimeRange` 是多个区间的集合，而 `Interval` 是集合中的单个元素。需要并集、差集、重叠合并时，应使用 `QMediaTimeRange`。

## 区间是闭区间

正常区间使用包含两端的形式：

```text
[start, end]
```

`Interval(1000, 3000)` 包含 `1000` 和 `3000`。这个类不规定单位；Qt Multimedia 的媒体时间通常以毫秒表达，但调用方仍应在接口边界明确约定单位。

## normal 与反向区间

当 `start <= end` 时，区间是 normal：

```cpp
QMediaTimeRange::Interval normal(100, 200);
Q_ASSERT(normal.isNormal());
```

当 `start > end` 时，它是非 normal 或反向区间：

```cpp
QMediaTimeRange::Interval reversed(200, 100);
Q_ASSERT(!reversed.isNormal());
```

反向区间不是构造错误，也不会自动交换端点。它可以作为一个临时值存在，但传给 `QMediaTimeRange::addInterval()` 或 `removeInterval()` 时会被视为无效并忽略。

需要规范化时：

```cpp
auto normalized = reversed.normalized(); // [100, 200]
```

`normalized()` 返回新对象，不修改原来的反向区间。

## contains() 的边界

`contains(time)` 使用闭区间判断。Qt 6.11.1 头文件中的实际行为是：

- normal 区间判断 `start <= time && time <= end`；
- 反向区间按反向端点包围的范围判断，即 `end <= time && time <= start`。

因此，`Interval(200, 100).contains(150)` 仍然返回 `true`。这和 `isNormal()` 是两个独立概念：反向区间可以包含一个时间点，但仍不适合作为 `QMediaTimeRange` 的有效成员。

## 不可变和值语义

这个结构没有设置端点的成员函数。构造后只能通过 `start()`、`end()` 读取，不能原地修改端点：

```cpp
const auto interval = QMediaTimeRange::Interval(1000, 5000);
qint64 begin = interval.start();
qint64 finish = interval.end();
```

如果需要新端点，应构造新的 `Interval` 或使用 `normalized()`、`translated()` 返回的新值。

它是轻量值类型，可以直接复制、作为 `QList` 元素或信号参数传递。复制不会连接任何媒体资源。

## translated() 与溢出

`translated(offset)` 给两个端点同时加上偏移：

```cpp
QMediaTimeRange::Interval source(1000, 3000);
auto shifted = source.translated(5000); // [6000, 8000]
```

正偏移向未来移动，负偏移向过去移动。计算使用 `qint64`，如果端点加偏移超出 `qint64` 表示范围，C++ 有符号整数溢出风险；不要把这个函数当作自动饱和运算。

## 比较运算的语义

`operator==` 和 `operator!=` 比较保存的原始端点，而不是比较它们覆盖的集合：

```cpp
QMediaTimeRange::Interval a(1, 3);
QMediaTimeRange::Interval b(3, 1);

Q_ASSERT(a != b);
Q_ASSERT(a.contains(2) == b.contains(2));
```

所以 `[1, 3]` 与 `[3, 1]` 的覆盖范围虽然相同，但对象本身不相等。需要按正常顺序比较或存入 `QMediaTimeRange` 前，应先调用 `normalized()`。

## 实际使用场景

- 表示视频片段的起止时间；
- 表示播放器缓冲区中的一个连续片段；
- 对剪辑入点、出点进行值传递；
- 使用 `translated()` 把章节时间映射到另一个时间轴；
- 将区间存入 `QVariant`、`QList` 或元对象系统。

## 生命周期和线程

`Interval` 不是 `QObject`，没有父对象、信号或异步操作。它只包含两个整数，生命周期和线程边界都很简单。

如果区间来自播放器或采集对象，生成 `Interval` 的动作应在相应对象所属线程完成；生成后的值可以复制给其它线程使用。

## 常见误区

- 认为 `start > end` 的构造会自动交换端点；
- 认为 `contains()` 对反向区间一定返回 `false`；
- 把 `normalized()` 当成原地修改；
- 用 `operator==` 判断两个区间的覆盖集合是否等价；
- 忽略区间是闭区间，错误地排除 `start` 或 `end`；
- 把时间单位默认为微秒或毫秒，而没有在业务接口中明确约定；
- 让 `translated()` 处理接近 `qint64` 边界的值，却没有考虑溢出。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `constexpr Interval() noexcept` | 创建默认区间 `[0, 0]`。 | 默认区间是 normal，且包含时间 `0`。 |
| 构造 | `explicit constexpr Interval(qint64 start, qint64 end) noexcept` | 用两个端点创建区间。 | 不自动规范化；允许构造反向区间。 |
| 查询 | `constexpr qint64 start() const noexcept` | 返回原始起点。 | 不保证小于或等于 `end()`。 |
| 查询 | `constexpr qint64 end() const noexcept` | 返回原始终点。 | 不保证大于或等于 `start()`。 |
| 查询 | `constexpr bool contains(qint64 time) const noexcept` | 判断时间点是否在端点包围的闭区间内。 | normal 与反向区间都按两端包围范围判断。 |
| 查询 | `constexpr bool isNormal() const noexcept` | 判断 `start <= end`。 | 反向区间返回 `false`。 |
| 转换 | `constexpr Interval normalized() const` | 返回端点按升序排列的新区间。 | 不修改原对象。 |
| 转换 | `constexpr Interval translated(qint64 offset) const` | 将两个端点同时平移。 | 可能发生 `qint64` 有符号溢出。 |
| 比较 | `operator==(Interval lhs, Interval rhs)` | 比较两个对象的原始端点是否都相同。 | `[1,3]` 与 `[3,1]` 不相等。 |
| 比较 | `operator!=(Interval lhs, Interval rhs)` | 判断原始端点是否不同。 | 与 `operator==` 相反。 |

## 一句话总结

`QMediaTimeRange::Interval` 是一个只保存两个 `qint64` 端点的不可变值对象：区间包含两端，normal 由 `start <= end` 决定，规范化和平移都会返回新对象。
