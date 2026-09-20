# QMimeType
> Qt 6.11.1 · Qt Core · 来自 `QMimeType`

## 作用定位
`QMimeType` 是 MIME 数据库中的一个类型描述值，包含规范名、注释、父类型、glob 模式、后缀和图标信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 返回规范 MIME 名，如 `image/png`。|
| `comment()` | 返回本地化描述。|
| `globPatterns()` | 返回文件名匹配模式。|
| `suffixes()` / `preferredSuffix()` | 返回可用或首选扩展名。|
| `parentMimeTypes()` | 返回继承的父类型。|
| `inherits()` | 判断是否属于某父 MIME 类型。|
| `iconName()` | 返回推荐图标名。|
| `isValid()` | 判断查找是否成功。|

## 使用场景
依据文件类型选择预览器、图标和导入逻辑，或构建“所有图像类型”之类的类型分类。

## 常见坑与经验
- `inherits("text/plain")` 表达的是类型层级，不证明文件内容真的安全可当文本处理。
- 后缀和 glob 仅是匹配提示；执行导入前仍要验证内容和资源限制。

## 知识点覆盖
MIME 类型、类型继承、文件后缀、图标、预览、内容安全。
