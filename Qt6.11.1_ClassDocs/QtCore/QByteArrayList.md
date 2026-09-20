# QByteArrayList
> Qt 6.11.1 · Qt Core · 来自 `QByteArrayList`

## 作用定位
`QByteArrayList` 是 `QList<QByteArray>` 的便利别名，补充了常用连接和过滤操作。

## API 速查
| API | 是做什么的 |
|---|---|
| `join()` | 用分隔符拼接全部字节串。|
| `filter()` | 按包含关系过滤。|
| `replaceInStrings()` | 批量替换内容。|

## 使用场景
处理 HTTP 头行、命令参数字节串、协议字段列表。

## 常见坑与经验
- `join()` 会创建完整副本，大量或大字段应避免多次拼接。

## 知识点覆盖
字节列表、批量文本处理、拼接成本、隐式共享。
