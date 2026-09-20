# QFormDataBuilder：构建 multipart/form-data 请求体

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFormDataBuilder>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：不可复制、可移动的值类型

## 它解决什么问题

`QFormDataBuilder` 是 Qt 6.8 引入的表单上传构建器。它用 `part(name)` 创建带有正确 `Content-Disposition: form-data; name=...` 语义的 part，并最终生成一个 `QHttpMultiPart`，省去手工拼接 `Content-Disposition`、文件名与 MIME 类型的易错字符串。

它特别解决了多语言文件名的互操作问题。不同 RFC 对 `multipart/form-data` 的 `filename` / `filename*` 编码要求并不完全一致，因此 `buildMultiPart()` 提供选项来适配服务端，而不是把某一种格式硬编码为唯一答案。

## 实际使用场景

- Web API 上传头像、附件、图片和普通文本字段。
- 调用需要 `multipart/form-data` 的 REST 服务，且字段名与文件名需要正确转义。
- 同时上传多个文件并希望大文件直接从 `QFile` 读取，而不是先装入 `QByteArray`。

它只构建请求体，不发送网络请求。发送由 `QNetworkAccessManager::post()`、`put()` 或 `sendCustomRequest()` 完成。

## 基本用法与生命周期

```cpp
QFormDataBuilder builder;

auto image = std::make_unique<QFile>(u":/upload/photo.png"_qs);
if (!image->open(QIODevice::ReadOnly))
    return;

builder.part(u"title"_qs).setBody("A photo");
builder.part(u"image"_qs).setBodyDevice(image.get(), u"photo.png"_qs, u"image/png"_qs);

auto multipart = builder.buildMultiPart();
image->setParent(multipart.get()); // QFormDataPartBuilder 不拥有 device
image.release();

QNetworkReply *reply = manager.post(request, multipart.get());
multipart->setParent(reply);        // 上传完成前让 reply 保持 multipart 存活
multipart.release();                // 所有权交给 QObject 父子链
```

`buildMultiPart()` 返回 `std::unique_ptr<QHttpMultiPart>`。若把它交给异步网络请求，不能在函数返回时让它析构；可像上例一样将其设为 reply 的子对象并 `release()`，也可由别的明确所有者在 reply 结束前保持它存活。

`QFormDataPartBuilder` 是关联到 `QFormDataBuilder` 内部状态的轻量代理。它只在关联 builder 存活期间有效，因此应以链式调用或局部短生命周期方式使用，不要把它从 builder 的作用域中返回或保存到成员中等待以后再用。

## 文件、内存与字段名边界

- `setBody()` 适合小字段和小内容；数据会作为内存体使用。
- `setBodyDevice()` 适合文件等大内容，会在发送时直接从 `QIODevice` 读取，避免内部复制。device 必须已打开、可读且在整个请求期间存活；builder 不拥有它。
- 若 device 是顺序设备（如 socket），应在其发出 `finished()` 后再调用 `QNetworkAccessManager::post()`。它不可随意倒带，重定向或重试时也未必能重放完整请求体。
- `part(name)` 的 `name` 强烈建议限制为 US-ASCII，以获得最佳服务端互操作性。
- `setBody()` 和 `setBodyDevice()` 后调用另一个，会替换前一个 body 来源，不会同时发送内存与 device 两份内容。

当省略 `mimeType` 时，`QFormDataPartBuilder` 会尝试用 `QMimeDatabase` 自动检测。对安全敏感的接口或需要严格协议行为的服务器，最好显式给出 MIME 类型，不把内容嗅探结果当作业务校验。

## 文件名编码选项

| `Option` | 作用 |
| --- | --- |
| `Default` | 默认互操作策略：非 ASCII 文件名保留常规 `filename`，并附带 RFC 8187 风格 `filename*`；UTF-8 文件名默认不做 RFC 7578 百分号编码。 |
| `OmitRfc8187EncodedFilename` | 不发送 RFC 8187 风格的 `filename*`。用于明确不接受该参数的服务端。 |
| `UseRfc7578PercentEncodedFilename` | 对 UTF-8 文件名按 RFC 7578 进行百分号编码。 |
| `PreferLatin1EncodedFilename` | 非 ASCII 名可用 Latin-1 表示时，优先 Latin-1 而非 UTF-8。 |
| `StrictRfc7578` | 等价于 `OmitRfc8187EncodedFilename | UseRfc7578PercentEncodedFilename`。 |

不要仅凭“规范名称”就启用严格模式：旧服务端、反向代理和上传组件对文件名处理各不相同。应以目标 API 的真实兼容性测试选择选项。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `Option` | 控制 `buildMultiPart()` 的文件名编码策略；按目标服务端兼容性选择。 |
| 标志 | `Options` | `QFlags<Option>`，可按位组合多个选项。 |
| 构造 | `QFormDataBuilder()` | 创建空的 form-data 构建器。 |
| 移动 | `QFormDataBuilder(QFormDataBuilder &&)` | 转移内部构建状态；该类不可复制。 |
| 移动 | `operator=(QFormDataBuilder &&)` | 移动赋值，原对象不再保有原来的构建状态。 |
| 交换 | `swap(QFormDataBuilder &)` | 无异常地交换两个 builder 的状态。 |
| part | `part(QAnyStringView name)` | 添加/取得一个以 `name` 为 form-data 名称的 part 代理；代理依赖 builder 生命周期，字段名宜用 ASCII。 |
| 构建 | `buildMultiPart(Options options = {})` | 生成默认 `FormDataType` 的 `std::unique_ptr<QHttpMultiPart>`；异步发送期间必须保持其存活。 |
| 生命周期 | `~QFormDataBuilder()` | 销毁内部构建状态；此前获得的 `QFormDataPartBuilder` 随之失效。 |
| 协作类型 | `QFormDataPartBuilder` | 为单个字段设置内存 body、device body 和额外 headers。 |
| 协作类型 | `QHttpMultiPart` | 最终 multipart 容器，可传给 `QNetworkAccessManager` 的 multipart 重载。 |

## 一句话总结

`QFormDataBuilder` 用结构化 API 生成 `multipart/form-data`：代理只在 builder 存活期有效，大文件 device 与生成的 multipart 必须一直活到异步请求完成，文件名编码则应按服务端兼容性显式选择。
