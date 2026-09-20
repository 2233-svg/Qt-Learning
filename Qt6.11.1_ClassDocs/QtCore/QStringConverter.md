# QStringConverter
> Qt 6.11.1 · Qt Core · 来自 `QStringConverter`

## 作用定位
`QStringConverter` 是编码器和解码器的公共基础，描述 UTF-8、UTF-16、Latin-1、System 等文本编码及转换选项。

## API 速查
| API | 是做什么的 |
|---|---|
| `Encoding` | 表示内置编码类型。 |
| `Flag` / `Flags` | 控制 BOM、无效字符处理等策略。 |
| `name()` | 查询编码名称。 |
| `encodingForName()` | 由名称查找编码。 |
| `availableCodecs()` | 列出可用编码。 |
| `hasError()` | 查询转换过程中是否出错。 |

## 使用场景
读取用户选择的编码名称后，构造 `QStringDecoder` 或 `QStringEncoder` 做流式转换。

## 常见坑与经验
- 编码名称来自外部时要处理未知编码。
- 错误策略要按业务决定：导入文本可替换，配置/协议更应失败。
- BOM 是文件格式线索，不是所有文本流都有。

## 知识点覆盖
字符编码、BOM、转换错误、编码名称、流式编码器/解码器。
