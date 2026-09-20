# QItemSelectionRange
> Qt 6.11.1 · Qt Core · 来自 `QItemSelectionRange`

## 作用定位
`QItemSelectionRange` 表示同一模型上的一个矩形索引范围，以左上和右下索引描述。

## API 速查
| API | 是做什么的 |
|---|---|
| `top()` / `bottom()` | 读取首尾行。|
| `left()` / `right()` | 读取首尾列。|
| `topLeft()` / `bottomRight()` | 读取边界索引。|
| `contains()` | 判断索引或另一个范围是否包含在内。|
| `intersected()` | 求两个范围的交集。|
| `indexes()` | 展开范围中的全部索引。|
| `isValid()` / `isEmpty()` | 检查范围有效性。|

## 使用场景
批量格式化、复制、导出表格矩形区域，或对选区做交集裁剪。

## 常见坑与经验
- 两端索引应属于同一模型且方向正确；跨模型比较没有意义。
- 大范围调用 `indexes()` 会生成大量索引，应优先按行列边界处理。

## 知识点覆盖
模型范围、矩形选区、交集、批量操作、索引归属、内存成本。
