# QPersistentModelIndex
> Qt 6.11.1 · Qt Core · 来自 `QPersistentModelIndex`

## 作用定位
`QPersistentModelIndex` 是可在模型插入、删除、排序和 layout 变更后自动跟踪同一逻辑项的模型索引句柄；当项被删除或模型 reset 时会失效。

## API 速查
| API | 是做什么的 |
|---|---|
| `isValid()` | 判断所指项是否仍存在。|
| `row()` / `column()` | 查询当前行列位置。|
| `data(role)` | 读取当前 role 数据。|
| `model()` | 获取所属模型。|
| 转换为 `QModelIndex` | 在需要普通索引的 API 中使用当前映射。|
| `swap()` | 交换两个持久索引。|

## 使用场景
异步任务完成后回到启动时的模型项、保存当前选择跨排序恢复、编辑器跟踪某条记录位置。

## 常见坑与经验
- 它不是永久业务 ID：模型 reset 或目标项删除后仍会无效，使用前始终检查 `isValid()`。
- 大量持久索引会增加模型维护开销；不要为每一行长期创建一个。
- 代理模型中的持久索引属于代理层，访问源数据前仍需 `mapToSource()`。

## 知识点覆盖
模型索引、布局变化、持久引用、模型 reset、异步回调、代理映射、性能。
