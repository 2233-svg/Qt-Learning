# QHelpFilterEngine
> Qt 6.11.1 · Qt Help · 来自 `QHelpFilterEngine`

## 1. 先建立直觉

`QHelpFilterEngine` 管理帮助系统里的过滤器：有哪些过滤器、当前激活哪个、每个过滤器包含哪些组件/版本，以及过滤后可见哪些 namespace、索引项。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpFilterEngine`，属于 Qt Help 模块，用于管理 Qt Help 文档过滤器。

它通常通过 `QHelpEngineCore::filterEngine()` 获取，不需要自己单独创建。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `filters()` | 列出过滤器名称。 |
| `activeFilter()` / `setActiveFilter()` | 查询或切换当前过滤器。 |
| `filterData(name)` / `setFilterData(name, data)` | 读取或保存过滤条件。 |
| `removeFilter(name)` | 删除过滤器。 |
| `availableComponents()` / `availableVersions()` | 查询已注册文档提供的组件和版本。 |
| `namespaceToComponent()` / `namespaceToVersion()` | 查询 namespace 到组件/版本的映射。 |
| `namespacesForFilter(name)` | 查询某过滤器匹配的 namespace。 |
| `indices()` / `indices(filterName)` | 查询过滤后的索引关键词。 |
| `filterActivated(newFilter)` | 当前过滤器改变时发出。 |

## 4. 典型流程

```cpp
auto *filters = helpEngine->filterEngine();
QHelpFilterData data;
data.setComponents({"widgets"});
filters->setFilterData("Widgets Only", data);
filters->setActiveFilter("Widgets Only");
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 产品版本切换 | 每个版本一个 filter。 |
| 模块文档筛选 | 只显示当前模块 component。 |
| 自定义帮助侧栏 | 根据 `filters()` 做下拉框。 |
| 搜索范围控制 | active filter 影响搜索和索引结果。 |

## 6. 常见坑与经验

修改过滤器后，内容树、索引和搜索结果可能需要刷新或重新查询。只切换 active filter 不代表你的 UI 已自动更新所有状态。

namespace、component、version 三者别混：namespace 是文档包身份，component/version 是过滤条件。

## 7. 知识点覆盖

- 帮助过滤器命名和激活。
- 组件/版本到 namespace 的映射。
- 过滤对索引、搜索、内容可见性的影响。
