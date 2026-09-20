# Qt QSaveFile 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSaveFile>`  
> 所属模块：`Qt6::Core`  
> 继承：`QFileDevice -> QSaveFile`  
> 定位：先写临时文件，成功后原子替换目标文件的安全写入设备

## 1. QSaveFile 解决什么问题

直接用 `QFile` 覆盖配置文件时，程序可能在截断旧文件后崩溃，留下半份内容。`QSaveFile` 把写入分成两步：

```text
目标 settings.ini
        |
        | open/write
        v
临时文件 settings.ini.XXXXXX
        |
        | commit()
        v
用完整临时文件替换目标
```

它适合配置、索引、项目文件和其他“要么旧版本，要么完整新版本”的普通文件更新。

它不解决：

- 多个进程同时写同一个文件的业务冲突。
- 文件内容格式本身损坏。
- 目录不存在或权限不足。
- 数据库级多文件事务。
- 所有平台上的绝对断电持久性保证。

## 2. 标准写入流程

```cpp
bool saveSettings(const QString &path, const QByteArray &data)
{
    QSaveFile file(path);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << file.errorString();
        return false;
    }

    if (file.write(data) != data.size()) {
        qWarning() << file.errorString();
        return false;
    }

    if (!file.commit()) {
        qWarning() << file.errorString();
        return false;
    }
    return true;
}
```

`commit()` 是关键。只 `write()` 后离开作用域，不等于把临时文件替换成目标文件；如果没有提交，QSaveFile 会取消临时写入。

## 3. 失败和取消

```cpp
QSaveFile file(path);
if (!file.open(QIODevice::WriteOnly))
    return false;

if (!writeDocument(file))
    return false; // 析构时取消临时文件

file.cancelWriting();
```

写入过程失败时，不要对旧目标文件做删除或截断补救。让 QSaveFile 保留旧文件，记录错误并让调用者决定是否重试。

## 4. Direct Write Fallback

```cpp
file.setDirectWriteFallback(true);
```

当目标文件所在文件系统不支持安全的临时文件替换时，QSaveFile 可以退回直接写目标文件。这样兼容性更好，但原子替换保证会减弱。对配置和索引等重要文件，默认的安全行为通常更合适；启用 fallback 前要明确接受风险。

## 5. 和文本流、数据流配合

```cpp
QSaveFile file("settings.ini");
if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    return false;

QTextStream out(&file);
out.setEncoding(QStringConverter::Utf8);
out << "[editor]\nfontSize=14\n";

return file.commit();
```

流对象必须在 `commit()` 前完成写入并保持设备有效。先检查流状态，再提交文件。

## 6. 常见误区

### 忘记 commit

这是最常见错误。QSaveFile 的成功条件不是 `open()` 或 `write()`，而是最后 `commit()` 返回 true。

### 以为 commit 后一定可回滚

替换完成后，QSaveFile 不提供撤销。需要历史版本应在应用层保留备份。

### 把 directWriteFallback 当默认优化

它牺牲了安全写入语义。只有明确知道目标文件系统限制并接受风险时才开启。

### 父目录不存在

QSaveFile 不会替你创建父目录。先用 `QDir::mkpath()` 创建，并处理权限失败。

### 多进程同时保存

两个进程都成功 commit 时，后提交者可能覆盖前者。需要锁、合并或数据库事务。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSaveFile(QString fileName, QObject *parent = nullptr)` | 创建一个针对目标路径的安全保存设备。 | 构造不创建目标文件；父目录和权限由调用者负责。 |
| 构造 | `QSaveFile(QObject *parent = nullptr)` | 创建未指定路径的 QSaveFile。 | 使用前必须 `setFileName()`。 |
| 析构 | `~QSaveFile()` | 关闭设备并清理未提交的临时文件。 | 未调用 commit 的内容不会成为目标文件。 |
| 路径 | `fileName()` | 返回当前目标文件路径。 | 返回的是目标路径，不是临时文件路径。 |
| 路径 | `setFileName(QString)` | 设置目标文件路径。 | 应在 open 前设置；不会移动已有目标文件。 |
| 打开 | `open(OpenMode)` | 创建临时文件并打开写入设备。 | 通常使用 WriteOnly；失败后读取 errorString。 |
| 提交 | `commit()` | 将已完整写好的临时文件替换目标文件。 | 这是成功保存的最终判断；返回 false 时目标文件可能仍是旧版本。 |
| 取消 | `cancelWriting()` | 主动取消当前临时写入。 | 目标文件保持原样；之后不要继续写入并期待成功提交。 |
| 回退 | `setDirectWriteFallback(bool)` | 允许在无法安全替换时直接写目标文件。 | 会减弱原子保存保证；默认不要随意开启。 |
| 回退 | `directWriteFallback()` | 查询 direct write fallback 设置。 | 只表示策略，不表示本次保存已经发生回退。 |
| 设备接口 | `write()` / `flush()` | 向临时设备写入内容并刷新缓冲。 | 写成功仍要 commit；检查部分写入和设备错误。 |
| 设备接口 | `errorString()` | 返回当前保存失败的诊断文字。 | 适合日志，不要依赖文字做程序分支。 |

---

### 一句话总结

`QSaveFile` 把“写配置”变成“先完成新文件，再替换旧文件”。真正的成功点是 `commit()`，真正的安全边界是不要随意启用 direct-write fallback，并且要把目录、权限、格式校验和并发策略一起设计。
