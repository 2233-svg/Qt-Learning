# QDomProcessingInstruction
> Qt 6.11.1 · Qt XML · 来自 `QDomProcessingInstruction`

## 1. 先建立直觉

`QDomProcessingInstruction` 表示 XML 处理指令，例如 `<?xml-stylesheet type="text/xsl" href="style.xsl"?>`。它不是普通元素，而是给处理器的附加指令。

## 2. 类说明

保留类说明：这些 API 来自 `QDomProcessingInstruction`，属于 Qt XML 模块，用于表示 XML 处理指令节点。

处理指令有两个关键部分：`target()` 是指令目标，`data()` 是目标后面的内容。创建含内容的处理指令应使用 `QDomDocument::createProcessingInstruction()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `target()` | 返回处理指令目标。 |
| `data()` / `setData()` | 读取或设置处理指令数据。 |
| `nodeType()` | 返回 `ProcessingInstructionNode`。 |

## 4. 典型流程

```cpp
auto pi = doc.createProcessingInstruction(
    "xml-stylesheet",
    "type=\"text/xsl\" href=\"style.xsl\"");
doc.insertBefore(pi, doc.documentElement());
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| XML 样式表声明 | `xml-stylesheet`。 |
| 兼容旧 XML 工作流 | 某些处理器读取 PI 控制行为。 |
| 文档转换工具 | 保留或重写处理指令。 |

## 6. 常见坑与经验

处理指令不是元素，不能用 `elementsByTagName()` 找。要遍历节点并检查 `nodeType()`。

`data()` 通常是一段约定格式字符串，Qt DOM 不会帮你解析其中的伪属性。需要自己按目标规范解析。

## 7. 知识点覆盖

- XML 处理指令的 target/data 结构。
- PI 与元素节点的区别。
- 样式表和旧 XML 处理管线。
