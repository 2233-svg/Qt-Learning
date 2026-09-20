# QMetaEnum
> Qt 6.11.1 · Qt Core · 来自 `QMetaEnum`

## 作用定位
`QMetaEnum` 描述经 `Q_ENUM` 或 `Q_FLAG` 注册到 Qt 元对象系统的枚举，可在运行时在枚举名、键名、整数值和 flags 字符串之间转换。

## API 速查
| API | 是做什么的 |
|---|---|
| `keyCount()` | 查询枚举键数量。|
| `key(index)` / `value(index)` | 按索引读取键和值。|
| `keyToValue()` | 将键名转为整数值。|
| `valueToKey()` | 将整数值转为键名。|
| `keysToValue()` | 解析 `A|B` flags 文本。|
| `valueToKeys()` | 将 flags 值转为键名列表。|
| `isFlag()` | 判断是否表示 flags。|
| `enumName()` | 查询枚举名称。|

## 使用场景
配置文件中以可读文本存放枚举、属性编辑器显示选项、日志中输出枚举名。

## 常见坑与经验
- 转换失败会返回无效结果，必须使用 `bool *ok` 或等价检查；不要把 `0` 当成天然失败值。
- 持久化枚举名会受重命名影响，跨版本配置应设计兼容别名或显式稳定代码。
- 只有通过 `Q_ENUM`/`Q_FLAG` 注册的类型才具备完整元对象信息。

## 知识点覆盖
枚举反射、Q_ENUM、Q_FLAG、字符串转换、配置兼容、flags。
