# QSaveFile
> Qt 6.11.1 · Qt Core · 来自 `QSaveFile`

## 作用定位
`QSaveFile` 用“写同目录临时文件，再原子替换目标文件”的方式保存内容。它用于配置、项目文件和数据库导出等不能接受半写入的文件；写完不调用 `commit()`，临时内容会被丢弃。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 / `setFileName()` | 指定最终目标路径。 |
| `open(WriteOnly...)` | 打开临时输出设备；必须包含 `WriteOnly`。 |
| `write()` | 通过继承的 `QIODevice` 写入暂存内容。 |
| `commit()` | 校验写入并关闭后，以原子替换提交；返回是否成功。 |
| `cancelWriting()` | 声明放弃当前写入，使 `commit()` 失败并删除临时文件。 |
| `setDirectWriteFallback()` | 无法建临时文件时允许直接覆盖目标，代价是失去原子性。 |
| `directWriteFallback()` | 查询是否启用该退化策略。 |

## 使用场景
```cpp
QSaveFile file(settingsPath);
if (!file.open(QIODevice::WriteOnly))
    return report(file.errorString());
file.write(QJsonDocument(object).toJson());
if (!file.commit())
    return report(file.errorString());
```

## 常见坑与经验
- `close()` 不等于提交，核心步骤是检查 `commit()` 返回值。
- 只读目录中开启 direct-write fallback 后，掉电或崩溃可留下半文件；内部数据默认不要开启它。
- 不支持 `Append`、`ReadWrite` 等与事务式重命名矛盾的打开方式。
- 目标目录的创建、权限和磁盘空间问题仍需处理，原子替换不等于写入必然成功。

## 知识点覆盖
原子保存、临时文件、崩溃一致性、文件权限、错误传播、JSON 序列化、数据完整性。
