# QRhiVertexInputAttribute
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiVertexInputAttribute`

## 1. 先建立直觉

`QRhiVertexInputAttribute` 描述顶点结构体里的一个字段如何送进 vertex shader：它来自哪个 binding，进 shader 的哪个 `location`，数据格式是什么，从每个顶点记录的哪个字节偏移开始读。

如果 `QRhiVertexInputBinding` 说的是“一行顶点数据多宽、按顶点还是按实例推进”，那么本类说的是“这一行里的 position/color/uv/normal 分别在哪里”。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型，可比较、可哈希
- 归属：RHI 私有接口，来自 `QRhiVertexInputAttribute`

它最终放进 `QRhiVertexInputLayout`，再交给 `QRhiGraphicsPipeline::setVertexInputLayout()`。它必须与 shader 输入声明一致。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建默认 attribute，通常只适合随后手动设置 |
| `QRhiVertexInputAttribute(binding, location, format, offset, matrixSlice)` | 一次性描述一个顶点输入字段 |
| `binding()` / `setBinding()` | 顶点 buffer binding 编号 |
| `location()` / `setLocation()` | shader 输入 location |
| `format()` / `setFormat()` | 输入数据格式 |
| `offset()` / `setOffset()` | 字段在单个顶点记录内的字节偏移 |
| `matrixSlice()` / `setMatrixSlice()` | 矩阵拆成多个 location 时标记第几片 |
| `operator==` / `operator!=` / `qHash()` | 用于比较、缓存 pipeline key |

## 4. Format 速查

| 格式族 | 典型枚举 | 适合数据 |
| --- | --- | --- |
| 32 位浮点 | `Float`、`Float2`、`Float3`、`Float4` | position、uv、normal、tangent |
| 归一化字节 | `UNormByte`、`UNormByte2`、`UNormByte4` | 颜色、权重、压缩属性 |
| 无符号整数 | `UInt`、`UInt2`、`UInt3`、`UInt4` | bone index、实例 id 类数据 |
| 有符号整数 | `SInt`、`SInt2`、`SInt3`、`SInt4` | 整数属性 |
| 半精度浮点 | `Half`、`Half2`、`Half3`、`Half4` | 带宽敏感的 uv、normal、实例属性 |
| 16 位整数 | `UShort*`、`SShort*` | 压缩索引、短整型实例数据 |

半精度属性依赖 `QRhi::HalfAttributes`。D3D 11/12 对部分 3 分量 16 位格式支持有限，跨平台时最好把 16 位 3 分量填充为 4 分量、8 字节对齐。

## 5. 关键用法

假设顶点结构如下：

```cpp
struct Vertex {
    QVector3D position;
    QVector2D uv;
    quint32 color;
};
```

对应 attribute 可以写成：

```cpp
QRhiVertexInputLayout inputLayout;
inputLayout.setBindings({
    QRhiVertexInputBinding(sizeof(Vertex))
});
inputLayout.setAttributes({
    QRhiVertexInputAttribute(0, 0, QRhiVertexInputAttribute::Float3, offsetof(Vertex, position)),
    QRhiVertexInputAttribute(0, 1, QRhiVertexInputAttribute::Float2, offsetof(Vertex, uv)),
    QRhiVertexInputAttribute(0, 2, QRhiVertexInputAttribute::UNormByte4, offsetof(Vertex, color))
});
```

shader 里必须有匹配的 location，例如 `layout(location = 0) in vec3 position;`。C++ 结构体、attribute format、shader 类型三者不一致时，最常见的表现是画面错乱，而不是立即崩溃。

## 6. 使用场景

- 普通 mesh：position、normal、uv、color。
- 实例化渲染：每实例 transform、颜色、索引。
- 压缩顶点：用 half、normalized byte、short 减少带宽。
- 矩阵属性：实例 transform 的 `mat4` 拆成 4 个连续 location。
- pipeline 缓存：attribute 可比较、可哈希，适合作为布局 key 的一部分。

## 7. 常见坑与经验

- `offset` 是相对单个 binding 的 stride 的字节偏移，不是整个 buffer 的全局偏移。
- `binding` 要对应 `setVertexInput()` 时绑定的 vertex buffer 槽位。
- `UNormByte4` 读入 shader 时是 0 到 1 的浮点归一化，不是 `uvec4`。
- 矩阵属性会消耗多个连续 location，`matrixSlice` 要让 `location - matrixSlice` 回到矩阵起始 location。
- 使用 `offsetof` 比手算字节偏移可靠，尤其结构体有 padding 时。

## 8. 知识点覆盖

本页覆盖：顶点输入 location、binding、format、offset、stride 协作关系，shader 输入匹配，压缩属性，实例矩阵，半精度支持，pipeline 布局缓存。
