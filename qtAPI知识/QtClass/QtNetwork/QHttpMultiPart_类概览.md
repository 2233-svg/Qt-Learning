# QHttpMultiPart：HTTP MIME multipart 请求体

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHttpMultiPart>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QHttpMultiPart` 表示要随 HTTP 请求发送的 MIME multipart 消息。它把多个 `QHttpPart` 按唯一 boundary 串联，并在 `QNetworkAccessManager` 发送时提供相应的 `Content-Type: multipart/...; boundary=...`。

典型用途是文件上传，但 multipart 不只等于 `multipart/form-data`：它还可表达相互独立附件、彼此相关资源或同一内容的替代表示。

## 实际使用场景

- HTML 表单式文件上传：`FormDataType`。
- 一个请求发送正文加多个附件：`MixedType`。
- 发送互相引用的 MIME 资源，例如有 `Content-ID` 的相关内容：`RelatedType`。
- 同一内容附带多种替代表示：`AlternativeType`。

它只管理 multipart 的格式和 part 集合。请求 URL、方法、认证、超时和响应处理仍属于 `QNetworkRequest`、`QNetworkAccessManager` 与 `QNetworkReply`。

## 基本用法

```cpp
auto multipart = std::make_unique<QHttpMultiPart>(QHttpMultiPart::FormDataType);

QHttpPart title;
title.setHeader(QNetworkRequest::ContentDispositionHeader,
                QVariant("form-data; name=\"title\""));
title.setBody("Quarterly report");

auto file = std::make_unique<QFile>(u"report.pdf"_qs);
if (!file->open(QIODevice::ReadOnly))
    return;

QHttpPart attachment;
attachment.setHeader(QNetworkRequest::ContentTypeHeader,
                     QVariant("application/pdf"));
attachment.setHeader(QNetworkRequest::ContentDispositionHeader,
                     QVariant("form-data; name=\"file\"; filename=\"report.pdf\""));
attachment.setBodyDevice(file.get());

multipart->append(title);
multipart->append(attachment);

file->setParent(multipart.get());
file.release();

QNetworkReply *reply = manager.post(request, multipart.get());
multipart->setParent(reply); // reply 生命周期覆盖异步上传
multipart.release();
```

`QHttpPart::setBodyDevice()` 不拥有 `file`，因此例中把 file 设为 multipart 的子对象。`QNetworkAccessManager::post()` 也不意味着 multipart 会自动随局部变量消失而安全发送；需要让 multipart 至少存活到 reply 结束。常见做法是发送后将 multipart 设为 `QNetworkReply` 的子对象。

## Content type 与 boundary

`QHttpMultiPart()` 默认是 `MixedType`。构造时指定类型，或发送前调用 `setContentType()`：

| `ContentType` | HTTP 子类型 | 表达的关系 |
| --- | --- | --- |
| `MixedType` | `multipart/mixed` | 每个 part 相互独立。 |
| `RelatedType` | `multipart/related` | parts 彼此关联。 |
| `FormDataType` | `multipart/form-data` | 表单字段和上传文件。 |
| `AlternativeType` | `multipart/alternative` | 同一信息的替代表示。 |

Qt 默认生成以 `boundary_.oOo._` 开头并带随机字符的 boundary，目标是避免它出现在 body 内容中。通常不要自行设置；固定或低熵 boundary 若恰好出现在某个 part body 内，会破坏整个请求解析。

只有在需要与严格协议或测试夹具互操作时才使用 `setBoundary()`，并由调用方确保 boundary 在所有 body 中唯一。使用不在枚举中的 multipart 子类型时，可手工给 `QNetworkRequest` 设置 `Content-Type`，但应确保其中的 `boundary` 与 `QHttpMultiPart::boundary()` 一致。

## 顺序、流式内容与重试

`append()` 按调用顺序添加 `QHttpPart`。有些服务端要求字段或资源有特定顺序，尤其是解析流式 multipart 的旧服务端；遇到这类 API 时把顺序当作协议契约。

若 part 使用 `QIODevice`，该 device 必须在上传实际执行时仍打开可读。顺序设备无法随意重新读取，因此认证重试、307/308 重定向或业务重发请求时，不能假定原 multipart 可直接复用；应按 device 的可重置能力决定重新定位或重新构建请求体。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `ContentType` | 已知 multipart 子类型：`MixedType`、`RelatedType`、`FormDataType`、`AlternativeType`。 |
| 构造 | `QHttpMultiPart(QObject *parent = nullptr)` | 创建 `multipart/mixed` 容器。 |
| 构造 | `QHttpMultiPart(ContentType, QObject *parent = nullptr)` | 创建指定子类型的容器；文件上传通常选 `FormDataType`。 |
| 生命周期 | `~QHttpMultiPart()` | 销毁 multipart 及其 QObject 子对象；不会自动拥有由 `QHttpPart` 引用但未设 parent 的 device。 |
| 追加 | `append(const QHttpPart &)` | 按顺序追加一个 part；part 的 headers、body 或 device 在发送时编码。 |
| 类型 | `setContentType(ContentType)` | 设置已知 multipart 子类型；发送时用于 HTTP `Content-Type`。 |
| boundary | `boundary()` | 返回当前 boundary 字节串。 |
| boundary | `setBoundary(const QByteArray &)` | 手动设置 boundary；调用者必须保证对 body 内容唯一。 |
| 协作类型 | `QHttpPart` | 表示一个带 headers 和 body 的 MIME part。 |
| 发送 | `QNetworkAccessManager::post/put/sendCustomRequest(..., QHttpMultiPart *)` | 将 multipart 作为请求体发送；需自行安排 multipart 与所有 body device 在异步操作中存活。 |

## 一句话总结

`QHttpMultiPart` 负责 HTTP multipart 的子类型、boundary 和 part 顺序；上传能否可靠完成还取决于 multipart 及其 body device 是否在异步发送全程持续存活。
