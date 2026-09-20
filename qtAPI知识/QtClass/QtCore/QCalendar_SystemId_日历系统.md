# Qt QCalendar::SystemId 深入笔记

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.2  
> 头文件：`#include <QCalendar>`  
> 所属模块：`Qt6::Core`  
> 核心定位：自定义日历后端的不可解释身份令牌

## 1. 它解决什么问题

`QCalendar::System` 只能选择 Qt 预定义的历法；应用或插件若提供了自定义日历后端，就需要一种方式把“这个已经注册的后端”交给 `QCalendar`。`QCalendar::SystemId` 就是这个方式。

它不是日期、不是历法名称，也不是给应用层自由分配的整数。Qt 文档将它定义为不透明类型：应用不应该理解其中的值，只应把来自后端的 ID 原样交给 `QCalendar` 构造函数。

```text
自定义日历后端
       |
       | calendarId()
       v
QCalendar::SystemId
       |
       | QCalendar(id)
       v
可用于转换和格式化的 QCalendar
```

它解决的典型问题是：自定义后端没有（或暂时不能）按名称注册，但代码仍要明确选择它创建一个 `QCalendar`。

## 2. 它不是用户可构造的“ID 值”

`SystemId` 的公开默认构造函数只会产生无效值。把任意整数转换为它的构造函数是私有的；合法 ID 唯一受支持的来源，是自定义日历后端的 `calendarId()` 方法。

```cpp
QCalendar::SystemId id;
Q_ASSERT(!id.isValid()); // 默认构造的哨兵值
```

因此下面两种做法都不对：

- 把 `index()` 返回的数字存进配置文件，日后再试图恢复同一个日历。
- 自己维护一张“整数到历法”的表，再假设整数可构造为 `SystemId`。

后端注册顺序、插件加载情况、Qt 版本以及应用链接方式都可能影响可用后端。长期保存历法选择时，优先保存稳定的名称，并在启动时通过 `availableCalendars()` 和名称构造做兼容处理；只有后端 API 直接交给你 `SystemId` 时才使用它。

## 3. 最小使用模型

一般应用代码不产生 `SystemId`，而是接收提供自定义日历的库或插件返回的值：

```cpp
#include <QCalendar>

QCalendar makeCalendar(QCalendar::SystemId backendId)
{
    if (!backendId.isValid()) {
        return {};
    }

    QCalendar calendar(backendId);
    if (!calendar.isValid()) {
        return {};
    }

    return calendar;
}
```

两个检查都必要，但含义不同：

1. `backendId.isValid()`：后端有没有成功注册并给出可用 ID。
2. `calendar.isValid()`：`QCalendar` 是否成功用这个 ID 找到有效后端。

后者尤其适合插件边界：调用方拿到 ID 与实际构造 `QCalendar` 之间，后端的可用性可能已经发生变化。

## 4. 与名称和 `System` 的选择关系

| 选择方式 | 适合谁 | 稳定性 | 使用建议 |
| --- | --- | --- | --- |
| `QCalendar::System` | Qt 内建历法 | 枚举语义稳定 | 使用已知内建历法时优先选择。 |
| 名称构造 `QCalendar(name)` | 用户设置、插件公开名称 | 名称可用于配置和显示 | 需要确认后端已注册；留意别名与主名称。 |
| `QCalendar::SystemId` | 自定义后端内部集成 | 仅在当前运行时有意义 | 只原样传递后端给出的值。 |

`SystemId` 的价值不在于“更快地查到名字”，而在于让后端和 `QCalendar` 之间保持一个不依赖公开名称的连接。

## 5. `index()` 为什么不能当业务 ID

Qt 6.11 的头文件公开了 `index()`，它返回底层索引值。这个 API 反映的是实现中的索引，并没有把该数值承诺为跨版本、跨插件加载顺序或跨进程的稳定协议。

可以把它用于受控的诊断日志，例如辅助确认两个当前运行时拿到的令牌是否相同；不要把它用于：

- 数据库字段或 JSON 配置。
- 网络协议。
- 哈希键的长期持久化。
- 根据固定数值分支来选择某个日历。

若要给用户保存选择，保存明确的历法名称，并对“名称不可用”的情况给出回退策略。

## 6. 生命周期与线程边界

`SystemId` 是一个很小的值类型，本身不拥有后端，也没有 `QObject` 生命周期。它的有效性取决于它指向的后端是否成功注册；`SystemId` 并不能延长插件、后端注册表或 `QCalendar` 后端的生命周期。

把它通过值传递没有所有权问题，但跨插件卸载边界长期缓存它没有意义。需要在后端仍有效的范围内尽快构造并使用 `QCalendar`，而不是把 ID 当作永久句柄。

## 7. 常见误区

### 7.1 默认构造后直接传给 `QCalendar`

默认值就是无效哨兵。`QCalendar(id)` 只能在 ID 有效且对应后端可用时产生有效日历。

### 7.2 误以为 `SystemId` 等同于 `QCalendar::System`

`System` 是 Qt 公开的内建枚举；`SystemId` 是自定义后端的运行时令牌。两者不能互换，也不该用数值比较它们。

### 7.3 把它当作“自定义历法的创建 API”

它不负责创建或注册后端。后端实现、注册和 `calendarId()` 的产生属于自定义日历后端的职责；`SystemId` 只负责把已注册后端交给 `QCalendar`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `constexpr SystemId()` | 创建默认的无效 ID。 | 适合作为空值或失败结果；不能据此构造有效自定义日历。 |
| 状态 | `constexpr bool isValid() const noexcept` | 判断 ID 是否表示成功注册的后端。 | 合法值只应来自后端的 `calendarId()`；为真后仍建议检查 `QCalendar(id).isValid()`。 |
| 调试索引 | `constexpr size_t index() const noexcept` | 返回该 ID 的底层索引值。 | 属于运行时实现细节；不要持久化、传输或以固定数值写业务分支。 |
| 消费位置 | `QCalendar::QCalendar(QCalendar::SystemId id)` | 用 ID 选择并构造相应的自定义日历。 | 这是 `SystemId` 唯一受支持的消费者；Qt 6.2 起提供。 |

---

### 一句话总结

`QCalendar::SystemId` 是自定义日历后端交给 `QCalendar` 的不透明令牌：只检查、传递和短期使用，不自行制造、不解释、更不持久化其数值。
