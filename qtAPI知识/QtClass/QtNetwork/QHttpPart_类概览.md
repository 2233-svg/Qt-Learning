# QHttpPart：multipart 中的一个 MIME body part

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHttpPart>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：隐式共享的值类型

## 它解决什么问题

`QHttpPart` 表示 `QHttpMultiPart` 中的一个 body part：它包含一组 part-level headers 和一段内存 body，或一个在发送时读取的 `QIODevice`。Qt 负责在 headers 与 body 之间插入 MIME 所需的空行，并由 `QHttpMultiPart` 再负责 boundary。

它用于精确构造 multipart 协议内容。相比把所有字段手工写进 `QByteArray`，它能将 header、内存内容和文件设备分开管理，避免 boundary、换行和大文件复制问题。

## 实际使用场景

- `multipart/form-data` 中的文本字段和文件字段。
- `multipart/related` 中带 `Content-ID` 的资源。
- 自定义 multipart 请求中需要 `Content-Type`、`Content-Disposition` 或业务 header 的单个部分。

若只是发送 JSON 或一个普通二进制请求体，应直接使用 `QNetworkAccessManager` 的 `QByteArray` / `QIODevice` 重载；没有 multipart 就不需要 `QHttpPart`。

## 基本用法

```cpp
QHttpPart part;
part.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("text/plain; charset=utf-8"));
part.setHeader(QNetworkRequest::ContentDispositionHeader,
               QVariant("form-data; name=\"comment\""));
part.setRawHeader("Content-ID", "comment-1");
part.setBody("hello");

multipart.append(part);
```

上传大文件时让 part 从 device 流式读取：

```cpp
auto *file = new QFile(u"archive.zip"_qs, &multipart);
if (!file->open(QIODevice::ReadOnly))
    return;

QHttpPart part;
part.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("application/zip"));
part.setHeader(QNetworkRequest::ContentDispositionHeader,
               QVariant("form-data; name=\"file\"; filename=\"archive.zip\""));
part.setBodyDevice(file);
multipart.append(part);
```

## Header 语义

`setHeader()` 接受 `QNetworkRequest::KnownHeaders`，行为与 `QNetworkRequest::setHeader()` 相同，适合 `Content-Type`、`Content-Disposition` 等 Qt 已知 header。

`setRawHeader()` 用字节串设置任意 header。若名称恰好是 Qt 已知 header，Qt 也会解析并更新对应的“cooked” header。再次设置同名 header 会覆盖旧值；需要多个同名 HTTP header 的语义时，按文档建议把值以逗号拼成一个 raw header，而不是期待它自动累加。

part header 与整个请求的 `QNetworkRequest` header 是不同层次：文件字段的 `Content-Disposition`、每个附件自己的 `Content-Type` 设在 `QHttpPart`；请求级鉴权、Accept、Cookie 等设在 `QNetworkRequest`。

## 内存 body 与 device body

`setBody()` 适合小内容。`setBodyDevice()` 不会把数据复制到内存，适合文件，但有严格的存活要求：

- device 必须在 `QNetworkAccessManager` 真正读取时仍然打开且可读。
- `QHttpPart` 不拥有 device，不能在 `append()` 后立刻关闭或析构它。
- 可把 device 设为 `QHttpMultiPart` 的子对象，再让 multipart 随 reply 存活，形成清晰的所有权链。
- 若 device 是顺序设备，应在它发出 `finished()` 后再发起 `post()`；其内容不一定能重放，重试和重定向要另行设计。
- 调用 `setBodyDevice(nullptr)` 可移除 device body，重新使用此前由 `setBody()` 设置的内存内容。

后设置的 device body 会优先于内存 body；对同一个 part 在异步发送已经开始后再修改 body 或 headers 没有可依赖的协议语义，应在提交给 `QHttpMultiPart` 前完成配置。

## 值语义与比较

`QHttpPart` 是隐式共享值类型，适合局部构造后按值 `append()`。`operator==` 比较 headers 与 body 是否相同；它不是网络资源可用性检查，两个引用同一已关闭 device 的 part 也不因此“可发送”。

`swap()` 只交换对象内部状态，适合实现高效的赋值或容器操作。Qt 6.8 起可用 `QDebug << part` 输出调试信息；若未设置 device，输出会显示 body 大小，而不应把它当作完整请求体抓包工具。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 构造 | `QHttpPart()` | 创建空 part。 |
| 构造 | `QHttpPart(const QHttpPart &)` | 复制 part 的值状态；适合按值追加到 multipart。 |
| 赋值 | `operator=(const QHttpPart &)` / `operator=(QHttpPart &&)` | 复制或移动赋值。 |
| 比较 | `operator==(const QHttpPart &)` / `operator!=(const QHttpPart &)` | 比较 headers 与 body；不验证 device 是否仍打开可读。 |
| 交换 | `swap(QHttpPart &)` | 高效、无异常地交换两个 part 的状态。 |
| known header | `setHeader(QNetworkRequest::KnownHeaders, const QVariant &)` | 设置已知 part header，覆盖此前同名值。 |
| raw header | `setRawHeader(const QByteArray &, const QByteArray &)` | 设置任意 part header；同名重复设置覆盖旧值，已知 header 会同步解析。 |
| 内存 body | `setBody(const QByteArray &)` | 设置内存内容；适合小数据。若已设置 device，device body 仍优先，除非先移除它。 |
| device body | `setBodyDevice(QIODevice *)` | 从 device 流式读取内容；不转移所有权，device 必须在请求全程打开且可读。传 `nullptr` 可取消 device body。 |
| 调试 | `operator<<(QDebug, const QHttpPart &)` | Qt 6.8 起；输出调试表示，未设置 device 时显示 body 大小。 |
| 协作类型 | `QHttpMultiPart::append(const QHttpPart &)` | 将 part 以当前值状态加入 multipart，并按追加顺序编码。 |

## 一句话总结

`QHttpPart` 描述 multipart 的一个 header/body 单元：小内容用内存 body，大内容用 device body，而 device 的可读状态与生命周期必须由应用负责到底。
