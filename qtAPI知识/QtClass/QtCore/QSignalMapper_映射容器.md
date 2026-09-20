# QSignalMapper：把无参信号重新发射为携带映射值的信号

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSignalMapper>`  
> 所属模块：Qt Core  
> 继承：`QObject`

`QSignalMapper` 把多个可识别 sender 的无参信号汇集到 `map()`，再按 sender 对应的 int、字符串或 QObject 映射值，发出 `mappedInt()`、`mappedString()` 或 `mappedObject()`。

它在 Qt 6.11.1 中仍是受支持 API，类页和头文件没有标记 deprecated；不过官方明确说明它主要在 lambda 可以作为 slot 之前更有价值。新代码通常应优先连接带 context 的 lambda，旧代码、统一配置驱动的动态信号路由或必须暴露 mapper 式接口时再使用它。

## 它解决的问题

假设工具栏在运行时创建很多按钮，每个按钮都发出无参 `clicked()`，业务层却想得到对应命令 ID。没有 mapper 时，可以为每个按钮单独写槽，或者用 lambda 捕获 ID。`QSignalMapper` 提供第三种集中映射方式：

```cpp
auto *mapper = new QSignalMapper(this);

for (int id : commandIds) {
    auto *button = createButton(id);

    connect(button, &QPushButton::clicked,
            mapper, qOverload<>(&QSignalMapper::map));
    mapper->setMapping(button, id);
}

connect(mapper, &QSignalMapper::mappedInt,
        this, &Toolbar::runCommand);
```

点击任一按钮时，`map()` 识别发信号的 button，再发出其映射的 `mappedInt(id)`。

它只能把 sender 映射为三类预设值：`int`、`QString`、`QObject *`。如果要传结构体、多个参数、索引和额外上下文，lambda 的表达力更好。

## 新代码优先使用 lambda

同一个按钮场景，用 lambda 更短、更少间接层：

```cpp
for (int id : commandIds) {
    auto *button = createButton(id);

    connect(button, &QPushButton::clicked,
            this, [this, id] { runCommand(id); });
}
```

这里的 `this` 是 connection context：`Toolbar` 析构时，连接自动断开。不要省略 context 后只捕获裸 `this`，否则 sender 比接收对象活得更久时可能留下悬空访问风险。

选择依据：

- **普通新 UI 代码**：lambda，参数捕获直观，类型不限；
- **已有 mapper 架构或统一的动态映射表**：`QSignalMapper`，可集中增删和反查 sender；
- **按钮互斥/选中语义**：考虑 `QButtonGroup`；
- **动作分组语义**：考虑 `QActionGroup`。

## 映射模型与信号流

`setMapping(sender, value)` 为一个 sender 配置某一类映射。调用 `map()` 时：

1. 无参 `map()` 根据当前信号 sender 选择映射；
2. `map(QObject *sender)` 显式按传入 sender 选择映射；
3. mapper 发出匹配映射类型的 `mappedInt`、`mappedString` 或 `mappedObject`。

```cpp
mapper->setMapping(button, QString("open-settings"));

connect(button, &QPushButton::clicked,
        mapper, qOverload<>(&QSignalMapper::map));
connect(mapper, &QSignalMapper::mappedString,
        this, &Controller::dispatch);
```

`map()` 是重载 slot。现代函数指针连接必须用 `qOverload<>` 指定无参版本；信号本身带 `QObject *` 参数、且确实要把该参数作为 sender 处理时，使用 `qOverload<QObject *>(&QSignalMapper::map)`。

直接调用无参 `map()` 没有来自信号调用链的 sender 时没有实际映射意义。需要由业务代码明确触发某对象的映射时，调用 `map(sender)`，而不是依赖 `QObject::sender()` 的上下文。

## 配置、反查与移除

```cpp
mapper->setMapping(button, 42);

