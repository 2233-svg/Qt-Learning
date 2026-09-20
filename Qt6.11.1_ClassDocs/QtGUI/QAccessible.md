# QAccessible

> Qt 6.11.1 · Qt GUI · 来自 `QAccessible`

## 1. 先建立直觉

`QAccessible` 是 Qt 无障碍系统的全局入口。它连接三方：应用中的 `QObject` / `QWidget`、Qt 的 `QAccessibleInterface` 表示层、以及屏幕阅读器和平台无障碍服务。标准 Qt 控件已有内建支持；此类主要服务于自定义控件、复合控件、画布和可访问性事件通知。

无障碍并不是给控件加一段说明文字。辅助技术需要知道它是什么（Role）、叫什么（Name）、当前状态如何（State）、可做什么（Action）、值和文本是什么，以及当这些信息变化时得到可靠的事件。

## 2. 类说明

- 头文件：`#include <QAccessible>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：静态工具类；不实例化。
- 协作类：`QAccessibleInterface` 为对象提供语义树，`QAccessibleEvent` 及其子类表达变化，`QAccessibleActionInterface` / `QAccessibleTextInterface` 等补充专业能力。

对于普通 `QWidget`，优先设置可见文本、`accessibleName`、`accessibleDescription` 和合理焦点行为。仅当标准映射无法表达自定义交互时，才实现接口工厂或自定义 `QAccessibleInterface`。

## 3. API 速查

| API | 用途 |
|---|---|
| `queryAccessibleInterface(object)` | 查询 Qt 为对象创建或缓存的可访问接口；调用方不拥有返回值。 |
| `isActive()` | 是否有平台辅助技术正在请求无障碍数据。 |
| `updateAccessibility(event)` | 将状态、文本、焦点等变化通知平台。 |
| `installFactory(factory)` | 注册自定义对象到接口的工厂函数。 |
| `removeFactory(factory)` | 移除之前注册的工厂。 |
| `registerAccessibleInterface(iface)` | 注册手工 `new` 出来的接口，交由 Qt 缓存管理。 |
| `accessibleInterface(id)` / `uniqueId(iface)` | 在接口和缓存 ID 间查询。 |
| `deleteAccessibleInterface(id)` | 删除已注册接口并使 ID 失效。 |
| `setRootObject(object)` | 设置无障碍树根；常规 Qt 应用通常不需要。 |
| `Role` | 描述对象类别，如 `Button`、`Slider`、`Table`、`Heading`、`Window`。 |
| `State` | 描述状态位，如 `focused`、`checked`、`disabled`、`expanded`、`invisible`。 |
| `Text` | 描述文本字段，如 `Name`、`Description`、`Value`、`Help`、`Identifier`。 |
| `Event` | 描述通知类型，如焦点、值、名称、对象显示/隐藏和文本变化。 |
| `InterfaceType` | 声明接口可转换到文本、值、动作、表格、选择或属性子接口。 |
| `Relation` | 表达 label、description、controller 等对象关系。 |
| `TextBoundaryType` | 指定字符、词、句、段、行等文本边界查询方式。 |
| `AnnouncementPoliteness` | 设置公告是正常排队还是立即打断；Qt 6.8 起。 |
| `Attribute` | 设置 Level、Locale、Orientation 或自定义属性；部分项有版本限制。 |

## 4. 关键用法

### 查询现有控件的语义

```cpp
QAccessibleInterface *iface =
    QAccessible::queryAccessibleInterface(myButton);

if (iface) {
    const auto role = iface->role();
    const auto state = iface->state();
    const QString name = iface->text(QAccessible::Name);
}
```

接口由 Qt 的缓存管理，不能 `delete`。查询函数会先尝试已安装的工厂和插件，随后可回退到父类实现；因此它是检查标准映射和调试自定义控件的首选入口。

### 在自定义状态变化后发送事件

```cpp
void Meter::setValue(int value)
{
    if (m_value == value)
        return;

    m_value = value;
    update();

    QAccessibleValueChangeEvent event(this, m_value);
    QAccessible::updateAccessibility(&event);
}
```

事件对象在栈上创建即可，`updateAccessibility()` 同步读取它。应只在可访问语义实际变化时发送，避免每一帧动画都制造事件洪流；若组装事件数据代价高，可先用 `isActive()` 判断是否有辅助技术监听。

### 为真正自定义的 QObject 安装工厂

```cpp
QAccessible::installFactory(
    [](const QString &key, QObject *object) -> QAccessibleInterface * {
        if (key == u"Meter"_s)
            return new AccessibleMeter(static_cast<Meter *>(object));
        return nullptr;
    });
```

工厂按后安装先尝试的顺序调用。它应只为能确认类型的对象返回接口，其余情况返回 `nullptr` 让其他工厂或父类映射继续处理。应用关闭、插件卸载或测试隔离时，应对称调用 `removeFactory()`。

## 5. 枚举怎样选

| 需求 | 首选语义 |
|---|---|
| 可点击的自定义命令 | `Role::Button` + `ActionInterface`，提供触发动作。 |
| 数值调节器 | `Role::Slider` 或 `SpinBox` + `ValueInterface`，报告当前/最小/最大值。 |
| 可展开树节点 | `Role::TreeItem`，用 `expandable` 与 `expanded` 表达状态。 |
| 图表或画布 | 外层可用 `Role::Chart` / `Canvas`；重要数据点要提供可导航子对象或文本替代。 |
| 纯装饰图片 | 让它不干扰无障碍树；不要为无语义的图案伪造名称。 |
| 状态提示 | 常规更新用合适事件；必须立即打断时才用 `AnnouncementPoliteness::Assertive`。 |
| 表单标签 | 用 `Relation::Label` / `Labelled` 建立关系，而非仅靠屏幕位置。 |

`Name` 是简短可识别名称，`Description` 用于补充，`Value` 是当前值，`Help` 是较长的操作帮助，`Identifier`（Qt 6.8 起）适合稳定测试或自动化识别。不要把整段说明、当前值和快捷键全塞进 Name。

## 6. 常见坑与经验

- 不要为标准控件重复实现接口。错误的 Role 或 State 比缺失信息更会误导读屏用户。
- `isActive()` 为 false 不代表不必维护控件语义；辅助技术可以在之后启动。它只适合跳过昂贵的事件数据构造。
- 手工 `new QAccessibleInterface` 后只能注册一次；更常见、更稳妥的方案是让 `queryAccessibleInterface()` 通过工厂管理。
- 对象销毁、隐藏、焦点、名称、值、选中状态和文本内容的变化，都应选择相应事件；不要一律发送模糊的通用通知。
- `State::invisible`、`offscreen`、`disabled`、`focused` 和 `selected` 不是同义词。尤其不要把“屏幕外但可滚动到”错误标为不存在。
- `Assertive` 公告会中断用户当前阅读，应只用于错误、危险或不可忽略的即时结果。
- 无障碍对象和 GUI 状态通常在 GUI 线程维护；后台任务应通过信号回到 GUI 线程再更新控件和发送事件。

## 7. 知识点覆盖

- Qt 无障碍树、平台桥接与接口缓存
- Role、Name、Description、Value、State 和 Relation
- 文本、值、动作、表格、选择等专用接口
- 自定义控件接口工厂与生命周期
- 无障碍事件、事件频率和公告优先级
- 屏幕阅读器、键盘焦点和自绘 UI 的验证思路
