# QSignalMapper
> Qt 6.11.1 · Qt Core · 来自 `QSignalMapper`
## 作用定位
`QSignalMapper` 将多个无参/同形信号映射成带整数、字符串或对象参数的单一信号。现代 Qt 通常用 lambda 捕获上下文，只有旧式动态映射场景才优先考虑它。
## API 速查
| API | 是做什么的 |
|---|---|
| `setMapping(sender, value)` | 为发送者配置映射值。 |
| `map(sender)` | 发出对应的 mapped 信号。 |
| `mappedInt/String/Object` | 接收统一映射后的值。 |
| `removeMappings(sender)` | 删除某发送者映射。 |
## 使用场景
对动态创建、连接签名固定的旧控件批量分派动作。
## 常见坑与经验
- 新代码优先 `connect(button, &QPushButton::clicked, this, [id]{...});`，类型更安全。
- 发送者销毁时及时清理映射，避免逻辑残留。
## 知识点覆盖
signals/slots、动态分派、lambda 捕获、旧接口迁移、对象生命周期。
