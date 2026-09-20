# QLatin1StringView
> Qt 6.11.1 · Qt Core · 来自 `QLatin1StringView`

## 作用定位
`QLatin1StringView` 是明确表示 Latin-1 编码字节区间的非拥有只读视图，是 `QLatin1String` 的现代 view 形式。

## API 速查
| API | 是做什么的 |
|---|---|
| `data()` / `size()` | 访问字节与长度。|
| `sliced()` / `first()` / `last()` | 创建子视图。|
| `compare()` | 与其他文本比较。|
| `toString()` | 转换为拥有数据的 `QString`。|
| `indexOf()` | 查找字符或子序列。|

## 使用场景
库接口接收明确 Latin-1 的只读文本、解析 ASCII 协议字段、避免字符串复制。

## 常见坑与经验
- 视图不拥有内存，传入临时 `QByteArray` 或局部 C buffer 后不能长期保存。
- Latin-1 字节不是 UTF-8；不要对网络 UTF-8 body 误用该类型。

## 知识点覆盖
字符串视图、Latin-1、生命周期、子视图、UTF-8 区分、零拷贝。
