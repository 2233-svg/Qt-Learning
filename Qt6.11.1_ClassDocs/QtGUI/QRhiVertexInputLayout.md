# QRhiVertexInputLayout
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiVertexInputLayout`

## 1. 先建立直觉

`QRhiVertexInputLayout` 是 graphics pipeline 的顶点输入总说明。它把一组 `QRhiVertexInputBinding` 和一组 `QRhiVertexInputAttribute` 放在一起，让 RHI 知道顶点 buffer 的记录宽度、推进方式，以及每个 shader input location 从哪里读。

如果 shader 是“我要 location 0/1/2”，layout 就是“这些 location 在哪些 buffer、哪些偏移、什么格式”。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型，可比较、可哈希
- 归属：RHI 私有接口，来自 `QRhiVertexInputLayout`
- 主要使用者：`QRhiGraphicsPipeline::setVertexInputLayout()`

layout 是 pipeline 状态的一部分。改变顶点结构、binding 数量、attribute format 或 location，都意味着 pipeline 需要使用新的 layout 创建。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建空 layout |
| `setBindings(...)` | 设置所有 vertex input binding |
| `bindingCount()` / `bindingAt()` | 查询 binding 数量和指定 binding |
| `cbeginBindings()` / `cendBindings()` | 遍历 binding |
| `setAttributes(...)` | 设置所有 attribute |
| `attributeCount()` / `attributeAt()` | 查询 attribute 数量和指定 attribute |
| `cbeginAttributes()` / `cendAttributes()` | 遍历 attribute |
| `operator==` / `operator!=` / `qHash()` | 用于 pipeline cache key |

## 4. 关键用法

典型 layout：

```cpp
QRhiVertexInputLayout inputLayout;
inputLayout.setBindings({
    QRhiVertexInputBinding(sizeof(Vertex))
});
inputLayout.setAttributes({
    QRhiVertexInputAttribute(0, 0, QRhiVertexInputAttribute::Float3, offsetof(Vertex, position)),
    QRhiVertexInputAttribute(0, 1, QRhiVertexInputAttribute::Float2, offsetof(Vertex, uv))
});

pipeline->setVertexInputLayout(inputLayout);
```

实例化渲染时增加第二个 binding：

```cpp
inputLayout.setBindings({
    QRhiVertexInputBinding(sizeof(Vertex), QRhiVertexInputBinding::PerVertex),
    QRhiVertexInputBinding(sizeof(InstanceData), QRhiVertexInputBinding::PerInstance)
});
```

然后把实例数据的 attributes 的 `binding` 设为 1。命令录制时，也要给 slot 0 和 slot 1 分别绑定实际 `QRhiBuffer`。

## 5. 使用场景

- 固定 mesh 顶点格式：position、normal、uv、color。
- 多种材质 pipeline 共享同一个 vertex layout。
- 实例化绘制，混合 per-vertex 和 per-instance 数据。
- 动态生成 pipeline cache key，避免重复创建相同管线。
- 跨后端渲染抽象，把 OpenGL/Vulkan/D3D/Metal 的输入布局统一到 RHI 描述。

## 6. 常见坑与经验

- layout 必须与 shader 输入 location 完全吻合；多一个少一个都可能导致验证错误或未定义画面。
- attribute 的 `binding` 必须小于 `bindingCount()`，并对应实际命令里绑定的 buffer slot。
- 修改 layout 后只改 pipeline 对象字段不够，通常要重新 `create()` pipeline。
- C++ 顶点结构体的 padding 会影响 offset 和 stride，用 `offsetof` 与 `sizeof` 不要手算。
- `qHash()` 很适合做 pipeline 缓存，但缓存 key 还应包含 shader、blend、depth、render pass descriptor 等其他状态。

## 7. 知识点覆盖

本页覆盖：顶点输入布局、binding/attribute 组合、shader location 匹配、实例化布局、多 buffer 输入、pipeline 状态与缓存。
