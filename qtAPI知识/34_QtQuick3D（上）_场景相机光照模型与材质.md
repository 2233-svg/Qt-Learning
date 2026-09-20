# Qt Quick 3D（上）：场景、相机、光照、模型与材质

Qt Quick 3D 让 QML 应用在同一场景图中组合 2D 界面和 3D 内容。它适合产品展示、仪表盘、轻量可视化和交互式配置器；其重点不是让开发者手写渲染循环，而是用声明式对象描述场景，由 Qt Rendering Hardware Interface（RHI）适配 Direct3D、Metal、Vulkan 或 OpenGL。

本文从一个可见的立方体开始，逐步解释 `View3D`、`Node`、相机、光源、模型、材质、纹理和动画。

## 1. 模块与 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick Quick3D)

qt_add_executable(mytarget main.cpp)

qt_add_qml_module(mytarget
    URI MyApp
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(mytarget PRIVATE
    Qt6::Quick
    Qt6::Quick3D
)
```

QML 导入：

```qml
import QtQuick
import QtQuick3D
```

部署时应使用 `windeployqt`、`macdeployqt` 或 CMake 安装规则带上 Quick 3D 插件和图形后端。开发机可运行不代表发布目录中的 QML 模块一定完整。

## 2. 最小可见场景

```qml
import QtQuick
import QtQuick3D

Window {
    width: 960
    height: 640
    visible: true
    color: "#202124"

    View3D {
        anchors.fill: parent

        environment: SceneEnvironment {
            clearColor: "#202124"
            backgroundMode: SceneEnvironment.Color
        }

        PerspectiveCamera {
            position: Qt.vector3d(0, 0, 500)
        }

        DirectionalLight {
            eulerRotation.x: -35
            eulerRotation.y: -25
            brightness: 1.2
        }

        Model {
            source: "#Cube"
            scale: Qt.vector3d(1.4, 1.4, 1.4)
            materials: PrincipledMaterial {
                baseColor: "#4db6ac"
                roughness: 0.35
            }
        }
    }
}
```

如果窗口只有背景色，依次检查：相机是否朝向模型、模型是否位于视锥内、是否有光源、材质是否可见、资源路径是否正确，以及图形后端是否成功初始化。

## 3. `View3D`：2D 与 3D 的边界

`View3D` 是一个 Qt Quick Item，它把 3D 场景渲染到 2D 界面中的一个区域。普通按钮、面板和文字仍是 2D Item，可以覆盖在 `View3D` 上方：

```qml
Item {
    View3D { anchors.fill: parent }

    Button {
        anchors.right: parent.right
        anchors.top: parent.top
        text: qsTr("Reset view")
        onClicked: cameraRig.eulerRotation = Qt.vector3d(0, 0, 0)
    }
}
```

不要为每个 3D 对象创建一个 `View3D`。同一空间中的对象应共享场景、相机和渲染环境，多个 View 会增加渲染目标和资源开销。

## 4. 坐标系与 `Node`

### 4.1 局部变换

`Node` 是 3D 场景层级的基础对象，提供 `position`、`rotation`/`eulerRotation`、`scale` 和可见性等属性：

```qml
Node {
    id: assembly
    position: Qt.vector3d(0, 40, 0)
    eulerRotation.y: 25

    Model {
        source: "#Cylinder"
        position.x: -80
    }

    Model {
        source: "#Sphere"
        position.x: 80
    }
}
```

子节点的变换相对于父节点。旋转 `assembly` 会整体带动两个模型，而模型之间的局部位置保持不变。这是构建机械结构、车辆和角色骨架的核心方法。

### 4.2 局部坐标与场景坐标

节点 API 可以在局部和场景坐标之间映射位置与方向。交互拾取、相机跟随和物理计算时先明确数据属于哪个坐标空间，避免把局部位置直接当作世界位置。

## 5. 相机

### 5.1 透视相机

`PerspectiveCamera` 模拟人眼和普通相机，远处物体更小：

```qml
PerspectiveCamera {
    id: camera
    position: Qt.vector3d(0, 120, 600)
    eulerRotation.x: -10
    fieldOfView: 45
    clipNear: 10
    clipFar: 5000
}
```

近远裁剪面不要设得过于悬殊。`clipNear` 极小而 `clipFar` 极大时，深度缓冲精度下降，容易出现表面闪烁（z-fighting）。

### 5.2 正交相机

`OrthographicCamera` 不产生透视缩小，适合 CAD 预览、图标和等距视觉：

```qml
OrthographicCamera {
    position: Qt.vector3d(0, 0, 500)
    horizontalMagnification: 2
    verticalMagnification: 2
}
```

### 5.3 相机支架模式

把相机放在父 `Node` 中，分别控制环绕和距离，比直接计算相机矩阵更清晰：

```qml
Node {
    id: cameraRig
    eulerRotation.y: 30

    Node {
        id: cameraTilt
        eulerRotation.x: -15

        PerspectiveCamera {
            id: camera
            z: 600
        }
    }
}
```

拖动水平方向修改 `cameraRig.eulerRotation.y`，垂直方向修改 `cameraTilt.eulerRotation.x`，滚轮修改相机 `z`，即可得到基本轨道相机。

## 6. 光源

### 6.1 方向光

`DirectionalLight` 类似无限远太阳，只关心方向，不随距离衰减：

```qml
DirectionalLight {
    eulerRotation: Qt.vector3d(-45, -35, 0)
    color: "#fff4e5"
    brightness: 1.5
    castsShadow: true
}
```

### 6.2 点光源和聚光灯

```qml
PointLight {
    position: Qt.vector3d(0, 200, 200)
    brightness: 250
    quadraticFade: 0.01
}

SpotLight {
    position: Qt.vector3d(200, 250, 300)
    eulerRotation: Qt.vector3d(-35, 25, 0)
    coneAngle: 35
    innerConeAngle: 25
}
```

点光源向所有方向发光，聚光灯限制在锥体内。动态光源和阴影数量越多，GPU 成本越高；移动端优先使用少量主光源和环境光照。

## 7. 模型与网格资源

### 7.1 内置基础几何体

```qml
Model { source: "#Cube" }
Model { source: "#Sphere" }
Model { source: "#Cylinder" }
Model { source: "#Cone" }
Model { source: "#Rectangle" }
```

基础几何体适合原型和调试。正式资产通常由 Blender、Maya 等工具导出为 glTF 2.0 等格式，再由 Qt Quick 3D 的资产管线处理。

### 7.2 外部模型

```qml
Model {
    source: "meshes/product.mesh"
    materials: [bodyMaterial, metalMaterial]
}
```

模型的材质数组顺序要与网格子集一致。缺失法线会影响光照，缺失切线会影响法线贴图；导入后应检查单位、朝向、UV、法线和包围盒。

## 8. `PrincipledMaterial`

`PrincipledMaterial` 基于物理材质模型，常用参数包括基础色、金属度、粗糙度、不透明度和各种纹理：

```qml
PrincipledMaterial {
    id: paintedMetal
    baseColor: "#d8483e"
    metalness: 0.65
    roughness: 0.28
    opacity: 1.0
}
```

- 非金属通常 `metalness` 接近 0。
- 金属通常接近 1，颜色来自反射而非漫反射。
- `roughness` 越低，高光越集中，越容易暴露环境贴图质量。
- 半透明会引入排序问题，应尽量减少重叠透明表面。

多个模型可以引用同一个材质对象，减少状态切换和内存占用。需要每个实例独立颜色时再创建独立材质。

## 9. 纹理

```qml
PrincipledMaterial {
    baseColorMap: Texture {
        source: "images/albedo.webp"
        generateMipmaps: true
        mipFilter: Texture.Linear
    }
    normalMap: Texture { source: "images/normal.png" }
    roughnessMap: Texture { source: "images/roughness.png" }
}
```

颜色纹理通常使用 sRGB，法线、粗糙度、金属度等数据纹理应按线性数据解释。纹理分辨率应与屏幕占用匹配；给小物体加载 8K 纹理只会增加显存和上传时间。

## 10. 场景环境与抗锯齿

```qml
environment: SceneEnvironment {
    backgroundMode: SceneEnvironment.SkyBox
    lightProbe: Texture { source: "maps/studio.hdr" }
    antialiasingMode: SceneEnvironment.MSAA
    antialiasingQuality: SceneEnvironment.High
    tonemapMode: SceneEnvironment.TonemapModeFilmic
}
```

环境贴图既可作为背景，也可提供基于图像的光照。高动态范围贴图配合色调映射能得到更自然的金属反射。MSAA、阴影和后处理都增加 GPU 成本，需在目标设备实测。

## 11. 属性动画

QML 动画可以直接作用于 3D 属性：

```qml
Model {
    id: cube
    source: "#Cube"

    NumberAnimation on eulerRotation.y {
        from: 0
        to: 360
        duration: 5000
        loops: Animation.Infinite
    }
}
```

多个轴或位置可用 `Vector3dAnimation`：

```qml
Vector3dAnimation {
    target: cube
    property: "position"
    from: Qt.vector3d(-100, 0, 0)
    to: Qt.vector3d(100, 0, 0)
    duration: 800
}
```

持续动画会让渲染循环保持活跃。静态页面应在不可见时暂停动画，降低功耗。

## 12. 初学者常见问题

### 模型太大或太小

统一资产单位，导入时记录缩放。不要在不同节点层级叠加许多不透明的 `scale` 修补问题，否则拾取距离、相机速度和阴影偏差都难以调试。

### 模型全黑

检查光源、法线、材质粗糙度和环境探针。使用 `PrincipledMaterial` 时，没有直射光和环境光的表面可能接近全黑。

### 透明物体显示顺序错误

透明物体通常按对象排序，交叉表面很难完全正确。可以拆分网格、减少交叉透明面，或用抖动/遮罩材质替代连续透明。

下一篇将深入拾取、输入交互、实例化、粒子、骨骼动画、运行时资源加载以及性能分析和部署。
