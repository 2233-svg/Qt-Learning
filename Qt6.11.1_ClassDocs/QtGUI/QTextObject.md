# QTextObject
> Qt 6.11.1 · Qt GUI · 来自 `QTextObject`

## 1. 先建立直觉

`QTextObject` 是文档内部对象的基类，例如 frame、list、table、block group。它把对象格式和所属文档联系起来。应用代码更多使用具体子类，本类用于统一理解文档对象模型。

## 2. 类说明

- 头文件：`#include <QTextObject>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 派生：`QTextFrame`、`QTextBlockGroup` 等

对象由 `QTextDocument` 管理，不是普通业务 QObject。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `document()` | 所属文档 |
| `format()` | 对象格式 |
| `formatIndex()` | 内部格式索引 |
| `objectIndex()` | 文档内部对象索引 |

## 4. 关键用法

```cpp
QTextObject *obj = doc->object(objectIndex);
QTextFormat fmt = obj->format();
```

更常见的是拿到 `QTextFrame *` 或 `QTextList *` 后使用具体 API。

## 5. 使用场景

文档结构调试、根据 object index 定位对象、自定义导出器统一处理对象格式。

## 6. 常见坑与经验

- `QObject` 继承不代表你应自己管理 parent 生命周期，文档拥有这些对象。
- `formatIndex()` 是内部优化细节，普通业务不要依赖其稳定性。
- 实际操作请转向具体子类。

## 7. 知识点覆盖

文档对象模型、对象格式、内部索引、frame/list/table 共同基础。
