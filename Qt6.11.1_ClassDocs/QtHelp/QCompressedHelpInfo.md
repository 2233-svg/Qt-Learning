# QCompressedHelpInfo
> Qt 6.11.1 · Qt Help · 来自 `QCompressedHelpInfo`

## 1. 先建立直觉

`QCompressedHelpInfo` 是 `.qch` 压缩帮助文件的轻量元信息。它不加载全部文档内容，只读取帮助文件声明的 namespace、component 和 version，适合在注册前做检查和展示。

## 2. 类说明

保留类说明：这些 API 来自 `QCompressedHelpInfo`，属于 Qt Help 模块，用于读取压缩帮助文件的身份信息。

`.qch` 是单个文档包，`.qhc` 是 collection 文件，负责登记多个 `.qch`。这个类只关心 `.qch` 自己是谁。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `fromCompressedHelpFile(file)` | 从 `.qch` 文件读取元信息。 |
| `namespaceName()` | 返回帮助包 namespace，是注册和资源定位的核心身份。 |
| `component()` | 返回组件名，用于过滤和分类。 |
| `version()` | 返回版本号。 |
| `isNull()` | 判断读取是否失败或对象为空。 |
| 拷贝/移动/赋值/swap | 值类型操作。 |

## 4. 典型流程

```cpp
QCompressedHelpInfo info =
    QCompressedHelpInfo::fromCompressedHelpFile("qtwidgets.qch");
if (!info.isNull())
    qDebug() << info.namespaceName() << info.component() << info.version();
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 注册前校验 qch | 先读 namespace，避免重复或错误包。 |
| 插件帮助包管理 | 展示组件和版本。 |
| 自动更新帮助文档 | 对比 version 决定是否替换。 |

## 6. 常见坑与经验

namespace 是帮助包身份，不是文件名。改了文件名不代表 namespace 变化；注册冲突通常看 namespace。

`isNull()` 必须检查。文件不存在、不是合法 qch、版本不兼容都可能读不到信息。

## 7. 知识点覆盖

- `.qch` 元信息读取。
- namespace/component/version 的意义。
- `.qch` 与 `.qhc` 的分工。
