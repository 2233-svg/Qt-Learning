# QItemSelection
> Qt 6.11.1 · Qt Core · 来自 `QItemSelection`

## 作用定位
`QItemSelection` 表示一组模型索引选区，内部以 `QItemSelectionRange` 合并连续矩形，适合跨行列传递选择状态。

## API 速查
| API | 是做什么的 |
|---|---|
| `select(topLeft, bottomRight)` | 添加一个矩形选区。|
| `merge()` | 按选择命令合并或移除选区。|
| `indexes()` | 展开为单个索引列表。|
| `contains()` | 判断某索引是否在选区中。|
| `isEmpty()` | 判断是否没有选择。|
| `first()` / `last()` | 访问首尾选区范围。|

## 使用场景
在 view、代理模型和复制导出逻辑之间传递多段表格选择。

## 常见坑与经验
- `indexes()` 可能产生大量临时索引；只需判断范围时直接遍历 selection ranges。
- 合并选区前必须确保索引属于同一模型，否则范围语义没有意义。

## 知识点覆盖
模型选择、矩形范围、选区合并、索引归属、批量操作。
