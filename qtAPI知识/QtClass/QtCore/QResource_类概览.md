# QResource：直接读取 Qt 资源系统中的原始字节

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QResource>`  
> 所属模块：Qt Core  
> 线程说明：所有成员函数均为可重入（reentrant）

`QResource` 是 Qt 资源系统中单个资源实体的低层读取接口。它可以指向一个资源文件或资源目录，直接给出资源字节、压缩信息、大小、最后修改时间和本地化结果。资源通常在构建时由 `rcc` 编进应用或库，也可以在运行时挂载二进制 `.rcc` 包。

它解决的是两类需求：

- 需要尽量少的中间层，直接访问内置图标、二进制模板、着色器或数据文件的字节；
- 需要按需挂载大资源包、皮肤包或插件附带资源，而不把它们全部链接进主程序。

若只想“像读普通文件一样”访问资源，优先使用 `QFile(":/...")`；若需要零拷贝的原始字节、检查压缩算法或控制动态挂载，使用 `QResource`。

## 基本使用

资源路径通常以 `:/` 开头：

```cpp
QResource logo(":/images/logo.png");

if (!logo.isValid()) {
    return;
}

const uchar *bytes = logo.data();
const qint64 byteCount = logo.size();
```

`data()` 指向资源存储中的只读字节，不做复制。这个优势适合只读解析器或把资源交给支持内存视图的库，但前提是资源未压缩。若资源由 `rcc` 压缩，`data()` 返回的仍是**压缩后的有效载荷**，不是原文件内容。

```cpp
const QByteArray plain = logo.uncompressedData();
if (plain.isNull()) {
    // 资源是目录，或解压失败
}
```

`uncompressedData()` 方便，但会创建 `QByteArray`；压缩资源每次调用都要重新解压，结果不会缓存。性能敏感路径应只调用一次并在业务层缓存，或根据压缩算法自行选择更合适的加载方案。

## 路径、搜索路径与本地化

构造函数或 `setFileName()` 可接受：

- 以 `:` 开头的资源路径，例如 `:/images/logo.png`；
- 以 `/` 为根的绝对路径；
- 相对路径，此时会在 `QDir::searchPaths()` 配置的搜索路径中查找。

`fileName()` 返回传入的完整路径表示；`absoluteFilePath()` 返回实际解析后的路径，若通过 `QDir::searchPaths()` 找到，结果会反映该解析路径。调试“为什么加载到另一套主题资源”时，后者更有价值。

资源文件可以包含 locale 变体。构造时传入 `QLocale` 或调用 `setLocale()` 指定查找语言：

```cpp
QResource help(":/docs/help.html", QLocale(QLocale::German));
```

若没有该 locale 的资源，Qt 回退到 `C` locale。`setLocale()` 和 `setFileName()` 都会改变当前对象所指向的资源，应在再次读取 `data()`、尺寸或时间前重新检查 `isValid()`。

## 文件、目录与字节语义

资源实体可能是文件，也可能是目录：

- 文件有数据，因此 `data()` 可返回字节指针；
- 目录只有子项，没有数据，`data()` 返回 `nullptr`；
- `children()`、`isDir()`、`isFile()` 是受保护接口，主要供 Qt 的资源文件引擎使用，不是普通业务层的目录枚举 API。

应用代码若需要遍历资源目录，通常使用 `QDir(":/prefix")`；不要为了调用受保护成员而派生一个仅用于枚举目录的 `QResource` 子类。

`size()` 是**存储数据**大小。资源被压缩时，它是压缩后的字节数；`uncompressedSize()` 是原始数据大小。两者相同并不代表一定没有压缩，但对未压缩资源 Qt 明确返回相同值。

## 压缩算法和读取策略

`compressionAlgorithm()` 返回 `rcc` 使用的压缩方式：

| 枚举 | 含义 | 正确读取方式 |
| --- | --- | --- |
| `NoCompression` | 存储字节就是原数据。 | 可以用 `data()` + `size()` 直接读取。 |
| `ZlibCompression` | 有效载荷经 zlib 压缩。 | 用 `uncompressedData()`，或对原始字节调用 `qUncompress()`。 |
| `ZstdCompression` | 有效载荷经 Zstandard 压缩。 | 用 `uncompressedData()`，或自行调用 zstd 库的 `ZSTD_decompress()`。 |

Qt 没有为 `ZstdCompression` 提供与 `qUncompress()` 对等的专用公开包装。若代码直接使用 `data()`，必须先检查 `compressionAlgorithm()`；把压缩字节当 PNG、JSON、字体或自定义协议解析是常见错误。

另一方面，`QFile` 访问资源时会自动处理资源压缩。资源只需要普通流式读取时，`QFile` 往往更少出错：

```cpp
QFile file(":/docs/readme.txt");
if (file.open(QIODevice::ReadOnly)) {
    const QByteArray text = file.readAll();
}
```

## 动态挂载 `.rcc` 资源

`registerResource()` 把 `rcc` 生成的二进制资源包挂到资源树；`mapRoot` 决定挂载根位置：

```cpp
if (!QResource::registerResource(pluginRccPath, "/themes/dark")) {
    return;
}

