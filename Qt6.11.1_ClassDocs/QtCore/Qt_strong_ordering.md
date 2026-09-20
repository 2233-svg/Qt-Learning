# Qt::strong_ordering
> Qt 6.11.1 · Qt Core · 来自 `Qt::strong_ordering`
## 作用定位
`Qt::strong_ordering` 表示强全序三路比较：相等值在所有可观察意义上等价，适合整数、指针包装和严格身份排序。
## API 速查
| API | 是做什么的 |
|---|---|
| `less/equal/equivalent/greater` | 表达比较结果。 |
| 与 0 比较 | 兼容 `<=>` 风格判断。 |
| 转换到弱/偏序 | 在需要较弱语义时可降级。 |
## 使用场景
为值类型实现确定、稳定且无 unordered 分支的比较。
## 常见坑与经验
- 如果“等价”但内部表现可不同，应考虑 weak ordering。
- 比较必须自洽，否则排序和关联容器会出错。
## 知识点覆盖
三路比较、强序、值语义、排序容器、自洽比较。
