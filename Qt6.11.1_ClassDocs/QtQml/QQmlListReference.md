# QQmlListReference
> Qt 6.11.1 · Qt QML · 来自 `QQmlListReference`

## 作用定位

`QQmlListReference` 是运行期操作 QML list property 的工具。`QQmlListProperty<T>` 用来“声明列表属性”，`QQmlListReference` 用来“拿到某个对象的列表属性后读写它”。

它适合通用编辑器、测试工具、动态对象构建器。

## 类说明

- 头文件：`#include <QQmlListReference>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 构造：从 QObject+属性名，或 Qt 6.1 起从 QVariant 构造

## API 速查

| API | 说明 |
| --- | --- |
| `isValid()` | 是否定位到合法 list property。 |
| `isReadable()` / `isManipulable()` | 能否读取或修改。 |
| `canAppend()` / `canAt()` / `canCount()` | 是否支持添加、索引访问、计数。 |
| `canClear()` / `canReplace()` / `canRemoveLast()` | 是否支持清空、替换、删除末尾。 |
| `append()` | 向列表追加 QObject。 |
| `at(index)` | 读取指定元素。 |
| `count()` / `size()` | 返回元素数量。 |
| `clear()` | 清空列表。 |
| `replace(index, object)` | 替换元素。 |
| `removeLast()` | 删除末尾元素。 |
| `listElementType()` | 返回元素类型元对象。 |
| `object()` | 返回宿主对象。 |
| `operator==` | 比较引用是否相同。 |

## 使用场景

- 运行期把子对象追加到某个 QML 容器属性。
- 属性编辑器读取任意 QObject 的 list property。
- 自动化测试检查 QML 子对象列表。
- 从 QVariant 里拿到 list property 后继续操作。

## 常见坑与经验

- 操作前先检查能力函数；不是每个 list property 都支持清空、替换或删除。
- `append()` 不一定自动设置 parent，取决于列表属性实现；需要了解宿主类型的协议。
- 元素类型要匹配 `listElementType()`，否则 append/replace 可能失败。
- `isReadable()` 不代表可修改，修改前看 `isManipulable()` 和具体 can*。
- 如果底层对象销毁，引用会失效，不要长期缓存。

## 知识点覆盖

- 运行期访问 QML list property
- 列表属性能力查询
- QObject 元类型匹配
- 运行期编辑器和测试工具场景