QResource themeAsset(":/themes/dark/icons/save.svg");
```

典型场景是按主题、语言包、可选内容包或插件加载一大组资源。Qt 会一次读入或内存映射资源包，然后按资源路径提供对其中片段的引用，避免大量离散文件打开操作。

两个 overload 的生命周期差异很重要：

- `registerResource(const QString &rccFileName, ...)`：Qt 以文件路径挂载包；
- `registerResource(const uchar *rccData, ...)`：调用方必须让该内存持续有效，至少覆盖所有可能引用该资源数据的 `QFile` 生命周期。不能把局部 `QByteArray::constData()` 注册后马上释放其 `QByteArray`。

`unregisterResource()` 会把资源包从根列表中移除，之后不能再新建指向该包内容的 `QResource`。已有的相关 `QResource` 仍可继续有效；资源内存会在最后一个引用它的 `QResource` 销毁后才解除映射。其 `bool` 返回值应检查，且不能把调用返回作为“所有旧指针立刻失效或资源已立刻卸载”的简单信号。

实践上，动态卸载前应先关闭使用该资源的 `QFile`、销毁或替换持有它的 `QResource`、图像和 QML 对象，再 unregister。对内存注册版本，缓冲区也必须保持到不再有任何资源使用它之后。

## 安全与可信边界

`QResource` 会做部分头部兼容性检查，例如拒绝当前 Qt 不支持的压缩特性或未来版本格式，但它**不会验证整个 `.rcc` 文件的完整性和安全性**。

因此不要把用户下载、网络传输或未知插件目录中的 `.rcc` 当作不可信输入直接挂载。运行时资源包的来源至少应与应用和插件本身同等可信；需要可更新资源时，应在挂载前由业务层完成签名、哈希、版本和来源验证。

资源本身也是只读数据，不提供写操作。想覆盖某个资源路径时，应该通过构建系统、动态资源挂载策略或应用配置控制资源树，而不是试图修改 `data()` 指向的内存。

## 生命周期与线程边界

`QResource` 的成员函数是可重入的，不依赖 GUI 线程，也没有 QObject 父子所有权。多个独立 `QResource` 实例可在各自线程中使用。

但以下对象的寿命仍须由调用方管理：

- `data()` 返回的指针只应在其底层资源保持可用时使用；不要在资源对象/动态资源引用释放或卸载流程之后保留它；
- `uncompressedData()` 返回独立的 `QByteArray`，其数据由该数组拥有，适合脱离 `QResource` 继续保存；
- 内存形式注册的 `rccData` 由调用方拥有，Qt 不会替你延长其寿命；
- 动态资源注册与卸载属于进程级资源树变更，应避免与其他线程正在创建或读取同一路径资源的逻辑无协调地交错。

## 常见错误

1. **把 `data()` 当解压后的文件内容。** 先检查 `compressionAlgorithm()`，或直接用 `uncompressedData()` / `QFile`。
2. **在循环中反复调用 `uncompressedData()`。** 压缩资源每次都会重新解压且不缓存。
3. **注册临时内存中的 `.rcc`。** `registerResource(const uchar *)` 不接管缓冲区所有权。
4. **卸载后仍期待新对象能解析旧路径。** 已有对象可保持有效，但以后不能再从资源根创建新引用。
5. **把动态 `.rcc` 当作已验证格式。** Qt 只做有限兼容性检查，不能替代可信来源和完整性验证。
6. **用 `size()` 分配原始内容缓冲区。** 压缩资源需要 `uncompressedSize()` 或 `uncompressedData()`。
7. **把资源目录当文件读取。** 目录没有 `data()`，会返回 `nullptr`。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `Compression` | 表示 `rcc` 对资源载荷使用的压缩算法。 | 决定 `data()` 能否直接当原文件内容解析。 |
| `NoCompression` | 资源未压缩。 | `data()` 和 `size()` 可直接表示内容字节。 |
| `ZlibCompression` | 资源经 zlib 压缩。 | 用 `uncompressedData()` 或 `qUncompress()`。 |
| `ZstdCompression` | 资源经 zstd 压缩。 | 用 `uncompressedData()` 或外部 zstd 的解压 API。 |
| `QResource(file, locale)` | 构造并定位一个资源实体。 | 路径可为资源、绝对或搜索路径相对形式；locale 控制本地化选择。 |
| `~QResource()` | 释放该对象持有的资源引用。 | 最后一个动态资源引用销毁后，底层包才可解除映射。 |
| `setFileName(file)` | 重新定位当前对象。 | 重新读取前检查 `isValid()`；旧 `data()` 指针不应继续用。 |
| `fileName()` | 返回传入的完整路径表示。 | 不一定反映搜索路径后的实际定位结果。 |
| `absoluteFilePath()` | 返回实际解析到的路径。 | 排查 `QDir::searchPaths()` 解析时优先用它。 |
| `setLocale(locale)` | 指定资源本地化查找语言。 | 不存在对应版本时回退到 `C` locale。 |
| `locale()` | 返回当前用于定位的 locale。 | 表示查找条件，不保证资源一定有该语言变体。 |
| `isValid()` | 判断资源是否存在于资源层级中。 | 使用 `data()`、大小或时间前先检查。 |
| `compressionAlgorithm()` | 返回存储载荷的压缩类型。 | 直接解析 `data()` 前必须确认。 |
| `data()` | 返回原始只读存储字节指针。 | 压缩资源返回压缩字节；目录返回 `nullptr`；不保存跨卸载流程。 |
| `size()` | 返回存储数据大小。 | 压缩资源是压缩后的大小。 |
| `uncompressedSize()` | 返回解压后的原始大小。 | 未压缩时等于 `size()`。 |
| `uncompressedData()` | 返回解压后的 `QByteArray`。 | 目录或解压失败返回 null；压缩资源每次调用都重新解压。 |
| `lastModified()` | 返回打包前文件的最后修改时间。 | 是打包元数据，不是运行时资源挂载时间。 |
| `registerResource(rccFileName, mapRoot)` | 从 `.rcc` 文件挂载资源包。 | 文件必须由 `rcc` 生成；检查返回值。 |
| `registerResource(rccData, mapRoot)` | 从内存中的 `.rcc` 字节挂载资源包。 | 调用方必须长期保存 `rccData` 缓冲区。 |
| `unregisterResource(rccFileName, mapRoot)` | 从资源根移除文件注册。 | 现有引用可能继续有效；检查返回值和引用生命周期。 |
| `unregisterResource(rccData, mapRoot)` | 从资源根移除内存注册。 | 缓冲区在所有相关引用结束前都不能释放。 |
| `children()` | 返回资源目录的子项名称。 | 受保护；应用层目录遍历通常改用 `QDir`。 |
| `isDir()` / `isFile()` | 判断实体是资源目录还是资源文件。 | 受保护；文件才有 data backing。 |

## 一句话总结

`QResource` 是读取 Qt 资源包原始内容的低层接口：`data()` 快但可能仍是压缩字节，`uncompressedData()` 易用但会反复解压；动态 `.rcc` 挂载必须管理注册内存、现有引用、卸载时机和资源包可信性。
