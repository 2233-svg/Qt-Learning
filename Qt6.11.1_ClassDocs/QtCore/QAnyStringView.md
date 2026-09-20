# QAnyStringView
> Qt 6.11.1 · Qt Core · 来自 `QAnyStringView`

## 作用定位
`QAnyStringView` 是只读、非拥有的字符串视图，可接受 `QString`、`QStringView`、UTF-16/UTF-8/Latin-1 数据而避免不必要转换。

## API 速查
| API | 是做什么的 |
|---|---|
| `size()` / `isEmpty()` | 查询视图长度和空状态。|
| `visit()` | 按底层编码访问具体视图。|
| `compare()` | 比较字符串内容。|
| `toString()` | 显式创建拥有数据的 `QString`。|

## 使用场景
库 API 仅需读取文本且希望同时接受多种 Qt 字符串表示时作为参数。

## 常见坑与经验
- 不拥有数据，不能保存超过原始字符串生命期。
- 异步调用前必须复制为 `QString`。

## 知识点覆盖
零拷贝视图、字符串编码、生命周期、API 设计、显式拥有化。
