# QCollatorSortKey
> Qt 6.11.1 · Qt Core · 来自 `QCollatorSortKey`

## 作用定位
`QCollatorSortKey` 是按某个 `QCollator` 预计算出的不可见排序键，适合让大量同 locale 字符串排序更高效。

## API 速查
| API | 是做什么的 |
|---|---|
| `compare()` | 与另一个排序键比较先后。|
| `operator<()` | 可直接提供给排序算法。|

## 使用场景
列表加载时为每项缓存 `collator.sortKey(name)`，排序时比较键而不是重复比较原始字符串。

## 常见坑与经验
- sort key 只与创建它的 collator 配置相匹配；locale、numeric mode 等改变后必须重建。
- 键用于排序，不应用作展示文本或持久跨版本格式。

## 知识点覆盖
排序键、本地化排序、缓存、比较器性能、配置一致性。
