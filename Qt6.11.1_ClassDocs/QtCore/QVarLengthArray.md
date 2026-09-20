# QVarLengthArray
> Qt 6.11.1 · Qt Core · 来自 `QVarLengthArray<T, Prealloc>`
## 作用定位
`QVarLengthArray` 是小数组优化容器：少量元素存在对象内预分配空间，超过阈值后转堆分配。适合短暂、尺寸通常较小但偶尔增长的临时数组。
## API 速查
| API | 是做什么的 |
|---|---|
| `append/push_back` | 添加元素。 |
| `resize/reserve` | 调整大小或容量。 |
| `data()` | 取得连续内存。 |
| `size/capacity` | 查询元素数和容量。 |
| `operator[]` | 按索引访问。 |
| `squeeze()` | 释放多余容量。 |
## 使用场景
```cpp
QVarLengthArray<QPointF, 8> polygon;
```
大多数多边形点数小于 8 时可避免堆分配。
## 常见坑与经验
- `data()` 指针在扩容后失效。
- 栈内预分配过大可能增加对象栈空间压力。
- 需要长期保存和频繁共享时普通容器更清晰。
## 知识点覆盖
小数组优化、连续内存、栈/堆权衡、指针失效、临时缓冲。
