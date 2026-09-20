# QVector
> Qt 6.11.1 · Qt Core · 来自 `QVector<T>`
## 作用定位
`QVector<T>` 是连续存储的动态数组；在 Qt 6 中它与 `QList` 语义靠近，适合按索引访问、批量遍历和与 C API 共享连续内存。
## API 速查
| API | 是做什么的 |
|---|---|
| `append/prepend/insert/remove` | 修改元素序列。 |
| `at/operator[]` | 读取或写入索引位置。 |
| `reserve/resize/squeeze` | 管理容量和大小。 |
| `data/constData` | 获取连续内存指针。 |
| `begin/end` | 迭代访问。 |
## 使用场景
保存绘制顶点、采样数据、模型内部行缓存等需要连续内存的列表。
## 常见坑与经验
- 扩容、插入和 detach 会使指针/引用/迭代器失效。
- `operator[]` 不检查范围；边界不可信时用 `value()` 或显式判断。
- 隐式共享不保证同一实例并发写安全。
## 知识点覆盖
动态数组、连续内存、容量、隐式共享、迭代器失效、索引访问。
