# QStringDecoder
> Qt 6.11.1 · Qt Core · 来自 `QStringDecoder`

## 作用定位
`QStringDecoder` 将字节流按指定编码解码为 `QString`。它保存跨调用状态，因此能正确处理 UTF-8 多字节字符被分块截断的情况。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 指定编码和转换策略。 |
| `operator()` / `decode` | 将一段字节解码为 Unicode 文本。 |
| `hasError()` | 判断是否遇到非法字节序列。 |
| `requiredSpace()` | 估算输出空间。 |
| `encoding()` | 查询当前编码。 |

## 使用场景
```cpp
QStringDecoder decoder(QStringConverter::Utf8);
while (device.bytesAvailable())
    text += decoder(device.read(4096));
```

## 常见坑与经验
- 分块读取时复用同一个 decoder，不要每块重新构造。
- 协议文本编码固定时显式写出，不要猜测本地编码。
- 遇到错误后继续还是中止，应由数据来源可信度决定。

## 知识点覆盖
流式解码、UTF-8 分块、错误恢复、文件导入、协议文本。
