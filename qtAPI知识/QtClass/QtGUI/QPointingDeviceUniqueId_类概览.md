# QPointingDeviceUniqueId：指向设备上的唯一对象标识

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPointingDeviceUniqueId>`  
> 所属模块：`Qt6::Gui`  
> 类型性质：轻量值类型、`Q_GADGET`

`QPointingDeviceUniqueId` 用来标识指向设备上的一个可追踪对象，例如带标签的触控物体、触控笔或其他由设备报告唯一编号的对象。它通常出现在 `QEventPoint` 和触摸/指针事件相关逻辑中，用来判断“这次事件中的对象是否和之前的是同一个”。

它解决的是对象身份跟踪问题，而不是坐标跟踪问题：

- `QEventPoint::position()` 告诉你对象当前在哪里。
- `QEventPoint::state()` 告诉你对象是否按下、移动或释放。
- `QPointingDeviceUniqueId` 用来判断事件序列中的对象身份是否相同。

## 实际使用场景

### 触摸对象跟踪

```cpp
void TouchHandler::handlePoint(const QEventPoint &point)
{
    const QPointingDeviceUniqueId id = point.uniqueId();
    if (!id.isValid())
        return; // 设备没有报告可用的唯一身份

    const auto key = id; // 可作为 QHash/QSet 的键
    m_tracks[key] = point.position();
}
```

真实设备不一定支持唯一对象编号。无效 ID 不是异常，而是“当前设备没有提供这种身份信息”。需要兼容普通多点触摸时，通常结合 `QEventPoint::id()`、事件点生命周期和设备能力使用。

### 判断前后事件是否同一对象

```cpp
if (previousPoint.uniqueId() == currentPoint.uniqueId()) {
    updateExistingTrack(currentPoint);
}
```

Qt 文档建议可移植代码依赖相等运算符，而不要依赖 `numericId()` 的具体数值。未来 Qt 可能扩展 ID 的内部表示，数值只适合诊断或与底层协议对接。

## 关键语义

### 无效值

默认构造会产生无效 ID，内部 numeric ID 为 `-1`。`isValid()` 是判断有效性的正式 API：

```cpp
QPointingDeviceUniqueId id;
Q_ASSERT(!id.isValid());

id = QPointingDeviceUniqueId::fromNumericId(42);
Q_ASSERT(id.isValid());
```

不要用 `numericId() == -1` 代替 `isValid()` 作为跨版本业务契约。`numericId` 的 `-1` 是当前 Qt 对“设备不提供数值 ID”的表示，业务身份判断应使用 `==`。

### 值语义和生命周期

这是一个只包含轻量 ID 的值类型，可以按值传递、复制、移动和存储。它不拥有设备、事件或触点资源，也不受对象销毁、事件循环或线程归属影响。

但它只表示一个身份值，不保证该对象当前仍在屏幕上，也不保证两个不同设备报告的数值在全局范围内唯一。需要全局键时，应把设备对象身份和该 ID 一起纳入键。

### 与 `QPointingDevice` 的关系

`QPointingDeviceUniqueId` 标识设备上的对象；`QPointingDevice` 标识产生输入的设备本身。实际跟踪常常需要同时使用：

```text
(QPointingDevice*, QPointingDeviceUniqueId)
```

因为不同设备可能复用相同的 numeric ID。对于同一事件序列，优先使用 Qt 已提供的点 ID、设备信息和 unique ID 的组合，不要只凭一个整数做全局身份。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QPointingDeviceUniqueId>
#include <QEventPoint>
#include <QHash>
```

## API 逐项说明

### 属性

#### `[read-only] qint64 QPointingDeviceUniqueId::numericId`

返回设备报告的数值唯一 ID。如果设备支持 numeric ID，`isValid()` 为 `true`，属性返回对应数值；否则返回 `-1`。

这是只读、常量属性，没有 setter。它适合日志、调试和与底层设备协议对照，不适合用作可移植的身份判断。比较两个对象应使用 `operator==`。

### 构造和生成

#### `constexpr noexcept QPointingDeviceUniqueId::QPointingDeviceUniqueId()`

构造无效的 unique ID。该操作不分配资源，也不会访问设备；新对象的 `isValid()` 为 `false`。

