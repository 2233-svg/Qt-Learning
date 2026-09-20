# QDomCharacterData
> Qt 6.11.1 · Qt XML · 来自 `QDomCharacterData`

## 1. 先建立直觉

`QDomCharacterData` 是文本类节点的共同基类。普通文本 `QDomText`、CDATA、注释都属于“字符数据”：它们不管理标签和属性，只管理一段字符串，以及对这段字符串的追加、插入、删除、替换、截取。

## 2. 类说明

保留类说明：这些 API 来自 `QDomCharacterData`，属于 Qt XML 模块，用于操作 DOM 字符数据节点的文本内容。

它继承 `QDomNode`，但比通用节点多了面向字符串的接口。一般通过具体派生类使用，而不是直接创建它。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `data()` / `setData()` | 读取或替换完整字符数据。 |
| `length()` | 返回字符数。 |
| `substringData(offset, count)` | 截取子串。 |
| `appendData(arg)` | 追加文本。 |
| `insertData(offset, arg)` | 在指定位置插入文本。 |
| `deleteData(offset, count)` | 删除一段文本。 |
| `replaceData(offset, count, arg)` | 替换一段文本。 |

## 4. 典型流程

```cpp
QDomText text = doc.createTextNode("hello");
QDomCharacterData data = text.toCharacterData();
data.appendData(" world");
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 修改文本节点内容 | `setData()` 或 replace/append。 |
| 清理注释或 CDATA | 转成 character data 后统一处理。 |
| 编写 DOM 文本编辑工具 | offset/count 操作比手动替换节点更直接。 |

## 6. 常见坑与经验

offset 和 count 按 Qt 字符串索引理解，不是 XML 字节偏移。包含非 ASCII 字符时不要用原文件字节位置直接套用。

字符数据节点的含义由具体类型决定。同样是字符串，Text 会被正常 XML 转义，CDATA 会以 CDATA 形式输出，Comment 则是注释内容。

## 7. 知识点覆盖

- DOM 字符数据基类。
- 文本内容的局部编辑。
- Text、CDATA、Comment 的共同点和输出差异。
