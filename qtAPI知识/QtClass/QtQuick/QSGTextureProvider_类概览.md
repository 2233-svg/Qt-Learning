# QSGTextureProvider：向其他场景图项暴露动态纹理

> Qt 6.11.1 · `#include <QSGTextureProvider>` · 模块：`Qt6::Quick` · 继承：`QObject`

`QSGTextureProvider` 是“这个对象可以提供一张供场景图采样的纹理”的小型接口。它让一个 Item、图层或自定义图形源能够把自己的输出交给另一个 Item 使用，而无需暴露底层渲染实现。

## 典型场景

`ShaderEffectSource`、带 layer 的 Item 以及实现了纹理提供能力的自定义 Item，都可被消费方识别为纹理来源。消费者在场景图同步/渲染路径中取得 provider，读取 `texture()`，并连接 `textureChanged()` 以便在源图更新时刷新自身节点或材质。

```cpp
QSGTextureProvider *provider = sourceItem->textureProvider();
connect(provider, &QSGTextureProvider::textureChanged,
        this, &Consumer::scheduleSceneGraphUpdate);
```

上例中的连接策略必须配合线程模型设计：provider 主要存在于场景图渲染线程，不能在 GUI 线程槽函数中直接访问其 `QSGTexture`。

## 语义与边界

`texture()` 返回的是裸指针，不表达调用方拥有所有权，也不保证纹理在 provider 下一次更新后仍代表同一底层资源。收到 `textureChanged()` 后应在正确的渲染阶段重新查询，而不是长期保存旧纹理指针。

该类的主要工作线程是场景图渲染线程。业务线程只应维护 Item 属性和触发 `update()`；纹理获取、材质重绑、QRhi 操作应留在由 Qt Quick 调度的场景图阶段。

## API 速查表

| API | 语义与边界 |
|---|---|
| `texture()` | 纯虚函数，返回当前 `QSGTexture *`；不转移所有权，只应在场景图线程使用。 |
| `textureChanged()` | 当前纹理或其内容变动时发出的信号；处理方应重新查询纹理并安排渲染侧更新。 |
| `QObject` 生命周期 | provider 销毁会使已保存的裸指针失效；不要把纹理的销毁责任交给消费者。 |
