# QMutableListIterator
> Qt 6.11.1 · Qt Core · 来自 `QMutableListIterator`

## 作用定位
`QMutableListIterator<T>` 是 Java 风格可变列表迭代器，支持在遍历时读取、替换、插入或删除当前元素。

## API 速查
| API | 是做什么的 |
|---|---|
| `next()` / `previous()` | 前后移动。|
| `value()` | 读取当前元素。|
| `setValue()` | 替换当前元素。|
| `remove()` | 删除当前元素。|
| `insert()` | 在当前位置插入元素。|
| `findNext()` | 向前查找指定值。|

## 使用场景
维护旧代码时一边扫描列表一边移除无效项或替换元素。

## 常见坑与经验
- 新代码常用标准 iterator 加 `erase()` 或算法，逻辑更易组合。
- 除该迭代器外不要同时修改列表，否则当前位置和删除语义会混乱。

## 知识点覆盖
可变列表迭代、插入删除、旧式 API、迭代器状态、容器修改。
