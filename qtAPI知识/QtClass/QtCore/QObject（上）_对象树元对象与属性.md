# Qt QObject 深入笔记（上）：对象树、元对象与属性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QObject>`  
> 所属模块：`Qt6::Core`  
> 直接基类：无  
> 定位：绝大多数 Qt 对象的共同基类，是对象树、信号槽、事件、属性、反射和线程亲和性的基础

`QObject` 不是普通的“工具基类”。Qt 中许多看似独立的能力都在它身上汇合：父子对象自动销毁、信号槽连接、事件投递、动态属性、运行时类型信息、翻译上下文、定时器和线程归属。理解 `QObject`，才能正确判断 Qt 对象“由谁拥有、在哪个线程使用、何时销毁、如何通信”。

本类内容较多，拆为两篇：

- 上篇：对象树、元对象、属性、查找和运行时类型。
- 下篇：信号槽、事件、定时器、线程亲和性与安全销毁。

## 1. 最小可用代码

### 1.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 1.2 一个最小 QObject 子类

```cpp
#include <QCoreApplication>
#include <QObject>
#include <QString>

class Counter final : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)

public:
    explicit Counter(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

    int value() const { return m_value; }

    void setValue(int value)
    {
        if (m_value == value)
            return;
        m_value = value;
        emit valueChanged(m_value);
    }

signals:
    void valueChanged(int value);

private:
    int m_value = 0;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    Counter counter;
    QObject::connect(&counter, &Counter::valueChanged,
                     [](int value) { qInfo() << value; });
    counter.setValue(1);

    return 0;
}
```

`Q_OBJECT` 让 Meta-Object Compiler（moc）为类生成元对象代码。`Q_PROPERTY` 声明运行时可发现的属性，`signals` 声明信号。CMake 的 Qt 目标会自动配置 moc；不要手工运行 moc 或把生成文件复制进源码。

## 2. QObject 的能力地图

```text
QObject
├─ 对象身份：objectName、metaObject
├─ 所有权：parent、children、setParent
├─ 通信：connect、disconnect、signals、slots
├─ 事件：event、eventFilter、customEvent
├─ 生命周期：destroyed、deleteLater
├─ 属性：Q_PROPERTY、property、setProperty
├─ 线程：thread、moveToThread
├─ 定时器：startTimer、killTimer、timerEvent
└─ 国际化：tr
```

这些能力不是彼此孤立的。例如带 context 的连接会在 context 销毁时自动断开；事件只能由对象所属线程的事件循环处理；父子对象原则上必须位于同一线程。

## 3. 构造与析构

### 3.1 构造函数

```cpp
explicit QObject(QObject *parent = nullptr);
```

传入 `parent` 后，新对象会加入父对象的 `children()` 列表，并通常由父对象在析构时删除：

```cpp
QObject *root = new QObject;
QObject *child = new QObject(root);

delete root; // child 随 root 一起删除
```

“父对象删除子对象”是 QObject 对象树的所有权规则，不是垃圾回收。对象仍然使用确定性析构，裸指针也不会自动变成安全指针。

### 3.2 析构行为

`QObject::~QObject()` 会：

1. 删除对象的全部子对象。
2. 自动断开与该对象相关的信号槽连接。
3. 移除等待投递给该对象的事件。
4. 发出 `destroyed(QObject *)` 信号。

不要在析构过程中依赖子对象仍全部存在，也不要在 `destroyed` 的接收槽中调用对象的业务接口；此时对象正在销毁，只能把信号用于清理外部引用或记录状态。

## 4. 对象树与所有权

### 4.1 `parent()`、`children()` 与 `setParent()`

```cpp
QObject owner;
QObject *child = new QObject(&owner);

QObject *p = child->parent();
const QObjectList &list = owner.children();

child->setParent(nullptr); // 从对象树摘下，不会自动删除
delete child;
```

`children()` 返回内部列表的 const 引用，不要长期保存该引用并假设内容不变。子对象创建、重新设父对象和析构都会改变列表。

### 4.2 重新设父对象

```cpp
child->setParent(newOwner);
```

这会把对象从旧父对象的 children 列表移到新父对象。旧父对象不再负责它，新父对象将在析构时删除它。

必须注意：父对象与子对象应处于同一线程。跨线程 `setParent()` 会失败；要迁移对象，应先解除父子关系，再按线程规则调用 `moveToThread()`。

