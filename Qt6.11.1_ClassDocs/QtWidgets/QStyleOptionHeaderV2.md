# QStyleOptionHeaderV2

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionHeaderV2`

## 1. 先建立直觉

`QStyleOptionHeaderV2` 是 header style option 的版本化兼容类型。它表示 `QStyleOptionHeader` 发展过程中的一个扩展版本。

在现代代码里，通常直接使用 `QStyleOptionHeader`。遇到 V2 名称时，把它理解成“为了二进制/源码兼容保留的 header option 版本”即可。

## 2. 类说明

`QStyleOptionHeaderV2` 继承自 `QStyleOptionHeader`。它服务 style 系统的版本识别，让旧 style 或旧代码能按预期读取字段。

写新控件和新 delegate 时，应优先参考当前 `QStyleOptionHeader` 文档。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStyleOptionHeaderV2()` | 创建 V2 header option。 |
| `QStyleOptionHeader` 继承字段 | 包括 text、icon、section、sortIndicator、position 等。 |
| `version` | 标识该 option 版本。 |
| `type` | 标识 option 类型。 |
| `qstyleoption_cast` | style 实现中安全识别 option 类型/版本。 |

## 4. 关键用法

新代码一般这样写：

```cpp
QStyleOptionHeader opt;
opt.initFrom(header);
```

只有维护旧接口或兼容代码时才会显式看到 V2。

## 5. 使用场景

适合维护旧 style、旧 Qt 迁移、理解历史生成文档中的 API。

普通业务开发不需要主动使用它。

## 6. 常见坑与经验

不要因为看到 V2 就以为功能更强。版本化类往往是兼容层，不是推荐新接口。

style 实现中应通过类型和版本谨慎读取字段，避免把旧 option 当新结构使用。

迁移文档时可以把重点放在 `QStyleOptionHeader` 的语义上。
