# QContiguousCache
> Qt 6.11.1 · Qt Core · 来自 `QContiguousCache`

## 作用定位
`QContiguousCache<T>` 是以连续整数索引表示的滑动窗口缓存，适合只保留最近或邻近区间数据，而不是任意键查找。

## API 速查
| API | 是做什么的 |
|---|---|
| `setCapacity()` | 设置最多保留的元素数。|
| `append()` / `prepend()` | 在缓存两端加入连续索引数据。|
| `insert(index, value)` | 在指定索引写入。|
| `at(index)` | 按逻辑索引读取。|
| `firstIndex()` / `lastIndex()` | 查询当前窗口边界。|
| `containsIndex()` | 判断索引是否仍在缓存中。|
| `normalizeIndexes()` | 重置逻辑索引以防长期溢出。|

## 使用场景
虚拟滚动列表、时间序列最近窗口、分页数据预取，索引自然连续且过期数据可丢弃。

## 常见坑与经验
- 它不是哈希表；随机跳跃的 key 或稀疏 ID 不适合。
- 容量淘汰会使旧索引不可访问，模型层应能重新加载缺失区间。

## 知识点覆盖
滑动窗口、连续索引、缓存淘汰、虚拟化、分页、内存边界。
