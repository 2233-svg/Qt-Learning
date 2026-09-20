# QSGGeometry::AttributeSet：一份顶点布局的计数、步长与字段数组

> Qt 6.11.1 | `#include <QSGGeometry>` | CMake: `Qt6::Quick`

`QSGGeometry::AttributeSet` 不是 Qt 容器，而是一个轻量 POD 描述：`count` 表示 attribute 数量，`stride` 表示一个顶点占多少字节，`attributes` 指向 `QSGGeometry::Attribute` 数组。它把 C++ 顶点结构的内存布局告诉 `QSGGeometry` 和材质 shader。

常见场景是自定义顶点类型：位置、颜色和 UV 混在一个 `struct Vertex` 中，随后用一个静态 `AttributeSet` 创建 geometry。Qt 不拥有或复制 `AttributeSet` 和它的数组，因而最重要的规则是二者必须比引用它的 `QSGGeometry` 活得久。

```cpp
struct Vertex { float x, y, u, v; };
static QSGGeometry::Attribute attrs[] = {
    QSGGeometry::Attribute::createWithAttributeType(
        0, 2, QSGGeometry::FloatType, QSGGeometry::PositionAttribute),
    QSGGeometry::Attribute::createWithAttributeType(
        1, 2, QSGGeometry::FloatType, QSGGeometry::TexCoordAttribute)
};
static QSGGeometry::AttributeSet layout {
    2, int(sizeof(Vertex)), attrs
};
```

`stride` 应为相邻顶点起始地址的字节距离，通常是 `sizeof(Vertex)`，并且要包含编译器插入的 padding。`count` 必须与数组元素数相同；若内容按 `Vertex` 结构写入却把 stride 填为字段大小，第二个顶点开始的所有读取都会错位。

## API 速查表

| 字段 | 语义 | 关键边界 |
|---|---|---|
| `count` | `attributes` 数组中的 attribute 数量 | 必须与真实数组长度一致 |
| `stride` | 一个顶点的字节跨度 | 通常为 `sizeof(Vertex)`，包括 C++ 对齐填充 |
| `attributes` | 指向顶点字段描述数组 | 指针、数组和 `AttributeSet` 本身必须覆盖 `QSGGeometry` 整个生命期 |
| `QSGGeometry(attributes, ...)` | 以本布局创建 geometry | geometry 仅保存引用，不复制 `AttributeSet` |