#### `static QPointingDeviceUniqueId QPointingDeviceUniqueId::fromNumericId(qint64 id)`

根据 numeric ID 构造一个 `QPointingDeviceUniqueId`。适合把设备协议中的数值包装成 Qt 类型，或在测试中构造稳定的 ID。

调用者应避免把任意外部整数误当成跨设备全局 ID。`id` 的具体有效范围由设备和协议决定；跨设备使用时仍应附带设备身份。

### 状态查询

#### `constexpr noexcept bool QPointingDeviceUniqueId::isValid() const`

返回该 ID 是否代表一个实际的指向对象。默认构造对象无效；设备不报告 ID 时也可能无效。

不要把无效 ID 当作一个可跟踪对象存入业务状态，除非业务明确需要表示“所有没有硬件 ID 的对象”这一类别。

#### `qint64 QPointingDeviceUniqueId::numericId() const`

返回 numeric ID。设备不支持时返回 `-1`。对于可移植代码，使用 `isValid()` 和相等运算符，不要依赖这个数值的编码规则、连续性或跨设备唯一性。

### 比较和哈希

#### `bool operator==(QPointingDeviceUniqueId lhs, QPointingDeviceUniqueId rhs) noexcept`

判断两个 ID 是否代表同一个指向对象。Qt 当前实现按内部 ID 比较；业务代码应把比较结果作为身份判断依据。

如果要做跨设备跟踪，不能只比较 unique ID，还应把 `QPointingDevice` 身份纳入比较键。

#### `bool operator!=(QPointingDeviceUniqueId lhs, QPointingDeviceUniqueId rhs) noexcept`

判断两个 ID 是否代表不同对象，语义与 `operator==` 相反。两个无效 ID 在当前类型语义下可以相等，但这不表示它们识别了一个真实对象。

#### `size_t qHash(QPointingDeviceUniqueId key, size_t seed = 0) noexcept`

返回适用于 `QHash`、`QSet` 等哈希容器的哈希值。`seed` 用于哈希随机化或组合；不要把哈希值当作稳定的持久化 ID。

```cpp
QHash<QPointingDeviceUniqueId, QPointF> lastPositions;
lastPositions[id] = point.position();
```

容器键若需要支持多个设备，应改为保存设备与 unique ID 的组合，而不是仅保存此类型。

## 常见错误排查

1. **把 `numericId()` 当作永远有效**：设备可能不提供 ID；先调用 `isValid()`。
2. **把 `-1` 写死成业务判断**：使用 `isValid()`，给未来内部表示变化留下空间。
3. **只用 unique ID 区分所有设备的触点**：不同设备可能复用相同编号，组合设备身份。
4. **把 unique ID 当作触点位置**：它只表示身份，位置和生命周期要从 `QEventPoint` 获取。
5. **把无效 ID 当作异常**：普通触摸设备不支持硬件唯一对象 ID 时，无效是正常能力边界。
6. **把哈希值或 numeric ID 持久化**：它们不是跨运行、跨设备或跨协议的持久化标识。
7. **用指针管理它**：这是轻量值类型，按值传递和存储即可。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 属性 | `numericId` | 读取设备报告的数值 ID | 设备不支持时为 `-1`；可移植判断使用 `isValid()` |
| 构造 | `QPointingDeviceUniqueId()` | 构造无效 ID | `constexpr noexcept`；不分配资源 |
| 工厂 | `fromNumericId(qint64)` | 用数值包装成 unique ID | 数值不代表跨设备全局唯一 |
| 状态 | `isValid()` | 判断是否代表真实对象 | 设备未提供 ID 时可能为 false |
| 读取 | `numericId()` | 返回数值 ID | 适合诊断，不要依赖数值编码 |
| 比较 | `operator==` | 判断是否同一对象 | 跨设备跟踪时还要比较设备身份 |
| 比较 | `operator!=` | 判断是否不同对象 | 两个无效 ID 相等不代表真实对象存在 |
| 哈希 | `qHash(key, seed)` | 用于 `QHash`/`QSet` | 哈希值不是持久化 ID |

### 一句话总结

`QPointingDeviceUniqueId` 是指向设备对象的轻量身份值：用 `isValid()` 判断设备是否提供身份，用相等运算符做可移植比较，把设备身份与它组合后再做全局触点跟踪。
