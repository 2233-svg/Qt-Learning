# QQuickAttachedPropertyPropagator
> Qt 6.11.1 · Qt Quick Controls · 来自 `QQuickAttachedPropertyPropagator`

## 1. 先建立直觉

`QQuickAttachedPropertyPropagator` 是给“可沿 QML 对象层级传播的附加属性”用的基类。Quick Controls 里的主题、字体、调色板一类设置，经常不是每个控件都手写一份，而是从父层级向子层级传播；这个类提供的就是这种 attached-property 传播骨架。

普通应用很少直接用它。它更像是写控件库、样式系统、设计系统基础设施时会碰到的底层类。

## 2. 类说明

保留类说明：这些 API 来自 `QQuickAttachedPropertyPropagator`，属于 Qt Quick Controls 模块，用于附加属性对象之间的父子传播关系。

它不是视觉项，也不是 QObject 父子关系的替代品。`attachedParent()` 指的是“附加属性传播意义上的父对象”，而 `QObject::parent()` 仍然是内存和对象树意义上的父对象。两者经常相关，但不能混为一谈。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QQuickAttachedPropertyPropagator(QObject *parent = nullptr)` | 创建附加属性传播对象。 |
| `~QQuickAttachedPropertyPropagator()` | 销毁并脱离传播关系。 |
| `attachedParent() const` | 返回传播链上的父附加属性对象。 |
| `attachedChildren() const` | 返回传播链上的子附加属性对象列表。 |
| `attachedParentChange(newParent, oldParent)` | 传播父级变化时的虚函数钩子。 |
| `initialize()` | 在派生类构造完成必要默认值后，建立传播关系。 |

## 4. 典型流程

派生类通常会在构造函数里先建立自己的默认状态，再调用 `initialize()`：

```cpp
MyThemeAttached::MyThemeAttached(QObject *parent)
    : QQuickAttachedPropertyPropagator(parent)
{
    m_accent = defaultAccentColor();
    initialize();
}
```

当传播父级变化时，重写 `attachedParentChange()`，从新父级读取可继承值，并通知子级继续更新：

```cpp
void MyThemeAttached::attachedParentChange(
        QQuickAttachedPropertyPropagator *newParent,
        QQuickAttachedPropertyPropagator *oldParent)
{
    Q_UNUSED(oldParent);
    if (auto *theme = qobject_cast<MyThemeAttached *>(newParent))
        inheritFrom(theme);
}
```

## 5. 使用场景

| 场景 | 为什么会用到 |
| --- | --- |
| 自定义 Quick Controls 风格系统 | 颜色、字体、圆角、密度等设置需要沿控件树继承。 |
| 设计系统 QML 模块 | 页面设定一次 token，子控件自动获得默认值。 |
| 控件库内部附加属性 | 类似 `MyTheme.accent`、`MyTheme.density` 的 API 需要传播。 |
| 对 Qt Quick Controls 源码做扩展 | 需要理解 palette/font/style 传播时，这个类是关键拼图。 |

## 6. 常见坑与经验

`initialize()` 的调用时机很重要。太早调用，派生类默认值还没准备好，子对象可能继承到半初始化状态；太晚调用，父子关系和初始传播可能缺失。通常在派生类构造函数体末尾调用。

传播逻辑要避免环和重复通知。属性值没变就不要继续向外发 changed 信号；否则一棵 QML 树里几十个控件会被无意义刷新拖慢。

不要拿 `attachedChildren()` 当普通对象所有权列表使用。它表达的是传播拓扑，不代表你可以随便 delete 子对象，也不代表业务层父子关系。

QML 对象和 Quick Controls 相关对象通常属于 GUI 线程。把附加属性对象跨线程改值，可能让 binding、polish、布局和渲染阶段互相踩踏。

## 7. 知识点覆盖

- QML attached property 的 C++ 实现思路。
- Quick Controls 中属性继承与传播关系。
- `QObject` 父子关系和 attached parent 的区别。
- 派生类初始化顺序、变更通知和传播循环控制。
- 控件库/主题系统的底层扩展方式。
