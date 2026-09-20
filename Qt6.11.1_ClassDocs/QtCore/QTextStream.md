# QTextStream
> Qt 6.11.1 · Qt Core · 来自 `QTextStream`

## 作用定位
`QTextStream` 在 `QIODevice`、`QString` 或 `QByteArray` 上提供文本读写、编码、数字格式和行读取。它面向文本，不适合二进制协议。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 绑定设备、字符串或字节数组。 |
| `setEncoding()` | 指定文本编码。 |
| `readLine()` / `readAll()` | 读取文本。 |
| `operator<<` / `operator>>` | 格式化输出或解析输入。 |
| `flush()` | 推送缓冲数据到设备。 |
| `status()` / `setStatus()` | 查询解析和 I/O 状态。 |
| `setLocale()` / 数字格式 API | 控制数字本地化输出。 |
## 使用场景
```cpp
QTextStream out(&file);
out.setEncoding(QStringConverter::Utf8);
out << title << '\n';
```
## 常见坑与经验
- 明确设置编码，尤其是跨平台文件。
- `operator>>` 以空白分隔，读取整行用 `readLine()`。
- 大文件逐行处理，避免 `readAll()` 一次占用大量内存。
## 知识点覆盖
文本 I/O、编码、缓冲、行读取、数字格式、本地化、状态检查。
