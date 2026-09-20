# QStringList
> Qt 6.11.1 · Qt Core · 来自 `QStringList`

## 作用定位
`QStringList` 是字符串列表，适合命令行参数、过滤条件、路径集合、CSV 简单字段和 UI 选项。它继承顺序容器能力，并增加文本相关工具。

## API 速查
| API | 是做什么的 |
|---|---|
| `join()` | 用分隔符拼接。 |
| `filter()` | 按文本或正则筛选。 |
| `replaceInStrings()` | 批量替换每个字符串。 |
| `sort()` | 排序列表。 |
| `removeDuplicates()` | 去重并保留第一次出现。 |
| 继承的 `append/insert/remove` | 管理列表元素。 |

## 使用场景
```cpp
QStringList args;
args << "--output" << outputPath;
process.start(program, args);
```

## 常见坑与经验
- `join(",")` 不是 CSV 序列化，含逗号、引号、换行时需要专门格式化。
- 大列表频繁正则过滤要注意性能。
- 去重后顺序与保留策略应写清楚，别把它当 `QSet`。

## 知识点覆盖
字符串集合、参数列表、过滤、拼接、去重、CSV 边界。
