# QTransposeProxyModel
> Qt 6.11.1 · Qt Core · 来自 `QTransposeProxyModel`
## 作用定位
`QTransposeProxyModel` 将源模型的行列互换，让视图以转置形式展示数据。它不复制数据，只做索引映射。
## API 速查
| API | 是做什么的 |
|---|---|
| `setSourceModel()` | 指定要转置的模型。 |
| `mapToSource()` / `mapFromSource()` | 转换代理索引与源索引。 |
| `rowCount()` / `columnCount()` | 代理中行列数对调。 |
| `data()` / `setData()` | 透传到转置后的源索引。 |
## 使用场景
把“字段为行、记录为列”的数据临时显示成更适合表格查看的形态。
## 常见坑与经验
- 索引来自代理时访问源模型必须映射。
- 树模型转置语义有限，主要用于表格。
- 头数据方向也会影响显示，必要时检查 header 映射。
## 知识点覆盖
代理模型、行列转置、索引映射、表格显示、源模型所有权。
