# QTemporaryDir
> Qt 6.11.1 · Qt Core · 来自 `QTemporaryDir`

## 作用定位
`QTemporaryDir` 创建唯一临时目录，并默认在对象析构时递归删除。它适合测试沙箱、解压中间目录和原子生成文件夹内容。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 按模板创建临时目录。 |
| `isValid()` | 判断目录是否创建成功。 |
| `path()` / `filePath()` | 获取目录或目录内路径。 |
| `setAutoRemove()` | 控制析构时是否删除。 |
| `remove()` | 立即删除临时目录。 |
| `errorString()` | 创建或删除失败说明。 |
## 使用场景
```cpp
QTemporaryDir dir;
if (!dir.isValid())
    return;
writeWorkFiles(dir.filePath("manifest.json"));
```
## 常见坑与经验
- auto-remove 会删除目录内所有内容，交给外部工具后要确认生命周期。
- 需要保留调试产物时关闭 auto-remove，并输出路径。
- 临时目录不是安全沙箱，权限和外部可见性仍取决于平台。
## 知识点覆盖
临时资源、递归删除、测试隔离、路径拼接、错误诊断。
