# QModelIndex
> Qt 6.11.1 · Qt Core · 来自 `QModelIndex`

## 作用定位
`QModelIndex` 是 Qt Model/View 中定位一个模型单元或树节点的轻量句柄，包含模型、行、列和内部标识信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `row()` / `column()` | 查询所在行列。|
| `parent()` | 查询树模型父索引。|
| `child()` | 获取子行列索引。|
| `data(role)` | 直接向所属模型读取某 role 数据。|
| `flags()` | 查询项交互能力。|
| `model()` | 获取所属模型。|
| `isValid()` | 判断是否表示有效位置。|
| `siblingAtRow()` / `siblingAtColumn()` | 定位同父节点的邻近单元。|

## 使用场景
view、delegate、selection model 与代理模型之间传递当前项、读取 role 数据和定位父子节点。

## 常见坑与经验
- `QModelIndex` 不是稳定业务 ID；行插入、删除、排序、layout 变化或 reset 后它可能失效或指向不同项目。
- 需要跨模型变动保持引用时使用 `QPersistentModelIndex`，或保存业务键后重新查找。
- 不要构造伪造索引；由模型的 `index()`、`createIndex()` 和映射 API 生成。

## 知识点覆盖
Model/View、树索引、角色数据、代理映射、索引失效、持久索引、业务 ID。
