# QDirListing::DirEntry
> Qt 6.11.1 · Qt Core · 来自 `QDirListing::DirEntry`

## 作用定位
`QDirListing::DirEntry` 表示 `QDirListing` 遍历产生的一个目录条目，延迟提供路径与文件信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `fileName()` | 返回文件名。|
| `filePath()` | 返回相对或遍历相关路径。|
| `absoluteFilePath()` | 返回绝对路径。|
| `fileInfo()` | 返回 `QFileInfo` 快照。|
| `exists()` | 判断条目当前是否存在。|
| `isDir()` / `isFile()` / `isSymLink()` | 判断条目类别。|

## 使用场景
在 range-for 中先按类型筛选，再将绝对路径提交给导入、索引或清理任务。

## 常见坑与经验
- `DirEntry` 描述遍历时观察到的状态；文件随后仍可能被移动或删除。
- `absoluteFilePath()` 不是安全授权证明，处理非可信目录时要结合规范路径和权限策略。

## 知识点覆盖
目录条目、文件属性、惰性遍历、TOCTOU、路径安全。
