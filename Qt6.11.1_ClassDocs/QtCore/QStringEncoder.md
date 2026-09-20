# QStringEncoder
> Qt 6.11.1 · Qt Core · 来自 `QStringEncoder`

## 作用定位
`QStringEncoder` 将 `QString` 或字符串视图编码成字节流，适合写文件、发网络协议或导出特定编码文本。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 指定目标编码和选项。 |
| `operator()` / `encode` | 将 Unicode 文本编码为 `QByteArray`。 |
| `hasError()` | 判断是否存在目标编码无法表示的字符。 |
| `requiredSpace()` | 估算输出字节空间。 |
| `encoding()` | 查询目标编码。 |

## 使用场景
```cpp
QStringEncoder encoder(QStringConverter::Utf8);
device.write(encoder(text));
```

## 常见坑与经验
- Latin-1 或本地编码可能无法表示所有 Unicode 字符；导出前定义替换/失败策略。
- 网络和新文件格式优先 UTF-8。
- 编码器可保存状态；流式输出时不要无意义地频繁重建。

## 知识点覆盖
文本编码、Unicode 到字节、导出、错误策略、流式状态。
