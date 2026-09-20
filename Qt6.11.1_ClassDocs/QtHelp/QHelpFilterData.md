# QHelpFilterData
> Qt 6.11.1 · Qt Help · 来自 `QHelpFilterData`

## 1. 先建立直觉

`QHelpFilterData` 是一个帮助过滤器的条件数据：允许哪些 component、哪些 version。过滤器本身有名字，名字和这份条件数据由 `QHelpFilterEngine` 管理。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpFilterData`，属于 Qt Help 模块，用于保存帮助过滤条件。

它是可拷贝值类型，只保存条件，不执行过滤。真正根据条件筛选 namespace、索引和文件的是帮助引擎。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `components()` / `setComponents()` | 读取或设置允许的组件列表。 |
| `versions()` / `setVersions()` | 读取或设置允许的版本列表。 |
| 拷贝/移动/赋值/swap | 值类型操作。 |

## 4. 典型流程

```cpp
QHelpFilterData data;
data.setComponents({"designer", "widgets"});
data.setVersions({QVersionNumber(6, 11)});
engine->filterEngine()->setFilterData("Qt Widgets", data);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 按产品组件过滤文档 | components 放产品/模块名。 |
| 按版本过滤文档 | versions 放可见版本。 |
| 保存用户过滤方案 | filter name + filter data。 |

## 6. 常见坑与经验

component/version 来自 qch 元数据。过滤器里写了不存在的组件或版本，不会凭空匹配文档。

过滤器是展示和检索范围控制，不是权限系统。不要用它保护敏感文档。

## 7. 知识点覆盖

- Qt Help filter 条件数据。
- component 和 version 匹配。
- 数据对象与 filter engine 的分工。
