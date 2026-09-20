# QMetaObject::Connection
> Qt 6.11.1 · Qt Core · 来自 `QMetaObject::Connection`

## 作用定位
`QMetaObject::Connection` 是 `QObject::connect()` 返回的连接句柄，可用来在不重新拼写信号与槽的情况下精确断开一条连接。

## API 速查
| API | 是做什么的 |
|---|---|
| `QObject::connect()` 返回值 | 获取连接句柄。|
| `QObject::disconnect(connection)` | 断开该条连接。|
| `operator bool()` | 判断句柄是否代表有效连接。|
| 移动构造/赋值 | 转移连接句柄管理责任。|

## 使用场景
临时模式、页面显示期间的订阅、可切换数据源、一次性或可撤销的事件连接。

## 常见坑与经验
- 连接句柄失效不代表对象仍存活；QObject 析构时相关连接也会自动解除。
- 保存同一信号连接的多个句柄时，断开一个不会断开其余连接。
- lambda 连接应提供 context QObject，避免捕获对象销毁后仍被调用。

## 知识点覆盖
信号槽、连接句柄、精确断开、RAII、lambda context、对象销毁。