### 4.3 栈对象的顺序陷阱

安全写法：

```cpp
QObject parent;
QObject child(&parent);
```

C++ 按构造逆序析构，`child` 先析构并从父列表移除，随后 `parent` 析构。

危险写法：

```cpp
QObject child;
QObject parent;
child.setParent(&parent);
```

离开作用域时 `parent` 先析构，并试图 `delete` 栈上的 `child`，随后 C++ 还会再次析构 `child`。不要把先构造的栈对象后来设成后构造栈对象的子对象。

### 4.4 对象树不等于 C++ 成员关系

```cpp
class Controller : public QObject
{
    Q_OBJECT
    Worker m_worker; // 值成员，C++ 自动析构
};
```

值成员不需要再以 `this` 为 QObject parent。成员自身由 C++ 对象生命周期管理；同时设置 QObject 父对象会引入双重销毁风险。对象树主要用于堆对象和动态 UI/服务对象。

## 5. `Q_OBJECT` 与 moc

### 5.1 它提供什么

`Q_OBJECT` 展开后配合 moc 生成：

- 信号实现和槽元数据。
- `staticMetaObject`。
- `metaObject()`、`qt_metacast()`、`qt_metacall()` 等支持。
- `tr()` 的类上下文。
- 属性、枚举和可调用方法的反射信息。

```cpp
class Device : public QObject
{
    Q_OBJECT
public:
    using QObject::QObject;

signals:
    void connected();
};
```

### 5.2 常见构建错误

出现 `undefined reference to vtable`、`unresolved external symbol staticMetaObject` 等问题时，检查：

1. 包含 `Q_OBJECT` 的头文件是否属于目标源文件。
2. 是否使用 Qt CMake API并启用了自动 moc。
3. 修改类后是否重新运行 CMake。
4. `Q_OBJECT` 是否放在模板类、局部类等 moc 不支持的位置。

### 5.3 `Q_GADGET` 不是 QObject

纯值类型若只需要枚举或属性元数据，可以使用 `Q_GADGET`。它没有对象树、信号槽和线程亲和性，不能替代 QObject，也不需要 QObject 指针身份。

## 6. 元对象：`metaObject()` 与 `staticMetaObject`

```cpp
const QMetaObject *mo = object->metaObject();
qDebug() << mo->className();
qDebug() << mo->methodCount();
qDebug() << mo->propertyCount();
```

`metaObject()` 返回对象实际动态类型的元对象；`MyType::staticMetaObject` 表示编译期类元对象。元对象形成和 C++ 继承相对应的父链。

枚举属性：

```cpp
for (int i = mo->propertyOffset(); i < mo->propertyCount(); ++i) {
    const QMetaProperty property = mo->property(i);
    qDebug() << property.name() << property.typeName();
}
```

`propertyOffset()` 跳过基类属性，只遍历当前类新增部分。遍历全部属性则从 0 开始。

## 7. 静态属性 `Q_PROPERTY`

```cpp
Q_PROPERTY(QString name
           READ name
           WRITE setName
           NOTIFY nameChanged
           FINAL)
```

常见组成：

- `READ`：读取函数。
- `WRITE`：写入函数。
- `NOTIFY`：属性变化信号。
- `MEMBER`：直接指定成员变量。
- `RESET`：恢复默认值。
- `CONSTANT`：对象生命周期内不变。
- `FINAL`：派生类不应覆盖。
- `BINDABLE`：暴露 Qt Bindable Property。

setter 应只在值真正改变时发出 NOTIFY：

```cpp
void Device::setName(const QString &name)
{
    if (m_name == name)
        return;
    m_name = name;
    emit nameChanged(m_name);
}
```

重复发信号会让 QML 绑定、模型和业务槽进行无意义更新，甚至形成反馈循环。

## 8. `objectName` 与可绑定属性

`QObject` 自带 `objectName` 属性：

```cpp
object->setObjectName("networkController");
qDebug() << object->objectName();

connect(object, &QObject::objectNameChanged,
        [](const QString &name) { qDebug() << name; });
```

Qt 6 还提供：

```cpp
QBindable<QString> binding = object->bindableObjectName();
```

`objectName` 常用于 Designer、测试查找、调试和对象树定位，不应代替业务主键。名称可以为空，也不保证全局唯一。

## 9. 统一属性访问：`property()` 与 `setProperty()`

```cpp
QVariant value = object->property("name");
const bool declaredProperty = object->setProperty("name", "sensor-A");
```

