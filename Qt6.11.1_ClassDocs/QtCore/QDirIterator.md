# QDirIterator
> Qt 6.11.1 · Qt Core · 来自 `QDirIterator`

## 作用定位
`QDirIterator` 是传统的增量目录遍历器，可在不一次性构建完整列表的情况下遍历匹配条目，支持递归和符号链接跟随选项。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` | 判断是否还有下一个条目。|
| `next()` | 前进并返回下一个文件路径。|
| `filePath()` | 读取当前文件路径。|
| `fileName()` | 读取当前文件名。|
| `fileInfo()` | 读取当前条目的 `QFileInfo`。|
| `path()` | 读取当前目录路径。|
| `Subdirectories` | 递归子目录。|
| `FollowSymlinks` | 允许递归跟随符号链接。|

## 使用场景
扫描大型目录树、导入符合名称过滤条件的文件、逐项处理而不占用大量列表内存。

## 常见坑与经验
- `FollowSymlinks` 可能形成循环或越过预期根目录；默认不要启用，启用时要做根路径与已访问目录控制。
- 迭代期间文件可被删除或权限改变，读取 `QFileInfo` 后仍要处理后续打开失败。
- 新代码也可评估 `QDirListing`，其 ranges 风格更适合现代 C++。

## 知识点覆盖
目录遍历、递归、符号链接、流式处理、TOCTOU、范围 API。