QObject *sender = mapper->mapping(42);
if (sender == button) {
    // 该 ID 当前映射到 button
}
```

三个 `mapping()` overload 从 int、字符串或对象映射值反查 sender。返回值是非拥有的 `QObject *`，可能为空；调用方要先检查，并且不能把结果保存到 sender 生命周期之后。

每个 sender 对每类映射最多设置一个值。需要替换某个 sender 的命令时，直接再次 `setMapping(sender, newValue)`；要全部撤销该 sender 的映射，调用 `removeMappings(sender)`。

`removeMappings()` **不会断开任何 signal/slot 连接**。若 sender 没有销毁，它之后仍会连接到 mapper 的 `map()`，只是不再产生对应映射信号。需要停止转发时，还应保存 `QMetaObject::Connection` 并 `disconnect()`，或销毁 sender/mapper。

文档说明映射目标对象销毁时，相关映射会自动移除；这不意味着使用 `mappedObject(QObject *)` 的槽可以无条件解引用任何已缓存的对象指针。始终把信号参数当作当次调用中使用的非拥有指针，跨事件循环保存时用 `QPointer` 或业务 ID。

## 生命周期和线程

`QSignalMapper` 是 QObject，通常以接收者为 parent：

```cpp
auto *mapper = new QSignalMapper(this);
```

这会在 parent 销毁时自动销毁 mapper，同时销毁以 mapper 为 context 的连接。mapper 不拥有 sender，也不拥有作为映射值传入的 QObject。

对象及其连接遵守标准 QObject 线程亲和性。应在 mapper 所属线程中修改 mapping；若 sender 在其他线程，连接类型和槽执行线程需明确设计。GUI 控件的 clicked 信号及其 mapper 通常都应留在 GUI 线程，不能在工作线程中直接改 mapper 配置或操作控件。

`mappedString(const QString &)` 在直接连接时引用只在信号调用期间使用；跨线程 queued connection 会按 Qt 元对象系统传递参数副本。槽中不要保存该引用本身。

## 常见错误

1. **在新代码中用 mapper 包装任意捕获。** lambda 通常更短、成本更低且类型不限。
2. **连接 `map()` 时忘记处理 overload。** 无参 sender 信号用 `qOverload<>(&QSignalMapper::map)`。
3. **误认为 `removeMappings()` 会断开连接。** 它只删映射记录。
4. **把 `mapping()` 的返回 QObject 指针当所有者。** 它是非拥有指针，可能为空或随后失效。
5. **跳过 connection context 捕获 `this`。** lambda 接收者析构后可能发生悬空访问。
6. **对同一 sender 期望一类映射保留多个值。** 每类映射最多一个，应改用自己的数据表或 lambda。
7. **跨线程直接改 GUI mapper。** QObject 和控件操作仍受线程亲和性约束。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QSignalMapper(parent)` | 创建 mapper。 | 以接收对象为 parent，统一管理 mapper 生命周期。 |
| `~QSignalMapper()` | 销毁 mapper。 | 不拥有 sender 或映射 QObject；相关以 mapper 为 context 的连接会断开。 |
| `setMapping(sender, int id)` | 为 sender 设置整数映射。 | 触发时发 `mappedInt(id)`；同一 sender 此类映射至多一个。 |
| `setMapping(sender, QString text)` | 为 sender 设置字符串映射。 | 触发时发 `mappedString(text)`；普通参数捕获更适合 lambda。 |
| `setMapping(sender, QObject *object)` | 为 sender 设置对象映射。 | 触发时发 `mappedObject(object)`；object 不被 mapper 拥有。 |
| `map()` | 根据发出当前信号的 sender 转发映射。 | 无参 overload；函数指针连接使用 `qOverload<>`。 |
| `map(QObject *sender)` | 显式按传入 sender 转发映射。 | 仅在信号确实提供 sender 或业务明确指定时使用。 |
| `mappedInt(int)` | sender 有 int 映射时发出。 | 用于统一分发整数命令/索引。 |
| `mappedString(const QString &)` | sender 有字符串映射时发出。 | 槽中不要长期保存参数引用。 |
| `mappedObject(QObject *)` | sender 有对象映射时发出。 | 参数是非拥有指针；跨异步边界改用 `QPointer` 或 ID。 |
| `mapping(int)` | 按整数映射值反查 sender。 | 结果可为空，且不拥有 QObject。 |
| `mapping(QString)` | 按字符串映射值反查 sender。 | 字符串键应有清晰唯一性约定。 |
| `mapping(QObject *)` | 按对象映射值反查 sender。 | 映射对象的生命周期仍由外部管理。 |
| `removeMappings(sender)` | 删除 sender 的全部映射记录。 | 不会断开 sender 到 mapper 的信号连接。 |

## 一句话总结

`QSignalMapper` 仍可把许多无参 sender 信号集中重发为 int、字符串或 QObject 参数，但它是 lambda 出现前的主要工具；新代码默认用带 context 的 lambda，使用 mapper 时要分清映射删除、连接断开和 QObject 所有权是三件不同的事。
