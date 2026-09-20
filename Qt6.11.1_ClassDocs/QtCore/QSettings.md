# QSettings
> Qt 6.11.1 · Qt Core · 来自 `QSettings`
## 作用定位
`QSettings` 持久化应用偏好和轻量配置，可使用平台原生存储或 INI 文件；它不是加密保险箱，也不适合大数据或事务数据库。
## API 速查
| API | 是做什么的 |
|---|---|
| `setValue()` / `value()` | 写入或读取键值，读取可给默认值。 |
| `beginGroup/endGroup` | 组织分组键路径。 |
| `beginWriteArray/beginReadArray` | 保存或读取重复项。 |
| `remove()` / `clear()` | 删除键或所有设置。 |
| `sync()` | 强制落盘并更新状态。 |
| `status()` | 诊断访问、格式错误。 |
## 使用场景
```cpp
QSettings s;
s.setValue("window/size", size());
resize(s.value("window/size", QSize(900, 600)).toSize());
```
## 常见坑与经验
- 使用稳定、层级清晰的键名；重命名键需迁移旧数据。
- 密码和令牌不应明文存入 QSettings。
- 多进程同时写同一 INI 仍应设计同步协议。
## 知识点覆盖
配置持久化、平台后端、INI、默认值、迁移、敏感数据边界。
