# QSGGeometry::Attribute：描述一个顶点字段如何传给材质

> Qt 6.11.1 | `#include <QSGGeometry>` | CMake: `Qt6::Quick`

`QSGGeometry::Attribute` 描述自定义顶点结构中的一个字段：它位于哪个 attribute register、包含几个分量、分量的数据类型，以及它代表位置、颜色还是纹理坐标。`QSGGeometry::AttributeSet` 用这些描述计算顶点 stride，`QSGGeometry` 再据此解释 `vertexData()` 的内存。

它用于标准 `Point2D` 等内置布局无法表达的场景，例如位置加自定义颜色、额外 UV、实例数据或专用材质输入。此类型是普通 C++ 元数据，不是 QObject；真正的限制来自它被 geometry 按引用保存，因而不能只存在于临时局部数组中。

```cpp
struct Vertex {
    float x, y;
    uchar r, g, b, a;
};

static QSGGeometry::Attribute attributes[] = {
    QSGGeometry::Attribute::createWithAttributeType(
        0, 2, QSGGeometry::FloatType, QSGGeometry::PositionAttribute),
    QSGGeometry::Attribute::createWithAttributeType(
        1, 4, QSGGeometry::UnsignedByteType, QSGGeometry::ColorAttribute)
};
static QSGGeometry::AttributeSet layout = {
    2, int(sizeof(Vertex)), attributes
};
```

attribute 的 register `position` 必须和 material shader 期望的输入位置相匹配；`tupleSize`、`primitiveType` 和 `AttributeSet::stride` 必须与真实 `Vertex` 内存布局一致。错一个字段不会由 Qt 自动修复，通常表现为顶点错位、颜色混乱或 backend validation 报错。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `position` | shader attribute register/位置 | 必须与材质 shader 的输入布局一致 |
| `tupleSize` | 此字段包含的分量数 | 例如二维位置为 2、RGBA 颜色为 4 |
| `type` | 每个分量的 `QSGGeometry::Type` | 与 C++ 字段类型和真实字节布局一致 |
| `isVertexCoordinate` | 标记该字段是否是顶点位置 | 是 renderer 可用的优化提示；推荐用工厂函数初始化 |
| `attributeType` | 标记 Position/Color/TexCoord 等语义 | 可让 renderer/材质理解字段用途，选择与数据一致的枚举 |
| `create(pos, tupleSize, primitiveType, isPosition)` | 创建 attribute，并可设置位置提示 | 比手工聚合初始化更安全，保留字段会被正确初始化 |
| `createWithAttributeType(pos, tupleSize, primitiveType, type)` | 创建带明确语义类型的 attribute | 自定义 shader 布局时优先使用，仍需保证 register 匹配 |
