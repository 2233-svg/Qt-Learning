# QAccessibleObject

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleObject`

## 1. 先建立直觉

`QAccessibleObject` 是把一个普通 `QObject` 包装成 `QAccessibleInterface` 的便利基类。它已经处理了关联对象、有效性判断、默认屏幕几何和按位置查找子节点，因此自定义非 QWidget 对象的无障碍实现可以少写一层重复代码。

它提供的是“接口骨架”，不是完整语义。你仍需实现对象的 Role、State、Name、父子关系及需要的专用接口；对 QWidget，则多数情况下应从 `QAccessibleWidget` 派生或使用 Qt 现成映射。

## 2. 类说明

- 头文件：`#include <QAccessibleObject>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleInterface`
- 直接派生：`QAccessibleWidget`
- 构造输入：需要提供无障碍语义的 `QObject *`。

它并不拥有传入的 QObject。底层对象销毁后，此接口应视为无效，不能再继续通过它读取属性、几何或子节点。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleObject(object)` | 建立对象关联。 |
| `object()` | 返回被包装的 QObject。 |
| `isValid()` | 检查关联对象是否仍有效。 |
| `rect()` | 返回对象屏幕几何；不可见或无视觉几何时可能无效。 |
| `childAt(x, y)` | 默认遍历可访问后代，返回命中屏幕坐标的对象。 |
| `setText(type, text)` | 尝试写入可访问文本属性。 |

`role()`、`state()`、`text()`、`parent()`、`childCount()`、`child()` 和 `indexOfChild()` 仍来自抽象基类，需要你的子类按对象真实语义实现。

## 4. 关键用法

```cpp
class AccessibleStatusBadge final : public QAccessibleObject
{
public:
    explicit AccessibleStatusBadge(StatusBadge *badge)
        : QAccessibleObject(badge) {}

    QAccessible::Role role() const override
    {
        return QAccessible::StaticText;
    }

    QAccessible::State state() const override
    {
        QAccessible::State result;
        result.invisible = !badge()->isVisible();
        return result;
    }

    QString text(QAccessible::Text type) const override
    {
        return type == QAccessible::Name ? badge()->statusText() : QString();
    }

    // 根据对象结构实现 parent/childCount/child/indexOfChild。
};
```

`rect()` 和 `childAt()` 使用全局屏幕坐标。若 `StatusBadge` 不是可视 QObject、位于视口内容中或绘制多个虚拟元素，通常需要重写几何和命中逻辑，不能只依赖默认实现。

## 5. 使用场景

| 场景 | 选择 |
|---|---|
| 现成 Qt 控件 | 优先让 Qt 提供接口，不要自行包装。 |
| 自定义 QWidget | 优先考虑 `QAccessibleWidget`，因为它理解 QWidget 几何和窗口关系。 |
| 非 QWidget 的可视 QObject | 使用 `QAccessibleObject` 作为接口基类。 |
| 单一画布上绘制许多逻辑元素 | 用它承载根节点，并为虚拟子项提供专用接口/几何。 |
| 无视图、无用户交互的 QObject | 通常不应暴露到无障碍树。 |

## 6. 常见坑与经验

- 构造时传入 QObject 并不会自动产生正确 Role、Name 或子节点；缺失这些信息仍会让对象不可用。
- 默认 `childAt()` 会遍历子树。虚拟表格、图表或长列表应使用索引/空间数据结构重写，避免鼠标探索时退化。
- `rect()` 对不可见对象不可靠；不要用无效几何表示“对象已删除”，应让 `isValid()` 和 State 明确表达。
- `setText()` 对多数属性没有效果。真正可读的 Name/Description/Value 通常应由 `text()` 根据底层状态返回。
- 接口由 Qt 可访问性缓存管理时，不要自己随意释放；底层对象销毁和接口失效必须保持同步。

## 7. 知识点覆盖

- `QObject` 到可访问接口的适配
- `QAccessibleObject` 与 `QAccessibleWidget` 的选择
- 默认几何/命中测试及虚拟子项性能
- 接口有效性与底层对象生命周期
- Role、State、Text、树导航的派生职责
