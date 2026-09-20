# QAbstractProxyModel
> Qt 6.11.1 · Qt Core · 来自 `QAbstractProxyModel`

## 作用定位
`QAbstractProxyModel` 是包装源模型的基类，负责 source 与 proxy 索引间的双向映射。

## API 速查
| API | 是做什么的 |
|---|---|
| `setSourceModel()` | 绑定被代理模型。|
| `sourceModel()` | 读取源模型。|
| `mapToSource()` | 将代理索引转为源索引。|
| `mapFromSource()` | 将源索引转为代理索引。|
| `mapSelectionToSource()` | 转换选择范围。|
| `mapSelectionFromSource()` | 将源选择映射到代理。|

## 使用场景
实现筛选、排序、列重组、权限遮罩或组合数据视图。

## 常见坑与经验
- 映射必须保持可逆一致；错误映射会导致编辑写回错误位置。
- proxy 链可能很长，操作真实数据前需一直 map 到最终源模型。

## 知识点覆盖
代理模型、索引映射、选择映射、数据变换、模型链。
