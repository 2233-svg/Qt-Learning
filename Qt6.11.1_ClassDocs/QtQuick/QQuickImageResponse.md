# QQuickImageResponse
> Qt 6.11.1 · Qt Quick · 来自 `QQuickImageResponse`

## 作用定位
`QQuickImageResponse` 表示一次异步图像请求的最终结果。它把后台工作产生的 `QQuickTextureFactory` 交还给 Qt Quick，并用 `finished()` 表示结果已可消费。

## API 速查
| API | 是做什么的 |
|---|---|
| `textureFactory()` | 必须重实现，返回完成后的纹理工厂。|
| `errorString()` | 出错时提供可诊断的文本。|
| `finished()` | 通知 Qt Quick 请求已完成，不区分成功或失败。|
| `cancel()` | Qt Quick 不再需要结果时请求取消。|

## 使用场景
子类把工作交给线程池；工作完成后保存不可变图像并发射 `finished()`。`textureFactory()` 应足够轻量，只把已得到的结果包装起来。

## 常见坑与经验
- `cancel()` 是协作式取消，不会强杀线程；耗时任务需要主动检查取消标志。
- 失败也必须发 `finished()`，并由 `errorString()` 给出原因，否则 QML 请求会悬挂。
- 发出 `finished()` 后不要再改动返回的图像数据。

## 知识点覆盖
异步协议、协作取消、错误传播、线程池、纹理工厂、结果不可变性。
