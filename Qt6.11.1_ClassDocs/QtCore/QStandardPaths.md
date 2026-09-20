# QStandardPaths
> Qt 6.11.1 · Qt Core · 来自 `QStandardPaths`

## 作用定位
`QStandardPaths` 按平台规范返回配置、缓存、数据、下载、文档等标准目录。它解决“文件应该放哪里”，避免把用户数据写到程序目录或手写平台路径。

## API 速查
| API | 是做什么的 |
|---|---|
| `writableLocation(type)` | 返回某用途的首选可写目录。 |
| `standardLocations(type)` | 返回某用途的候选目录列表。 |
| `locate()` | 在标准目录中查找文件。 |
| `locateAll()` | 找出所有匹配项。 |
| `findExecutable()` | 按 PATH 或指定路径找可执行文件。 |
| `setTestModeEnabled()` | 测试中切换到隔离目录。 |
| `displayName()` | 获取目录类型的本地化显示名。 |

## 使用场景
```cpp
const QString dir = QStandardPaths::writableLocation(
    QStandardPaths::AppConfigLocation);
QDir().mkpath(dir);
```

## 常见坑与经验
- 返回路径不保证目录已经存在，写入前 `mkpath()`。
- `TempLocation`、`CacheLocation`、`AppDataLocation` 的清理策略不同，不要混放。
- 测试用 `setTestModeEnabled(true)`，避免污染真实用户目录。
- WebAssembly、移动端和沙盒平台路径语义可能受权限限制。

## 知识点覆盖
平台目录规范、配置/缓存/数据分离、沙盒、测试隔离、可执行文件搜索。
