# QDebugStateSaver
> Qt 6.11.1 · Qt Core · 来自 `QDebugStateSaver`

## 作用定位
`QDebugStateSaver` 是用于自定义 `QDebug` 输出运算符的 RAII 辅助类：进入作用域时保存格式状态，离开时自动恢复。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `QDebugStateSaver(QDebug&)` | 保存指定 debug 流状态。|
| 析构函数 | 自动恢复空格、引号等格式设置。|

## 使用场景
```cpp
QDebug operator<<(QDebug debug, const Packet &p)
{
    QDebugStateSaver saver(debug);
    debug.nospace().noquote() << "Packet(" << p.id << ')';
    return debug;
}
```

## 常见坑与经验
- 它只保存 QDebug 格式状态，不会管理被输出对象的生命周期或线程安全。
- 自定义运算符应按值接收并返回 `QDebug`，沿用 Qt 的流式约定。

## 知识点覆盖
RAII、日志格式、运算符重载、异常安全、调用方状态保护。
