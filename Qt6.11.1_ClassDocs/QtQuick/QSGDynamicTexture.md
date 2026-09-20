# QSGDynamicTexture
> Qt 6.11.1 · Qt Quick · 来自 `QSGDynamicTexture`

## 作用定位
`QSGDynamicTexture` 表示内容会持续改变的纹理，例如视频帧、摄像头画面或外部渲染结果。

## API 速查
| API | 是做什么的 |
|---|---|
| `updateTexture()` | 拉取或提交最新纹理内容；有变化时返回真。|

## 使用场景
自定义 texture provider 将生产者的新帧暴露给 QML 时实现它，并在每帧合适时更新底层资源。

## 常见坑与经验
- `updateTexture()` 运行于渲染相关路径，不能在其中做网络请求、磁盘解码等耗时操作。
- 没有新帧时返回 false，避免触发不必要的状态更新。

## 知识点覆盖
动态纹理、生产者消费者、实时画面、渲染线程、帧节流。
