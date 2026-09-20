# QTemporaryFile
> Qt 6.11.1 · Qt Core · 来自 `QTemporaryFile`

## 作用定位
`QTemporaryFile` 安全创建唯一临时文件，避免文件名竞争，并默认在析构时删除。它适合下载缓存、外部程序输入和中间结果。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 设置模板路径。 |
| `open()` | 创建并打开唯一文件。 |
| `fileName()` / `fileTemplate()` | 查询实际路径和模板。 |
| `setAutoRemove()` | 控制析构时是否删除文件。 |
| `rename()` | 将临时文件移动为目标文件。 |
| `createNativeFile()` | 为资源或非本地文件生成本地临时副本。 |
## 使用场景
把内存数据写成临时文件交给只接受路径的第三方程序。
## 常见坑与经验
- 必须成功 `open()` 后才有实际唯一文件名。
- 默认 auto-remove，外部程序异步使用时要延长对象生命周期。
- 持久保存重要文件优先用 `QSaveFile`。
## 知识点覆盖
临时文件、安全命名、auto-remove、外部程序互操作、原子保存区别。
