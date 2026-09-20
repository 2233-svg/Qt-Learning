# QQuick3DObject
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3DObject`

## 1. 先建立直觉

`QQuick3DObject` 是一批 C++ Quick 3D 扩展对象的基类。它不是普通 3D 节点的全部功能集合，而是给几何、实例化、纹理数据、渲染扩展等对象提供 QML 生命周期、parent 关系和 state 属性。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3DObject`，属于 Qt Quick 3D 模块，用于 Quick 3D C++ 扩展对象的共同基类。

它继承 `QObject` 和 `QQmlParserStatus`，说明它关心 QML 组件创建完成阶段。很多派生类会在 QML 属性收齐后同步到底层渲染节点。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `parent : QQuick3DObject*` | Quick 3D 对象层级父对象，不等同于所有 QObject 父子场景都可混用。 |
| `state : QString` | QML State 机制使用的状态名。 |
| `parentItem()` / `setParentItem()` | 读取或设置 Quick 3D parent。 |
| `state()` / `setState()` | 读取或设置状态。 |
| `parentChanged()` / `stateChanged()` | 对应属性变化信号。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 写自定义 geometry/texture/extension | 继承链中会接触它。 |
| 从 C++ 操作 Quick 3D 扩展对象 | 需要理解 parentItem 和 QObject parent 的差别。 |
| QML 状态驱动 3D 扩展属性 | 使用 `state` 与 QML 状态系统配合。 |

## 5. 常见坑与经验

不要把 `parentItem()` 简单等同于 QObject parent。Quick 3D 的对象层级影响场景/资源关系，QObject parent 更偏生命周期管理。

渲染相关派生类的属性改变通常不会立即变成 GPU 资源更新，而是在 Quick/scene graph 的同步阶段生效。

## 6. 知识点覆盖

- Quick 3D 扩展对象基类。
- QML parser status、state、parentItem。
- GUI/QML 对象与渲染节点同步边界。
