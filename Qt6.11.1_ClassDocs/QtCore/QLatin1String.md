# QLatin1String
> Qt 6.11.1 · Qt Core · 来自 `QLatin1String`

## 作用定位
`QLatin1String` 是 Latin-1 字节文本的轻量只读包装，常用于与 `QString` 比较或传递确定只含 Latin-1 的常量。

## API 速查
| API | 是做什么的 |
|---|---|
| `data()` / `size()` | 访问底层字节和长度。|
| `latin1()` | 取得 Latin-1 视图。|
| `operator QString()` | 显式或隐式转换为 Unicode 字符串。|
| 比较运算符 | 与 `QString` 或同类内容比较。|

## 使用场景
固定协议关键字、ASCII/Latin-1 资源名、与 `QString` 比较时避免先创建临时 QString。

## 常见坑与经验
- Latin-1 只能表达 U+0000 到 U+00FF；中文、emoji 等 Unicode 文本绝不能用它编码。
- 它不拥有数据，传入动态缓冲时要确保原内存仍有效。

## 知识点覆盖
Latin-1、Unicode、字符串视图、零拷贝、编码边界。
