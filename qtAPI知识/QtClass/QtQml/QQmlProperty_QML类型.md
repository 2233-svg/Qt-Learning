# QQmlProperty：按 QML 语义访问某个对象实例的属性

> Qt 6.11.1 | `#include <QQmlProperty>` | CMake: `Qt6::Qml`

`QQmlProperty` 是“某一个对象上的某一个 QML 属性”的运行时描述。`QMetaProperty` 描述的是类的属性定义，而 `QQmlProperty` 绑定到具体 `QObject` 实例；它额外处理 QML 的类型安全和附加属性等规则。

它适合通用检查器、自动化测试、组件编辑器和框架代码：属性名在编译期不知道，但仍需要按 QML 可见的方式读取、写入或订阅变化。

## 从具体对象取得属性

```cpp
#include <QQmlProperty>

QQmlProperty pixelSize(view.rootObject(), "font.pixelSize");
if (!pixelSize.isValid() || !pixelSize.isWritable())
    return;

qDebug() << "old:" << pixelSize.read().toInt();
if (!pixelSize.write(24))
    qWarning() << "could not set font.pixelSize";
```

构造时给出 `QObject *` 和属性路径。只有对象而没有名称的构造函数可用于取得对象的默认属性语义；需要对特定属性读写时，应明确传入名称。

若属性解析依赖 QML 上下文或引擎，可传 `QQmlContext *` 或 `QQmlEngine *` 的重载。框架代码不要为了省一个参数随意使用全局或不相关的 engine；上下文决定 QML 特有属性和类型信息如何解析。

## 先区分三种状态

1. `isValid()` 为 false：名字无法解析、对象无效，或属性不可用。
2. `isProperty()` 为 true：普通 Qt/QML 属性，可检查读写、reset、notify。
3. `isSignalProperty()` 为 true：这是 QML 信号属性而不是存储值，应该从 `method()` 获取 `QMetaMethod`，不能把它当普通 QVariant 属性读写。

```cpp
if (property.isSignalProperty()) {
    const QMetaMethod signal = property.method();
    // 使用 QMetaMethod 做信号相关的反射处理。
} else if (property.isProperty()) {
    const QVariant current = property.read();
}
```

`PropertyTypeCategory` 再把正常属性分为 `List`、`Object`、`Normal`；无效属性和 signal property 为 `InvalidCategory`。它适合让通用 UI 决定用对象树、列表编辑器还是标量编辑器展示，而不是用 `propertyTypeName()` 的字符串猜测。

## 写入、重置和变化通知

`write()` 返回 `bool`，必须检查。失败的常见原因包括属性无效、只读、QVariant 无法转换为目标 `QMetaType`，或目标对象的设置逻辑拒绝该值。

```cpp
if (property.isResettable())
    property.reset();

if (property.hasNotifySignal()) {
    const bool connected = property.connectNotifySignal(
        observer, SLOT(refresh()));
    Q_ASSERT(connected);
}
```

`hasNotifySignal()` 仅表示存在变化通知；`needsNotifySignal()` 用于判断该属性在 QML 使用中是否需要通知语义。`connectNotifySignal()` 会在属性不是普通 Qt 属性、缺少 NOTIFY，或目标槽不存在时失败。传字符串槽名的重载需要 `SLOT(...)` 宏，避免元对象签名不匹配。

不要把 `QQmlProperty` 当作线程同步工具。它操作的仍是 QObject，读写和信号连接必须遵守对象线程亲和性；跨线程时应改为信号槽或在对象所属线程执行操作。

## 反射代码的边界

- `read()` 返回的是 `QVariant`，空 QVariant 既可能是一个有效“无效值”也可能表示无法读取，先检查 property 状态与目标类型。
- `propertyMetaType()` 比旧的整型 `propertyType()` 更适合新代码中的类型判断。
- `object()` 只返回被包装对象，并不延长其生命周期。对象销毁后不应继续使用已保存的 property。
- 静态 `read()` / `write()` 是一次性快捷入口；要多次操作或订阅通知，持有实例更清晰。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQmlProperty(QObject *, QString)` | 解析指定实例上的 QML 属性 | 先用 `isValid()` 确认名称和路径有效 |
| 带 `QQmlContext *` / `QQmlEngine *` 的构造函数 | 按给定 QML 环境解析属性 | 使用实际所属上下文，避免错解附加属性 |
| `isValid()` | 是否成功表示一个可用属性 | 不代表可读或可写 |
| `type()` / `isProperty()` / `isSignalProperty()` | 区分无效、普通属性和 signal property | signal property 通过 `method()` 处理，不是 QVariant 值 |
| `read()` / 静态 `read()` | 读取属性为 QVariant | 返回值要结合元类型和有效性解释 |
| `write()` / 静态 `write()` | 写入 QVariant，返回是否成功 | 检查可写性和转换失败 |
| `reset()` | 调用属性的 RESET 行为 | 仅 `isResettable()` 为 true 时有意义 |
| `propertyMetaType()` / `propertyTypeCategory()` | 查询元类型和列表/对象/普通分类 | 用于运行时编辑器和校验，不改变属性 |
| `hasNotifySignal()` / `connectNotifySignal()` | 检查并连接 NOTIFY 信号 | 不是普通属性、无 NOTIFY 或槽签名错误都会失败 |
| `isBindable()` / `isDesignable()` | 查询 Qt 属性附加能力 | 只反映元对象能力，不替代业务层权限判断 |

## 相关类型

- `QMetaProperty`：描述类定义上的 Qt 属性，不绑定具体对象。
- `QQmlContext`、`QQmlEngine`：为 QML 特有的属性解析提供环境。
- `QVariant`、`QMetaType`：反射式读写中的值和类型载体。
