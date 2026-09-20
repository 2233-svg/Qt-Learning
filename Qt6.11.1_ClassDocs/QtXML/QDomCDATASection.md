# QDomCDATASection
> Qt 6.11.1 · Qt XML · 来自 `QDomCDATASection`

## 1. 先建立直觉

`QDomCDATASection` 表示 XML 的 CDATA 区块：`<![CDATA[ ... ]]>`。它适合保存大段不想按普通文本频繁转义的内容，例如脚本片段、模板文本或包含很多 `<`、`&` 的原样字符串。

## 2. 类说明

保留类说明：这些 API 来自 `QDomCDATASection`，属于 Qt XML 模块，用于表示 CDATA 字符数据节点。

它继承 `QDomText`，再由 `nodeType()` 区分为 `CDATASectionNode`。创建含内容的节点应使用 `QDomDocument::createCDATASection()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QDomCDATASection()` | 创建空 CDATA 句柄。 |
| `nodeType()` | 返回 `CDATASectionNode`。 |
| 继承的 `data()` / `setData()` | 读取或设置 CDATA 内容。 |

## 4. 典型流程

```cpp
QDomElement script = doc.createElement("script");
script.appendChild(doc.createCDATASection("if (a < b && c > d) run();"));
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 保存代码或表达式 | 避免大量 XML 转义影响可读性。 |
| 保存模板片段 | 原样内容比普通 text node 更清楚。 |
| 与旧 XML 格式兼容 | 某些格式约定大段文本放 CDATA。 |

## 6. 常见坑与经验

CDATA 不是安全沙箱。里面的内容仍是字符串，只是 XML 解析方式不同；真正执行脚本或解释模板前仍要做安全检查。

CDATA 内容不能直接包含 `]]>` 结束序列。需要保存这种内容时，要拆分多个 CDATA 节点或改用普通文本转义。

## 7. 知识点覆盖

- CDATA 与普通文本节点的区别。
- CDATA 创建、读取、序列化。
- `]]>` 边界和安全误区。
