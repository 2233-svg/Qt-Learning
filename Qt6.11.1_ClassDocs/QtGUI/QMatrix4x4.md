# QMatrix4x4

> Qt 6.11.1 · Qt GUI · 来自 `QMatrix4x4`

## 1. 先建立直觉

`QMatrix4x4` 是三维齐次变换矩阵：它可把平移、旋转、缩放、相机视图、透视投影和视口映射放进同一份 4x4 数据。它是 Qt 3D/图形代码里连接模型空间、世界空间、相机空间、裁剪空间和屏幕空间的基础值类型。

矩阵本身不会“知道”你要的是 model、view 还是 projection；这是你的命名和组合约定。最可靠的实践是给每个空间转换单独命名，在边界处组合，并用已知点测试其映射。

## 2. 类说明

- 头文件：`#include <QMatrix4x4>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：float 4x4 值类型；适合 CPU 侧变换、传给 shader uniform 或与 Qt 数学类型互转。
- 默认构造为恒等矩阵；`setToIdentity()` 可重置。
- 对用于旋转/缩放的矩阵，变换顺序和向量语义比元素索引更重要；不要在业务代码里直接手填 16 个数字，除非对矩阵布局非常确定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setToIdentity()` / `isIdentity()` | 重置或判断恒等矩阵 |
| `translate()` | 追加 3D 平移 |
| `scale()` | 追加统一或非统一缩放 |
| `rotate(angle, axis)` / `rotate(quaternion)` | 追加轴角或四元数旋转 |
| `lookAt(eye, center, up)` | 追加/建立观察变换 |
| `perspective(fov, aspect, near, far)` | 设置透视投影 |
| `frustum(left, right, bottom, top, near, far)` | 设置离轴透视视锥 |
| `ortho(...)` | 设置正交投影，适合 2D/UI/工程视图 |
| `viewport(...)` | 添加 NDC 到窗口/深度范围映射 |
| `map(QVector3D/4D)` | 映射点；3D 点会参与齐次除法 |
| `mapVector(vector)` | 映射方向，不应用平移 |
| `mapRect()` | 映射二维矩形的包围框 |
| `inverted(&ok)` / `determinant()` | 求逆与诊断退化矩阵 |
| `normalMatrix()` | 取得正确变换法线的 3x3 矩阵 |
| `isAffine()` | 判断是否没有透视投影 |
| `row()` / `column()` / `operator()(r,c)` | 读取/修改矩阵元素 |
| `data()` / `constData()` / `copyDataTo()` | 访问列主序连续数据，常用于 GPU uniform |
| `transposed()` | 获取转置矩阵，适配不同数学/图形 API |
| `optimize()` | 在手工填值后让 Qt 重新识别矩阵特征 |
| `toTransform()` | 转为二维 `QTransform`，可指定投影平面距离 |
| `toGenericMatrix()` / 构造 `QGenericMatrix` | 与编译期维度矩阵互转 |

## 4. 关键用法

### 明确构建 model、view、projection

```cpp
QMatrix4x4 model;
model.translate(position);
model.rotate(orientation);
model.scale(scale);

QMatrix4x4 view;
view.lookAt(cameraEye, cameraTarget, QVector3D(0, 1, 0));

QMatrix4x4 projection;
projection.perspective(55.0f, aspectRatio, 0.1f, 1000.0f);

const QMatrix4x4 mvp = projection * view * model;
```

命名把空间关系写在代码表面，远比“一个 matrix 连续改 20 次”更可维护。改变乘法顺序会改变对象先后经过的空间；不要为了“看上去顺手”随意调换 `projection * view * model`。

### 分清点与方向

```cpp
const QVector3D worldPoint = model.map(localPoint);
const QVector3D worldNormalDirection = model.mapVector(localDirection);
```

点应受到平移影响，方向不应受到平移影响。`mapVector()` 专门表达 `w=0` 的方向变换；若用 `map()` 处理法线/切线，会把 position 误加到方向上。

### 用 normalMatrix 变换法线

```cpp
const QMatrix3x3 normal = modelView.normalMatrix();
const QVector3D n = (normal * localNormal).normalized();
```

非均匀缩放时，直接拿 model-view 左上角 3x3 乘法线会失去垂直关系。`normalMatrix()` 计算逆转置的正确 3x3 形式；若矩阵不可逆，要设计退化处理并避免生成零缩放模型。

### 传给 GPU 前确认内存布局

```cpp
program.setUniformValue("u_mvp", mvp);

// 对需要原始 float 指针的 API：
const float *columnMajor = mvp.constData();
```

`data()` / `constData()` 是列主序，符合常见 OpenGL uniform 约定。不要按 row-major 假设把其传给第三方 API；若目标 API 期待行主序，传 `transposed()` 或按其文档转换。

### 屏幕点反投影

```cpp
bool ok = false;
const QMatrix4x4 inv = mvp.inverted(&ok);
if (!ok)
    return;

const QVector4D clip(xNdc, yNdc, zNdc, 1.0f);
const QVector4D localH = inv * clip;
const QVector3D local = localH.toVector3DAffine();
```

逆投影要处理齐次坐标与 `w` 除法，不能只把二维鼠标位置丢进 `map(QVector3D)` 就期待得到射线。实际拾取通常要用 near/far 两个深度点反投影，得到一条世界空间射线。

## 5. 投影与视图速查

| API | 适用情况 | 关键约束 |
| --- | --- | --- |
| `perspective()` | 常规 3D 相机 | FOV 通常为垂直角；aspect 为宽/高；near/far 必须有效且 near > 0 |
| `frustum()` | 非对称投影、VR、阴影贴图 | left/right/top/bottom 描述 near plane 边界 |
| `ortho()` | 2D、CAD、UI、等距视图 | 无近大远小的透视效果 |
| `lookAt()` | 相机从 eye 看向 center | up 不能与视线共线 |
| `viewport()` | NDC 映射到窗口/纹理坐标 | 明确深度范围与目标坐标原点 |

## 6. 常见坑与经验

- **近裁剪面不要设为 0。** 透视投影要求 `nearPlane > 0`；太小的 near/far 比也会降低深度精度。
- **`lookAt()` 的 up 不能平行视线。** 接近共线时相机 roll 不稳定；为轨道相机保留稳定的 up 约束。
- **矩阵乘法不交换。** 使用单元测试映射一个原点、一个轴向点和一个已知对象，而不是只看画面“差不多”。
- **`normalMatrix()` 不会替你归一化。** 光照前通常仍要 normalize 法线。
- **手动写元素后调用 `optimize()`。** Qt 可为纯平移/缩放等结构走快速路径；直接改 `data()` 或 `operator()` 后让它重新分类。
- **`mapRect()` 只给外包框。** 用于 UI/2D 时旋转后想要精确角点，映射四个点或使用 `QTransform`/polygon。
- **QMatrix4x4 是 float。** 大世界坐标或长期累计变换会遇到精度问题；采用局部原点、双精度业务坐标或浮动原点策略。

## 7. 知识点覆盖

模型视图投影、齐次坐标、点与方向、法线逆转置、透视/正交投影、相机、视口、矩阵布局、GPU uniform、逆投影、深度精度、浮点大世界问题。