对声明在元对象中的属性，`setProperty()` 会调用对应写入路径；返回值表示是否成功设置了已声明属性。

Qt 6.6 起还提供接收右值 `QVariant` 的重载，适合转移较大值：

```cpp
object->setProperty("payload", QVariant::fromValue(std::move(data)));
```

## 10. 动态属性

属性名未在元对象中声明时，`setProperty()` 会创建动态属性，通常返回 `false`，但值仍被保存：

```cpp
object->setProperty("requestId", 42);
qDebug() << object->property("requestId").toInt();

for (const QByteArray &name : object->dynamicPropertyNames())
    qDebug() << name;
```

把无效 `QVariant` 设给动态属性可删除它：

```cpp
object->setProperty("requestId", QVariant());
```

动态属性适合测试标签、插件元数据和临时扩展，但缺少编译期类型检查。稳定业务数据应使用正式 `Q_PROPERTY` 或明确成员。

动态属性变化会产生 `QDynamicPropertyChangeEvent`，可在 `event()` 或事件过滤器中观察。

## 11. 查找子对象

### 11.1 `findChild<T>()`

```cpp
QPushButton *saveButton =
    window.findChild<QPushButton *>("saveButton");
```

默认递归查找后代，并返回第一个匹配类型和名称的对象。若名称为空或省略，只按类型查找：

```cpp
auto *button = window.findChild<QPushButton *>();
```

### 11.2 `findChildren<T>()`

```cpp
const QList<QLineEdit *> edits =
    window.findChildren<QLineEdit *>(
        QAnyStringView{}, Qt::FindDirectChildrenOnly);
```

可用 `Qt::FindDirectChildrenOnly` 限制直接子项，或默认使用 `Qt::FindChildrenRecursively`。还可以按 `QRegularExpression` 匹配对象名。

查找适合测试、Designer 对象和松耦合扩展。频繁业务路径应保存明确指针，避免每次遍历对象树。

## 12. 运行时类型判断

### 12.1 `qobject_cast`

```cpp
QObject *object = obtainObject();
if (auto *button = qobject_cast<QPushButton *>(object))
    button->click();
```

`qobject_cast` 基于 Qt 元对象，不依赖 C++ RTTI；目标类需要相应 Qt 元对象声明。它是 QObject 层级最常用的安全向下转换。

### 12.2 `inherits()`

```cpp
if (object->inherits("QAbstractButton"))
    qDebug() << "button-like object";
```

`inherits()` 使用字符串类名，重构不安全，主要用于插件、脚本和调试。普通 C++ 代码优先 `qobject_cast`。

### 12.3 快速类别判断

```cpp
object->isWidgetType();
object->isWindowType();
object->isQuickItemType();
object->isQmlExposed();
```

这些函数针对特定 Qt 类别进行了快速判断。`isWidgetType()` 不等于对象当前可见，`isWindowType()` 也不说明它是顶层 QWidget；它们只描述类型类别。

## 13. QObject 禁止复制

`QObject` 使用 `Q_DISABLE_COPY` 禁止复制构造和赋值：

```cpp
QObject a;
// QObject b = a; // 编译错误
```

原因是 QObject 具有稳定身份：连接、父子关系、线程归属、事件队列和动态属性都绑定到这个身份。复制这些关系没有清晰语义。

容器中通常保存指针：

```cpp
QList<QPointer<QObject>> objects;
```

需要可复制业务数据时，把数据提取为值类型结构体，QObject 只负责生命周期和通信。

## 14. 调试对象树

```cpp
object->dumpObjectInfo();
object->dumpObjectTree();
```

`dumpObjectInfo()` 输出当前对象的连接等信息，`dumpObjectTree()` 输出子树。它们适合临时诊断，不应解析其文本输出作为业务协议。

为关键对象设置有意义的 `objectName`，调试输出会更容易定位：

