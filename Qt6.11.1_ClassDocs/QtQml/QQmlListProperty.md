# QQmlListProperty
> Qt 6.11.1 · Qt QML · 来自 `QQmlListProperty`

## 作用定位

`QQmlListProperty<T>` 用来把 C++ 对象中的“QObject 子对象列表”声明为 QML 可写的 list property。QML 里常见的：

```qml
Container {
    Item {}
    Item {}
}
```

背后就需要类似的列表属性协议，让 QML 引擎知道怎么 append、count、at、clear、replace、removeLast。

## 类说明

- 头文件：`#include <QQmlListProperty>`
- CMake：链接 `Qt6::Qml`
- 模板参数：列表元素 QObject 派生类型
- 用途：写在 `Q_PROPERTY(QQmlListProperty<T> items READ items)` 中

## API 速查

| API | 说明 |
| --- | --- |
| `AppendFunction` | QML 添加元素时调用。 |
| `CountFunction` | 返回元素数量。 |
| `AtFunction` | 按索引返回元素。 |
| `ClearFunction` | 清空列表。 |
| `ReplaceFunction` | 替换指定索引元素。 |
| `RemoveLastFunction` | 删除最后一个元素。 |
| `QQmlListProperty(object, QList<T*> *list)` | 直接用现成 QList 暴露，适合简单场景。 |
| 带函数指针构造 | 完全自定义列表访问和修改行为。 |
| `object` / `data` | 回调中的宿主对象和自定义数据指针。 |
| `operator==` | 比较两个列表属性是否指向同一协议。 |
| `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND` | QML 赋值时追加。 |
| `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE` | QML 赋值时替换。 |
| `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT` | 非默认列表时替换。 |

## 典型写法

```cpp
Q_PROPERTY(QQmlListProperty<Page> pages READ pages)

QQmlListProperty<Page> Book::pages()
{
    return QQmlListProperty<Page>(this, &m_pages);
}
```

复杂场景则提供静态回调，便于控制 parent、去重、通知信号和存储结构。

## 使用场景

- QML 容器组件暴露子项列表。
- C++ 类型希望支持 QML 嵌套对象语法。
- 列表底层不是 QList，需要自定义访问逻辑。

## 常见坑与经验

- 列表元素通常应设置合适 parent，否则 QML 创建的子对象生命周期容易失控。
- QML list property 不是 `QList<T*>` 直接暴露，而是一个回调协议。
- 如果不提供 replace/removeLast，某些 QML 赋值或编辑行为会受限。
- 列表变化如果需要通知外部，仍要自己设计 NOTIFY 信号或模型接口。
- 大型、可变、带角色的数据集合更适合 `QAbstractItemModel`，不是 list property。

## 知识点覆盖

- QML 默认属性和嵌套对象
- QObject 列表属性协议
- append/count/at/clear/replace/removeLast 回调
- QML list property 赋值行为
- 生命周期和 parent 管理
