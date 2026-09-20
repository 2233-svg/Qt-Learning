# QHelpFilterSettingsWidget
> Qt 6.11.1 · Qt Help · 来自 `QHelpFilterSettingsWidget`

## 1. 先建立直觉

`QHelpFilterSettingsWidget` 是帮助过滤器的现成设置界面。它让用户编辑过滤器名称、组件和版本选择，并把结果同步到 `QHelpFilterEngine`。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpFilterSettingsWidget`，属于 Qt Help 模块，用于提供帮助过滤设置 UI。

它是 QWidget，适合放在偏好设置对话框或帮助中心设置页中。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpFilterSettingsWidget(parent)` | 创建过滤设置控件。 |
| `readSettings(filterEngine)` | 从过滤引擎读取当前过滤器配置到界面。 |
| `applySettings(filterEngine)` | 把界面上的修改写回过滤引擎。 |
| `filterActivated(filter)` | 用户在界面中激活过滤器时通知。 |

## 4. 典型流程

```cpp
auto *widget = new QHelpFilterSettingsWidget(this);
widget->readSettings(helpEngine->filterEngine());

if (dialog.exec() == QDialog::Accepted)
    widget->applySettings(helpEngine->filterEngine());
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 帮助中心设置页 | 允许用户选择显示哪些组件/版本。 |
| IDE/工具文档过滤 | 项目切换时应用不同 filter。 |
| 管理多个 qch 包 | 给用户一个可视化过滤配置入口。 |

## 6. 常见坑与经验

读取和应用是两个动作。用户改了界面但没有 `applySettings()`，filter engine 不会改变。

设置改变后，要考虑刷新内容树、索引和搜索结果，否则用户会看到旧过滤状态。

## 7. 知识点覆盖

- 帮助过滤设置 UI。
- settings widget 与 filter engine 的读写关系。
- 配置应用后的 UI 刷新。
