# QFileSelector
> Qt 6.11.1 · Qt Core · 来自 `QFileSelector`

## 作用定位
`QFileSelector` 根据平台、语言、主题或自定义 selector，从一组带 `+selector` 后缀的资源文件中选择最合适的文件路径。

## API 速查
| API | 是做什么的 |
|---|---|
| `select(filePath)` | 为单个文件选择最佳变体。|
| `select(url)` | 为 URL 资源选择最佳变体。|
| `setExtraSelectors()` | 添加应用自定义选择条件。|
| `extraSelectors()` | 查询当前自定义选择条件。|
| `allSelectors()` | 查询内置和自定义 selector。|

## 使用场景
按平台提供 `+android`、`+windows` 资源，或按用户主题选择 `+dark` 配置文件。

## 常见坑与经验
- selector 是资源选择规则，不是访问控制；不能用它隔离机密文件。
- 变体文件缺失时会回退到基础文件，发布前应测试每个平台与主题组合。
- 自定义 selector 顺序和命名应稳定，避免不同模块对同一资源选择出意外版本。

## 知识点覆盖
资源变体、平台适配、主题、语言、回退、部署测试。
