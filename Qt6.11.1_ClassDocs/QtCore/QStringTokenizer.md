# QStringTokenizer
> Qt 6.11.1 · Qt Core · 来自 `QStringTokenizer`

## 作用定位
`QStringTokenizer` 是惰性字符串分割器，按分隔符逐段产生视图，避免 `QString::split()` 立即分配整个列表。

## API 速查
| API | 是做什么的 |
|---|---|
| `qTokenize()` | 创建 tokenizer。 |
| `begin/end` | 范围 for 遍历片段。 |
| 分割行为选项 | 控制保留或跳过空片段。 |
| 视图返回 | 片段通常引用原字符串，不拥有数据。 |

## 使用场景
```cpp
for (QStringView part : qTokenize(line, u',', Qt::SkipEmptyParts))
    consume(part);
```

## 常见坑与经验
- 原始字符串必须比 tokenizer 和片段视图活得久。
- 需要长期保存片段时转换成 `QString`。
- CSV、转义和引号规则不能靠简单分割完整处理。

## 知识点覆盖
惰性分割、字符串视图、零拷贝、生命周期、CSV 边界。
