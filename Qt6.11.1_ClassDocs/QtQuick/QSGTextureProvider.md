# QSGTextureProvider
> Qt 6.11.1 · Qt Quick · 来自 `QSGTextureProvider`

## 作用定位
`QSGTextureProvider` 让一个对象把当前可用的 Scene Graph 纹理暴露给其他节点或效果使用。`ShaderEffectSource`、自定义纹理项等会用到它。

## API 速查
| API | 是做什么的 |
|---|---|
| `texture()` | 返回当前纹理对象。|
| `textureChanged()` | 通知纹理对象或内容发生变化。|

## 使用场景
自定义 item 输出一张动态纹理，供另一个材质采样，实现后处理、镜像或合成。

## 常见坑与经验
- 纹理 provider 的对象和纹理通常与窗口场景图绑定，不能跨窗口复用。
- 内容变了但对象没变时也可能需要发 `textureChanged()`，取决于消费者是否会主动刷新。

## 知识点覆盖
纹理共享、动态效果、跨节点采样、Scene Graph 生命周期。
