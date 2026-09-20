# QTypeRevision
> Qt 6.11.1 · Qt Core · 来自 `QTypeRevision`
## 作用定位
`QTypeRevision` 表示类型、属性或方法的主/次版本修订号，常用于 QML 类型系统判断某 API 从哪个版本开始可见。
## API 速查
| API | 是做什么的 |
|---|---|
| `fromVersion()` | 构造主次版本。 |
| `majorVersion()` / `minorVersion()` | 读取版本分量。 |
| `hasMajorVersion()` / `hasMinorVersion()` | 判断分量是否存在。 |
| `isValid()` | 判断修订值是否有效。 |
| 比较运算 | 判断版本先后。 |
## 使用场景
注册 QML 类型 API 时标注成员引入版本，保护旧 QML 代码兼容性。
## 常见坑与经验
- 版本修订是 API 可见性，不是包管理语义版本的完整替代。
- 未设置主/次版本与 0 不完全等价，要用 `has*` 判断。
## 知识点覆盖
QML 版本化、API 可见性、主次版本、兼容性、元对象。
