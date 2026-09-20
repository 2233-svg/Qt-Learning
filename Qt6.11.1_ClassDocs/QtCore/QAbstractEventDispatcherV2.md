# QAbstractEventDispatcherV2
> Qt 6.11.1 · Qt Core · 来自 `QAbstractEventDispatcherV2`

## 作用定位
`QAbstractEventDispatcherV2` 是事件分发器的新接口版本，为更现代的定时器和事件处理能力提供扩展点。

## API 速查
| API | 是做什么的 |
|---|---|
| `processEvents()` | 按传入选项分发事件。|
| `registerTimer()` | 注册带时间类型信息的计时器。|
| `timersForObject()` | 查询对象当前注册计时器。|
| `wakeUp()` / `interrupt()` | 唤醒或中断事件处理。|

## 使用场景
仅在编写自定义 QPA 平台插件或深度嵌入外部事件循环时使用。

## 常见坑与经验
- 应用层定时需求用 `QTimer` 或 `QChronoTimer`；不要直接依赖 dispatcher 私有调度细节。

## 知识点覆盖
事件分发器演进、平台插件、时间类型、线程事件循环。
