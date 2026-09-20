# QAbstractTableModel
> Qt 6.11.1 · Qt Core · 来自 `QAbstractTableModel`

## 作用定位
`QAbstractTableModel` 是二维表模型便利基类，默认没有树形 parent 关系。

## API 速查
| API | 是做什么的 |
|---|---|
| `rowCount()` / `columnCount()` | 返回表格尺寸。|
| `data()` | 返回单元格数据。|
| `headerData()` | 返回行列标题。|
| `setData()` | 支持单元格编辑。|
| `flags()` | 设置编辑/选择能力。|

## 使用场景
数据库结果、配置编辑器、统计表、表格式业务数据。

## 常见坑与经验
- 列序与角色含义应稳定；视图保存列宽、排序状态时依赖它。
- 更新多个单元格时用准确矩形的 `dataChanged()`。

## 知识点覆盖
表模型、单元格角色、表头、编辑、批量通知。
