# QQuick3D
> Qt 6.11.1 · Qt Quick 3D · 来自 `QQuick3D`

## 1. 先建立直觉

`QQuick3D` 是 Qt Quick 3D 的小型工具类，目前最常用的入口是取得适合 Quick 3D 的 `QSurfaceFormat`。它不是场景对象，也不表示 View3D、模型或材质。

## 2. 类说明

保留类说明：这些 API 来自 `QQuick3D`，属于 Qt Quick 3D 模块，用于提供 Quick 3D 运行环境相关的辅助能力。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `idealSurfaceFormat(samples = -1)` | 返回适合 Quick 3D 渲染的 surface format，可在创建窗口前设置默认格式。 |

## 4. 典型流程

```cpp
QSurfaceFormat::setDefaultFormat(QQuick3D::idealSurfaceFormat(4));
QGuiApplication app(argc, argv);
```

## 5. 使用场景

| 场景 | 说明 |
| --- | --- |
| 需要 MSAA/深度缓冲等默认格式 | 在 application 创建窗口前设置。 |
| 混用 Quick 2D/3D/OpenGL 或 RHI 后端 | 统一 surface format，减少平台差异。 |

## 6. 常见坑与经验

默认 surface format 要尽早设置，窗口或渲染上下文创建后再改通常已经太晚。

`samples` 不是“画质越高越好”的旋钮。移动端和嵌入式设备上过高 MSAA 会明显增加显存和带宽压力。

## 7. 知识点覆盖

- Quick 3D 渲染 surface format。
- 抗锯齿采样数和窗口创建时机。
- Quick 3D 初始化前置配置。
