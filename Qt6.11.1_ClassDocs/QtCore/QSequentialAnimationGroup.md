# QSequentialAnimationGroup
> Qt 6.11.1 · Qt Core · 来自 `QSequentialAnimationGroup`

## 作用定位
`QSequentialAnimationGroup` 按加入顺序串行播放多个 `QAbstractAnimation`，适合进入、停留、退出等明确阶段的动效编排。
## API 速查
| API | 是做什么的 |
|---|---|
| `addAnimation()` | 将动画追加到序列。 |
| `insertAnimation()` | 在指定阶段插入。 |
| `currentAnimation()` | 查询当前正在运行的子动画。 |
| `currentAnimationChanged()` | 当前阶段切换时通知。 |
| 继承的 `start/stop/pause` | 控制整个序列。 |
## 使用场景
```cpp
auto *group = new QSequentialAnimationGroup(this);
group->addAnimation(fadeIn);
group->addPause(200);
group->addAnimation(fadeOut);
group->start(QAbstractAnimation::DeleteWhenStopped);
```
## 常见坑与经验
- 子动画被 group 接管；不要再独立删除。
- 动画目标对象必须比动画活得久。
- 在运行中改组结构会影响当前时间轴，复杂交互先停止再重建。
## 知识点覆盖
动画时间轴、对象所有权、暂停阶段、状态机式动效、生命周期。
