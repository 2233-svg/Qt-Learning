# QMatrix4x4：三维变换、视图与投影矩阵

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMatrix4x4>`  
> 模块：`Qt6::Gui`  
> 常用协作类型：`QVector3D`、`QVector4D`、`QQuaternion`、`QMatrix3x3`、`QTransform`

`QMatrix4x4` 是一个 4x4 浮点矩阵值类型，用于把三维点、方向和齐次坐标从一个坐标空间变换到另一个坐标空间。它可表达平移、缩放、旋转、正交投影、透视投影与视图变换，是 Qt OpenGL/QRhi 渲染、三维几何计算和带透视的二维效果中的基础数据类型。

## 它解决的问题

一个物体的局部顶点通常不能直接画到屏幕上。典型渲染流程需要依次完成：

1. **Model**：物体局部空间到世界空间，例如把模型移到场景中并旋转。
2. **View**：世界空间到相机空间，例如从相机位置朝目标看。
3. **Projection**：相机空间到裁剪空间，例如透视近大远小。
4. **Viewport**：标准化设备坐标到窗口像素坐标。

`QMatrix4x4` 用矩阵连乘把这些步骤合成。它只描述数学变换，不创建 GPU 资源、不绑定着色器，也不会自行把数据上传给图形 API。

## 起步：构造模型、视图和投影

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(my_renderer PRIVATE Qt6::Gui)
```

```cpp
#include <QMatrix4x4>
#include <QVector3D>

QMatrix4x4 model;
model.translate(0.0f, 0.0f, -3.0f);
model.rotate(35.0f, 0.0f, 1.0f, 0.0f);
model.scale(1.2f);

QMatrix4x4 view;
view.lookAt(QVector3D(3.0f, 2.0f, 5.0f),
            QVector3D(0.0f, 0.0f, 0.0f),
            QVector3D(0.0f, 1.0f, 0.0f));

QMatrix4x4 projection;
projection.perspective(45.0f, 16.0f / 9.0f, 0.1f, 100.0f);

const QMatrix4x4 mvp = projection * view * model;
```

默认构造得到单位矩阵，因此可以直接累积变换。对列向量的常规使用方式，`mvp.map(point)` 等价于把 `model`、`view`、`projection` 按从右到左的数学顺序应用于点。

## 最容易出错的地方：调用顺序与实际作用顺序

`translate()`、`scale()`、`rotate()`、`perspective()`、`lookAt()` 等成员函数都会把新的变换乘到当前矩阵上。矩阵乘法不满足交换律，代码的调用顺序不等于点实际经历的变换顺序。

```cpp
QMatrix4x4 transform;
transform.translate(10.0f, 0.0f, 0.0f);
transform.rotate(90.0f, 0.0f, 0.0f, 1.0f);

const QVector3D result = transform.map(QVector3D(1.0f, 0.0f, 0.0f));
```

这会构成 `T * R`；点先旋转，再平移。若目标是“先平移物体，再绕世界原点旋转”，应改变组合顺序，或显式拆分矩阵后按所需顺序相乘。

调试矩阵时不要仅凭代码行序猜结果。写出目标公式，例如 `projection * view * model * position`，再令构造过程与公式一致，能省掉许多“旋转中心不对”的排查时间。

## 行主序接口与列主序原始内存

`QMatrix4x4` 有一个刻意容易混淆的约定：

- 16 个标量构造函数、`QMatrix4x4(const float *)`、`operator()(row, column)` 和 `copyDataTo()` 按**行主序**理解或输出数据。
- `data()` 与 `constData()` 返回用于图形 API 的**列主序**连续内存。

```cpp
const float rowMajor[16] = {
    1, 0, 0, 10,
    0, 1, 0, 20,
    0, 0, 1, 30,
    0, 0, 0, 1
};

QMatrix4x4 matrix(rowMajor);        // 输入按行主序
const float *forGpu = matrix.constData(); // 输出按列主序
```

向 OpenGL 风格 uniform 上传时，`constData()` 正是通常需要的内存布局。相反，若将 `constData()` 的指针直接喂给期待行主序的第三方格式，结果会相当于转置，常见症状是平移出现在错误的行/列。

