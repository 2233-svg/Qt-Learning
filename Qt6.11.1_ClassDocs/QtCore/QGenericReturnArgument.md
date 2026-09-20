# QGenericReturnArgument
> Qt 6.11.1 · Qt Core · 来自 `QGenericReturnArgument`

## 作用定位
`QGenericReturnArgument` 是旧式 `QMetaObject::invokeMethod()` 调用中承接返回值的运行时参数包装类型。

## API 速查
| API | 是做什么的 |
|---|---|
| `Q_RETURN_ARG(Type, value)` | 为运行时调用准备返回值存储位置。|
| `name()` | 返回声明的返回值类型名。|
| `data()` | 返回调用应写入的内存地址。|

## 使用场景
在同线程的直接元对象调用中，用方法名字符串动态调用并获取返回值。

## 常见坑与经验
- queued 异步调用不能以这种方式同步取得返回值；应改为信号、future 或回调。
- 返回存储变量的类型必须与方法签名一致，否则调用失败或产生未定义行为。
- 新代码优先使用编译期检查更强的函数指针/lambda 调用形式。

## 知识点覆盖
元对象、动态调用、返回值、直接与 queued 调用、类型匹配。
