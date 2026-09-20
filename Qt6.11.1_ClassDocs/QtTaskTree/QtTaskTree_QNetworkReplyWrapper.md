# QtTaskTree::QNetworkReplyWrapper
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QNetworkReplyWrapper`

## 作用定位

`QNetworkReplyWrapper` 把 `QNetworkReply` 风格的异步网络请求包装成 TaskTree 任务。它通常用于下载、请求 API、等待网络完成并按错误状态返回 `DoneResult`。

## 类说明

- 头文件：`#include <qnetworkreplywrappertask.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `start()` | 启动/进入等待网络 reply 完成的流程。 |
| `setNetworkReply()` 或相关设置入口 | 指定要包装的网络响应对象。 |
| `reply()` | 访问底层 `QNetworkReply`。 |
| `done(result)` | 网络任务完成时发出。 |
| `started()` | 任务启动时发出。 |

## 使用场景

- 在 TaskTree 中发起 HTTP 请求。
- 顺序请求：登录 -> 拉配置 -> 下载资源。
- 并行请求并统一等待。

## 常见坑与经验
- `QNetworkReply` 所属线程必须有事件循环。
- 网络错误、HTTP 状态码错误、业务 JSON 错误是三层不同失败，要在 done handler 里区分。
- reply 生命周期要和任务一致，避免提前 deleteLater。

## 知识点覆盖

- 网络异步任务包装
- QNetworkReply 生命周期
- 网络错误分层
- 顺序/并行网络工作流
