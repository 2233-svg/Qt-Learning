# QDirListing
> Qt 6.11.1 · Qt Core · 来自 `QDirListing`

## 作用定位
`QDirListing` 是 Qt 6 的目录 ranges 风格遍历工具，通过 range-for 延迟产生 `DirEntry`，支持过滤、递归与符号链接策略。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `QDirListing(path, options)` | 指定起始目录和遍历选项。|
| `begin()` / `end()` | 提供 range-for 迭代入口。|
| `IteratorFlag::Recursive` | 递归遍历子目录。|
| `IteratorFlag::IncludeDirs` | 在结果中包含目录。|
| `IteratorFlag::FollowDirSymlinks` | 跟随目录符号链接。|
| `IteratorFlag::ResolveSymlinks` | 解析链接目标信息。|

## 使用场景
```cpp
for (const auto &entry : QDirListing(root,
        QDirListing::IteratorFlag::Recursive)) {
    if (entry.fileInfo().isFile())
        importFile(entry.absoluteFilePath());
}
```

## 常见坑与经验
- 这是惰性遍历，循环内耗时处理会延长目录打开和资源占用时间；必要时先收集路径或将处理放入工作队列。
- 跟随符号链接可能逃出预期目录树或遇到循环，涉及安全边界时需比较规范路径并限制根目录。

## 知识点覆盖
现代 C++ ranges、惰性目录遍历、递归、符号链接、文件导入、安全边界。
