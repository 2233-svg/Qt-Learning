# QSGMaterialType：材质 shader 缓存使用的唯一身份令牌

> Qt 6.11.1 · `#include <QSGMaterialType>` · 模块：`Qt6::Quick`

`QSGMaterialType` 是一个空结构体，却承担了自定义 `QSGMaterial` 最重要的身份职责：它告诉场景图“这些材质实例应共享同一个 `QSGMaterialShader` 实现”。

## 它解决的问题

Qt Quick 会为每个材质类型与渲染模式缓存 shader。材质实例可能只在颜色、纹理或 uniform 值上不同，因而应该返回同一个静态令牌；场景图即可复用 shader 和 pipeline 准备工作。

```cpp
QSGMaterialType *MyMaterial::type() const
{
    static QSGMaterialType type;
    return &type;
}
```

如果同一 C++ 材质类会选择不同的顶点/片段 shader 组合，则每个组合必须返回不同的静态 `QSGMaterialType`。否则 Qt Quick 可能错误复用先创建的 shader，形成难以定位的渲染错误。

## 边界

这个类型在 `QSGMaterial::type()` 之外没有业务用途，没有字段和成员函数，也不是运行时类别反射系统。它只利用对象地址作为稳定、类型安全、唯一的缓存键。

与其他 QSG 类一样，它只应在场景图渲染线程相关路径使用。最常用实现是函数内 `static` 对象：地址稳定、无需手动销毁，也自然保证同类材质共享同一令牌。

## API 速查表

| API / 约定 | 语义与边界 |
|---|---|
| `QSGMaterialType` | 空身份类型，没有公开成员函数或数据字段。 |
| `QSGMaterial::type()` | 必须返回指向唯一令牌的指针；这是该类型唯一的预期用途。 |
| 函数内 `static QSGMaterialType` | 常用写法，提供稳定地址并让所有同 shader 组合的材质实例共享类型。 |
| 不同 shader 组合 | 必须使用不同令牌，否则场景图会按同类型复用错误的 `QSGMaterialShader`。 |
