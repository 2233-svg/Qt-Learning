# Qt QDomDocument::ParseResult 深入笔记：`setContent()` 的结构化解析结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomDocument>`  
> 所属模块：`Qt6::Xml`  
> 引入版本：Qt 6.5  
> 类型性质：轻量结果结构体，不是 DOM 节点。

`QDomDocument::ParseResult` 是 Qt 6.5 起 `QDomDocument::setContent()` 返回的结构化解析结果。它把旧 API 中分散的 `bool`、错误字符串、错误行和错误列收在一个值对象里。

它解决的是“解析 XML 时，如何既方便判断成功，又能在失败时拿到可记录、可定位的诊断信息”。

```cpp
QDomDocument document;
QDomDocument::ParseResult result = document.setContent(xmlBytes);

if (!result) {
    qWarning().noquote()
        << "XML parse error at"
        << result.errorLine << ":" << result.errorColumn
        << result.errorMessage;
    return;
}
```

## 1. 成功与失败的唯一判断规则

`ParseResult` 支持显式转换为 `bool`：

```cpp
if (document.setContent(xml)) {
    // 解析成功
}
```

它的规则非常直接：`errorMessage` 为空时，转换为 `true`；非空时，转换为 `false`。因此不要自行发明“行号为 0 就成功”或“列号大于 0 才失败”之类的判断，先使用 `if (!result)`。

## 2. 失败日志该记录什么

解析失败时，至少保留：

- `errorMessage`：人类可读的失败原因。
- `errorLine`：解析器报告的位置行。
- `errorColumn`：解析器报告的位置列。

真实项目里还应在日志中带上 XML 来源，例如文件路径、资源名、请求 URL 或配置项名称。只有“第 12 行第 8 列”通常不足以知道到底是哪一份输入坏了。

```cpp
const auto result = document.setContent(&file);
if (!result) {
    qWarning().noquote()
        << file.fileName()
        << "line" << result.errorLine
        << "column" << result.errorColumn
        << result.errorMessage;
}
```

对于 `QIODevice *` 重载，应用应在调用前自行以只读方式打开设备。Qt 6.11.1 仍会尝试打开未打开的 device，但 Qt 文档说明 Qt 7 将不再这样做，主动打开设备能避免版本升级时行为改变。

## 3. 它只报告解析，不保证业务有效

`ParseResult` 成功意味着 XML 已按当前 `ParseOptions` 解析为 DOM，不代表：

- 必填业务字段都存在。
- 属性值符合你的业务范围。
- XML 通过 XSD、DTD 或其他外部规范验证。
- 命名空间、空白文本节点的处理方式符合你的业务期望。

解析成功后仍应继续检查根元素、必填属性、元素顺序和业务约束。`ParseResult` 是语法和 DOM 建树的第一道门，不是完整的数据校验报告。

## 4. 与 `ParseOptions` 的配合

`setContent()` 的返回类型是 `ParseResult`，解析选项属于 `QDomDocument::ParseOptions`：

- 默认不启用命名空间处理。
- `UseNamespaceProcessing` 启用 namespace 解析。
- `PreserveSpacingOnlyNodes` 保留只含空白的文本节点。

错误处理逻辑不因选项而改变：先检查 `ParseResult`，成功后再按所选选项读取节点的 namespace、local name 或空白文本。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结果字段 | `errorMessage` | 保存解析失败的人类可读原因 | `operator bool()` 就以它是否为空判断成功；失败日志应原样保留 |
| 结果字段 | `errorLine` | 保存解析器报告的错误行位置 | 仅在失败诊断中使用；结合输入来源一起记录才便于定位 |
| 结果字段 | `errorColumn` | 保存解析器报告的错误列位置 | 与 `errorLine` 配合查看，不要单独代替成功判断 |
| 成功判断 | `explicit operator bool() const noexcept` | 当 `errorMessage` 为空时返回 `true` | 使用 `if (result)` 或 `if (!result)`；这是唯一应优先采用的成功判断 |

---

### 一句话总结

`QDomDocument::ParseResult` 让 `setContent()` 的失败信息不再散落在多个输出参数中。先用它的布尔转换判断解析是否成功，失败时记录来源、错误文本、行号和列号；成功后再进入业务层校验。
