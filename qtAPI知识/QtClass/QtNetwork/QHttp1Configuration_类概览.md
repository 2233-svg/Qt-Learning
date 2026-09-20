# QHttp1Configuration：HTTP/1 每主机连接数配置

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHttp1Configuration>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：可复制、可移动、可哈希的值类型（Qt 6.5 起）

## 它解决什么问题

`QHttp1Configuration` 控制 `QNetworkAccessManager` 为同一 HTTP/1 `host:port` 建立的并发连接数。HTTP/1.1 的一条连接通常不能像 HTTP/2 那样高效复用为多个并行流，因此客户端常需要连接池来避免一个慢请求阻塞其他请求。

该类目前只公开一个调节项：每个 `http(s) host:port` 组合的连接数上限。它不会开启 HTTP/1、不会强制协议降级，也不控制 HTTP/2 的 stream 数量。

## 实际使用场景

- 同一 HTTP/1 API 主机上有多个独立的并发下载或上传任务。
- 服务端对每客户端并发连接有明确限制，需要降低默认并发量。
- 内网服务延迟低但应用需要更高的 HTTP/1 并发，经过压测后适度上调连接池上限。

若服务器实际协商为 HTTP/2，这个“每 host TCP 连接数”调节不是并发请求的主要控制杆；HTTP/2 使用单连接多 stream，相关参数应看 `QHttp2Configuration`。

## 关键时机：第一条请求之前

配置必须在目标 `host:port` 的第一条请求发出前设置。第一条请求会建立或复用该主机的 HTTP/1 会话；之后再修改后续 request 上的配置，不能指望它回溯改变已经存在的连接池。

```cpp
QHttp1Configuration http1;
http1.setNumberOfConnectionsPerHost(4);

QNetworkRequest request(url);
request.setHttp1Configuration(http1);

QNetworkReply *reply = manager.get(request); // 此 host:port 的第一条请求前设置
```

同一个 `QNetworkAccessManager` 中，若不同模块首次向同一主机发送请求时带不同配置，先发出的请求实际上决定会话建立时使用的配置。需要一致策略的应用应在网络层集中构造 request，而不是让业务层临时各自设置。

## 参数语义与边界

默认值是每个 `host:port` 六条连接。`setNumberOfConnectionsPerHost()` 接收的有效范围为 1 到 255：

- 小于等于 0：不改变当前配置。
- 大于 255：按 255 使用。
- 增大连接数可能提升高延迟、独立请求的并行度，但也增加 TCP/TLS 握手、服务端负载、带宽竞争和文件描述符消耗。
- 减小连接数有助于尊重服务端限制，但可能让 HTTP/1 队列等待更明显。

这个值是每个 `host:port` 的上限，不是整个 `QNetworkAccessManager` 或整个应用的全局连接总数。`https://api.example.com:443` 与相同主机的不同端口是不同池。

## 值语义与可重入性

该类所有函数可重入，适合按值存进配置对象或 request 工厂。移动后的对象处于部分形成状态，只应销毁或重新赋值，不应再读取其参数。`operator==`、`operator!=` 与 `qHash()` 比较/散列的是 HTTP/1 参数集合，可用于去重或缓存配置，不表示两个运行中的连接池状态相同。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 构造 | `QHttp1Configuration()` | 创建默认配置，连接数默认 6。 |
| 构造 | 复制/移动构造 | 复制或转移配置值；移动后原对象只应销毁或重新赋值。 |
| 赋值 | 复制/移动 `operator=` | 复制或转移配置；不改变已建立连接池。 |
| 核心配置 | `setNumberOfConnectionsPerHost(qsizetype)` | 设置每个 HTTP(S) `host:port` 的 HTTP/1 连接数，范围 1-255；非正数无效，过大钳制为 255。 |
| 核心查询 | `numberOfConnectionsPerHost()` | 返回配置的每 host 连接数。 |
| 交换 | `swap(QHttp1Configuration &)` | 快速、无异常地交换两个配置。 |
| 比较 | `operator==` / `operator!=` | Qt 6.5 起；比较参数集合而不是当前网络连接状态。 |
| 散列 | `qHash(const QHttp1Configuration &, size_t seed = 0)` | Qt 6.5 起；用于哈希容器中的配置值。 |
| 请求协作 | `QNetworkRequest::setHttp1Configuration()` | 把配置附到 request；应在目标 host 第一条请求之前设置。 |
| 请求协作 | `QNetworkRequest::http1Configuration()` | 读取 request/底层 HTTP/1 连接所用的参数。 |

## 一句话总结

`QHttp1Configuration` 只调节 HTTP/1 每个 `host:port` 的连接池上限：默认 6，取值 1-255，并且要在目标主机的第一条请求之前确定。
