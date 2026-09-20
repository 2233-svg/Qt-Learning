# QLibraryInfo
> Qt 6.11.1 · Qt Core · 来自 `QLibraryInfo`

## 作用定位
`QLibraryInfo` 提供当前 Qt 安装、构建与运行时布局信息，例如插件、翻译、示例、库和可执行文件的标准路径。

## API 速查
| API | 是做什么的 |
|---|---|
| `path(LibraryPath)` | 返回指定 Qt 资源类别的本地路径。|
| `paths(LibraryPath)` | 返回可能的多个查找路径。|
| `build()` | 查询 Qt 构建配置。|
| `isDebugBuild()` | 判断当前 Qt 是否为 debug build。|
| `version()` | 返回运行时 Qt 版本。|
| `location()` | 兼容旧 API 的单一路径查询。|

## 使用场景
诊断插件无法加载、定位 Qt 翻译资源、在部署工具中检查运行时版本与路径。

## 常见坑与经验
- 返回的是 Qt 运行时布局信息，不是应用数据目录；用户数据使用 `QStandardPaths`。
- 打包后路径可能与开发机不同，不能把开发环境的 Qt 安装路径写死在程序配置中。

## 知识点覆盖
Qt 运行时、插件路径、翻译路径、构建配置、部署、应用数据目录区分。
