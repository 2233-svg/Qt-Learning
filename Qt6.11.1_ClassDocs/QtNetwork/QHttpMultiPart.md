# QHttpMultiPart
> Qt 6.11.1 · Qt Network · 来自 `QHttpMultiPart`

## 作用定位
`QHttpMultiPart` 组织 `multipart/form-data`、`multipart/related` 等分段 HTTP 请求体，最常用于文件上传。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `ContentType` | 选择 form-data、mixed、related、alternative。|
| `append()` | 添加一个 `QHttpPart`。|
| `setBoundary()` | 设置 multipart 边界。|
| `boundary()` | 读取当前边界。|

## 使用场景
```cpp
auto *multi = new QHttpMultiPart(QHttpMultiPart::FormDataType);
multi->append(filePart);
reply = manager.post(request, multi);
multi->setParent(reply);
```

## 常见坑与经验
- 必须让 multipart 和作为 body 的 `QIODevice` 活到请求结束；通常把它们设为 reply 的子对象。
- 不要手工设置与实际 boundary 不一致的 `Content-Type`。

## 知识点覆盖
multipart、文件上传、MIME、QIODevice 生命周期、HTTP body。
