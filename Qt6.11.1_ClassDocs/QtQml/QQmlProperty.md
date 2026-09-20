# QQmlProperty
> Qt 6.11.1 · Qt QML · 来自 `QQmlProperty`

## 作用定位

`QQmlProperty` 是 QML 视角下的属性反射工具。它可以在运行期定位某个 QObject 的属性或信号属性，读取、写入、reset、连接 NOTIFY 信号，并识别属性类别：普通值、QObject 指针、列表属性或无效属性。

它比 `QMetaProperty` 更懂 QML 上下文和引擎，因此能处理 QML 扩展属性、绑定环境下的类型转换等问题。

## 类说明

- 头文件：`#include <QQmlProperty>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 常用协作：`QQmlContext`、`QQmlEngine`、`QQmlListReference`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 可只给对象，也可给对象+属性名，并传入 context 或 engine。 |
| `isValid()` | 是否成功定位到属性。 |
| `type()` | 区分普通属性、信号属性或无效。 |
| `propertyTypeCategory()` | 区分 normal、object、list、invalid。 |
| `read()` / `write()` | 读取或写入属性值。 |
| 静态 `read()` / `write()` | 一次性按对象和属性名读写。 |
| `reset()` | 调用属性 reset 函数。 |
| `isWritable()` / `isResettable()` / `isDesignable()` | 查询元属性能力。 |
| `hasNotifySignal()` / `needsNotifySignal()` | 判断属性是否有通知信号以及绑定是否需要它。 |
| `connectNotifySignal()` | 把属性 NOTIFY 信号连接到槽。 |
| `property()` / `method()` | 返回底层 `QMetaProperty` 或信号 `QMetaMethod`。 |
| `propertyMetaType()` / `propertyTypeName()` / `propertyType()` | 查询属性类型。 |
| `object()` / `name()` / `index()` | 查询目标对象、属性名和元对象索引。 |

## 使用场景

- 写属性编辑器、调试器、自动表单。
- C++ 中动态读写 QML 对象属性。
- 检查某属性是否可绑定、可写、是否有 NOTIFY。
- 在通用框架里监听属性变化。

## 常见坑与经验

- 构造时给 context/engine 很重要，尤其是 QML 扩展属性或需要 QML 类型转换的属性。
- 写属性返回 false 时，先查属性是否 `isWritable()`，再查 QVariant 类型是否能转换。
- 没有 NOTIFY 的属性可以读写，但 QML 绑定无法可靠自动更新。
- `SignalProperty` 不是普通值属性，不能按 `read()`/`write()` 使用。
- 列表属性要结合 `QQmlListReference` 操作，不要把它当普通 QVariantList。

## 知识点覆盖

- QML 属性反射
- QMetaProperty 与 QML 上下文
- NOTIFY 信号和绑定刷新
- 属性类别：普通、对象、列表、信号
- 动态属性编辑与调试
