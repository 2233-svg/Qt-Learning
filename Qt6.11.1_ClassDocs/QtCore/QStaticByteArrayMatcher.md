# QStaticByteArrayMatcher
> Qt 6.11.1 · Qt Core · 来自 `QStaticByteArrayMatcher`

## 作用定位
`QStaticByteArrayMatcher` 为编译期已知的字节模式构建快速搜索器，用来在 `QByteArrayView` 或原始字节范围中查找固定片段。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造宏/辅助形式 | 以静态字节字面量创建 matcher。 |
| `indexIn()` | 在目标字节序列中查找首次出现位置。 |
| `pattern()` | 查询被匹配的固定模式。 |

## 使用场景
协议解析中反复查找固定分隔符，如 `"\r\n\r\n"`、魔数或帧头。

## 常见坑与经验
- 它处理字节，不理解文本编码和大小写。
- 模式适合静态常量；运行时模式用 `QByteArrayMatcher`。
- 返回位置是字节偏移，不是 Unicode 字符索引。

## 知识点覆盖
字节搜索、协议分隔符、静态模式、编码边界、偏移量。
