# QSortFilterProxyModel
> Qt 6.11.1 · Qt Core · 来自 `QSortFilterProxyModel`

## 作用定位
`QSortFilterProxyModel` 位于源模型和视图之间，负责排序、过滤、列映射和索引转换。它不拥有业务数据，只改变视图看到的数据顺序和可见性。

## API 速查
| API | 是做什么的 |
|---|---|
| `setSourceModel()` | 指定被代理的原始模型。 |
| `sort()` | 按列和方向排序代理视图。 |
| `setFilterRegularExpression()` | 设置文本过滤规则。 |
| `setFilterKeyColumn()` | 指定过滤作用的列。 |
| `setFilterRole()` / `setSortRole()` | 指定过滤和排序使用的数据角色。 |
| `mapToSource()` / `mapFromSource()` | 在代理索引与源索引之间转换。 |
| `filterAcceptsRow()` | 自定义行过滤逻辑。 |
| `lessThan()` | 自定义排序比较。 |
| `invalidateFilter()` / `invalidate()` | 源外部条件变化后刷新代理结果。 |

## 使用场景
```cpp
auto *proxy = new QSortFilterProxyModel(this);
proxy->setSourceModel(source);
proxy->setFilterCaseSensitivity(Qt::CaseInsensitive);
proxy->setFilterRegularExpression(searchText);
view->setModel(proxy);
```

## 常见坑与经验
- 视图返回的索引属于代理模型，访问源数据前必须 `mapToSource()`。
- 自定义过滤依赖外部变量时，变量变化后要让代理失效重算。
- 复杂正则过滤和深层树递归可能很贵，搜索框输入应节流。
- 排序比较必须稳定且自洽，别让 `lessThan(a,b)` 和 `lessThan(b,a)` 同时为真。

## 知识点覆盖
代理模型、索引映射、角色数据、排序比较、正则过滤、树模型递归、性能节流。
