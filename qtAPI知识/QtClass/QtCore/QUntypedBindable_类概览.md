# Qt QUntypedBindable：在不知道属性类型时操作 Qt 绑定

`QUntypedBindable` 是 Qt 属性绑定系统的类型擦除接口。它把 `QProperty<T>`、`QObjectBindableProperty` 等不同实现、不同值类型的可绑定属性包装成统一句柄，让元对象、属性编辑器或通用框架在**不知道 `T` 是什么**时仍能检查、观察和替换绑定。

最常见的来源不是手工构造，而是运行时反射：

```cpp
QMetaProperty property =
    object->metaObject()->property(propertyIndex);

QUntypedBindable bindable = property.bindable(object);
if (!bindable.isValid())
    return;

const QMetaType type = bindable.metaType();
qDebug() << property.name() << type.name();
```

它能做的是绑定管理和变化观察，不是通用的“无类型读写属性”对象。读取或设置属性值仍然应使用 `QMetaProperty::read()` / `write()`、`QVariant`，或者在编译期已知类型时改用 `QBindable<T>`。

## 它解决什么问题

`QBindable<T>` 有明确的值类型，日常 C++ 代码应优先使用它：

```cpp
QBindable<int> width = widget->bindableWidth();
width.setBinding([settings] { return settings->preferredWidth(); });
```

但工具型代码往往只拿到一个 `QObject *` 和一个 `QMetaProperty`。例如属性检查器、Designer 类工具、通用配置框架或自动化测试器不知道属性是 `int`、`QString`、枚举还是自定义 metatype。为每种类型写一套绑定逻辑既不现实，也会破坏运行时反射的通用性。

`QUntypedBindable` 解决的正是这个问题：

- 用一个非模板值类型表示任意可绑定属性；
- 查询底层属性的 `QMetaType`；
- 读取、取走或安装 `QUntypedPropertyBinding`；
- 监听值变化，而不用知道回调参数类型；
- 区分无效接口、只读接口、可访问但不支持绑定的接口。

它并不会抹掉所有类型约束。安装绑定时，Qt 仍然要求绑定结果的 `QMetaType` 与目标属性的类型完全匹配。

## 构建与包含

`QUntypedBindable` 在 Qt 6.0 引入，属于 Qt Core：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QUntypedBindable>
```

qmake 工程使用：

```text
QT += core
```

公共包含文件最终导出的是 `qproperty.h`。如果接口来自 `QMetaProperty::bindable()`，还需要相应的元对象和 QObject 定义。

## 先区分四个状态问题

使用 `QUntypedBindable` 时，很多 bug 来自只检查了一个布尔值。下面四个问题彼此不同：

| 问题 | 对应 API | 含义 |
| --- | --- | --- |
| 句柄是否指向属性 | `isValid()` | 是否有底层属性数据；默认构造和空指针构造为无效 |
| 属性是否有绑定接口 | `isBindable()` | 是否能读取/安装 property binding |
| 能否安装绑定或观察 | `isReadOnly()` | const 属性或不支持写入/观察的接口为只读 |
| 值类型是什么 | `metaType()` | 用于检查无类型 binding 是否与目标属性匹配 |

`isValid()` 不是“属性一定能绑定”。Qt 的头文件将两层概念分开：一个有效的无类型句柄可以仍然没有 `getBinding` 接口；此时 `binding()` 返回空 binding，`hasBinding()` 为 `false`。

```cpp
QUntypedBindable bindable = property.bindable(object);
if (!bindable.isValid())
    return;

if (!bindable.isBindable()) {
    qDebug() << "The property has no binding interface";
    return;
}

