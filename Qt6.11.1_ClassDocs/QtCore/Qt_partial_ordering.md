# Qt::partial_ordering
> Qt 6.11.1 · Qt Core · 来自 `Qt::partial_ordering`
## 作用定位
`Qt::partial_ordering` 表示三路比较结果可能“不可比较”，用于兼容没有 `<=>` 标准库支持的环境。
## API 速查
| API | 是做什么的 |
|---|---|
| `less/equivalent/greater/unordered` | 四种比较结果。 |
| 与 0 比较 | 支持 `< 0`、`== 0` 等写法。 |
## 使用场景
浮点 NaN 或集合偏序比较中，两个值可能 unordered。
## 常见坑与经验
- unordered 不是相等，也不是大于或小于。
- 排序容器通常需要严格弱序，不能直接把偏序结果塞进去。
## 知识点覆盖
三路比较、偏序、NaN、C++20 兼容、排序要求。