```cpp
controller->setObjectName("main/networkController");
```

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与所有权 | `QObject(QObject *parent = nullptr)` | 构造一个带 Qt 对象身份的基类对象；传入 parent 后加入父对象的对象树 | parent 是 QObject 所有权，不是 C++ 基类；栈对象不要随意后来设置成另一个栈对象的子对象 |
| 构造与所有权 | `~QObject()` | 析构对象，删除子对象并清理连接、事件和动态属性 | 不要在析构期间依赖子对象仍完整存在；跨线程销毁不要直接 `delete` |
| 对象树 | `parent()` | 返回当前 QObject 的父对象 | 返回值为空表示没有 Qt 父对象；它与 C++ 继承关系无关 |
| 对象树 | `children()` | 返回直接子对象列表 | 列表会随着添加、换父对象和析构变化，不要长期缓存并假定不变 |
| 对象树 | `setParent(QObject *)` | 把对象从旧父对象移到新父对象，改变 Qt 所有权 | 新旧父对象必须满足同线程规则；设为 `nullptr` 只会摘出对象，不会删除它 |
| 元对象系统 | `Q_OBJECT` | 为 QObject 子类启用信号槽、元对象、属性、枚举和翻译上下文等能力 | 需要 moc 生成代码；缺少构建配置时常见结果是 vtable 或 `staticMetaObject` 链接错误 |
| 元对象系统 | `metaObject()` | 获取对象运行时实际类型的 `QMetaObject` | 通过基类指针调用时仍能得到动态类型；元对象指针不由调用者删除 |
| 元对象系统 | `staticMetaObject` | 获取某个类的编译期类级元对象 | 不需要对象实例；只描述声明了元对象信息的类 |
| 元对象系统 | `Q_PROPERTY(...)` | 在元对象中声明可读写、可通知或可绑定的静态属性 | `NOTIFY` 应只在值真正变化时发出，否则会造成无意义更新或绑定反馈 |
| 元对象系统 | `property(const char *)` | 按名字读取静态属性或动态属性，结果以 `QVariant` 返回 | 名字不存在时得到无效 `QVariant`；动态访问失去编译期类型检查 |
| 元对象系统 | `setProperty(const char *, const QVariant &)` | 按名字写入声明属性，或创建/修改动态属性 | 返回值主要表示是否找到了声明属性；写入动态属性时可能返回 `false` 但值仍已保存 |
| 属性绑定 | `objectName()` / `setObjectName(const QString &)` | 读取或修改 QObject 自带的对象名称 | 适合调试、Designer、测试查找和对象树定位；名称为空且不保证唯一 |
| 属性绑定 | `objectNameChanged(const QString &)` | 在 `objectName` 改变后通知观察者 | 只表示名称变化，不代表对象树或业务主键变化 |
| 属性绑定 | `bindableObjectName()` | 获取 `objectName` 对应的 `QBindable<QString>` | 用于 Qt 属性绑定；不要把绑定接口当作普通字符串存储 |
| 动态属性 | `dynamicPropertyNames()` | 枚举当前对象上运行时添加的动态属性名 | 适合插件标签、测试元数据等临时扩展；稳定业务字段应声明为 `Q_PROPERTY` |
| 子对象查找 | `findChild<T>(...)` | 在对象树中按类型和可选名称查找一个后代对象 | 默认递归并返回第一个匹配项；频繁业务路径应保存明确指针，避免反复遍历 |
| 子对象查找 | `findChildren<T>(...)` | 查找多个指定类型的后代对象，可按名称或正则过滤 | 可用 `Qt::FindDirectChildrenOnly` 限制为直接子项；对象树变化后结果需重新获取 |
| 运行时类型 | `qobject_cast<T *>(QObject *)` | 基于 Qt 元对象安全地向下转换 QObject 指针 | 目标类型需要可用的元对象信息；普通 C++ 代码优先它，而不是字符串比较 |
| 运行时类型 | `inherits(const char *)` | 按类名字符串判断对象是否继承自某个 QObject 类型 | 适合插件、脚本和诊断；类名重构不会被编译器检查 |
| 运行时类型 | `isWidgetType()` / `isWindowType()` / `isQuickItemType()` / `isQmlExposed()` | 快速判断对象是否属于特定 Qt 类型类别 | 它们判断的是类型类别，不代表对象当前可见、已经显示或一定能直接操作 |
| 调试 | `dumpObjectInfo()` | 输出对象自身的调试信息和连接概况 | 输出格式面向人阅读，不要解析文本作为业务协议 |
| 调试 | `dumpObjectTree()` | 输出当前对象及其子对象树 | 给关键对象设置有意义的 `objectName` 后更容易定位问题 |

下篇继续讲 `connect`/`disconnect` 的所有重载和连接类型、事件过滤、基础定时器、`moveToThread()`、`deleteLater()`、`destroyed()` 以及多线程生命周期陷阱。
