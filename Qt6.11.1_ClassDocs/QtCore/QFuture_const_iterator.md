# QFuture::const_iterator
> Qt 6.11.1 · Qt Core · 来自 `QFuture::const_iterator`

## 作用定位
`QFuture::const_iterator` 提供对 `QFuture` 结果序列的只读迭代访问，适合结果已经就绪或允许按需等待的遍历场景。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取当前结果。|
| `operator++()` | 移到下一个结果。|
| `operator==()` | 比较迭代位置。|
| `begin()` / `end()` | 获取 future 的遍历边界。|

## 使用场景
在后台线程或任务完成后，以 range-for 处理多结果 future。

## 常见坑与经验
- 若结果尚未产生，解引用或推进的等待行为会阻塞当前线程；GUI 代码优先用 watcher。
- future 取消或异常结束时，遍历代码也要有错误处理路径。

## 知识点覆盖
结果迭代、Future、多结果、阻塞、异常、线程边界。
