# QFormDataPartBuilder：配置一个 form-data 字段

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFormDataPartBuilder>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：由 `QFormDataBuilder::part()` 返回的共享状态代理

## 它解决什么问题

`QFormDataPartBuilder` 用于填写 `multipart/form-data` 的单个字段。`QFormDataBuilder::part(name)` 已经为它创建了 `Content-Disposition: form-data` 以及字段名；此类型继续负责设置 body、可选文件名、MIME 类型和额外 part headers。

它不是可独立保存的完整 `QHttpPart`。它只是指向某个 `QFormDataBuilder` 内部 part 的代理，因此其有效期受 builder 严格限制。

## 实际使用场景

- `part("comment").setBody("hello")` 添加普通文本字段。
- `part("attachment").setBodyDevice(&file, "report.pdf", "application/pdf")` 流式上传文件。
- 为一个字段添加业务相关 part header，例如 `Content-ID`；而表单自身的 `Content-Disposition` 与 `Content-Type` 仍由 builder 统一维护。

## 生命周期和共享副本

```cpp
QFormDataBuilder builder;
auto image = builder.part(u"image"_qs);
auto alias = image; // 浅副本，仍指向 builder 中同一个字段

alias.setBody("replacement");
// image 对应的字段也已被修改。
```

复制 `QFormDataPartBuilder` 是浅复制：副本与原对象修改的是同一个内部 part。所有副本都在关联的 `QFormDataBuilder` 析构后失效。不要从创建 builder 的函数返回这个类型，也不要在 builder 已移动或销毁后继续调用它。

## Body 的选择

### `setBody()`

用于小型内存内容。传入可选 `fileName` 时，会把它写入 `Content-Disposition`；传入非空 `mimeType` 时，会设为 part 的 `Content-Type`。省略 MIME 类型时 Qt 尝试用 `QMimeDatabase` 从数据自动检测。

后续调用 `setBodyDevice()` 会丢弃这里设置的内存 body。

### `setBodyDevice()`

用于文件和大内容。device 内容在发送时直接读取，避免把整个文件复制到内存中。device 必须打开且可读，且直到请求真正结束前都不得被关闭或销毁；`QFormDataPartBuilder` 不接管所有权。

后续调用 `setBody()` 会丢弃 device body。若 device 是顺序设备，等它发出 `finished()` 再 `post()`；它的内容通常不可重放，网络重试和重定向的可用性因此受限。

## Header 的边界

`setHeaders(const QHttpHeaders &)` 可添加 part headers，但其中的 `content-type` 和 `content-disposition` 会被 builder 覆盖。原因是这两个 header 必须与 form 字段名、文件名和 MIME 类型保持一致。

因此：

- 用 `setBody(..., fileName, mimeType)` / `setBodyDevice(..., fileName, mimeType)` 控制文件名和 MIME 类型。
- 用 `setHeaders()` 放置其他 headers，例如 `Content-ID`。
- 不要依赖 `setHeaders()` 强行改写 builder 自动生成的 `Content-Disposition`。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 获取方式 | `QFormDataBuilder::part(QAnyStringView)` | 以字段名创建代理；该名称会进入 form-data 的 `Content-Disposition`。 |
| 构造 | `QFormDataPartBuilder()` | 默认构造的对象没有关联 builder，通常不应作为可配置字段使用。 |
| 复制 | `QFormDataPartBuilder(const QFormDataPartBuilder &)` | 浅复制，同一内部 part；改副本也会改原代理所代表的字段。 |
| 移动 | `QFormDataPartBuilder(QFormDataPartBuilder &&)` | 移动代理引用。 |
| 赋值 | `operator=(const QFormDataPartBuilder &)` | 浅赋值，关联到同一个内部 part；有效期仍由 builder 决定。 |
| 赋值 | `operator=(QFormDataPartBuilder &&)` | 移动赋值。 |
| 交换 | `swap(QFormDataPartBuilder &)` | 交换两个代理的关联状态。 |
| 内存 body | `setBody(QByteArrayView, QAnyStringView fileName = {}, QAnyStringView mimeType = {})` | 设置内存内容；适合小数据。后续 `setBodyDevice()` 会替换它。 |
| 流式 body | `setBodyDevice(QIODevice *, QAnyStringView fileName = {}, QAnyStringView mimeType = {})` | 设置读取设备；适合大数据且不复制。device 必须打开、可读且在请求全程存活，不转移所有权。 |
| headers | `setHeaders(const QHttpHeaders &)` | 设置额外 part headers；`content-type` 和 `content-disposition` 会被 builder 覆盖。 |
| 生命周期 | `~QFormDataPartBuilder()` | 销毁代理本身，不销毁 builder 或 body device。 |

## 一句话总结

`QFormDataPartBuilder` 是绑定到 `QFormDataBuilder` 的单字段编辑器：用它选择内存或流式 body，但要让 builder、multipart 与 device 在整次异步上传期间保持正确的存活关系。
