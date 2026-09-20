# Qt QAccessibleObject 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleObject>`  
> 所属模块：`Qt6::Gui`  
> 基类：`QAccessibleInterface`  
> 定位：为普通 `QObject` 实现部分无障碍接口的便利基类

## 1. 它解决什么问题

`QAccessibleObject` 为包装普通 `QObject` 的 accessible interface 提供基础实现。它保存关联对象，并默认完成对象有效性、QObject 返回、屏幕几何、按点查找子项和可访问文本设置等通用部分。

它的目标是减少自定义非 QWidget 对象实现无障碍支持时的重复代码，不是完整可访问对象：

- 仍须实现 `parent()`、`child()`、`childCount()`、`indexOfChild()`；
- 仍须实现 `text()`、`role()`、`state()`；
- 对复杂布局、逻辑子项和专用接口通常还需要覆盖 `childAt()`、`rect()` 或 `interface_cast()`；
- QWidget 子类优先考虑 `QAccessibleWidget`，它比本类提供更多 widget 语义。

## 2. 实际使用场景

例如应用有一个自绘的 QObject 驱动仪表对象，不是 QWidget，但需要让辅助技术读取名称、值和状态：

```cpp
class GaugeAccessible final : public QAccessibleObject,
                              public QAccessibleValueInterface
{
public:
    explicit GaugeAccessible(Gauge *gauge)
        : QAccessibleObject(gauge)
    {
    }

    QAccessibleInterface *parent() const override;
    QAccessibleInterface *child(int) const override { return nullptr; }
    int childCount() const override { return 0; }
    int indexOfChild(const QAccessibleInterface *) const override { return -1; }
    QString text(QAccessible::Text type) const override;
    QAccessible::Role role() const override { return QAccessible::Dial; }
    QAccessible::State state() const override;
};
```

实例通常由 `QAccessible::InterfaceFactory` 或 `QAccessiblePlugin` 创建，交给 `QAccessible` 缓存管理，而不是由业务代码直接长期持有。

## 3. 关联对象与生命周期

构造函数接收 `QObject *`，但 `QAccessibleObject` 不取得 QObject 所有权。底层对象销毁后，这个 accessible object 不应再被当作有效对象使用，`isValid()` 会反映该状态。

基类析构函数为 protected。用户代码不能把 Qt 查询得到的 `QAccessibleObject *` 直接删除；Qt 内部缓存会在合适时机释放它。自定义 factory 返回此类对象后，应让 `QAccessible::queryAccessibleInterface()` 和 cache 接管管理。

对象和 interface 都应在对象所属线程使用。基类并不把 QObject 变成线程安全对象，后台线程仍不能直接读取其 GUI 状态。

## 4. 逐项 API 说明

### `explicit QAccessibleObject(QObject *object)`

为 `object` 创建 accessible wrapper。`object` 必须在 wrapper 有效期内存在；构造函数不设置 QObject parent，也不转移所有权。

它适合普通 QObject 的基础封装。对于 QWidget，优先使用能提供 window、widget geometry、action 等更多默认行为的 `QAccessibleWidget`。

### `~QAccessibleObject()`（保护）

受保护虚析构函数。析构由 Qt 无障碍缓存与派生对象控制；不要从客户端路径显式 delete。

### `bool isValid() const override`

检查关联 QObject 是否仍可用。返回 `false` 后，调用者不应继续根据 `object()`、`rect()` 或自定义状态访问底层对象。

它不检查对象是否 visible、enabled 或有焦点；这些属于 `state()` 的语义。

### `QObject *object() const override`

返回关联 QObject 的非拥有指针。对象已失效时可能返回空或不可用的结果，调用方应先看 `isValid()`。

### `QRect rect() const override`

返回关联对象的屏幕几何。只有可映射到视觉几何的 QObject 才能提供有意义的结果；非视觉 QObject 或不可见对象可能得到空/无效矩形。

自绘对象或对象的可访问区域不等于底层 QObject 几何时，应覆盖此函数，确保结果和 `childAt()` 使用同一坐标体系。

### `void setText(QAccessible::Text type, const QString &text) override`

尝试设置对象的可访问文本属性。底层对象是否支持写入取决于对象实现；不少文本属性仍是只读，调用可能无效果。

覆盖时要把 `Name`、`Description`、`Value` 等属性映射到真实的、允许写入的对象状态，不能为了接口而绕过验证或在属性查询时产生副作用。

### `QAccessibleInterface *childAt(int x, int y) const override`

提供按屏幕坐标查找 accessible 子项的默认实现。它会基于对象子项进行遍历，因此适合子项不多、层级接近 QObject tree 的对象。

表格、树、大量图元或虚拟化列表应覆盖它，用自己的空间索引或模型命中计算，避免为一次鼠标命中创建/遍历大量 interface。点不在 child 上时返回 `nullptr`。

## 5. 实现边界

### 不要把 QObject 子树机械映射为 accessible 子树

很多 QObject 是内部控制器、布局辅助对象或模型，不应成为辅助技术导航目标。只暴露用户能感知、需要操作或需要获知变化的对象。

### 可访问几何必须是屏幕坐标

`rect()` 和 `childAt()` 均按屏幕坐标工作。若对象在滚动区域、缩放视图或多屏窗口中，必须完成正确映射；不要直接返回局部 `geometry()`。

### 子项应由缓存管理

从 `child()` 或 `childAt()` 动态创建 accessible 子项时，按 `QAccessible::registerAccessibleInterface()` 的规则注册，避免返回无人管理的裸指针或同一 child 被重复注册。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QAccessibleObject(QObject *)` | 创建 QObject 的基础 accessible wrapper。 | 不拥有 QObject；非 QWidget 对象的常用基类。 |
| 生命周期 | `~QAccessibleObject()` | 受保护虚析构。 | 由 Qt cache/派生对象管理，客户端不删除。 |
| 有效性 | `isValid()` | 检查关联对象是否仍可用。 | 不等于 enabled 或 visible。 |
| 对象 | `object()` | 返回被包装 QObject。 | 非拥有指针，先检查有效性。 |
| 几何 | `rect()` | 返回对象屏幕几何。 | 非视觉/不可见对象可能无有效矩形。 |
| 文本 | `setText(Text, QString)` | 尝试设置可访问文本。 | 多数属性只读；不可绕过业务验证。 |
| 命中 | `childAt(int, int)` | 按屏幕点查找 child。 | 默认遍历适合小树；虚拟化/大模型应覆盖优化。 |

### 一句话总结

`QAccessibleObject` 是普通 QObject 的无障碍便利底座：它处理对象关联和基础几何/命中，但仍需要派生类准确提供层级、角色、状态和文本语义，并让动态子项交给 Qt 的 accessible cache 管理。
