# QSSGCameraHelpers
> Qt 6.11.1 · Qt Quick 3D · 来自 `QSSGCameraHelpers`

## 1. 先建立直觉

`QSSGCameraHelpers` 是相机相关的静态辅助函数集合。它帮助渲染扩展根据 camera id 取得视图投影矩阵等数据，而不需要直接理解 Quick 3D 内部相机对象布局。

## 2. 类说明

保留类说明：这些 API 来自 `QSSGCameraHelpers`，属于 Qt Quick 3D 模块，用于查询 Quick 3D 渲染相机矩阵。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `getViewProjectionMatrix(cameraId, globalTransform)` | 返回相机 view-projection 矩阵，可选传入全局变换。 |

## 4. 使用场景

| 场景 | 说明 |
| --- | --- |
| 自定义渲染扩展 | 需要把世界坐标投影到裁剪空间。 |
| 调试绘制包围盒/辅助线 | 使用相机矩阵计算屏幕位置。 |
| 后处理或屏幕空间效果 | 需要当前相机投影信息。 |

## 5. 常见坑与经验

矩阵的坐标空间要和你的输入数据一致。世界矩阵、模型局部坐标、视图空间混用会导致投影位置错乱。

camera id 必须来自当前有效帧；不要长期缓存后跨场景使用。

## 6. 知识点覆盖

- 相机 view-projection 矩阵。
- 世界/视图/裁剪空间转换。
- 渲染扩展中的相机查询。