if (bindable.isReadOnly()) {
    qDebug() << "The property binding cannot be replaced";
    return;
}
```

`isBindable()` 是头文件公开的能力检查，但当前类页的成员表没有将它列出。写通用框架时仍应使用这个检查，而不要从 `hasBinding()` 反推出属性支持绑定。

## 构造与生命周期

默认构造得到无效句柄：

```cpp
QUntypedBindable bindable;
Q_ASSERT(!bindable.isValid());
```

也可以从属性对象指针构造：

```cpp
QProperty<int> count = 1;
QUntypedBindable bindable(&count);
Q_ASSERT(bindable.isValid());
```

如果传入的是 `const` 属性指针，句柄会是只读的：

```cpp
const QProperty<int> count = 1;
QUntypedBindable bindable(&count);
Q_ASSERT(bindable.isReadOnly());
```

传入空指针会得到无效句柄。构造完成后，`QUntypedBindable` **不拥有**属性，也不延长属性或所属 `QObject` 的生命周期。属性销毁、被移动或其 owner 被销毁后，先前保存的句柄不应再被调用；不要把它当作 `QPointer`。

这个接口按值复制很轻量，但副本仍然只是同一个底层属性的非拥有视图。工具代码常把它短暂保存到当前操作范围内；需要跨对象销毁边界保存时，应保存 QObject 的受控引用和属性标识，在使用前重新取得 bindable。

## 从元对象获得无类型 bindable

`Q_PROPERTY` 可通过 `BINDABLE` 属性声明对绑定系统的支持。`QMetaProperty::bindable(QObject *)` 会把具体属性封装为 `QUntypedBindable`，让反射代码不必知道类型：

```cpp
void inspectBindableProperties(QObject *object)
{
    const QMetaObject *metaObject = object->metaObject();
    for (int i = 0; i < metaObject->propertyCount(); ++i) {
        const QMetaProperty property = metaObject->property(i);
        const QUntypedBindable bindable = property.bindable(object);

        if (!bindable.isValid())
            continue;

        qDebug().noquote()
            << property.name()
            << bindable.metaType().name()
            << "binding:" << bindable.hasBinding()
            << "read-only:" << bindable.isReadOnly();
    }
}
```

`QMetaProperty::bindable()` 不会因为属性有 `NOTIFY` 信号就必然返回有效句柄。真正的可绑定元对象属性通常需要 `Q_PROPERTY(... BINDABLE bindableAccessor)`，或者由 Qt 提供兼容的属性适配路径。返回无效句柄时，应回退到普通 `QMetaProperty::read()` / `write()` 与 `NOTIFY` 信号逻辑。

如果在编译期知道属性类型，应直接调用对象的 `bindableXxx()`，因为 `QBindable<T>` 会在编译期保留类型，并能直接读取 `value()`、安装 `QPropertyBinding<T>`。

## binding、makeBinding 与 takeBinding 不是同一件事

这三个 API 的名字相近，语义却不同。

### `binding()`：拿到当前已安装的表达式

`binding()` 返回属性目前正在使用的 `QUntypedPropertyBinding`。没有绑定时返回默认构造的空 binding：

```cpp
QUntypedPropertyBinding current = bindable.binding();
if (current.isNull()) {
    qDebug() << "No binding is installed";
}
```

它不会移除绑定，也不会计算新表达式。把返回值保存起来可用于之后恢复，但绑定中的依赖对象仍需要保持有效。

### `makeBinding()`：制造“读取该属性”的表达式

`makeBinding()` 创建一个新的 binding，表达式的结果就是底层属性的当前值。它通常用于将一个未知类型属性作为另一个未知类型属性的依赖来源：

```cpp
QUntypedPropertyBinding mirrorSource = sourceBindable.makeBinding();
const bool installed = targetBindable.setBinding(mirrorSource);
```

这里不是复制 source 当前的值，而是创建“target 跟随 source”的绑定关系。`location` 默认使用 `QT_PROPERTY_DEFAULT_BINDING_LOCATION`，用于记录绑定创建位置，便于诊断绑定循环和错误。应用通常不必手写该参数；框架可在需要时传入自己的 `QPropertyBindingSourceLocation`。

### `takeBinding()`：移除并交还当前绑定

`takeBinding()` 从属性中移除当前 binding，并把被移除的对象返回：

```cpp
QUntypedPropertyBinding saved = bindable.takeBinding();
Q_ASSERT(!bindable.hasBinding());

