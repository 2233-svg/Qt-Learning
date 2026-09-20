# Qt Quick 3D（下）：交互拾取、实例化、动画与性能

本篇建立在可正确显示的 Quick 3D 场景之上，继续解决“如何让用户操作场景”和“如何稳定运行在目标设备”两个问题。内容包括拾取、坐标转换、相机控制、实例化、粒子、骨骼动画、运行时资产加载、离屏渲染和性能排查。

## 1. 从 2D 指针到 3D 拾取

`View3D::pick(x, y)` 接收 View 内的 2D 坐标，返回 `PickResult`：

```qml
TapHandler {
    onTapped: function(eventPoint) {
        const p = eventPoint.position
        const result = view3d.pick(p.x, p.y)
        if (result.objectHit) {
            console.log("命中:", result.objectHit)
            console.log("场景坐标:", result.scenePosition)
            console.log("UV:", result.uvPosition)
        }
    }
}
```

模型必须启用拾取，并具有可用于碰撞检测的几何数据。屏幕上看得见不等于一定能被拾取；若 `objectHit` 为空，检查对象可见性、拾取设置、相机和坐标是否相对于正确的 `View3D`。

## 2. 可拾取对象与选择状态

```qml
Model {
    id: product
    source: "meshes/product.mesh"
    pickable: true

    materials: PrincipledMaterial {
        baseColor: product.selected ? "#ef5350" : "#e0e0e0"
    }

    property bool selected: false
}
```

点击后只修改业务选择状态，不要永久替换原材质对象。复杂模型可通过材质参数、轮廓后处理或单独的高亮副本表达选择，退出选择时才能可靠恢复。

## 3. 轨道相机交互

### 3.1 拖动旋转

```qml
DragHandler {
    target: null
    property real startYaw
    property real startPitch

    onActiveChanged: if (active) {
        startYaw = cameraRig.eulerRotation.y
        startPitch = cameraTilt.eulerRotation.x
    }

    onTranslationChanged: {
        cameraRig.eulerRotation.y = startYaw + translation.x * 0.25
        cameraTilt.eulerRotation.x = Math.max(-80,
            Math.min(80, startPitch - translation.y * 0.25))
    }
}
```

俯仰角需要限制，否则相机越过极点后左右方向会反转。拖动速度使用固定逻辑值，不要直接随窗口宽度缩放，保证不同屏幕上的操作一致。

### 3.2 滚轮缩放

```qml
WheelHandler {
    target: null
    onWheel: function(event) {
        const next = camera.z - event.angleDelta.y * 0.35
        camera.z = Math.max(150, Math.min(1600, next))
    }
}
```

缩放范围应结合模型包围盒计算。相机不能进入模型内部，也不应越过近裁剪面。触控设备可添加 `PinchHandler`，将缩放映射到相机距离而非模型缩放。

## 4. 坐标映射与 3D 标注

产品标签和数据提示通常是 2D Item，但需要跟随 3D 点移动。使用 View3D 的场景到视图映射 API：

```qml
Item {
    id: marker
    property vector3d worldPoint: Qt.vector3d(0, 100, 0)
    property vector3d projected: view3d.mapFrom3DScene(worldPoint)

    x: projected.x - width / 2
    y: projected.y - height
    visible: projected.z > 0
}
```

还要做遮挡判断：点在相机前方不代表没有被其他模型挡住。可从标注屏幕位置向场景拾取，比较最近命中距离与目标点距离。

## 5. 实例化大量相同网格

创建上千个独立 `Model` 会产生大量 QML 对象和绘制状态。实例化让多个对象共享一个网格和材质，只传递不同的变换与颜色。

```qml
Model {
    source: "#Cube"
    instancing: InstanceList {
        instances: [
            InstanceListEntry { position: Qt.vector3d(-100, 0, 0) },
            InstanceListEntry { position: Qt.vector3d(0, 0, 0) },
            InstanceListEntry { position: Qt.vector3d(100, 0, 0) }
        ]
    }
    materials: PrincipledMaterial { baseColor: "#42a5f5" }
}
```

静态大量数据可使用自定义实例表或随机实例化组件。实例化适合相同网格和材质；如果每个对象的材质、骨骼或拓扑都不同，就无法在一次实例绘制中合并。

## 6. 粒子系统

Qt Quick 3D Particles 提供发射器、粒子、影响器和轨迹：

```qml
import QtQuick3D.Particles3D

ParticleSystem3D {
    id: system

    SpriteParticle3D {
        id: sparks
        sprite: Texture { source: "images/spark.png" }
        maxAmount: 800
        color: "#ffca55"
    }

    ParticleEmitter3D {
        particle: sparks
        emitRate: 120
        lifeSpan: 900
        velocity: VectorDirection3D {
            direction: Qt.vector3d(0, 120, 0)
            directionVariation: Qt.vector3d(80, 30, 80)
        }
    }
}
```

粒子数量、透明填充面积和 overdraw 会直接影响性能。效果不可见时暂停系统；移动端优先使用小纹理、较短生命周期和受控的最大粒子数。

## 7. 导入动画资产

包含骨骼和关键帧动画的资产通常通过 glTF 等格式导入。导入结果会生成节点、模型、骨骼和动画时间线，QML 侧控制时间或动画片段：

