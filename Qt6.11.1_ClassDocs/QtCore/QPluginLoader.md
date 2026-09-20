# QPluginLoader
> Qt 6.11.1 · Qt Core · 来自 `QPluginLoader`

## 作用定位
`QPluginLoader` 加载 Qt 插件动态库、读取嵌入的 JSON 元数据，并创建插件根 QObject 实例以供接口转换和调用。

## API 速查
| API | 是做什么的 |
|---|---|
| `setFileName()` | 指定插件库路径。|
| `load()` / `unload()` | 加载或卸载插件库。|
| `instance()` | 创建或返回插件根 QObject。|
| `metaData()` | 读取嵌入式插件 JSON 元数据。|
| `errorString()` | 查询加载、实例化失败原因。|
| `isLoaded()` | 查询库是否已加载。|
| `staticInstances()` | 获取静态链接插件实例。|

## 使用场景
可扩展编辑器、驱动适配层、格式导入器或业务模块按目录发现插件，再通过 `qobject_cast<ExpectedInterface*>` 获取接口。

## 常见坑与经验
- 插件接口必须使用稳定 IID 和兼容 ABI；仅库能加载不代表接口可安全互调。
- `instance()` 返回对象通常由 loader/插件生命周期管理，卸载前必须停止所有使用插件代码的对象与线程。
- 插件目录和元数据均不可信时要实施签名、白名单或权限策略，不能加载任意用户可写路径下的库。

## 知识点覆盖
插件、动态库、JSON 元数据、IID、ABI、对象生命周期、加载安全。
