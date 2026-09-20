# Qt QScopedPropertyUpdateGroup：属性批量更新的 RAII 作用域

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScopedPropertyUpdateGroup>`  
> 所属模块：`Qt6::Core`  
> 自 Qt：6.6  
> 类型性质：不可复制、不可移动的作用域守卫

## 1. 它解决什么问题

`QScopedPropertyUpdateGroup` 把一段属性修改包成一个更新组。构造时调用 `Qt::beginPropertyUpdateGroup()`，析构时调用 `Qt::endPropertyUpdateGroup()`，从而保证即使提前 `return` 或抛出异常，也能结束更新组。

```cpp
{
    QScopedPropertyUpdateGroup group;
    width = 640;
    height = 480;
}
```

组内修改不会立刻重新计算依赖属性，也不会立即触发变化通知；这些动作延迟到最外层更新组结束时统一处理。

它适合：

- 同时修改多个相互关联的 `QProperty`；
- 在一组字段更新完毕前保持类不变量；
- 避免观察者看到“宽已变、高未变”的中间状态；
- 用 RAII 处理异常和提前返回路径。

## 2. 为什么需要更新组

假设总面积绑定为：

```cpp
QProperty<int> width(10);
QProperty<int> height(20);
QProperty<int> area([&] { return width.value() * height.value(); });
```

如果分别写入 `width` 和 `height`，外部观察者可能先看到一次中间的 `area`，再看到最终值。更新组把它们当成一个同步提交：

```cpp
{
    QScopedPropertyUpdateGroup group;
    width = 100;
    height = 50;
} // 此处才进行延迟的绑定求值和通知
```

通知发生时，组内涉及的属性都已经是新值，观察者更容易维护类不变量。

## 3. 嵌套规则

更新组可以嵌套：

```cpp
{
    QScopedPropertyUpdateGroup outer;
    first = 1;
    {
        QScopedPropertyUpdateGroup inner;
        second = 2;
    } // 仍处于 outer 中，不会最终刷新
    third = 3;
} // 最外层结束，统一求值和通知
```

只有最外层组结束时，延迟的绑定求值和通知才会真正发生。内层作用域结束只减少嵌套深度。

## 4. 与手动 API 的关系

RAII 类对应：

```cpp
Qt::beginPropertyUpdateGroup();
// 修改属性
Qt::endPropertyUpdateGroup();
```

手动版本必须严格配对。Qt 文档明确指出，没有先调用 `beginPropertyUpdateGroup()` 就调用 `endPropertyUpdateGroup()` 是未定义行为。

通常用 `QScopedPropertyUpdateGroup`，因为它能覆盖早退和常规异常路径；只有需要精确控制 `endPropertyUpdateGroup()` 的异常处理时，才考虑手动调用。

## 5. 异常安全边界

`endPropertyUpdateGroup()` 在最外层组结束时会触发延迟绑定求值和通知。绑定求值可能抛出异常，因此 `QScopedPropertyUpdateGroup` 的析构函数标记为 `noexcept(false)`。

危险情况是：外层代码已经因为另一个异常开始栈展开，守卫析构时又从绑定求值抛出异常。C++ 在同一时间处理两个未捕获异常时会调用 `std::terminate()`。

如果绑定求值可能抛异常，并且你需要捕获它，应使用手动 API：

```cpp
Qt::beginPropertyUpdateGroup();
try {
    width = 640;
    height = 480;
    Qt::endPropertyUpdateGroup();
} catch (...) {
    // 根据业务记录、回滚或转换错误
    throw;
}
```

这里要特别注意：若 `endPropertyUpdateGroup()` 自身抛出，更新组已经进入结束流程，不能简单地再次无条件调用 `endPropertyUpdateGroup()`。

## 6. 它不是什么

`QScopedPropertyUpdateGroup`：

- 不提供事务回滚；
- 不复制旧值；
- 不保证绑定求值只执行一次；
- 不把通知转换成 queued event；
- 不提供线程同步；
- 不会合并不相关的业务副作用。

它只控制属性系统的“延迟求值与通知”边界。若中途写入失败，已写入的普通值不会自动恢复。

## 7. 真实使用场景

### 7.1 恢复多字段类不变量

```cpp
class RectangleState
{
public:
    void setSize(int w, int h)
    {
        QScopedPropertyUpdateGroup group;
        m_width = w;
        m_height = h;
    }

    QProperty<int> area{[this] {
        return m_width.value() * m_height.value();
    }};

private:
    QProperty<int> m_width{1};
    QProperty<int> m_height{1};
};
```

### 7.2 批量加载配置

```cpp
void SettingsModel::load(const Settings &settings)
{
    QScopedPropertyUpdateGroup group;
    m_theme = settings.theme;
    m_fontSize = settings.fontSize;
    m_scale = settings.scale;
}
```

界面依赖可以等全部配置字段到位后再重新计算。

## 8. 常见错误

### 8.1 误以为有回滚

离开作用域只会结束延迟通知，不会把已写入的属性恢复为旧值。需要回滚时必须自行保存旧值并实现异常策略。

### 8.2 把组跨越事件循环或阻塞等待

更新组应该是短小同步作用域。跨越事件循环、等待其他线程或调用复杂外部代码，会让依赖观察者长时间看不到更新，也会扩大重入风险。

### 8.3 在组内依赖外部观察者立即响应

组内通知被延迟。如果业务逻辑必须依赖某个绑定已经更新，应该先结束当前组，再执行后续逻辑。

### 8.4 析构期间抛异常

如果已有异常正在栈展开，守卫析构再触发绑定异常可能导致 `std::terminate()`。有异常绑定场景时采用手动 begin/end 并显式捕获。

### 8.5 跨线程当作锁使用

更新组不是互斥机制。它只影响当前属性系统的更新批次，不能保护跨线程共享内存。

## 9. 逐项 API 语义

| API | 语义 | 边界 |
| --- | --- | --- |
| `QScopedPropertyUpdateGroup()` | 开始一个属性更新组。 | 组可嵌套；构造后应在同一控制流中正常析构。 |
| `~QScopedPropertyUpdateGroup()` | 结束当前更新组。若是最外层，则执行延迟绑定求值和通知。 | 可能抛绑定求值异常；栈展开期间要特别谨慎。 |
| `Qt::beginPropertyUpdateGroup()` | 手动开始更新组。 | 自 Qt 6.2；必须与 end 配对。 |
| `Qt::endPropertyUpdateGroup()` | 手动结束更新组并在最外层触发刷新。 | 未配对调用是未定义行为。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| RAII | `QScopedPropertyUpdateGroup group;` | 进入作用域时延迟属性更新。 | 不可复制、不可移动。 |
| 结束 | `~QScopedPropertyUpdateGroup()` | 离开作用域时恢复更新和通知。 | 可能触发绑定求值与异常。 |
| 手动开始 | `Qt::beginPropertyUpdateGroup()` | 开始手动更新组。 | 必须配对 end。 |
| 手动结束 | `Qt::endPropertyUpdateGroup()` | 结束手动更新组。 | 最外层结束时才真正刷新；未配对是未定义行为。 |

---

### 一句话总结

`QScopedPropertyUpdateGroup` 是属性系统的批量提交守卫：组内延迟依赖更新，最外层结束时统一求值通知，但它没有回滚能力，析构也可能触发绑定异常。
