# QParallelAnimationGroup
> Qt 6.11.1 · Qt Core · 来自 `QParallelAnimationGroup`

## 作用定位
`QParallelAnimationGroup` 同时驱动多个子动画，组的总时长通常由其中最长的子动画决定。

## API 速查
| API | 是做什么的 |
|---|---|
| `addAnimation()` | 加入一个并行执行的子动画。|
| `insertAnimation()` | 在指定位置加入子动画。|
| `removeAnimation()` | 移出子动画但不删除。|
| `takeAnimation()` | 移出并转移子动画所有权。|
| `duration()` | 返回并行组的有效总时长。|
| `currentTime()` | 设置所有子动画的共同时间线位置。|

## 使用场景
面板出现时同时淡入、平移和缩放，或让多条属性动画以同一开始/结束节奏播放。

## 常见坑与经验
- 并行不等于相同持续时间；较短动画结束后会停在最终状态直到组结束。
- 子动画一旦加入 group，通常由 group 管理和启动，不要独立重复启动。
- 需要有先后依赖时用 `QSequentialAnimationGroup` 或嵌套组合。

## 知识点覆盖
并行动画、时间线、所有权、组合动画、属性同步、嵌套编排。
