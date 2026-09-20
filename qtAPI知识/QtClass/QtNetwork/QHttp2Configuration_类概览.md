# QHttp2Configuration：HTTP/2 SETTINGS 与流控参数

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHttp2Configuration>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：可复制、可移动、可重入的值类型

## 它解决什么问题

`QHttp2Configuration` 定义 `QNetworkAccessManager` 在使用 HTTP/2 时向对端通告和采用的一组参数：连接/stream 接收窗口、最大 frame 大小、允许的并发 streams、server push 和 HPACK Huffman 字符串压缩。

它解决的是 HTTP/2 连接级的吞吐量与资源边界问题，不是请求 header 配置，也不是“强制服务器支持 HTTP/2”的开关。协议是否会使用 HTTP/2 仍取决于请求属性、TLS/ALPN 或 h2c 协商以及服务端能力。

## 实际使用场景

- 高带宽或高往返延迟 API 需要调整 HTTP/2 的接收窗口，减少流控等待。
- 受内存预算限制的客户端降低接收窗口或并发 stream 上限。
- 需要明确拒绝或允许 server push 的嵌入式客户端。
- 与特定 HTTP/2 设备或代理互操作，需要控制初始 SETTINGS 值和 frame 上限。

如果应用只是普通 REST 客户端，默认配置通常更合适。盲目增大窗口、frame 或并发 stream 并不会保证更快，反而可能增加缓冲、竞争和故障面。

## 关键时机：同一主机的第一条 HTTP/2 请求

先把配置放到 `QNetworkRequest`，再发起到目标 `host:port` 的第一条请求：

```cpp
QHttp2Configuration http2;
http2.setServerPushEnabled(false);
http2.setSessionReceiveWindowSize(1U << 20);
http2.setStreamReceiveWindowSize(1U << 20);

QNetworkRequest request(url);
request.setHttp2Configuration(http2);

QNetworkReply *reply = manager.get(request);
```

HTTP/2 在一条连接上复用多个 stream。Qt 对同一主机的连续请求会使用建立好的会话，因此**第一条请求的配置决定该连接**；后续 request 即使携带不同的 `QHttp2Configuration`，也不能重新协商已发送的初始 SETTINGS。

`QNetworkRequest::Http2AllowedAttribute` 默认是 `true`，但这仅允许 Qt 尝试 HTTP/2。`Http2DirectAttribute` 会跳过初始协商并要求服务器支持 HTTP/2；若服务器不支持，Qt 不会回退 HTTP/1.1。配置对象本身不改变这些协议选择规则。

## 各参数的语义

| 参数 | 影响 | 默认构造值 |
| --- | --- | --- |
| `serverPushEnabled` | 是否在初始 SETTINGS 中允许服务端主动推送响应。 | `false` |
| `huffmanCompressionEnabled` | Qt 发送 HEADERS 时，HPACK 字符串是否额外使用 Huffman 编码。 | `true` |
| `sessionReceiveWindowSize` | 连接级接收流控窗口，对端在所有 streams 合计可发送的数据上限。 | 65,535 字节 |
| `streamReceiveWindowSize` | 每个 stream 的接收流控窗口。 | 65,535 字节 |
| `maxFrameSize` | 向服务端通告的最大 HTTP/2 frame payload 大小。 | 16,384 字节 |
| `maxConcurrentStreams` | Qt 6.9 起，向对端通告的最大并发 streams。 | 使用默认配置值 |

接收窗口越大，允许对端在等待 `WINDOW_UPDATE` 前发送更多数据，但也可能提高单连接或单 stream 的缓存压力和公平性问题。窗口值不是下载缓冲区大小的精确承诺，也不控制客户端向服务端上传的流控额度。

`setHuffmanCompressionEnabled()` 只影响 Qt 发送的 HEADERS frame，不改变对端如何编码响应 headers。启用 server push 也不等于应用会自动消费或缓存所有推送资源；应确认 `QNetworkAccessManager` 侧的处理契约和产品需求。

## 参数校验与边界

- `setSessionReceiveWindowSize()` 与 `setStreamReceiveWindowSize()` 仅接受 `1` 到 `2,147,483,647`，非法值返回 `false` 且不应被忽略。
- `setMaxFrameSize()` 仅接受 `16,384` 到 `16,777,215`，非法值返回 `false`。即使设置更大，具体 payload frame 仍可能小于 16,384。
- `setMaxConcurrentStreams()` 不返回状态；设置的值会在初始 SETTINGS 中通告给对端，不能把它理解为 Qt 客户端必然同时发出的请求数。
- 新建 `QHttp2Configuration` 的默认值是协议基础配置；不要把它与 `QNetworkRequest::http2Configuration()` 报告的 `QNetworkAccessManager` 实际默认参数混为一谈。若行为必须固定，显式设置并在首个请求前附加。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 构造 | `QHttp2Configuration()` | 默认：push 关闭、Huffman 开启、两个接收窗口 65,535、frame 16,384。 |
| 构造 | 复制/移动构造 | 复制或转移 HTTP/2 参数值。 |
| 赋值 | 复制/移动 `operator=` | 复制或转移配置，不会改变已建立 HTTP/2 会话。 |
| server push | `setServerPushEnabled(bool)` / `serverPushEnabled()` | 控制/读取初始 SETTINGS 的 push 允许项；默认禁用。 |
| HPACK | `setHuffmanCompressionEnabled(bool)` / `huffmanCompressionEnabled()` | 控制/读取 Qt 发送 headers 的 Huffman 字符串压缩；仅影响出站 HEADERS。 |
| 连接流控 | `setSessionReceiveWindowSize(unsigned)` / `sessionReceiveWindowSize()` | 设置/读取连接级接收窗口；范围 1 至 2,147,483,647，setter 以 `bool` 报告非法值。 |
| stream 流控 | `setStreamReceiveWindowSize(unsigned)` / `streamReceiveWindowSize()` | 设置/读取每 stream 接收窗口；范围和失败语义同连接窗口。 |
| frame | `setMaxFrameSize(unsigned)` / `maxFrameSize()` | 设置/读取通告给对端的最大 frame payload；范围 16,384 至 16,777,215，非法值返回 `false`。 |
| 并发 streams | `setMaxConcurrentStreams(unsigned)` / `maxConcurrentStreams()` | Qt 6.9 起；通告对端可并发的最大 stream 数。 |
| 交换 | `swap(QHttp2Configuration &)` | 快速、无异常地交换两个配置。 |
| 比较 | `operator==` / `operator!=` | 比较参数集合，不比较已有连接的实时状态。 |
| 请求协作 | `QNetworkRequest::setHttp2Configuration()` | 在发起请求前附加配置；同一主机的首个 HTTP/2 request 决定会话使用的配置。 |
| 请求协作 | `QNetworkRequest::http2Configuration()` | 返回 request/底层 HTTP/2 连接所用或默认的参数。 |
| 协议协作 | `Http2AllowedAttribute` | 默认允许 HTTP/2 协商；与配置对象不同，决定 Qt 是否可尝试使用 HTTP/2。 |
| 协议协作 | `Http2DirectAttribute` | 跳过协商直接要求 HTTP/2；服务器不支持时不回退 HTTP/1.1。 |

## 一句话总结

`QHttp2Configuration` 用于在建立 HTTP/2 会话前设定 SETTINGS 与接收流控：它的参数应基于吞吐、内存与互操作测试确定，而同一主机的第一条请求会锁定后续复用连接的配置。
