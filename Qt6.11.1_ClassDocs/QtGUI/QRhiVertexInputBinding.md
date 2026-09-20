# QRhiVertexInputBinding
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiVertexInputBinding`

## 1. 先建立直觉

`QRhiVertexInputBinding` 描述一个顶点 buffer 槽位怎样被读取：每条记录的 `stride` 是多少，是每个顶点推进一次，还是每个实例推进一次。它回答的是“buffer 这一行怎么走”，而不是“行里的字段是什么”。

字段位置由 `QRhiVertexInputAttribute` 描述；两者组合成 `QRhiVertexInputLayout`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型，可比较、可哈希
- 归属：RHI 私有接口，来自 `QRhiVertexInputBinding`

一个 graphics pipeline 可以有多个 binding，例如 binding 0 放 per-vertex mesh 数据，binding 1 放 per-instance transform 数据。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建默认 binding，通常随后设置 stride |
| `QRhiVertexInputBinding(stride, classification, stepRate)` | 一次性描述 stride、推进方式和步率 |
| `stride()` / `setStride()` | 每条顶点或实例记录的字节宽度 |
| `classification()` / `setClassification()` | `PerVertex` 或 `PerInstance` |
| `instanceStepRate()` / `setInstanceStepRate()` | 每多少个实例推进到下一条记录 |
| `operator==` / `operator!=` / `qHash()` | 用于布局比较和 pipeline 缓存 |

## 4. Classification 速查

| 枚举 | 含义 | 常见用途 |
| --- | --- | --- |
| `PerVertex` | 每处理一个顶点读取下一条记录 | mesh 顶点、线条顶点、sprite 顶点 |
| `PerInstance` | 每处理一个实例读取下一条记录 | 实例矩阵、实例颜色、每实例参数 |

`instanceStepRate` 让 per-instance 数据不是每个实例都推进。它依赖后端能力，设计跨平台渲染器时应先检查相关 feature，或保持默认的 1。

## 5. 关键用法

单 buffer 顶点布局：

```cpp
QRhiVertexInputBinding vertexBinding(sizeof(Vertex));
```

mesh 数据和实例数据分离：

```cpp
inputLayout.setBindings({
    QRhiVertexInputBinding(sizeof(Vertex), QRhiVertexInputBinding::PerVertex),
    QRhiVertexInputBinding(sizeof(InstanceData), QRhiVertexInputBinding::PerInstance)
});
```

此时 attribute 通过自己的 `binding` 字段选择读哪个 buffer。`QRhiCommandBuffer::setVertexInput()` 也要在对应槽位绑定 buffer，否则 pipeline 布局和实际命令不匹配。

## 6. 使用场景

- 静态或动态 mesh 顶点读取。
- 实例化绘制，把大量对象的 transform 放在 per-instance buffer。
- 多流顶点数据，position/normal 与 uv/color 分 buffer 以便按需更新。
- 粒子系统，用实例数据表达每个粒子的状态。
- pipeline key 构建，用 binding 列表区分不同 vertex layout。

## 7. 常见坑与经验

- `stride` 必须覆盖该 binding 下最大 attribute offset 加格式大小，且通常应按结构体实际 `sizeof` 填。
- binding 编号是布局内的槽位，不是 `QRhiBuffer` 对象的编号。
- per-instance attribute 的 shader location 看起来和 per-vertex 一样，差别在 binding 的推进方式。
- step rate 不等于 instance count；它表示输入记录推进频率。
- 一个 binding 可以没有 attribute，但通常是配置错误，除非你在构造通用布局时临时占位。

## 8. 知识点覆盖

本页覆盖：vertex buffer slot、stride、per-vertex/per-instance 分类、instance step rate、多流顶点布局、attribute 与 buffer 绑定关系。
