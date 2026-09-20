# QAnimationGroup
> Qt 6.11.1 · Qt Core · 来自 `QAnimationGroup`

## 作用定位
`QAnimationGroup` 是持有多个动画的抽象容器；`QSequentialAnimationGroup` 与 `QParallelAnimationGroup` 分别定义串行和并行调度。

## API 速查
| API | 是做什么的 |
|---|---|
| `addAnimation()` | 加入子动画，group 获得所有权。|
| `insertAnimation()` | 按顺序插入子动画。|
| `removeAnimation()` | 移出但不删除。|
| `takeAnimation()` | 移出并转移所有权。|
| `animationAt()` / `animationCount()` | 查询子动画。|

## 使用场景
让多个属性同时淡入，或依次执行展开、停顿、收起。

## 常见坑与经验
- 加入 group 后不应独立启动子动画；由 group 驱动。
- 重排运行中的子动画会造成难以预测的时间线，先停止再编辑结构。

## 知识点覆盖
组合动画、所有权、串行/并行、时间线编排、状态控制。