```qml
TimelineAnimation {
    id: walkAnimation
    running: true
    loops: Animation.Infinite
    duration: 1200
    from: 0
    to: 1200
}
```

导入前在 DCC 工具中处理好骨骼层级、蒙皮权重、动画帧率和循环边界。运行时修复错误骨骼比重新导出成本高，也容易造成平台差异。

## 8. 运行时加载资产

`RuntimeLoader` 可以在程序运行时加载支持的 3D 文件：

```qml
import QtQuick3D.AssetUtils

RuntimeLoader {
    id: loader
    source: "file:///D:/models/product.glb"

    onStatusChanged: {
        if (status === RuntimeLoader.Error)
            console.warn("加载失败:", errorString)
    }
}
```

运行时加载适合用户导入和可下载内容，但必须限制文件大小、纹理分辨率、节点数量和可访问路径。不可信模型可能造成内存耗尽或长时间解析，最好在隔离进程中做预检。

## 9. 2D 内容作为 3D 材质

可以将 Qt Quick Item 渲染到纹理，再贴到 3D 模型：

```qml
Rectangle {
    id: panelUi
    width: 512
    height: 256
    color: "#20252b"
    Text { anchors.centerIn: parent; text: qsTr("System ready") }
}

Model {
    source: "#Rectangle"
    materials: PrincipledMaterial {
        baseColorMap: Texture { sourceItem: panelUi }
    }
}
```

`sourceItem` 会产生额外渲染工作。只在内容变化时更新，避免把复杂、持续动画的完整界面复制到多个材质中。

## 10. 渲染模式与合成

`View3D` 可以直接参与主场景渲染，也可以先渲染到纹理再合成。选择取决于是否需要 2D/3D 交错、后处理和缓存。直接渲染通常开销较低；离屏模式更灵活，但会占用额外颜色/深度缓冲和带宽。

## 11. 阴影与画质成本

阴影问题应按顺序排查：

1. 光源是否启用 `castsShadow`。
2. 模型是否允许投射和接收阴影。
3. 阴影贴图尺寸和相机覆盖范围是否合适。
4. bias 是否导致悬浮或自阴影条纹。

每个动态投影光源都可能额外渲染一遍场景。先减少投影光源数量，再调整贴图质量，通常比盲目降低模型精度更有效。

## 12. 性能分析方法

### 12.1 先区分 CPU 和 GPU 瓶颈

- CPU 瓶颈：大量 QML 对象、绑定反复求值、频繁资源创建、场景树遍历。
- GPU 瓶颈：高分辨率、多光源阴影、透明 overdraw、复杂材质、后处理。
- I/O 瓶颈：运行时加载大模型、纹理解码和着色器首次编译。

用 Qt Quick Profiler、渲染统计和平台 GPU 工具分别验证，不要只凭帧率猜测。

### 12.2 常见优化顺序

1. 删除不可见或永不使用的节点和材质。
2. 合并相同材质，使用实例化。
3. 限制动态阴影和透明层。
4. 为纹理生成 mipmap，并按设备选择分辨率。
5. 降低离屏渲染目标和 MSAA 成本。
6. 预热或缓存运行时资产与着色器。

## 13. 资源生命周期

资源从 `source` 移除后，不一定立即释放 GPU 内存；场景图会在渲染线程安全点清理。频繁切换大模型时使用加载页面和容量预算，避免同时保留旧模型、新模型和解码临时数据。

动态创建对象应设置明确父节点：

```qml
const object = component.createObject(sceneRoot, {
    position: Qt.vector3d(0, 0, 0)
})
// 不再需要时：object.destroy()
```

不要仅从数组中删除引用而忘记销毁 QML 对象。

## 14. 跨后端与部署测试

Quick 3D 通过 RHI 支持多种图形 API，但驱动精度、纹理格式和着色器限制仍可能不同。发布前至少验证：

- Windows 的 Direct3D 后端。
- macOS/iOS 的 Metal 后端。
- Linux/Android 的实际 Vulkan 或 OpenGL 后端。
- 集成显卡和高 DPI/多屏场景。

不要强制切换后端来掩盖资源或着色器错误；应保留可诊断日志，并在设备不满足能力要求时提供明确降级。

## 15. 速查表

| 目标 | API/类型 |
| --- | --- |
| 2D 坐标拾取 | `View3D::pick()`、`PickResult` |
| 3D 点投影到界面 | `mapFrom3DScene()` |
| 轨道相机 | 父 `Node` + `DragHandler`/`WheelHandler` |
| 大量相同模型 | `InstanceList`、`InstanceListEntry` |
| 3D 粒子 | `ParticleSystem3D`、`ParticleEmitter3D` |
| 用户模型导入 | `RuntimeLoader` |
| 2D 界面贴图 | `Texture::sourceItem` |
| 场景画质 | `SceneEnvironment` |

到这里，Qt Quick 3D 已从静态展示扩展到可交互、可加载、可测量的 3D 应用。下一步若需要定制渲染效果，应进入 Qt Shader Tools 和 `CustomMaterial`，而不是直接绕开 Qt 的渲染管线。