`operator()(row, column)` 的索引范围都是 `0..3`。它可读写元素，但直接写入会让类失去对“当前是单位/平移/缩放矩阵”等优化类别的跟踪；写完后可调用 `optimize()` 让 Qt 重新识别可优化类型。

## 点、方向、法线：不要使用同一种映射

`QVector3D` 既可能表示空间中的点，也可能表示方向。两者对平移的处理不同：

```cpp
QMatrix4x4 matrix;
matrix.translate(5.0f, 0.0f, 0.0f);
matrix.rotate(90.0f, 0.0f, 0.0f, 1.0f);

const QVector3D point = matrix.map(QVector3D(1.0f, 0.0f, 0.0f));
const QVector3D direction = matrix.mapVector(QVector3D(1.0f, 0.0f, 0.0f));
```

| 输入含义 | 应用 API | 齐次坐标语义 |
| --- | --- | --- |
| 位置、顶点、物体中心 | `map(QVector3D)` | 按 `w = 1` 处理，所以会受到平移；有投影时会进行透视除法。 |
| 速度、朝向、切线 | `mapVector(QVector3D)` | 只应用左上 3x3，忽略平移与投影。 |
| 需要保留 `w` 的裁剪坐标 | `map(QVector4D)` 或矩阵乘法 | 不自动把结果压回三维，适合着色器和裁剪空间计算。 |
| 表面法线 | `normalMatrix()` 产生的 `QMatrix3x3` | 非均匀缩放时不能直接套用模型矩阵的 3x3 部分。 |

`mapRect()` 会映射矩形的角点后返回一个轴对齐包围矩形。经过旋转、透视后，它不会保留“旋转后的四边形”形状；若需要真实四个顶点，逐点 `map()`。

## 视图、投影与坐标系边界

### 相机视图

```cpp
QMatrix4x4 view;
view.lookAt(eye, center, up);
```

`lookAt()` 用相机位置 `eye`、注视目标 `center` 和向上方向 `up` 右乘一个视图矩阵。`up` 不能与 `eye -> center` 的视线平行，否则无法确定稳定的相机横轴。

### 正交与透视

| API | 用途 | 参数边界 |
| --- | --- | --- |
| `ortho()` | 平行投影，不产生近大远小。 | 用于 UI、CAD、二维叠加层或正交世界。 |
| `frustum()` | 以近平面四边界显式定义非对称透视体。 | 适合偏轴投影、立体渲染和自定义投影。 |
| `perspective()` | 以垂直视场角和宽高比构造常规透视。 | 视场角用度；宽高比应是 `width / height`；近平面与远平面应构成有效裁剪范围。 |
| `viewport()` | 把 `[-1, 1]` 的 NDC 区间映射到窗口区域。 | 行为对应 OpenGL 风格 viewport，原点和 Y 方向须与实际渲染后端一致。 |

投影矩阵、视图矩阵和模型矩阵最好分开维护。将它们反复累积进同一个对象，窗口 resize 后很容易重复叠加 `perspective()`，造成画面越来越畸变。

## 逆矩阵、法线矩阵与可逆性

逆矩阵常用于从屏幕射线回推世界坐标、撤销变换或计算局部坐标：

```cpp
bool ok = false;
const QMatrix4x4 inverse = model.inverted(&ok);
if (!ok) {
    // 例如某个维度缩放为 0，模型矩阵不可逆。
}
```

`inverted()` 在不可逆时返回单位矩阵，因此不能只检查返回值是否“看起来合理”，需要传入 `bool *invertible`。接近奇异的浮点矩阵也可能数值不稳定；需要鲁棒几何算法时，应额外限制极小缩放与病态投影参数。

`normalMatrix()` 返回左上 3x3 的逆转置。均匀缩放或纯旋转时直接变换法线有时看不出问题；一旦有非均匀缩放，必须使用法线矩阵，否则光照方向会明显错误。其 3x3 子矩阵不可逆时，Qt 返回单位矩阵。

## 值语义、性能与线程

`QMatrix4x4` 是包含 16 个 `float` 的普通值类型，不拥有 `QObject`、窗口或 GPU 资源。可按值返回、放入容器或跨线程传递副本。

