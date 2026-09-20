# QResource
> Qt 6.11.1 · Qt Core · 来自 `QResource`

## 作用定位
`QResource` 访问编译进应用或运行时注册的 Qt 资源系统内容。资源路径以 `:` 开头，例如 `:/icons/open.svg`；它解决的是只读应用资源的部署与定位，不是用户数据目录。

## API 速查
| API | 是做什么的 |
|---|---|
| `QResource(path)` / `setFileName()` | 选择资源路径。 |
| `isValid()` | 判断路径是否存在且资源可访问。 |
| `data()` / `size()` | 直接读取资源内存与长度。 |
| `uncompressedData()` / `uncompressedSize()` | 取得解压后的数据；可能产生额外内存。 |
| `isCompressed()` | 判断 `.rcc` 内资源是否压缩。 |
| `fileName()` / `absoluteFilePath()` | 查询资源路径信息。 |
| `registerResource()` | 运行时挂载外部 `.rcc` 包。 |
| `unregisterResource()` | 卸载动态资源包；仍被使用时会失败。 |
| `locale()` / `setLocale()` | 选择本地化资源变体。 |

## 使用场景
```cpp
QFile stylesheet(":/themes/dark.qss");
if (stylesheet.open(QIODevice::ReadOnly))
    app.setStyleSheet(QString::fromUtf8(stylesheet.readAll()));
```

## 常见坑与经验
- 资源路径与文件系统路径不同，`:/` 不能传给期望原生磁盘文件的第三方库；必要时复制到临时文件。
- `data()` 指针由资源系统所有，资源卸载或对象语义变化后不要长期保存。
- 动态 `unregisterResource()` 前必须确保没有仍在读取该包的对象。
- 用户可修改内容应放在 `QStandardPaths` 目录，不能尝试写回 qrc。

## 知识点覆盖
qrc、rcc、只读资源、部署、本地化资源、压缩数据、内存生命周期、与文件系统的边界。
