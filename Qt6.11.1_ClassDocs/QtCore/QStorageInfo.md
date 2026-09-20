# QStorageInfo
> Qt 6.11.1 · Qt Core · 来自 `QStorageInfo`

## 作用定位
`QStorageInfo` 查询磁盘卷、挂载点、总容量、可用空间、只读状态和文件系统名称。它适合保存前检查空间、列出磁盘、判断路径所在卷。

## API 速查
| API | 是做什么的 |
|---|---|
| `QStorageInfo(path)` | 查询路径所在的存储卷。 |
| `root()` | 获取根卷信息。 |
| `mountedVolumes()` | 列出已挂载卷。 |
| `refresh()` | 重新读取系统状态。 |
| `bytesTotal()` / `bytesAvailable()` / `bytesFree()` | 查询容量与可用空间。 |
| `isValid()` / `isReady()` | 判断信息是否有效、设备是否可用。 |
| `isReadOnly()` | 判断卷是否只读。 |
| `rootPath()` / `fileSystemType()` / `displayName()` | 查询挂载点、文件系统和显示名。 |

## 使用场景
```cpp
QStorageInfo storage(targetPath);
storage.refresh();
if (!storage.isReady() || storage.bytesAvailable() < expectedBytes)
    warnUser();
```

## 常见坑与经验
- 空间检查不是事务，检查后到写入前空间可能变化。
- 网络盘、移动盘可能暂时不可用，先看 `isReady()`。
- `bytesAvailable()` 通常更贴近当前用户可写空间，`bytesFree()` 可能包含无权限使用的空间。
- 不同平台文件系统名称和挂载语义差异很大，不要做过窄字符串判断。

## 知识点覆盖
挂载卷、容量检查、只读介质、网络/移动存储、平台差异、保存前诊断。