- 同一可变实例不能被多线程无同步地读写。
- 建模、数学计算和数据准备可在工作线程进行；把矩阵上传到图形上下文或用于 GUI 绘制时，仍要遵守该上下文/GUI 的线程归属。
- 连续调用 `translate()`、`scale()`、`rotate()` 时，Qt 会跟踪常见矩阵类别以走更快路径。
- 使用 `data()`、`operator()`、`setRow()` 或 `setColumn()` 直接修改后，如后续要频繁变换，调用一次 `optimize()`。

## 常见错误

1. **把 `data()` 当行主序。** 它是列主序；需要行主序副本时使用 `copyDataTo()`。
2. **把点和方向都用 `map()`。** 方向应使用 `mapVector()`，否则平移会污染方向。
3. **忽略透视除法。** `map(QVector3D)` 假设 `w = 1` 并可能除以结果 `w`；需要原始裁剪坐标时用 `QVector4D`。
4. **重复累积投影。** resize 时应重新从单位矩阵构建 projection。
5. **直接修改矩阵后不调用 `optimize()`。** 结果正确但可能失去快路径。
6. **对不可逆矩阵直接使用 `inverted()` 返回值。** 必须检查 `invertible`。
7. **用模型矩阵直接变换非均匀缩放下的法线。** 使用 `normalMatrix()`。
8. **把 `mapRect()` 当透视后的真实四边形。** 它返回的是轴对齐包围矩形。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `QMatrix4x4()` | 构造单位矩阵。 | 最常用起点；随后累积 model、view 或 projection 变换。 |
| `QMatrix4x4(Qt::Initialization)` | 构造未初始化矩阵。 | 仅在立刻写满全部 16 个元素时使用；读取任何未写元素会产生未定义结果。 |
| `QMatrix4x4(const float *values)` | 从 16 个浮点数构造。 | 输入按行主序；若内容是常见特殊变换且后续高频修改，可调用 `optimize()`。 |
| `QMatrix4x4(float m11, ..., float m44)` | 从 16 个显式元素构造。 | 参数按行主序，适合审查固定矩阵；不要与 `constData()` 的列主序混淆。 |
| `QMatrix4x4(const float *values, int cols, int rows)` | 从给定行列规模的数组构造 4x4。 | 属于较少使用的兼容入口；调用前确认输入维度与布局，常规代码优先完整 16 元素构造。 |
| `QMatrix4x4(const QGenericMatrix<N, M, float> &)` / `toGenericMatrix<N, M>()` | 与通用矩阵模板互转。 | 用于固定维度泛型算法；转换维度应与目标算法的语义一致。 |
| `QMatrix4x4(const QTransform &)` / `toTransform()` | 在 2D `QTransform` 与 4x4 间转换。 | 适合二维变换桥接；包含透视时，使用带 `distanceToPlane` 的 `toTransform(float)` 明确投影距离。 |
| `operator()(row, column)` | 读取或写入单元格。 | 索引均为 `0..3`，按行列访问；直接写后调用 `optimize()` 可恢复快路径识别。 |
| `row()` / `column()` | 读取指定行或列为 `QVector4D`。 | 索引范围 `0..3`；用于检查数学布局，不等同于原始内存线性顺序。 |
| `setRow()` / `setColumn()` | 设置指定行或列。 | 会改变矩阵；避免拿它们替代明确的高层变换 API。 |
| `isIdentity()` / `setToIdentity()` | 判断或恢复单位矩阵。 | 每次重建投影、视图或 model 时优先 `setToIdentity()`，避免无意累积旧变换。 |
| `isAffine()` | 判断是否没有投影项。 | 仿射矩阵不含 projective 系数；用于决定是否可安全按二维/仿射路径处理。 |
| `fill(float)` | 用同一数值填满 16 个元素。 | 不等于清零后恢复单位矩阵；需要单位矩阵请用 `setToIdentity()`。 |
| `determinant()` | 返回行列式。 | 可辅助判断退化，但浮点接近零时不应用精确 `== 0` 作为唯一鲁棒策略。 |
| `inverted(bool *invertible)` | 返回逆矩阵。 | 不可逆时返回单位矩阵；传 `invertible` 并检查结果。 |
| `transposed()` | 返回转置矩阵。 | 用于特定线性代数或布局转换；不是“把列主序变行主序”的常规上传方法。 |
| `normalMatrix()` | 返回左上 3x3 的逆转置。 | 用于变换法线；3x3 不可逆时返回单位矩阵。 |
| `translate(...)` | 右乘平移变换。 | 有 `QVector3D`、二维和三维重载；实际应用顺序受矩阵连乘规则影响。 |
| `scale(...)` | 右乘缩放变换。 | 有向量、统一缩放、二维和三维重载；缩放为 0 会使矩阵不可逆。 |
| `rotate(...)` | 右乘旋转变换。 | 支持轴角、`QVector3D` 与 `QQuaternion`；轴必须有合理非零长度。 |
| `lookAt(eye, center, up)` | 右乘相机视图矩阵。 | `up` 不能与视线平行；将 view 与 model/projection 分开保存。 |
| `ortho(...)` | 右乘正交投影。 | 可传边界或 `QRect`/`QRectF`；适合平行投影。 |
| `frustum(...)` | 右乘非对称透视投影。 | 参数描述近平面窗口及近远裁剪面；适合偏轴投影。 |
| `perspective(fov, aspect, near, far)` | 右乘常规透视投影。 | `fov` 为垂直角度；`aspect = width / height`；确保裁剪参数有效。 |
| `viewport(...)` | 右乘 NDC 到窗口的映射。 | 遵循 OpenGL 风格的下边界与深度范围约定；检查渲染后端的 Y 轴方向。 |
| `flipCoordinates()` | 翻转二维坐标约定。 | 较少使用的便利变换；需要可审计的坐标变换时，显式使用缩放/平移更清楚。 |
| `projectedRotate(...)` | 添加投影式旋转。 | Qt 7 前的兼容入口；新代码优先组合明确的投影与旋转矩阵。 |
| `map(QPoint/QPointF)` | 映射二维位置。 | 适合 2D 几何；投影/旋转后的精度与包围范围要单独考虑。 |
| `map(QVector3D)` | 映射三维点。 | 按 `w = 1` 处理，受平移影响，并会在需要时透视除法。 |
| `mapVector(QVector3D)` | 映射三维方向。 | 忽略平移和投影；用于方向、切线和速度。 |
| `map(QVector4D)` | 映射齐次四维向量。 | 保留 `w`，适合裁剪空间与手动透视处理。 |
| `mapRect(QRect/QRectF)` | 映射矩形并返回轴对齐包围矩形。 | 旋转或透视后不保留真实四边形；需要顶点时逐点映射。 |
| `data()` / `constData()` | 取得列主序原始内存。 | 适合图形 API；可写 `data()` 会使内部优化类别退化。 |
| `copyDataTo(float *)` | 复制出 16 个行主序元素。 | 目标必须容纳 16 个 `float`；适合 C 风格行主序接口。 |
| `optimize()` | 根据当前元素重新识别优化类别。 | 直接改元素或从原始数据构造后，若后续大量变换，可调用一次。 |
| `operator+=` / `-=` / `*=` / `/=` | 原地矩阵或标量运算。 | `*=(matrix)` 是矩阵乘法；除以 0 会产生无效浮点结果。 |
| `operator+` / `-` / 一元 `-` / `operator*` / `operator/` | 返回新的矩阵或向量运算结果。 | 明确左右乘顺序；Qt 6.1 起优先 `map()`，避免已弃用的某些“矩阵在左”的点/三维向量乘法形式。 |
| `operator==` / `!=` | 精确比较元素。 | 浮点计算结果比较通常改用 `qFuzzyCompare()`。 |
| `qFuzzyCompare(m1, m2)` | 近似比较两个矩阵。 | 适合浮点容差判断；容差规则不是业务几何误差模型的替代品。 |
| `operator QVariant()` | 转为 `QVariant`。 | 用于 Qt 属性、模型或通用容器；接收方需知道实际类型。 |
| `QDataStream <<` / `>>` | 二进制写入或读取矩阵。 | 用于 Qt 流序列化；两端应协商数据流版本，不是人可编辑格式。 |
| `QDebug <<` | 输出调试表示。 | 在启用 Qt 调试流时可用，适合日志检查矩阵元素。 |

## 一句话总结

`QMatrix4x4` 的难点不在 API 数量，而在约定：高层访问按行理解、GPU 原始内存按列输出；点用 `map()`、方向用 `mapVector()`；组合时先写清 `projection * view * model` 再落实调用顺序。
