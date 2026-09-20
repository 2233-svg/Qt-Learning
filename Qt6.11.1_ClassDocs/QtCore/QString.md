# QString
> Qt 6.11.1 · Qt Core · 来自 `QString`

## 作用定位
`QString` 是 Qt 的 Unicode 文本类型，内部以 UTF-16 代码单元存储。它适合用户可见文本、路径片段、协议字段的文本层处理；二进制数据应使用 `QByteArray`。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造与 `fromUtf8/fromLatin1` | 从不同编码创建字符串。 |
| `toUtf8/toLatin1` | 编码输出到字节数组。 |
| `size/length/isEmpty` | 查询 UTF-16 代码单元数量和空状态。 |
| `append/prepend/insert/remove/replace` | 修改文本。 |
| `contains/indexOf/lastIndexOf` | 查找子串。 |
| `split/join` | 分割与拼接。 |
| `trimmed/simplified` | 处理空白。 |
| `arg` | 格式化占位文本。 |
| `number/toInt/toDouble` | 数字与文本转换。 |
| `localeAwareCompare` | 按本地化规则比较。 |

## 使用场景
```cpp
QString title = tr("User %1").arg(userName);
QByteArray payload = title.toUtf8();
```

## 常见坑与经验
- `size()` 不是用户看到的字符数；emoji 和组合字符可能占多个代码单元。
- 不要把 `QString` 当二进制缓冲区，NUL 和编码转换都会制造误会。
- 隐式共享让传值便宜，但并发写同一实例仍不安全。
- 网络、JSON、文件文本通常明确使用 UTF-8，不要依赖本地 8 位编码。

## 知识点覆盖
Unicode、UTF-16、编码转换、隐式共享、本地化、文本查找、数字转换、二进制边界。
