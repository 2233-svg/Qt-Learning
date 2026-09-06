# QQmlListProperty

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlListProperty` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlListProperty` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlListProperty>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

### 公有类型

- `AppendFunction`
- `AtFunction`
- `ClearFunction`
- `CountFunction`
- `RemoveLastFunction`
- `ReplaceFunction`

### 公有函数

- `QQmlListProperty(QObject *object, QList<T *> *list)`
- `QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at)`
- `QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear)`
- `QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear, QQmlListProperty<T>::ReplaceFunction replace, QQmlListProperty<T>::RemoveLastFunction removeLast)`
- `bool operator==(const QQmlListProperty<T> &other) const`

### 公开宏

- `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND`
- `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE`
- `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QQmlListProperty::AppendFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property, T *value)`的同义词。
请将`value`附在`property`列表后。

### `[alias] QQmlListProperty::AtFunction`

**作用与语义：**

`T *(*)(QQmlListProperty<T> *property, qsizetype index)`的同义词。
返回列表`property`中位置`index`的元素。

### `[alias] QQmlListProperty::ClearFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property)`的同义词。
清空名单，`property`。

### `[alias] QQmlListProperty::CountFunction`

**作用与语义：**

`qsizetype (*)(QQmlListProperty<T> *property)`的同义词。
返回列表中的元素数量`property`。

### `[alias] QQmlListProperty::RemoveLastFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property)`的同义词。
从列表中移除最后一个元素`property`。

### `[alias] QQmlListProperty::ReplaceFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property, qsizetype index, T *value)`的同义词。
将列表`property`中位置`index`的元素替换为`value`。

### `QQmlListProperty::QQmlListProperty(QObject *object, QList<T *> *list)`

**作用与语义：**

方便构造工具，用于从现有`QList` `list`中生成QQmlListProperty值。只要你持有指向该列表的QQmlListProperty，就必须提供并保持该列表及其`object` `list`的存续。
这是提供由`QList`支持的QQmlListProperty最简单且最安全的方式，在大多数情况下应使用。典型的调用如下：

**官方示例：**

```cpp
 QQmlListProperty<PieSlice> PieChart::slices()
 {
     return QQmlListProperty<PieSlice>(this, &m_slices);
 }
```

### `QQmlListProperty::QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at)`

**作用与语义：**

从一组操作函数 `count` 和 `at` 构造一个只读的 QQmlListProperty。可以传递一个不透明的 `data` 句柄，可以从操作函数内部访问。只要拥有该列表属性的`object`存在，列表属性依然有效。

### `QQmlListProperty::QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear)`

**作用与语义：**

从一组操作函数`append`、`count`、`at`和`clear`构造一个QQmlListProperty。可以传递一个不透明的`data`柄，可以从操作函数内部访问。只要拥有列表属性的`object`存在，列表属性就保持有效。
任何函数都可以传递空指针。如果传递了任何空指针，该列表将无法被调试器设计或修改。建议为所有函数提供有效的指针。
注意：最终的QQmlListProperty会综合removeLast()和replace（如果这些方法都给出了，`count`、`at`、`clear`和replace（`append`）。这很慢。如果你打算操作列表，除了清除它之外，应明确提供这些方法。

### `QQmlListProperty::QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear, QQmlListProperty<T>::ReplaceFunction replace, QQmlListProperty<T>::RemoveLastFunction removeLast)`

**作用与语义：**

从一组操作函数 `append`、`count`、`at`、`clear`、`replace` 和 removeLast 构造 QQmlListProperty。可以传递一个不透明度的 `data` 句柄，可以从操作函数内部访问。只要拥有该列表属性的 `object` 存在，列表属性依然有效。
可以传递任何函数的空指针，如果可能的话，使相应函数被合成为其他函数。QQmlListProperty 可以合成。
- `clear`使用`count`和`removeLast`
- `replace`使用`count`、`at`、`clear`和`append`
- `replace`使用`count`、`at`、`removeLast`和`append`
- `removeLast`使用`count`、`at`、`clear`和`append`
如果这些都给出了。这很慢，但如果你的列表本身没有为这些原语提供更快的选项，你可能想用合成的。
此外，如果`count`、`at`、`append`和`clear`中的任何一个都没有明确给出或合成，那么该列表将无法被调试器设计或修改。建议提供足够的有效指针以避免这种情况。

### `bool QQmlListProperty::operator==(const QQmlListProperty<T> &other) const`

**作用与语义：**

如果该`QQmlListProperty`等于 `other`，则返回真，否则为假。

### `void *QQmlListProperty::data`

**作用与语义：**

该字段可以存储任意数据指针。
如果你手动实现了访问器方法并需要存储自定义数据，可以将任意指针传递给`QQmlListProperty`构造函数，之后访问同一`QQmlListProperty`时从数据字段中取回。
由QList指针构建的QQmlListProperty使用该字段存储指向列表本身的指针，因为它无法直接访问所有者的列表内容。

### `QObject *QQmlListProperty::object`

**作用与语义：**

这块田地的主人是`QQmlListProperty`。
在手动实现访问器方法时，可能需要使用该字段来检索作列表的内容。

### `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND`

**作用与语义：**

该宏定义了该类列表属性的行为以进行附加。在赋值于衍生类型时，值会附加到基类的值上。这是默认行为。

**官方示例：**

```cpp
 class FruitBasket : QObject {
     Q_OBJECT
     QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND
     Q_PROPERTY(QQmlListProperty<Fruit> fruit READ fruit)

     public:
     // ...
     QQmlListProperty<Fruit> fruit();
     // ...
 };
```

### `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE`

**作用与语义：**

该宏定义了该类列表属性的行为以替换。在赋值于派生类型时，值会替换基类的值。

**官方示例：**

```cpp
 class FruitBasket : QObject {
     Q_OBJECT
     QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE
     Q_PROPERTY(QQmlListProperty<Fruit> fruit READ fruit)

     public:
     // ...
     QQmlListProperty<Fruit> fruit();
     // ...
 };
```

### `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT`

**作用与语义：**

该宏定义了该类列表属性的行为，即 ReplaceIfNotDefault。在赋值时，除非是默认属性，否则这些值会替换基类的值。对于默认属性，值会附加到基类的值上。

**官方示例：**

```cpp
 class FruitBasket : QObject {
     Q_OBJECT
     QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT
     Q_PROPERTY(QQmlListProperty<Fruit> fruit READ fruit)

     public:
     // ...
     QQmlListProperty<Fruit> fruit();
     // ...
 };
```

### `AppendFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property, T *value)`的同义词。
请将`value`附在`property`列表后。

### `AtFunction`

**作用与语义：**

`T *(*)(QQmlListProperty<T> *property, qsizetype index)`的同义词。
返回列表`property`中位置`index`的元素。

### `ClearFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property)`的同义词。
清空名单，`property`。

### `CountFunction`

**作用与语义：**

`qsizetype (*)(QQmlListProperty<T> *property)`的同义词。
返回列表中的元素数量`property`。

### `RemoveLastFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property)`的同义词。
从列表中移除最后一个元素`property`。

### `ReplaceFunction`

**作用与语义：**

`void (*)(QQmlListProperty<T> *property, qsizetype index, T *value)`的同义词。
将列表`property`中位置`index`的元素替换为`value`。

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

`QQmlListProperty` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
