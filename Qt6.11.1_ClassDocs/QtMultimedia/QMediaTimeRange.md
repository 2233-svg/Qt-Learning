# QMediaTimeRange
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaTimeRange`

## 作用定位

`QMediaTimeRange` 表示一个或多个媒体时间区间。它常用于描述可播放、已缓冲、可跳转或片段选择范围。它不是单个时间点，而是可合并、可查询的区间集合。

## 类说明

- 头文件：`#include <QMediaTimeRange>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 创建空范围、单区间范围或从 interval 列表创建。 |
| `addInterval()` / `removeInterval()` | 增加或移除时间区间。 |
| `addTimeRange()` / `removeTimeRange()` | 合并或扣除另一个范围。 |
| `contains(time)` | 判断某时间点是否在范围内。 |
| `isEmpty()` / `isContinuous()` | 是否为空、是否为连续单段。 |
| `earliestTime()` / `latestTime()` | 最早和最晚时间。 |
| `intervals()` | 返回区间列表。 |

## 使用场景
- 显示媒体缓冲区间。
- 限制用户只能在某些片段内 seek。
- 表示剪辑、标注、章节时间范围。

## 常见坑与经验
- 区间单位通常是毫秒，要和播放器 position/duration 保持一致。
- 多个相邻或重叠区间可能被合并，不能假设添加后数量不变。
- `isContinuous()` 为 false 时，进度条显示要能处理断续区间。

## 知识点覆盖

- 媒体时间线区间
- 缓冲/可 seek 范围
- 区间合并与扣除
- 多段时间集合
