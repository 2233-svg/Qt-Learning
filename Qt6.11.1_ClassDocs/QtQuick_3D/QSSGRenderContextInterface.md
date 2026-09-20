# QSSGRenderContextInterface
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGRenderContextInterface`

## 1. 先建立直觉

`QSSGRenderContextInterface` 是 Quick 3D 渲染上下文的窄接口，主要给扩展拿到 `QSSGRhiContext`。它把内部庞大的渲染上下文收束成可公开访问的小入口。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGRenderContextInterface`，属于 Qt Quick 3D 模块，用于访问渲染上下文中的 RHI 资源。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `rhiContext()` | 返回当前 `QSSGRhiContext` 的 unique_ptr 引用。 |

## 4. 常见坑与经验

拿到的是上下文引用，不代表你拥有它。不要释放、替换或跨生命周期保存。

访问 RHI 资源要在允许的渲染阶段进行；GUI 线程里的业务代码不应该直接操作这些对象。

## 5. 知识点覆盖

- Quick 3D render context 公开接口。
- RHI context 访问和所有权边界。
