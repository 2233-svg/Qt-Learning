# QPointingDeviceUniqueId

> Qt 6.11.1 · Qt GUI · 来自 `QPointingDeviceUniqueId`

## 1. 先建立直觉

`QPointingDeviceUniqueId` 是一个轻量值类型，用来表示指针设备或工具端提供的唯一标识。例如同一台绘图板上的不同笔、同一支笔的不同工具信息，平台可能用这个 ID 协助区分。

它的主要价值是比较和作为哈希键，而不是拿 `numericId()` 做跨平台业务协议。Qt 明确把数值 ID 视为平台相关实现细节；在可移植代码中，优先使用 `==`、`!=` 和 `qHash()`。

## 2. 类说明

`QPointingDeviceUniqueId` 不继承 `QObject`，是可复制的值类型。常从 `QPointingDevice::uniqueId()` 或 `QEventPoint::uniqueId()` 取得。

类说明只用于表明这些 API 来自 `QPointingDeviceUniqueId`：它负责标识与比较，不保存设备名称、能力、生命周期或输入状态；这些信息应从 `QPointingDevice` 和事件对象读取。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QPointingDeviceUniqueId()` | 构造无效的唯一 ID。 |
| `fromNumericId(id)` | 从平台给出的数值创建唯一 ID 包装对象。 |
| `isValid() const` | 判断 ID 是否代表实际有效的指针或工具标识。 |
| `numericId() const` | 返回底层数值 ID；无效时通常为 `-1`，不建议作为可移植持久值。 |
| `operator==` / `operator!=` | 比较两个 ID 是否表示同一指针或工具。 |
| `qHash(id, seed)` | 让 ID 可作为 `QHash` / `QSet` 的键。 |

## 4. 关键用法

### 用相等比较识别同一工具

```cpp
void ToolRegistry::remember(const QPointingDevice *device)
{
    const auto id = device->uniqueId();
    if (id.isValid())
        m_lastToolById.insert(id, currentToolSettings());
}
```

之后再次遇到 ID 时可以恢复相应笔刷设置：

```cpp
const auto id = event->uniqueId();
if (m_lastToolById.contains(id))
    applyToolSettings(m_lastToolById.value(id));
```

这种写法让比较语义集中在类型本身，不需要业务代码理解数值 ID 的具体来源。

### 无效 ID 必须有降级路径

```cpp
const auto id = event->uniqueId();
if (!id.isValid()) {
    applyDefaultToolSettings();
    return;
}
```

不少平台不会提供有效工具 ID。应用仍应能正常处理压力、位置和 pointer type，不能因为 ID 缺失就拒绝输入。

## 5. 使用场景

`QPointingDeviceUniqueId` 适合专业绘图软件保存不同笔工具的临时偏好、手写输入系统区分硬件工具、诊断日志关联同一输入来源、`QHash` 缓存按工具区分的状态。

它也可用于测试或模拟输入：通过 `fromNumericId()` 创建可比较的标识，让测试事件能够模拟不同工具来源。

普通鼠标点击、简单触摸按钮和不关心具体硬件工具的界面，通常没有必要直接使用它。

## 6. 常见坑与经验

不要把 `numericId()` 写进文件格式、网络协议或数据库主键。它不保证跨平台、跨驱动、跨重连仍然稳定。

不要跳过 `isValid()`。无效 ID 与一个真实值不同，不能把 `-1` 当作普通设备编号参与业务分支。

不要把它当成触点 ID。`QEventPoint::id()` 用于一段触摸交互内部跟踪不同点；`QPointingDeviceUniqueId` 用于标识设备或工具来源，两者生命周期和语义不同。

不要用 ID 替代 pointer type。笔尖和橡皮擦的功能差异仍应主要通过 `pointerType()` 判断。

## 7. 知识点覆盖

学习 `QPointingDeviceUniqueId` 应覆盖值类型、有效性、相等比较、哈希容器、平台相关数值 ID、设备/工具标识、触点 ID 区别、专业输入设备降级策略。
