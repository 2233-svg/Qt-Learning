# QQmlPropertyMap

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlPropertyMap` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlPropertyMap` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlPropertyMap>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `virtual ~QQmlPropertyMap() override`
- `void clear(const QString &key)`
- `bool contains(const QString &key) const`
- `int count() const`
- `(since 6.1) void freeze()`
- `(since 6.1) void insert(const QVariantHash &values)`
- `void insert(const QString &key, const QVariant &value)`
- `bool isEmpty() const`
- `QStringList keys() const`
- `int size() const`
- `QVariant value(const QString &key) const`
- `QVariant & operator[](const QString &key)`
- `QVariant operator[](const QString &key) const`

### 信号

- `void valueChanged(const QString &key, const QVariant &value)`

### 静态公有成员

- `QQmlPropertyMap * create(QObject *parent = nullptr)`

### 保护函数

- `QQmlPropertyMap(DerivedType *derived, QObject *parent)`
- `virtual QVariant updateValue(const QString &key, const QVariant &input)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[protected] template <typename DerivedType> QQmlPropertyMap::QQmlPropertyMap(DerivedType *derived, QObject *parent)`

**作用与语义：**

构造一个带有父对象`parent`的可绑定映射。在从 QQmlPropertyMap 派生的类中使用此构造器。
`derived`类型用于向元对象系统注册属性映射，这对于确保派生类的属性可访问至关重要。该类型必须从 QQmlPropertyMap 派生。
在C文件中：
然后，`main.qml`：

**官方示例：**

```cpp
 class MyQmlPropertyMap : public QQmlPropertyMap
 {
     Q_OBJECT
     QML_NAMED_ELEMENT(MyQmlPropertyMap)
 public:
     explicit MyQmlPropertyMap(QObject *parent = nullptr)
         : QQmlPropertyMap(this, parent)
     {
         insert("name", "John Smith");
         insert("phone", "555-5555");
         insert("email", "john.smith@example.com");
     }

 public slots:
     void updateEmail(const QString &newEmail)
     {
         insert("email", newEmail);
     }
 };
     QQuickView view;
     view.setSource(QUrl("qrc:/main.qml"));
     view.show();
```

### `[override virtual noexcept] QQmlPropertyMap::~QQmlPropertyMap()`

**作用与语义：**

摧毁可绑定的地图。

### `void QQmlPropertyMap::clear(const QString &key)`

**作用与语义：**

清除与`key`相关的价值（如果有的话）。

### `bool QQmlPropertyMap::contains(const QString &key) const`

**作用与语义：**

如果映射包含`key`，则返回真。

### `int QQmlPropertyMap::count() const`

**作用与语义：**

和`size()`一样。

### `[static] QQmlPropertyMap *QQmlPropertyMap::create(QObject *parent = nullptr)`

**作用与语义：**

创建一个带有父对象`parent`的可绑定映射。

### `[since 6.1] void QQmlPropertyMap::freeze()`

**作用与语义：**

禁止向该属性图添加任何其他属性。现有属性可以被修改或清除。
相应地，为现有属性开启内部缓存，这可能带来更快的QML访问。

### `[since 6.1] void QQmlPropertyMap::insert(const QVariantHash &values)`

**作用与语义：**

将`values`插入`QQmlPropertyMap`。
不存在的密钥会自动生成。
这种方法比连续多次调用`insert(key, value)`快得多。

### `void QQmlPropertyMap::insert(const QString &key, const QVariant &value)`

**作用与语义：**

将`key`关联的值设置为`value`。
如果密钥不存在，它会自动生成。

### `bool QQmlPropertyMap::isEmpty() const`

**作用与语义：**

如果映射中没有键，则返回为真;否则返回为假。

### `[invokable] QStringList QQmlPropertyMap::keys() const`

**作用与语义：**

返回密钥列表。
已被清除的键仍会出现在列表中，尽管其关联值是无效的QVariant。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `int QQmlPropertyMap::size() const`

**作用与语义：**

返回地图中的键数。

### `[virtual protected] QVariant QQmlPropertyMap::updateValue(const QString &key, const QVariant &input)`

**作用与语义：**

返回键`key`要存储的新值。该函数用于拦截QML中属性的更新，其中QML提供的值为`input`。
覆盖该函数以在属性值更新时操作。注意，该函数仅在从 QML 更新值时调用。

### `QVariant QQmlPropertyMap::value(const QString &key) const`

**作用与语义：**

返回与`key`相关的值。
如果该键未设置值（或值已被清除），则返回无效`QVariant`。

### `[signal] void QQmlPropertyMap::valueChanged(const QString &key, const QVariant &value)`

**作用与语义：**

每当映射中的某个值发生变化时，该信号就会发出。`key` 是对应被更改`value`的密钥。
注意：当调用 `insert()` 或 `clear()` 进行更改时，不会发出 valueChanged() ——只有从 QML 更新值时才会发出。

### `QVariant &QQmlPropertyMap::operator[](const QString &key)`

**作用与语义：**

返回与密钥`key`关联的值作为可修改的引用。
如果映射中没有关键字`key`的项，函数会在关键字`key`的映射中插入一个无效的`QVariant`，并返回该项的引用。

### `QVariant QQmlPropertyMap::operator[](const QString &key) const`

**作用与语义：**

和`value()`一样。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQmlPropertyMap` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
