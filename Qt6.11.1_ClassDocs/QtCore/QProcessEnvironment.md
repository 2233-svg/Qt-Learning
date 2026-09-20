# QProcessEnvironment
> Qt 6.11.1 · Qt Core · 来自 `QProcessEnvironment`

## 作用定位
`QProcessEnvironment` 是子进程环境变量的值类型映射，用于继承、过滤或构造启动外部程序所见的环境。

## API 速查
| API | 是做什么的 |
|---|---|
| `systemEnvironment()` | 获取当前进程环境快照。|
| `insert()` | 设置或覆盖变量。|
| `remove()` | 删除变量。|
| `value()` | 读取变量值或默认值。|
| `contains()` | 判断变量存在。|
| `keys()` | 枚举变量名。|
| `clear()` | 清空环境。|

## 使用场景
为 `QProcess` 注入固定语言、临时目录、工具路径或认证代理配置；也可过滤继承环境以提升可重复性。

## 常见坑与经验
- 环境变量常含 token、路径和代理凭据，日志输出前必须脱敏。
- `PATH`、`LD_LIBRARY_PATH`、`DYLD_*` 等变量会影响程序与库加载，来自用户输入时有安全风险。
- Windows 环境变量名通常大小写不敏感，跨平台代码不要依赖大小写区分。

## 知识点覆盖
子进程环境、环境继承、PATH、安全、跨平台大小写、可重复构建。