// 之后可在类型仍匹配时重新安装。
bindable.setBinding(saved);
```

没有绑定、接口无效或接口不支持设置时返回空 binding。它从 Qt 6.1 开始提供。取走后属性保留当时的值，但不再随原依赖变化；这不是“暂停求值”的通用开关。

## 安装绑定：类型、只读与失败返回

`setBinding(const QUntypedPropertyBinding &binding)` 将 binding 安装到目标属性。成功需要同时满足：

1. `QUntypedBindable` 有效；
2. 目标不是只读；
3. 目标支持设置 binding；
4. binding 为空，或者 `binding.valueMetaType()` 与 `bindable.metaType()` 完全相同。

```cpp
const QUntypedPropertyBinding sourceBinding =
    sourceBindable.makeBinding();

if (sourceBinding.valueMetaType() != targetBindable.metaType()) {
    qWarning() << "Cannot bind different property types";
    return;
}

if (!targetBindable.setBinding(sourceBinding))
    qWarning() << "Target rejected the binding";
```

这里的类型匹配不是 `QVariant` 风格的“能转换就行”。例如 `int` 到 `double`、枚举到整数、`QString` 到 `QByteArray` 都不应假设可由 `setBinding()` 自动转换。需要转换时，创建一个返回目标类型的显式 binding，或通过类型明确的 `QBindable<T>` 完成转换。

向属性直接赋值通常会移除其已有 binding。不同属性实现的 setter 规则仍需遵守其类文档；不要在已经安装 binding 的属性上随意调用普通 setter 后，期待绑定仍然存在。

## 观察值变化：返回对象就是订阅生命线

`onValueChanged()`、`subscribe()` 和 `addNotifier()` 都安装回调，但最容易错的地方是：**返回的 handler/notifier 必须保持存活。**

```cpp
class Inspector
{
    QPropertyNotifier notifier;

public:
    void watch(QUntypedBindable bindable)
    {
        notifier = bindable.addNotifier([this] {
            refreshCurrentValue();
        });
    }
};
```

如果把返回值丢弃，临时对象会立刻析构，回调也随之取消：

```cpp
bindable.addNotifier([] {
    qDebug() << "This observer dies immediately";
}); // 错误：返回的 QPropertyNotifier 没有保存
```

三者的区别：

| API | 首次调用时机 | 返回类型 | 常见用途 |
| --- | --- | --- |
| `onValueChanged(f)` | 只在后续值变化时 | `QPropertyChangeHandler<Functor>` | 类型已知或局部闭包可保存时 |
| `subscribe(f)` | 先立刻调用一次，再监听后续变化 | `QPropertyChangeHandler<Functor>` | 初始化 UI 后持续同步 |
| `addNotifier(f)` | 只在后续值变化时 | `QPropertyNotifier` | 需要把无模板返回对象存为成员时 |

变化处理器可能立即调用，也可能根据绑定求值上下文被延后调用。因此回调应短小、可重入安全，且不要在回调里无条件再次写回同一属性，否则可能形成反馈循环或重复求值。

回调没有自动绑定到 `QObject` 的生命周期。捕获 `this` 时，要保证 handler 在对象销毁前先被销毁或清空；可以将 notifier 作为 owner 的成员，或在 QObject 销毁路径中重置它。

## `metaType()` 与类型擦除

类型被擦除后，`metaType()` 是恢复运行时类型信息的入口：

```cpp
const QMetaType type = bindable.metaType();
if (type == QMetaType::fromType<int>()) {
    // 现在可以走 int 专用的框架分支
}
```

无效 bindable 返回无效 `QMetaType`。不要只检查 `type.id() != 0` 来判断所有情况，优先使用 `bindable.isValid()`，再按需要使用 `QMetaType` 的有效性检查。

`QUntypedPropertyBinding::valueMetaType()` 说明绑定表达式会生成什么类型；它与目标 `metaType()` 相等是 `setBinding()` 成功的关键条件。值读取/写入并不由 `QUntypedBindable` 提供，通用编辑器应将 `metaType()` 与 `QMetaProperty::read()` / `write()` 配合使用。

## 线程、求值和循环

Qt 的属性绑定不是自动线程同步机制。属性、其 owner、依赖属性和回调通常应由同一线程访问。把 `QUntypedBindable` 复制到其他线程不会让底层 `QProperty` 变成线程安全对象。

绑定表达式通常在 Qt 需要最新值时求值，调用 `value()`、读取依赖或触发更新都可能促使求值。表达式不应修改参与该绑定的属性，也不应执行阻塞 I/O、长计算或跨线程等待。

循环依赖是实际风险：

```text
a 绑定到 b
b 又绑定到 a
```

运行时可能报告 binding loop 或得到不符合预期的更新。通过 `makeBinding()` 动态接线时，应在安装前维护依赖图，至少避免将一个属性间接绑定回自身。

## 常见使用场景

### 通用属性面板

运行时遍历 `QMetaObject`，对支持 `BINDABLE` 的属性显示类型、是否已绑定和只读状态，并允许用户为兼容类型的属性建立跟随关系。

### 设计器、调试器和自动化工具

框架无需在编译期依赖业务 QObject 类型，即可观察某属性变化、诊断 binding 错误或暂时取走绑定。

### 以未知类型转发属性依赖

通过 `source.makeBinding()` 生成表达式，再用 `target.setBinding()` 安装到同类型目标属性，构建通用镜像或配置联动。

### 适配不同属性实现

业务库可能使用 `QProperty<T>`，Qt 类可能返回 `QObjectBindableProperty` 的包装；`QUntypedBindable` 让工具代码只面对统一接口。

## 常见错误与排查顺序

- 只检查 `isValid()`，却忽略 `isBindable()` 或 `isReadOnly()`。
- 把无类型 bindable 当作通用 `QVariant` getter/setter。值访问应交给 `QMetaProperty` 或 `QBindable<T>`。
- 创建 `QPropertyNotifier` / `QPropertyChangeHandler` 后不保存返回值，导致订阅立即取消。
- 误把 `subscribe()` 当成“只监听未来”。它会先同步调用一次回调。
- 将 `binding()` 误解为“创建跟随当前属性的绑定”。要创建来源表达式使用 `makeBinding()`。
- 将 `takeBinding()` 误解为临时冻结。它会移除绑定，后续不会自动恢复。
- 忽略 `setBinding()` 的 `false` 返回值。检查有效性、只读状态和 `metaType()` 是否相等。
- 假设 `int` binding 能自动绑定到 `double` property。类型擦除不等于放弃类型匹配。
- 在 binding 回调中无条件写回同一属性，形成反馈或循环。
- 将 bindable 保存到属性或 QObject 已销毁之后再使用。
- 跨线程读写同一个 property，并误以为 bindable 负责同步。

## 逐项 API 说明

### 构造与能力检查

#### `QUntypedBindable::QUntypedBindable()`

默认构造无效句柄。除非成员另有说明，在无效对象上调用操作通常没有效果；使用前先检查 `isValid()`。

#### `QUntypedBindable::QUntypedBindable(Property *property)`

从支持 Qt bindable 接口的属性对象构造非拥有视图。空指针产生无效对象；若 `Property` 是 const，结果为只读，不能安装或取走 binding。

#### `bool QUntypedBindable::isValid() const`

判断对象是否关联了底层属性数据。它不保证接口可以读取或设置 binding，因此通用代码还应检查 `isBindable()` 和 `isReadOnly()`。

#### `bool QUntypedBindable::isBindable() const`

判断底层接口是否提供读取 binding 的能力。该公开头文件 API 在当前类页成员表中未列出；无绑定接口时 `binding()` 返回空对象，`hasBinding()` 为 `false`。

#### `bool QUntypedBindable::isReadOnly() const`

判断是否不能通过此接口设置 binding 或安装 observer。const 属性构造出来的 bindable 是只读。该 API 自 Qt 6.1 提供。

#### `QMetaType QUntypedBindable::metaType() const`

返回底层属性的运行时值类型。无效 bindable 返回无效 `QMetaType`；用它与 `QUntypedPropertyBinding::valueMetaType()` 比较以验证 binding 是否可安装。该 API 自 Qt 6.2 提供。

### Binding 管理

#### `QUntypedPropertyBinding QUntypedBindable::binding() const`

返回当前已安装的 binding；没有 binding 或不支持绑定时返回空对象。不会改变属性状态。

#### `bool QUntypedBindable::hasBinding() const`

判断是否有非空的当前 binding。本质上是对 `binding()` 结果的空值检查，不是“属性支持绑定”的能力检查。

#### `QUntypedPropertyBinding QUntypedBindable::makeBinding(const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION) const`

创建一个返回底层属性值的新 binding，可用于让另一个同类型属性跟随当前属性。它不会安装到当前属性，也不会复制当前已有 binding。

#### `bool QUntypedBindable::setBinding(const QUntypedPropertyBinding &binding)`

安装或清除 binding。目标无效、只读、不可设置，或非空 binding 的 `valueMetaType()` 与目标 `metaType()` 不相等时返回 `false`。传入空 binding 用于清除已有 binding。

#### `QUntypedPropertyBinding QUntypedBindable::takeBinding()`

移除并返回当前 binding。没有 binding 或无法写入时返回空 binding；取走后属性仍保留当前值，但不再跟随原依赖。该 API 自 Qt 6.1 提供。

### 变化观察

#### `QPropertyChangeHandler<Functor> QUntypedBindable::onValueChanged(Functor f) const`

注册值变化回调。回调在值变化后立即或延后执行，具体取决于求值上下文；必须保存返回 handler，handler 或属性销毁后观察停止。

#### `QPropertyChangeHandler<Functor> QUntypedBindable::subscribe(Functor f) const`

先调用一次 `f()`，再按 `onValueChanged()` 的规则持续观察。适合“立即刷新，再跟随更新”的场景；首次调用也要求回调对当前状态安全。

#### `QPropertyNotifier QUntypedBindable::addNotifier(Functor f)`

注册值变化回调并返回非模板 `QPropertyNotifier`。它与 `onValueChanged()` 的监听生命周期相同，但更容易作为固定类型成员保存。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUntypedBindable()` | 创建无效句柄 | 默认不关联任何属性 |
| `QUntypedBindable(Property *property)` | 包装任意属性实现 | 非拥有；空指针无效，const property 为只读 |
| `isValid()` | 判断是否关联属性 | 不等于一定支持 binding |
| `isBindable()` | 判断能否访问 binding 接口 | 头文件公开；应与 `isValid()` 区分 |
| `isReadOnly()` | 判断能否写入 binding/观察 | Qt 6.1 起；const property 通常为 true |
| `metaType()` | 查询底层值类型 | Qt 6.2 起；无效对象返回无效 metatype |
| `binding()` | 获取当前 binding | 无 binding 或接口不支持时返回空 binding |
| `hasBinding()` | 查询是否装有 binding | 不是“属性支持绑定”的判断 |
| `makeBinding(location)` | 创建读取该属性值的新表达式 | 用于建立跟随关系；不会安装或复制现有 binding |
| `setBinding(binding)` | 安装或清除 binding | 目标可写且类型严格匹配才成功；检查 `false` |
| `takeBinding()` | 移除并返回现有 binding | Qt 6.1 起；移除后不再自动跟随 |
| `onValueChanged(f)` | 只监听后续变化 | 返回 handler 必须存活；调用可能延后 |
| `subscribe(f)` | 立即调用并持续监听 | 首次回调同步发生，需保证状态可用 |
| `addNotifier(f)` | 注册变化通知 | 返回 `QPropertyNotifier`，适合无模板成员保存 |
| `QMetaProperty::bindable(QObject *)` | 反射方式获取 bindable | 属性不支持 BINDABLE 时可能无效 |
| `QBindable<T>` | 类型明确的绑定接口 | 日常业务代码优先使用，能保留编译期类型检查 |
| `QUntypedPropertyBinding::valueMetaType()` | 查询 binding 结果类型 | 必须与目标 `metaType()` 相等才能安装 |

---

### 一句话总结

`QUntypedBindable` 让通用框架在不知道属性类型时管理 Qt 绑定；先区分有效、可绑定、只读和类型，再保存观察器返回值并严格检查 binding 的 `QMetaType` 匹配。
